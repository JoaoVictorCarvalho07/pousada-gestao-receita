"""Planilha do fechamento: Detalhe, Resumo de negócio e Feriados.

Os valores monetários e as quantidades são números. O formato da célula só
controla a aparência.
"""

from datetime import date, datetime
from numbers import Number
from pathlib import Path

import pandas as pd
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

from pipeline.rules import OCTOBER_REFERENCE, available_room_nights

CURRENCY = '"R$" #,##0.00'
DATE_FORMAT = "yyyy-mm-dd"
INTEGER = "0"
ONE_DECIMAL = "0.0"

HEADER_FILL = PatternFill("solid", fgColor="1F4E79")
HEADER_FONT = Font(bold=True, color="FFFFFF", name="Calibri", size=11)
TITLE_FONT = Font(bold=True, color="1F4E79", name="Calibri", size=12)
THIN = Border(
    left=Side(style="thin", color="D9E2F3"),
    right=Side(style="thin", color="D9E2F3"),
    top=Side(style="thin", color="D9E2F3"),
    bottom=Side(style="thin", color="D9E2F3"),
)
PREFERRED_WIDTH = {
    "Arquivo de origem": 28,
    "Id da execução": 20,
    "Hóspede": 22,
    "Canal": 18,
    "Tipo de quarto": 16,
    "Check-in": 14,
    "Data": 14,
    "Nome": 36,
    "Dia da semana": 16,
    "Classe": 12,
    "Indicador": 22,
}

DETAIL_COLUMNS = [
    ("source_file", "Arquivo de origem", None),
    ("run_id", "Id da execução", None),
    ("booking_id", "Reserva", None),
    ("guest", "Hóspede", None),
    ("channel", "Canal", None),
    ("room", "Quarto", INTEGER),
    ("room_type", "Tipo de quarto", None),
    ("checkin", "Check-in", DATE_FORMAT),
    ("nights", "Noites", INTEGER),
    ("guests", "Hóspedes", INTEGER),
    ("nightly_rate", "Diária (R$)", CURRENCY),
    ("room_charges", "Diárias do quarto (R$)", CURRENCY),
    ("extra_guest_charge", "Hóspede extra (R$)", CURRENCY),
    ("discount_percentage", "Desconto estadia (%)", ONE_DECIMAL),
    ("discount_amount", "Desconto (R$)", CURRENCY),
    ("accommodation_total", "Hospedagem (R$)", CURRENCY),
    ("tourism_tax_total", "Taxa de turismo (R$)", CURRENCY),
    ("amount_paid", "Valor pago (R$)", CURRENCY),
    ("commission_percentage", "Comissão (%)", ONE_DECIMAL),
    ("commission_amount", "Comissão (R$)", CURRENCY),
    ("breakfast_cost", "Café da manhã (R$)", CURRENCY),
    ("cleaning_fee", "Limpeza (R$)", CURRENCY),
    ("net_revenue", "Receita líquida (R$)", CURRENCY),
]

SUMMARY_COLUMNS = [
    ("month", "Mês", None),
    ("channel", "Canal", None),
    ("bookings", "Reservas", INTEGER),
    ("nights", "Diárias", INTEGER),
    ("amount_paid", "Valor pago (R$)", CURRENCY),
    ("commission_amount", "Comissão (R$)", CURRENCY),
    ("net_revenue", "Receita líquida (R$)", CURRENCY),
    ("retained", "Percentual retido (%)", ONE_DECIMAL),
]

HOLIDAY_COLUMNS = [
    ("run_id", "Id da execução", None),
    ("night_date", "Data", DATE_FORMAT),
    ("weekday", "Dia da semana", None),
    ("holiday_name", "Nome", None),
    ("holiday_type", "Tipo", None),
    ("classe", "Classe", None),
    ("in_period", "No período", None),
    ("occupied_nights", "Diárias ocupadas", INTEGER),
    ("available_rooms", "Quartos disponíveis", INTEGER),
    ("occupancy_percent", "Ocupação (%)", ONE_DECIMAL),
    ("net_revenue", "Receita líquida rateada (R$)", CURRENCY),
]

MONTH_HEADERS = [
    "Mês",
    "Reservas",
    "Diárias",
    "Diárias disponíveis",
    "Ocupação (%)",
    "Valor pago (R$)",
    "Comissão (R$)",
    "Receita líquida (R$)",
]
MONTH_FORMATS = {
    "Reservas": INTEGER,
    "Diárias": INTEGER,
    "Diárias disponíveis": INTEGER,
    "Ocupação (%)": ONE_DECIMAL,
    "Valor pago (R$)": CURRENCY,
    "Comissão (R$)": CURRENCY,
    "Receita líquida (R$)": CURRENCY,
}


