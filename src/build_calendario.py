#!/usr/bin/env python3
# Genera calendario-contenidos.html reutilizando estilos y scripts de build_estrategia.py
import datetime as dt
import io
import contextlib

with contextlib.redirect_stdout(io.StringIO()):
    import build_estrategia as B

OUT = "calendario-contenidos.html"
e, fmt, chip = B.e, B.fmt, B.chip

DAYS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
MON = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
MONF = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
START = dt.date(2026, 11, 9)


def D(m, d):
    return dt.date(2026 if m >= 11 else 2027, m, d)


def week_range(n):
    a = START + dt.timedelta(days=7 * (n - 1))
    b = a + dt.timedelta(days=6)
    if a.month == b.month:
        return f"{a.day} al {b.day} de {MONF[b.month-1]}"
    return f"{a.day} de {MONF[a.month-1]} al {b.day} de {MONF[b.month-1]}"


def short_range(n):
    a = START + dt.timedelta(days=7 * (n - 1))
    b = a + dt.timedelta(days=6)
    if a.month == b.month:
        return f"{a.day} al {b.day} {MON[b.month-1]}"
    return f"{a.day} {MON[a.month-1]} al {b.day} {MON[b.month-1]}"


def row(wd, m, d, hour, title, meta, kind, note=""):
    date = D(m, d)
    assert DAYS[date.weekday()] == wd, f"Fecha incoherente: {wd} {d}/{m} es {DAYS[date.weekday()]}"
    return B.slot(f"{wd} {d} {MON[m-1]}", hour, title, meta, kind, note)


def week_block(n, rows, note=""):
    body = "".join(rows)
    n_html = f'<p class="note">{fmt(note)}</p>' if note else ""
    return (
        f'<h4 class="wkh">Semana {n}<span>{e(week_range(n))}</span></h4>'
        f'<ul class="slots">{body}</ul>{n_html}'
    )


def wrow(n, theme, text, key="", phase=""):
    ph = {1: "Base", 2: "Temporada", 3: "Consolidación"}[1 if n <= 4 else 2 if n <= 8 else 3]
    k = f'<p class="wk">{fmt(key)}</p>' if key else ""
    return (
        '<li class="wrow">'
        f'<div><p class="wn">S{n}</p><p class="wd">{e(short_range(n))}</p></div>'
        f'<div><p class="wt">{fmt(theme)} <span class="ph">{ph}</span></p><p class="wp">{fmt(text)}</p>{k}</div></li>'
    )


def wlist(items):
    return '<ul class="wlist">' + "".join(items) + "</ul>"


section, callout, tagbox, kpis = B.section, B.callout, B.tagbox, B.kpis

import sys as _sys
_sys.path.insert(0, ".")
import tiktok_data as T

TT_ES = {
    "KG1": "Ají amarillo: el sabor de la cocina peruana",
    "KG2": "Plátano verde, amarillo o negro: para qué sirve cada uno",
    "KG3": "Arroz con frijoles caribeño: el scotch bonnet entero",
    "KG4": "¿Está maduro tu mango? Sin mirar el color",
    "KG5": "Un acompañante nuevo para la mesa de Thanksgiving",
    "KG6": "Cómo elegir una piña dulce",
    "KG7": "Cómo elegir la yuca (y nunca comerla cruda)",
    "KG8": "Cinco productos para empezar a cocinar peruano y caribeño",
    "KN1": "Mito: más producto no limpia más",
    "KN2": "Limpiar en orden: de arriba hacia abajo",
    "KN3": "Día de rotación: el orden que ahorra tiempo",
    "KN4": "Nunca mezcles estos dos productos de limpieza",
    "KN5": "Recibir invitados: 15 minutos antes de que lleguen",
    "KN6": "Cuatro preguntas antes de contratar una empresa de limpieza",
    "KN7": "Tres errores que esparcen la suciedad",
    "KN8": "Cuatro puntos para limpiar una vez al mes",
}


def tt(pid):
    p = next(x for x in T.P if x["id"] == pid)
    y, m, d = (int(v) for v in p["date"].split("-"))
    wd = DAYS[dt.date(y, m, d).weekday()]
    return row(wd, m, d, "18:00", f"TikTok: {TT_ES[pid]}",
               f"TikTok ({T.HANDLE[p['brand']]}), video de unos 18 s con presentador IA distinto en cada video",
               "hip",
               "Borrador en Metricool con una foto provisoria: subir el video y marcar «contenido generado por IA». Guion y prompt en las pestañas Week 1 a Week 4 de esta marca.")

import linkedin_video as LV

LI_ES = {
    "LI1": "Video: cuatro datos que enviar antes de contratar una limpieza",
    "LI2": "Video: unidad vacía en las fiestas, cuatro cosas que hacer antes",
}


def li(pid):
    p = next(x for x in LV.L if x["id"] == pid)
    y, m, d = (int(v) for v in p["date"].split("-"))
    wd = DAYS[dt.date(y, m, d).weekday()]
    return row(wd, m, d, "11:00", LI_ES[pid],
               "LinkedIn, video cuadrado de unos 30 s con presentador IA, B2B",
               "hip",
               "Borrador en Metricool solo con el texto (ya incluye «AI-generated video.»): subir el video y activar subtítulos. Guion y prompts en las pestañas Week 3 y Week 4 de esta marca.")


