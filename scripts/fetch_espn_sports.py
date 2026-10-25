"""Trae fútbol (todas las ligas en alcance), NBA, Euroliga y rugby via la misma API no oficial
de ESPN que ya usamos para UFC -- sin API key. Probado 2026-10-24: las 8 ligas de fútbol, NBA
y Euroliga responden bien con este mismo patrón (site.api.espn.com/apis/site/v2/sports/...).

Reemplaza el enfoque anterior (API-Football + balldontlie, que pedían key) por decisión del
usuario: "por ahora nada de API [con key], haz un barrido ... que sea el mismo proceso que
ufc y demás, un scrap de info disponible en internet".
"""
from datetime import datetime, timedelta, timezone

import requests

from common import BROWSER_HEADERS, write_raw

# (espn_sport, slug) -> (competition_tier, nombre legible, sport del esquema común)
LEAGUES = [
    ("soccer", "chi.1", "liga-de-primera-chile", "Liga de Primera (Chile)", "football"),
    ("soccer", "eng.1", "premier-league", "Premier League", "football"),
    ("soccer", "esp.1", "laliga", "LaLiga", "football"),
    ("soccer", "fra.1", "ligue-1", "Ligue 1", "football"),
    ("soccer", "arg.1", "liga-profesional-argentina", "Liga Profesional Argentina", "football"),
    ("soccer", "bra.1", "brasileirao", "Brasileirão", "football"),
    ("soccer", "conmebol.libertadores", "copa-libertadores", "Copa Libertadores", "football"),
    ("soccer", "conmebol.sudamericana", "copa-sudamericana", "Copa Sudamericana", "football"),
    ("soccer", "uefa.champions", "champions-league", "UEFA Champions League", "football"),
    ("basketball", "nba", "nba", "NBA", "basketball"),
    ("basketball", "euroleague", "euroliga", "Euroliga", "basketball"),
    ("rugby", "180659", "rugby-tier1", "Six Nations", "rugby"),
    ("rugby", "289234", "rugby-tier1", "International Test Match", "rugby"),
]


def target_dates():
    today = datetime.now(timezone.utc).date()
    return [today, today + timedelta(days=1)]


def fetch():
    all_events = []
    dates = target_dates()
    for espn_sport, slug, tier, name, sport in LEAGUES:
        for date in dates:
            url = f"https://site.api.espn.com/apis/site/v2/sports/{espn_sport}/{slug}/scoreboard"
            resp = requests.get(url, headers=BROWSER_HEADERS, params={"dates": date.strftime("%Y%m%d")}, timeout=20)
            if resp.status_code != 200:
                print(f"[!] {espn_sport}/{slug} {date}: status {resp.status_code}, se omite")
                continue
            data = resp.json()
            league_logo = None
            logos = data.get("leagues", [{}])[0].get("logos", [])
            default_logo = next((l["href"] for l in logos if "default" in l.get("rel", [])), None)
            league_logo = default_logo or (logos[0]["href"] if logos else None)

            for ev in data.get("events", []):
                ev["_competition_tier"] = tier
                ev["_competition_name"] = name
                ev["_sport"] = sport
                ev["_league_logo"] = league_logo
                all_events.append(ev)

    write_raw("espn_sports", {"events": all_events})
    return all_events


if __name__ == "__main__":
    events = fetch()
    by_tier = {}
    for e in events:
        by_tier[e["_competition_tier"]] = by_tier.get(e["_competition_tier"], 0) + 1
    print(f"ESPN sports: {len(events)} eventos encontrados para hoy/mañana")
    for tier, count in by_tier.items():
        print(f"  {tier}: {count}")
