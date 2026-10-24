# Calendario Deportes

Página personal con el calendario de partidos de hoy + mañana (fútbol, básquet, UFC/One Championship, rugby), con filtros por deporte, app de streaming (Chile) y horario. Pensada para reemplazar 365Scores + FotMob + app NBA + buscar UFC a mano.

Ver [PLAN.md](PLAN.md) (arquitectura y alcance) y [PROGRESS.md](PROGRESS.md) (investigación de fuentes de datos) para el contexto completo.

## Cómo funciona

1. Un GitHub Action corre 2 veces al día (`.github/workflows/update-data.yml`), sin depender de ningún PC encendido.
2. Los scripts en `scripts/fetch_*.py` traen partidos de cada fuente (APIs + scraping) y los guardan en `data/raw/`.
3. `scripts/build_report.py` junta todo (+ los eventos manuales de `data/manual_events/` + la tabla de streaming de `data/streaming_rules.json`) en `data/today.json`.
4. `index.html` es la página que lee `data/today.json` y muestra el calendario con filtros.

## Setup (una vez)

### 1. API keys (gratis)
- **API-Football** (fútbol): creá una cuenta gratis en [api-sports.io](https://api-sports.io) o [RapidAPI](https://rapidapi.com/api-sports/api/api-football), y conseguí tu `API_FOOTBALL_KEY`.
- **balldontlie** (NBA): creá una cuenta gratis en [balldontlie.io](https://balldontlie.io), y conseguí tu `BALLDONTLIE_KEY`.

UFC, rugby y ONE Championship **no necesitan key** (APIs/scraping público).

### 2. Resolver los IDs de liga de fútbol (una sola vez)
```bash
pip install -r requirements.txt
API_FOOTBALL_KEY=tu_key python scripts/resolve_football_leagues.py
```
Esto completa `data/football_league_ids.json` con los IDs reales de cada liga (quedan committeados, no hace falta repetirlo salvo que agreguemos una liga nueva).

### 3. Secrets en GitHub
En el repo de GitHub: Settings → Secrets and variables → Actions, agregar:
- `API_FOOTBALL_KEY`
- `BALLDONTLIE_KEY`

Si no se agregan, el Action igual corre y arma el calendario solo con UFC + rugby + One Championship (fútbol y NBA quedan vacíos hasta que se agreguen las keys).

### 4. Activar GitHub Pages
Settings → Pages → Source: `main` branch, carpeta `/ (root)`. Con eso `index.html` queda publicado en `https://<usuario>.github.io/<repo>/`.

## Correr todo a mano (para probar)

```bash
pip install -r requirements.txt
python scripts/fetch_ufc.py
python scripts/fetch_rugby_espn.py
python scripts/fetch_one_championship.py
API_FOOTBALL_KEY=tu_key python scripts/fetch_football.py   # opcional
BALLDONTLIE_KEY=tu_key python scripts/fetch_nba.py          # opcional
python scripts/build_report.py
python -m http.server 8765   # y abrir http://localhost:8765/index.html
```

## Mantención manual
- `data/streaming_rules.json` — qué app transmite cada competencia en Chile. Revisar cuando cambien los derechos de TV (ver notas de "última revisión" en cada fila).
- `data/followed_entities.json` — jugadores/equipos chilenos seguidos. Revisar en cada ventana de pases.
- `data/manual_events/` — LNB Chile y Los Cóndores específicos (ver el README de esa carpeta).