# ---------------------------------------------------------------------------
# K&G MARKET
# ---------------------------------------------------------------------------
kg = ""
kg += section(
    "Semanas 1 a 4: día por día (hora de Nueva York)",
    callout(
        "Tres publicaciones por semana, las historias del sábado y dos TikToks con presentadores IA (martes y jueves a las 18:00; en la semana 3, martes y miércoles por Thanksgiving). Los productos entre corchetes se confirman con la tienda. El ají amarillo y la chicha morada ya aparecen en publicaciones de la cuenta.",
        "Ritmo.",
    )
    + week_block(
        1,
        [
            row("Lun", 11, 9, "10:00", "Llegó hoy: ají amarillo", "Facebook e Instagram, foto", "ref", "Llegó hoy. Conjunto «Producto peruano»."),
            tt("KG1"),
            row("Mié", 11, 11, "12:00", "Reel: tres usos del ají amarillo", "Facebook e Instagram, Reel de 15 a 30 s", "ref", "Cómo se usa. Conjunto «Producto peruano»."),
            tt("KG2"),
            row("Vie", 11, 13, "10:00", "Quién atiende la tienda", "Facebook e Instagram, foto del equipo con su permiso", "ref", "Gente y barrio. Conjunto «Base local»."),
            row("Sáb", 11, 14, "10:00", "Historias: tienda abierta, producto de la semana y horario", "Instagram y Facebook, 3 historias", "ref", "Información útil."),
        ],
    )
    + week_block(
        2,
        [
            row("Lun", 11, 16, "10:00", "Llegó hoy: [producto caribeño]", "Facebook e Instagram, foto", "ref", "Llegó hoy. Conjunto «Producto caribeño»."),
            tt("KG3"),
            row("Mié", 11, 18, "12:00", "Reel: [plato caribeño] con ingredientes de la tienda", "Facebook e Instagram, Reel", "ref", "Cómo se usa. Conjunto «Producto caribeño»."),
            tt("KG4"),
            row("Vie", 11, 20, "10:00", "Aviso: pedidos y horario de Thanksgiving", "Facebook e Instagram, imagen única", "ref", "Ofertas y temporada. Conjunto «Temporada»."),
            row("Sáb", 11, 21, "10:00", "Historias: qué hay hoy y cómo pedir con anticipación", "Instagram y Facebook, 3 historias", "ref", "Información útil."),
        ],
        "Revisión 1 el viernes 20 de noviembre.",
    )
    + week_block(
        3,
        [
            row("Lun", 11, 23, "10:00", "Thanksgiving: productos para tu mesa", "Facebook e Instagram, carrusel de 3 imágenes", "ref", "Ofertas y temporada. Conjunto «Temporada»."),
            tt("KG5"),
            row("Mié", 11, 25, "12:00", "Reel: [plato] para la mesa de Thanksgiving", "Facebook e Instagram, Reel", "ref", "Cómo se usa. Conjunto «Temporada»."),
            tt("KG6"),
            row("Vie", 11, 27, "10:00", "Sábado de pequeños negocios: ven a conocernos", "Facebook e Instagram, imagen única", "ref", "Gente y barrio. Conjunto «Base local»."),
            row("Sáb", 11, 28, "10:00", "Historias: Small Business Saturday en la tienda", "Instagram y Facebook, 3 historias", "ref", "Gente y barrio."),
        ],
        "Jueves 26 (Thanksgiving): sin publicación fija; una historia de saludo si se desea. Confirmar el horario de la tienda del jueves 26 y del viernes 27.",
    )
    + week_block(
        4,
        [
            row("Lun", 11, 30, "10:00", "Llegó hoy: [producto], reposición después de Thanksgiving", "Facebook e Instagram, foto", "ref", "Llegó hoy. Conjunto «Producto peruano»."),
            tt("KG7"),
            row("Mié", 12, 2, "12:00", "Reel: chicha morada en casa, paso a paso", "Facebook e Instagram, Reel", "ref", "Cómo se usa. Conjunto «Bebidas y tradiciones»."),
            tt("KG8"),
            row("Vie", 12, 4, "10:00", "Diciembre en K&G: horarios y pedidos de Navidad", "Facebook e Instagram, imagen única", "ref", "Ofertas y temporada. Conjunto «Temporada»."),
            row("Sáb", 12, 5, "10:00", "Historias: tienda abierta y producto de la semana", "Instagram y Facebook, 3 historias", "ref", "Información útil."),
        ],
        "Revisión 2 el viernes 4 de diciembre. Con sus resultados se detallan las semanas 5 a 8.",
    ),
)
kg += section(
    "Semanas 5 a 13: tema de cada semana",
    callout("Desde la semana 5 se mantienen los dos TikToks semanales con un presentador IA distinto en cada video. Sus temas se definen en cada revisión, según lo que haya funcionado.") + wlist(
        [
            wrow(5, "Mesa de Navidad, primera parte", "Producto para platos de fiestas, un Reel de un plato navideño y el aviso de horarios.", "Martes 8: feriado en Perú."),
            wrow(6, "Pedidos y horarios de Navidad", "Fecha límite de pedidos anticipados y horarios especiales, producto por producto.", "Revisión 3 el viernes 18 de diciembre."),
            wrow(7, "Nochebuena y Navidad", "Dos publicaciones más historias con saludo y horarios del 24 y el 25. Sin publicación fija el 25.", "Jueves 24 y viernes 25."),
            wrow(8, "Cierre de año y Año Nuevo", "Ideas para la cena del 31, resumen del año en fotos de la tienda y saludo del 1 de enero.", "Jueves 31 y viernes 1 de enero."),
            wrow(9, "Día de Reyes y despensa del año", "Producto de la semana, publicación de Reyes con los productos disponibles y un Reel de receta.", "Miércoles 6: Día de Reyes."),
            wrow(10, "Platos de invierno", "Caldos y guisos con ingredientes de la tienda. Un Reel por semana, o dos si superó el umbral de 150 vistas."),
            wrow(11, "Gente y barrio", "Clientes y recetas de la comunidad con su permiso, y la historia del equipo.", "Lunes 18: feriado federal en EE. UU.; confirmar horario."),
            wrow(12, "Repetir lo que funcionó", "Los tres formatos con más alcance de los dos primeros meses.", "Revisión 4 el viernes 29 de enero."),
            wrow(13, "Puente al siguiente trimestre", "Primeras piezas del plan de febrero a abril definido en la revisión 4."),
        ]
    ),
)
kg += section(
    "Conjuntos de hashtags del calendario",
    '<p class="lead-s">Cinco por publicación en Instagram y hasta tres en Facebook.</p>'
    + tagbox("Base local", "#KGMarket #BrooklynEats #BrooklynFood #NYCFood")
    + tagbox("Producto peruano", "#KGMarket #BrooklynEats #PeruvianFood #AjiAmarillo #ComidaPeruana")
    + tagbox("Producto caribeño", "#KGMarket #BrooklynEats #CaribbeanFood #CaribbeanCuisine #BrooklynFood")
    + tagbox("Bebidas y tradiciones", "#KGMarket #ChichaMorada #PeruvianFood #NYCFood #BrooklynFood")
    + tagbox("Temporada", "#KGMarket #ThanksgivingFood #HolidayTable #BrooklynEats #NYCFood"),
)

