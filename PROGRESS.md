# Progreso de investigación

Estado: investigación inicial en curso (agentes lanzados en paralelo) — 2026-10-24.

Ver [PLAN.md](PLAN.md) para la arquitectura y el alcance acordado.

## Áreas en investigación

- [ ] Fútbol: APIs de fixtures gratuitas + roster actual de chilenos en el extranjero (agente en curso)
- [ ] Básquet: APIs de fixtures (NBA/Euroliga/LNB) + equipos actuales de Sebastián Herrera y Sebastián Carrasco (agente en curso)
- [ ] Combate (UFC/One Championship) y Rugby (Cóndores/tier 1-2): fuentes oficiales, viabilidad de scraping (agente en curso)
- [x] Streaming en Chile: qué plataforma transmite cada liga/torneo/evento (ver tabla abajo, 2026-10-24)

Esta sección se va completando a medida que cada investigación termina.

## Tabla de streaming en Chile (investigado 2026-10-24, vía búsqueda web — verificar fecha a fecha porque los derechos cambian seguido)

| Liga / evento | Plataforma(s) en Chile | Notas / fuente |
|---|---|---|
| NBA | TNT Sports + HBO Max (principal, 120 partidos/temporada, exclusivo), Prime Video (Play-In, algunos playoffs, Finales), ESPN/Disney+ (partidos sueltos, ya sin exclusividad) | Cambia de señal según el día del partido. [Redgol](https://redgol.cl/redsport/golpazo-en-las-transmisiones-tnt-sports-chile-le-arrebata-la-nba-a-espn-y-disney), [Prensafutbol](https://www.prensafutbol.cl/nba-2026-2027-donde-y-como-ver-en-chile/) |
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

### Pendiente de confirmar / zonas grises (abierto)
- Confirmar si CDO (Euroliga) tiene app de streaming accesible sin cable.
- Copa Sudamericana y LaLiga/Premier/Ligue1: se resolverán con datos partido a partido (vía API de fixtures + guía de TV), no con una regla estática por liga.
- One Championship en Chile: confirmar acceso exacto vía Claro Sports (¿requiere ser cliente Claro?).
- Rugby Championship / Nations Cup 2026 (solo se confirmó para partidos de clasificatorio mundialista 2025, vía ESPN/Disney+).
