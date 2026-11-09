#!/usr/bin/env python3
# Un solo HTML con una pestaña por marca: K&G Market (nuevo) y Klean N Green NYC (el paquete actual).
# Reutiliza build_estrategia (helpers y CSS) y build_publicaciones (paquete de Klean). No modifica ninguno de los dos.
import io
import re
import contextlib
import os

os.environ.setdefault("CONTENT_LANG", "en")

with contextlib.redirect_stdout(io.StringIO()):
    import build_estrategia as B
    import build_publicaciones as K

OUT = "publicaciones-marcas-sem1-4.html"
e, fmt = B.e, B.fmt
det, meta_box, chipx = K.det, K.meta_box, K.chipx
import characters as CH

ADDR = "📍 9420 Church Ave, Brooklyn, NY 11212"
SITE = "https://kngmarket.com/?utm_source=google&utm_medium=business-profile&utm_campaign={camp}&utm_content=learn-more"

# ---------------------------------------------------------------------------
# Estados de cada pieza
# ---------------------------------------------------------------------------
S_IMG = "Text ready · add image"
S_VID = "Text ready · add video"
S_PH = "Text ready · add real photo"
S_SHOOT = "Shoot on the day"
S_OPT = "Optional"
KIND = {S_IMG: "hip", S_VID: "hip", S_PH: "hip", S_SHOOT: "ref", S_OPT: "ref"}


def piece(day, hour, title, nets, formato, status, body):
    return (
        '<article class="piece">'
        '<div class="slot"><div class="when">'
        f"<b>{e(day)}</b><span>{e(hour)}</span></div>"
        f'<div class="what"><p class="what-t">{e(title)}</p>'
        f'<p class="what-m">{e(nets)} · {e(formato)} {chipx(status, KIND[status])}</p></div></div>'
        f"{body}</article>"
    )


# ---------------------------------------------------------------------------
# Hashtags (conjuntos de la estrategia y del calendario)
# ---------------------------------------------------------------------------
TG_PERU = "#KGMarket #BrooklynEats #PeruvianFood #AjiAmarillo #ComidaPeruana"
TG_CARIB = "#KGMarket #BrooklynEats #CaribbeanFood #CaribbeanCuisine #BrooklynFood"
TG_DRINK = "#KGMarket #ChichaMorada #PeruvianFood #NYCFood #BrooklynFood"
TG_SEASON = "#KGMarket #ThanksgivingFood #HolidayTable #BrooklynEats #NYCFood"
TG_LOCAL = "#KGMarket #BrooklynEats #BrooklynFood #NYCFood"
TG_SBS = "#KGMarket #SmallBusinessSaturday #BrooklynEats #BrooklynFood #NYCFood"
TG_XMAS = "#KGMarket #HolidayTable #ChristmasFood #BrooklynEats #NYCFood"
TG_FB = "#KGMarket #BrooklynEats #NYCFood"

# ---------------------------------------------------------------------------
# Prompts de imagen (fotografía realista, sin texto, sin personas)
# ---------------------------------------------------------------------------
def people_kg(chars=None):
    """The 'who may appear' sentence of an image prompt."""
    if not chars:
        return "No people. "
    ident = " ".join(f"{CH.identity(k)}." for k in chars)
    return (
        f"The only {'person' if len(chars) == 1 else 'people'} in the image {'is' if len(chars) == 1 else 'are'}: {ident} "
        + (CH.ref_sentence(chars[0]) if len(chars) == 1 else CH.ref_sentence_many(chars))
        + " Candid and relaxed, natural proportions and natural hands with five fingers, no exaggerated smile, not posing for the camera. No other people. "
    )


def style_kg(fmt_txt="Vertical 4:5 format, 1080 x 1350 px", chars=None):
    return (
        "Photorealistic photograph, not an illustration, for a social media post by K&G Market, a Peruvian and Caribbean grocery store in Brooklyn, New York. "
        f"{fmt_txt}. Shot on a full-frame camera with a 35mm lens, soft natural daylight with a warm tone, shallow depth of field, "
        "realistic textures and true-to-life food colors, appetizing and honest, like a food magazine's market feature. "
        "Natural wood, linen and white ceramic surfaces, so the color of the produce stands out. "
        "No cartoon, vector or 3D-render look. "
        "No text of any kind anywhere in the image: no letters, numbers, signs, labels or writing, and no readable brand names or logos on packaging. "
        + people_kg(chars) +
        "Leave a clear, uncluttered square of 160 x 160 px at the bottom left for the logo, which I will add later; do not draw a logo."
    )


def photo_prompt(scene, top_space=False, fmt_txt="Vertical 4:5 format, 1080 x 1350 px", chars=None):
    extra = " Keep the top third of the frame calm and uncluttered, because text will be added there later." if top_space else ""
    return style_kg(fmt_txt, chars) + extra + " Scene: " + scene + "."


GOOGLE_FMT = "Horizontal 4:3 format, 1200 x 900 px"

SC_AJI = (
    "a pile of fresh ají amarillo peppers, long, slightly curved, glossy and bright orange-yellow, on a rustic wooden table; a few are cut open to show the seeds; "
    "a small white ceramic bowl of smooth orange-yellow ají paste sits beside them, with a halved lime and a bunch of cilantro at the edge; "
    "the peppers fill the center of the frame, low camera angle, warm side light"
)
SC_CARIB = (
    "[product] arranged on a rustic wooden table in a natural, abundant way, a small white ceramic bowl and a linen cloth beside it, "
    "one or two ingredients that go with it at the edge of the frame; the product fills the center of the frame, low camera angle, warm side light"
)
SC_THANKS = (
    "a Thanksgiving table still life on a wooden table: a roasted whole squash, ripe plantains, ears of corn in their husks, a bunch of green herbs and small yellow-orange peppers "
    "around a large empty white platter, warm late-afternoon light"
)
SC_BASKET = (
    "a wooden counter in a small neighborhood grocery, a woven basket full of fresh produce in the foreground (plantains, limes, yellow peppers, herbs), "
    "shelves softly out of focus behind it, warm morning light, welcoming and uncluttered"
)
SC_RESTOCK = (
    "a freshly restocked wooden shelf with neat rows of [product], arranged generously and evenly, natural daylight from a window on the left, a few loose items in the foreground"
)
SC_DEC = (
    "a steaming ceramic pitcher and two glasses on a wooden table, surrounded by cinnamon sticks, whole cloves, oranges, half a pineapple and a small pine branch, "
    "warm string lights softly blurred in the background"
)

# Scenes with the recurring characters: the product stays the hero, the character holds or presents it.
SC_AJI_C = (
    "a rustic wooden table with a pile of fresh ají amarillo peppers, long, slightly curved, glossy and bright orange-yellow, a few cut open to show the seeds, "
    "a small white ceramic bowl of smooth orange-yellow ají paste, a halved lime and a bunch of cilantro; "
    "Rosa stands behind the table in the left third of the frame, holding one fresh ají amarillo between two fingers and looking at it with a soft smile; "
    "the peppers fill the foreground and the lower half of the frame, low camera angle, warm side light"
)
SC_CARIB_C = (
    "[product] arranged on a rustic wooden table in a natural, abundant way, a small white ceramic bowl and a linen cloth beside it, "
    "one or two ingredients that go with it at the edge of the frame; "
    "Dre leans on the table in the right third of the frame, holding one [product] up in one hand and looking at it with a relaxed smile; "
    "the product fills the foreground, low camera angle, warm side light"
)
SC_THANKS_C = (
    "a Thanksgiving spread on a wooden table: a roasted whole squash, ripe plantains, ears of corn in their husks, a bunch of green herbs and small yellow-orange peppers "
    "around a large white platter; Rosa and Dre sit at the far side of the table, shown from the chest up in the middle third of the frame, "
    "passing a dish of sweet plantains between them and smiling at each other, not at the camera; the wall above them is plain and calm, warm late-afternoon light"
)
SC_RESTOCK_C = (
    "a freshly restocked wooden shelf with neat rows of [product], arranged generously and evenly, natural daylight from a window on the left; "
    "Rosa stands beside the shelf in the right third of the frame, holding one [product] in her hands as if showing it, looking at it with a soft smile"
)
SC_DEC_C = (
    "a steaming ceramic pitcher and two glasses on a wooden table, surrounded by cinnamon sticks, whole cloves, oranges, half a pineapple and a small pine branch, "
    "warm string lights softly blurred in the background; Rosa and Dre sit at the far side of the table, shown from the chest up in the middle third of the frame, "
    "each holding a glass and smiling at each other, not at the camera; the wall above them is plain and calm"
)

# ---------------------------------------------------------------------------
# Piezas reutilizables
# ---------------------------------------------------------------------------
REAL_PHOTO = [
    "A real photo is the best option for a product post: customers recognize the real shelf. Vertical 4:5, 1080 x 1350 px.",
    "Shoot with the phone held steady at chest height, near a window or the door for daylight. Fill the frame with the product.",
    "Keep price tags out of the frame unless the price has an end date. Leave the bottom-left corner clear for the logo.",
]