# ---------------------------------------------------------------------------
# KLEAN N GREEN NYC
# ---------------------------------------------------------------------------
kn = ""
kn += section(
    "Semanas 1 a 4: día por día (hora de Nueva York)",
    callout(
        "Plan completo de 7 días: lunes Google, martes LinkedIn, miércoles Instagram y Facebook (carrusel), jueves LinkedIn, viernes Reel, sábado imagen única en Instagram y Facebook, domingo Instagram (carrusel). Plan mínimo: martes, miércoles y jueves. El Reel y la imagen única son formatos nuevos y se miden como hipótesis desde la revisión 1. A eso se suman dos TikToks por semana con presentadores IA a las 18:00 (martes y jueves; en la semana 3, martes y viernes). Además, dos videos de LinkedIn con presentador IA, los miércoles 25 de noviembre y 2 de diciembre a las 11:00.",
        "Ritmo.",
    )
    + week_block(
        1,
        [
            row("Lun", 11, 9, "10:00", "Google: qué hace Klean N Green NYC", "Perfil de Empresa de Google, publicación con botón", "ref", "Borrador en Metricool (solo texto). La imagen y el botón se agregan en el editor."),
            row("Mar", 11, 10, "11:00", "Checklist «Turnover week: 5 checks» para administradores", "LinkedIn", "ref", "Checklists y guías. Conjunto «LinkedIn, administración de propiedades»."),
            tt("KN1"),
            row("Mié", 11, 11, "12:00", "Carrusel: la cocina en 6 puntos que se pasan por alto", "Instagram y Facebook, carrusel", "ref", "Checklists y guías. Conjuntos «Instagram, hogares» y «Facebook»."),
            row("Jue", 11, 12, "11:00", "Qué incluye la limpieza de oficinas", "LinkedIn", "ref", "Servicios explicados. Conjunto «LinkedIn, oficinas»."),
            tt("KN2"),
            row("Vie", 11, 13, "12:00", "Reel: 3 limpiezas rápidas del baño", "Instagram y Facebook, Reel de unos 12 segundos", "hip", "Checklists y guías. Conjunto «Instagram, Reels»."),
            row("Sáb", 11, 14, "11:00", "Imagen única: primera limpieza, los 4 datos que hay que enviar", "Instagram y Facebook, imagen única", "hip", "Servicios explicados. Conjunto «Instagram, sábados»."),
            row("Dom", 11, 15, "18:00", "«Sunday reset»: 20 minutos, 6 puntos", "Instagram, carrusel", "hip", "Checklists y guías. Conjunto «Instagram, hogares»."),
        ],
    )
    + week_block(
        2,
        [
            row("Lun", 11, 16, "10:00", "Google: limpiezas entre inquilinos o huéspedes", "Perfil de Empresa de Google, publicación con botón", "ref", "Borrador en Metricool (solo texto)."),
            row("Mar", 11, 17, "11:00", "Cómo se verifica una unidad antes de entregarla, en 3 pasos", "LinkedIn", "ref", "Equipo y proceso. Conjunto «LinkedIn, administración de propiedades»."),
            tt("KN3"),
            row("Mié", 11, 18, "12:00", "Carrusel: 20 minutos antes de recibir invitados", "Instagram y Facebook, carrusel", "ref", "Checklists y guías. Conjuntos «Instagram, hogares» y «Facebook»."),
            row("Jue", 11, 19, "11:00", "Reseña de un cliente, con su autorización", "LinkedIn", "ref", "Reseñas. Conjunto «LinkedIn, administración de propiedades»."),
            tt("KN4"),
            row("Vie", 11, 20, "12:00", "Reel: rieles de ventanas, el punto que nadie limpia", "Instagram y Facebook, Reel de unos 12 segundos", "hip", "Checklists y guías. Conjunto «Instagram, Reels»."),
            row("Sáb", 11, 21, "11:00", "Imagen única: ¿cada cuánto limpiar?", "Instagram y Facebook, imagen única", "hip", "Servicios explicados. Conjunto «Instagram, sábados»."),
            row("Dom", 11, 22, "18:00", "Entrada y recibidor: la primera impresión en 5 puntos", "Instagram, carrusel", "hip", "Checklists y guías. Conjunto «Instagram, hogares»."),
        ],
        "Revisión 1 el viernes 20 de noviembre: comparar los Reels del viernes con los carruseles del miércoles.",
    )
    + week_block(
        3,
        [
            row("Lun", 11, 23, "10:00", "Google: limpieza de oficina antes de las fiestas", "Perfil de Empresa de Google, publicación con botón «Call now»", "ref", "Borrador en Metricool (solo texto)."),
            row("Mar", 11, 24, "11:00", "Checklist de oficina antes del cierre de año", "LinkedIn", "ref", "Checklists y guías. Conjunto «LinkedIn, oficinas»."),
            tt("KN5"),
            li("LI1"),
            row("Mié", 11, 25, "12:00", "Carrusel: después de la cena, la cocina en 30 minutos", "Instagram y Facebook, carrusel", "ref", "Checklists y guías. Conjuntos «Instagram, hogares» y «Facebook»."),
            row("Vie", 11, 27, "12:00", "Reel: la habitación de huéspedes en 3 pasos", "Instagram y Facebook, Reel de unos 12 segundos", "hip", "Checklists y guías. Conjunto «Instagram, Reels»."),
            tt("KN6"),
            row("Sáb", 11, 28, "11:00", "Imagen única: ¿invitados en diciembre?", "Instagram y Facebook, imagen única", "hip", "Servicios explicados. Conjunto «Instagram, sábados»."),
            row("Dom", 11, 29, "18:00", "«Sunday reset» después del fin de semana largo", "Instagram, carrusel", "hip", "Checklists y guías. Conjunto «Instagram, hogares»."),
        ],
        "Semana sin jueves: el 26 es Thanksgiving y no se publica. El viernes 27 vuelve el ritmo con el Reel.",
    )
    + week_block(
        4,
        [
            row("Lun", 11, 30, "10:00", "Google: limpieza recurrente del hogar", "Perfil de Empresa de Google, publicación con botón", "ref", "Borrador en Metricool (solo texto)."),
            row("Mar", 12, 1, "11:00", "Administradores: calendario de limpieza para el cierre de año", "LinkedIn", "ref", "Servicios explicados. Conjunto «LinkedIn, administración de propiedades»."),
            tt("KN7"),
            li("LI2"),
            row("Mié", 12, 2, "12:00", "Antes y después de un trabajo real, con autorización", "Instagram y Facebook, carrusel de 2 a 4 imágenes", "ref", "Antes y después. Conjuntos «Instagram, hogares» y «Facebook»."),
            row("Jue", 12, 3, "11:00", "Qué incluye la limpieza para administración de propiedades", "LinkedIn", "ref", "Servicios explicados. Conjunto «LinkedIn, administración de propiedades»."),
            tt("KN8"),
            row("Vie", 12, 4, "12:00", "Reel: los puntos que todos tocan, antes de las visitas", "Instagram y Facebook, Reel de unos 12 segundos", "hip", "Checklists y guías. Conjunto «Instagram, Reels»."),
            row("Sáb", 12, 5, "11:00", "Imagen única: ¿empezar enero con la casa limpia?", "Instagram y Facebook, imagen única", "hip", "Servicios explicados. Conjunto «Instagram, sábados»."),
            row("Dom", 12, 6, "18:00", "Entrada en invierno: sal, humedad y alfombras", "Instagram, carrusel", "hip", "Checklists y guías. Conjunto «Instagram, hogares»."),
        ],
        "Revisión 2 el viernes 4 de diciembre. Con sus resultados se detallan las semanas 5 a 8.",
    ),
)
kn += section(
    "Semanas 5 a 13: tema de cada semana",
    callout("Desde la semana 5 se mantienen el Reel del viernes y la imagen única del sábado. Sus temas se definen en cada revisión, según lo que haya funcionado. Los dos TikToks semanales siguen con un presentador IA distinto en cada video.") + wlist(
        [
            wrow(5, "Antes y después de las fiestas", "Checklist para recibir invitados y checklist del día siguiente para hogares; en LinkedIn, la oficina en la última semana del año."),
            wrow(6, "Cierre de año para oficinas y edificios", "Limpieza profunda antes del receso e invitación a reservar fechas de enero con una sola acción: pedir presupuesto.", "Revisión 3 el viernes 18 de diciembre."),
            wrow(7, "Semana baja", "Dos piezas: LinkedIn el martes 22 con agradecimiento y horarios de fin de año, e Instagram el domingo 27 con «Sunday reset» posfiestas.", "Sin publicación el jueves 24 ni el viernes 25."),
            wrow(8, "Reset de año nuevo", "LinkedIn el martes 29: la oficina lista antes de que vuelva el equipo. Instagram el miércoles 30 y el domingo 3 de enero: «New year reset» para hogares.", "Jueves 31 y viernes 1 de enero."),
            wrow(9, "Vuelta a la oficina", "Dos publicaciones en LinkedIn (martes 5 y jueves 7), Instagram y Facebook el miércoles 6 y Instagram el domingo 10."),
            wrow(10, "Prueba social", "Reseñas y trabajos reales con autorización, en LinkedIn e Instagram."),
            wrow(11, "Educación para administradores", "Mantenimiento trimestral de unidades y áreas comunes, en tres pasos.", "Lunes 18: feriado federal en EE. UU.; oficinas cerradas. Publicar el martes 19."),
            wrow(12, "Repetir lo que funcionó", "Los formatos y temas con más impresiones de los dos primeros meses, en versión nueva.", "Revisión 4 el viernes 29 de enero."),
            wrow(13, "Puente al siguiente trimestre", "Primeras piezas del plan de febrero a abril, con preparación de la limpieza de primavera."),
        ]
    ),
)
kn += section(
    "Blog en kleannyc.com",
    callout(
        "El blog del sitio ya existe, pero está detenido. Se retoma con un artículo cada dos semanas, cada uno sobre una sola búsqueda concreta y con un botón final para pedir presupuesto. Los posts de LinkedIn enlazan al artículo en lugar de a la página de contacto cuando haya uno relacionado. El efecto en Google tarda meses y no está garantizado.",
        "Propuesta.",
    )
    + '<div class="tablewrap"><table class="rev"><thead><tr><th>Publicar</th><th>Artículo</th><th>Enlaza desde</th></tr></thead><tbody>'
    "<tr><th scope='row'>Vie 20 nov (S2)</th><td>Checklist de oficina antes del cierre de año</td><td>LinkedIn, martes 24 de noviembre</td></tr>"
    "<tr><th scope='row'>Mié 2 dic (S4)</th><td>Qué incluye la limpieza para administración de propiedades</td><td>LinkedIn, jueves 3 de diciembre</td></tr>"
    "<tr><th scope='row'>Semana 6</th><td>Cómo se verifica una unidad antes de entregarla</td><td>LinkedIn y Google</td></tr>"
    "<tr><th scope='row'>Semana 8</th><td>Checklist de turnover para administradores</td><td>LinkedIn</td></tr>"
    "</tbody></table></div>"
    '<p class="note">Los borradores de LinkedIn del 24 de noviembre y el 3 de diciembre apuntan hoy a la página de contacto con parámetros UTM. Si el artículo está publicado a tiempo, se cambia el enlace; si no, se mantienen.</p>'
    '<ul class="rules">'
    "<li><b>Antes de publicar.</b> Corregir el bloqueo inválido de robots.txt y las páginas duplicadas /dtut/ y /new-clients/ señalados en la evaluación SEO.</li>"
    "<li><b>Cada artículo.</b> Una sola pregunta, un título claro, una imagen destacada y el botón final de pedir presupuesto con parámetros UTM.</li></ul>",
)
kn += section(
    "Imágenes destacadas del sitio",
    callout(
        "Una imagen realista por página, en formato horizontal 1.91:1 y sin texto. Sirve de imagen destacada y de tarjeta de vista previa en LinkedIn, Facebook y Google. Los prompts están en el archivo klean-nyc-imagenes-web.html. Son imágenes generadas e ilustrativas: reemplazarlas por fotos reales del equipo o de un trabajo cuando existan.",
        "Qué es.",
    )
    + '<div class="tablewrap"><table class="rev"><thead><tr><th>Antes de</th><th>Imagen</th><th>Archivo sugerido</th></tr></thead><tbody>'
    "<tr><th scope='row'>Lun 9 nov</th><td>Contacto, destino de los botones de Google y de los enlaces de LinkedIn y Facebook</td><td>klean-nyc-contact.jpg</td></tr>"
    "<tr><th scope='row'>Lun 16 nov</th><td>Alquileres vacacionales, destino del botón de Google</td><td>klean-nyc-vacation-rental-cleaning.jpg</td></tr>"
    "<tr><th scope='row'>Semana 1</th><td>Home</td><td>klean-nyc-home.jpg</td></tr>"
    "<tr><th scope='row'>Semana 2</th><td>Limpieza residencial, oficinas, administración de propiedades y post-construcción (las páginas que existan)</td><td>klean-nyc-residential-cleaning.jpg y las demás</td></tr>"
    "<tr><th scope='row'>Antes del primer artículo</th><td>Índice del blog</td><td>klean-nyc-blog.jpg</td></tr>"
    "</tbody></table></div>",
)
kn += section(
    "Conjuntos de hashtags del calendario",
    '<p class="lead-s">Tres en LinkedIn, cinco en Instagram y hasta tres en Facebook.</p>'
    + tagbox("LinkedIn, administración de propiedades", "#NYCCleaning #PropertyManagement #CommercialCleaning")
    + tagbox("LinkedIn, oficinas", "#NYCCleaning #OfficeCleaning #FacilitiesManagement")
    + tagbox("Instagram, hogares", "#NYCCleaning #ResidentialCleaning #CleaningTips #ApartmentCleaning #SundayReset")
    + tagbox("Instagram, Reels", "#NYCCleaning #CleaningTips #ApartmentCleaning #SatisfyingClean #CleaningReel")
    + tagbox("Instagram, sábados", "#NYCCleaning #ResidentialCleaning #CleaningService #ApartmentCleaning #NYCHome")
    + tagbox("Facebook", "#NYCCleaning #ResidentialCleaning #CleaningTips"),
)

