"""Trae el calendario completo de UFC via la API no oficial de ESPN.
Sin API key. Probado y funcionando (2026-10-24): devuelve el calendario anual completo.
"""
import requests
from common import BROWSER_HEADERS, write_raw

URL = "https://site.api.espn.com/apis/site/v2/sports/mma/ufc/scoreboard"


def fetch():
    resp = requests.get(URL, headers=BROWSER_HEADERS, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    league = data["leagues"][0]
    calendar = league["calendar"]
    logos = league.get("logos", [])
    logo = next((l["href"] for l in logos if "default" in l.get("rel", [])), None) or (logos[0]["href"] if logos else None)
    write_raw("ufc", {"events": calendar, "logo": logo})
    return calendar


if __name__ == "__main__":
    events = fetch()
    print(f"UFC: {len(events)} eventos encontrados")