_MO = {m: i + 1 for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}


def iso_of(day):
    """'Mon, Nov 9' -> '2026-11-09'"""
    m = re.match(r"\w{3}, (\w{3}) (\d+)", day)
    return f"2026-{_MO[m.group(1)]:02d}-{int(m.group(2)):02d}"


def alt_det(alt):
    return det("Alt text", meta_box(["Paste this in the image's alt text field when you add the image."]) + B.copybox("Alt text", alt), False)


def just_in(day, title, scene, alt, ig, fb, nets="Instagram and Facebook", real=True, top_space=False, chars=None, scene_char=None):
    parts = []
    if chars:
        who = CH.names(chars)
        for k in chars:
            CH.use(k, iso_of(day), "Image", title)
        parts.append(det(f"Image with {who}: prompt", meta_box([
            f"No text in the image: the caption carries the message. {who} {'is' if len(chars) == 1 else 'are'} the only {'person' if len(chars) == 1 else 'people'} allowed.",
            "Attach the reference portrait" + ("" if len(chars) == 1 else "s") + " from the Characters section in the Overview.",
            CH.tag_ai_note(chars),
        ]) + B.copybox("Image prompt (complete, paste into the generator)", photo_prompt(scene_char, top_space, chars=chars)), False))
        if real:
            parts.append(det("Real photo without the character (alternative)", meta_box(REAL_PHOTO), False))
        parts.append(det("Image: prompt without the character (alternative)", meta_box(["Use this if you prefer a product-only image. No text and no people."]) + B.copybox("Image prompt (complete, paste into the generator)", photo_prompt(scene, top_space)), False))
    else:
        if real:
            parts.append(det("Real photo (best option)", meta_box(REAL_PHOTO), False))
        parts.append(det("Image: prompt" + (" (alternative to a real photo)" if real else ""), meta_box(["No text and no people in the image: the caption carries the message."]) + B.copybox("Image prompt (complete, paste into the generator)", photo_prompt(scene, top_space)), False))
    parts.append(alt_det(alt))
    parts.append(det("Instagram text", B.copybox("Instagram text", ig), True))
    parts.append(det("Facebook text", B.copybox("Facebook text", fb), False))
    return "".join(parts)


def google_piece(day, key, title, text, scene, camp, button="Learn more"):
    url = SITE.format(camp=camp)
    inner = B.copybox("Google Business Profile text", text)
    inner += meta_box([
        f"Button: **{button}**, pointing to the website. Google posts do not accept a phone number in the text, so there is none.",
        "If you publish this post directly in Google, choose the button and paste the link below into the button's URL field.",
    ])
    inner += B.tagbox("Link for the button", url)
    img = (
        meta_box(["A real photo of the product is better, horizontal 1200 x 900 px. Google prefers real photos of the business.",
                  "If there is none, this generated image works as an alternative. Never use it to show the team or the store itself."])
        + B.copybox("Image prompt (complete, paste into the generator)", photo_prompt(scene, False, GOOGLE_FMT))
    )
    body = det("Text and button", inner, True) + det("Image: prompt", img, False)
    return piece(day, "11 AM", title, "Google Business Profile", "Post with image and button", S_IMG, body)


# Textos de Google (inglés primero, español después; sin teléfono ni hashtags)
GBP = {
    "11-09": (
        "Just in at K&G Market: ají amarillo. 🌶️\n"
        "The Peruvian pepper behind ají de gallina, huancaína sauce and ceviche is on our shelves today.\n\n"
        "Llegó hoy el ají amarillo, listo para tu mesa.\n\n"
        "Peruvian and Caribbean groceries at 9420 Church Ave, Brooklyn. Open today [opening hours]."
    ),
    "11-16": (
        "Just in at K&G Market: [Caribbean product]. 🌴\n"
        "Ideal for [use 1] and [use 2].\n\n"
        "Llegó hoy [producto caribeño], listo para tu mesa.\n\n"
        "Peruvian and Caribbean groceries at 9420 Church Ave, Brooklyn. Open today [opening hours]."
    ),
    "11-23": (
        "Thanksgiving week at K&G Market. 🦃\n"
        "For your table: [product 1], [product 2] and [product 3]. Ask about [pre-order, if offered].\n\n"
        "Semana de Thanksgiving en K&G: [producto 1], [producto 2] y [producto 3] para tu mesa.\n\n"
        "9420 Church Ave, Brooklyn. Special hours: [hours]."
    ),
    "11-30": (
        "Back in stock at K&G Market: [product]. 🛒\n"
        "The shelves are full again after Thanksgiving.\n\n"
        "De vuelta en K&G: [producto]. Los estantes están llenos otra vez.\n\n"
        "Peruvian and Caribbean groceries at 9420 Church Ave, Brooklyn. Open today [opening hours]."
    ),
}

# ---------------------------------------------------------------------------
# Seedance (solo manos, tres escenas de 4 s)
# ---------------------------------------------------------------------------
SD_SECS = 4
SD_STYLE = "photorealistic live-action food footage, warm natural window light, true-to-life food colors, shallow depth of field, 24 fps, smooth slow satisfying motion"
SD_CONSTRAINTS = (
    "Constraints: only hands appear, no faces; no text, captions, subtitles or watermarks; no logos, no readable brand names or labels on packaging; "
    "no cartoon, illustration or 3D-render look; natural, physically plausible hand, food and liquid movement; no cuts inside the scene."
)
SD_CONSTRAINTS_CHAR = (
    "Constraints: the only person is the cook, a fictional AI character who does not speak and looks at the camera only for a moment; no other people; "
    "no text, captions, subtitles or watermarks; no logos, no readable brand names or labels on packaging; "
    "no cartoon, illustration or 3D-render look; natural, physically plausible hand, face, food and liquid movement; no cuts inside the scene."
)
SD_SETTINGS = [
    "Aspect ratio 9:16 (vertical), the highest resolution the tool offers (1080 x 1920 px or above).",
    f"{SD_SECS} seconds per scene, 3 scenes, about 12 seconds in total. Use 5 seconds per scene if you want more room to trim when editing.",
    "Sound: ambient only (pouring, sizzling, simmering). No music and no voice inside Seedance; add the voiceover (each Reel card has its script) and licensed music in the video editor.",
    "Paste the continuity block at the start of every scene prompt, so the kitchen, the light, the props and the hands stay the same from scene to scene.",
    "Generate and judge one scene at a time. If the tool offers it, use the last frame of the previous scene as the reference for the next one.",
    "Change one line at a time: if the movement is right but the framing is off, edit only the Camera line; if the framing is right but the movement is off, edit only Subject and action.",
    "Every Reel here has a cook, Rosa or Dre. The constraints line allows that one character and nobody else; attach the character's reference portrait to every scene prompt.",
]
ANCHOR = (
    "a bright home kitchen with a light-wood table and a white linen cloth, soft window daylight from the left, white ceramic plates and bowls; "
    "the same adult hands in every scene (medium-brown skin, short natural nails, no jewelry, neutral linen sleeves); {extra}"
)


def anchor_char(k, extra):
    x = CH.c(k)
    return (
        "a bright home kitchen with a light-wood table and a white linen cloth, soft window daylight from the left, white ceramic plates and bowls; "
        f"the cook is {CH.identity(k)}, with the same face, hair and clothes in every scene. {CH.ref_sentence(k)} "
        f"In close-ups only {CH.pron(k, 'pos')} hands show: {x['hands']}. {extra[:1].upper() + extra[1:]}"
    )


def seedance_scene(title, i, n, anchor, action, camera, sound, cons=None):
    return (
        f"Scene {i} of {n} of a vertical Reel titled \"{title}\". 9:16, {SD_SECS} seconds, one continuous shot.\n"
        f"Continuity: {anchor}\n"
        f"Subject and action: {action}\n"
        f"Camera: {camera}\n"
        f"Style: {SD_STYLE}.\n"
        f"Sound: {sound}\n"
        + (cons or SD_CONSTRAINTS)
    )


def seedance_combo(title, anchor, scenes, cons=None, through="the same hands are the through-line"):
    n = len(scenes)
    parts = [
        f"Vertical 9:16 Reel titled \"{title}\", {n * SD_SECS} seconds, a {n}-shot sequence with clean cuts between shots; {through}.",
        f"Continuity: {anchor}",
    ]
    for i, (action, camera, sound) in enumerate(scenes, 1):
        parts.append(f"Shot {i} ({SD_SECS} s): {action} Camera: {camera} Sound: {sound}")
    parts.append(f"Style: {SD_STYLE}.")
    parts.append(cons or SD_CONSTRAINTS)
    return "\n".join(parts)


