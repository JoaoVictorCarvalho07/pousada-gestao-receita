"""Consulta de feriados nacionais na BrasilAPI, com cache local.

Reação a dado inválido: a resposta bruta só é gravada depois de passar na
checagem de estrutura, tipo e cobertura. Se a consulta ao vivo falha ou o
JSON não serve, o pipeline usa o último arquivo válido em data/external e
registra source_mode=cache. Sem cache válido, a execução para. Não se inventa
feriado e não se publica o fechamento como se a junção tivesse ocorrido.
"""

import json
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import requests

ENDPOINT = "https://brasilapi.com.br/api/feriados/v1/{year}"
TERMS_OF_USE = (
    "A BrasilAPI oferece feriados nacionais como dado público, sem chave de acesso. "
    "O uso neste trabalho é acadêmico. Não há garantia de disponibilidade: se a consulta "
    "falhar, fica valendo a última resposta bruta salva em data/external. A resposta "
    "bruta não é editada à mão. Termos e documentação: https://brasilapi.com.br/"
)
TZ = ZoneInfo("America/Sao_Paulo")
TIMEOUT_SECONDS = 20
USER_AGENT = "pousada-fechamento/1.0"

FIXED_HOLIDAYS = ("01-01", "04-21", "05-01", "09-07", "10-12", "11-02", "11-15", "12-25")


class ExternalDataError(Exception):
    """O dado externo não pôde ser usado com segurança."""


def fetch_live(year, timeout=TIMEOUT_SECONDS):
    """GET na BrasilAPI. O ano vai no caminho e também em params."""
    url = ENDPOINT.format(year=year)
    try:
        response = requests.get(
            url,
            params={"year": year},
            timeout=timeout,
            headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        )
        response.raise_for_status()
    except requests.Timeout as exc:
        raise ExternalDataError(f"Tempo esgotado ao consultar a BrasilAPI ({timeout}s).") from exc
    except requests.ConnectionError as exc:
        raise ExternalDataError("Falha de conexão com a BrasilAPI.") from exc
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "?"
        raise ExternalDataError(f"BrasilAPI respondeu HTTP {status}.") from exc
    return response.text, response.status_code


def parse_holiday_payload(text, year):
    """Converte o JSON em DataFrame com colunas date, name e type.

    Exige lista de objetos, data ISO no ano pedido, nome e tipo textuais,
    datas únicas e a presença dos feriados nacionais fixos.
    """
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ExternalDataError(f"JSON inválido: {exc}.") from exc
    if not isinstance(payload, list):
        raise ExternalDataError("A resposta não é uma lista de feriados.")

    rows = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ExternalDataError(f"Item {index} não é um objeto.")
        for key in ("date", "name", "type"):
            if key not in item:
                raise ExternalDataError(f"Item {index} sem o campo {key}.")
        if not isinstance(item["date"], str):
            raise ExternalDataError(f"Item {index} com date que não é texto.")
        if not isinstance(item["name"], str) or not item["name"].strip():
            raise ExternalDataError(f"Item {index} com name vazio ou de tipo inesperado.")
        if not isinstance(item["type"], str) or not item["type"].strip():
            raise ExternalDataError(f"Item {index} com type vazio ou de tipo inesperado.")
        try:
            parsed = datetime.strptime(item["date"], "%Y-%m-%d").date()
        except ValueError as exc:
            raise ExternalDataError(f"Data inválida no item {index}: {item['date']}.") from exc
        if parsed.year != int(year):
            raise ExternalDataError(f"Data {item['date']} está fora do ano {year}.")
        rows.append(
            {
                "date": parsed.isoformat(),
                "name": item["name"].strip(),
                "type": item["type"].strip(),
            }
        )

    frame = pd.DataFrame(rows, columns=["date", "name", "type"])
    if frame.empty:
        raise ExternalDataError("A lista de feriados veio vazia.")
    duplicated = frame.loc[frame["date"].duplicated(), "date"].tolist()
    if duplicated:
        raise ExternalDataError("Há datas de feriado repetidas: " + ", ".join(duplicated) + ".")
    if len(frame) < 8:
        raise ExternalDataError(f"Cobertura insuficiente: {len(frame)} feriados (mínimo 8).")
    present = set(frame["date"])
    missing = [f"{year}-{month_day}" for month_day in FIXED_HOLIDAYS if f"{year}-{month_day}" not in present]
    if missing:
        raise ExternalDataError("Faltam feriados nacionais fixos: " + ", ".join(missing) + ".")
    return frame.sort_values("date").reset_index(drop=True)


