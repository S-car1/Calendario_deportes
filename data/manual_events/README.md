# Eventos manuales

Cada archivo `.json` acá adentro tiene la forma `{"events": [...]}`, con objetos que ya siguen el formato común de `docs/schema.md` directamente (build_report.py los toma tal cual, sin normalizar).

Archivos esperados:
- `lnb_chile.json` — partidos de la Liga Chery (LNB Chile) que se quieran destacar a mano (decisión: no se automatiza, ver PROGRESS.md).
- `rugby_condores.json` — partidos específicos de Los Cóndores cuando no los cubre la API de ESPN (torneos nuevos como la Nations Cup).
- `one_small_events.json` — opcional, si se quiere agregar a mano algún Friday Fight/Samurai de ONE que no se haya querido traer automático.

Ejemplo de un evento:

```json
{
  "events": [
    {
      "id": "lnb-manual-2026-11-01-colocolo-uc",
      "sport": "basketball",
      "competition": "Liga Chery (LNB Chile)",
      "competition_tier": "lnb-chile",
      "date_utc": "2026-11-01T23:00:00Z",
      "home": "Colo-Colo",
      "away": "Universidad Católica",
      "status": "scheduled",
      "importance": [],
      "followed_entities": [],
      "streaming_chile": ["TNT Sports"],
      "source": "manual",
      "notes": null
    }
  ]
}
```