# key -> título, texto en pantalla por escena, escenas (acción, cámara, sonido), anclaje, Instagram, Facebook
REEL = {
    "11-11": dict(
        title="3 ways to use ají amarillo",
        overlay=["3 ways to use ají amarillo · 1. Huancaína", "2. Ají de gallina", "3. Ceviche"],
        char="rosa",
        anchor=anchor_char("rosa", "a small bunch of ají amarillo peppers rests in the same top corner of every frame."),
        scenes=[
            ("Rosa pours a thick, smooth, bright yellow sauce from a small white jug over halved boiled yellow potatoes on a white plate, watching the pour with a soft smile",
             "medium shot from the front-left at table height, slow push-in toward the plate, her face and shoulders in frame", "soft pouring"),
            ("Rosa's hands lift a wooden spoonful of creamy yellow-orange stew with shredded chicken from a white bowl, steam rising, and rest it beside white rice on a plate; only her hands and the cuffs of her blouse show",
             "slow side tracking close-up, shallow depth of field", "faint bubbling and a spoon touching ceramic"),
            ("Rosa squeezes half a lime over a glass bowl of fresh white fish cubes with red onion slivers and a few thin slices of ají amarillo, juice dripping, then glances up with a small smile",
             "slow push-in from chest height, her face softly in focus behind the bowl", "juice dripping"),
        ],
        vo=["[curious] Ají amarillo, three ways. [warmly] One: huancaína over potatoes.",
            "[warmly] Two: ají de gallina, creamy and warm.",
            "[excited] Three: ceviche! Find the ají at K&G Market."],
        ig=("3 ways to use ají amarillo. / 3 usos del ají amarillo.\n\n"
            "1. Huancaína sauce over potatoes\n2. Ají de gallina\n3. Ceviche\n\n"
            "Get your ají amarillo at K&G Market. / Consigue tu ají amarillo en K&G Market.\n"
            f"{ADDR}\n\nSave this video for the weekend. / Guarda este video para el fin de semana.\n\n" + TG_PERU),
        fb=("3 ways to use ají amarillo. / 3 usos del ají amarillo.\n\n"
            "1. Huancaína sauce over potatoes\n2. Ají de gallina\n3. Ceviche\n\n"
            "Everything you need is at K&G Market. / Todo lo que necesitas está en K&G Market.\n"
            f"{ADDR}\n🕘 Open today [opening hours] / Hoy abierto [horario]\n\n" + TG_FB),
        day="Wed, Nov 11",
    ),
    "11-18": dict(
        title="Rice and peas in 3 steps",
        overlay=["Rice and peas in 3 steps · 1. Simmer the beans", "2. Add the rice and one whole scotch bonnet", "3. Cover, steam, fluff"],
        char="dre",
        anchor=anchor_char("dre", "a wide pot with a glass lid on the stove, a small bowl of fresh thyme and scallions at the edge of the frame in every scene."),
        scenes=[
            ("Dre stirs red kidney beans, chopped scallions and fresh thyme in a pot of simmering coconut milk with a wooden spoon, leaning over the pot",
             "medium shot from the side at stove height, slow push-in, his face in profile", "gentle simmering"),
            ("Dre's hands pour rinsed white rice into the simmering pot, then rest one whole orange scotch bonnet pepper on top; only his hands and forearms show",
             "slow overhead view, locked off", "rice falling into liquid"),
            ("Dre lifts the glass lid from the pot and a cloud of steam rises over the fluffy rice and peas; he looks into the pot, then up with a satisfied smile",
             "slow low-angle push-in toward the pot, his face behind the steam", "soft steam hiss and a lid lifting"),
        ],
        vo=["[curious] Rice and peas in three steps. One: simmer the beans.",
            "[warmly] Two: add the rice and one whole scotch bonnet.",
            "[excited] Three: cover, steam, fluff. It's all at K&G Market!"],
        ig=("Rice and peas in 3 steps. / Arroz con frijoles caribeño en 3 pasos.\n\n"
            "1. Simmer red beans, scallions and thyme in coconut milk\n2. Add rice and one whole scotch bonnet\n3. Cover, steam and fluff\n\n"
            "Everything you need is at K&G Market. / Todo lo que necesitas está en K&G Market.\n"
            f"{ADDR}\n\nSave this video for the weekend. / Guarda este video para el fin de semana.\n\n" + TG_CARIB),
        fb=("Rice and peas in 3 steps. / Arroz con frijoles caribeño en 3 pasos.\n\n"
            "1. Simmer red beans, scallions and thyme in coconut milk\n2. Add rice and one whole scotch bonnet\n3. Cover, steam and fluff\n\n"
            "Find the ingredients at K&G Market. / Encuentra los ingredientes en K&G Market.\n"
            f"{ADDR}\n🕘 Open today [opening hours] / Hoy abierto [horario]\n\n" + TG_FB),
        day="Wed, Nov 18",
    ),
    "11-25": dict(
        title="Sweet plantains for the Thanksgiving table",
        overlay=["Sweet plantains for Thanksgiving · 1. Slice", "2. Fry until golden", "3. Serve warm"],
        char="dre",
        anchor=anchor_char("dre", "a wooden cutting board and a black cast-iron skillet on the stove, a small bowl of coarse salt at the edge of the frame in every scene."),
        scenes=[
            ("Dre slices a very ripe yellow plantain with black spots on a diagonal into thick slices on a wooden board, glancing up and smiling",
             "medium shot from the front, slow push-in, his face and the board in frame", "knife on wood"),
            ("Dre's hands lay thick plantain slices in a hot cast-iron skillet with a little oil, the edges turning deep golden; only his hands show",
             "slow side view at skillet height", "gentle sizzling"),
            ("Dre lifts golden, caramelized plantains with tongs onto a large white platter, steam rising, then holds the platter slightly toward the camera with a small smile",
             "slow pull-back from the platter to a medium shot of Dre", "tongs touching ceramic"),
        ],
        vo=["[curious] Sweet plantains for your Thanksgiving table. One: slice ripe plantains.",
            "[warmly] Two: fry until deep golden.",
            "[excited] Three: serve warm! Get them at K&G Market."],
        ig=("Sweet plantains for the Thanksgiving table. / Plátanos maduros para la mesa de Thanksgiving.\n\n"
            "1. Slice very ripe plantains\n2. Fry until deep golden\n3. Serve warm\n\n"
            "Find the plantains at K&G Market. / Encuentra los plátanos en K&G Market.\n"
            f"{ADDR}\n🕘 Special hours: [hours] / Horario especial: [horario]\n\n" + TG_SEASON),
        fb=("Sweet plantains for the Thanksgiving table. / Plátanos maduros para la mesa de Thanksgiving.\n\n"
            "1. Slice very ripe plantains\n2. Fry until deep golden\n3. Serve warm\n\n"
            "Find the plantains at K&G Market. / Encuentra los plátanos en K&G Market.\n"
            f"{ADDR}\n🕘 Special hours: [hours] / Horario especial: [horario]\n\n" + TG_FB),
        day="Wed, Nov 25",
    ),
    "12-02": dict(
        title="Chicha morada at home, step by step",
        overlay=["Chicha morada at home · 1. Simmer", "2. Strain, add sugar and lime", "3. Chill and pour over ice"],
        char="rosa",
        anchor=anchor_char("rosa", "a tall glass pitcher and a fine metal strainer on the table, a bowl of lime wedges at the edge of the frame in every scene."),
        scenes=[
            ("Rosa's hands drop purple corn, pineapple peel, a cinnamon stick and whole cloves into a large pot of water on the stove; only her hands and the cuffs of her blouse show",
             "slow overhead push-in", "water bubbling softly"),
            ("Rosa pours a deep purple liquid through a fine strainer into a glass pitcher, watching it fill",
             "slow side view at table height, her face softly in frame behind the pitcher", "liquid pouring"),
            ("Rosa squeezes a lime wedge over a tall glass filled with ice and deep purple chicha morada, droplets falling, then lifts the glass slightly toward the camera and smiles",
             "slow push-in to a medium close-up", "ice settling and droplets"),
        ],
        vo=["[curious] Chicha morada, step by step. One: simmer purple corn with spices.",
            "[warmly] Two: strain it, then add sugar and lime.",
            "[excited] Three: serve over ice! Purple corn at K&G Market."],
        ig=("Chicha morada at home, step by step. / Chicha morada en casa, paso a paso.\n\n"
            "1. Simmer purple corn with pineapple peel, cinnamon and cloves\n2. Strain, add sugar and lime\n3. Chill and serve over ice\n\n"
            "Find the ingredients at K&G Market. / Encuentra los ingredientes en K&G Market.\n"
            f"{ADDR}\n\nSave this video for your next family table. / Guarda este video para tu próxima mesa en familia.\n\n" + TG_DRINK),
        fb=("Chicha morada at home, step by step. / Chicha morada en casa, paso a paso.\n\n"
            "1. Simmer purple corn with pineapple peel, cinnamon and cloves\n2. Strain, add sugar and lime\n3. Chill and serve over ice\n\n"
            "Find the ingredients at K&G Market. / Encuentra los ingredientes en K&G Market.\n"
            f"{ADDR}\n🕘 Open today [opening hours] / Hoy abierto [horario]\n\n" + TG_FB),
        day="Wed, Dec 2",
    ),
}
# El guion de voz usa los mismos cuadros de build_publicaciones (tiempos, Eleven v4, guion limpio)
for _k, _v in REEL.items():
    K.VO["kg-" + _k] = _v["vo"]
    if _v.get("char"):
        K.REEL_CHAR["kg-" + _k] = _v["char"]


