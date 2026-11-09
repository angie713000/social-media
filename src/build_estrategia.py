#!/usr/bin/env python3
# Genera estrategia-contenidos.html (una sola página, sin dependencias en tiempo de ejecución).
import html
import re
import itertools

OUT = "estrategia-contenidos.html"
_ids = itertools.count(1)


def e(s):
    return html.escape(s, quote=False)


def fmt(s):
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", e(s))


def chip(kind):
    label = {"dato": "Dato", "ref": "Referencia", "hip": "Hipótesis"}[kind]
    return f'<span class="chip chip-{kind}">{label}</span>'


def tile(value, label, kind="dato"):
    return (
        f'<div class="tile"><b>{e(value)}</b><span>{fmt(label)}</span>{chip(kind)}</div>'
    )


def tiles(items):
    return '<div class="tiles">' + "".join(tile(*i) for i in items) + "</div>"


def callout(text, title=None):
    t = f"<b>{e(title)}</b> " if title else ""
    return f'<div class="callout"><p>{t}{fmt(text)}</p></div>'


def trait(label, hoy, ajuste):
    return (
        '<div class="trait">'
        f'<h4>{e(label)}</h4>'
        f'<div class="hoy"><small>Hoy</small><p>{fmt(hoy)}</p></div>'
        f'<div class="aj"><small>Ajuste</small><p>{fmt(ajuste)}</p></div>'
        "</div>"
    )


def traits(items):
    return '<div class="traits">' + "".join(trait(*i) for i in items) + "</div>"


def voice(dice, evita, extra=""):
    d = "".join(f"<li>{fmt(x)}</li>" for x in dice)
    v = "".join(f"<li>{fmt(x)}</li>" for x in evita)
    return (
        '<div class="voice">'
        f'<div><h4>La voz dice</h4><ul>{d}</ul></div>'
        f'<div><h4>La voz evita</h4><ul>{v}</ul></div>'
        "</div>" + (f'<p class="note">{fmt(extra)}</p>' if extra else "")
    )


def pillars(items):
    rows = ""
    for name, pct, desc, fmt_ in items:
        rows += (
            '<li class="pillar">'
            f'<div class="pct">{e(pct)}</div>'
            f'<div><p class="pillar-t">{e(name)}</p><p class="pillar-d">{fmt(desc)}</p>'
            f'<p class="pillar-f">{e(fmt_)}</p></div></li>'
        )
    return f'<ol class="pillars">{rows}</ol>'


def slot(day, hour, title, meta, kind, note=""):
    n = f'<p class="what-n">{fmt(note)}</p>' if note else ""
    return (
        '<li class="slot">'
        f'<div class="when"><b>{e(day)}</b><span>{e(hour)}</span></div>'
        f'<div class="what"><p class="what-t">{fmt(title)}</p>'
        f'<p class="what-m">{fmt(meta)} {chip(kind)}</p>{n}</div></li>'
    )


def slots(items):
    return '<ul class="slots">' + "".join(slot(*i) for i in items) + "</ul>"


def copybox(title, text):
    n = next(_ids)
    return (
        '<div class="copybox">'
        f'<div class="copybar"><span>{e(title)}</span>'
        f'<button type="button" class="copybtn" data-copy="cb{n}">Copiar</button></div>'
        f'<pre id="cb{n}">{e(text)}</pre></div>'
    )


def tagbox(title, tags):
    n = next(_ids)
    return (
        '<div class="copybox">'
        f'<div class="copybar"><span>{e(title)}</span>'
        f'<button type="button" class="copybtn" data-copy="cb{n}">Copiar</button></div>'
        f'<p class="tags" id="cb{n}">{e(tags)}</p></div>'
    )


def kpis(rows):
    body = "".join(
        f"<tr><th scope='row'>{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>"
        for a, b, c in rows
    )
    return (
        '<div class="tablewrap"><table class="kpi"><thead><tr><th>Métrica</th>'
        "<th>Hoy</th><th>Meta propuesta</th></tr></thead>"
        f"<tbody>{body}</tbody></table></div>"
    )


def section(title, body, lead=""):
    l = f'<p class="lead-s">{fmt(lead)}</p>' if lead else ""
    return f"<section class='blk'><h3>{e(title)}</h3>{l}{body}</section>"


def panel(pid, cls, name, subtitle, body, hidden=False):
    return (
        f'<section role="tabpanel" id="panel-{pid}" class="panel {cls}" '
        f'aria-labelledby="tab-{pid}"{" hidden" if hidden else ""}>'
        f'<div class="panel-head"><h2>{e(name)}</h2><p>{fmt(subtitle)}</p></div>'
        f"{body}</section>"
    )


