# Calendario Deportes — Plan del proyecto

Objetivo: reemplazar 365scores + FotMob + app NBA + búsquedas sueltas de UFC por **una sola página web** con el reporte de partidos de hoy + mañana, filtrable por deporte / app de streaming (Chile) / horario, con foco en las ligas y personas que me interesan.

## Decisiones de arquitectura (acordadas 2026-10-24)

- **Actualización de datos**: GitHub Action corriendo 1-2 veces al día (gratis, en la nube). No depende de ningún PC encendido.
- **Almacenamiento**: empezar simple — JSON/archivos de datos versionados en el repo (lo que el Action genera). Si crece mucho, migrar a una BD liviana (Supabase/SQLite) más adelante.
- **Frontend**: página web (artifact / sitio estático) con filtros por deporte, app, horario. Mobile-friendly.
- **Fuente de fixtures (fútbol + básquet)**: APIs deportivas gratuitas (API-Football / TheSportsDB u otra equivalente). Presupuesto: **100% gratis**, aceptando que la cobertura puede ser parcial para ligas chicas.
- **Transmisión en Chile (qué app transmite qué)**: no hay API confiable gratis para esto. Se mantiene como **tabla manual** que actualizamos juntos cuando cambie (ej. temporada NBA, cambios de derechos TV).
- **UFC / One Championship / Rugby (Cóndores y tier 1-2)**: sin API deportiva gratis confiable. Se resuelve con **scraping de fuentes oficiales globales** (ufc.com, onefc.com, World Rugby / unión de rugby de Chile) en el mismo GitHub Action. Si el scraping resulta muy frágil, caemos a mantención manual semanal como respaldo.
- **Repo**: nuevo repo privado en GitHub, inicializado aquí mismo (`git init` ya hecho). Falta conectarlo a GitHub (crear el repo remoto y hacer push) cuando tengamos el primer contenido.
- **Ventana del reporte**: hoy + mañana.

## Alcance MVP (deportes incluidos ahora)

### Fútbol
- Chile Primera División (**prioridad: Colo-Colo**, siempre destacado si juega)
- Copa Libertadores / Copa Sudamericana
- LaLiga, Premier League, Ligue 1
- Liga Profesional Argentina, Brasileirão
- Chilenos jugando en el extranjero (ver lista draft abajo)
- Criterio de "importante" en cualquier liga: finales, partidos eliminatorios/playoffs, clásicos, duelos entre primeros lugares

### Básquetbol
- NBA completa
- Euroliga
- Liga Nacional de Básquetbol de Chile (LNB)
- Jugadores chilenos específicos en el exterior (ver lista draft abajo)

### Combate / Rugby
- UFC: todos los eventos completos (main + prelims)
- One Championship: eventos completos
- Rugby: Los Cóndores (selección chilena) + partidos relevantes tier 1 / tier 2

## Draft lista de chilenos a seguir (a validar/ajustar contigo)

**Fútbol (referencia — objetivo real es "todos los chilenos relevantes en el extranjero", esta es una lista base de arranque, hay que revisarla porque los planteles cambian):**
- Alexis Sánchez
- Arturo Vidal
- Ben Brereton Díaz
- Claudio Bravo
- Marcelino Núñez
- Darío Osorio
- Gabriel Suazo
- Rodrigo Echeverría
- (lista a completar/corregir contigo — rosters de fútbol cambian seguido, por lo que probablemente convenga una lógica más genérica: "jugador chileno + equipo" como tabla editable fácil de actualizar, no hardcodeada en el código)

**Básquetbol:**
- Sebastián Herrera (Paris Basketball, a confirmar equipo actual)
- Sebastián Carrasco (Comodoro Rivadavia / liga argentina, a confirmar equipo actual)
- (agregar otros si los sigues)

## Riesgos / cosas abiertas

1. **APIs gratis de fútbol/básquet suelen tener rate limits bajos** (ej. 100 requests/día) — hay que diseñar el Action para pedir lo mínimo necesario y cachear.
2. **Scraping de UFC/One/Rugby es frágil** — si cambian el HTML de sus sitios, se rompe. Hay que avisar cuando falle (ej. un paso del Action que marque error visible) en vez de fallar en silencio.
3. **Tabla de transmisión en Chile** es manual por naturaleza — hay que decidir cada cuánto la revisamos (sugerido: al inicio de cada temporada o cuando algo cambie).
4. **Lista de "chilenos en el extranjero"** cambia con las ventanas de pases — conviene que sea una tabla editable simple (no algo que yo deba tocar código para actualizar).

## Próximos pasos

1. Validar contigo esta lista de jugadores y la tabla de transmisión actual (NBA: ESPN/Disney+, HBO Max, Prime — confirmar fútbol chileno, Champions, etc.)
2. Elegir y probar la API de fixtures (fútbol + básquet) gratuita concreta
3. Armar el primer script de scraping/consulta y el GitHub Action
4. Construir la página web con los filtros
5. Crear el repo remoto en GitHub y conectar el Action
