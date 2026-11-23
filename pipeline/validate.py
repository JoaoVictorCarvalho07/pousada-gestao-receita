"""Validação do lote de reservas.

Linha incompleta (campo obrigatório vazio) é separada e não entra no fechamento.
Linha completa com valor fora das regras rejeita o lote inteiro: não se publica
um fechamento parcial.
"""

import re
from datetime import datetime, timedelta

import pandas as pd

from pipeline.rules import CHANNELS, MAX_GUESTS, ROOMS

REQUIRED_COLUMNS = ["booking_id", "guest", "channel", "room", "checkin", "nights", "guests"]


class BatchRejected(Exception):
    """O lote inteiro foi recusado. Nenhuma saída de fechamento deve ser gravada."""

    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__(self.format_message())

    def format_message(self):
        lines = ["Lote rejeitado. Nenhuma saída de fechamento foi gerada."]
        for error in self.errors:
            lines.append(f"- {error}")
        return "\n".join(lines)


def separate_incomplete(raw):
    """Separa linhas com algum campo obrigatório vazio."""
    missing = raw.apply(
        lambda row: any(str(row[column]).strip() == "" for column in REQUIRED_COLUMNS),
        axis=1,
    )
    return raw.loc[~missing].copy(), raw.loc[missing].copy()


def _parse_int(text):
    if re.fullmatch(r"\d+", text):
        return int(text)
    return None


def _last_night(checkin, nights):
    return checkin + timedelta(days=nights - 1)


def apply_business_rules(complete):
    """Converte e confere as linhas completas. Erros acumulados rejeitam o lote."""
    errors = []
    duplicated = complete.loc[complete["booking_id"].duplicated(), "booking_id"].unique()
    if len(duplicated):
        listed = ", ".join(str(item) for item in duplicated)
        errors.append(f"booking_id repetido no lote: {listed}.")

    typed_rows = []
    for row in complete.itertuples(index=False):
        booking_id = row.booking_id
        room = _parse_int(row.room)
        nights = _parse_int(row.nights)
        guests = _parse_int(row.guests)
        try:
            checkin = datetime.strptime(row.checkin, "%Y-%m-%d").date()
        except ValueError:
            checkin = None

        if row.channel not in CHANNELS:
            accepted = ", ".join(CHANNELS)
            errors.append(
                f"Canal desconhecido em {booking_id}: \"{row.channel}\". Canais aceitos: {accepted}."
            )
        if room is None or room not in ROOMS:
            errors.append(f"Quarto inexistente em {booking_id}: \"{row.room}\". Os quartos vão de 1 a 8.")
        if guests is None or guests < 1 or guests > MAX_GUESTS:
            errors.append(
                f"Hóspedes fora do intervalo em {booking_id}: \"{row.guests}\". O quarto aceita de 1 a {MAX_GUESTS}."
            )
        if nights is None or nights < 1:
            errors.append(
                f"Noites fora do intervalo em {booking_id}: \"{row.nights}\". Use um inteiro a partir de 1."
            )
        if checkin is None:
            errors.append(f"Check-in inválido em {booking_id}: \"{row.checkin}\". Use AAAA-MM-DD.")

        if checkin is not None and nights is not None and nights >= 1:
            last_night = _last_night(checkin, nights)
            if last_night.year != checkin.year or last_night.month != checkin.month:
                errors.append(
                    f"A estadia de {booking_id} termina em {last_night.isoformat()}, fora do mês do check-in. "
                    "O fechamento mensal, como no theme2.py, não atravessa o mês."
                )

        if None not in (room, nights, guests, checkin) and room in ROOMS and nights >= 1 and 1 <= guests <= MAX_GUESTS:
            typed_rows.append(
                {
                    "booking_id": booking_id,
                    "guest": row.guest,
                    "channel": row.channel,
                    "room": room,
                    "checkin": checkin,
                    "nights": nights,
                    "guests": guests,
                    "source_file": row.source_file,
                }
            )

    _append_overlap_errors(typed_rows, errors)
    if errors:
        raise BatchRejected(errors)

    return pd.DataFrame(typed_rows)


def _append_overlap_errors(typed_rows, errors):
    for index, left in enumerate(typed_rows):
        left_end = left["checkin"] + timedelta(days=left["nights"])
        for right in typed_rows[index + 1 :]:
            if left["room"] != right["room"]:
                continue
            right_end = right["checkin"] + timedelta(days=right["nights"])
            if left["checkin"] < right_end and right["checkin"] < left_end:
                errors.append(
                    f"Quarto {left['room']} com estadias sobrepostas: "
                    f"{left['booking_id']} (check-in {left['checkin'].isoformat()}, {left['nights']} noites) e "
                    f"{right['booking_id']} (check-in {right['checkin'].isoformat()}, {right['nights']} noites)."
                )


def validate_batch(raw, logger=None):
    """Separa incompletas e rejeita o lote se alguma linha completa for inválida."""
    complete, incomplete = separate_incomplete(raw)
    if logger is not None:
        logger.info("passo=validacao completas=%s incompletas=%s", len(complete), len(incomplete))
        if len(incomplete):
            identifiers = incomplete["booking_id"].tolist()
            logger.info("incompletas_ids=%s", identifiers)
    if complete.empty:
        raise BatchRejected(
            [
                "Não há linhas completas para fechar. "
                "As linhas incompletas foram separadas e o lote inteiro foi rejeitado."
            ]
        )
    return apply_business_rules(complete), incomplete