def reel_piece(key):
    r = REEL[key]
    title, anchor, scenes, ov = r["title"], r["anchor"], r["scenes"], r["overlay"]
    n = len(scenes)
    ch = r.get("char")
    cons = SD_CONSTRAINTS_CHAR if ch else None
    if ch:
        CH.use(ch, iso_of(r["day"]), "Reel", title)
    boxes = "".join(
        B.copybox(f"Scene {i} of {n}: {ov[i-1]}", seedance_scene(title, i, n, anchor, a, c, s, cons))
        for i, (a, c, s) in enumerate(scenes, 1)
    )
    overlay = "\n".join(f"Scene {i}: {t}" for i, t in enumerate(ov, 1))
    draft = meta_box([
        "Drafts created in Metricool for K&G Market (Instagram and Facebook), New York time, with the caption and hashtags. Nothing is published. Instagram holds a placeholder image and Facebook is text only: in the editor, switch each one to Reel and upload the video.",
        "Reels are the format that reached the most people on this account (the August Reel got 136 views), so this is the weekly anchor.",
    ])
    needs = meta_box([
        f"Vertical 9:16, 1080 x 1920 px. {n} scenes of {SD_SECS} seconds each, about {n * SD_SECS} seconds in total.",
        "If the store can film the real dish, a real video beats a generated one. The prompts below are for when it cannot.",
        *([f"**{CH.name(ch)}** is the cook in this Reel (scenes 1 and 3 show the face; scene 2 shows the hands). Attach {CH.name(ch)}'s reference portrait to every scene prompt. The voiceover is {CH.name(ch)}'s voice; the voice description is in the Characters section of the Overview.",
           CH.ai_video_note([ch])] if ch else []),
        "Add the on-screen text, the voiceover (script below) and licensed music in the video editor: generators garble text inside video.",
        "Cover: use a frame from scene 1 and add the title in Canva.",
        "The settings and the way the prompts are built are explained in the Overview, under \"Video prompts for Seedance\".",
    ])
    body = (
        det("Metricool: status", draft, True)
        + det("What the video needs", needs, False)
        + det("Continuity block: paste it at the start of every scene", B.copybox("Continuity block", anchor[0].upper() + anchor[1:]), False)
        + det(f"Seedance prompts: {n} scenes, one prompt per scene", boxes, False)
        + det("All scenes in one prompt (optional)", B.copybox("Single prompt with three labeled shots", seedance_combo(title, anchor, scenes, cons, f"{CH.name(ch)} is the through-line" if ch else "the same hands are the through-line")), False)
        + det("On-screen text by scene", B.copybox("On-screen text (add in the video editor)", overlay), False)
        + det("Voiceover script (audio)", K.vo_boxes("kg-" + key), False)
        + det("Instagram text", B.copybox("Instagram text", r["ig"]), True)
        + det("Facebook text", B.copybox("Facebook text", r["fb"]), False)
        + det("Facebook title (Metricool, Facebook presets)",
              meta_box(["In the Metricool editor, open **Facebook presets** and paste this in **Title**. It is optional and only applies to video posts and Reels."])
              + B.copybox("Facebook title", title), False)
    )
    return piece(r["day"], "12 PM", "Reel: " + title, "Instagram and Facebook", "Reel, about 12 seconds", S_VID, body)


# ---------------------------------------------------------------------------
# Historias del sábado y publicaciones sueltas
# ---------------------------------------------------------------------------
def story_piece(day, title, frames, note, status=S_SHOOT, nets="Instagram and Facebook", hour="10 AM", fmt_txt="3 Stories"):
    frames_html = "<ol class='checks mini'>" + "".join(
        f"<li><b>Frame {i}.</b> Shoot: {e(a)}.<br>Text on screen: {e(t.replace(chr(10), ' · '))}</li>" for i, (a, _b, t) in enumerate(frames, 1)
    ) + "</ol>"
    table = frames_html
    overlay = "\n\n".join(f"Frame {i}\n{t}" for i, (_a, _b, t) in enumerate(frames, 1))
    needs = meta_box([
        "Vertical 9:16, 1080 x 1920 px. Real photos or short clips taken that day with the phone: Stories are about what is happening now, so they are not generated.",
        "Keep the key content away from the top and bottom 250 px, where the app draws its own controls.",
        "Add the text with the app's text tool (short, one line per language), plus a Location sticker for K&G Market on the first frame.",
        note,
    ])
    body = (
        det("What to shoot and what to write", needs + table, True)
        + det("Text on screen: copy", B.copybox("Text for the frames", overlay), False)
    )
    return piece(day, hour, title, nets, fmt_txt, status, body)


def fri_notice(day, title, scene, alt, canva, ig, fb, chars=None, scene_char=None):
    if chars:
        who = CH.names(chars)
        for k in chars:
            CH.use(k, iso_of(day), "Image", title)
        needs = det("What the image needs", meta_box([
            "4:5 format, 1080 x 1350 px, one image with no text on it. The top third stays clear so the key details can be added in Canva, where the type is crisp.",
            f"This image shows {who}, in the middle of the frame. Attach the reference portraits from the Characters section in the Overview.",
            CH.tag_ai_note(chars),
        ]), False)
        img = (
            det(f"Image with {who}: prompt", B.copybox("Image prompt (complete, paste into the generator)", photo_prompt(scene_char, True, chars=chars)), False)
            + det("Image: prompt without the characters (alternative)", meta_box(["Use this if you prefer a product-only image, or a real photo of the table, the counter or the products. No text and no people."])
                  + B.copybox("Image prompt (complete, paste into the generator)", photo_prompt(scene, True)), False)
        )
    else:
        needs = det("What the image needs", meta_box([
            "4:5 format, 1080 x 1350 px, one image with no text on it. The top third stays clear so the key details can be added in Canva, where the type is crisp.",
            "A real photo of the table, the counter or the products works better than a generated one if the store has it.",
        ]), False)
        img = det("Image: prompt", B.copybox("Image prompt (complete, paste into the generator)", photo_prompt(scene, True)), False)
    body = (
        needs
        + img
        + det("Text to add in Canva", B.copybox("Text on the image (Canva)", canva), True)
        + alt_det(alt)
        + det("Instagram text", B.copybox("Instagram text", ig), True)
        + det("Facebook text", B.copybox("Facebook text", fb), False)
    )
    return piece(day, "10 AM", title, "Instagram and Facebook", "Single image", S_IMG, body)


# ---------------------------------------------------------------------------
# SEMANAS 1 A 4
# ---------------------------------------------------------------------------
W = {}

