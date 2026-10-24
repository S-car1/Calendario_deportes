"""Junta todas las fuentes (data/raw/*.json de las APIs + data/manual_events/*.json a mano)
en un único data/today.json con el formato común (ver docs/schema.md). Es lo único que
lee la página web.

Corre esto DESPUÉS de los scripts fetch_*.py. Si algún data/raw/<fuente>.json no existe
(por ejemplo porque todavía no configuraste la API key de esa fuente), simplemente la
omite -- no rompe el build.
"""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
MANUAL_DIR = ROOT / "data" / "manual_events"
OUTPUT_PATH = ROOT / "data" / "today.json"

STREAMING_RULES = json.loads((ROOT / "data" / "streaming_rules.json").read_text(encoding="utf-8"))["rules"]
FOLLOWED = json.loads((ROOT / "data" / "followed_entities.json").read_text(encoding="utf-8"))


def window():
    """Hoy + mañana, en UTC, como par de datetimes [start, end)."""
    today = datetime.now(timezone.utc).date()
    start = datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc)
    end = start + timedelta(days=2)
    return start, end


def in_window(dt: datetime, start: datetime, end: datetime) -> bool:
    return start <= dt < end


def load_raw(name):
    path = RAW_DIR / f"{name}.json"
    if not path.exists():
        print(f"[skip] data/raw/{name}.json no existe, se omite esa fuente")
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def streaming_for(competition_key: str):
    for rule in STREAMING_RULES:
        if competition_key in rule["competition_match"]:
            return rule["platforms"]
    return []


def followed_entities_in(*names):
    """Devuelve la lista de nombres seguidos que aparecen (substring, case-insensitive) en los nombres dados."""
    haystack = " ".join(n or "" for n in names).lower()
    found = []
    if FOLLOWED["priority_team"]["name"].lower() in haystack:
        found.append(FOLLOWED["priority_team"]["name"])
    for p in FOLLOWED["football_players_abroad"] + FOLLOWED["basketball_players_abroad"]:
        if p["name"].split()[-1].lower() in haystack:  # match por apellido alcanza
            found.append(p["name"])
    return found


# ---------------------------------------------------------------------------
# Normalizadores por fuente
# ---------------------------------------------------------------------------

def normalize_ufc(raw, start, end):
    if not raw:
        return []
    out = []
    for ev in raw["events"]:
        dt = datetime.fromisoformat(ev["startDate"].replace("Z", "+00:00"))
        if not in_window(dt, start, end):
            continue
        out.append({
            "id": f"ufc-{ev['startDate']}-{ev['label']}",
            "sport": "mma",
            "competition": "UFC",
            "competition_tier": "ufc",
            "date_utc": ev["startDate"],
            "home": ev["label"],
            "away": None,
            "status": "scheduled",
            "importance": [],
            "followed_entities": [],
            "streaming_chile": streaming_for("ufc"),
            "source": "espn-api",
            "notes": None,
        })
    return out


def normalize_one(raw, start, end):
    if not raw:
        return []
    out = []
    for ev in raw["events"]:
        if not ev.get("utc_timestamp"):
            continue
        dt = datetime.fromtimestamp(ev["utc_timestamp"], tz=timezone.utc)
        if not in_window(dt, start, end):
            continue
        tier = "one-fight-night" if ev["is_fight_night"] else "one-friday-fights"
        out.append({
            "id": f"one-{ev['slug']}",
            "sport": "mma",
            "competition": "ONE Championship",
            "competition_tier": tier,
            "date_utc": dt.isoformat(),
            "home": ev["title"],
            "away": None,
            "status": "scheduled",
            "importance": ["destacado"] if ev["is_fight_night"] else [],
            "followed_entities": [],
            "streaming_chile": streaming_for("one-fight-night") if ev["is_fight_night"] else [],
            "source": "onefc-scrape",
            "notes": ev.get("location"),
        })
    return out


