# Progreso de investigación

## Estado del proyecto (2026-10-24, última actualización)

**MVP funcional construido y probado localmente.** Ver [README.md](README.md) para cómo correrlo. Resumen de qué está listo y qué falta:

✅ Listo y probado:
- Scripts de ingesta para UFC, Rugby (ESPN) y ONE Championship — corren sin API key, probados con datos reales.
- `scripts/build_report.py` — junta todo en `data/today.json`, probado end-to-end.
- `index.html` — página con filtros (deporte/app/horario), probada en desktop y mobile con datos reales.
- `.github/workflows/update-data.yml` — Action que corre 2x al día.
- Tabla de streaming Chile y lista de jugadores chilenos (`data/streaming_rules.json`, `data/followed_entities.json`), consolidadas de toda la investigación.

✅ Hecho (actualización 2026-10-25):
- Repo conectado y publicado: https://s-car1.github.io/Calendario_deportes/ (GitHub Action corriendo 2x/día, confirmado funcionando en los servidores de GitHub).
- Se reemplazó el enfoque con API keys (API-Football/balldontlie) por **scraping 100% gratis vía la API no oficial de ESPN** (mismo patrón que UFC) — cubre las 8 ligas de fútbol + Champions League + NBA + Euroliga + rugby, sin ninguna cuenta.
- Se sacó la lista REAL de equipos/ligas seguidos desde la cuenta de 365Scores del usuario (29 equipos, 31 ligas) y se reemplazó el borrador de `data/followed_entities.json`.
- Rediseño completo de `index.html`: grilla moderna con logos de equipos/ligas (vía ESPN), orden por relevancia (combinando gustos del usuario + importancia del partido, con auto-detección de clásicos), filtros por deporte/día/app/destacados. Probado en desktop y mobile.

⏳ Falta:
1. Validar que los logos/nombres de equipo calcen bien en casos raros (ej. equipos chicos sin logo en ESPN).
2. Ampliar cobertura a más ligas de la lista real de 365Scores si se justifica (Copa Chile, Top 14, Super Rugby, AmeriCup, etc. — ver `data/followed_entities.json -> leagues_followed_in_365scores`).
3. LNB Chile y Los Cóndores específicos siguen manuales (decisión ya tomada).


Estado: **investigación inicial completa** — 2026-10-24. Las 4 áreas (fútbol, básquet, combate/rugby, streaming Chile) están listas. Falta tu validación de las listas de jugadores y luego pasamos a construir.

Ver [PLAN.md](PLAN.md) para la arquitectura y el alcance acordado.

## Áreas en investigación

- [x] Fútbol: APIs de fixtures gratuitas + roster actual de chilenos en el extranjero (ver sección abajo, 2026-10-24)
- [x] Básquet: APIs de fixtures (NBA/Euroliga/LNB) + equipos actuales de Sebastián Herrera y Sebastián Carrasco (ver sección abajo, 2026-10-24)
- [x] Combate (UFC/One Championship) y Rugby (Cóndores/tier 1-2): fuentes oficiales, viabilidad de scraping (ver sección abajo, 2026-10-24)
- [x] Streaming en Chile: qué plataforma transmite cada liga/torneo/evento (ver tabla abajo, 2026-10-24)

Esta sección se va completando a medida que cada investigación termina.

## Tabla de streaming en Chile (investigado 2026-10-24, vía búsqueda web — verificar fecha a fecha porque los derechos cambian seguido)

