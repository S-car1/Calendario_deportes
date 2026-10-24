"""Trae los partidos de NBA de hoy + mañana via balldontlie.io.
Necesita BALLDONTLIE_KEY (cuenta gratis en balldontlie.io). Probado 2026-10-24: el endpoint
rechaza con 401 sin el header Authorization, así que la key es obligatoria (ya no es
totalmente libre como versiones viejas de la API).
"""
from datetime import datetime, timedelta, timezone

import requests

from common import BROWSER_HEADERS, env, write_raw

BASE_URL = "https://api.balldontlie.io/nba/v1/games"


def target_dates():
    today = datetime.now(timezone.utc).date()
    return [today, today + timedelta(days=1)]


def fetch():
    api_key = env("BALLDONTLIE_KEY")
    headers = {**BROWSER_HEADERS, "Authorization": api_key}

    dates = [d.strftime("%Y-%m-%d") for d in target_dates()]
    resp = requests.get(
        BASE_URL,
        headers=headers,
        params=[("dates[]", d) for d in dates],
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()
    games = data.get("data", [])
    write_raw("nba", {"games": games})
    return games


if __name__ == "__main__":
    games = fetch()
    print(f"NBA: {len(games)} partidos encontrados para hoy/mañana")
