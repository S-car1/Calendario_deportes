"""Trae los partidos de hoy + mañana de las competencias de fútbol en alcance, via API-Football.
Necesita API_FOOTBALL_KEY (gratis en api-sports.io/api-football, ~100 req/día).
Necesita que data/football_league_ids.json ya tenga los IDs resueltos
(correr scripts/resolve_football_leagues.py una vez primero).
"""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

from common import BROWSER_HEADERS, env, write_raw

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "data" / "football_league_ids.json"
BASE_URL = "https://v3.football.api-sports.io"


def target_dates():
    today = datetime.now(timezone.utc).date()
    return [today, today + timedelta(days=1)]


def fetch():
    api_key = env("API_FOOTBALL_KEY")
    headers = {**BROWSER_HEADERS, "x-apisports-key": api_key}

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    league_by_id = {lg["id"]: lg["key"] for lg in config["leagues"] if lg.get("id")}
    missing = [lg["key"] for lg in config["leagues"] if not lg.get("id")]
    if missing:
        print(f"[!] Ligas sin ID resuelto (se van a omitir): {missing}. "
              f"Corré resolve_football_leagues.py primero.")

    all_fixtures = []
    for date in target_dates():
        date_str = date.strftime("%Y-%m-%d")
        resp = requests.get(f"{BASE_URL}/fixtures", headers=headers, params={"date": date_str}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        for fixture in data.get("response", []):
            league_id = fixture.get("league", {}).get("id")
            if league_id in league_by_id:
                fixture["_competition_key"] = league_by_id[league_id]
                all_fixtures.append(fixture)

    write_raw("football", {"fixtures": all_fixtures})
    return all_fixtures


if __name__ == "__main__":
    fixtures = fetch()
    print(f"Fútbol: {len(fixtures)} partidos encontrados para hoy/mañana en las ligas de interés")
