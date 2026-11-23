"""Fecha o lote de reservas da pousada num único comando.

Uso, a partir da raiz do repositório:

    python run_pipeline.py
    python run_pipeline.py --offline
    python run_pipeline.py --input-dir data/raw/invalid_example
"""

import argparse
import json
import logging
import shutil
import sys
import traceback
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from pipeline.api import ExternalDataError, acquire_holidays
from pipeline.batch import (
    acquire_bookings,
    check_october_reference,
    price_bookings,
    store_results,
)
from pipeline.integrate import IntegrationError, build_holiday_sheet, concentration_stats, integrate_bookings
from pipeline.report import build_report
from pipeline.rules import ReconciliationError
from pipeline.validate import BatchRejected, validate_batch

TZ = ZoneInfo("America/Sao_Paulo")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Fechamento em lote da pousada (ST4 e ST5).")
    parser.add_argument("--input-dir", default="data/raw", help="Pasta com os CSV de reservas. Não entra em subpastas.")
    parser.add_argument("--offline", action="store_true", help="Não consulta a BrasilAPI; usa o último JSON salvo.")
    parser.add_argument("--output-root", default="output", help="Pasta onde cada execução cria run_<id>.")
    parser.add_argument("--log-dir", default="logs", help="Pasta dos logs, um arquivo por execução.")
    parser.add_argument("--external-dir", default="data/external", help="Cache bruto dos feriados.")
    return parser.parse_args(argv)


def command_line(args):
    parts = ["python run_pipeline.py"]
    if args.input_dir != "data/raw":
        parts.extend(["--input-dir", args.input_dir])
    if args.offline:
        parts.append("--offline")
    if args.output_root != "output":
        parts.extend(["--output-root", args.output_root])
    if args.log_dir != "logs":
        parts.extend(["--log-dir", args.log_dir])
    if args.external_dir != "data/external":
        parts.extend(["--external-dir", args.external_dir])
    return " ".join(parts)


def new_run_id(output_root, log_dir):
    stamp = datetime.now(TZ).strftime("%Y%m%dT%H%M%S")
    run_id = stamp
    suffix = 2
    while _run_id_taken(output_root, log_dir, run_id):
        run_id = f"{stamp}-{suffix}"
        suffix += 1
    return run_id


def _run_id_taken(output_root, log_dir, run_id):
    return any(
        path.exists()
        for path in (
            output_root / f"run_{run_id}",
            output_root / f".tmp_{run_id}",
            log_dir / f"run_{run_id}.log",
        )
    )