# ---------------------------------------------------------------------------
# JDET CAPITAL
# ---------------------------------------------------------------------------
jd = ""
jd += section(
    "Semanas 1 a 4: día por día (hora de Nueva York)",
    callout(
        "Si las cuatro definiciones no están cerradas el viernes 13 de noviembre, todo el calendario se corre una semana. Los temas entre corchetes se completan cuando se confirme la actividad.",
        "Condición.",
    )
    + '<h4 class="wkh">Semana 1<span>' + e(week_range(1)) + "</span></h4>"
    + '<p class="note">Sin publicaciones. Cerrar las cuatro definiciones (qué ofrece y a quién, dónde llega el público, quién habla y qué límites tienen los textos) y completar el perfil el viernes 13.</p>'
    + week_block(
        2,
        [
            row("Mar", 11, 17, "11:00", "Perspectiva del sector n.º 1", "LinkedIn", "ref", "Perspectiva del sector."),
            row("Jue", 11, 19, "11:00", "Cómo trabajamos n.º 1", "LinkedIn", "ref", "Cómo trabajamos."),
        ],
        "Revisión 1 el viernes 20 de noviembre.",
    )
    + week_block(
        3,
        [
            row("Mar", 11, 24, "11:00", "Pregunta frecuente n.º 1", "LinkedIn", "ref", "Preguntas frecuentes."),
            row("Mié", 11, 25, "11:00", "Perspectiva del sector n.º 2", "LinkedIn", "ref", "Se adelanta al miércoles por Thanksgiving. En la referencia de Metricool, el miércoles a las 11:00 supera al martes."),
        ],
    )
    + week_block(
        4,
        [
            row("Mar", 12, 1, "11:00", "Cómo trabajamos n.º 2", "LinkedIn", "ref", "Cómo trabajamos."),
            row("Jue", 12, 3, "11:00", "Equipo: presentación de [persona]", "LinkedIn", "ref", "Equipo."),
        ],
        "Revisión 2 el viernes 4 de diciembre.",
    ),
)
jd += section(
    "Semanas 5 a 13: tema de cada semana",
    wlist(
        [
            wrow(5, "Perspectiva y preguntas frecuentes", "Martes: perspectiva del sector. Jueves: pregunta frecuente."),
            wrow(6, "Cómo trabajamos y equipo", "Martes: proceso. Jueves: equipo.", "Revisión 3 el viernes 18 de diciembre."),
            wrow(7, "Semana baja", "Una publicación el martes 22 con saludo de fin de año.", "Sin publicación el jueves 24 ni el viernes 25."),
            wrow(8, "Mirada al nuevo año", "Una publicación el martes 29 sobre qué mirar en 2027, sin promesas de resultado.", "Jueves 31 y viernes 1 de enero."),
            wrow(9, "Reanudar el ritmo", "Martes 5: perspectiva del sector. Jueves 7: pregunta frecuente."),
            wrow(10, "Cómo trabajamos y equipo", "Martes: proceso. Jueves: equipo."),
            wrow(11, "Perspectiva y preguntas frecuentes", "Martes 19: perspectiva. Jueves 21: pregunta frecuente.", "Lunes 18: feriado federal en EE. UU."),
            wrow(12, "Repetir lo que funcionó", "Los temas con más impresiones, en versión nueva.", "Revisión 4 el viernes 29 de enero."),
            wrow(13, "Puente al siguiente trimestre", "Primeras piezas del plan de febrero a abril."),
        ]
    ),
)

