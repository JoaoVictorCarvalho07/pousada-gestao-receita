"""Conferências do fechamento: outubro, rejeição do lote e feriados."""

import json
import subprocess
import sys
from numbers import Real
from pathlib import Path

import pandas as pd
import pytest
import requests
from openpyxl import load_workbook

import theme2
from pipeline.api import ExternalDataError, acquire_holidays, fetch_live, parse_holiday_payload
from pipeline.batch import acquire_bookings, price_bookings
from pipeline.integrate import integrate_bookings, long_weekend_dates
from pipeline.rules import OCTOBER_REFERENCE
from pipeline.validate import BatchRejected, validate_batch

ROOT = Path(__file__).resolve().parents[1]

VALID_HOLIDAYS = [
    {"date": "2026-01-01", "name": "Confraternização mundial", "type": "national"},
    {"date": "2026-04-21", "name": "Tiradentes", "type": "national"},
    {"date": "2026-05-01", "name": "Dia do Trabalho", "type": "national"},
    {"date": "2026-09-07", "name": "Independência do Brasil", "type": "national"},
    {"date": "2026-10-12", "name": "Nossa Senhora Aparecida", "type": "national"},
    {"date": "2026-11-02", "name": "Finados", "type": "national"},
    {"date": "2026-11-15", "name": "Proclamação da República", "type": "national"},
    {"date": "2026-12-25", "name": "Natal", "type": "national"},
]


def _october_detail():
    raw, _files = acquire_bookings(ROOT / "data" / "raw")
    clean, incomplete = validate_batch(raw)
    detail = price_bookings(clean, "teste")
    october = detail[detail["source_file"] == "reservas_2026-10.csv"].copy()
    return october, incomplete


def test_outubro_bate_com_o_fechamento_conhecido_e_com_theme2():
    october, incomplete = _october_detail()
    assert len(incomplete) == 0
    assert len(october) == OCTOBER_REFERENCE["bookings"]
    assert int(october["nights"].sum()) == OCTOBER_REFERENCE["nights"]
    assert round(float(october["net_revenue"].sum()), 2) == OCTOBER_REFERENCE["net_revenue"]
    assert round(float(october["commission_amount"].sum()), 2) == OCTOBER_REFERENCE["commission"]
    occupancy = round(int(october["nights"].sum()) / (8 * 31) * 100, 1)
    assert occupancy == OCTOBER_REFERENCE["occupancy_percent"]

    for record in october.itertuples(index=False):
        values = theme2.calculate_booking(
            {
                "guest": record.guest,
                "channel": record.channel,
                "room": int(record.room),
                "checkin": record.checkin.day,
                "nights": int(record.nights),
                "guests": int(record.guests),
            }
        )
        assert values["net_revenue"] == record.net_revenue
        assert values["commission_amount"] == record.commission_amount
        assert values["amount_paid"] == record.amount_paid


def test_taxa_de_turismo_nao_e_descontada_de_novo_da_receita_liquida():
    october, _incomplete = _october_detail()
    net = round(float(october["net_revenue"].sum()), 2)
    net_minus_tax = round(float((october["net_revenue"] - october["tourism_tax_total"]).sum()), 2)
    assert net == 27234.12
    assert net_minus_tax != 27234.12