# --------------------------------------------------------------------------
# K&G MARKET
# --------------------------------------------------------------------------
kg = ""
kg += section(
    "Punto de partida",
    tiles(
        [
            ("62", "seguidores en Instagram (60 el 26 de octubre)", "dato"),
            ("5 + 5", "publicaciones en Instagram y en Facebook en 30 días", "dato"),
            ("2 a 13", "impresiones por publicación de imagen reciente en Instagram, con 0 interacciones", "dato"),
            ("55", "clics en «cómo llegar» en Google del 8 oct al 3 nov (4 al sitio web, 2 llamadas)", "dato"),
        ]
    )
    + callout(
        "Hoy la búsqueda en Google genera más acción que Instagram. Las publicaciones deben llevar dirección y horario para sostener ese camino, y las redes deben dar razones concretas para visitar la tienda.",
        "Lectura.",
    ),
)
kg += section(
    "Tono y estilo: lo que se ve y qué ajustar",
    traits(
        [
            ("Apertura", "Emoji y una frase de gancho general.", "Mantener el emoji. Nombrar el producto concreto en las primeras seis palabras."),
            ("Cuerpo", "Un párrafo nostálgico y una lista de productos.", "Reducir la nostalgia a una frase. La lista de productos y su uso pasan al centro."),
            ("Idioma", "Mezcla inglés y español sin una regla fija.", "Primera línea en inglés para alcanzar a todo Brooklyn. Segunda línea en español para la comunidad. Los nombres de productos se dejan en su idioma original."),
            ("Cierre", "Dirección y una pregunta abierta.", "Agregar el horario del día y una sola acción: visitar, guardar la publicación o escribir por mensaje. Preguntar solo cuando la respuesta sea fácil."),
            ("Distribución", "El mismo texto y la misma imagen en Instagram y Facebook.", "Instagram con texto corto y visual. Facebook con horario, dirección y ofertas."),
            ("Formato", "Imágenes fijas. El Reel del 9 de agosto alcanzó 136 vistas; las imágenes de octubre y noviembre quedaron entre 2 y 17 impresiones.", "Un Reel de 15 a 30 segundos por semana."),
            ("Hashtags", "Cinco de tema general en las imágenes y quince en el Reel de agosto.", "Entre tres y cinco por publicación, en conjuntos por tema (ver más abajo)."),
        ]
    ),
)
kg += section(
    "Voz propuesta: el vecino que conoce la tienda",
    voice(
        [
            "Habla de producto concreto: «llegó hoy», «para tu mesa», «pregunta por».",
            "Cercana y orgullosa de la cocina peruana y caribeña.",
            "Frases de menos de 15 palabras y un dato útil por publicación.",
        ],
        [
            "Precios o promociones sin fecha de vigencia.",
            "Párrafos largos y varias acciones a la vez.",
            "Lenguaje corporativo o de catálogo.",
        ],
        "Los nombres propios de productos (ají amarillo, chicha morada) no se traducen.",
    ),
)
kg += section(
    "Qué publicar",
    pillars(
        [
            ("Llegó hoy", "35%", "Producto fresco o nuevo, con su uso en una línea y el horario del día.", "Foto o carrusel de 3 imágenes"),
            ("Cómo se usa", "25%", "Receta rápida con ingredientes que se consiguen en la tienda.", "Reel de 15 a 30 segundos"),
            ("Gente y barrio", "15%", "Quién atiende, clientes que lo autoricen, el movimiento de la tienda.", "Foto o historia"),
            ("Ofertas y temporada", "15%", "Thanksgiving (26 de noviembre), Navidad y Año Nuevo, con fechas de vigencia.", "Imagen única"),
            ("Información útil", "10%", "Horarios especiales, cómo llegar, productos agotados o repuestos.", "Historia destacada"),
        ]
    ),
)
kg += section(
    "Cuándo publicar (hora de Nueva York)",
    callout(
        "Una publicación cada 2 o 3 días: lunes, miércoles y viernes, más historias el sábado. Hoy son 5 publicaciones en 30 días. Si el equipo no alcanza, empezar con lunes y viernes y sumar el miércoles desde la tercera semana.",
        "Ritmo.",
    )
    + slots(
        [
            ("Lun", "10:00", "Llegó hoy", "Facebook e Instagram, foto o carrusel", "ref"),
            ("Mié", "12:00", "Cómo se usa", "Facebook e Instagram, Reel", "ref", "El miércoles a las 12:00 marca el índice más alto de la semana en Facebook."),
            ("Vie", "10:00", "Oferta o antojo del fin de semana", "Facebook e Instagram, imagen única", "ref"),
            ("Sáb", "10:00", "Historias de la tienda abierta", "Instagram y Facebook, 3 historias: tienda, producto, horario", "ref", "Es el pico del sábado, con valores menores que los días hábiles."),
        ]
    )
    + '<p class="note">Facebook usa la referencia general de Metricool: picos de lunes a miércoles entre 10:00 y 12:00, y un segundo tramo hacia las 17:00. Instagram no tiene historial en esta cuenta y se publica a la misma hora. Desde la tercera semana, probar durante dos semanas una ventana de 18:00 a 20:00 en Instagram '
    + chip("hip")
    + ". El Perfil de Empresa de Google lleva una publicación semanal los lunes.</p>",
)
kg += section(
    "Hashtags",
    '<p class="lead-s">Entre tres y cinco por publicación en Instagram y hasta tres en Facebook. Rotar los conjuntos y comparar el alcance en Metricool. Antes de adoptar #KGMarket, confirmar en Instagram que no lo use otro negocio, y sustituir un hashtag genérico por el del barrio exacto de la tienda.</p>'
    + tagbox("Producto peruano", "#KGMarket #BrooklynEats #PeruvianFood #AjiAmarillo #ComidaPeruana")
    + tagbox("Producto caribeño", "#KGMarket #BrooklynEats #CaribbeanFood #CaribbeanCuisine #BrooklynFood")
    + tagbox("Bebidas y tradiciones", "#KGMarket #ChichaMorada #PeruvianFood #NYCFood #BrooklynFood")
    + tagbox("Temporada", "#KGMarket #ThanksgivingFood #HolidayTable #BrooklynEats #NYCFood")
    + tagbox("Facebook", "#KGMarket #BrooklynEats #NYCFood"),
)
kg += section(
    "Textos listos para adaptar",
    '<p class="lead-s">Los datos entre corchetes se completan con información real de la tienda.</p>'
    + copybox(
        "Llegó hoy (imagen o carrusel)",
        "Just in: [producto]. 🌶️\nLlegó hoy [producto], listo para tu mesa.\n\nIdeal para [uso 1] y [uso 2].\n\n📍 9420 Church Ave, Brooklyn, NY 11212\n🕘 Hoy abierto de [hora] a [hora]\n\n¿Qué vas a cocinar con esto? Cuéntanos en los comentarios.",
    )
    + copybox(
        "Cómo se usa (Reel)",
        "[Plato] in 3 steps. / [Plato] en 3 pasos.\n\n1. [paso]\n2. [paso]\n3. [paso]\n\nTodo lo que necesitas está en K&G Market: [ingrediente 1], [ingrediente 2].\n📍 9420 Church Ave, Brooklyn, NY 11212\n\nGuarda este video para cocinarlo el fin de semana.",
    )
    + copybox(
        "Temporada (Thanksgiving)",
        "Thanksgiving week at K&G. / Semana de Thanksgiving en K&G.\n\nPara tu mesa: [producto 1], [producto 2] y [producto 3].\nPregunta por [pedido anticipado, si existe].\n\n📍 9420 Church Ave, Brooklyn, NY 11212\n🕘 Horario especial: [horario]",
    ),
)
kg += section(
    "Qué medir en 4 semanas",
    kpis(
        [
            ("Seguidores en Instagram", "62", "80"),
            ("Impresiones por publicación de imagen en Instagram", "2 a 17", "40 o más"),
            ("Vistas del Reel semanal", "136 (Reel de agosto)", "150 o más"),
            ("Clics en «cómo llegar» en Google (27 días)", "55", "70"),
        ]
    )
    + '<p class="note">Metas propuestas para revisar tras dos semanas de datos.</p>',
)