| Liga / evento | Plataforma(s) en Chile | Notas / fuente |
|---|---|---|
| NBA | **Regla práctica confirmada: casi todos los partidos de temporada regular y playoffs van EN VIVO por HBO Max** (simulcast de cada partido que transmite TNT Sports, sea señal Premium o básica — la señal de cable cambia según el partido pero HBO Max los tiene todos). **Excepción: Play-In completo y Knockout Rounds de la NBA Cup van exclusivo por Prime Video** (sin TNT/HBO Max), y algunos playoffs/Finales también. ESPN/Disney+ solo partidos sueltos, ya no exclusividad. | Confirmado con ejemplo real (apertura de temporada, Thunder-Rockets y Lakers-Warriors ambos en vivo por HBO Max + señal TNT distinta cada uno). [Redgol](https://redgol.cl/redsport/nba-hoy-horario-y-donde-ver-en-vivo-todos-los-partidos-de-este-martes-21-de-octubre) — **Regla simplificada para la app: por defecto mostrar "HBO Max", y marcar "Prime Video" solo en fechas de Play-In / NBA Cup Knockout / Finales (fechas conocidas de antemano en el calendario oficial NBA), sin necesidad de scrapear señal partido por partido.** |
| Campeonato Nacional (Liga de Primera, Chile) | TNT Sports / TNT Sports Premium + HBO Max (principal), Canal 13 / 13.cl / Deportes 13 (1 partido por fecha gratis en TV abierta, reemplazó a Mega) | [DF.cl](https://www.df.cl/empresas/actualidad/canal-13-transmitira-el-campeonato-de-futbol-chileno-en-2026-tras-acuerdo), [Encancha](https://www.encancha.cl/futbol-chileno/primera/2026/01/22/confirmado-este-sera-el-canal-de-tv-abierta-que-transmitira-el-futbol-chileno-en-2026/) |
| Copa Libertadores | ESPN Premium + Disney+ (pago), Chilevisión/CHV (1 partido/semana gratis, también Pluto TV, chv.cl, YouTube CHV) | Copa Sudamericana no confirmada, falta buscar específico. [Redgol](https://redgol.cl/copa-libertadores/copa-libertadores-2026-partidos-horario-y-como-seguir-en-chile-la-fecha-1-de-la-fase-de-grupos) |
| LaLiga / Premier League / Ligue 1 | ESPN / ESPN2 / ESPN3, DGO, Disney+ Premium (mezclados, sin mapeo exacto liga→canal confirmado) | No confirmado con precisión qué liga va en qué señal exacta — revisar guía de ESPN/DGO antes de cada fecha. [FotMob TV guide Chile](https://www.fotmob.com/id/tv-guide/cl) |
| Liga Profesional Argentina | ESPN / Disney+ (según 365Scores) | Confirmación débil, conviene re-chequear. |
| Brasileirão | Kick (gratis, 76 partidos/temporada, 2 por fecha), Zapping con señal Fanatiz 1 (incluido en planes Plus/Cine/Cine Fútbol/Plus Fútbol/Full) | [Redgol](https://redgol.cl/noticias/completamente-gratis-confirman-la-senal-que-transmitira-el-brasileirao-en-chile-y-latam), [Descubre.vc](https://www.descubre.vc/noticia/zapping-suma-a-fanatiz-1-para-transmitir-el-brasileir-o-en-chile-2026-07-14) |
| UFC | **Paramount+** desde enero 2026 (exclusivo, incluido en suscripción ~$4.299/mes, sin PPV). Antes era Disney+ Premium/ESPN (ya no vigente) | Cambio grande de plataforma en 2026 — ojo que mucha info vieja en internet todavía dice ESPN/Disney+. [Ultimate Fighting Calendar](https://www.ufcalendar.com/es/how-to-watch/ufc-fight-night-288-2026-09-12), [El Mercurio Ecuador](https://elmercurio.com.ec/?p=1221763) |
| One Championship | No confirmado para Chile específicamente. Prime Video cubre Fight Nights pero enfocado en US/Canadá; Claro Sports tenía acuerdo histórico para Latam (sin Brasil) pero no se confirmó vigencia 2026 | Pendiente de más investigación (agente de combate lo está viendo también) |
| Rugby — Los Cóndores | ESPN (TV) + Disney+ (streaming), a veces también RugbyPass | Confirmado para partidos de Clasificatorio Mundial 2025. Rugby Championship / Nations Cup 2026 sin confirmar. [Encancha](https://www.encancha.cl/polideportivo/rugby/2025/09/05/juegan-los-condores-donde-ver-uruguay-vs-chile-y-que-necesitan-para-ir-al-mundial-de-rugby/) |
| Euroliga | "CDO" aparece como socio oficial en Chile para 2025/26 — no identificado qué es ni si transmite directo al público, falta confirmar | [Watchathletics](https://www.watchathletics.com/page/6191/uleb-euroleague-live-stream-and-tv-channels-by-country) |
| Liga Nacional de Básquetbol Chile (LNB) | TNT Sports + HBO Max (1 partido exclusivo por fecha, acuerdo para Torneo de Clausura 2026) | [Encancha](https://www.encancha.cl/polideportivo/basquetbol/2026/06/10/tnt-sports-confirma-transmision-de-la-liga-nacional-de-basquetbol-para-el-segundo-semestre-de-2026/) |

### Actualización zonas grises (segunda pasada, 2026-10-24)
- **Euroliga / "CDO"**: CDO = Canal del Deporte Olímpico, canal de TV de pago chileno (del Comité Olímpico de Chile), con planes "CDO" y "CDO+". Es el emisor oficial de Euroliga en Chile para 2025/26. Pendiente: confirmar si tiene app de streaming propia o solo cable.
- **Copa Sudamericana 2026**: repartida entre DSports, DGO, Amazon Prime Video, Disney+/ESPN según el partido — no hay una sola plataforma fija, cambia por encuentro (similar a Libertadores pero sin el partido gratis semanal confirmado en CHV). Hay que resolverlo con datos partido a partido, no con una regla fija.
- **LaLiga/Premier/Ligue1 mapeo exacto**: no se pudo confirmar una tabla fija liga→señal. Lo que sí: ESPN tiene Premier League asegurada en Latam hasta 2030-31 (renovación feb 2026) y LaLiga de forma no exclusiva hasta 2026 (ojo, vence este año, revisar qué pasa después). Ligue 1 sin dato. Conclusión: esta fila va a necesitar resolución partido a partido (vía API o guía de TV), no una regla fija simple.
- **One Championship en Chile**: Claro Sports tiene los derechos para toda Latam excepto Brasil (donde es Globo/Combate). No se confirmó specific channel/app en Chile, pero lo más probable es que sea a través de Claro Sports (canal/app ClaroSports). Falta confirmar si requiere ser cliente Claro o es con cuenta gratuita en clarosports.com.

## Básquet — APIs de fixtures y chilenos en el extranjero (investigado 2026-10-24)

| API | Cobertura útil | Límite gratis | Auth |
|---|---|---|---|
| **balldontlie.io** | Solo NBA (regular + playoffs). No Euroliga/LNB Chile. | ~5 req/min en el tier gratis (cifra de terceros, falta confirmar en el sitio). Stats avanzadas requieren plan pago. | API key gratis |
| **API-Basketball (api-sports.io)** | NBA confirmada; EuroLeague y LNB Chile sin confirmar (su doc bloqueó el fetch) — hay que probar `GET /leagues?search=euroleague` / `search=chile` con key gratis | ~100 req/día (estimado, comparte infra con API-Football) | API key |
| **EuroLeague** | No hay API oficial pública. Hay SDKs no oficiales (TS/R) que replican los endpoints del sitio — funcionan pero pueden romperse sin aviso | Sin límite formal, sin SLA | Sin auth (scrapers de endpoints públicos) |
| **TheSportsDB** | Cobertura de básquet no confirmada con precisión para NBA/Euroliga/LNB | No documentado con exactitud | API key simple |
| **LNB Chile** | **Sin API pública.** FeedConstruct tiene los derechos EXCLUSIVOS de datos/video de la LNB y LNB2 desde enero 2026 — ojo con esto si se scrapea, podría chocar con esos derechos. Fuente de fixtures: lnbchile.com + redes @chilelnb, sin endpoint documentado | — | — |

**Recomendación:** balldontlie.io para NBA, probar API-Basketball o el SDK no oficial para Euroliga, y para LNB Chile + jugadores chilenos en el exterior (pocos partidos) ir con seguimiento manual/curado en vez de scraping, dado el tema de derechos exclusivos de FeedConstruct.

**Jugadores chilenos de básquet en el exterior (confirmado):**
- **Sebastián Herrera** — Paris Basketball (Francia) — Betclic Élite / EuroLeague — contrato hasta fin de temporada 2026-27. Primer chileno en jugar EuroLeague.
- **Sebastián Carrasco** — Gimnasia y Esgrima de Comodoro Rivadavia — Liga Nacional de Básquet de Argentina — campeón y MVP de Finales 2025-26, contrato vigente hasta 2027.
- *(baja confianza, revisar antes de usar)* Ignacio Arroyo (posible Caja 87, Primera FEB España), Nico Carvacho y Manny Suárez (clubes actuales sin confirmar).

## UFC, One Championship y Rugby — fuentes de datos (investigado 2026-10-24)

**Hallazgo clave: ESPN tiene una API pública NO OFICIAL, gratis, sin API key, que cubre UFC y rugby completos.**
- UFC: `https://site.api.espn.com/apis/site/v2/sports/mma/ufc/scoreboard` (+ `?dates=YYYYMMDD` para otras fechas) → JSON con calendario completo de eventos UFC.
- Rugby por liga: `https://site.api.espn.com/apis/site/v2/sports/rugby/{leagueId}/scoreboard` — Six Nations `leagueId=180659`, International Test Match `leagueId=289234`. Falta el ID de "The Rugby Championship" y de la nueva "Nations Cup 2026" (torneo donde juegan Los Cóndores) — se puede sacar visitando espn.com/rugby/scoreboard y leyendo el parámetro `league=` en la URL.
- **Importante técnico:** hay que pedir estas URLs con header `User-Agent` de navegador y aceptando gzip (`curl -A "Mozilla/5.0" --compressed ...`), si no algunos clientes reciben 403 o la respuesta gzip sin descomprimir.
- Es una API no documentada oficialmente por ESPN (puede cambiar sin aviso) pero muy usada por la comunidad — conviene tener un fallback/cache si falla.
- ufc.com oficial: solo HTML server-rendered, sin endpoint `/api/` visible — descartado como fuente primaria (frágil).
- TheSportsDB: sin cobertura de MMA/UFC. APIs de pago (Sportradar, Zylalabs) descartadas por costo.

**One Championship:** no se encontró ninguna API pública ni gratuita confiable (ni oficial ni de terceros). onefc.com/events parece ser una SPA que podría tener un endpoint interno, pero no se pudo confirmar sin inspección de red con navegador real. **Recomendación: mantención manual** (son solo 1-2 eventos al mes, manejable).

**Los Cóndores (rugby chileno):** sin API confirmada. Calendario 2026 confirmado vía prensa (no la federación directamente, feracvi.cl no resolvió DNS al momento de la investigación — revisar si cambió de dominio): 4 julio vs Rumania (Estadio Nacional), 11 julio vs Hong Kong China (Sausalito, Viña del Mar), 18 julio vs Georgia (La Portada, La Serena), como parte de la nueva "World Rugby Nations Cup 2026". **Recomendación: mantención manual/semi-manual**, con la API de ESPN como respaldo automático si en algún momento ESPN trackea ese torneo.

### Resumen combate/rugby
| Deporte | Mejor opción | Tipo |
|---|---|---|
| UFC | API no oficial de ESPN (`mma/ufc/scoreboard`) | Automatizable, gratis |
| Rugby tier 1/2 (Six Nations, test matches) | API no oficial de ESPN (`rugby/{id}/scoreboard`) | Automatizable, gratis |
| One Championship | — | Manual |
| Los Cóndores / Nations Cup 2026 | — | Manual/semi-manual, con ESPN como respaldo a futuro |

## Fútbol — APIs de fixtures y chilenos en el extranjero (investigado 2026-10-24)

| API | Límite free | Cobertura | Broadcast info | Auth |
|---|---|---|---|---|
| **API-Football (api-sports.io)** | ~100 req/día, 10 req/min | La más completa: LaLiga, Premier, Ligue 1, Brasileirão, Liga Arg., Chile Primera División, Copa Libertadores y Sudamericana | No | API key simple en header |
| **football-data.org** | 10 req/min, 12 competiciones en free tier | Solo ligas europeas top (Champions, Premier, LaLiga, Bundesliga, Ligue1, Serie A, etc.) + Brasileirão. **No** cubre Libertadores/Sudamericana/Chile/Argentina | No | API key header |
| **TheSportsDB** | ~30 req/min (clave "test" compartida) | Cubre Chile Primera División (ID 4627) y Liga Argentina, Brasileirão. Libertadores/Sudamericana sin confirmar | No | API key en URL |
| **OpenLigaDB** | Sin key, sin límite | Solo fútbol alemán + algo de Champions/Premier/LaLiga. No sirve para Sudamérica | No | Sin auth |
| **Highlightly** | 100 req/día | Dice cubrir 950+ ligas, sin confirmar Chile/Libertadores específicamente | No (video/odds es pago) | API key |
| **SportMonks** | Free real: solo 2 ligas (Dinamarca/Escocia) | No sirve para este proyecto | No | API key |

**Recomendación: API-Football (api-sports.io) como fuente principal.** Es la única que cubre TODO lo que pedimos (Chile, Libertadores, Sudamericana, LaLiga, Premier, Ligue1, Argentina, Brasil) con 100 req/día gratis — alcanza sobrando para 1-2 refrescos diarios vía GitHub Actions. TheSportsDB sirve como respaldo gratuito para datos básicos de equipos. Ninguna API da info de "dónde se transmite" — eso seguirá siendo la tabla manual de streaming.

**Chilenos en el extranjero (fútbol) — borrador a validar, fichajes cambian rápido:**
- Alexis Sánchez — Sevilla — LaLiga (España)
- Ben Brereton Díaz — Southampton — Championship/Premier (Inglaterra)
- Marcelino Núñez — Ipswich Town — Championship (Inglaterra)
- Darío Osorio — FC Midtjylland — Superliga (Dinamarca), renovó hasta 2030 pero hay rumores de venta
- Gabriel Suazo — Toulouse FC — Ligue 1 (Francia), contrato hasta jun. 2026
- Rodrigo Echeverría — León — Liga MX (México)
- Damián Pizarro — Racing Club (préstamo desde Udinese) — Liga Profesional Argentina
- Felipe Loyola — dato débil, posiblemente Huachipato (Chile) — revisar
- **En Chile, NO en el extranjero** (ajustar si los seguías como "afuera"): Arturo Vidal (Colo-Colo), Lucas Assadi (U. de Chile)
- Claudio Bravo: sin confirmación de club activo, posible retiro/rol de comentarista ESPN

### Pendiente de confirmar / zonas grises (abierto)
- Confirmar si CDO (Euroliga) tiene app de streaming accesible sin cable.
- Copa Sudamericana y LaLiga/Premier/Ligue1: se resolverán con datos partido a partido (vía API de fixtures + guía de TV), no con una regla estática por liga.
- One Championship en Chile: confirmar acceso exacto vía Claro Sports (¿requiere ser cliente Claro?).
- Rugby Championship / Nations Cup 2026 (solo se confirmó para partidos de clasificatorio mundialista 2025, vía ESPN/Disney+).

## Actualización 2026-10-24 (segunda pasada): scraping real probado con navegador

Ver detalle técnico completo en [SCRAPING_NOTES.md](SCRAPING_NOTES.md). Resumen:
- **UFC**: calendario completo 2026 (52 eventos) obtenido y guardado en `data/ufc_calendar_2026.md` vía la API de ESPN. 100% automatizable.
- **One Championship**: calendario completo de próximos eventos obtenido por scraping HTML simple (sin Playwright) en `data/one_championship_calendar_2026.md`. **Streaming confirmado: Amazon Prime Video en Chile** para los eventos grandes "ONE Fight Night".
- **LNB Chile**: se encontró el sitio oficial real (lnbchile.com, con calendario/box scores muy completos), pero requiere Playwright (datos cargan client-side). **Decisión del usuario: queda como entrada manual**, no vale la pena automatizarlo — la temporada además está terminando.
- **Rugby/Los Cóndores**: sitio oficial chile.rugby confirmado funcionando (el DNS que falló antes era algo puntual), pero sin calendario estructurado para scrapear — sigue siendo manual.
- **365Scores**: se revisó si la cuenta del usuario estaba logueada en el navegador de la sesión — no lo estaba, no se pudo usar como atajo para ver sus equipos/ligas ya seleccionados.

## Conclusión: stack de datos recomendado (fuentes automatizables)

| Deporte/competencia | Fuente automática | Tipo |
|---|---|---|
| Fútbol (todas las ligas pedidas, incluido Chile/Libertadores/Sudamericana) | API-Football (api-sports.io), 100 req/día gratis | API, automatizable |
| NBA | balldontlie.io | API, automatizable |
| Euroliga | API-Basketball o SDK no oficial de EuroLeague | API/scraper, automatizable (con riesgo de romperse) |
| LNB Chile + jugadores chilenos de básquet en el exterior | — | Manual/curado (sin API; LNB tiene derechos exclusivos de FeedConstruct) |
| UFC | API no oficial de ESPN (`site.api.espn.com/.../mma/ufc/scoreboard`) | API, automatizable |
| Rugby tier 1/2 (Six Nations, test matches) | API no oficial de ESPN (`site.api.espn.com/.../rugby/{id}/scoreboard`) | API, automatizable |
| One Championship | — | Manual (1-2 eventos/mes) |
| Los Cóndores / Nations Cup 2026 | — | Manual/semi-manual |
| Streaming en Chile (qué app transmite qué) | — | Siempre manual, ninguna API lo da |

**Resumen:** la mayoría de lo importante SÍ se puede automatizar gratis (fútbol, NBA, UFC, rugby internacional). Quedan 4 cosas que son manuales por naturaleza: LNB Chile, jugadores chilenos de básquet en el exterior, One Championship, Los Cóndores/rugby chileno específico, y la tabla de streaming — pero son pocos eventos/partidos, manejable con una tabla simple que revisamos juntos cada tanto.

## Próximos pasos (actualizado)

1. **Que valides** las dos listas de jugadores chilenos en el extranjero (fútbol y básquet, en las secciones de arriba) y me digas si agrego/quito a alguien.
2. Crear cuenta gratis en api-sports.io (API-Football) y balldontlie.io para obtener las API keys (esto lo tienes que hacer tú, son cuentas personales).
3. Armar el script de GitHub Actions que junta: fixtures de fútbol/NBA/Euroliga/UFC/rugby vía API + tabla manual de streaming + tabla manual de LNB/One/Cóndores/jugadores chilenos de básquet.
4. Construir la página web con los filtros (deporte / app / horario).
5. Conectar este repo local a un repo remoto privado en tu GitHub.
