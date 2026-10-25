# Esquema de datos

Todo el pipeline converge en un único archivo `data/today.json`, que es lo que lee la página web. Cada partido/evento es un objeto con esta forma:

```json
{
  "id": "espn-600123456",
  "sport": "football",
  "competition": "Liga de Primera (Chile)",
  "competition_tier": "liga-de-primera-chile",
  "date_utc": "2026-10-25T23:00:00Z",
  "home": "Colo Colo",
  "away": "Universidad de Chile",
  "home_logo": "https://a.espncdn.com/i/teamlogos/soccer/500/XXXX.png",
  "away_logo": "https://a.espncdn.com/i/teamlogos/soccer/500/YYYY.png",
  "league_logo": "https://a.espncdn.com/i/leaguelogos/soccer/500/ZZZ.png",
  "status": "Scheduled",
  "importance": ["Superclásico"],
  "followed_entities": ["Colo-Colo"],
  "streaming_chile": ["TNT Sports", "HBO Max", "Canal 13 (1 partido/fecha, gratis)"],
  "relevance_score": 90,
  "source": "espn-api",
  "notes": null
}
```

`relevance_score` se calcula en `build_report.py`: peso base por competencia (`TIER_WEIGHT`) + 50 por cada entidad seguida que aparece + 30 por cada tag de `importance`. El build ordena por día y, dentro del día, de mayor a menor relevancia — el frontend puede reordenar por hora si se prefiere.

Campos:
- `sport`: `football` | `basketball` | `mma` | `rugby`
- `competition_tier`: etiqueta libre para agrupar/filtrar (ej. `chile`, `europa-top`, `sudamerica`, `nba`, `euroliga`, `lnb`, `ufc`, `one`, `rugby-tier1`)
- `importance`: lista de tags opcionales (`clasico`, `final`, `eliminatoria`, `top-of-table`, `jugador-seguido`) — se usa para resaltar partidos en la UI, no para filtrar/ocultar
- `followed_entities`: equipo/jugador seguido involucrado en el partido (para el filtro "mis seguidos")
- `streaming_chile`: lista (puede ser más de una app/señal) — viene de `data/streaming_rules.json` cruzado por competencia, o reglas especiales (ej. NBA)
- `source`: de dónde vino el dato (`api-football`, `balldontlie`, `espn-api`, `onefc-scrape`, `manual`) — útil para debug

## Archivos del pipeline

- `data/streaming_rules.json` — tabla manual: competencia/liga → plataforma(s) en Chile. Mantenida a mano.
- `data/followed_entities.json` — equipos/jugadores que el usuario sigue especialmente (Colo-Colo, chilenos en el extranjero, etc.)
- `data/manual_events/*.json` — eventos curados a mano para lo que no tiene API (LNB Chile, Los Cóndores, One Championship chico)
- `data/today.json` — **output final**, generado por `scripts/build_report.py`, es lo único que lee la web

## Scripts de ingesta (cada uno escribe a `data/raw/<fuente>.json`)

Todos sin API key — 100% APIs públicas/scraping, igual que UFC.

- `scripts/fetch_ufc.py` — API no oficial de ESPN
- `scripts/fetch_one_championship.py` — scraping HTML de onefc.com/events
- `scripts/fetch_espn_sports.py` — API no oficial de ESPN: fútbol (las 8 ligas en alcance), NBA, Euroliga y rugby (Six Nations + International Test Match), todo en un solo script

`scripts/build_report.py` lee todos los `data/raw/*.json` + los archivos manuales, aplica el criterio de alcance (ligas/equipos de PLAN.md), cruza con `streaming_rules.json`, y escribe `data/today.json` con los partidos de hoy + mañana.
