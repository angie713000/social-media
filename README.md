# Contenidos por marca

Calendario de 3 meses y publicaciones de 4 semanas para K&G Market, Klean N Green NYC, JDET Capital y Klean N Green Perú.
Todo vive en un solo archivo, `contenidos-por-marca.html`, con una pestaña por marca.

## Cómo está armado el HTML

- **Resumen:** fases, semanas, revisiones, reglas de ajuste y fechas clave de las cuatro marcas.
- **K&G Market y Klean NYC:** pestañas Calendario (español), Overview y Week 1 a Week 4 (posts en inglés, con prompts, guiones y captions).
- **JDET Capital y Klean Perú:** solo Calendario.

## Cómo regenerarlo

```
python3 build_all.py
```

Genera `contenidos-por-marca.html` en la raíz. Solo usa la biblioteca estándar de Python 3. Los HTML intermedios quedan en `src/` y no se suben.

## Dónde se cambia cada cosa (`src/`)

| Archivo | Qué contiene |
| --- | --- |
| `build_estrategia.py` | Estilos, componentes y fuentes compartidos |
| `build_publicaciones.py` | Posts de Klean NYC (semanas 1 a 4) |
| `build_kg_publicaciones.py` | Posts de K&G Market y los Overview de ambas marcas |
| `tiktok_data.py`, `tiktok_html.py` | Los 16 TikToks con presentador IA (guion, prompt, caption, borrador de Metricool) |
| `linkedin_video.py` | Los 2 videos de LinkedIn de Klean NYC (25 nov y 2 dic) |
| `build_calendario.py` | Calendario de 3 meses en español de las cuatro marcas |
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

## Revisiones previstas

Viernes 20 de noviembre, 4 de diciembre, 18 de diciembre y 29 de enero.
