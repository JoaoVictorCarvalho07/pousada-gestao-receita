"""Relatório em texto do fechamento.

Os números saem do mesmo DataFrame validado que gera o CSV e a planilha.
A evidência (contagens e valores) fica separada da interpretação.
"""

from pipeline.integrate import concentration_stats
from pipeline.rules import N_ROOMS, available_room_nights


def brl(value):
    rounded = round(float(value), 2)
    text = f"{rounded:,.2f}"
    text = text.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {text}"


def pct(value, digits=1):
    rounded = round(float(value), digits)
    text = f"{rounded:.{digits}f}".replace(".", ",")
    return f"{text}%"


def _month_parts(detail):
    parts = []
    frame = detail.copy()
    frame["year_month"] = frame["checkin"].map(lambda value: (value.year, value.month))
    for (year, month), part in frame.groupby("year_month", sort=True):
        nights = int(part["nights"].sum())
        available = available_room_nights(year, month)
        paid = float(part["amount_paid"].sum())
        net = float(part["net_revenue"].sum())
        parts.append(
            {
                "label": f"{year:04d}-{month:02d}",
                "bookings": int(len(part)),
                "nights": nights,
                "available": available,
                "occupancy": nights / available * 100,
                "paid": paid,
                "commission": float(part["commission_amount"].sum()),
                "net": net,
                "retained": (net / paid * 100) if paid else 0.0,
            }
        )
    return parts


def _indicator_table(parts, total):
    header = "| Indicador | " + " | ".join(part["label"] for part in parts) + " | Lote |"
    separator = "| --- | " + " | ".join("---" for _ in parts) + " | --- |"
    rows = [
        ("Reservas", [str(part["bookings"]) for part in parts], str(total["bookings"])),
        ("Diárias vendidas", [str(part["nights"]) for part in parts], str(total["nights"])),
        ("Diárias disponíveis", [str(part["available"]) for part in parts], str(total["available"])),
        ("Ocupação", [pct(part["occupancy"]) for part in parts], pct(total["occupancy"])),
        ("Valor pago pelo hóspede", [brl(part["paid"]) for part in parts], brl(total["paid"])),
        ("Comissão dos canais", [brl(part["commission"]) for part in parts], brl(total["commission"])),
        ("Receita líquida", [brl(part["net"]) for part in parts], brl(total["net"])),
        ("Percentual retido", [pct(part["retained"]) for part in parts], pct(total["retained"])),
    ]
    lines = [header, separator]
    for name, values, overall in rows:
        lines.append("| " + " | ".join([name, *values, overall]) + " |")
    return "\n".join(lines)


def _total_from_parts(parts):
    nights = sum(part["nights"] for part in parts)
    available = sum(part["available"] for part in parts)
    paid = sum(part["paid"] for part in parts)
    net = sum(part["net"] for part in parts)
    return {
        "bookings": sum(part["bookings"] for part in parts),
        "nights": nights,
        "available": available,
        "occupancy": (nights / available * 100) if available else 0.0,
        "paid": paid,
        "commission": sum(part["commission"] for part in parts),
        "net": net,
        "retained": (net / paid * 100) if paid else 0.0,
    }


def _points(stats):
    baseline = stats["baseline_share"] * 100
    return stats["sold_share"] * 100 - baseline, stats["revenue_share"] * 100 - baseline


def _evidence_block(stats):
    dates = ", ".join(f"{iso[8:10]}/{iso[5:7]}" for iso in stats["special_dates"])
    return (
        f"- Mês {stats['month']}: {stats['special_days']} de {stats['calendar_days']} dias do calendário "
        f"são feriado ou ponte ({pct(stats['baseline_share'] * 100)}). Datas: {dates}. "
        f"Nesses dias caem {stats['sold_special']} de {stats['sold_nights']} diárias vendidas "
        f"({pct(stats['sold_share'] * 100)}) e {brl(stats['net_special'])} de {brl(stats['net'])} "
        f"da receita líquida rateada ({pct(stats['revenue_share'] * 100)}). "
        f"Ocupação nesses dias: {pct(stats['occupancy_special'])}. "
        f"Ocupação nos demais dias: {pct(stats['occupancy_other'])}."
    )