# --------------------------------------------------------------------------
# KLEAN N GREEN NYC
# --------------------------------------------------------------------------
kn = ""
kn += section(
    "Punto de partida",
    tiles(
        [
            ("95", "seguidores en Instagram, sin crecimiento", "dato"),
            ("37 y 18", "impresiones de los dos carruseles de Instagram (26 jul y 9 ago), con 3 y 2 interacciones", "dato"),
            ("1", "seguidor en LinkedIn y 4 publicaciones; la mejor tuvo 14 impresiones y 2 interacciones (14 oct)", "dato"),
            ("1", "publicación en Facebook (28 sep)", "dato"),
        ]
    )
    + callout(
        "Las cuatro publicaciones de LinkedIn terminan con el mismo mensaje y el mismo enlace, y el nombre de la marca cambia según el canal. La prioridad es hablar a dos públicos distintos con un solo nombre: administradores de edificios y oficinas en LinkedIn, hogares en Instagram y Facebook.",
        "Lectura.",
    ),
)
kn += section(
    "Tono y estilo: lo que se ve y qué ajustar",
    traits(
        [
            ("Enfoque", "Centrado en la lista de servicios.", "Abrir con el problema del cliente (una unidad lista para el próximo inquilino, una oficina limpia el lunes) y nombrar el servicio después."),
            ("Cierre", "«Request a free estimate» con el mismo enlace en las 4 publicaciones de LinkedIn.", "Una sola acción por publicación, alternando entre pedir presupuesto, descargar un checklist y escribir por mensaje."),
            ("Formato en Instagram", "Carruseles: lista de servicios y checklist «Weekend reset».", "Mantener los carruseles tipo checklist. La lista de servicios pasa a una historia destacada."),
            ("Nombre", "Cambia según el canal.", "Usar «Klean N Green NYC» en perfil, firma y publicaciones."),
            ("Credibilidad", "Declara «más de 9 años de experiencia». Thumbtack muestra 9 o 10 años según la versión del listado.", "Usar una sola cifra y respaldarla con fotos del equipo, reseñas autorizadas y los productos que se utilizan."),
            ("Audiencia", "Un solo mensaje para empresas y hogares.", "LinkedIn para administradores de propiedades y oficinas. Instagram y Facebook para hogares."),
            ("Hashtags", "De 3 a 4 en LinkedIn; 5 y 10 en los carruseles.", "Tres en LinkedIn y cinco en Instagram."),
        ]
    ),
)
kn += section(
    "Voz propuesta: profesional cercano y verificable",
    voice(
        [
            "Pasos concretos, tiempos reales y resultados visibles.",
            "Un tema por publicación, con lenguaje que entiende un administrador de edificio y un inquilino.",
            "Inglés como idioma principal, por el mercado de Nueva York.",
        ],
        [
            "Superlativos como «the best» sin respaldo.",
            "Afirmaciones ecológicas sin indicar qué productos se usan.",
            "Tecnicismos de limpieza industrial.",
        ],
        "Si la clientela incluye hogares hispanohablantes, agregar una versión en español de las publicaciones de Instagram (por confirmar).",
    ),
)
kn += section(
    "Qué publicar",
    pillars(
        [
            ("Checklists y guías", "30%", "Listas cortas y guardables: «Turnover week», «Sunday reset».", "Carrusel o publicación de texto en LinkedIn"),
            ("Antes y después", "20%", "Trabajos reales con autorización del cliente.", "Carrusel de 2 a 4 imágenes"),
            ("Servicios explicados", "20%", "Qué incluye la limpieza de oficinas, de hogares y para administración de propiedades.", "Texto en LinkedIn o historia destacada"),
            ("Equipo y proceso", "15%", "Quién limpia, con qué productos y cómo se verifica el trabajo.", "Foto o Reel corto"),
            ("Reseñas", "15%", "Texto exacto de la reseña, con permiso de quien la escribió.", "Imagen única o publicación de texto"),
        ]
    ),
)
kn += section(
    "Cuándo publicar (hora de Nueva York)",
    callout(
        "Plan completo: 5 piezas por semana, cada 2 o 3 días. Plan mínimo: 3 piezas (martes en LinkedIn, miércoles en Instagram y Facebook, jueves en LinkedIn). Hoy son 4 publicaciones de LinkedIn en 3 semanas.",
        "Ritmo.",
    )
    + slots(
        [
            ("Mar", "11:00", "Guía o checklist para administradores y oficinas", "LinkedIn", "ref", "En LinkedIn, las 11:00 son el tramo más alto del martes."),
            ("Mié", "12:00", "Carrusel educativo o antes y después", "Instagram y Facebook", "ref", "Miércoles a las 12:00 es el pico de Facebook. En Instagram se usa el mismo horario hasta tener datos."),
            ("Jue", "11:00", "Servicio explicado o reseña", "LinkedIn", "ref", "En LinkedIn, las 11:00 son el tramo más alto del jueves."),
            ("Dom", "18:00", "«Sunday reset»: checklist corto para hogares", "Instagram, Reel o carrusel", "hip", "Probar durante 4 semanas y comparar con el tráfico del miércoles."),
        ]
    )
    + '<p class="note">En LinkedIn, el tramo de las 11:00 es el más alto de martes a viernes, con tramos secundarios a las 10:00 y a las 13:00. El viernes marca el índice más alto de la semana y el martes el más bajo de esos cuatro días: desde la tercera semana, probar el viernes en lugar del martes. Con un solo seguidor, el alcance depende de que el dueño y el equipo compartan cada publicación desde sus perfiles personales y envíen solicitudes de conexión a administradores de propiedades. El Perfil de Empresa de Google lleva una publicación semanal los lunes.</p>',
)
kn += section(
    "Hashtags",
    '<p class="lead-s">Tres en LinkedIn, cinco en Instagram y hasta tres en Facebook. Los de mayor volumen ya se usan en la cuenta; los nuevos requieren revisar su volumen en la búsqueda de cada red antes de adoptarlos.</p>'
    + tagbox("LinkedIn, administración de propiedades", "#NYCCleaning #PropertyManagement #CommercialCleaning")
    + tagbox("LinkedIn, oficinas", "#NYCCleaning #OfficeCleaning #FacilitiesManagement")
    + tagbox("Instagram, hogares", "#NYCCleaning #ResidentialCleaning #CleaningTips #ApartmentCleaning #SundayReset")
    + tagbox("Facebook", "#NYCCleaning #ResidentialCleaning #CleaningTips"),
)
kn += section(
    "Textos listos para adaptar",
    '<p class="lead-s">Los datos entre corchetes se completan con información real del negocio. Crear el archivo descargable antes de publicar el primer texto.</p>'
    + copybox(
        "LinkedIn: checklist para administradores",
        "Turnover week: 5 checks before the next tenant walks in.\n\n1. Kitchen: inside the oven, fridge and cabinets.\n2. Bathrooms: grout, fixtures and exhaust fans.\n3. Windows: glass, tracks and sills.\n4. Floors: edges and corners, not only the center.\n5. Final walkthrough with photos.\n\n[Descripción real del servicio para propiedades en NYC.]\nWant this checklist as a printable PDF? Message us and we will send it.",
    )
    + copybox(
        "Instagram: carrusel «Sunday reset»",
        "Sunday reset: 20 minutes, 6 spots.\n\nSlide 1: Sink and counters\nSlide 2: Bathroom mirror and faucet\nSlide 3: Floors at the entrance\nSlide 4: Trash and recycling\nSlide 5: Bedding\nSlide 6: Fridge shelf cleanup\n\nSave this for next Sunday.",
    )
    + copybox(
        "LinkedIn: reseña de un cliente",
        "\"[Texto exacto de la reseña, con permiso de quien la escribió]\"\n[Nombre o cargo, si lo autoriza]\n\nWhat it took: [qué se hizo, en cuánto tiempo y en qué tipo de espacio].\n\nRequest a free estimate: [enlace con UTM]",
    ),
)
kn += section(
    "Qué medir en 4 semanas",
    kpis(
        [
            ("Seguidores en LinkedIn", "1", "25"),
            ("Impresiones por publicación en LinkedIn", "0 a 14", "50 o más"),
            ("Seguidores en Instagram", "95", "110"),
            ("Solicitudes de presupuesto desde redes", "Sin medir", "Medir con un enlace UTM por red"),
        ]
    )
    + '<p class="note">Metas propuestas para revisar tras dos semanas de datos.</p>',
)

