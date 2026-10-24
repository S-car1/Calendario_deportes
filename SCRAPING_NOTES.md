# Notas técnicas de scraping (investigación práctica, 2026-10-24)

Esto complementa [PROGRESS.md](PROGRESS.md) con hallazgos concretos de scraping/API reales probados con el navegador (no solo lo que reportaron los agentes de investigación).

## UFC — CONFIRMADO, automatizable 100%
`https://site.api.espn.com/apis/site/v2/sports/mma/ufc/scoreboard` con header `User-Agent` de navegador da el **calendario completo 2026: 52 eventos**, de enero a diciembre. Probado y guardado en [data/ufc_calendar_2026.md](data/ufc_calendar_2026.md) (y el JSON crudo en `data/ufc_calendar_2026_raw.json`). Esto es mejor de lo esperado — no hace falta scraping de HTML para UFC, es una API JSON limpia.

## ONE Championship — CONFIRMADO, automatizable con scraping HTML simple (sin Playwright)
`https://www.onefc.com/events/` es HTML server-renderizado plano — se puede extraer con un fetch + parser simple (BeautifulSoup/cheerio), sin necesidad de ejecutar JavaScript. Ya probado: se obtuvo el calendario completo de eventos próximos (ver [data/one_championship_calendar_2026.md](data/one_championship_calendar_2026.md)).

**Streaming confirmado para Chile:** existe una página por país `https://www.onefc.com/how-to-watch/cl/{event-slug}/` que redirige automático al detectar Chile, y confirma explícitamente que los eventos grandes "ONE Fight Night" se transmiten por **Amazon Prime Video** en Chile (hora ya convertida a "-03 Santiago"). Los eventos chicos (Friday Fights, Samurai) probablemente van por el ONE Super App propio — falta confirmar.

## LNB Chile (básquet chileno) — sitio oficial encontrado, pero queda FUERA del alcance automatizado (decisión del usuario, 2026-10-24)
Se encontró el sitio oficial real: **lnbchile.com** (el dominio lnb.cl está parqueado/no es el oficial; se confirmó vía la ficha de la app oficial "LNBCHILE" en la App Store). El sitio tiene un calendario completo con resultados, marcador por cuarto, box score y hasta shot charts — pero los datos se cargan 100% client-side después de hidratar React (no hay API JSON expuesta ni HTML con los datos ya renderizado), así que requeriría Playwright/navegador headless para scrapear, no un simple `curl`/`fetch`.

**Decisión:** dado que la temporada está terminando y es la fuente más difícil de las 4 manuales, **LNB Chile se mantiene como entrada manual/curada** en vez de invertir en scraping con Playwright. Si más adelante se justifica, el camino técnico ya está mapeado (Playwright contra `lnbchile.com/liga/uno/calendario`).

## Rugby Los Cóndores — sitio oficial confirmado funcionando, pero sin calendario estructurado
El sitio oficial es **chile.rugby** (la búsqueda anterior decía que no resolvía DNS, pero al probarlo directo sí funciona). Es un sitio de noticias/WordPress sin una página de fixture estructurada y scrapeable — el calendario se menciona en posts de Instagram embebidos, no en una tabla HTML. **Se mantiene como manual**, consistente con lo ya decidido para UFC/One/Rugby en el plan original.

## Pendiente de revisar (si se quiere seguir)
- NBA: mapeo exacto de qué señal (TNT Sports Premium / HBO Max / Prime Video / ESPN) transmite cada partido específico — no se encontró todavía una página con el calendario completo de señales por partido; puede necesitar revisar la programación oficial de TNT Sports Chile o HBO Max directamente.
- 365Scores: se revisó si la cuenta del usuario estaba logueada en el navegador — **no lo estaba** (la sección "My Scores" aparece vacía, "Select Teams and Leagues"), así que no se pudo usar como atajo para ver sus ligas/equipos ya seleccionados. Si el usuario quiere, puede loguearse él mismo en el navegador y luego revisamos juntos qué tiene seleccionado — no es algo que deba hacer por él (no se ingresan credenciales de cuentas reales).
