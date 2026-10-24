"""Trae partidos de rugby (Six Nations + International Test Match) via la API no oficial de ESPN.
Sin API key. A diferencia de UFC, esta API no da un calendario anual con nombres de evento
para rugby -- hay que pedir el scoreboard de fechas puntuales. Como el reporte es "hoy + mañana",
pedimos esas dos fechas nomás (barato, 2 llamadas por liga).

IDs de liga conocidos (ESPN):
- 180659: Six Nations
- 289234: International Test Match (incluye partidos de selecciones nacionales tier 1/2,
  pero no está confirmado si cubre la nueva World Rugby Nations Cup 2026 de Los Cóndores --
  revisar manualmente si no aparece).

TODO: falta encontrar el league id de "The Rugby Championship" y de la "Nations Cup 2026"
específicamente -- no se encontró en esta pasada. Los Cóndores se siguen manejando a mano
(ver data/manual_events/rugby.json) hasta confirmar esos IDs.
"""
from datetime import datetime, timedelta, timezone

import requests

from common import BROWSER_HEADERS, write_raw

LEAGUES = {
    "180659": "Six Nations",
    "289234": "International Test Match",
}


def target_dates():
    today = datetime.now(timezone.utc).date()
    return [today, today + timedelta(days=1)]


def fetch():
    all_events = []
    for date in target_dates():
        date_str = date.strftime("%Y%m%d")
        for league_id, league_name in LEAGUES.items():
            url = f"https://site.api.espn.com/apis/site/v2/sports/rugby/{league_id}/scoreboard"
            resp = requests.get(url, headers=BROWSER_HEADERS, params={"dates": date_str}, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            for ev in data.get("events", []):
                ev["_league_name"] = league_name
                all_events.append(ev)
    write_raw("rugby_espn", {"events": all_events})
    return all_events


if __name__ == "__main__":
    events = fetch()
    print(f"Rugby (ESPN): {len(events)} partidos encontrados para hoy/mañana")