# Semana 1
W[1] = (
    google_piece("Mon, Nov 9", "11-09", "Just in: ají amarillo (Google)", GBP["11-09"], SC_AJI, "kg-nov-wk1")
    + piece("Mon, Nov 9", "10 AM", "Just in: ají amarillo", "Instagram and Facebook", "Image with Rosa", S_IMG,
            just_in("Mon, Nov 9", "Just in: ají amarillo", SC_AJI,
                    "A woman in her 60s with short silver hair holds a fresh ají amarillo pepper behind a wooden table covered with bright orange-yellow peppers, a small bowl of ají paste and a halved lime.",
                    ("Just in: ají amarillo. 🌶️\nLlegó hoy el ají amarillo, listo para tu mesa.\n\n"
                     "Perfect for ají de gallina, huancaína and ceviche.\nIdeal para ají de gallina, huancaína y ceviche.\n\n"
                     f"{ADDR}\n🕘 Open today [opening hours]\n\nWhat will you cook with it? Tell us below. / ¿Qué vas a cocinar con esto? Cuéntanos.\n\n" + TG_PERU),
                    ("Just in: ají amarillo. 🌶️ Llegó hoy.\n\n"
                     "The base of ají de gallina, huancaína sauce and ceviche is now on our shelves. / La base del ají de gallina, la salsa huancaína y el ceviche ya está en nuestros estantes.\n\n"
                     f"{ADDR}\n🕘 Open today [opening hours] / Hoy abierto [horario]\n\nStop by, or send us a message with your questions. / Pasa por la tienda o escríbenos tus preguntas.\n\n" + TG_FB), chars=["rosa"], scene_char=SC_AJI_C))
    + reel_piece("11-11")
    + piece("Fri, Nov 13", "10 AM", "Who runs the store", "Instagram and Facebook", "Photo of the team", S_PH,
            det("Real photo: what it needs", meta_box([
                "A real photo of the people behind the counter, taken with their permission. Vertical 4:5, 1080 x 1350 px.",
                "Never use a generated image for this post: it would show people who do not work there.",
                "Photograph them at work, in daylight, with a shelf or the counter behind them. Candid is better than posed.",
                "Leave the bottom-left corner clear for the logo.",
            ]), True)
            + det("Instagram text", B.copybox("Instagram text",
                  "Meet the people behind the counter. 👋\nConoce a quienes te atienden en K&G Market.\n\n"
                  "[Name] and [name] can help you find [product] and tell you how to cook it.\nTe ayudan a encontrar [producto] y te dicen cómo cocinarlo.\n\n"
                  f"{ADDR}\n🕘 Open today [opening hours]\n\nSay hi next time you stop by. / Salúdalos en tu próxima visita.\n\n" + TG_LOCAL), True)
            + det("Facebook text", B.copybox("Facebook text",
                  "Meet the people behind the counter. 👋 Conoce a quienes te atienden.\n\n"
                  "[Name] and [name] can help you find [product] and tell you how to cook it. / Te ayudan a encontrar [producto] y te dicen cómo cocinarlo.\n\n"
                  f"{ADDR}\n🕘 Open today [opening hours] / Hoy abierto [horario]\n\nSay hi next time you stop by. / Salúdalos en tu próxima visita.\n\n" + TG_FB), False))
    + story_piece("Sat, Nov 14", "Stories: store open, product of the week, hours",
                  [("The store entrance or the counter, open and bright", "Open today · Abierto hoy\n[opening hours]", "Open today · Abierto hoy\n[opening hours / horario]"),
                   ("A close-up of the ají amarillo on the shelf", "Product of the week: ají amarillo", "Product of the week · Producto de la semana\nAjí amarillo"),
                   ("The street or the door from outside, with the street number in sight if possible", "Find us: 9420 Church Ave", "Find us · Encuéntranos\n9420 Church Ave, Brooklyn")],
                  "These stories keep the same structure every Saturday; only the product of the week changes.")
)

# Semana 2
W[2] = (
    google_piece("Mon, Nov 16", "11-16", "Just in: [Caribbean product] (Google)", GBP["11-16"], SC_CARIB, "kg-nov-wk2")
    + piece("Mon, Nov 16", "10 AM", "Just in: [Caribbean product]", "Instagram and Facebook", "Image with Dre", S_IMG,
            meta_box(["Fill in the product before using the prompt: replace **[product]** with the item that arrived (for example plantains, scotch bonnet peppers or sorrel, if the store carries them)."])
            + just_in("Mon, Nov 16", "Just in: [Caribbean product]", SC_CARIB,
                      "A man in his early 30s with a short beard holds up [product] next to a wooden table with a small bowl and a linen cloth.",
                      ("Just in: [Caribbean product]. 🌴\nLlegó hoy [producto caribeño], listo para tu mesa.\n\n"
                       "Ideal for [use 1] and [use 2].\nIdeal para [uso 1] y [uso 2].\n\n"
                       f"{ADDR}\n🕘 Open today [opening hours]\n\nWhat will you cook with it? Tell us below. / ¿Qué vas a cocinar con esto? Cuéntanos.\n\n" + TG_CARIB),
                      ("Just in: [Caribbean product]. 🌴 Llegó hoy.\n\n"
                       "Ideal for [use 1] and [use 2]. / Ideal para [uso 1] y [uso 2].\n\n"
                       f"{ADDR}\n🕘 Open today [opening hours] / Hoy abierto [horario]\n\nStop by, or send us a message with your questions. / Pasa por la tienda o escríbenos tus preguntas.\n\n" + TG_FB), chars=["dre"], scene_char=SC_CARIB_C))
    + reel_piece("11-18")
    + fri_notice("Fri, Nov 20", "Thanksgiving: orders and hours", SC_THANKS,
                 "A woman in her 60s with short silver hair and a man in his early 30s with a short beard sit at a Thanksgiving table with a roasted squash, ripe plantains, corn in husks and herbs, passing a dish between them.",
                 "Thanksgiving at K&G\nOrders until [date, if offered]\nThu, Nov 26: [hours]\nFri, Nov 27: [hours]\n\nThanksgiving en K&G\nPedidos hasta el [fecha]\n9420 Church Ave, Brooklyn",
                 ("Thanksgiving at K&G: orders and hours. 🦃\nThanksgiving en K&G: pedidos y horario.\n\n"
                  "Orders until [date, if offered]. / Pedidos hasta el [fecha].\nThu, Nov 26: [hours]\nFri, Nov 27: [hours]\n\n"
                  f"{ADDR}\n\nMessage us with your questions, or stop by. / Escríbenos tus preguntas o pasa por la tienda.\n\n" + TG_SEASON),
                 ("Thanksgiving at K&G: orders and hours. 🦃\nThanksgiving en K&G: pedidos y horario.\n\n"
                  "Orders until [date, if offered]. / Pedidos hasta el [fecha].\nThu, Nov 26: [hours]\nFri, Nov 27: [hours]\n\n"
                  f"{ADDR}\n\nMessage us with your questions, or stop by. / Escríbenos tus preguntas o pasa por la tienda.\n\n" + TG_FB), chars=["rosa", "dre"], scene_char=SC_THANKS_C)
    + story_piece("Sat, Nov 21", "Stories: what's in today and how to order ahead",
                  [("Fresh products on the shelf or the counter, wide shot", "What's in today", "What's in today · Qué hay hoy\n[product]"),
                   ("A close-up of one product that is good for the holiday table", "Order ahead", "Order ahead for Thanksgiving · Pedidos para Thanksgiving\n[date, if offered]"),
                   ("The entrance or the counter", "Hours", "Hours this week · Horario de la semana\n[hours]")],
                  "If the store does not take pre-orders, replace frame 2 with a second product and delete the order line from the Friday post.")
)

# Semana 3
W[3] = (
    google_piece("Mon, Nov 23", "11-23", "Thanksgiving: products for your table (Google)", GBP["11-23"], SC_THANKS, "kg-nov-wk3")
    + piece("Mon, Nov 23", "10 AM", "Thanksgiving: products for your table", "Instagram and Facebook", "Carousel, 3 images", S_IMG,
            det("What the images need", meta_box([
                "4:5 format, 1080 x 1350 px, 3 images, one product per image, with no text on them. Product names and the closing details are added in Canva.",
                "Fill in the three products before using the prompts: replace **[product 1]**, **[product 2]** and **[product 3]** with the real items.",
                "Real photos of the same products are better than generated ones.",
            ]), False)
            + det("Image 1 of 3: cover", B.copybox("Image prompt (complete, paste into the generator)",
                  photo_prompt("[product 1] on a wooden table set for Thanksgiving, with a few autumn leaves, a white ceramic dish and a linen cloth; the product is the hero, in the center of the frame, warm late-afternoon light", True)), False)
            + det("Image 2 of 3", B.copybox("Image prompt (complete, paste into the generator)",
                  photo_prompt("[product 2] on a wooden table next to a white ceramic dish and a linen cloth, with one or two ingredients that go with it at the edge of the frame; the product is the hero, in the center of the frame, warm side light", True)), False)
            + det("Image 3 of 3: closing", B.copybox("Image prompt (complete, paste into the generator)",
                  photo_prompt("[product 3] on a wooden table next to a white ceramic dish and a linen cloth, with a small pine branch and a few cinnamon sticks at the edge of the frame; the product is the hero, in the center of the frame, warm side light", True)), False)
            + det("Text to add in Canva", B.copybox("Text on the images (Canva)",
                  "Image 1\nThanksgiving week at K&G\nSemana de Thanksgiving\n\nImage 2\n[Product 2]\n\nImage 3\n[Product 3]\n9420 Church Ave, Brooklyn · Special hours [hours]\n\n(Name [product 1] on image 1 under the title.)"), False)
            + alt_det("Three photos of products for a Thanksgiving table, one per image, on a wooden table with a white ceramic dish.")
            + det("Instagram text", B.copybox("Instagram text",
                  "Thanksgiving week at K&G. 🦃 / Semana de Thanksgiving en K&G.\n\n"
                  "For your table: [product 1], [product 2] and [product 3].\nPara tu mesa: [producto 1], [producto 2] y [producto 3].\n\n"
                  f"Ask about [pre-order, if offered]. / Pregunta por [pedido anticipado, si existe].\n\n{ADDR}\n🕘 Special hours: [hours] / Horario especial: [horario]\n\n"
                  "Swipe to see them. / Desliza para verlos.\n\n" + TG_SEASON), True)
            + det("Facebook text", B.copybox("Facebook text",
                  "Thanksgiving week at K&G. 🦃 / Semana de Thanksgiving en K&G.\n\n"
                  "For your table: [product 1], [product 2] and [product 3]. / Para tu mesa: [producto 1], [producto 2] y [producto 3].\n\n"
                  f"Ask about [pre-order, if offered]. / Pregunta por [pedido anticipado, si existe].\n\n{ADDR}\n🕘 Special hours: [hours] / Horario especial: [horario]\n\n" + TG_FB), False))
    + reel_piece("11-25")
    + piece("Thu, Nov 26", "9 AM", "Thanksgiving greeting (Story)", "Instagram and Facebook", "1 Story", S_OPT,
            det("Story", meta_box([
                "No fixed post on Thanksgiving. If you want to greet, one Story is enough: a real photo of the store or a product, vertical 1080 x 1920 px.",
                "Confirm the store's hours for Thursday, Nov 26 before writing them.",
            ]) + B.copybox("Text for the Story",
                           "Happy Thanksgiving from K&G Market. / Feliz Thanksgiving de K&G Market.\nOpen [hours] · Abierto [horario]"), True))
    + piece("Fri, Nov 27", "10 AM", "Small Business Saturday: come meet us", "Instagram and Facebook", "Single image", S_PH,
            det("Real photo (best option)", meta_box([
                "A real photo of the store from the street, or of the owners at the counter with their permission. Vertical 4:5, 1080 x 1350 px.",
                "The generated image below is a neutral alternative: it shows a generic neighborhood grocery counter, not the store itself.",
                "Leave the bottom-left corner clear for the logo.",
            ]), False)
            + det("Image: prompt (alternative to a real photo)", B.copybox("Image prompt (complete, paste into the generator)", photo_prompt(SC_BASKET, True)), False)
            + alt_det("A basket of fresh produce on a wooden counter in a small neighborhood grocery.")
            + det("Instagram text", B.copybox("Instagram text",
                  "Small Business Saturday is tomorrow. 💛\nEl Small Business Saturday es mañana.\n\n"
                  "Shop small: Peruvian and Caribbean groceries for your table.\nCompra local: productos peruanos y caribeños para tu mesa.\n\n"
                  f"{ADDR}\n🕘 Open Saturday [hours]\n\nTag a neighbor who loves to cook. / Etiqueta a un vecino que ama cocinar.\n\n" + TG_SBS), True)
            + det("Facebook text", B.copybox("Facebook text",
                  "Small Business Saturday is tomorrow. 💛 El Small Business Saturday es mañana.\n\n"
                  "Come meet us: Peruvian and Caribbean groceries for your table. / Ven a conocernos: productos peruanos y caribeños para tu mesa.\n\n"
                  f"{ADDR}\n🕘 Open Saturday [hours] / Abierto el sábado [horario]\n\n" + TG_FB), False))
    + story_piece("Sat, Nov 28", "Stories: Small Business Saturday in the store",
                  [("The entrance or the counter, with customers only if they agree to be filmed", "Welcome", "Small Business Saturday · Compra local\nOpen [hours]"),
                   ("A product the team recommends, held or on the shelf", "Team pick", "Our pick today · Nuestra recomendación\n[product]"),
                   ("The bags or the counter at the end of the day", "Thank you", "Thank you for shopping small · Gracias por comprar local")],
                  "Frame 2: ask the team for their pick; a recommendation by name works better than a general promo.")
)

