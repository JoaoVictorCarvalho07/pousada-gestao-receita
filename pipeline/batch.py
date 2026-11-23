"""Aquisição dos CSV e armazenamento das saídas do fechamento.

Os arquivos em data/raw são só lidos. Cada execução grava uma pasta nova.
"""

from pathlib import Path

import pandas as pd

from pipeline.rules import (
    OCTOBER_REFERENCE,
    ReconciliationError,
    available_room_nights,
    calculate_booking,
)
from pipeline.spreadsheet import build_workbook
from pipeline.validate import REQUIRED_COLUMNS, BatchRejected


def acquire_bookings(input_dir):
    """Lê todos os CSV compatíveis de uma pasta (sem entrar em subpastas)."""
    folder = Path(input_dir)
    if not folder.is_dir():
        raise BatchRejected([f"Pasta de entrada não encontrada: {folder}."])

    files = sorted(path for path in folder.glob("*.csv") if path.is_file())
    if not files:
        raise BatchRejected([f"Nenhum CSV em {folder}. O lote foi rejeitado."])

    frames = []
    for path in files:
        frame = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
        frame.columns = [str(column).strip() for column in frame.columns]
        missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
        if missing:
            listed = ", ".join(missing)
            raise BatchRejected(
                [
                    f"{path.name} não tem as colunas obrigatórias ({listed}). "
                    "Arquivo incompatível rejeita o lote inteiro."
                ]
            )
        frame = frame[REQUIRED_COLUMNS].copy()
        for column in REQUIRED_COLUMNS:
            frame[column] = frame[column].map(lambda value: str(value).strip())
        frame["source_file"] = path.name
        frames.append(frame)

    return pd.concat(frames, ignore_index=True), files


def price_bookings(clean, run_id):
    """Aplica calculate_booking em cada reserva já validada."""
    rows = []
    for record in clean.itertuples(index=False):
        values = calculate_booking(
            {
                "room": int(record.room),
                "nights": int(record.nights),
                "guests": int(record.guests),
                "channel": record.channel,
            }
        )
        rows.append(
            {
                "source_file": record.source_file,
                "run_id": run_id,
                "booking_id": record.booking_id,
                "guest": record.guest,
                "channel": record.channel,
                "room": int(record.room),
                "room_type": values.pop("room_type"),
                "checkin": record.checkin,
                "nights": int(record.nights),
                "guests": int(record.guests),
                **values,
            }
        )
    return pd.DataFrame(rows)


def check_october_reference(detail):
    """Confere o arquivo canônico de outubro com o fechamento conhecido.

    Se o arquivo não está no lote, a conferência não se aplica. Se está e os
    totais divergem, a execução falha em vez de publicar um número errado.
    """
    part = detail[detail["source_file"] == OCTOBER_REFERENCE["source_file"]]
    if part.empty:
        return None

    outside = [
        record.booking_id
        for record in part.itertuples(index=False)
        if record.checkin.year != OCTOBER_REFERENCE["year"] or record.checkin.month != OCTOBER_REFERENCE["month"]
    ]
    nights = int(part["nights"].sum())
    calculated = {
        "bookings": int(len(part)),
        "nights": nights,
        "occupancy_percent": round(nights / available_room_nights(2026, 10) * 100, 1),
        "net_revenue": round(float(part["net_revenue"].sum()), 2),
        "commission": round(float(part["commission_amount"].sum()), 2),
    }
    mismatches = []
    if outside:
        mismatches.append("há reservas fora de outubro/2026: " + ", ".join(outside))
    labels = {
        "bookings": "reservas",
        "nights": "diárias",
        "occupancy_percent": "ocupação (%)",
        "net_revenue": "receita líquida",
        "commission": "comissão",
    }
    for key, label in labels.items():
        expected = OCTOBER_REFERENCE[key]
        if calculated[key] != expected:
            mismatches.append(f"{label}: calculado {calculated[key]} e esperado {expected}")
    if mismatches:
        detail_text = "\n- ".join(mismatches)
        raise ReconciliationError(f"A conferência de outubro/2026 falhou.\n- {detail_text}")
    return calculated


def _csv_ready(detail):
    ready = detail.copy()
    ready["checkin"] = ready["checkin"].map(lambda value: value.isoformat())
    return ready


def store_results(run_dir, detail, incomplete, integrated, holiday_sheet, report_text, conference):
    """Grava CSV processados, CSV integrado, planilha e relatório numa pasta nova."""
    folder = Path(run_dir)
    folder.mkdir(parents=True, exist_ok=False)
    written = []

    for source_file, part in detail.groupby("source_file", sort=True):
        destination = folder / f"processado_{source_file}"
        _csv_ready(part).to_csv(destination, index=False, encoding="utf-8")
        written.append(destination.name)

    if len(incomplete):
        incomplete_path = folder / "incompletas.csv"
        incomplete.to_csv(incomplete_path, index=False, encoding="utf-8")
        written.append(incomplete_path.name)

    integrated_path = folder / "integrado_noites.csv"
    integrated.to_csv(integrated_path, index=False, encoding="utf-8")
    written.append(integrated_path.name)

    workbook_path = folder / "fechamento_pousada.xlsx"
    build_workbook(workbook_path, detail, holiday_sheet, conference)
    written.append(workbook_path.name)

    report_path = folder / "report.md"
    report_path.write_text(report_text, encoding="utf-8")
    written.append(report_path.name)
    return written