def test_lote_invalido_rejeita_o_lote_inteiro(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "run_pipeline.py",
            "--input-dir",
            "data/raw/invalid_example",
            "--output-root",
            str(tmp_path / "output"),
            "--log-dir",
            str(tmp_path / "logs"),
            "--external-dir",
            str(tmp_path / "external"),
            "--offline",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "Lote rejeitado" in result.stdout
    assert "Instagram" in result.stdout
    assert "sobrepostas" in result.stdout
    assert list((tmp_path / "output").rglob("*.xlsx")) == []
    assert list((tmp_path / "output").glob("run_*")) == []
    log_text = next((tmp_path / "logs").glob("*.log")).read_text(encoding="utf-8")
    assert "incompletas=1" in log_text
    assert "status=falha" in log_text
    status = json.loads((tmp_path / "output" / "latest_status.json").read_text(encoding="utf-8"))
    assert status["status"] == "falha"


def test_canal_desconhecido_rejeita_sem_gravar_parcial():
    frame = pd.DataFrame(
        [
            {
                "booking_id": "X1",
                "guest": "Ana",
                "channel": "Instagram",
                "room": "1",
                "checkin": "2026-10-01",
                "nights": "1",
                "guests": "1",
                "source_file": "teste.csv",
            }
        ]
    )
    with pytest.raises(BatchRejected, match="Instagram"):
        validate_batch(frame)


def test_id_da_execucao_nao_reaproveita_log_existente(tmp_path):
    from run_pipeline import _run_id_taken

    log_dir = tmp_path / "logs"
    output_root = tmp_path / "output"
    log_dir.mkdir()
    output_root.mkdir()
    (log_dir / "run_20261123T151053.log").write_text("ja usado", encoding="utf-8")
    assert _run_id_taken(output_root, log_dir, "20261123T151053") is True
    assert _run_id_taken(output_root, log_dir, "20261123T151054") is False


def test_ponte_de_feriado_na_segunda():
    labels = long_weekend_dates(["2026-09-07"])
    assert set(labels) == {"2026-09-05", "2026-09-06", "2026-09-07"}


def test_integracao_preserva_totais_e_rastreio():
    raw, _files = acquire_bookings(ROOT / "data" / "raw")
    clean, _incomplete = validate_batch(raw)
    detail = price_bookings(clean, "teste")
    holidays = pd.DataFrame(VALID_HOLIDAYS)
    integrated, checks = integrate_bookings(detail, holidays, "teste")
    assert checks["nights_before"] == checks["nights_after"]
    assert checks["bookings_before"] == checks["bookings_after"]
    assert abs(checks["net_before"] - checks["net_after"]) < 1e-6
    assert abs(checks["paid_before"] - checks["paid_after"]) < 1e-6
    assert checks["cardinality"] == "many_to_one"
    assert integrated["source_file"].notna().all()
    assert (integrated["run_id"] == "teste").all()
    september_fifth = integrated[integrated["night_date"] == "2026-09-05"]
    assert len(september_fifth) > 0
    assert bool(september_fifth["is_long_weekend"].all())
    assert not bool(september_fifth["is_holiday"].any())


def test_json_de_feriado_invalido_e_recusado():
    with pytest.raises(ExternalDataError):
        parse_holiday_payload('{"date": "2026-01-01"}', 2026)
    with pytest.raises(ExternalDataError):
        parse_holiday_payload("[]", 2026)
    duplicated = list(VALID_HOLIDAYS) + [dict(VALID_HOLIDAYS[0])]
    with pytest.raises(ExternalDataError, match="repetidas"):
        parse_holiday_payload(json.dumps(duplicated), 2026)


def test_consulta_envia_params_e_timeout(monkeypatch):
    captured = {}

    class Response:
        status_code = 200
        text = json.dumps(VALID_HOLIDAYS)

        def raise_for_status(self):
            return None

    def fake_get(url, params=None, timeout=None, headers=None):
        captured["url"] = url
        captured["params"] = params
        captured["timeout"] = timeout
        return Response()

    monkeypatch.setattr(requests, "get", fake_get)
    body, status = fetch_live(2026, timeout=20)
    assert captured["params"] == {"year": 2026}
    assert captured["timeout"] == 20
    assert "/2026" in captured["url"]
    assert status == 200
    assert "2026-09-07" in body


def test_http_500_vira_erro_claro(monkeypatch):
    class Response:
        status_code = 500
        text = "erro"

        def raise_for_status(self):
            raise requests.HTTPError(response=self)

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: Response())
    with pytest.raises(ExternalDataError, match="HTTP 500"):
        fetch_live(2026, timeout=5)