def _build_meta(year, status, source_mode, count):
    return {
        "provider": "BrasilAPI",
        "endpoint": ENDPOINT.format(year=year),
        "params": {"year": int(year)},
        "params_note": (
            "O ano entra no caminho da URL. A mesma informação é enviada em params "
            "do requests; a consulta de verificação devolveu o mesmo JSON com e sem esse parâmetro."
        ),
        "retrieved_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "http_status": status,
        "source_mode": source_mode,
        "record_count": int(count),
        "units": {
            "date": "data civil no calendário gregoriano, formato ISO-8601 (YYYY-MM-DD)",
            "name": "nome do feriado nacional em português",
            "type": "classificação da BrasilAPI; nesta rota o valor esperado é national",
        },
        "terms_of_use": TERMS_OF_USE,
    }


def _paths(external_dir, year):
    folder = external_dir
    return folder / f"feriados_{year}.json", folder / f"feriados_{year}.meta.json"


def _read_cache(raw_path, meta_path, year):
    if not raw_path.exists():
        raise ExternalDataError(f"Modo cache sem o arquivo {raw_path.name}. Rode uma vez com a rede disponível.")
    body = raw_path.read_text(encoding="utf-8-sig")
    try:
        frame = parse_holiday_payload(body, year)
    except ExternalDataError as exc:
        raise ExternalDataError(f"O cache {raw_path.name} é inválido e não foi usado: {exc}") from exc
    stored = {}
    if meta_path.exists():
        stored = json.loads(meta_path.read_text(encoding="utf-8"))
    meta = dict(stored)
    meta["source_mode"] = "cache"
    meta["cache_file"] = raw_path.name
    meta.setdefault("provider", "BrasilAPI")
    meta.setdefault("endpoint", ENDPOINT.format(year=year))
    meta.setdefault("params", {"year": int(year)})
    meta.setdefault("units", _build_meta(year, None, "cache", len(frame))["units"])
    meta.setdefault("terms_of_use", TERMS_OF_USE)
    meta["record_count"] = int(len(frame))
    return frame, meta


def _cache_is_usable(raw_path, year):
    if not raw_path.exists():
        return False
    try:
        parse_holiday_payload(raw_path.read_text(encoding="utf-8-sig"), year)
    except (ExternalDataError, OSError, UnicodeError):
        return False
    return True


def _acquire_year(year, external_dir, offline, logger):
    external_dir.mkdir(parents=True, exist_ok=True)
    raw_path, meta_path = _paths(external_dir, year)
    if offline:
        logger.info("passo=feriados ano=%s source_mode=cache motivo=offline arquivo=%s", year, raw_path.name)
        return _read_cache(raw_path, meta_path, year)

    try:
        body, status = fetch_live(year)
        frame = parse_holiday_payload(body, year)
    except (ExternalDataError, requests.RequestException) as exc:
        logger.warning("passo=feriados ano=%s consulta_ao_vivo_falhou erro=%s", year, exc)
        if _cache_is_usable(raw_path, year):
            logger.info("passo=feriados ano=%s source_mode=cache motivo=fallback arquivo=%s", year, raw_path.name)
            return _read_cache(raw_path, meta_path, year)
        raise ExternalDataError(
            f"Não foi possível obter feriados de {year} e não há cache válido em {raw_path}."
        ) from exc

    meta = _build_meta(year, status, "live", len(frame))
    raw_path.write_text(body, encoding="utf-8")
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    logger.info(
        "passo=feriados ano=%s source_mode=live http=%s registros=%s arquivo=%s",
        year,
        status,
        len(frame),
        raw_path.name,
    )
    return frame, meta


def acquire_holidays(years, external_dir, offline, logger=None):
    """Busca um ano de cada vez e devolve um DataFrame com date, name e type."""
    if logger is None:
        logger = logging.getLogger("pousada.pipeline")
    frames = []
    metas = []
    for year in years:
        frame, meta = _acquire_year(int(year), external_dir, offline, logger)
        frames.append(frame)
        metas.append(meta)
    combined = pd.concat(frames, ignore_index=True)
    modes = {meta.get("source_mode") for meta in metas}
    if modes == {"live"}:
        source_mode = "live"
    elif modes == {"cache"}:
        source_mode = "cache"
    else:
        source_mode = "misto"
    return combined, {
        "source_mode": source_mode,
        "years": [int(year) for year in years],
        "records": int(len(combined)),
        "by_year": metas,
    }
