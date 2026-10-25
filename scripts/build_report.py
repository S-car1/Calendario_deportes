"""Junta todas las fuentes (data/raw/*.json de las APIs + data/manual_events/*.json a mano)
en un único data/today.json con el formato común (ver docs/schema.md). Es lo único que
lee la página web.

Corre esto DESPUÉS de los scripts fetch_*.py. Si algún data/raw/<fuente>.json no existe,
simplemente la omite -- no rompe el build.
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
NBA_SPECIAL_WINDOWS = json.loads((ROOT / "data" / "nba_special_windows.json").read_text(encoding="utf-8"))["windows"]
RIVALRIES = json.loads((ROOT / "data" / "rivalries.json").read_text(encoding="utf-8"))["rivalries"]

# Peso base de relevancia por competencia -- refleja cuánto le importan al usuario estas
# ligas en general (independiente de si sigue a un equipo/jugador puntual en el partido).
TIER_WEIGHT = {
    "liga-de-primera-chile": 40,
    "copa-libertadores": 38,
    "nba": 35,
    "ufc": 32,
    "one-fight-night": 32,
    "copa-sudamericana": 28,
    "premier-league": 25,
    "laliga": 25,
    "brasileirao": 20,
    "liga-profesional-argentina": 20,
    "ligue-1": 18,
    "euroliga": 15,
    "rugby-tier1": 15,
    "one-friday-fights": 8,
}
FOLLOWED_BONUS = 50
IMPORTANCE_BONUS = 30


def nba_streaming_for(dt: datetime):
    """Regla NBA: default HBO Max, salvo que la fecha caiga en una ventana especial (Prime Video)."""
    day = dt.date().isoformat()
    for w in NBA_SPECIAL_WINDOWS:
        if w["start_date"] <= day <= w["end_date"]:
            return w["platforms"]
    return streaming_for("nba")


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


def _norm(s: str) -> str:
    """Minúsculas y sin guiones, para que 'Colo-Colo' matchee con el 'Colo Colo' de ESPN."""
    return (s or "").lower().replace("-", " ").replace("  ", " ").strip()


def followed_entities_in(*names):
    """Devuelve la lista de nombres seguidos que aparecen (substring, normalizado) en los nombres dados.
    Cruza contra los 29 equipos reales de 365Scores (data/followed_entities.json -> teams) +
    los jugadores chilenos en el extranjero que no son ya uno de esos equipos."""
    haystack = _norm(" ".join(n or "" for n in names))
    found = []
    for team in FOLLOWED["teams"]:
        if _norm(team) in haystack:
            found.append(team)
    for p in FOLLOWED["football_players_abroad"] + FOLLOWED["basketball_players_abroad"]:
        if _norm(p["name"].split()[-1]) in haystack:  # match por apellido alcanza
            found.append(p["name"])
    return found


def importance_tags(home, away):
    """Detecta clásicos/rivalidades conocidas por substring en home/away."""
    if not home or not away:
        return []
    haystack = _norm(f"{home} {away}")
    for riv in RIVALRIES:
        a, b = riv["teams"]
        if _norm(a) in haystack and _norm(b) in haystack:
            return [riv["label"]]
    return []


PRIORITY_TEAM_BONUS = 25


def relevance_score(tier, followed, importance):
    score = TIER_WEIGHT.get(tier, 10)
    score += FOLLOWED_BONUS * len(followed)
    score += IMPORTANCE_BONUS * len(importance)
    if any(_norm(FOLLOWED["priority_team"]["name"]) == _norm(f) for f in followed):
        score += PRIORITY_TEAM_BONUS
    return score


def build_event(**kwargs):
    """Construye un evento del esquema común, calculando relevance_score automáticamente."""
    kwargs["relevance_score"] = relevance_score(
        kwargs["competition_tier"], kwargs["followed_entities"], kwargs["importance"]
    )
    return kwargs


# ---------------------------------------------------------------------------
# Normalizadores por fuente
# ---------------------------------------------------------------------------

def normalize_ufc(raw, start, end):
    if not raw:
        return []
    out = []
    logo = raw.get("logo")
    for ev in raw["events"]:
        dt = datetime.fromisoformat(ev["startDate"].replace("Z", "+00:00"))
        if not in_window(dt, start, end):
            continue
        out.append(build_event(
            id=f"ufc-{ev['startDate']}-{ev['label']}",
            sport="mma",
            competition="UFC",
            competition_tier="ufc",
            date_utc=ev["startDate"],
            home=ev["label"],
            away=None,
            home_logo=logo,
            away_logo=None,
            league_logo=logo,
            status="scheduled",
            importance=[],
            followed_entities=[],
            streaming_chile=streaming_for("ufc"),
            source="espn-api",
            notes=None,
        ))
    return out


def normalize_one(raw, start, end):
    if not raw:
        return []
    out = []
    logo = raw.get("logo")
    for ev in raw["events"]:
        if not ev.get("utc_timestamp"):
            continue
        dt = datetime.fromtimestamp(ev["utc_timestamp"], tz=timezone.utc)
        if not in_window(dt, start, end):
            continue
        tier = "one-fight-night" if ev["is_fight_night"] else "one-friday-fights"
        importance = ["destacado"] if ev["is_fight_night"] else []
        out.append(build_event(
            id=f"one-{ev['slug']}",
            sport="mma",
            competition="ONE Championship",
            competition_tier=tier,
            date_utc=dt.isoformat(),
            home=ev["title"],
            away=None,
            home_logo=logo,
            away_logo=None,
            league_logo=logo,
            status="scheduled",
            importance=importance,
            followed_entities=[],
            streaming_chile=streaming_for("one-fight-night") if ev["is_fight_night"] else [],
            source="onefc-scrape",
            notes=ev.get("location"),
        ))
    return out


def normalize_espn_sports(raw, start, end):
    """Normaliza la fuente unificada (fútbol todas las ligas + NBA + Euroliga + rugby),
    todas via la misma API no oficial de ESPN -- sin API key."""
    if not raw:
        return []
    out = []
    seen_ids = set()
    for ev in raw["events"]:
        if ev["id"] in seen_ids:  # mismo evento puede salir 2 veces (query por hoy y por mañana)
            continue
        seen_ids.add(ev["id"])

        dt = datetime.fromisoformat(ev["date"].replace("Z", "+00:00"))
        if not in_window(dt, start, end):
            continue

        competitors = ev.get("competitions", [{}])[0].get("competitors", [])
        home_c = next((c for c in competitors if c.get("homeAway") == "home"), None)
        away_c = next((c for c in competitors if c.get("homeAway") == "away"), None)
        home = home_c["team"]["displayName"] if home_c else ev.get("name")
        away = away_c["team"]["displayName"] if away_c else None
        home_logo = home_c["team"].get("logo") if home_c else None
        away_logo = away_c["team"].get("logo") if away_c else None

        tier = ev["_competition_tier"]
        sport = ev["_sport"]
        followed = followed_entities_in(home, away)
        importance = importance_tags(home, away)

        if tier == "nba":
            streaming = nba_streaming_for(dt)
        elif tier in ("rugby-tier1",) and followed:
            streaming = streaming_for("rugby-los-condores")
        else:
            streaming = streaming_for(tier)

        status = ev.get("status", {}).get("type", {}).get("description", "Scheduled")

        out.append(build_event(
            id=f"espn-{ev['id']}",
            sport=sport,
            competition=ev["_competition_name"],
            competition_tier=tier,
            date_utc=ev["date"],
            home=home,
            away=away,
            home_logo=home_logo,
            away_logo=away_logo,
            league_logo=ev.get("_league_logo"),
            status=status,
            importance=importance,
            followed_entities=followed,
            streaming_chile=streaming,
            source="espn-api",
            notes=None,
        ))
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
                item.setdefault("home_logo", None)
                item.setdefault("away_logo", None)
                item.setdefault("league_logo", None)
                item.setdefault("relevance_score", relevance_score(
                    item["competition_tier"], item.get("followed_entities", []), item.get("importance", [])
                ))
                out.append(item)
    return out


def main():
    start, end = window()
    all_events = []
    all_events += normalize_ufc(load_raw("ufc"), start, end)
    all_events += normalize_one(load_raw("one_championship"), start, end)
    all_events += normalize_espn_sports(load_raw("espn_sports"), start, end)
    all_events += load_manual_events(start, end)

    # Orden por defecto: día, y dentro del día por relevancia (desc); el frontend puede
    # re-ordenar por hora si el usuario prefiere.
    all_events.sort(key=lambda e: (e["date_utc"][:10], -e["relevance_score"], e["date_utc"]))

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