# Semana 4
W[4] = (
    google_piece("Mon, Nov 30", "11-30", "Back in stock: [product] (Google)", GBP["11-30"], SC_RESTOCK, "kg-nov-wk4")
    + piece("Mon, Nov 30", "10 AM", "Just in: [product], back in stock after Thanksgiving", "Instagram and Facebook", "Image with Rosa", S_IMG,
            meta_box(["Fill in the product before using the prompt: replace **[product]** with the item that was restocked."])
            + just_in("Mon, Nov 30", "Back in stock", SC_RESTOCK,
                      "A woman in her 60s with short silver hair holds [product] next to a wooden shelf with neat rows of the same product.",
                      ("Back in stock: [product]. 🛒\nDe vuelta: [producto].\n\n"
                       "The shelves are full again after Thanksgiving.\nLos estantes están llenos otra vez después de Thanksgiving.\n\n"
                       f"{ADDR}\n🕘 Open today [opening hours]\n\nWhat's on your list? Tell us below. / ¿Qué hay en tu lista? Cuéntanos.\n\n" + TG_PERU),
                      ("Back in stock: [product]. 🛒 De vuelta: [producto].\n\n"
                       "The shelves are full again after Thanksgiving. / Los estantes están llenos otra vez después de Thanksgiving.\n\n"
                       f"{ADDR}\n🕘 Open today [opening hours] / Hoy abierto [horario]\n\nStop by, or send us a message with your questions. / Pasa por la tienda o escríbenos tus preguntas.\n\n" + TG_FB), chars=["rosa"], scene_char=SC_RESTOCK_C))
    + reel_piece("12-02")
    + fri_notice("Fri, Dec 4", "December at K&G: hours and Christmas orders", SC_DEC,
                 "A woman in her 60s and a man in his early 30s sit at a wooden table with glasses, a steaming pitcher, cinnamon, cloves, oranges, pineapple and a pine branch.",
                 "December at K&G\nChristmas orders until [date, if offered]\nHours: [hours]\nDec 24: [hours] · Dec 25: [hours]\n\nDiciembre en K&G\nPedidos de Navidad hasta el [fecha]\n9420 Church Ave, Brooklyn",
                 ("December at K&G: hours and Christmas orders. 🎄\nDiciembre en K&G: horarios y pedidos de Navidad.\n\n"
                  "Orders until [date, if offered]. / Pedidos hasta el [fecha].\nHours: [hours]\nDec 24: [hours] · Dec 25: [hours]\n\n"
                  f"{ADDR}\n\nSave this post so you have the hours. / Guarda esta publicación para tener los horarios.\n\n" + TG_XMAS),
                 ("December at K&G: hours and Christmas orders. 🎄\nDiciembre en K&G: horarios y pedidos de Navidad.\n\n"
                  "Orders until [date, if offered]. / Pedidos hasta el [fecha].\nHours: [hours]\nDec 24: [hours] · Dec 25: [hours]\n\n"
                  f"{ADDR}\n\nMessage us with your questions, or stop by. / Escríbenos tus preguntas o pasa por la tienda.\n\n" + TG_FB), chars=["rosa", "dre"], scene_char=SC_DEC_C)
    + story_piece("Sat, Dec 5", "Stories: store open and product of the week",
                  [("The store entrance or the counter, open and bright", "Open today", "Open today · Abierto hoy\n[opening hours / horario]"),
                   ("A close-up of the product of the week", "Product of the week", "Product of the week · Producto de la semana\n[product]"),
                   ("The counter or a shelf with a seasonal product", "December hours", "December hours · Horario de diciembre\n[hours]")],
                  "Same structure as every Saturday; the product of the week changes.")
)

# ---------------------------------------------------------------------------
# VISIÓN GENERAL DE K&G MARKET
# ---------------------------------------------------------------------------
board_rows = [
    ("Mon, Nov 9 · 10 AM", "Instagram and Facebook", "Just in: ají amarillo · Rosa", S_IMG),
    ("Mon, Nov 9 · 11 AM", "Google", "Just in: ají amarillo", S_IMG),
    ("Wed, Nov 11 · 12 PM", "Instagram and Facebook", "Reel: 3 ways to use ají amarillo", S_VID),
    ("Fri, Nov 13 · 10 AM", "Instagram and Facebook", "Who runs the store", S_PH),
    ("Sat, Nov 14 · 10 AM", "Instagram and Facebook", "Stories: open, product of the week, hours", S_SHOOT),
    ("Mon, Nov 16 · 10 AM", "Instagram and Facebook", "Just in: [Caribbean product] · Dre", S_IMG),
    ("Mon, Nov 16 · 11 AM", "Google", "Just in: [Caribbean product]", S_IMG),
    ("Wed, Nov 18 · 12 PM", "Instagram and Facebook", "Reel: Rice and peas in 3 steps", S_VID),
    ("Fri, Nov 20 · 10 AM", "Instagram and Facebook", "Single image: Thanksgiving orders and hours · Rosa and Dre", S_IMG),
    ("Sat, Nov 21 · 10 AM", "Instagram and Facebook", "Stories: what's in today, how to order ahead", S_SHOOT),
    ("Mon, Nov 23 · 10 AM", "Instagram and Facebook", "Carousel: Thanksgiving, products for your table", S_IMG),
    ("Mon, Nov 23 · 11 AM", "Google", "Thanksgiving week", S_IMG),
    ("Wed, Nov 25 · 12 PM", "Instagram and Facebook", "Reel: Sweet plantains for Thanksgiving", S_VID),
    ("Thu, Nov 26 · 9 AM", "Instagram and Facebook", "Thanksgiving greeting (one Story)", S_OPT),
    ("Fri, Nov 27 · 10 AM", "Instagram and Facebook", "Single image: Small Business Saturday", S_PH),
    ("Sat, Nov 28 · 10 AM", "Instagram and Facebook", "Stories: Small Business Saturday", S_SHOOT),
    ("Mon, Nov 30 · 10 AM", "Instagram and Facebook", "Just in: [product], back in stock · Rosa", S_IMG),
    ("Mon, Nov 30 · 11 AM", "Google", "Back in stock: [product]", S_IMG),
    ("Wed, Dec 2 · 12 PM", "Instagram and Facebook", "Reel: Chicha morada at home", S_VID),
    ("Fri, Dec 4 · 10 AM", "Instagram and Facebook", "Single image: December hours and Christmas orders · Rosa and Dre", S_IMG),
    ("Sat, Dec 5 · 10 AM", "Instagram and Facebook", "Stories: open, product of the week", S_SHOOT),
]
board = (
    '<div class="tablewrap"><table class="rev"><thead><tr><th>Date</th><th>Network</th><th>Piece</th><th>Status</th></tr></thead><tbody>'
    + "".join(f"<tr><th scope='row'>{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td><td>{chipx(d, KIND[d])}</td></tr>" for a, b, c, d in board_rows)
    + "</tbody></table></div>"
    + "<p class='note'>Tuesdays, Thursdays and Sundays have no fixed post. The rhythm comes from the strategy: Monday, Wednesday and Friday plus Saturday Stories, and a weekly Google post on Mondays.</p>"
)