def normalize_rugby(raw, start, end):
    if not raw:
        return []
    out = []
    for ev in raw["events"]:
        dt = datetime.fromisoformat(ev["date"].replace("Z", "+00:00"))
        if not in_window(dt, start, end):
            continue
        competitors = ev.get("competitions", [{}])[0].get("competitors", [])
        home = next((c["team"]["displayName"] for c in competitors if c.get("homeAway") == "home"), None)
        away = next((c["team"]["displayName"] for c in competitors if c.get("homeAway") == "away"), None)
        out.append({
            "id": f"rugby-{ev['id']}",
            "sport": "rugby",
            "competition": ev.get("_league_name", "Rugby"),
            "competition_tier": "rugby-tier1",
            "date_utc": ev["date"],
            "home": home or ev.get("name"),
            "away": away,
            "status": "scheduled",
            "importance": [],
            "followed_entities": followed_entities_in(home, away),
            "streaming_chile": streaming_for("rugby-los-condores") if followed_entities_in(home, away) else [],
            "source": "espn-api",
            "notes": None,
        })
    return out


def normalize_football(raw, start, end):
    if not raw:
        return []
    out = []
    for fx in raw["fixtures"]:
        dt = datetime.fromisoformat(fx["fixture"]["date"])
        if not in_window(dt, start, end):
            continue
        home = fx["teams"]["home"]["name"]
        away = fx["teams"]["away"]["name"]
        comp_key = fx["_competition_key"]
        out.append({
            "id": f"football-{fx['fixture']['id']}",
            "sport": "football",
            "competition": fx["league"]["name"],
            "competition_tier": comp_key,
            "date_utc": fx["fixture"]["date"],
            "home": home,
            "away": away,
            "status": fx["fixture"]["status"]["short"],
            "importance": [],
            "followed_entities": followed_entities_in(home, away),
            "streaming_chile": streaming_for(comp_key),
            "source": "api-football",
            "notes": None,
        })
    return out


def normalize_nba(raw, start, end):
    if not raw:
        return []
    out = []
    for g in raw["games"]:
        dt = datetime.fromisoformat(g["date"]).replace(tzinfo=timezone.utc) if "T" not in g["date"] else datetime.fromisoformat(g["date"].replace("Z", "+00:00"))
        if not in_window(dt, start, end):
            continue
        home = g["home_team"]["full_name"]
        away = g["visitor_team"]["full_name"]
        out.append({
            "id": f"nba-{g['id']}",
            "sport": "basketball",
            "competition": "NBA",
            "competition_tier": "nba",
            "date_utc": dt.isoformat(),
            "home": home,
            "away": away,
            "status": g.get("status", "scheduled"),
            "importance": [],
            "followed_entities": [],
            "streaming_chile": streaming_for("nba"),
            "source": "balldontlie",
            "notes": None,
        })
    return out


def load_manual_events(start, end):
    """Carga data/manual_events/*.json -- cada archivo ya tiene el formato común directamente."""
    out = []
    if not MANUAL_DIR.exists():
        return out
    for path in MANUAL_DIR.glob("*.json"):
        items = json.loads(path.read_text(encoding="utf-8"))
        for item in items.get("events", []):
            dt = datetime.fromisoformat(item["date_utc"].replace("Z", "+00:00"))
            if in_window(dt, start, end):
                out.append(item)
    return out


def main():
    start, end = window()
    all_events = []
    all_events += normalize_ufc(load_raw("ufc"), start, end)
    all_events += normalize_one(load_raw("one_championship"), start, end)
    all_events += normalize_rugby(load_raw("rugby_espn"), start, end)
    all_events += normalize_football(load_raw("football"), start, end)
    all_events += normalize_nba(load_raw("nba"), start, end)
    all_events += load_manual_events(start, end)

    all_events.sort(key=lambda e: e["date_utc"])

    OUTPUT_PATH.write_text(
        json.dumps({
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "window": {"start": start.isoformat(), "end": end.isoformat()},
            "events": all_events,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"{len(all_events)} eventos escritos en {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