def business_summary(detail):
    """Agrega mês e canal e ordena pela receita líquida, da maior para a menor."""
    frame = detail.copy()
    frame["month"] = frame["checkin"].map(lambda value: f"{value.year:04d}-{value.month:02d}")
    grouped = frame.groupby(["month", "channel"], as_index=False).agg(
        bookings=("booking_id", "count"),
        nights=("nights", "sum"),
        amount_paid=("amount_paid", "sum"),
        commission_amount=("commission_amount", "sum"),
        net_revenue=("net_revenue", "sum"),
    )
    grouped["retained"] = grouped.apply(
        lambda row: (row["net_revenue"] / row["amount_paid"] * 100) if row["amount_paid"] else 0.0,
        axis=1,
    )
    return grouped.sort_values(
        ["net_revenue", "month", "channel"],
        ascending=[False, True, True],
        kind="mergesort",
    ).reset_index(drop=True)


def month_summary(detail):
    rows = []
    frame = detail.copy()
    frame["year_month"] = frame["checkin"].map(lambda value: (value.year, value.month))
    for (year, month), part in frame.groupby("year_month", sort=True):
        nights = int(part["nights"].sum())
        available = available_room_nights(year, month)
        rows.append(
            {
                "month": f"{year:04d}-{month:02d}",
                "bookings": int(len(part)),
                "nights": nights,
                "available": available,
                "occupancy": nights / available * 100,
                "amount_paid": float(part["amount_paid"].sum()),
                "commission": float(part["commission_amount"].sum()),
                "net_revenue": float(part["net_revenue"].sum()),
            }
        )
    return (
        pd.DataFrame(rows)
        .sort_values("net_revenue", ascending=False, kind="mergesort")
        .reset_index(drop=True)
    )


def _view(frame, columns):
    view = frame[[field for field, _, _ in columns]].copy()
    view.columns = [header for _, header, _ in columns]
    return view


def _formats(columns):
    return {header: fmt for _, header, fmt in columns if fmt}


def _display_length(value):
    if isinstance(value, datetime):
        return 10
    return len(str(value))


def _apply_format(cell, fmt):
    if not fmt or cell.value is None:
        return
    if isinstance(cell.value, (datetime, date)) or (
        isinstance(cell.value, Number) and not isinstance(cell.value, bool)
    ):
        cell.number_format = fmt


def _style_header(ws, start_col, end_col, row=1):
    for col in range(start_col, end_col + 1):
        cell = ws.cell(row, col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 32


def _apply_body(ws, start_row, end_row, start_col, headers, formats):
    for col_offset, header in enumerate(headers):
        col = start_col + col_offset
        letter = get_column_letter(col)
        longest = len(str(header))
        fmt = formats.get(header)
        for row in range(start_row, end_row + 1):
            cell = ws.cell(row, col)
            cell.border = THIN
            cell.alignment = Alignment(vertical="center")
            _apply_format(cell, fmt)
            if cell.value is not None:
                longest = max(longest, min(_display_length(cell.value), 36))
        width = max(PREFERRED_WIDTH.get(header, 12), longest + 2)
        ws.column_dimensions[letter].width = min(width, 42)


def _prepare_sheet(ws, n_cols, n_data_rows):
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(n_cols)}{n_data_rows + 1}"
    ws.print_title_rows = "1:1"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.horizontalCentered = True
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddHeader.left.text = "Pousada — fechamento"
    ws.oddFooter.right.text = "Página &P de &N"
    ws.page_setup.leftMargin = 0.4
    ws.page_setup.rightMargin = 0.4
    ws.sheet_view.zoomScale = 110


def _write_rows(ws, start_row, start_col, headers, rows, formats):
    for offset, header in enumerate(headers):
        ws.cell(start_row, start_col + offset, header)
    _style_header(ws, start_col, start_col + len(headers) - 1, row=start_row)
    for row_offset, values in enumerate(rows):
        for col_offset, value in enumerate(values):
            cell = ws.cell(start_row + 1 + row_offset, start_col + col_offset, value)
            _apply_format(cell, formats.get(headers[col_offset]))
            cell.border = THIN
            cell.alignment = Alignment(vertical="center")
    if rows:
        _apply_body(
            ws,
            start_row + 1,
            start_row + len(rows),
            start_col,
            headers,
            formats,
        )
    else:
        for offset, header in enumerate(headers):
            letter = get_column_letter(start_col + offset)
            ws.column_dimensions[letter].width = max(PREFERRED_WIDTH.get(header, 12), len(header) + 2)