formats = (
    '<div class="tablewrap"><table class="rev"><thead><tr><th>Piece</th><th>Size</th><th>Notes</th></tr></thead><tbody>'
    "<tr><th scope='row'>Photo and single image</th><td>1080 x 1350 px (4:5)</td><td>Instagram and Facebook. Five of them (Nov 9, 16, 20, 30 and Dec 4) show Rosa or Dre as the main image; a real photo or a product-only image is the alternative. No text on the generated image: the key details are added in Canva.</td></tr>"
    "<tr><th scope='row'>Carousel (Nov 23)</th><td>1080 x 1350 px (4:5)</td><td>3 images, one product per image.</td></tr>"
    "<tr><th scope='row'>Reel</th><td>1080 x 1920 px (9:16)</td><td>About 12 seconds, 3 Seedance scenes of about 4 seconds, with Rosa or Dre cooking: the face shows in two scenes and only the hands in the third. Wednesdays, Instagram and Facebook.</td></tr>"
    "<tr><th scope='row'>Stories</th><td>1080 x 1920 px (9:16)</td><td>Saturdays, 3 frames shot that day with the phone. Keep key content out of the top and bottom 250 px.</td></tr>"
    "<tr><th scope='row'>Google Business Profile</th><td>1200 x 900 px (4:3)</td><td>Mondays. A real photo is better; the generated image is the alternative. No phone number in the text.</td></tr>"
    "</tbody></table></div>"
)

confirm = [
    "**Opening hours.** Every text has **[opening hours]**. Send the regular hours and the special ones for Nov 26, Nov 27, Dec 24, Dec 25, Dec 31 and Jan 1.",
    "**Products.** The brackets for the Caribbean product (Nov 16), the three Thanksgiving products (Nov 23) and the restocked product (Nov 30) need real items. Ají amarillo and chicha morada already appear in the account's own posts.",
    "**Dishes in the Reels.** Rice and peas (Nov 18) and sweet plantains (Nov 25) are proposals for the [Caribbean dish] and [dish] in the calendar. Confirm that the store sells the ingredients, or give another dish and the prompts are rewritten.",
    "**Purple corn (Dec 2).** The Reel assumes the store sells purple corn. If it sells ready-made chicha morada, the steps change to \"shake, chill and pour\".",
    "**Pre-orders.** Thanksgiving and Christmas posts mention **[date, if offered]**. If the store does not take orders ahead, delete those lines.",
    "**Store hours.** The website header lists Mon to Sat 7:30am to 8pm and Sun 7:30am to 6:30pm. The [hours] in the holiday posts (Thanksgiving, Small Business Saturday, December) stay open because holiday hours may differ: send the real ones and they are filled in.",
    "**Phone number.** No text includes it. The website and the Google profile show +1 347-365-9656 and a Facebook extract shows 347-739-5457: confirm which one is correct before adding it anywhere.",
    "**Website.** The Google button points to kngmarket.com. The site was hidden from Google by a WordPress setting; on Nov 9 that was turned off, the sitemap was sent to Search Console and indexing of the home page was requested. It can take from a few days to a couple of weeks to show up. The site now has Yoast SEO with titles and descriptions on the main pages and every product category, one H1 per page and alt text on the product images. If you prefer, use the Call now button once the phone is confirmed.",
    "**Hashtag #KGMarket.** Check on Instagram that no other business uses it. The Small Business Saturday and Christmas posts add #SmallBusinessSaturday and #ChristmasFood to the calendar's sets.",
    "**Team photo (Nov 13).** Needs the team's permission and their names. Never use a generated image for that post.",
    "**Rosa and Dre.** They are AI characters, not staff, and they appear only in the TikToks, the four Reels and five single images. Generate each portrait once (see Characters) and attach it every time. The AI label is needed on every video and image that shows them. The Google posts, the Stories and the team post stay free of generated people.",
    "**Spanish lines.** They are written in neutral Spanish. Tell me if the store prefers Peruvian or Caribbean terms for any product.",
    "**Colors and logo.** No palette or fonts were provided for K&G Market, so the prompts use natural food colors and leave the bottom-left corner empty for your logo. If you share the logo and colors, the Canva overlays can match.",
    "**Metricool.** The 36 drafts (28 for Instagram, Facebook and Google, plus 8 for TikTok) are created for K&G Market and none is published. Before scheduling each one, in the editor: replace the Instagram placeholder image with the real one, fill in every bracket, switch the four Instagram and Facebook Reels to Reel and upload the video, add the Brooklyn location on Instagram and Facebook, add the image and button on the Google posts, and on TikTok replace the placeholder photo with the video and switch on the AI-generated content label.",
]
confirm_html = "<ul class='checks'>" + "".join(f"<li>{fmt(x)}</li>" for x in confirm) + "</ul>"

look = (
    meta_box([
        "Photorealistic, soft daylight with a warm tone, wood, linen and white ceramic, so the produce color carries the image.",
        "No text in generated images; text goes on in Canva. Rosa and Dre, the two AI characters, are the only people allowed in generated images and videos. Real people appear only in real photos, with their permission.",
        "Bottom-left corner empty for the logo, as in the Klean N Green NYC pack.",
        "Stories are not generated: they are shot that day with the phone.",
    ])
)
sd = meta_box(SD_SETTINGS)

rs = B.section(
    "What is ready and what is missing",
    B.tiles([
        ("21", "pieces over four weeks: 8 for Instagram and Facebook (photos, a carousel, single images), 4 Reels, 4 Google posts, 4 Saturday Story sets and one optional Thanksgiving Story", "dato"),
        ("4", "Reels, two with Rosa and two with Dre, each with a continuity block, 3 Seedance scene prompts, a voiceover with Eleven v4 tags, on-screen text and captions", "dato"),
        ("4", "Google Business Profile posts, one every Monday, with text, button and link", "dato"),
        ("13", "image prompts for product photos, notices, the carousel and the four Google posts, all without text. Five of the posts also have a version with Rosa or Dre; the Google posts and the carousel have no people", "dato"),
        ("36", "drafts in Metricool for K&G Market (Instagram, Facebook, Google and TikTok), none published; they still need the real images, the bracket details and the videos for the Reels and TikToks", "dato"),
        ("8", "TikToks of about 18 seconds, four with Rosa and four with Dre, each with a script, a video prompt and a caption", "dato"),
    ])
    + B.callout(
        "All texts are written in English with a Spanish line, as the brand voice defines. What is left is the real material: opening hours, the products behind each bracket, the team photo, and the Saturday Stories on the day. Nothing is published without approval.",
        "Next step.",
    ),
    "K&G Market, Monday, November 9 to Sunday, December 6, 2026. All times are New York time.",
)
rs += B.section("Four-week calendar", board)
rs += B.section("Pieces and sizes", formats)
rs += B.section("Look of the images", look)
rs += B.section("Video prompts for Seedance", sd, "Every Reel in this pack follows the same settings.")
rs += B.section("Before approving", confirm_html)

WEEK_TXT = {
    1: ("Week 1", "November 9 to 15. A first Peruvian product, the team and the store's Saturday routine."),
    2: ("Week 2", "November 16 to 22. A Caribbean product and the first Thanksgiving notice."),
    3: ("Week 3", "November 23 to 29. Thursday the 26th is Thanksgiving: no fixed post, one optional Story. Saturday the 28th is Small Business Saturday."),
    4: ("Week 4", "November 30 to December 6. Restock after Thanksgiving, a chicha morada Reel and the December hours."),
}
KG_PANELS = [("resumen", "Overview")] + [(f"sem{n}", f"Week {n}") for n in (1, 2, 3, 4)]
kg_panels = B.panel("kg-resumen", "b-kg", "Overview", "Texts, image prompts, Reels and hashtags for K&G Market over four weeks.", rs)
for n in (1, 2, 3, 4):
    kg_panels += B.panel(f"kg-sem{n}", "b-kg", WEEK_TXT[n][0], WEEK_TXT[n][1], f'<div class="pieces">{W[n]}</div>', True)