# --------------------------------------------------------------------------
# JDET CAPITAL
# --------------------------------------------------------------------------
jd = ""
jd += section(
    "Punto de partida",
    tiles(
        [
            ("0", "seguidores en Instagram", "dato"),
            ("1", "publicación en Facebook (1 nov), sin texto", "dato"),
            ("0", "sitio web registrado", "dato"),
        ]
    )
    + callout(
        "No hay publicaciones con texto ni información sobre qué ofrece la empresa, por lo que no se puede analizar el tono actual. Este marco queda provisional hasta cerrar las cuatro definiciones de la semana 0.",
        "Estado.",
    ),
)
jd += section(
    "Semana 0: cuatro definiciones (9 al 13 de noviembre)",
    '<ul class="checks"><li><b>Qué ofrece y a quién.</b> Una frase para el perfil y una para el público principal.</li>'
    "<li><b>Dónde llega el público.</b> Sitio web o enlace de destino para cada publicación.</li>"
    "<li><b>Quién habla.</b> La empresa o una persona del equipo con su propio perfil.</li>"
    "<li><b>Límites de lo que se puede decir.</b> Si la actividad es regulada, revisar con un asesor legal los textos antes de publicar cualquier cifra o promesa de resultado.</li></ul>",
)
jd += section(
    "Voz propuesta: sobria, precisa y sin promesas",
    voice(
        [
            "Datos con fuente y fecha, explicados en pocas líneas.",
            "Primera persona del plural: «vemos», «trabajamos».",
            "Una pregunta cerrada al final para invitar a comentar.",
        ],
        [
            "Promesas de resultado o de rendimiento.",
            "Superlativos y urgencia artificial.",
            "Jerga que el público principal no use.",
        ],
        "La voz se confirma con el público y el servicio definidos en la semana 0.",
    ),
)
jd += section(
    "Qué publicar",
    pillars(
        [
            ("Perspectiva del sector", "40%", "Un hecho del sector con fuente, qué significa para el público y cómo lo ve la empresa.", "Texto en LinkedIn"),
            ("Cómo trabajamos", "25%", "Proceso, criterios y tiempos, sin cifras de resultados.", "Carrusel o texto"),
            ("Preguntas frecuentes", "20%", "Una pregunta real de clientes y su respuesta.", "Texto en LinkedIn"),
            ("Equipo", "15%", "Quién es quién y qué hace cada persona.", "Foto con texto"),
        ]
    ),
)
jd += section(
    "Cuándo publicar (hora de Nueva York)",
    callout(
        "Desde el 16 de noviembre, dos publicaciones por semana en LinkedIn, martes y jueves. Facebook e Instagram solo reutilizan lo publicado en LinkedIn una vez cerradas las definiciones.",
        "Ritmo.",
    )
    + slots(
        [
            ("Mar", "11:00", "Perspectiva del sector", "LinkedIn", "ref", "En LinkedIn, las 11:00 son el tramo más alto del martes."),
            ("Jue", "11:00", "Cómo trabajamos o pregunta frecuente", "LinkedIn", "ref", "En LinkedIn, las 11:00 son el tramo más alto del jueves."),
        ]
    )
    + '<p class="note">Desde la tercera semana, probar el viernes a las 11:00 en lugar del martes: es el tramo con el índice más alto de la semana en la referencia de Metricool.</p>',
)
jd += section(
    "Hashtags",
    '<p class="lead-s">Tres por publicación en LinkedIn: uno de marca y dos de tema. Los de tema se definen cuando se confirme la actividad.</p>'
    + tagbox("LinkedIn", "#JDETCapital #[tema 1] #[tema 2]"),
)
jd += section(
    "Estructura de publicación",
    copybox(
        "Perspectiva del sector (LinkedIn)",
        "[Hecho o dato del sector, con fuente y fecha]\n\nQué significa para [público]: [una frase].\n\nCómo lo vemos en JDET Capital: [dos frases, sin promesas de resultado].\n\n[Pregunta cerrada para los comentarios]",
    ),
)
jd += section(
    "Qué medir en 4 semanas",
    kpis(
        [
            ("Definiciones cerradas", "0 de 4", "4 de 4"),
            ("Publicaciones con texto completo", "0 de 1", "8 en 4 semanas"),
        ]
    ),
)