def setup_logger(log_path):
    logger = logging.getLogger("pousada.pipeline")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False
    handler = logging.FileHandler(log_path, mode="x", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    formatter.converter = lambda timestamp: datetime.fromtimestamp(timestamp, TZ).timetuple()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger, handler


def write_status(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def execute(args):
    output_root = Path(args.output_root)
    log_dir = Path(args.log_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    run_id = new_run_id(output_root, log_dir)
    started_at = datetime.now(TZ).isoformat(timespec="seconds")
    log_path = log_dir / f"run_{run_id}.log"
    logger, handler = setup_logger(log_path)
    status_path = output_root / "latest_status.json"
    source_mode = None
    file_names = []
    command = command_line(args)
    tmp_dir = output_root / f".tmp_{run_id}"
    run_dir = output_root / f"run_{run_id}"

    try:
        logger.info("run_id=%s comando=%s", run_id, command)
        logger.info("passo=aquisicao diretorio=%s", args.input_dir)
        raw, files = acquire_bookings(args.input_dir)
        file_names = [path.name for path in files]
        for path in files:
            logger.info("arquivo=%s", path.name)
        logger.info("linhas_lidas=%s", len(raw))

        clean, incomplete = validate_batch(raw, logger)
        detail = price_bookings(clean, run_id)
        logger.info("passo=regras reservas=%s", len(detail))
        conference = check_october_reference(detail)
        if conference is None:
            logger.info("conferencia_outubro=nao_aplicavel")
        else:
            logger.info(
                "conferencia_outubro=ok reservas=%s diarias=%s ocupacao=%s liquida=%s comissao=%s",
                conference["bookings"],
                conference["nights"],
                conference["occupancy_percent"],
                conference["net_revenue"],
                conference["commission"],
            )

        years = sorted({value.year for value in detail["checkin"]})
        logger.info("passo=feriados anos=%s offline=%s", years, bool(args.offline))
        holidays, external_meta = acquire_holidays(
            years,
            Path(args.external_dir),
            offline=bool(args.offline),
            logger=logger,
        )
        source_mode = external_meta["source_mode"]

        logger.info("passo=integracao source_mode=%s", source_mode)
        integrated, checks = integrate_bookings(detail, holidays, run_id)
        logger.info(
            "integracao reservas=%s/%s diarias=%s/%s liquida_antes=%.2f liquida_depois=%.2f "
            "cardinalidade=%s sem_feriado=%s com_feriado=%s",
            checks["bookings_before"],
            checks["bookings_after"],
            checks["nights_before"],
            checks["nights_after"],
            checks["net_before"],
            checks["net_after"],
            checks["cardinality"],
            checks["unmatched_nights"],
            checks["matched_holiday_nights"],
        )
        holiday_sheet = build_holiday_sheet(detail, integrated, holidays, run_id)
        concentration = concentration_stats(detail, integrated, holidays)

        run_info = {
            "run_id": run_id,
            "started_at": started_at,
            "command": command,
            "files": file_names,
            "output_dir": str(run_dir),
            "log_file": str(log_path),
        }
        report_text = build_report(
            detail,
            incomplete,
            integrated,
            holidays,
            external_meta,
            checks,
            conference,
            concentration,
            run_info,
        )
        logger.info("passo=armazenamento pasta=%s", run_dir)
        written = store_results(tmp_dir, detail, incomplete, integrated, holiday_sheet, report_text, conference)
        tmp_dir.rename(run_dir)
        logger.info("arquivos_gravados=%s", ",".join(written))
        logger.info("passo=fim status=sucesso source_mode=%s", source_mode)
        finished_at = datetime.now(TZ).isoformat(timespec="seconds")
        write_status(
            status_path,
            {
                "run_id": run_id,
                "status": "sucesso",
                "source_mode": source_mode,
                "started_at": started_at,
                "finished_at": finished_at,
                "input_dir": args.input_dir,
                "files": file_names,
                "output_dir": str(run_dir),
                "log_file": str(log_path),
                "message": "Fechamento concluído.",
            },
        )
        print(f"Execução {run_id} concluída.")
        print("Status: sucesso")
        print(f"Modo da fonte externa: {source_mode}")
        print(f"Pasta: {run_dir}")
        print(f"Log: {log_path}")
        print(f"Última execução: {status_path}")
        if conference is not None:
            print(
                "Outubro/2026: "
                f"{conference['bookings']} reservas, {conference['nights']} diárias, "
                f"ocupação {conference['occupancy_percent']}%, "
                f"líquida {conference['net_revenue']}, comissão {conference['commission']}."
            )
        return 0
    except (BatchRejected, ExternalDataError, IntegrationError, ReconciliationError) as exc:
        logger.error("passo=fim status=falha")
        logger.error("%s", exc)
        finished_at = datetime.now(TZ).isoformat(timespec="seconds")
        write_status(
            status_path,
            {
                "run_id": run_id,
                "status": "falha",
                "source_mode": source_mode,
                "started_at": started_at,
                "finished_at": finished_at,
                "input_dir": args.input_dir,
                "files": file_names,
                "output_dir": None,
                "log_file": str(log_path),
                "message": str(exc),
            },
        )
        if tmp_dir.exists() and not run_dir.exists():
            shutil.rmtree(tmp_dir)
        print(str(exc))
        print("Status: falha")
        print(f"Execução {run_id}")
        print(f"Log: {log_path}")
        print(f"Última execução: {status_path}")
        return 1
    except Exception:
        logger.error("passo=fim status=falha")
        logger.error("%s", traceback.format_exc())
        finished_at = datetime.now(TZ).isoformat(timespec="seconds")
        write_status(
            status_path,
            {
                "run_id": run_id,
                "status": "falha",
                "source_mode": source_mode,
                "started_at": started_at,
                "finished_at": finished_at,
                "input_dir": args.input_dir,
                "files": file_names,
                "output_dir": None,
                "log_file": str(log_path),
                "message": "Falha inesperada. O detalhe está no log.",
            },
        )
        if tmp_dir.exists() and not run_dir.exists():
            shutil.rmtree(tmp_dir)
        print("Falha inesperada. O detalhe está no log.")
        print("Status: falha")
        print(f"Execução {run_id}")
        print(f"Log: {log_path}")
        return 1
    finally:
        handler.close()
        logger.handlers.clear()


def main(argv=None):
    return execute(parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