# ---------------------------------------------------------------------------
# KLEAN N GREEN NYC: el paquete actual, con ids propios
# ---------------------------------------------------------------------------
kn_panels = K.panels.replace('class="panel b-all"', 'class="panel b-klean"')
kn_panels = re.sub(r'(id|aria-labelledby)="(panel|tab)-(resumen|sem[1-4])"', r'\1="\2-kn-\3"', kn_panels)
kn_panels = kn_panels.replace("Four-week board", "Four-week calendar")

import tiktok_html as TH
import linkedin_video as LV  # imported first so Daniel's LinkedIn videos are registered before the Characters sections are built

kg_panels = TH.inject(kg_panels, "kg")
kn_panels = TH.inject(kn_panels, "kn")
kn_panels = LV.inject(kn_panels, "kn")


def tab_buttons(brand, cls, items):
    return "".join(
        f'<button type="button" role="tab" id="tab-{brand}-{i}" class="tab {cls}" aria-controls="panel-{brand}-{i}" '
        f'aria-selected="false" data-tab="{i}"><i class="dot"></i>{e(n)}</button>'
        for i, n in items
    )


kg_tabs = tab_buttons("kg", "b-kg", KG_PANELS)
kn_tabs = tab_buttons("kn", "b-klean", KG_PANELS)

JS_HEAD = """
(function(){
  var BR={kg:['resumen','sem1','sem2','sem3','sem4'],kn:['resumen','sem1','sem2','sem3','sem4']};
  var bar=document.getElementById('brands');
  var state={brand:'kg',kg:'resumen',kn:'resumen'};
  function showBrand(b){
    Object.keys(BR).forEach(function(k){
      var p=document.getElementById('brand-'+k),t=document.getElementById('btab-'+k),on=(k===b);
      p.hidden=!on;
      t.setAttribute('aria-selected',on?'true':'false');
      t.tabIndex=on?0:-1;
    });
    state.brand=b;
  }
  function showTab(b,id,scroll){
    if(BR[b].indexOf(id)<0){id='resumen';}
    BR[b].forEach(function(k){
      var p=document.getElementById('panel-'+b+'-'+k),t=document.getElementById('tab-'+b+'-'+k),on=(k===id);
      p.hidden=!on;
      t.setAttribute('aria-selected',on?'true':'false');
      t.tabIndex=on?0:-1;
      if(on){try{t.scrollIntoView({inline:'center',block:'nearest'});}catch(e){}}
    });
    state[b]=id;
    if(scroll){try{
      var nav=document.getElementById('tabs-'+b);
      var top=document.getElementById('panel-'+b+'-'+id).getBoundingClientRect().top+window.pageYOffset-bar.offsetHeight-nav.offsetHeight-4;
      window.scrollTo(0,Math.max(0,top));
    }catch(e){}}
  }
  function hashOf(b,id){return b+(id==='resumen'?'':'-'+id);}
  function apply(scroll){
    var m=/^(kg|kn)(?:-(.+))?$/.exec((location.hash||'').replace('#',''));
    var b=m?m[1]:state.brand,id=m&&m[2]?m[2]:(m?'resumen':state[b]);
    showBrand(b);showTab(b,id,scroll);
  }
  var bt=document.querySelectorAll('.btab');
  Array.prototype.forEach.call(bt,function(t,i){
    t.addEventListener('click',function(){
      var b=t.getAttribute('data-brand');
      showBrand(b);showTab(b,state[b],false);
      try{location.hash=hashOf(b,state[b]);}catch(e){}
      window.scrollTo(0,0);
    });
    t.addEventListener('keydown',function(ev){
      var j=-1;
      if(ev.key==='ArrowRight'){j=(i+1)%bt.length;}
      if(ev.key==='ArrowLeft'){j=(i-1+bt.length)%bt.length;}
      if(j>=0){ev.preventDefault();bt[j].focus();bt[j].click();}
    });
  });
  ['kg','kn'].forEach(function(b){
    var tl=document.querySelectorAll('#tabs-'+b+' .tab');
    Array.prototype.forEach.call(tl,function(t,i){
      t.addEventListener('click',function(){
        var id=t.getAttribute('data-tab');
        showTab(b,id,true);
        try{location.hash=hashOf(b,id);}catch(e){}
      });
      t.addEventListener('keydown',function(ev){
        var j=-1;
        if(ev.key==='ArrowRight'){j=(i+1)%tl.length;}
        if(ev.key==='ArrowLeft'){j=(i-1+tl.length)%tl.length;}
        if(j>=0){ev.preventDefault();tl[j].focus();tl[j].click();}
      });
    });
  });
  window.addEventListener('hashchange',function(){apply(false);});
  apply(false);
"""
_copy = B.JS.split("  document.addEventListener('click',function(ev){", 1)[1]
JS = (JS_HEAD + "\n  document.addEventListener('click',function(ev){" + _copy).replace("'Copiado'", "'Copied'").replace("'Seleccione y copie'", "'Select and copy'")
assert "Copied" in JS and "btab-" in JS

EXTRA_CSS = K.EXTRA_CSS + """
:root{--bh:62px}
.brands{position:sticky;top:0;z-index:6;background:var(--bg);border-bottom:1px solid var(--line)}
.brandlist{max-width:920px;margin:0 auto;display:flex;gap:8px;padding:8px}
.btab{flex:1 1 0;display:flex;align-items:center;justify-content:center;gap:8px;min-height:44px;padding:8px 10px;border:1px solid var(--line);border-radius:12px;background:var(--surface);color:var(--muted);font:600 15px/1.15 var(--font-body);cursor:pointer;text-align:center}
.btab .dot{flex:0 0 auto;width:10px;height:10px;border-radius:50%;background:var(--brand)}
.btab[aria-selected="true"]{background:var(--brand-soft);color:var(--ink);border-color:var(--brand)}
.btab:hover{color:var(--ink)}
.tabs{top:var(--bh)}
.main{max-width:920px;margin:0 auto;padding:8px 16px 40px}
.pieces{grid-template-columns:minmax(0,1fr)}
.brandpane[hidden]{display:none}
"""

TOP = """<header class="top">
<p class="eyebrow">Content packs · November 9 to December 6, 2026</p>
<h1>Posts by brand</h1>
<p class="lead">One tab per brand. Each tab opens that brand's 28-day calendar, with the texts, image prompts, Reels, TikTok videos and hashtags ready to copy. Dates and times are New York time.</p>
</header>"""

FOOT = """<footer>
<div class="fnt">
<p><b>How to use it.</b> Choose the brand at the top, then a week. Each card has copy-ready text with a Copy button. All times are New York time.</p>
<p><b>Limits.</b> The texts are based on each brand's strategy and calendar. Items that depend on the business are listed under "Before approving" in each Overview. Nothing is published without approval.</p>
</div>
</footer>"""

DOC = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Posts by brand: K&amp;G Market and Klean N Green NYC</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{B.FONTS}" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">
<style>{B.CSS}{EXTRA_CSS}</style>
</head>
<body>
{TOP}
<nav class="brands" id="brands"><div class="brandlist" role="tablist" aria-label="Brands">
<button type="button" role="tab" id="btab-kg" class="btab b-kg" aria-controls="brand-kg" aria-selected="true" data-brand="kg"><i class="dot"></i>K&amp;G Market</button>
<button type="button" role="tab" id="btab-kn" class="btab b-klean" aria-controls="brand-kn" aria-selected="false" data-brand="kn"><i class="dot"></i>Klean N Green NYC</button>
</div></nav>
<div class="brandpane" id="brand-kg" role="tabpanel" aria-labelledby="btab-kg">
<nav class="tabs" id="tabs-kg"><div class="tablist" role="tablist" aria-label="K&amp;G Market sections">{kg_tabs}</div></nav>
<div class="main">
{kg_panels}
</div>
</div>
<div class="brandpane" id="brand-kn" role="tabpanel" aria-labelledby="btab-kn" hidden>
<nav class="tabs" id="tabs-kn"><div class="tablist" role="tablist" aria-label="Klean N Green NYC sections">{kn_tabs}</div></nav>
<div class="main">
{kn_panels}
</div>
</div>
{FOOT}
<script>{JS}</script>
</body>
</html>
"""

DOC = (
    DOC.replace(">Copiar</button>", ">Copy</button>")
    .replace('chip chip-dato">Dato<', 'chip chip-dato">Data<')
    .replace('chip chip-ref">Referencia<', 'chip chip-ref">Reference<')
    .replace('chip chip-hip">Hipótesis<', 'chip chip-hip">Hypothesis<')
)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(DOC)

if __name__ == "__main__":
    print("ok", len(DOC))