def test_resposta_invalida_nao_apaga_o_cache(tmp_path, monkeypatch):
    raw_path = tmp_path / "feriados_2026.json"
    raw_path.write_text(json.dumps(VALID_HOLIDAYS), encoding="utf-8")
    meta_path = tmp_path / "feriados_2026.meta.json"
    meta_path.write_text(json.dumps({"retrieved_at": "2026-01-01T00:00:00-03:00"}), encoding="utf-8")

    class Response:
        status_code = 200
        text = '{"erro": true}'

        def raise_for_status(self):
            return None

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: Response())
    frame, meta = acquire_holidays([2026], tmp_path, offline=False)
    assert meta["source_mode"] == "cache"
    assert raw_path.read_text(encoding="utf-8") == json.dumps(VALID_HOLIDAYS)
    assert len(frame) == 8


def test_offline_nao_chama_a_rede(tmp_path, monkeypatch):
    (tmp_path / "feriados_2026.json").write_text(json.dumps(VALID_HOLIDAYS), encoding="utf-8")

    def fail_get(*args, **kwargs):
        raise AssertionError("não deveria chamar a rede")

    monkeypatch.setattr(requests, "get", fail_get)
    frame, meta = acquire_holidays([2026], tmp_path, offline=True)
    assert meta["source_mode"] == "cache"
    assert set(frame["date"]) >= {"2026-09-07", "2026-10-12"}


def test_pipeline_offline_grava_planilha_com_outubro(tmp_path):
    cache = ROOT / "data" / "external" / "feriados_2026.json"
    if not cache.exists():
        pytest.skip("cache da BrasilAPI ainda não foi gravado")
    result = subprocess.run(
        [
            sys.executable,
            "run_pipeline.py",
            "--offline",
            "--output-root",
            str(tmp_path / "output"),
            "--log-dir",
            str(tmp_path / "logs"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Status: sucesso" in result.stdout
    assert "Modo da fonte externa: cache" in result.stdout
    workbook_path = next((tmp_path / "output").rglob("*.xlsx"))
    report = next((tmp_path / "output").rglob("report.md")).read_text(encoding="utf-8")
    assert "R$ 27.234,12" in report
    assert "54,0%" in report
    assert "Evidência:" in report
    assert "Interpretação:" in report
    assert "Limitação" in report

    workbook = load_workbook(workbook_path)
    assert workbook.sheetnames == ["Detalhe", "Resumo de negócio", "Feriados"]
    detail = workbook["Detalhe"]
    summary = workbook["Resumo de negócio"]
    holidays = workbook["Feriados"]
    for sheet in (detail, summary, holidays):
        assert sheet.freeze_panes == "A2"
        assert sheet.auto_filter.ref.startswith("A1:")
    headers = [cell.value for cell in detail[1]]
    assert detail.cell(1, 1).font.bold is True
    checkin_column = headers.index("Check-in") + 1
    assert detail.cell(2, checkin_column).number_format == "yyyy-mm-dd"
    net_column = headers.index("Receita líquida (R$)") + 1
    assert "R$" in detail.cell(2, net_column).number_format
    assert isinstance(detail.cell(2, net_column).value, Real)
    assert not isinstance(detail.cell(2, net_column).value, bool)
    source_column = headers.index("Arquivo de origem") + 1
    nights_column = headers.index("Noites") + 1
    commission_column = headers.index("Comissão (R$)") + 1
    october_net = 0.0
    october_commission = 0.0
    october_nights = 0
    october_rows = 0
    for row in range(2, detail.max_row + 1):
        if detail.cell(row, source_column).value == "reservas_2026-10.csv":
            october_rows += 1
            october_nights += detail.cell(row, nights_column).value
            october_net += detail.cell(row, net_column).value
            october_commission += detail.cell(row, commission_column).value
    assert october_rows == 39
    assert october_nights == 134
    assert round(october_net, 2) == 27234.12
    assert round(october_commission, 2) == 3535.08

    summary_headers = [cell.value for cell in summary[1]]
    net_header = summary_headers.index("Receita líquida (R$)") + 1
    previous = None
    for row in range(2, 2 + 8):
        value = summary.cell(row, net_header).value
        assert isinstance(value, Real)
        assert not isinstance(value, bool)
        if previous is not None:
            assert value <= previous
        previous = value
