# Contenidos por marca

Calendario de 3 meses y publicaciones de 4 semanas para K&G Market, Klean N Green NYC, JDET Capital y Klean N Green Perú.
Todo vive en un solo archivo, `contenidos-por-marca.html`, con una pestaña por marca. El archivo completo está en inglés; solo los captions de K&G Market son bilingües (inglés y español) a propósito, porque se publican así en Metricool.

## Cómo está armado el HTML

- **Resumen:** fases, semanas, revisiones, reglas de ajuste y fechas clave de las cuatro marcas.
- **K&G Market y Klean NYC:** pestañas Calendar, Overview y Week 1 a Week 4 (con prompts, guiones y captions).
- **JDET Capital y Klean Perú:** solo Calendario.

## Cómo regenerarlo

```
python3 build_all.py
```

Genera `contenidos-por-marca.html` en la raíz. Solo usa la biblioteca estándar de Python 3. La interfaz compartida sale en inglés cuando `CONTENT_LANG=en` (es el valor por defecto de los tres scripts del HTML unificado); `src/build_estrategia.py` ejecutado solo genera la página de estrategia en español. Los HTML intermedios quedan en `src/` y no se suben.

## Dónde se cambia cada cosa (`src/`)

| Archivo | Qué contiene |
| --- | --- |
| `build_estrategia.py` | Estilos, componentes y fuentes compartidos |
| `build_publicaciones.py` | Posts de Klean NYC (semanas 1 a 4) |
| `build_kg_publicaciones.py` | Posts de K&G Market y los Overview de ambas marcas |
| `characters.py` | Los 4 personajes IA recurrentes (Rosa y Dre en K&G Market; Maya y Daniel en Klean NYC): aspecto fijo, voz, retratos de referencia, mapa de qué pieza usa a quién |
| `tiktok_data.py`, `tiktok_html.py` | Los 16 TikToks (guion, prompt, caption, borrador de Metricool) y la sección «Characters» de ambos Overview |
| `kn_timeback.py` | Estrategia «tiempo recuperado» de Klean NYC: tipo de cada pieza (25 de tiempo recuperado, 13 de consejo con puente), textos nuevos de las semanas 1 a 4 y líneas puente |
| `linkedin_video.py` | Los 2 videos de LinkedIn de Klean NYC (25 nov y 2 dic) |
| `build_calendario.py` | Calendario de 3 meses (en inglés) de las cuatro marcas |
| `build_unificado.py` | Une calendario y posts en el HTML final |

## Metricool

| Marca | brandId |
| --- | --- |
| Klean N Green NYC | 7768295 |
| K&G Market | 7762750 |
| Klean N Green Perú | 7768301 |
| JDET Capital | 7768317 |

- Los cambios en el HTML no modifican Metricool, ni al revés. Si un cambio afecta a ambos, se hace en los dos.
- Los borradores de Metricool no se pueden borrar desde la API: antes de crear muchos, conviene confirmar el plan.
- Nada se publica en redes sin aprobación. No se tocan las publicaciones ya programadas.

## Estrategia de Klean NYC: tiempo recuperado

- Mensaje central: contratar a Klean N Green NYC le da al cliente tiempo para hacer lo que antes no podía. 2 de cada 3 piezas lo muestran; las demás son consejos que cierran con un puente al servicio.
- Semanas 1 y 2 ya están programadas en Metricool con su imagen o video: solo se propone cambiar el texto (se muestra el texto actual y el nuevo). Semanas 3 y 4 están reescritas por completo como borradores.
- Estado: propuesta para revisión. Metricool no se modifica hasta que cada pieza esté aprobada.

## Estado del SEO de los sitios (9 de noviembre de 2026)

- **Klean N Green NYC (kleannyc.com):** texto alternativo en imágenes, un solo H1 en las 8 páginas de servicio, 3 redirecciones 301 nuevas, /dtut/ y /new-clients/ en noindex, teléfono del pie corregido a (347) 883-4766.
- **K&G Market (kngmarket.com):** Yoast SEO instalado y configurado; títulos y descripciones en páginas y categorías; un H1 por página; texto alternativo en 1.894 imágenes de producto; se quitó el noindex de WordPress; sitemap enviado a Search Console y la home enviada a indexar. Puede tardar de días a semanas en aparecer en Google.
- **Pendiente de decisión:** las páginas /post-renovation-cleaning/ y /post-construction-cleaning/ de Klean repiten el mismo texto (reescribir una, redirigir o marcar canonical). Teléfono de K&G sin confirmar (347-365-9656 en el sitio y en Google, 347-739-5457 en un extracto de Facebook). Actualizaciones de plugins y tema en ambos sitios. Horarios especiales de feriados de K&G (los `[hours]` de los captions).
- Los cambios del sitio se hicieron directamente en WordPress; no hay código del sitio en este repositorio. Solo se actualizaron las notas del HTML.

## Revisiones previstas

Viernes 20 de noviembre, 4 de diciembre, 18 de diciembre y 29 de enero.

## Personajes (`src/characters.py`)

- Dos personajes IA recurrentes por marca: Rosa y Dre (K&G Market), Maya y Daniel (Klean NYC, junto a Clover el gato). Son anfitriones, no empleados ni clientes; todo lo que los muestra se rotula como IA.
- El aspecto de cada uno (`look`, `outfit`, `hands`) se escribe una sola vez en `CHARS`; todos los prompts de video e imagen lo toman de ahí. Cambiar una línea y ejecutar `python3 build_all.py` actualiza todos los prompts.
- Quién aparece en cada pieza: TikToks y videos de LinkedIn en los diccionarios `TT` y `LI` de `characters.py`; Reels e imágenes en `build_kg_publicaciones.py` (K&G) y en `build_publicaciones.py` / `kn_timeback.py` (Klean).
- Los personajes no cambian ningún borrador de Metricool: los captions siguen igual. No aparecen en las semanas 1 y 2 de Klean (ya programadas con material terminado), ni en el TikTok del 10 de noviembre, ni en los posts de Google, las Stories y la foto del equipo de K&G.