# ---------------------------------------------------------------------------
# KLEAN N GREEN PERU
# ---------------------------------------------------------------------------
pe = ""
pe += section(
    "Semanas 1 a 4: día por día (hora de Lima)",
    callout(
        "Todos los horarios son hipótesis y se reemplazan por el mejor horario de la cuenta cuando haya datos. Si la red no está conectada el 20 de noviembre, la publicación se corre una semana.",
        "Condición.",
    )
    + '<h4 class="wkh">Semana 1<span>' + e(week_range(1)) + "</span></h4>"
    + '<p class="note">Sin publicaciones. Cerrar las cuatro decisiones previas (marca, segmento inicial, red de partida y servicios con zonas) el viernes 13.</p>'
    + '<h4 class="wkh">Semana 2<span>' + e(week_range(2)) + "</span></h4>"
    + '<p class="note">Sin publicaciones. Crear y completar el perfil de Instagram y el Perfil de Empresa de Google, y conectar Instagram a Metricool. Revisión 1 el viernes 20 de noviembre.</p>'
    + week_block(
        3,
        [
            row("Lun", 11, 23, "12:00", "Presentación del servicio: qué incluye y en qué zonas", "Instagram, carrusel", "hip", "Presentación del servicio."),
            row("Mié", 11, 25, "19:00", "Guía de limpieza: [tema]", "Instagram, carrusel", "hip", "Guías de limpieza."),
            row("Vie", 11, 27, "12:00", "Antes y después, o reseña si aún no hay trabajos publicables", "Instagram, carrusel o imagen única", "hip", "Antes y después o reseñas."),
        ],
    )
    + week_block(
        4,
        [
            row("Lun", 11, 30, "12:00", "Servicios por tipo de cliente", "Instagram, carrusel", "hip", "Presentación del servicio."),
            row("Mié", 12, 2, "19:00", "Guía de limpieza: [tema 2]", "Instagram, Reel o carrusel", "hip", "Guías de limpieza."),
            row("Vie", 12, 4, "12:00", "Antes y después, o reseña", "Instagram, carrusel o imagen única", "hip", "Antes y después o reseñas."),
        ],
        "Revisión 2 el viernes 4 de diciembre.",
    ),
)
pe += section(
    "Semanas 5 a 13: tema de cada semana",
    wlist(
        [
            wrow(5, "Casa lista para las fiestas", "Checklist para recibir visitas en Navidad y Año Nuevo.", "Martes 8: feriado en Perú (no cae en lunes, miércoles ni viernes)."),
            wrow(6, "Oficinas: cierre de año", "Limpieza antes del receso e invitación a reservar fechas de enero.", "Revisión 3 el viernes 18 de diciembre."),
            wrow(7, "Navidad", "Dos publicaciones (lunes 21 y miércoles 23) con saludo y horarios.", "Sin publicación el viernes 25."),
            wrow(8, "Año Nuevo", "Lunes 28 y miércoles 30: checklist posfiestas y saludo.", "Sin publicación el viernes 1 de enero."),
            wrow(9, "Verano: al volver de vacaciones", "Limpieza de casas y oficinas después del receso, en tres pasos."),
            wrow(10, "Antes y después", "Trabajos reales con autorización."),
            wrow(11, "Reseñas", "Texto exacto de cada reseña, con permiso."),
            wrow(12, "Repetir lo que funcionó", "Los formatos con más alcance de las primeras semanas de datos.", "Revisión 4 el viernes 29 de enero."),
            wrow(13, "Puente al siguiente trimestre", "Primeras piezas del plan de febrero a abril."),
        ]
    ),
)