def _interpretation(overall, by_month):
    night_gap, revenue_gap = _points(overall)
    rate_gap = overall["occupancy_special"] - overall["occupancy_other"]
    concentrates = night_gap >= 2 and revenue_gap >= 2 and rate_gap > 0
    if concentrates:
        answer = (
            "Por esse critério, a resposta para o lote é sim: a fatia das diárias e a fatia da "
            "receita rateada superam o peso desses dias no calendário."
        )
    else:
        answer = (
            "Por esse critério, a resposta para o lote é não. A fatia das diárias e a fatia da "
            "receita rateada ficam perto do peso desses dias no calendário, sem folga de 2 pontos percentuais."
        )
    by_name = {item["month"]: item for item in by_month}
    month_notes = []
    for label in ("2026-09", "2026-10"):
        item = by_name.get(label)
        if item is None:
            continue
        nights, revenue = _points(item)
        nights_text = f"{nights:+.1f}".replace(".", ",")
        revenue_text = f"{revenue:+.1f}".replace(".", ",")
        month_notes.append(
            f"{label} fica {nights_text} pontos percentuais nas diárias e {revenue_text} na receita rateada, "
            "em relação ao calendário do mês."
        )
    october_note = ""
    october = by_name.get("2026-10")
    if october and "2026-10-31" in october["special_dates"]:
        october_note = (
            " Em outubro as datas especiais são 10, 11 e 12/10, a ponte de Nossa Senhora Aparecida "
            "(feriado numa segunda), e também 31/10: Finados em 2026 cai numa segunda, e a regra da ponte "
            "puxa o sábado anterior, que ainda é outubro."
        )
    rate_text = f"{abs(rate_gap):.1f}".replace(".", ",")
    direction = "acima" if rate_gap >= 0 else "abaixo"
    rate_sentence = (
        f"A ocupação nos dias especiais ficou {rate_text} pontos percentuais {direction} da ocupação dos outros dias."
    )
    if not concentrates:
        rate_sentence += " A taxa pode subir sem que o volume se afaste do calendário, porque esses dias são poucos."
    return (
        "Interpretação: chamo de concentração quando a fatia das diárias e a fatia da receita rateada "
        "superam, cada uma, a fatia do calendário em pelo menos 2 pontos percentuais, e a ocupação desses "
        f"dias também supera a dos demais. {answer} {rate_sentence} "
        + " ".join(month_notes)
        + october_note
        + " Setembro é um caderno fictício; outubro reproduz o theme2.py. Por isso a evidência está aberta por mês."
    )


