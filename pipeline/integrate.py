"""Integra reservas validadas com o calendário de feriados.

Uma linha de reserva é uma hospedagem (um hóspede, um quarto, um check-in).
Uma linha de feriado é uma data nacional. A junção acontece na noite ocupada:
a reserva é expandida para uma linha por noite, e a chave é a data ISO.
"""

from calendar import monthrange
from datetime import date, timedelta

import pandas as pd

from pipeline.rules import N_ROOMS


class IntegrationError(Exception):
    """A junção mudou contagem ou total e por isso não foi publicada."""


def long_weekend_dates(holiday_dates):
    """Datas de feriado e de ponte / fim de semana prolongado.

    - Segunda: sábado, domingo e segunda.
    - Sexta: sexta, sábado e domingo.
    - Terça: sábado, domingo, segunda (ponte) e terça.
    - Quinta: quinta, sexta (ponte), sábado e domingo.
    - Quarta: só o feriado.
    - Sábado ou domingo: o fim de semana em que o feriado cai.

    A chave é a data ISO. O valor é o rótulo da regra que a incluiu.
    """
    labels = {}
    for iso in holiday_dates:
        day = date.fromisoformat(iso)
        weekday = day.weekday()
        if weekday == 0:
            extra = [day - timedelta(days=2), day - timedelta(days=1), day]
            label = "fim de semana prolongado (feriado na segunda)"
        elif weekday == 4:
            extra = [day, day + timedelta(days=1), day + timedelta(days=2)]
            label = "fim de semana prolongado (feriado na sexta)"
        elif weekday == 1:
            extra = [day - timedelta(days=3), day - timedelta(days=2), day - timedelta(days=1), day]
            label = "ponte (feriado na terça)"
        elif weekday == 3:
            extra = [day, day + timedelta(days=1), day + timedelta(days=2), day + timedelta(days=3)]
            label = "ponte (feriado na quinta)"
        elif weekday == 2:
            extra = [day]
            label = "feriado isolado (quarta)"
        elif weekday == 5:
            extra = [day, day + timedelta(days=1)]
            label = "feriado no fim de semana"
        else:
            extra = [day - timedelta(days=1), day]
            label = "feriado no fim de semana"
        for item in extra:
            labels.setdefault(item.isoformat(), label)
    return labels


def _shares(total, parts):
    if parts == 1:
        return [total]
    base = total / parts
    shares = [base] * (parts - 1)
    shares.append(total - sum(shares))
    return shares


def expand_bookings_to_nights(detail):
    """Uma linha por noite ocupada, do check-in inclusive até a véspera da saída."""
    rows = []
    for record in detail.itertuples(index=False):
        net_shares = _shares(float(record.net_revenue), int(record.nights))
        paid_shares = _shares(float(record.amount_paid), int(record.nights))
        for offset in range(int(record.nights)):
            night = record.checkin + timedelta(days=offset)
            rows.append(
                {
                    "run_id": record.run_id,
                    "source_file": record.source_file,
                    "booking_id": record.booking_id,
                    "guest": record.guest,
                    "channel": record.channel,
                    "room": int(record.room),
                    "room_type": record.room_type,
                    "night_date": night.isoformat(),
                    "night_index": offset + 1,
                    "guests": int(record.guests),
                    "net_revenue_night": net_shares[offset],
                    "amount_paid_night": paid_shares[offset],
                }
            )
    return pd.DataFrame(rows)


def integrate_bookings(detail, holidays, run_id):
    """Junção many-to-one pela data. Noite sem feriado permanece no resultado."""
    if holidays["date"].duplicated().any():
        raise IntegrationError("A data do feriado não é única. A junção foi cancelada.")

    nights = expand_bookings_to_nights(detail)
    holiday_side = holidays.rename(
        columns={"date": "night_date", "name": "holiday_name", "type": "holiday_type"}
    )
    merged = nights.merge(holiday_side, on="night_date", how="left", validate="many_to_one")
    labels = long_weekend_dates(holidays["date"].tolist())
    merged["is_holiday"] = merged["holiday_name"].notna()
    merged["is_long_weekend"] = merged["night_date"].map(lambda value: value in labels)
    merged["long_weekend_label"] = merged["night_date"].map(lambda value: labels.get(value, ""))
    merged["run_id"] = run_id

    if merged.duplicated(["booking_id", "night_date"]).any():
        raise IntegrationError("A chave (booking_id, night_date) ficou duplicada depois da expansão.")

    net_before = float(detail["net_revenue"].sum())
    net_after = float(merged["net_revenue_night"].sum())
    paid_before = float(detail["amount_paid"].sum())
    paid_after = float(merged["amount_paid_night"].sum())
    nights_before = int(detail["nights"].sum())
    nights_after = int(len(merged))
    bookings_before = int(detail["booking_id"].nunique())
    bookings_after = int(merged["booking_id"].nunique())

    problems = []
    if nights_before != nights_after:
        problems.append(f"diárias {nights_before} antes e {nights_after} depois")
    if bookings_before != bookings_after:
        problems.append(f"reservas {bookings_before} antes e {bookings_after} depois")
    if abs(net_before - net_after) > 1e-6:
        problems.append(f"receita líquida {net_before} antes e {net_after} depois")
    if abs(paid_before - paid_after) > 1e-6:
        problems.append(f"valor pago {paid_before} antes e {paid_after} depois")
    if problems:
        raise IntegrationError("A junção não preservou os totais: " + "; ".join(problems) + ".")

    holiday_dates = set(holidays["date"])
    matched_dates = set(merged.loc[merged["is_holiday"], "night_date"])
    checks = {
        "bookings_before": bookings_before,
        "bookings_after": bookings_after,
        "nights_before": nights_before,
        "nights_after": nights_after,
        "net_before": net_before,
        "net_after": net_after,
        "paid_before": paid_before,
        "paid_after": paid_after,
        "holiday_dates_unique": True,
        "night_key_unique": True,
        "cardinality": "many_to_one",
        "matched_holiday_nights": int(merged["is_holiday"].sum()),
        "unmatched_nights": int((~merged["is_holiday"]).sum()),
        "holidays_without_nights": int(len(holiday_dates - matched_dates)),
        "long_weekend_nights": int(merged["is_long_weekend"].sum()),
    }
    return merged, checks