# ---------------------------------------------------------------------------
# RESUMEN
# ---------------------------------------------------------------------------
rs = ""
rs += section(
    "Cómo está armado",
    callout(
        "Las cuatro primeras semanas se detallan día por día porque ya hay datos de partida. Las otras nueve se planifican por tema. En cada revisión se consulta Metricool, se compara con la línea base y se detalla el siguiente bloque. Planificar las 13 semanas pieza por pieza sería adelantarse a datos que todavía no existen.",
    )
    + '<div class="cards">'
    '<article class="card"><h4>Base · semanas 1 a 4</h4><p>9 de noviembre al 6 de diciembre. Instalar el ritmo, ordenar la identidad de cada marca y medir. Incluye Thanksgiving.</p></article>'
    '<article class="card"><h4>Temporada · semanas 5 a 8</h4><p>7 de diciembre al 3 de enero. Navidad, fin de año y Año Nuevo, con una semana baja.</p></article>'
    '<article class="card"><h4>Consolidación · semanas 9 a 13</h4><p>4 de enero al 7 de febrero. Repetir lo que funcionó y preparar el siguiente trimestre.</p></article>'
    "</div>",
)
rs += section(
    "Las 13 semanas",
    wlist(
        [
            wrow(1, "Primera semana de publicación", "K&G Market y Klean N Green NYC empiezan. JDET Capital y Klean N Green Perú cierran definiciones."),
            wrow(2, "Primeras señales", "Entran JDET Capital en LinkedIn y el perfil de Klean N Green Perú.", "Revisión 1 el viernes 20 de noviembre."),
            wrow(3, "Thanksgiving", "Semana corta para Klean N Green NYC y JDET Capital. Klean N Green Perú empieza a publicar.", "Jueves 26 Thanksgiving, viernes 27 Black Friday, sábado 28 Small Business Saturday."),
            wrow(4, "Cierre de la base", "Cuatro semanas contra la línea base.", "Revisión 2 el viernes 4 de diciembre."),
            wrow(5, "Mesa de Navidad y fiestas", "Contenido de temporada en las cuatro marcas.", "Martes 8: feriado en Perú."),
            wrow(6, "Pedidos y cierre de año", "Fechas límite de pedidos y reservas de enero.", "Revisión 3 el viernes 18 de diciembre."),
            wrow(7, "Semana baja", "Menos piezas y más historias con saludos y horarios.", "Jueves 24 y viernes 25."),
            wrow(8, "Año Nuevo", "Reset de año nuevo y mirada a 2027.", "Jueves 31 y viernes 1 de enero."),
            wrow(9, "Vuelta al ritmo", "Reanudar el ritmo completo.", "Miércoles 6: Día de Reyes (K&G Market)."),
            wrow(10, "Platos de invierno y prueba social", "Contenido de invierno y reseñas."),
            wrow(11, "Gente, barrio y educación", "Comunidad en K&G Market y educación para administradores en Klean N Green NYC.", "Lunes 18: feriado federal en EE. UU."),
            wrow(12, "Repetir lo que funcionó", "Formatos y temas con más alcance.", "Revisión 4 el viernes 29 de enero."),
            wrow(13, "Puente al siguiente trimestre", "Primeras piezas del plan de febrero a abril."),
        ]
    ),
)
rev = [
    ("Vie 20 nov", "Cumplimiento del ritmo, impresiones por publicación y primeras lecturas de formato y hora.", "Ajustar horarios. Mantener el plan o bajar al mínimo."),
    ("Vie 4 dic", "Cuatro semanas contra la línea base: seguidores, impresiones, Reel, clics en Google y LinkedIn.", "Resultado de la ventana de Instagram, formatos a repetir y detalle de las semanas 5 a 8."),
    ("Vie 18 dic", "Temporada de fiestas: alcance y mensajes.", "Detalle de enero (semanas 9 a 12) y ritmo de la semana baja."),
    ("Vie 29 ene", "Trimestre completo contra las metas propuestas.", "Plan de febrero a abril."),
]
rev_rows = "".join(
    f"<tr><th scope='row'>{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in rev
)
rs += section(
    "Puntos de revisión",
    '<div class="tablewrap"><table class="rev"><thead><tr><th>Fecha</th><th>Qué se revisa</th><th>Qué se decide</th></tr></thead>'
    f"<tbody>{rev_rows}</tbody></table></div>"
    '<p class="note">En cada fecha basta con pedir la revisión: se consultan los datos de Metricool y se actualiza este calendario.</p>',
)
rs += section(
    "Reglas de ajuste",
    '<p class="lead-s">Umbrales propuestos, para confirmar con los primeros datos.</p>'
    '<ul class="rules">'
    "<li><b>Reel de K&amp;G Market.</b> Si supera 150 vistas dos semanas seguidas, pasar de uno a dos Reels por semana.</li>"
    "<li><b>Reels de Klean N Green NYC.</b> En la revisión 1 se comparan con los carruseles del miércoles. Si tienen menos alcance, el viernes pasa a imagen única.</li>"
    "<li><b>Horario de Instagram.</b> Si la ventana de 18:00 a 20:00 supera en impresiones a la de 10:00 a 12:00 durante dos semanas, mover Instagram a la tarde.</li>"
    "<li><b>LinkedIn con buen resultado.</b> Si una publicación supera 50 impresiones, repetir el tema con otro formato en las dos semanas siguientes.</li>"
    "<li><b>LinkedIn con bajo alcance.</b> Si sigue bajo 15 impresiones por publicación tras cuatro semanas, reforzar conexiones y compartidos desde perfiles personales antes de aumentar el ritmo.</li>"
    "<li><b>TikTok.</b> Las cuentas son nuevas y no hay datos propios: los horarios de martes y jueves a las 18:00 vienen de la referencia general de Metricool. En la revisión 1 se comparan vistas y reproducción completa entre martes y jueves y entre temas; se repite el tipo de tema que supere a los demás y se mueve el horario si otra franja rinde más.</li>"
    "<li><b>Capacidad del equipo.</b> Si se cumple menos del 80% de lo programado dos semanas seguidas, volver al plan mínimo.</li></ul>",
)
dates = [
    ("Jue 26 nov", "Thanksgiving", "Todas", "K&G Market con horario especial. Klean N Green NYC y JDET Capital sin publicación ese día."),
    ("Vie 27 y sáb 28 nov", "Black Friday y Small Business Saturday", "K&G Market", "Publicación e historias de comercio local."),
    ("Mar 8 dic", "Inmaculada Concepción (feriado en Perú)", "Klean N Green Perú", "No cae en día de publicación."),
    ("Jue 24 y vie 25 dic", "Nochebuena y Navidad", "Todas", "Saludo en historias. Sin publicación fija el 25."),
    ("Jue 31 dic y vie 1 ene", "Fin de año y Año Nuevo", "Todas", "Saludo y horarios. Sin publicación fija el 1."),
    ("Mié 6 ene", "Día de Reyes", "K&G Market", "Publicación con los productos disponibles, si aplica."),
    ("Lun 18 ene", "Martin Luther King Jr. Day (feriado federal)", "Klean N Green NYC y JDET Capital", "Oficinas cerradas. Publicar el martes 19."),
]
dr = "".join(
    f"<tr><th scope='row'>{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>"
    for a, b, c, d in dates
)
rs += section(
    "Fechas clave",
    '<div class="tablewrap"><table class="rev wide"><thead><tr><th>Fecha</th><th>Qué</th><th>Marcas</th><th>Qué hacer</th></tr></thead>'
    f"<tbody>{dr}</tbody></table></div>",
)