# --------------------------------------------------------------------------
# KLEAN N GREEN PERU
# --------------------------------------------------------------------------
pe = ""
pe += section(
    "Punto de partida",
    tiles(
        [
            ("0", "redes conectadas a Metricool", "dato"),
            ("0", "datos de audiencia o de horarios para Lima", "dato"),
        ]
    )
    + callout(
        "Sin redes conectadas no hay datos ni horarios de referencia para Lima. Este marco queda provisional hasta cerrar cuatro decisiones y conectar la primera red.",
        "Estado.",
    ),
)
pe += section(
    "Cuatro decisiones previas",
    '<ul class="checks"><li><b>Marca.</b> Misma marca que Nueva York o una marca separada para Perú.</li>'
    "<li><b>Segmento inicial.</b> Hogares, oficinas u otro.</li>"
    "<li><b>Red de partida.</b> Instagram, Perfil de Empresa de Google y WhatsApp Business son el punto de partida habitual para un servicio local.</li>"
    "<li><b>Servicios y zonas.</b> Qué se ofrece y en qué distritos de Lima.</li></ul>",
)
pe += section(
    "Voz propuesta: profesional cercano",
    voice(
        [
            "Español claro, con pasos concretos y resultados visibles.",
            "Trato de usted con empresas y de tú con hogares, a confirmar según el segmento.",
            "Un tema y una acción por publicación.",
        ],
        [
            "Afirmaciones ecológicas sin respaldo.",
            "Precios sin vigencia ni alcance del servicio.",
            "Mensajes copiados de la versión de Nueva York sin adaptar al contexto de Lima.",
        ],
    ),
)
pe += section(
    "Qué publicar",
    pillars(
        [
            ("Presentación del servicio", "30%", "Qué incluye, en qué zonas y cómo se solicita.", "Carrusel"),
            ("Guías de limpieza", "30%", "Listas cortas y guardables.", "Carrusel o Reel"),
            ("Antes y después", "25%", "Trabajos reales con autorización del cliente.", "Carrusel de 2 a 4 imágenes"),
            ("Reseñas", "15%", "Texto exacto, con permiso.", "Imagen única"),
        ]
    ),
)
pe += section(
    "Cuándo publicar (hora de Lima)",
    callout(
        "Una vez conectada la primera red: tres publicaciones por semana, lunes, miércoles y viernes. Los horarios son hipótesis para medir durante 4 semanas.",
        "Ritmo.",
    )
    + slots(
        [
            ("Lun", "12:00", "Presentación del servicio", "Instagram", "hip"),
            ("Mié", "19:00", "Guía de limpieza", "Instagram", "hip"),
            ("Vie", "12:00", "Antes y después", "Instagram", "hip"),
        ]
    )
    + '<p class="note">Al conectar la red en Metricool, reemplazar estas ventanas por el mejor horario de la propia cuenta.</p>',
)
pe += section(
    "Hashtags",
    '<p class="lead-s">Tres a cinco por publicación. Revisar el volumen en la búsqueda de Instagram antes de adoptarlos.</p>'
    + tagbox("Instagram, punto de partida", "#LimpiezaLima #LimpiezaProfesional #Lima #[marca]"),
)
pe += section(
    "Qué medir en 4 semanas",
    kpis(
        [
            ("Decisiones cerradas", "0 de 4", "4 de 4"),
            ("Redes conectadas a Metricool", "0", "1 como mínimo"),
        ]
    ),
)

# --------------------------------------------------------------------------
# RESUMEN
# --------------------------------------------------------------------------
matrix_rows = [
    ("Lun", "10:00 Facebook e Instagram", "—", "—", "12:00 Instagram"),
    ("Mar", "—", "11:00 LinkedIn", "11:00 LinkedIn", "—"),
    ("Mié", "12:00 Facebook e Instagram", "12:00 Instagram y Facebook", "—", "19:00 Instagram"),
    ("Jue", "—", "11:00 LinkedIn", "11:00 LinkedIn", "—"),
    ("Vie", "10:00 Facebook e Instagram", "—", "—", "12:00 Instagram"),
    ("Sáb", "10:00 Historias", "—", "—", "—"),
    ("Dom", "—", "18:00 Instagram", "—", "—"),
]
mx = "".join(
    "<tr><th scope='row'>%s</th>%s</tr>"
    % (r[0], "".join("<td class='%s'>%s</td>" % ("empty" if c == "—" else "", e(c)) for c in r[1:]))
    for r in matrix_rows
)
matrix = (
    '<div class="tablewrap"><table class="matrix"><thead><tr><th>Día</th><th>K&amp;G Market</th>'
    "<th>Klean N Green NYC</th><th>JDET Capital (provisional)</th><th>Klean N Green Perú (provisional, hora de Lima)</th></tr></thead>"
    f"<tbody>{mx}</tbody></table></div>"
)