def build_report(detail, incomplete, integrated, holidays, external_meta, checks, conference, concentration, run_info):
    parts = _month_parts(detail)
    total = _total_from_parts(parts)
    overall, by_month = concentration
    files = ", ".join(run_info["files"])
    incomplete_count = int(len(incomplete))
    meta_lines = []
    for meta in external_meta["by_year"]:
        params = meta.get("params", {})
        param_text = ", ".join(f"{key}={value}" for key, value in params.items()) or "nenhum"
        units = meta.get("units", {})
        unit_text = "; ".join(f"{key}: {value}" for key, value in units.items())
        meta_lines.append(
            "\n".join(
                [
                    f"- Provedor: {meta.get('provider', 'BrasilAPI')}",
                    f"- Endpoint: {meta.get('endpoint', '')}",
                    f"- Parâmetros: {param_text}",
                    f"- Coleta registrada no arquivo: {meta.get('retrieved_at', 'não informada')}",
                    f"- Modo nesta execução: {external_meta['source_mode']}",
                    f"- Registros: {meta.get('record_count', len(holidays))}",
                    f"- Unidades: {unit_text}",
                    f"- Termos de uso: {meta.get('terms_of_use', '')}",
                ]
            )
        )

    october_lines = ["O arquivo reservas_2026-10.csv não estava neste lote."]
    if conference is not None:
        october_lines = [
            "O arquivo reservas_2026-10.csv foi conferido contra o fechamento conhecido do theme2.py.",
            f"- Reservas: {conference['bookings']} (esperado 39) — confere",
            f"- Diárias: {conference['nights']} (esperado 134) — confere",
            f"- Ocupação: {pct(conference['occupancy_percent'])} (esperado 54,0%) — confere",
            f"- Receita líquida: {brl(conference['net_revenue'])} (esperado R$ 27.234,12) — confere",
            f"- Comissão: {brl(conference['commission'])} (esperado R$ 3.535,08) — confere",
        ]

    evidence = "\n".join(_evidence_block(stats) for stats in [*by_month, overall])
    interpretation = _interpretation(overall, by_month)
    same_base = (
        f"Reservas válidas no CSV processado e na aba Detalhe: {len(detail)}. "
        f"Noites no CSV integrado: {len(integrated)}. "
        f"Receita líquida do detalhe: {brl(total['net'])}. "
        f"Receita líquida depois da expansão das noites: {brl(checks['net_after'])}."
    )

    return f"""# Relatório de fechamento da pousada

## Execução

- Id da execução: {run_info["run_id"]}
- Início: {run_info["started_at"]}
- Comando: `{run_info["command"]}`
- Situação: sucesso
- Modo da fonte externa: {external_meta["source_mode"]}
- Pasta: {run_info["output_dir"]}
- Log: {run_info["log_file"]}

## Escopo

Tarefa recorrente: fechar a receita da pousada de {N_ROOMS} quartos a partir dos CSV de reservas exportados pela recepção. O usuário é quem opera a pousada e precisa de ocupação, comissão e receita líquida sem redigitar o mês. Entrada: um CSV por período, com o mesmo leiaute. Saída desta execução: CSV processado por arquivo, CSV de noites integradas aos feriados, planilha e este relatório.

Arquivos lidos: {files}.
Meses presentes: {", ".join(part["label"] for part in parts)}.
Os originais em data/raw não são alterados. Cada linha processada guarda o nome do arquivo de origem e o id desta execução.

## Validação

Três regras, com o motivo de cada uma:

1. Campo obrigatório vazio torna a linha incompleta. Ela sai do fechamento e, quando existe, vai para `incompletas.csv`. Motivo: completar hóspede, data ou noites no chute inventaria receita. Linha incompleta não é mostrada como reserva válida.
2. Canal, quarto, hóspedes e noites precisam cair no domínio do theme2.py: canais Booking, Airbnb, Own website e WhatsApp direct; quartos 1 a 8; 1 a 4 hóspedes; noites inteiras que terminam dentro do mês do check-in. Motivo: fora desse domínio não há tarifa nem comissão definidas. Um valor inválido rejeita o lote inteiro, para não publicar um fechamento parcial com cara de oficial.
3. `booking_id` não pode repetir e o mesmo quarto não pode ter duas estadias sobrepostas. Motivo: identificador repetido contaria a reserva duas vezes; sobreposição contaria a diária duas vezes e poderia levar a ocupação acima de 100% sem o quarto existir em dobro.

Nesta execução, linhas incompletas separadas: {incomplete_count}. Reservas válidas: {len(detail)}.

## Indicadores

Os cinco indicadores abaixo saem das reservas válidas. Ocupação é diárias vendidas divididas por {N_ROOMS} quartos vezes os dias do mês. Comissão é a soma da comissão sobre a hospedagem, sem a taxa de turismo. Receita líquida é hospedagem menos comissão, café da manhã e limpeza. Percentual retido é a receita líquida dividida pelo valor pago pelo hóspede. Diárias vendidas são a soma das noites.

{_indicator_table(parts, total)}

## Conferência de outubro

{chr(10).join(october_lines)}

## Achado

Pergunta: a ocupação e a receita se concentram em feriados nacionais e em pontes (fins de semana prolongados)?

Regra do calendário usada na evidência: feriado na segunda puxa sábado e domingo; feriado na sexta puxa sábado e domingo; feriado na terça inclui a segunda; feriado na quinta inclui a sexta. A receita de cada reserva é rateada em partes iguais entre as noites da estadia.

Evidência:

{evidence}

{interpretation}

## Limitação

A evidência acima descreve este lote, não um efeito causal do feriado. A BrasilAPI traz só feriados nacionais: feriado estadual ou municipal da cidade da pousada entra como dia comum. O rateio igual da receita líquida reparte também café, limpeza e comissão entre as noites; o modelo de tarifa, herdado do theme2.py, não tem preço diferente no fim de semana. Estadia que cruzaria o mês é rejeitada, como o limite de noites do theme2.py. Setembro de 2026 foi escrito para o exercício e não é um extrato real; outubro é o caderno do theme2.py.

## Dados externos e junção

{chr(10).join(meta_lines)}

O que cada linha significa: no CSV de reservas, uma linha é uma hospedagem; no JSON de feriados, uma linha é uma data nacional; no CSV integrado, uma linha é uma noite ocupada de uma reserva. A chave de junção é a data ISO (`night_date`). A relação é many-to-one: várias noites podem cair no mesmo feriado e cada noite encontra no máximo um feriado. Noite sem feriado permanece no arquivo, com o nome do feriado vazio. Isso é ausência esperada de correspondência, não erro.

Checagens desta execução:

- Datas de feriado únicas: {"sim" if checks["holiday_dates_unique"] else "não"}.
- Cardinalidade declarada na junção: {checks["cardinality"]}.
- Chave (booking_id, night_date) única: {"sim" if checks["night_key_unique"] else "não"}.
- Reservas antes e depois: {checks["bookings_before"]} e {checks["bookings_after"]}.
- Diárias antes e depois: {checks["nights_before"]} e {checks["nights_after"]}.
- Receita líquida antes e depois: {brl(checks["net_before"])} e {brl(checks["net_after"])}.
- Valor pago antes e depois: {brl(checks["paid_before"])} e {brl(checks["paid_after"])}.
- Noites com feriado: {checks["matched_holiday_nights"]}. Noites sem feriado: {checks["unmatched_nights"]}.
- Feriados do ano sem nenhuma diária neste lote: {checks["holidays_without_nights"]}.
- Noites em feriado ou ponte: {checks["long_weekend_nights"]}.

Rastreio: as colunas `source_file` e `run_id` seguem da reserva para a noite integrada. O id desta execução é {run_info["run_id"]}.

## Mesma base nas três saídas

{same_base}

Reação a dado externo inválido, se ocorresse: JSON fora da estrutura, data ilegível, data repetida ou cobertura abaixo do mínimo não substitui o arquivo em data/external. Havendo cache válido, o log marca source_mode=cache e o fechamento segue. Sem cache válido, a execução para com status falha e não grava CSV, planilha nem este relatório.
"""