# ---------------------------------------------------------------------------
# ENSAMBLE
# ---------------------------------------------------------------------------
BRANDS = B.BRANDS
tabs = "".join(
    f'<button type="button" role="tab" id="tab-{i}" class="tab {c}" aria-controls="panel-{i}" '
    f'aria-selected="{"true" if k == 0 else "false"}" data-tab="{i}"><i class="dot"></i>{e(n)}</button>'
    for k, (i, c, n) in enumerate(BRANDS)
)

panels = ""
panels += B.panel("resumen", "b-all", "Resumen", "Fases, semanas, revisiones, reglas de ajuste y fechas clave de las cuatro marcas.", rs)
panels += B.panel("kg-market", "b-kg", "K&G Market", "Productos peruanos y caribeños en Brooklyn.", kg, True)
panels += B.panel("klean-nyc", "b-klean", "Klean N Green NYC", "Servicios de limpieza para hogares, oficinas y administración de propiedades en Nueva York.", kn, True)
panels += B.panel("jdet-capital", "b-jdet", "JDET Capital", "Calendario provisional hasta definir la actividad y el público.", jd, True)
panels += B.panel("klean-peru", "b-peru", "Klean N Green Perú", "Calendario provisional hasta conectar la primera red.", pe, True)

EXTRA_CSS = """
.wlist{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.wrow{display:grid;grid-template-columns:78px 1fr;gap:12px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px;align-items:start}
.wn{font:700 22px/1 var(--font-display);color:var(--brand);font-variant-numeric:tabular-nums}
.wd{font-size:12.5px;color:var(--muted);margin-top:4px;line-height:1.3}
.wt{font-weight:600}
.wp{font-size:14.5px;color:var(--muted);margin-top:2px}
.wk{font-size:13px;margin-top:6px;background:var(--soft);display:inline-block;padding:2px 8px;border-radius:6px}
.ph{display:inline-block;margin-left:4px;font:600 11px/1.5 var(--font-body);padding:1px 8px;border-radius:999px;background:var(--soft);color:var(--muted);vertical-align:1px;white-space:nowrap}
.wkh{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;margin-top:22px;font-size:17px;color:var(--brand)}
.wkh span{font:400 14px var(--font-body);color:var(--muted)}
.blk>.wkh:first-of-type{margin-top:16px}
.slot{grid-template-columns:104px 1fr}
.when b{font-size:13px;letter-spacing:.03em}
.callout+.cards{margin-top:12px}
.rev{min-width:560px}
.rev.wide{min-width:680px}
.rev tbody th{white-space:nowrap}
"""