rs = ""
rs += section(
    "Cómo leer las horas",
    '<ul class="legend">'
    f"<li>{chip('dato')}<span>Calculado con la cuenta de la marca en Metricool.</span></li>"
    f"<li>{chip('ref')}<span>Promedio general que entrega Metricool. No mide la cuenta propia.</span></li>"
    f"<li>{chip('hip')}<span>Sin historial. Se prueba 4 semanas y se ajusta.</span></li></ul>"
    '<p class="note">Todas las horas están en hora de Nueva York, salvo las de Perú. Hasta mediados de marzo de 2027 coinciden con la hora de Lima. Instagram devolvió valores en cero para K&amp;G Market y Klean N Green NYC, por lo que sus horarios propios son hipótesis.</p>',
)
rs += section("Semana tipo de las cuatro marcas", matrix)
rs += section(
    "Una frase por marca",
    '<div class="cards">'
    '<article class="card b-kg"><h4>K&amp;G Market</h4><p><b>Tres publicaciones por semana y las historias del sábado.</b> Voz de vecino que conoce la tienda, cálida y bilingüe. Prioridad: convertir búsquedas en Google en visitas.</p></article>'
    '<article class="card b-klean"><h4>Klean N Green NYC</h4><p><b>LinkedIn dos veces y Instagram dos veces por semana.</b> Voz profesional cercana y verificable. Prioridad: un solo nombre y dos públicos separados.</p></article>'
    '<article class="card b-jdet"><h4>JDET Capital</h4><p><b>Dos publicaciones por semana en LinkedIn desde el 16 de noviembre.</b> Voz sobria y sin promesas. Prioridad: definir qué ofrece y a quién.</p></article>'
    '<article class="card b-peru"><h4>Klean N Green Perú</h4><p><b>Tres publicaciones por semana cuando haya una red conectada.</b> Voz profesional cercana. Prioridad: cuatro decisiones previas y conectar Instagram.</p></article>'
    "</div>",
)
rs += section(
    "Reglas comunes",
    '<ul class="rules">'
    "<li><b>Una acción por publicación.</b> Visitar, guardar, escribir o pedir presupuesto, no varias a la vez.</li>"
    "<li><b>Hashtags.</b> De tres a cinco en Instagram, tres en LinkedIn y hasta tres en Facebook.</li>"
    "<li><b>Respuesta en 24 horas</b> a comentarios y mensajes.</li>"
    "<li><b>Programación semanal.</b> Cargar la semana completa en Metricool cada lunes.</li>"
    "<li><b>Revisión de los viernes.</b> Anotar seguidores, impresiones por publicación, interacciones y clics en Google.</li></ul>",
)
rs += section(
    "Pendiente",
    callout(
        "La revisión de SEO de los sitios web sigue abierta: kngmarket.com y kleannyc.com no se pudieron abrir desde aquí. Se retoma con el texto de las páginas, capturas o una sesión con Chrome abierto, y con las direcciones de JDET Capital y Klean N Green Perú.",
    ),
)

# --------------------------------------------------------------------------
# ENSAMBLE
# --------------------------------------------------------------------------
BRANDS = [
    ("resumen", "b-all", "Resumen"),
    ("kg-market", "b-kg", "K&G Market"),
    ("klean-nyc", "b-klean", "Klean NYC"),
    ("jdet-capital", "b-jdet", "JDET Capital"),
    ("klean-peru", "b-peru", "Klean Perú"),
]

tabs = "".join(
    f'<button type="button" role="tab" id="tab-{i}" class="tab {c}" aria-controls="panel-{i}" '
    f'aria-selected="{"true" if k == 0 else "false"}" data-tab="{i}"><i class="dot"></i>{e(n)}</button>'
    for k, (i, c, n) in enumerate(BRANDS)
)

panels = ""
panels += panel("resumen", "b-all", "Resumen", "Las cuatro marcas en una vista. Cada pestaña desarrolla tono, publicaciones, ritmo, horarios y hashtags.", rs)
panels += panel("kg-market", "b-kg", "K&G Market", "Productos peruanos y caribeños en Brooklyn.", kg, True)
panels += panel("klean-nyc", "b-klean", "Klean N Green NYC", "Servicios de limpieza para hogares, oficinas y administración de propiedades en Nueva York.", kn, True)
panels += panel("jdet-capital", "b-jdet", "JDET Capital", "Marco provisional hasta definir la actividad y el público.", jd, True)
panels += panel("klean-peru", "b-peru", "Klean N Green Perú", "Marco provisional hasta conectar la primera red.", pe, True)

LIGHT = """--bg:#F3F5F2;--surface:#FFFFFF;--ink:#17211D;--muted:#55625B;--line:#D9DFD9;--soft:#E9EDE8;
--brand:#2B3A35;--brand-soft:#E4EAE6;--on-brand:#FFFFFF;
--c-dato-bg:#DCEFE3;--c-dato-ink:#17572F;--c-ref-bg:#DDE8F7;--c-ref-ink:#1F4580;--c-hip-bg:#F7E8C8;--c-hip-ink:#734700;"""
DARK = """--bg:#101614;--surface:#19221F;--ink:#E8EEEB;--muted:#A2AFA9;--line:#2B3733;--soft:#212B28;
--brand:#D3DCD7;--brand-soft:#23302C;--on-brand:#101614;
--c-dato-bg:#1B3829;--c-dato-ink:#8ED5A8;--c-ref-bg:#1C2E46;--c-ref-ink:#9AC1EF;--c-hip-bg:#42311A;--c-hip-ink:#EFC675;"""

BR = {
    "b-kg": ("#B5432A", "#F9E8E2", "#F0957F", "#3A2520"),
    "b-klean": ("#1B7A55", "#E1F1E9", "#62C9A0", "#1B3329"),
    "b-jdet": ("#3A4F8C", "#E5EAF7", "#98ADEB", "#212A47"),
    "b-peru": ("#8C5A12", "#F6ECDA", "#E3B567", "#3A2F1B"),
}
brand_light = "".join(f".{k}{{--brand:{v[0]};--brand-soft:{v[1]}}}" for k, v in BR.items())
brand_dark = "".join(f".{k}{{--brand:{v[2]};--brand-soft:{v[3]}}}" for k, v in BR.items())
dark_scoped = ":root:not([data-theme=\"light\"]) "
brand_dark_media = "".join(
    f":root:not([data-theme=\"light\"]) .{k}{{--brand:{v[2]};--brand-soft:{v[3]}}}" for k, v in BR.items()
)
brand_dark_attr = "".join(
    f":root[data-theme=\"dark\"] .{k}{{--brand:{v[2]};--brand-soft:{v[3]}}}" for k, v in BR.items()
)

