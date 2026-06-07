from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from datetime import date
from email.utils import parsedate_to_datetime

from playwright.sync_api import sync_playwright


#################################################
#################################################
####                                         ####
####                                         ####
####      VERSIÓN REALIZADA CON chatGPT      ####
####      2026/03                            ####
####                                         ####
#################################################
#################################################

# ---------------------------------------------------------------------------
# Primitiva
# ---------------------------------------------------------------------------
# En arisrv, los endpoints/HTML habituales de SELAE pueden devolver 403 de forma
# no fiable según el edge/CDN. La obtención de resultados de Primitiva se hace
# por tanto a través del RSS oficial, accedido con Playwright (navegador real).
#
# Formato devuelto por getPrimiLatestResults():
#   {fecha_sorteo: [n1, n2, n3, n4, n5, n6, complementario, reintegro]}
# ---------------------------------------------------------------------------

PRIMI_RSS_URL = "https://www.loteriasyapuestas.es/es/la-primitiva/resultados/.formatoRSS"
EURO_RSS_URL = "https://www.loteriasyapuestas.es/es/euromillones/resultados/.formatoRSS"

_PRIMI_NUMBERS_RE = re.compile(
    r"(\d{1,2})\s*-\s*(\d{1,2})\s*-\s*(\d{1,2})\s*-\s*(\d{1,2})\s*-\s*(\d{1,2})\s*-\s*(\d{1,2})"
    r"\s*Complementario:\s*C\((\d{1,2})\)"
    r"\s*Reintegro:\s*R\((\d{1,2})\)"
    r"(?:\s*Joker:\s*J\((\d+)\))?"
)
_EURO_NUMBERS_RE = re.compile(
    r"(\d{1,2})\s*-\s*(\d{1,2})\s*-\s*(\d{1,2})\s*-\s*(\d{1,2})\s*-\s*(\d{1,2})"
    r"\s*Estrellas:\s*(\d{1,2})\s*-\s*(\d{1,2})"
)


def _fetch_xml_with_playwright(url: str, timeout_ms: int = 30000) -> str:
    """
    Descarga una URL con un navegador real (Playwright + Firefox) y devuelve
    el bloque XML RSS extraído del contenido renderizado.

    Se usa Playwright porque, en arisrv, curl/requests pueden recibir 403
    aunque Firefox sí obtenga el RSS correctamente.
    """
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        content = page.content()
        browser.close()

    # Firefox puede mostrar el XML dentro de un visor HTML. Extraemos el bloque RSS.
    match = re.search(r"(<rss\b.*</rss>)", content, flags=re.DOTALL)
    if not match:
        raise RuntimeError(f"No se pudo extraer XML RSS válido desde {url}")

    return match.group(1)


def _parse_primi_description(description_html: str) -> list[int]:
    """
    Extrae números de Primitiva desde el HTML embebido en <description> del RSS.

    Devuelve:
        [n1, n2, n3, n4, n5, n6, complementario, reintegro]
    """
    text = html.unescape(description_html)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    match = _PRIMI_NUMBERS_RE.search(text)
    if not match:
        raise RuntimeError(
            "No se pudo extraer combinación/complementario/reintegro "
            "del RSS de Primitiva"
        )

    return [int(match.group(i)) for i in range(1, 9)]


def _parse_euro_description(description_html: str) -> list[int]:
    """
    Extrae números de Euromillones desde el HTML embebido en <description> del RSS.

    Devuelve:
        [n1, n2, n3, n4, n5, e1, e2]
    """
    text = html.unescape(description_html)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    match = _EURO_NUMBERS_RE.search(text)
    if not match:
        raise RuntimeError(
            "No se pudo extraer combinación/estrellas del RSS de Euromillones"
        )

    return [int(match.group(i)) for i in range(1, 8)]



def getPrimiLatestResults(fecha_inicial: date | None = None) -> dict[date, list[int]]:
    """
    Devuelve resultados recientes de Primitiva usando el RSS oficial.

    Resultado:
        {fecha_sorteo: [n1, n2, n3, n4, n5, n6, complementario, reintegro]}

    Si fecha_inicial no es None, solo se devuelven sorteos con fecha >= fecha_inicial.
    """
    rss_xml = _fetch_xml_with_playwright(PRIMI_RSS_URL)
    root = ET.fromstring(rss_xml)

    channel = root.find("channel")
    if channel is None:
        raise RuntimeError("RSS de Primitiva sin nodo <channel>")

    resultados: dict[date, list[int]] = {}

    for item in channel.findall("item"):
        pub_date_text = item.findtext("pubDate")
        description_html = item.findtext("description")

        if not pub_date_text or not description_html:
            continue

        draw_date = parsedate_to_datetime(pub_date_text).date()

        if fecha_inicial is not None and draw_date < fecha_inicial:
            continue

        resultados[draw_date] = _parse_primi_description(description_html)

    return dict(sorted(resultados.items(), reverse=True))


# ---------------------------------------------------------------------------
# Euromillones
# ---------------------------------------------------------------------------

def getEuroLatestResults(fecha_inicial: date | None = None) -> dict[date, list[int]]:
    """
    Devuelve resultados recientes de Euromillones usando el RSS oficial.

    Resultado:
        {fecha_sorteo: [n1, n2, n3, n4, n5, e1, e2]}

    Si fecha_inicial no es None, solo se devuelven sorteos con fecha >= fecha_inicial.
    """
    rss_xml = _fetch_xml_with_playwright(EURO_RSS_URL)
    root = ET.fromstring(rss_xml)

    channel = root.find("channel")
    if channel is None:
        raise RuntimeError("RSS de Euromillones sin nodo <channel>")

    resultados: dict[date, list[int]] = {}

    for item in channel.findall("item"):
        pub_date_text = item.findtext("pubDate")
        description_html = item.findtext("description")

        if not pub_date_text or not description_html:
            continue

        draw_date = parsedate_to_datetime(pub_date_text).date()

        if fecha_inicial is not None and draw_date < fecha_inicial:
            continue

        resultados[draw_date] = _parse_euro_description(description_html)

    return dict(sorted(resultados.items(), reverse=True))
