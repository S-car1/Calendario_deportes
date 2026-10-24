"""Corre esto UNA VEZ (a mano, con tu API_FOOTBALL_KEY) para resolver y cachear los IDs
reales de cada competencia en API-Football. No conviene adivinar los IDs de memoria --
quedan guardados en data/football_league_ids.json para que fetch_football.py no tenga
que resolverlos de nuevo cada día (ahorra cuota gratis).

Uso:
    API_FOOTBALL_KEY=tu_key python scripts/resolve_football_leagues.py
"""
import json
from pathlib import Path

import requests

from common import BROWSER_HEADERS, env

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "data" / "football_league_ids.json"
BASE_URL = "https://v3.football.api-sports.io"


def main():
    api_key = env("API_FOOTBALL_KEY")
    headers = {**BROWSER_HEADERS, "x-apisports-key": api_key}

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    for league in config["leagues"]:
        if league.get("id"):
            print(f"[skip] {league['key']} ya tiene id {league['id']}")
            continue
        params = {"search": league["search_name"]}
        resp = requests.get(f"{BASE_URL}/leagues", headers=headers, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("response", [])

        if league.get("search_country"):
            results = [
                r for r in results
                if r.get("country", {}).get("name", "").lower() == league["search_country"].lower()
            ]

        if not results:
            print(f"[!] {league['key']}: sin resultados para '{league['search_name']}' -- revisar a mano")
            continue

        if len(results) > 1:
            print(f"[?] {league['key']}: {len(results)} resultados, tomando el primero -- VERIFICAR A MANO:")
            for r in results:
                lg = r["league"]
                print(f"    id={lg['id']} name={lg['name']} country={r['country']['name']}")

        chosen = results[0]["league"]
        league["id"] = chosen["id"]
        league["resolved_name"] = chosen["name"]
        print(f"[ok] {league['key']} -> id={chosen['id']} ({chosen['name']})")

    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nGuardado en {CONFIG_PATH}")


if __name__ == "__main__":
    main()
