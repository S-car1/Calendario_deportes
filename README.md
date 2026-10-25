# Calendario Deportes

Página personal con el calendario de partidos de hoy + mañana (fútbol, básquet, UFC/One Championship, rugby), con filtros por deporte, app de streaming (Chile) y horario. Pensada para reemplazar 365Scores + FotMob + app NBA + buscar UFC a mano.

🔗 **Publicada en: https://s-car1.github.io/Calendario_deportes/**

Ver [PLAN.md](PLAN.md) (arquitectura y alcance) y [PROGRESS.md](PROGRESS.md) (investigación de fuentes de datos) para el contexto completo.

## Cómo funciona

1. Un GitHub Action corre 2 veces al día (`.github/workflows/update-data.yml`), sin depender de ningún PC encendido.
2. Los scripts en `scripts/fetch_*.py` traen partidos de cada fuente — **todo por scraping/APIs públicas gratis, sin ninguna API key**: UFC y fútbol/NBA/Euroliga/rugby via la API no oficial de ESPN, y ONE Championship por scraping HTML de su sitio.
3. `scripts/build_report.py` junta todo (+ los eventos manuales de `data/manual_events/` + la tabla de streaming de `data/streaming_rules.json`) en `data/today.json`.
4. `index.html` es la página que lee `data/today.json` y muestra el calendario con filtros.

No hace falta ninguna cuenta ni API key para que esto funcione — es 100% scraping de fuentes públicas, igual que UFC.

## Correr todo a mano (para probar)

```bash
pip install -r requirements.txt
python scripts/fetch_ufc.py
python scripts/fetch_one_championship.py
python scripts/fetch_espn_sports.py   # fútbol (todas las ligas) + NBA + Euroliga + rugby
python scripts/build_report.py
python -m http.server 8765   # y abrir http://localhost:8765/index.html
```

## Mantención manual
- `data/streaming_rules.json` — qué app transmite cada competencia en Chile. Revisar cuando cambien los derechos de TV (ver notas de "última revisión" en cada fila).
- `data/nba_special_windows.json` — fechas de NBA Cup Knockout / Play-In / Finales donde cambia a Prime Video en vez del default HBO Max. Hay que actualizarlo cada temporada (las fechas no se repiten).
- `data/followed_entities.json` — jugadores/equipos chilenos seguidos. Revisar en cada ventana de pases.
- `data/manual_events/` — LNB Chile y Los Cóndores específicos (ver el README de esa carpeta).

## Si en el futuro se quiere más cobertura con API keys
Se evaluaron API-Football (fútbol) y balldontlie (NBA) como alternativas con más detalle/confiabilidad, pero por ahora se descartaron a favor del scraping 100% gratis vía ESPN. Ver [PROGRESS.md](PROGRESS.md) si más adelante se quiere reconsiderar.
