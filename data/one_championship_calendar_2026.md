# ONE Championship — calendario (scrapeado 2026-10-24)

**Buena noticia: onefc.com/events es 100% HTML server-renderizado, sin JS, fácil de scrapear con un simple fetch + parser (no hace falta Playwright).** Las horas ya vienen en GMT-3 (coincide con la detección geográfica CL-RM que hizo el sitio).

No existe una API pública documentada (el `wp-json/public/v2/events/{id}` solo da estado live/is_past de UN evento conocido, no sirve para listar). La fuente confiable es el HTML de `https://www.onefc.com/events/` (texto plano, selectores simples por tarjeta de evento).

## Próximos eventos (extraído 2026-10-24)

| Evento | Fecha | Hora (GMT-3) | Venue | Nota |
|---|---|---|---|---|
| ONE Friday Fights 176 & The Inner Circle 36 | 30 oct | 8:30 AM | Lumpinee Stadium, Bangkok | Próximo evento |
| ONE Friday Fights 177 & The Inner Circle 37 | 6 nov | 8:30 AM | Lumpinee Stadium, Bangkok | |
| ONE Fight Night 49: Gabriel vs. Magomedov | 6 nov | 11:00 PM | Lumpinee Stadium, Bangkok | |
| ONE Friday Fights 178 & The Inner Circle 38 | 13 nov | 8:30 AM | Lumpinee Stadium, Bangkok | |
| ONE SAMURAI 5 | 18 nov | 5:30 AM | EBARA WAVE Arena Ota, Tokyo | |
| ONE Friday Fights 179 & The Inner Circle 39 | 20 nov | 8:30 AM | Lumpinee Stadium, Bangkok | |
| ONE Friday Fights 180 & The Inner Circle 40 | 27 nov | 8:30 AM | Lumpinee Stadium, Bangkok | |
| ONE SAMURAI 6 | 2 dic | 5:30 AM | Yokohama Buntai, Yokohama | |
| ONE Friday Fights 181 & The Inner Circle 41 | 4 dic | 8:30 AM | Lumpinee Stadium, Bangkok | |
| ONE Friday Fights 182 & The Inner Circle 42 | 11 dic | 8:30 AM | Lumpinee Stadium, Bangkok | |
| ONE Friday Fights 183 & The Inner Circle 43 | 18 dic | 8:30 AM | Lumpinee Stadium, Bangkok | |
| ONE Fight Night 50 | 18 dic | 11:00 PM | Lumpinee Stadium, Bangkok | |
| ONE: Qatar | 25 mar (2027) | — | Aspire Dome, Doha | |

Nota: "ONE Friday Fights" y "ONE SAMURAI" son eventos chicos/semanales en Bangkok/Japón — altísimo volumen (varios por semana). Los "ONE Fight Night" son los eventos grandes/numerados (equivalentes a los PPV/eventos principales de UFC) — algunos marcados explícitamente "on Prime Video" en el listado de eventos pasados (ej. "ONE Fight Night 48: Erdogan vs. Elliott on Prime Video", "ONE Fight Night 47: Stamp vs. Flores on Prime Video").

**Para el filtro "eventos importantes" de la app, probablemente conviene quedarse solo con los ONE Fight Night (los grandes) y no los Friday Fights/Samurai semanales**, salvo que el usuario quiera el calendario completo.

## Streaming — CONFIRMADO para Chile
El sitio tiene páginas "how to watch" por país: `https://www.onefc.com/how-to-watch/cl/{event-slug}/` (redirige automático a `/cl/` al detectar geo Chile). Para los eventos grandes (ONE Fight Night) se confirmó explícitamente: **"ONE Fight Night 39: Rambolek vs. Dayakaev on Prime Video"**, con hora mostrada ya convertida a "-03 — Santiago". Es decir: **ONE Fight Night = Amazon Prime Video en Chile**, igual que la mayoría de los Fight Nights en Latam/US. Pendiente: confirmar streaming de los Friday Fights/Samurai (eventos chicos semanales) — probablemente vía el ONE Super App propio (gratis).