def build_workbook(path, detail, holiday_sheet, conference):
    """Gera o xlsx a partir do mesmo detalhe validado que alimenta CSV e relatório."""
    detail_view = _view(detail, DETAIL_COLUMNS)
    detail_view["Check-in"] = pd.to_datetime(detail_view["Check-in"])

    summary = business_summary(detail)
    summary_view = _view(summary, SUMMARY_COLUMNS)

    holiday_view = _view(holiday_sheet, HOLIDAY_COLUMNS)
    holiday_view["Data"] = pd.to_datetime(holiday_view["Data"])
    for column in ("Diárias ocupadas", "Quartos disponíveis", "Ocupação (%)", "Receita líquida rateada (R$)"):
        holiday_view[column] = holiday_view[column].astype(object).where(pd.notna(holiday_view[column]), None)

    destination = Path(path)
    with pd.ExcelWriter(destination, engine="openpyxl") as writer:
        detail_view.to_excel(writer, sheet_name="Detalhe", index=False)
        summary_view.to_excel(writer, sheet_name="Resumo de negócio", index=False)
        holiday_view.to_excel(writer, sheet_name="Feriados", index=False)

    workbook = load_workbook(destination)
    _finish_table(workbook["Detalhe"], DETAIL_COLUMNS)
    _finish_table(workbook["Resumo de negócio"], SUMMARY_COLUMNS)
    _finish_table(workbook["Feriados"], HOLIDAY_COLUMNS)
    _add_month_and_check(workbook["Resumo de negócio"], detail, conference)
    workbook.properties.title = "Fechamento da pousada"
    workbook.properties.subject = "Reservas validadas e feriados nacionais"
    workbook.properties.creator = "run_pipeline.py"
    workbook.save(destination)


def _finish_table(ws, columns):
    headers = [header for _, header, _ in columns]
    formats = _formats(columns)
    n_rows = ws.max_row - 1
    _style_header(ws, 1, len(headers))
    if n_rows > 0:
        _apply_body(ws, 2, n_rows + 1, 1, headers, formats)
    _prepare_sheet(ws, len(headers), n_rows)


def _add_month_and_check(ws, detail, conference):
    months = month_summary(detail)
    month_rows = [
        [
            row.month,
            int(row.bookings),
            int(row.nights),
            int(row.available),
            float(row.occupancy),
            float(row.amount_paid),
            float(row.commission),
            float(row.net_revenue),
        ]
        for row in months.itertuples(index=False)
    ]
    _write_rows(ws, 1, 10, MONTH_HEADERS, month_rows, MONTH_FORMATS)

    start = len(month_rows) + 4
    caption = ws.cell(start, 10, "Conferência de outubro/2026")
    caption.font = TITLE_FONT
    headers = ["Indicador", "Calculado", "Esperado", "Confere"]
    if conference is None:
        ws.cell(start + 1, 10, "O arquivo reservas_2026-10.csv não estava neste lote.")
        return

    rows = [
        ["Reservas", conference["bookings"], OCTOBER_REFERENCE["bookings"], "sim"],
        ["Diárias", conference["nights"], OCTOBER_REFERENCE["nights"], "sim"],
        ["Ocupação (%)", conference["occupancy_percent"], OCTOBER_REFERENCE["occupancy_percent"], "sim"],
        ["Receita líquida (R$)", conference["net_revenue"], OCTOBER_REFERENCE["net_revenue"], "sim"],
        ["Comissão (R$)", conference["commission"], OCTOBER_REFERENCE["commission"], "sim"],
    ]
    _write_rows(ws, start + 1, 10, headers, rows, {})
    integer_rows = (start + 2, start + 3)
    decimal_row = start + 4
    money_rows = (start + 5, start + 6)
    for row_index in integer_rows:
        ws.cell(row_index, 11).number_format = INTEGER
        ws.cell(row_index, 12).number_format = INTEGER
    ws.cell(decimal_row, 11).number_format = ONE_DECIMAL
    ws.cell(decimal_row, 12).number_format = ONE_DECIMAL
    for row_index in money_rows:
        ws.cell(row_index, 11).number_format = CURRENCY
        ws.cell(row_index, 12).number_format = CURRENCY