WEEKDAYS = (
    "segunda-feira",
    "terça-feira",
    "quarta-feira",
    "quinta-feira",
    "sexta-feira",
    "sábado",
    "domingo",
)


def concentration_stats(detail, integrated, holidays):
    """Compara feriados/pontes com o restante do calendário dos meses do lote."""
    labels = long_weekend_dates(holidays["date"].tolist())
    months = sorted({(value.year, value.month) for value in detail["checkin"]})

    def summarize(day_list, night_frame):
        special = [day for day in day_list if day in labels]
        available = len(day_list) * N_ROOMS
        available_special = len(special) * N_ROOMS
        sold = int(len(night_frame))
        if sold:
            sold_special = int(night_frame["is_long_weekend"].sum())
            net = float(night_frame["net_revenue_night"].sum())
            net_special = float(night_frame.loc[night_frame["is_long_weekend"], "net_revenue_night"].sum())
        else:
            sold_special = 0
            net = 0.0
            net_special = 0.0
        other_available = available - available_special
        other_sold = sold - sold_special
        return {
            "calendar_days": len(day_list),
            "special_days": len(special),
            "special_dates": special,
            "baseline_share": (len(special) / len(day_list)) if day_list else 0.0,
            "sold_nights": sold,
            "sold_special": sold_special,
            "sold_share": (sold_special / sold) if sold else 0.0,
            "net": net,
            "net_special": net_special,
            "revenue_share": (net_special / net) if net else 0.0,
            "occupancy": (sold / available * 100) if available else 0.0,
            "occupancy_special": (sold_special / available_special * 100) if available_special else 0.0,
            "occupancy_other": (other_sold / other_available * 100) if other_available else 0.0,
            "available": available,
            "available_special": available_special,
        }

    by_month = []
    all_days = []
    for year, month in months:
        days = [date(year, month, day).isoformat() for day in range(1, monthrange(year, month)[1] + 1)]
        all_days.extend(days)
        prefix = f"{year:04d}-{month:02d}"
        month_nights = integrated[integrated["night_date"].str.startswith(prefix)]
        stats = summarize(days, month_nights)
        stats["month"] = prefix
        by_month.append(stats)
    overall = summarize(all_days, integrated)
    overall["month"] = "lote"
    return overall, by_month


def build_holiday_sheet(detail, integrated, holidays, run_id):
    """Uma linha por feriado do ano e por dia de ponte dentro dos meses do lote."""
    labels = long_weekend_dates(holidays["date"].tolist())
    months = {(value.year, value.month) for value in detail["checkin"]}
    names = dict(zip(holidays["date"], holidays["name"]))
    types = dict(zip(holidays["date"], holidays["type"]))
    dates = set(holidays["date"]) | {day for day in labels if date.fromisoformat(day).year in {year for year, _ in months}}
    # Pontes só entram se caírem num mês que o lote realmente fecha.
    dates = {day for day in dates if day in names or (date.fromisoformat(day).year, date.fromisoformat(day).month) in months}

    occupied = integrated.groupby("night_date").agg(
        occupied_nights=("booking_id", "count"),
        net_revenue=("net_revenue_night", "sum"),
    )

    rows = []
    for iso in sorted(dates):
        current = date.fromisoformat(iso)
        in_period = (current.year, current.month) in months
        if in_period and iso in occupied.index:
            nights = int(occupied.loc[iso, "occupied_nights"])
            net = float(occupied.loc[iso, "net_revenue"])
            occupancy = nights / N_ROOMS * 100
            available = N_ROOMS
        elif in_period:
            nights = 0
            net = 0.0
            occupancy = 0.0
            available = N_ROOMS
        else:
            nights = None
            net = None
            occupancy = None
            available = None
        rows.append(
            {
                "run_id": run_id,
                "night_date": current,
                "weekday": WEEKDAYS[current.weekday()],
                "holiday_name": names.get(iso, ""),
                "holiday_type": types.get(iso, ""),
                "classe": "Feriado" if iso in names else "Ponte",
                "in_period": "sim" if in_period else "não",
                "occupied_nights": nights,
                "available_rooms": available,
                "occupancy_percent": occupancy,
                "net_revenue": net,
            }
        )
    return pd.DataFrame(rows)