TOP = """<header class="top">
<p class="eyebrow">13 semanas: 9 de noviembre de 2026 al 7 de febrero de 2027</p>
<h1>Calendario de contenidos a 3 meses</h1>
<p class="lead">Cuatro semanas detalladas día por día y nueve semanas por tema para K&amp;G Market, Klean N Green NYC, JDET Capital y Klean N Green Perú. Cuatro revisiones con datos de Metricool ajustan lo que sigue.</p>
</header>"""

FOOT = """<footer>
<div class="fnt">
<p><b>Cómo usarlo.</b> Las horas son de Nueva York, salvo las de Klean N Green Perú, que son de Lima. Las etiquetas Referencia e Hipótesis tienen el mismo significado que en la página de estrategia. Los textos de cada publicación y los conjuntos de hashtags se adaptan de esa página.</p>
<p>Los datos entre corchetes se completan con información real de cada negocio. Salvo el ají amarillo y la chicha morada, que ya aparecen en publicaciones de la cuenta, los productos y platos se confirman con la tienda.</p>
<p>Las semanas 5 a 13 se detallan día por día en cada revisión. JDET Capital y Klean N Green Perú dependen de las definiciones de la semana 1, y sus fechas se corren si no se cierran.</p>
</div>
</footer>"""

DOC = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Calendario de Contenidos</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{B.FONTS}" rel="stylesheet">
<style>{B.CSS}{EXTRA_CSS}</style>
</head>
<body>
{TOP}
<nav class="tabs" id="tabs"><div class="tablist" role="tablist" aria-label="Marcas">{tabs}</div></nav>
<main>
{panels}
</main>
{FOOT}
<script>{B.JS}</script>
</body>
</html>
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(DOC)
print("ok", len(DOC))