CSS = """
/* Idea de diseño: ficha de trabajo con una pestaña por marca; cada marca cambia solo el color de acento. */
:root{
%LIGHT%
--font-display:'Bricolage Grotesque','Segoe UI',system-ui,sans-serif;
--font-body:'IBM Plex Sans','Segoe UI',system-ui,sans-serif;
color-scheme:light;
}
%BRAND_LIGHT%
@media (prefers-color-scheme: dark){
:root:not([data-theme="light"]){
%DARK%
color-scheme:dark;
}
%BRAND_DARK_MEDIA%
}
:root[data-theme="dark"]{
%DARK%
color-scheme:dark;
}
%BRAND_DARK_ATTR%
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.55 var(--font-body)}
h1,h2,h3,h4{font-family:var(--font-display);text-wrap:balance;margin:0}
p{margin:0}
b{font-weight:600}
.top{max-width:920px;margin:0 auto;padding:28px 16px 18px}
.eyebrow{font-size:13px;color:var(--muted);letter-spacing:.02em;margin-bottom:8px}
.top h1{font-size:clamp(28px,6.4vw,44px);line-height:1.08;font-weight:700}
.top .lead{margin-top:12px;color:var(--muted);max-width:62ch}
.tabs{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line)}
.tablist{max-width:920px;margin:0 auto;display:flex;gap:2px;overflow-x:auto;padding:0 8px;scrollbar-width:none}
.tablist::-webkit-scrollbar{display:none}
.tab{flex:0 0 auto;display:flex;align-items:center;gap:8px;padding:12px 10px;border:0;border-bottom:3px solid transparent;background:none;color:var(--muted);font:600 14px/1 var(--font-body);cursor:pointer;white-space:nowrap}
.tab .dot{width:8px;height:8px;border-radius:50%;background:var(--brand)}
.tab[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--brand)}
.tab:hover{color:var(--ink)}
:focus-visible{outline:3px solid var(--brand);outline-offset:2px;border-radius:4px}
main{max-width:920px;margin:0 auto;padding:8px 16px 40px}
.panel-head{padding:22px 0 6px}
.panel-head h2{font-size:clamp(24px,5vw,32px);font-weight:700;color:var(--brand)}
.panel-head p{margin-top:6px;color:var(--muted);max-width:62ch}
.blk{margin-top:30px}
.blk>h3{font-size:19px;font-weight:700;padding-bottom:8px;border-bottom:1px solid var(--line);margin-bottom:14px}
.lead-s{color:var(--muted);margin-bottom:12px;max-width:68ch}
.note{margin-top:12px;font-size:14px;color:var(--muted);max-width:68ch}
.note .chip{vertical-align:1px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.tile{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px;display:flex;flex-direction:column;gap:6px;align-items:flex-start}
.tile b{font:700 30px/1 var(--font-display);color:var(--brand);font-variant-numeric:tabular-nums}
.tile span:not(.chip){font-size:14px;color:var(--muted);line-height:1.4}
.chip{display:inline-block;padding:2px 8px;border-radius:999px;font:600 11.5px/1.5 var(--font-body);letter-spacing:.02em;white-space:nowrap}
.chip-dato{background:var(--c-dato-bg);color:var(--c-dato-ink)}
.chip-ref{background:var(--c-ref-bg);color:var(--c-ref-ink)}
.chip-hip{background:var(--c-hip-bg);color:var(--c-hip-ink)}
.callout{margin-top:14px;padding:12px 14px;background:var(--brand-soft);border-left:4px solid var(--brand);border-radius:0 8px 8px 0}
.callout p{max-width:70ch}
.traits{display:flex;flex-direction:column;gap:12px}
.trait{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px;display:grid;gap:10px}
.trait h4{font-size:16px;color:var(--brand)}
.trait small{display:block;font:600 11.5px/1.2 var(--font-body);color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}
.trait .aj{background:var(--brand-soft);border-radius:8px;padding:10px 12px}
.trait .aj small{color:var(--brand)}
.trait p{font-size:15px}
@media (min-width:720px){
.trait{grid-template-columns:150px 1fr 1fr;align-items:start}
}
.voice{display:grid;gap:12px}
@media (min-width:640px){.voice{grid-template-columns:1fr 1fr}}
.voice>div{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px}
.voice h4{font-size:15px;color:var(--brand);margin-bottom:6px}
.voice ul{margin:0;padding-left:18px;display:grid;gap:6px;font-size:15px}
.pillars{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.pillar{display:grid;grid-template-columns:64px 1fr;gap:12px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px;align-items:start}
.pillar .pct{font:700 24px/1.1 var(--font-display);color:var(--brand);font-variant-numeric:tabular-nums}
.pillar-t{font-weight:600}
.pillar-d{font-size:15px;color:var(--muted);margin-top:2px}
.pillar-f{font-size:13px;margin-top:6px;color:var(--ink);background:var(--soft);display:inline-block;padding:2px 8px;border-radius:6px}
.slots{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:10px}
.slot{display:grid;grid-template-columns:84px 1fr;gap:14px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px;align-items:start}
.when{display:flex;flex-direction:column;gap:2px}
.when b{font-size:14px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.06em}
.when span{font:700 26px/1 var(--font-display);color:var(--brand);font-variant-numeric:tabular-nums}
.what-t{font-weight:600}
.what-m{font-size:14px;color:var(--muted);margin-top:2px}
.what-n{font-size:13.5px;color:var(--muted);margin-top:6px}
.copybox{margin-top:10px;background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.copybar{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 8px 8px 14px;background:var(--soft);font-weight:600;font-size:14px}
.copybtn{border:0;border-radius:7px;background:var(--brand);color:var(--on-brand);font:600 13px/1 var(--font-body);padding:9px 14px;cursor:pointer;min-width:84px}
.copybtn:hover{filter:brightness(1.08)}
.copybox pre{margin:0;padding:12px 14px;white-space:pre-wrap;word-break:break-word;font:400 14.5px/1.55 var(--font-body)}
.tags{padding:12px 14px;font-size:15px;word-break:break-word;color:var(--ink)}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--surface)}
table{border-collapse:collapse;width:100%;font-size:14.5px}
th,td{padding:10px 12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
thead th{background:var(--soft);font-weight:600;font-size:13px;white-space:nowrap}
tbody tr:last-child th,tbody tr:last-child td{border-bottom:0}
tbody th{font-weight:600}
.kpi td{font-variant-numeric:tabular-nums}
.matrix{min-width:620px}
.matrix td.empty{color:var(--muted);opacity:.6}
.matrix tbody th{white-space:nowrap}
.legend{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.legend li{display:flex;gap:10px;align-items:baseline}
.cards{display:grid;gap:12px}
@media (min-width:640px){.cards{grid-template-columns:1fr 1fr}}
.card{background:var(--surface);border:1px solid var(--line);border-top:4px solid var(--brand);border-radius:10px;padding:14px}
.card h4{font-size:17px;color:var(--brand);margin-bottom:6px}
.card p{font-size:15px}
.rules,.checks{margin:0;padding-left:20px;display:grid;gap:8px;max-width:70ch}
footer{max-width:920px;margin:0 auto;padding:0 16px 48px}
footer .fnt{border-top:1px solid var(--line);padding-top:18px;font-size:13.5px;color:var(--muted);display:grid;gap:8px;max-width:78ch}
footer a{color:var(--ink)}
@media (prefers-reduced-motion:no-preference){.tab,.copybtn{transition:color .15s,border-color .15s,filter .15s}}
"""

CSS = (
    CSS.replace("%LIGHT%", LIGHT)
    .replace("%DARK%", DARK)
    .replace("%BRAND_LIGHT%", brand_light)
    .replace("%BRAND_DARK_MEDIA%", brand_dark_media)
    .replace("%BRAND_DARK_ATTR%", brand_dark_attr)
)

JS = """
(function(){
  var ids=['resumen','kg-market','klean-nyc','jdet-capital','klean-peru'];
  var nav=document.getElementById('tabs');
  function show(id,scroll){
    if(ids.indexOf(id)<0){id='resumen';}
    ids.forEach(function(k){
      var p=document.getElementById('panel-'+k),t=document.getElementById('tab-'+k),on=(k===id);
      p.hidden=!on;
      t.setAttribute('aria-selected',on?'true':'false');
      t.tabIndex=on?0:-1;
      if(on){try{t.scrollIntoView({inline:'center',block:'nearest'});}catch(e){}}
    });
    if(scroll){try{var top=document.getElementById('panel-'+id).getBoundingClientRect().top+window.pageYOffset-nav.offsetHeight-4;window.scrollTo(0,Math.max(0,top));}catch(e){}}
  }
  var tl=document.querySelectorAll('.tab');
  Array.prototype.forEach.call(tl,function(t,i){
    t.addEventListener('click',function(){
      var id=t.getAttribute('data-tab');
      try{location.hash=id;}catch(e){}
      show(id,true);
    });
    t.addEventListener('keydown',function(ev){
      var j=-1;
      if(ev.key==='ArrowRight'){j=(i+1)%tl.length;}
      if(ev.key==='ArrowLeft'){j=(i-1+tl.length)%tl.length;}
      if(j>=0){ev.preventDefault();tl[j].focus();tl[j].click();}
    });
  });
  window.addEventListener('hashchange',function(){show((location.hash||'').replace('#',''),false);});
  show((location.hash||'').replace('#',''),false);

  document.addEventListener('click',function(ev){
    var btn=ev.target.closest?ev.target.closest('[data-copy]'):null;
    if(!btn){return;}
    var src=document.getElementById(btn.getAttribute('data-copy'));
    if(!src){return;}
    var text=src.textContent;
    var label=btn.getAttribute('data-label')||btn.textContent;
    btn.setAttribute('data-label',label);
    function done(ok){
      btn.textContent=ok?'Copiado':'Seleccione y copie';
      setTimeout(function(){btn.textContent=label;},1800);
    }
    function fallback(){
      try{
        var r=document.createRange();r.selectNodeContents(src);
        var s=window.getSelection();s.removeAllRanges();s.addRange(r);
        done(document.execCommand('copy'));
      }catch(e){done(false);}
    }
    try{
      navigator.clipboard.writeText(text).then(function(){done(true);},fallback);
    }catch(e){fallback();}
  });
})();
"""

FONTS = "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap"

DOC = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Estrategia de Contenidos</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header class="top">
<p class="eyebrow">Plan de arranque: lunes 9 de noviembre de 2026</p>
<h1>Estrategia de contenidos por marca</h1>
<p class="lead">Tono y estilo, qué publicar, cada cuántos días, a qué hora y con qué hashtags para K&amp;G Market, Klean N Green NYC, JDET Capital y Klean N Green Perú. Basado en los datos de Metricool al 7 de noviembre de 2026.</p>
</header>
<nav class="tabs" id="tabs"><div class="tablist" role="tablist" aria-label="Marcas">{tabs}</div></nav>
<main>
{panels}
</main>
<footer>
<div class="fnt">
<p><b>Fuentes y límites.</b> Las cifras vienen de las cuentas conectadas en Metricool (K&amp;G Market, Klean N Green NYC y JDET Capital) al 7 de noviembre de 2026. Klean N Green Perú no tiene redes conectadas.</p>
<p>Los horarios de referencia son promedios generales de Metricool para la semana del 9 al 15 de noviembre. Los de Instagram son hipótesis porque la cuenta no tiene historial. Las metas son propuestas, no proyecciones.</p>
<p>Hashtags: Metricool recomienda de 3 a 5 por publicación en Instagram (<a href="https://metricool.com/blog/how-many-hashtags-to-use/">guía de Metricool</a>). Las fuentes difieren sobre el tope vigente, de 5 a 30, por lo que conviene confirmarlo al programar. No se validó el volumen de cada hashtag.</p>
<p>No se revisaron las páginas web de las marcas, por lo que no hay hallazgos de SEO en este documento.</p>
</div>
</footer>
<script>{JS}</script>
</body>
</html>
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(DOC)
print("ok", len(DOC))
