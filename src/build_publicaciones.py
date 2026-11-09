#!/usr/bin/env python3
# Genera klean-nyc-publicaciones-sem1-4.html: prompts de imagen, copy y hashtags de Klean N Green NYC
# para las semanas 1 a 4, reutilizando estilos y scripts de build_estrategia.py
import io
import os

os.environ.setdefault("CONTENT_LANG", "en")
import json
import re
import contextlib

with contextlib.redirect_stdout(io.StringIO()):
    import build_estrategia as B
import characters as CH

OUT = "klean-nyc-publicaciones-sem1-4.html"
e, fmt = B.e, B.fmt

UTM = "https://kleannyc.com/contact-us/?utm_source={src}&utm_medium={med}&utm_campaign={camp}"


def link(src, med, camp):
    return UTM.format(src=src, med=med, camp=camp)


def link_to(path, src, med, camp):
    """UTM link to any page of the site (path as it appears on the website)."""
    return f"https://kleannyc.com{path}?utm_source={src}&utm_medium={med}&utm_campaign={camp}"


TAGS_LI_PM = "#NYCCleaning #PropertyManagement #CommercialCleaning"
TAGS_LI_OF = "#NYCCleaning #OfficeCleaning #FacilitiesManagement"
TAGS_LI_REV = "#NYCCleaning #CustomerReviews #CleaningService"
TAGS_IG = "#NYCCleaning #ResidentialCleaning #CleaningTips #ApartmentCleaning #SundayReset"
TAGS_IG_WED = "#NYCCleaning #ResidentialCleaning #CleaningTips #ApartmentCleaning #KitchenCleaning"
TAGS_IG_WED2 = "#NYCCleaning #ResidentialCleaning #CleaningTips #ApartmentCleaning #HostingTips"
TAGS_IG_WED3 = "#NYCCleaning #ResidentialCleaning #CleaningTips #ApartmentCleaning #KitchenReset"
TAGS_IG_BA = "#NYCCleaning #ResidentialCleaning #BeforeAndAfter #CleaningTransformation #ApartmentCleaning"
TAGS_IG_WIN = "#NYCCleaning #ResidentialCleaning #CleaningTips #ApartmentCleaning #WinterHome"
TAGS_FB = "#NYCCleaning #ResidentialCleaning #CleaningTips"

# ---------------------------------------------------------------------------
# LinkedIn (se crean como borrador en Metricool)
# ---------------------------------------------------------------------------
LI = {}

LI["2026-11-10"] = (
    "Turnover week: 5 checks before the next tenant walks in.\n\n"
    "1. Kitchen: inside the oven, fridge and cabinets.\n"
    "2. Bathrooms: grout, fixtures and exhaust fans.\n"
    "3. Windows: glass, tracks and sills.\n"
    "4. Floors: edges and corners, not only the center.\n"
    "5. Final walkthrough with photos.\n\n"
    "A unit can look clean from the doorway and still fail the first walkthrough. These five spots are where it usually shows.\n\n"
    "Property managers in NYC: tell us how many units you turn over each month and we will scope it. "
    "Request a free estimate: " + link("linkedin", "social", "nov2026_turnover") + "\n\n" + TAGS_LI_PM
)

LI["2026-11-12"] = (
    "What does office cleaning actually include?\n\n"
    "The scope changes with the space, but a regular office clean usually covers:\n"
    "• Desks and shared surfaces, including high-touch points like handles and switches\n"
    "• Kitchenette and break room\n"
    "• Restrooms, cleaned and restocked\n"
    "• Trash and recycling\n"
    "• Floors, vacuumed and mopped\n"
    "• Entrance, glass and common areas\n\n"
    "The right frequency depends on headcount and how the space is used. A 3-person studio and a 40-person floor need different plans.\n\n"
    "Message us the size of your space and how often you would like service, and we will send a scope.\n\n" + TAGS_LI_OF
)

LI["2026-11-17"] = (
    "How we verify a unit before handing it back, in 3 steps:\n\n"
    "1. A room-by-room checklist, so nothing depends on memory.\n"
    "2. Photos of the key areas: kitchen, bathrooms, floors and windows.\n"
    "3. A final walkthrough before we call it done.\n\n"
    "For property managers, the photos are the useful part: they show the condition of the unit at handover.\n\n"
    "See the full cleaning checklist: " + link_to("/post-construction-cleaning-checklist/", "linkedin", "social", "nov2026_verificacion") + "\n\n" + TAGS_LI_PM
)

LI["2026-11-24"] = (
    "Before the office closes for the holidays: a 6-point cleaning checklist. Swipe through.\n\n"
    "1. Clear and wipe desks, so nothing sits for two weeks.\n"
    "2. Empty the break room fridge and microwave.\n"
    "3. Restrooms: deep clean and restock.\n"
    "4. Trash and recycling: empty everything and replace liners.\n"
    "5. Floors: vacuum and mop, including corners and under desks.\n"
    "6. Glass, entrance and high-touch points.\n\n"
    "Coming back to a clean office on the first Monday of January sets the tone for the quarter.\n\n"
    "Planning a pre-break deep clean? Request a free estimate: " + link_to("/commercial", "linkedin", "social", "nov2026_cierre_oficina") + "\n\n" + TAGS_LI_OF
)

LI["2026-12-01"] = (
    "Property managers: a year-end cleaning calendar for December.\n\n"
    "Dec 1-6: schedule cleans for units that will sit vacant over the holidays.\n"
    "Dec 7-13: common areas, including lobby, hallways and entrances.\n"
    "Dec 14-20: confirm access, keys and building rules for the holiday week.\n"
    "Dec 21-27: only what cannot wait, like move-outs.\n"
    "Early January: plan turnovers for the new year.\n\n"
    "Sequencing it early keeps the holiday week calm.\n\n"
    "Planning your December? Message us the units and dates and we will help you put them in order.\n\n" + TAGS_LI_PM
)

LI["2026-11-26"] = (
    "Happy Thanksgiving from all of us at Klean N Green NYC.\n\n"
    "Thank you to the property managers, office teams and families in New York City who trust us with their spaces.\n\n"
    "Wishing you a calm day, and an easy cleanup tomorrow.\n\n"
    "#NYCCleaning #Thanksgiving #PropertyManagement"
)

FB_THANKS = (
    "Happy Thanksgiving from Klean N Green NYC.\n\n"
    "Thank you to the families, offices and property managers who trust us with their spaces. Wishing you a calm day, and an easy cleanup tomorrow.\n\n"
    "#NYCCleaning #Thanksgiving #CleaningTips"
)

LI["2026-12-03"] = (
    "What does cleaning for property management include? Swipe through.\n\n"
    "• Turnover cleans for vacant units between tenants\n"
    "• Vacation rental and corporate housing cleans between guests\n"
    "• Post-renovation cleaning before a unit goes back on the market\n"
    "• Photos of the key areas at handover\n\n"
    "Every building is different. Tell us the type of property and the number of units, and we will put together a plan.\n\n"
    "Request a free estimate: " + link_to("/professional-cleaning-service-in-brooklyn/", "linkedin", "social", "dic2026_administracion") + "\n\n" + TAGS_LI_PM
)

REVIEW_QUOTE = "Amazing service. This team is unbelievable. They came right away the next day on a Sunday and did an amazing job. I recommend them highly!!!!"
LI_REVIEW = (
    "\u2605\u2605\u2605\u2605\u2605\n\n"
    "\"" + REVIEW_QUOTE + "\"\n"
    "Client, Google review\n\n"
    "What stood out for this client: a next-day visit, on a Sunday.\n\n"
    "Thank you for taking the time to write it.\n\n"
    "Read more reviews from NYC clients: " + link_to("/testimonials/", "linkedin", "social", "nov2026_resena") + "\n\n" + TAGS_LI_REV
)

# ---------------------------------------------------------------------------
# Google Business Profile (borradores en Metricool, solo texto; imagen y boton se agregan en el editor)
# ---------------------------------------------------------------------------
GBP = {
    "2026-11-09": (
        "Green cleaning for homes, offices and rentals in Manhattan, Brooklyn and Queens. "
        "Klean N Green NYC cleans apartments and houses, offices, rental properties and post-construction sites.\n\n"
        "Book now to request a free estimate: https://kleannyc.com/contact-us/?utm_source=google&utm_medium=gbp&utm_campaign=nov2026_overview&utm_content=book_now"
    ),
    "2026-11-16": (
        "Turnover cleans for rentals and vacation properties. Between tenants or guests, we get the unit ready for the next arrival.\n\n"
        "Learn more about how it works: https://kleannyc.com/vacation-rentals-cleaning/?utm_source=google&utm_medium=gbp&utm_campaign=nov2026_turnover&utm_content=learn_more\n\n"
        "Then send us your dates and the number of units."
    ),
    "2026-11-23": (
        "Planning a pre-holiday office clean? Tell us the size of your space and how often you want service, and we will send a scope.\n\n"
        "Request a scope: https://kleannyc.com/contact-us/?utm_source=google&utm_medium=gbp&utm_campaign=nov2026_office&utm_content=request_scope"
    ),
    "2026-11-30": (
        "Recurring home cleaning: weekly, every two weeks or monthly. "
        "A steady schedule keeps the home ready all month.\n\n"
        "Book now to request a free estimate: https://kleannyc.com/contact-us/?utm_source=google&utm_medium=gbp&utm_campaign=nov2026_recurring&utm_content=book_now"
    ),
}

# Google Business Profile button per post: (button, link or None)
GBP_BTN = {
    "2026-11-09": ("Book", "https://kleannyc.com/contact-us/?utm_source=google&utm_medium=gbp&utm_campaign=nov2026_overview&utm_content=book_now"),
    "2026-11-16": ("Learn more", "https://kleannyc.com/vacation-rentals-cleaning/?utm_source=google&utm_medium=gbp&utm_campaign=nov2026_turnover&utm_content=learn_more"),
    "2026-11-23": ("Learn more", "https://kleannyc.com/contact-us/?utm_source=google&utm_medium=gbp&utm_campaign=nov2026_office&utm_content=request_scope"),
    "2026-11-30": ("Book", "https://kleannyc.com/contact-us/?utm_source=google&utm_medium=gbp&utm_campaign=nov2026_recurring&utm_content=book_now"),
}

# ---------------------------------------------------------------------------
# Image prompts: one per image, each complete (a generator creates one image per prompt). Photorealistic style.
# ---------------------------------------------------------------------------
# Brand system taken from the website (global colors and fonts). Used in every image prompt and shown in the Overview.
PALETTE = [
    ("Primary green", "#2E7D32", "Main accent: check marks, thin rules and the call-to-action panel. White text on it passes contrast (5.1:1)."),
    ("Bright green", "#4CB748", "Tiny decorative details only (accent line, dot, leaf). Never for text: 2.6:1 on white."),
    ("Ink", "#1E2A23", "Headlines and anything that must be read first (13.8:1 on the off-white)."),
    ("Paragraph text", "#55645B", "Body copy and captions (5.8:1 on the off-white)."),
    ("Slate", "#54595F", "Secondary labels and icons (6.5:1 on the off-white)."),
    ("Background", "#F7F6F1", "Warm off-white: the text panel and any flat background."),
    ("Hover tint", "#DCEBD5", "Soft green for secondary shapes, chips and hairline dividers."),
    ("White", "#FFFFFF", "Highlights and text on green."),
]

BRAND = (
    "Brand colors, in this proportion: about 60% warm off-white #F7F6F1 and white #FFFFFF, about 30% the natural tones of the photo and dark ink #1E2A23, "
    "and about 10% green, with forest green #2E7D32 as the main accent and bright green #4CB748 only for tiny decorative details such as a short accent line. "
    "Body text color #55645B; soft green tint #DCEBD5 for secondary shapes and hairline dividers."
)
TYPE = (
    "Typography: headline in Cormorant Garamond bold (an elegant high-contrast serif), color #1E2A23; "
    "body text and labels in Jost regular or medium (a clean geometric sans-serif), color #55645B."
)
DESIGN = (
    "Design: one text panel in warm off-white #F7F6F1 with 28 px rounded corners, between 45% and 80% of the frame height and inside a 90 px safe margin, "
    "with a 6 x 120 px bright-green #4CB748 accent line above the headline. Clear hierarchy: the headline at least 1.8 times larger than the body text. "
    "Everything left-aligned to one edge, generous white space inside the panel, large and legible on a phone. "
    "Compose the photo with the subject on one third of the frame and keep at least half of the image visible as photo around the panel."
)


def style(fmt_txt="Vertical 4:5 format, 1080 x 1350 px"):
    return (
        "Photorealistic photograph, not an illustration, for a social media post by Klean N Green NYC, a green cleaning company in New York City. "
        f"{fmt_txt}. Shot on a full-frame camera with a 35mm lens, natural window daylight at about 5500 K, shallow depth of field, realistic textures and true-to-life colors, "
        "bright and airy, in a real New York apartment or office, with the same soft light and color grading in every image of the set. "
        "Props and surfaces in white, soft neutral and natural wood tones, with leaf-green accents such as a plant or a green microfiber cloth. "
        "No cartoon, vector or 3D-render look, no faces (only hands if a person appears), no readable brand names or product labels, no logos, no badges, no prices, no claims. "
        + BRAND + " " + TYPE + " " + DESIGN + " "
        "Leave a clear empty square of 160 x 160 px at the bottom left for the logo, which I will add later; do not draw a logo."
    )


NO_NUM = "Do not add slide numbers, page counters, arrows, dots or swipe hints anywhere on the image."


HANDS = {
    "6 kitchen spots people miss": "the hands of an older adult, medium-brown skin with a few age spots, short natural nails, no jewelry",
    "Sunday reset: 20 minutes, 6 spots": "the hands of a young adult, pale skin with light freckles, short natural nails, no jewelry",
    "Entryway: first impression in 5 points": "adult hands with deep brown skin, short natural nails, no jewelry",
    "After dinner: the kitchen in 30 minutes": "adult hands with light-beige skin and warm undertones, short natural nails, no jewelry",
    "Office checklist before the holidays": "adult hands with olive skin, short natural nails, no jewelry, a plain watch is fine",
    "What property management cleaning includes": "adult hands with tan skin and a few fine lines, short natural nails, no jewelry",
}


# Carousels of the draft weeks use the hands of a recurring character, so the set matches the videos and single images.
HANDS_CHAR = {
    "After dinner: the kitchen in 30 minutes": ("maya", "2026-11-25", "Instagram carousel"),
    "Office checklist before the holidays": ("daniel", "2026-11-24", "LinkedIn carousel"),
    "What property management cleaning includes": ("daniel", "2026-12-03", "LinkedIn carousel"),
}
for _t, (_k, _d, _f) in HANDS_CHAR.items():
    HANDS[_t] = CH.hands_text(_k)
    CH.use(_k, _d, _f, _t)


def slide_prompt(title, i, n, head, body, scene, handle="@kleanngreen"):
    role = "cover slide" if i == 1 else ("closing slide" if i == n else "content slide")
    s = style() + f" This is the {role} of a carousel titled \"{title}\". "
    s += "Write exactly this text on the image, in English, spelled exactly as given, and add no other text: "
    s += f"headline \"{head}\""
    if body:
        s += f"; body \"{body}\""
    s += ". "
    if i == 1:
        s += "Make the headline very large, at least 96 px. "
    else:
        s += "Set the headline at about 64 px and the body text at about 36 px. "
    if i == n:
        s += ("On this closing slide use a forest-green #2E7D32 panel with a white Cormorant Garamond headline instead of the off-white panel, "
              "so the set ends with a clear signal. ")
    s += f"Photo scene: {scene}. "
    if title in HANDS:
        s += f"If hands appear in the photo, they are {HANDS[title]}, the same on every slide of this set. "
    if title in HANDS_CHAR and "Maya" in scene:
        k = HANDS_CHAR[title][0]
        s += (f"This is the one slide of the set where a face appears, and the rule above about faces does not apply to {CH.name(k)}: {CH.identity(k)}. "
              + CH.ref_sentence(k) + " Candid, relaxed, not looking at the camera, natural hands with five fingers. ")
    s += NO_NUM
    if i == n:
        s += f" Also write \"{handle}\" in small Jost text at the bottom right."
    return s


# key -> (carousel title, [(headline, body, photo scene)])
CAR = {}

CAR["11-11"] = ("6 kitchen spots people miss", [
    ("6 kitchen spots people miss", "Swipe to check your list", "a bright, spotless kitchen counter in a New York apartment with a leaf-green microfiber cloth and an unlabeled spray bottle, soft morning light"),
    ("1. Microwave", "Splatters build up on the ceiling and turntable. Steam a bowl of water, then wipe.", "close-up of an open microwave with a hand wiping the glass turntable with a leaf-green microfiber cloth, a little steam rising"),
    ("2. Range hood filter", "Grease collects here. Soak it in hot, soapy water and let it dry fully.", "a metal range hood filter resting in a sink of hot soapy water with a sponge beside it"),
    ("3. Cabinet fronts and handles", "Near the stove they gather a film. Wipe from top to bottom.", "close-up of a hand wiping a white kitchen cabinet door and its brushed-steel handle with a cloth"),
    ("4. Behind small appliances", "Crumbs hide behind the toaster and coffee maker. Unplug, move, wipe.", "a toaster and a coffee maker pulled slightly away from the wall on a clean counter, a hand wiping the space behind them"),
    ("5. Sink drain and faucet base", "Residue builds where water pools. Use a soft brush on the edges.", "close-up of a stainless-steel faucet base and sink edge with a hand scrubbing it with a small soft brush"),
    ("6. Fridge door seal", "Crumbs hide in the rubber folds. Wipe with a damp cloth.", "close-up of a hand wiping the rubber seal of an open fridge door with a damp cloth"),
    ("Save this for your next cleaning day", "", "a tidy kitchen counter with a smartphone, a small notebook and a cup of coffee in soft daylight"),
])

CAR["11-15"] = ("Sunday reset: 20 minutes, 6 spots", [
    ("Sunday reset", "20 minutes, 6 spots", "a bright, tidy apartment kitchen on a Sunday morning with a small kitchen timer on the counter"),
    ("1. Sink and counters", "4 min", "a clean kitchen sink and counter with a sponge and an unlabeled spray bottle, a hand wiping the counter"),
    ("2. Bathroom mirror and faucet", "3 min", "a bright bathroom mirror and a chrome faucet, spotless, a hand holding a microfiber cloth"),
    ("3. Floors at the entrance", "4 min", "a clean entryway floor with a doormat, a hand pushing a microfiber mop near the front door"),
    ("4. Trash and recycling", "2 min", "a kitchen trash bin and a recycling bin side by side with fresh liners"),
    ("5. Bedding", "4 min", "a neatly made bed with crisp white sheets and two pillows in soft light"),
    ("6. Fridge shelf cleanup", "3 min", "an open fridge with one shelf freshly wiped clean and a hand placing a container"),
    ("Save this for next Sunday", "", "a tidy bedside table with a phone and a notebook in soft morning light"),
])

CAR["11-22"] = ("Entryway: first impression in 5 points", [
    ("Your entryway, in 5 points", "The first thing guests see", "a bright apartment entryway with a welcome mat and a small console table, no people"),
    ("1. Door and handle", "Wipe the high-touch points.", "close-up of a hand wiping a door handle with a cloth"),
    ("2. Doormat", "Shake it out or vacuum it so grit stays outside.", "a doormat being shaken out at an apartment door, only hands visible"),
    ("3. Floor edges and corners", "Dust collects where the mop does not reach.", "a hand wiping a baseboard corner with a microfiber cloth"),
    ("4. Mirror and glass", "Remove smudges for a brighter space.", "a spotless hallway mirror reflecting a bright entryway"),
    ("5. Shoe and coat zone", "Clear it and tidy it once a week.", "a tidy shoe rack and coat hooks in an entryway"),
    ("Save this for your next Sunday reset", "", "a clean entryway with a small plant on a console table in soft light"),
])

CAR["11-25"] = ("After dinner: the kitchen in 30 minutes", [
    ("After dinner: the kitchen in 30 minutes", "A plan for the big meal", "a tidy kitchen after a holiday dinner with a kitchen timer on the counter, warm evening light"),
    ("1. Clear and stack, 5 min", "Scrape plates and stack them by type.", "neatly stacked dinner plates next to a sink, a hand scraping one plate"),
    ("2. Soak, 2 min", "Put the roasting pan and pots to soak.", "a roasting pan soaking in a sink full of soapy water"),
    ("3. Dishes, 10 min", "Load the dishwasher and hand-wash the rest.", "an open dishwasher being loaded with plates, a dish rack beside it"),
    ("4. Counters and stovetop, 8 min", "Wipe from top to bottom.", "a hand wiping a stovetop and counter with a cloth"),
    ("5. Floor and trash, 5 min", "Sweep the crumbs. Take out the trash.", "a broom sweeping crumbs on a kitchen floor next to a tied trash bag"),
    ("Save this for Thursday night", "", "a clean kitchen at night with soft warm lights and empty counters; in the background Maya sits relaxed at the dining table with a mug of tea in both hands, looking out of the frame, the work already done"),
])


# Before and after: only the text slide can be generated; the rest use real photos
BA_CLOSING = (
    style() + " This is the closing slide of a carousel about a real cleaning job. "
    "Write exactly this text on the image, in English, spelled exactly as given, and add no other text: "
    "headline \"What we did\"; body \"[short list of what was done]. Time: [hours].\"; "
    "call to action \"Message us for a free estimate\". "
    "Put the headline and body on the off-white panel and the call to action on a forest-green #2E7D32 band under it, with white Jost medium text, so the set ends with a clear signal. "
    "Photo scene: a clipboard with a blank checklist on a clean kitchen counter in soft daylight, no readable text on the clipboard. "
    + NO_NUM + " Write \"@kleanngreen\" in small Jost text at the bottom right."
)

BA_FRAME = (
    "Built in Canva with real photos, not with a generator. Slide 1 (cover): the best after photo full-bleed, "
    "with the headline \"Before and after\" in Cormorant Garamond bold and the label \"[type of space]\" in Jost. Slides 2 and 3: before and after of the same angle, "
    "labeled \"Before\" or \"After\" at the top left, in a forest-green #2E7D32 pill with white Jost medium text. Slides 4 and 5: before and after of a detail (oven, bathroom grout or window track), same labels. "
    "4:5 format, 1080 x 1350 px. No slide numbers or counters on any slide."
)

REVIEW_PROMPT = (
    style("Vertical 4:5 format, 1080 x 1350 px") + " Single image for a LinkedIn post: a customer review card. "
    "Photo scene: a softly blurred, bright apartment interior as the background. "
    "Write exactly this text on the image, in English, spelled exactly as given, and add no other text: "
    "quote \"" + REVIEW_QUOTE + "\"; attribution \"Client\". "
    "Layout: a large forest-green #2E7D32 quotation mark in Cormorant Garamond at the top left of the off-white panel, the quote set in Cormorant Garamond at 48 px or larger in #1E2A23, "
    "the attribution below it in Jost in #55645B, and five small bright-green #4CB748 stars under the attribution. "
    "Keep the quote exactly as given, with its four exclamation marks, and do not add a name."
)


def li_prompt(head, rows, layout, scene):
    s = style() + " Single image for a LinkedIn post. Write exactly this text on the image, in English, spelled exactly as given, and add no other text: "
    s += f"headline \"{head}\"; then these text lines, in this order: " + "; ".join(f"\"{r}\"" for r in rows) + ". "
    s += f"Layout: {layout}. Because this image carries a list, the panel is taller than usual: from 10% to 80% of the frame height, still above the logo square. "
    s += "Set the headline at about 64 px and the list at about 34 px, with equal spacing between rows. "
    s += f"Photo scene: {scene}. "
    s += "Write \"Klean N Green NYC\" in small Jost text at the bottom right. Do not add numbers other than the ones in the text above."
    return s


LIIMG = {
    "2026-11-10": li_prompt("Turnover week: 5 checks",
                            ["1. Kitchen: oven, fridge, cabinets", "2. Bathrooms: grout, fixtures, fans", "3. Windows: glass, tracks, sills", "4. Floors: edges and corners", "5. Final walkthrough with photos"],
                            "the off-white panel with the headline at the top and a vertical checklist of five rows, each row starting with a forest-green #2E7D32 check mark, rows separated by hairlines in #DCEBD5",
                            "a bright, empty, freshly cleaned apartment kitchen ready for a new tenant, with a single key on the counter"),
    "2026-11-12": li_prompt("What office cleaning includes",
                            ["Desks and shared surfaces", "Kitchenette and break room", "Restrooms, cleaned and restocked", "Trash and recycling", "Floors, vacuumed and mopped", "Entrance and glass"],
                            "the off-white panel with the headline at the top and a 2 by 3 grid of six small cards in soft green tint #DCEBD5, each card with one label in Jost",
                            "a modern, bright open office with desks, monitors and plants, freshly cleaned, no people"),
    "2026-11-17": li_prompt("How we verify a unit before handover",
                            ["1. Room-by-room checklist", "2. Photos of the key areas", "3. Final walkthrough"],
                            "the off-white panel with the headline at the top and three large steps stacked vertically, each with a forest-green #2E7D32 number in Cormorant Garamond",
                            "a clipboard and a smartphone resting on a clean apartment counter, no faces and no readable text on the clipboard"),
    "2026-12-01": li_prompt("December cleaning calendar for property managers",
                            ["Dec 1-6: vacant units", "Dec 7-13: common areas", "Dec 14-20: confirm access and keys", "Dec 21-27: only what cannot wait", "Early January: plan turnovers"],
                            "the off-white panel with the headline at the top and a vertical timeline of five dots on a thin forest-green #2E7D32 line, each dot with its label to the right",
                            "a desk with a laptop, a set of keys and a wall calendar in the background, soft daylight, no people"),
}


def gbp_prompt(scene):
    return (
        "Photorealistic photograph, not an illustration, for a Google Business Profile post by Klean N Green NYC, a green cleaning company in New York City. "
        "Horizontal 4:3 format, 1200 x 900 px. Shot on a full-frame camera with a 35mm lens, natural window daylight, shallow depth of field, realistic textures "
        "and true-to-life colors, bright and airy. Palette: warm off-white #F7F6F1 and white surfaces, natural wood, and a small accent of forest green #2E7D32 (a plant or a cloth). Subject on one third of the frame with calm negative space. Scene: " + scene + ". "
        "No text, no letters, no people, no faces, no logos, no readable brand names or product labels, no badges, no cartoon or vector look."
    )


GBPIMG = {
    "2026-11-09": gbp_prompt("a bright, spotless apartment living room with a sofa and a plant, a mop and an unlabeled spray bottle leaning neatly against the wall"),
    "2026-11-16": gbp_prompt("an apartment front door with a key in the lock and a clean hallway in soft light, suggesting a unit ready for the next arrival"),
    "2026-11-23": gbp_prompt("a tidy open office with four desks, monitors and a plant, freshly cleaned"),
    "2026-11-30": gbp_prompt("a bright, tidy living room in morning light with plumped sofa cushions and fresh flowers on the coffee table, suggesting a regular clean"),
}

PHOTO_BRIEF = [
    "Get the customer's written authorization before photographing and publishing.",
    "Same phone position, height and light in the before and after.",
    "Vertical or 4:5 photos. Two wide shots and two detail shots (oven, bathroom grout, window track).",
    "No people, personal items, addresses or door numbers in view.",
    "Do not use AI-generated images for a before and after: it has to be a real job.",
]

# ---------------------------------------------------------------------------
# Textos de Instagram y Facebook
# ---------------------------------------------------------------------------
IGC = {}
FBC = {}

IGC["11-11"] = (
    "Six kitchen spots that get skipped, even in a weekly clean. \U0001F9FD\n"
    "Swipe through and count how many you did this week.\n"
    "Save this for your next cleaning day.\n\n" + TAGS_IG_WED
)
FBC["11-11"] = (
    "Six kitchen spots that get skipped, even when the counters look clean: the microwave ceiling, the range hood filter, "
    "cabinet handles, the space behind small appliances, the faucet base and the fridge door seal.\n\n"
    "Which one do you skip most often? Tell us in the comments.\n\n" + TAGS_FB
)

IGC["11-15"] = (
    "Sunday reset: 20 minutes, 6 spots.\n"
    "Start the week in a home that already feels clean.\n"
    "Save this for next Sunday.\n\n" + TAGS_IG
)

IGC["11-18"] = (
    "Guests in 20 minutes? Here is the order that works.\n"
    "Entry (3 min), bathroom (5), kitchen (5), living room (5) and one last look (2).\n"
    "Send this to someone who is hosting this month.\n\n" + TAGS_IG_WED2
)
FBC["11-18"] = (
    "Guests arriving in 20 minutes? Here is the order that works: entry (3 min), bathroom (5), kitchen (5), living room (5) and one last look (2).\n\n"
    "What is your must-do before guests arrive?\n\n" + TAGS_FB
)

IGC["11-22"] = (
    "Your entryway sets the tone before anyone sits down.\n"
    "Five points that take a few minutes, once a week.\n"
    "Save this for your next Sunday reset.\n\n" + TAGS_IG
)

IGC["11-25"] = (
    "Tomorrow is the big meal. Here is a 30-minute plan for the kitchen afterward. \U0001F9FD\n"
    "Five steps, with the minutes for each.\n"
    "Save this for Thursday night.\n\n" + TAGS_IG_WED3
)
FBC["11-25"] = (
    "Tomorrow is the big meal. Here is a 30-minute plan for the kitchen afterward: clear and stack (5 min), soak the pots (2), "
    "dishes (10), counters and stovetop (8), floor and trash (5).\n\n"
    "Share it with whoever is doing the dishes. \U0001F609\n\n" + TAGS_FB
)

IGC["11-29"] = (
    "Sunday reset after the long weekend: 20 minutes, 6 spots.\n"
    "Fridge (3 min), counters and stove (4), floors (4), guest bathroom (3), linens (3) and trash (3).\n"
    "Save this for the next long weekend.\n\n" + TAGS_IG
)

IGC["12-02"] = (
    "A real job, before and after. [Type of space] in [neighborhood], cleaned in [hours].\n"
    "What we did: [short list].\n"
    "Message us for a free estimate.\n\n" + TAGS_IG_BA
)
FBC["12-02"] = (
    "Before and after: [type of space] in [neighborhood], cleaned in [hours]. What we did: [short list].\n\n"
    "Want the same for your place? Message us for a free estimate.\n\n" + TAGS_FB
)

# ---------------------------------------------------------------------------
# Pieces
# ---------------------------------------------------------------------------
DAYN = {"2026-11-09": "Mon, Nov 9", "2026-11-16": "Mon, Nov 16", "2026-11-23": "Mon, Nov 23", "2026-11-30": "Mon, Nov 30"}

S_DRAFT, S_IMG, S_REVIEW, S_PHOTOS, S_MANUAL = "Draft in Metricool", "Draft · add image", "Draft · add real review", "Draft · add real photos", "Post manually"
S_VID = "Draft · add video"
KIND = {S_DRAFT: "dato", S_IMG: "hip", S_REVIEW: "hip", S_PHOTOS: "hip", S_MANUAL: "ref", S_VID: "hip"}


def chipx(label, kind):
    return f'<span class="chip chip-{kind}">{e(label)}</span>'


def meta_box(items):
    return '<ul class="checks mini">' + "".join(f"<li>{fmt(x)}</li>" for x in items) + "</ul>"


PIECE_META = {}  # (day, hour) -> dict(type, tk, angle, mode); filled by kn_timeback.apply


def piece(day, hour, title, nets, formato, status, body):
    m = PIECE_META.get((day, hour))
    chips = chipx(status, KIND[status])
    angle = ""
    if m:
        chips = chipx(m["type"], m["tk"]) + " " + chips
        if m["mode"] == "draft":
            chips += " " + chipx(S_NEW, "hip")
        angle = f'<p class="angle"><b>Angle:</b> {e(m["angle"])}</p>'
    return (
        '<article class="piece">'
        '<div class="slot"><div class="when">'
        f"<b>{e(day)}</b><span>{e(hour)}</span></div>"
        f'<div class="what"><p class="what-t">{e(title)}</p>'
        f'<p class="what-m">{e(nets)} · {e(formato)} {chips}</p></div></div>'
        f"{angle}{body}</article>"
    )


def det(summary, inner, open_=False):
    return f'<details class="dt"{" open" if open_ else ""}><summary>{e(summary)}</summary>{inner}</details>'


# ---------------------------------------------------------------------------
# Featured images of linked pages (one prompt per page, shown in every piece that links to it)
# ---------------------------------------------------------------------------
def web_prompt(scene):
    return (
        "Photorealistic editorial photograph, not an illustration, for the website of Klean N Green NYC, a green cleaning company in New York City. "
        "Horizontal format, 1.91:1 ratio, 1200 x 630 px. Shot on a full-frame camera with a 35mm lens, natural window daylight, shallow depth of field, "
        "realistic textures and true-to-life colors, bright and airy. Palette: warm off-white #F7F6F1 and white surfaces, natural wood, and a small accent of forest green #2E7D32 (a plant or a cloth). "
        "Keep the main subject inside the central 60% of the frame so the image survives cropping to 16:9 and 1:1, and leave calm negative space on one side. "
        f"Scene: {scene}. "
        "No text, no logos, no watermarks, no readable brand names or product labels, no faces (only hands if a person appears), "
        "no cartoon, vector or 3D-render look."
    )


PAGE_IMG = {
    "contact": ("Contact", "/contact-us/", "klean-nyc-contact.jpg",
                "a tidy desk beside a window with a phone, a closed notebook, a pen, a cup of coffee and a small plant in soft morning light, calm and inviting, no readable text on any object",
                "Desk by a window with a phone, a notebook and a coffee cup"),
    "checklist": ("Post-construction cleaning checklist (article)", "/post-construction-cleaning-checklist/", "klean-nyc-post-construction-cleaning-checklist.jpg",
                  "a freshly renovated, empty apartment room with new white walls and light hardwood floors, a HEPA vacuum and a microfiber mop leaning against the wall, bright window light, no dust or debris, no people, no readable text",
                  "Freshly renovated empty room with a vacuum and a mop against the wall"),
    "testimonials": ("Testimonials", "/testimonials/", "klean-nyc-testimonials.jpg",
                     "a sunlit, welcoming apartment entryway with the front door slightly open, a woven welcome mat, a small plant on a console table and a coat hook with a soft scarf, calm and warm mood, no people, no readable text",
                     "Welcoming apartment entryway with a plant and a welcome mat"),
    "commercial": ("Commercial cleaning", "/commercial", "klean-nyc-commercial-cleaning.jpg",
                   "a bright open-plan office with four clear desks, monitors, plants, a glass partition and a freshly vacuumed carpet, soft daylight, no people",
                   "Bright open-plan office with clear desks and plants"),
    "brooklyn": ("Cleaning service in Brooklyn", "/professional-cleaning-service-in-brooklyn/", "klean-nyc-cleaning-service-brooklyn.jpg",
                 "a bright Brooklyn apartment living room with tall windows and parquet floors, a sofa with a folded throw, and softly blurred brownstone stoops and a tree-lined street outside, calm morning light, no people",
                 "Bright Brooklyn apartment living room with tall windows and parquet floors"),
    "vacation": ("Vacation rentals and turnover", "/vacation-rentals-cleaning/", "klean-nyc-vacation-rental-cleaning.jpg",
                 "a bright studio apartment ready for a guest, with a neatly made bed in crisp white linens, folded towels at the foot, a small plant on the nightstand and a key on a small tray, soft daylight",
                 "Made bed with white linens and folded towels in a rental apartment"),
}


def page_of(text):
    for frag, key in (("post-construction-cleaning-checklist", "checklist"), ("/testimonials/", "testimonials"),
                      ("kleannyc.com/commercial", "commercial"), ("professional-cleaning-service-in-brooklyn", "brooklyn"),
                      ("vacation-rentals-cleaning", "vacation")):
        if frag in text:
            return key
    return "contact"


def page_img_det(key):
    name, path, fname, scene, alt = PAGE_IMG[key]
    inner = meta_box([
        f"Page: **{name}** ({path}). This is the page's featured image and the preview card of the link.",
        "Generate it once: every piece that links to this page uses the same image.",
        f"File name: **{fname}**. Alt text: **{alt}**.",
        "Horizontal 1.91:1, 1200 x 630 px, no text. This is the website image, not the image of the post: post images are always 4:5, 1080 x 1350 px.",
    ]) + B.copybox("Featured image prompt (complete, paste into the generator)", web_prompt(scene))
    return det("Featured image of the linked page: prompt", inner, False)


def li_piece(key, day, hour, title):
    inner = B.copybox("LinkedIn text", LI[key])
    if "https://" in LI[key]:
        inner += meta_box(["URL shortener is on in the Metricool draft. The post is published with a short link (a t.mtrbio.com type domain) that redirects to the page with its UTM parameters.", "The draft preview still shows the long link, because the link is shortened at publishing time."])
    img = (
        meta_box(["The Metricool draft is text only. If this image is used, it gets added to the draft.", "4:5 format, 1080 x 1350 px."])
        + B.copybox("Image prompt (complete, paste into the generator)", LIIMG[key])
    )
    return piece(day, hour, title, "LinkedIn", "Text with optional image", S_DRAFT,
                 det("Text and hashtags", inner, True) + det("Optional image: prompt", img, False)
                 + (page_img_det(page_of(LI[key])) if "https://" in LI[key] else ""))


# LinkedIn carousels (uploaded as images, published as a PDF document). key -> (title, [(headline, body, photo scene)])
LICAR = {
    "2026-11-24": ("Office checklist before the holidays", [
        ("Office checklist before the holidays", "6 points before the doors close", "a tidy office with cleared desks in soft winter light, no people"),
        ("1. Clear and wipe desks", "So nothing sits for two weeks.", "a cleared office desk being wiped with a leaf-green microfiber cloth, only a hand visible, soft light"),
        ("2. Fridge and microwave", "Empty the break room fridge and microwave.", "an open, empty office break room fridge with clean shelves in bright light"),
        ("3. Restrooms", "Deep clean and restock.", "a clean office restroom with a row of sinks, a large mirror and a paper towel dispenser, no readable labels"),
        ("4. Trash and recycling", "Empty everything and replace the liners.", "an office trash bin with a fresh liner beside a recycling bin on a tidy floor"),
        ("5. Floors", "Vacuum and mop, including corners and under desks.", "a vacuum cleaner on a clean office carpet next to desks, no people"),
        ("6. Glass and high-touch points", "Entrance glass, handles and switches.", "a hand wiping the handle of a glass office entrance door with a cloth, bright entrance"),
        ("Planning a pre-break deep clean?", "Message us your space and dates for a free estimate.", "a quiet, tidy office with closed laptops and a small plant on a desk in winter light"),
    ]),
    "2026-12-03": ("What property management cleaning includes", [
        ("What property management cleaning includes", "Four things we cover", "a bright vacant apartment living room with large windows and polished wood floors, no furniture and no people"),
        ("Turnover cleans", "Vacant units between tenants.", "a bright, empty apartment bedroom with clean floors and open blinds, no people"),
        ("Vacation rentals and corporate housing", "Cleans between guests.", "a made bed with fresh white linens and folded towels in a bright furnished apartment"),
        ("Post-renovation cleaning", "Before a unit goes back on the market.", "a freshly renovated apartment kitchen with clean counters and no dust, no people"),
        ("Photos at handover", "Photos of the key areas show the condition of the unit.", "a hand holding a smartphone toward a clean apartment bathroom to photograph it, no faces"),
        ("Tell us about your buildings", "Share the property type and number of units for a free estimate.", "a bright vacant apartment hallway leading to a living room with polished floors, no people"),
    ]),
}


def li_car_piece(key, day, hour, title):
    title_c, slides = LICAR[key]
    n = len(slides)
    inner = B.copybox("LinkedIn text", LI[key])
    if "https://" in LI[key]:
        inner += meta_box(["URL shortener is on in the Metricool draft. The post is published with a short link (a t.mtrbio.com type domain) that redirects to the page with its UTM parameters.", "The draft preview still shows the long link, because the link is shortened at publishing time."])
    needs = meta_box([
        f"4:5 format, 1080 x 1350 px, {n} slides, PNG or JPG. Same size as the Instagram carousels, so the Canva design can be reused.",
        f"The Metricool draft is text only and is already set to publish images as a PDF carousel, with the document title \"{title_c}\". Add the {n} images to the LinkedIn draft in order; LinkedIn then shows one swipeable document.",
        "A carousel replaces the link preview card, so the featured image of the linked page is not needed for this post.",
        "Same visual system as the other carousels: one idea per slide and a green closing slide. On LinkedIn the closing slide carries the company name instead of the Instagram handle.",
    ])
    boxes = "".join(
        B.copybox(f"Slide {i} of {n}: " + ("cover" if i == 1 else "closing" if i == n else "content"),
                  slide_prompt(title_c, i, n, h, b, ic, handle="Klean N Green NYC"))
        for i, (h, b, ic) in enumerate(slides, 1)
    )
    return piece(day, hour, title, "LinkedIn", f"{n}-slide carousel", S_IMG,
                 det("Text and hashtags", inner, True)
                 + det("What the images need", needs, False)
                 + det(f"Prompts: {n} images, one per slide", boxes, False))


def ig_piece(key, day, hour, title, nets, formato, quick, status=S_IMG):
    parts = []
    if key == "12-02":
        parts.append(det("Real photos: what they need", meta_box(quick) + meta_box(PHOTO_BRIEF) + "<p class='note'>" + e(BA_FRAME) + "</p>", False))
        parts.append(det("Prompt for the closing slide (the only one that is generated)", B.copybox("Slide 6 of 6", BA_CLOSING), False))
    else:
        title_c, slides = CAR[key]
        n = len(slides)
        boxes = "".join(
            B.copybox(f"Slide {i} of {n}: " + ("cover" if i == 1 else "closing" if i == n else "content"), slide_prompt(title_c, i, n, h, b, ic))
            for i, (h, b, ic) in enumerate(slides, 1)
        )
        parts.append(det("What the images need", meta_box(quick), False))
        parts.append(det(f"Prompts: {n} images, one per slide", boxes, False))
    parts.append(det("Instagram text", B.copybox("Instagram text", IGC[key]), True))
    if key in FBC:
        parts.append(det("Facebook text", B.copybox("Facebook text", FBC[key]), False))
    return piece(day, hour, title, nets, formato, status, "".join(parts))


def gbp_piece(key, title):
    btn, url = GBP_BTN[key]
    inner = B.copybox("Google Business Profile text", GBP[key])
    if url:
        inner += meta_box([f"The link is in the text, labelled to match the call to action, with a UTM that ends in utm_content for the button name ({btn}). Metricool has no button field for Google, so in Google the link shows as plain text, not as a clickable button.", f"If you publish this post directly in Google, choose the button **{btn}** and paste the link below into the button's URL field."])
        inner += B.tagbox("Link for the button (if published directly in Google)", url)
    else:
        inner += meta_box([f"Button: **{btn}**. It uses the phone number already on the profile, so no link and no number in the text. Metricool cannot add this button, so this post still says \"Tap Call now\" and needs a decision: publish it directly in Google, or change the closing line to a link."])
    inner += meta_box(["Saved as a draft in Metricool, text only, for Monday at 10 AM (New York time). Google Business Profile is now connected to the brand.", "Add the image in the Metricool editor. The editor has no button option for Google."])
    img = (
        meta_box(["A real photo of the team or a job is better, horizontal 1200 x 900 px.", "If there is no photo, this generated image works as an alternative. Google prefers real photos of the business, so never use it to show the team or a real job."])
        + B.copybox("Image prompt (complete, paste into the generator)", GBPIMG[key])
    )
    return piece(DAYN[key], "10 AM", title, "Google Business Profile", "Post with image and button", S_DRAFT,
                 det("Text and button", inner, True) + det("Image: prompt", img, False)
                 + (page_img_det(page_of(url)) if url else ""))


SLIDES_FMT = "4:5 format, 1080 x 1350 px, {n} slides."

# ---------------------------------------------------------------------------
# Friday Reels and Saturday single images (added for a 7-day cadence)
# ---------------------------------------------------------------------------
TAGS_REEL = "#NYCCleaning #CleaningTips #ApartmentCleaning #SatisfyingClean #CleaningReel"
TAGS_SAT = "#NYCCleaning #ResidentialCleaning #CleaningService #ApartmentCleaning #NYCHome"
UTM_FB = "https://kleannyc.com/contact-us/?utm_source=facebook&utm_medium=social&utm_campaign="


# ---------------------------------------------------------------------------
# Seedance prompts, scene by scene. Spine: subject and action, camera, style, sound, constraints. One action and one camera move per scene.
# A continuity block (location, light, props, the same hand) is pasted at the start of every scene so the scenes match when edited together.
# ---------------------------------------------------------------------------
SD_SECS = 4
SD_STYLE = "photorealistic live-action footage in the Klean N Green NYC look: bright and airy, natural color, warm off-white and white tones with leaf-green accents, 24 fps, smooth slow satisfying motion"
SD_CONSTRAINTS = (
    "Constraints: only hands appear, no faces; no text, captions, subtitles or watermarks; no logos, no readable brand names or product labels; "
    "no cartoon, illustration or 3D-render look; natural, physically plausible hand and object movement; no cuts inside the scene."
)
SD_CONSTRAINTS_CHAR = (
    "Constraints: the only person is the recurring character named in the continuity block, a fictional AI character who does not speak and looks at the camera only for a moment; no other people; "
    "no text, captions, subtitles or watermarks; no logos, no readable brand names or product labels; "
    "no cartoon, illustration or 3D-render look; natural, physically plausible face, hand and object movement; no cuts inside the scene."
)
REEL_DATE = {"11-27": "2026-11-27", "12-04": "2026-12-04", "12-06": "2026-12-06"}
REEL_CHAR = {}  # reel key (here "11-27"; K&G uses "kg-11-11") -> character key


def anchor_char(k, place_and_props):
    x = CH.c(k)
    return (
        f"{place_and_props} The person is {CH.identity(k)}, with the same face, hair and clothes in every scene where the face shows. {CH.ref_sentence(k)} "
        f"In close-ups only {CH.pron(k, 'pos')} hands show: {x['hands']}."
    )


SD_SETTINGS = [
    "Aspect ratio 9:16 (vertical), the highest resolution the tool offers (1080 x 1920 px or above).",
    f"{SD_SECS} seconds per scene, 3 scenes, about 12 seconds in total. Use 5 seconds per scene if you want more room to trim when editing.",
    "Sound: ambient only (cloth on a surface, water). No music and no voice inside Seedance; add the voiceover (each Reel card has its script) and licensed music in the video editor.",
    "Paste the continuity block at the start of every scene prompt, so location, light, props and the hand stay the same from scene to scene.",
    "Generate and judge one scene at a time. If the tool offers it, use the last frame of the previous scene as the reference for the next one.",
    "Change one line at a time: if the movement is right but the framing is off, edit only the Camera line; if the framing is right but the movement is off, edit only Subject and action.",
    "Reels with Maya or Daniel (Nov 27, Dec 4 and Dec 6) use a constraints line that allows that one character and nobody else; attach the character's reference portrait to every scene prompt. The Reels of weeks 1 and 2 are already finished and stay hands-only.",
]


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


def seedance_combo(title, anchor, scenes, cons=None, through="the same hand is the through-line"):
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


CHAR_NAME = "Clover"
CHAR_CAT = (
    "Clover, the cat: an adult gray tabby shorthair with a white chest, white front paws and a small white blaze on the nose, "
    "green eyes, upright ears and a calm, curious expression, wearing a thin leaf-green #2E7D32 collar with no tag. "
    "Keep the same markings, size and collar every time. Clover is a real-looking cat in a real photo: natural proportions and pose, no clothes, nothing held in its paws, "
    "no human gestures or expressions. Clover is always clean and well groomed, and never sits on food, dishes, a sink or freshly folded linens."
)
CHAR_ALONE = "No other animals and no other people."


def style_photo():
    return (
        "Photorealistic photograph, not an illustration, for a social media post by Klean N Green NYC, a green cleaning company in New York City. "
        "Vertical 4:5 format, 1080 x 1350 px. Shot on a full-frame camera with a 35mm lens, natural window daylight at about 5500 K, shallow depth of field, "
        "realistic textures and true-to-life colors, bright and airy, in a real New York apartment, with the same soft light and color grading in every image of the set. "
        "Surfaces and props in warm whites (#F7F6F1 and #FFFFFF), soft neutral and natural wood tones, with leaf-green accents such as a plant; "
        "about 60% warm whites, 30% natural tones and 10% green, with forest green #2E7D32 as the main accent. "
        "Compose with the characters on one third of the frame, eyes sharp, with calm space around them; candid, as if the photo were taken in the middle of the moment. "
        "No cartoon, vector or 3D-render look. No text of any kind anywhere in the image: no letters, numbers, signs, labels, clock numerals, or writing on calendars, notebooks or screens. "
        "No logos and no readable brand names. "
        "Leave a clear, uncluttered square of 160 x 160 px at the bottom left for the logo, which I will add later; do not draw a logo."
    )


PERSON_RULES = (
    " Candid and absorbed in what they are doing, not looking at the camera. Natural proportions and natural hands with five fingers, no exaggerated smile. "
    "This person appears only in this image; do not reuse their face anywhere else in the set."
)
# key -> (person block for the prompt, who they are for the alt text)
CAST = {
    "11-14": ("The person: a Black man in his late fifties with short gray hair and a neatly trimmed gray beard, brown eyes, wearing a soft gray cardigan over a white t-shirt; a forest-green throw pillow on the sofa is the green accent." + PERSON_RULES,
              "A Black man in his late fifties in a gray cardigan"),
    "11-18": ("The person: a South Asian woman in her mid-twenties with long black hair in a loose braid and dark brown eyes, wearing a cream knit sweater and jeans; a small green plant on the shelf is the green accent." + PERSON_RULES,
              "A South Asian woman in her mid-twenties in a cream sweater"),
    "11-21": ("The person: a Latino man in his mid-thirties with short dark wavy hair and light stubble, wearing a gray hoodie with the sleeves pushed up and holding a leaf-green mug." + PERSON_RULES,
              "A Latino man in his mid-thirties in a gray hoodie"),
    "11-28": (CH.block_scene("maya", "a small green plant on the nightstand is the green accent"), CH.alt_person("maya")),
    "11-29": (CH.block_scene("daniel", "a green plant on the shelves in the background is the green accent"), CH.alt_person("daniel")),
    "12-05": (CH.block_scene("maya", "a leaf-green mug in hand is the green accent"), CH.alt_person("maya")),
}


CAST_CHAR = {"11-28": "maya", "11-29": "daniel", "12-05": "maya"}
SING_DATE = {"11-28": "2026-11-28", "11-29": "2026-11-29", "12-05": "2026-12-05"}


def single_photo_prompt(scene, person=None, char=None):
    if person and char:
        lead = f" Characters. {CH.name(char)} is a recurring character of the brand and Clover, the cat, is the same in every image of the set. "
        chars = person + " " + CHAR_CAT
    elif person:
        lead = " Characters. The person is specific to this image and does not recur; Clover, the cat, is the same in every image of the set. "
        chars = person + " " + CHAR_CAT
    else:
        lead = " Character, the same in every image of the set. "
        chars = CHAR_CAT
    return style_photo() + lead + chars + " " + CHAR_ALONE + " Scene: " + scene + "."


# key -> (title, [(on-screen text, clip scene)], Instagram text, Facebook text)
REEL = {
    "11-13": ("3 quick bathroom wipes", [
        ("3 quick bathroom wipes · 1. Faucet", "close-up of a hand wiping a chrome bathroom faucet with a leaf-green microfiber cloth, water spots disappearing, bright bathroom in natural light"),
        ("2. Mirror", "a hand wiping a bathroom mirror from top to bottom with a leaf-green microfiber cloth, leaving a clear streak-free reflection of a bright bathroom"),
        ("3. Sink · Save this for your next reset", "a hand wiping a white ceramic sink basin with a leaf-green microfiber cloth, ending on a clean shine in daylight"),
    ],
        "Three quick bathroom wipes: faucet, mirror, sink.\nA cloth and a minute each.\nSave this for your next reset.\n\n" + TAGS_REEL,
        "Three quick bathroom wipes: faucet, mirror and sink. A cloth and a minute each.\n\nWhich one do you skip most often? Tell us in the comments.\n\n" + TAGS_FB),
    "11-20": ("Window tracks: the spot nobody cleans", [
        ("The spot nobody cleans: window tracks", "close-up of a window track with a light layer of dust and grit, a bright apartment window in natural light"),
        ("Loosen it with a soft brush", "a hand brushing a window track with a small soft brush, loosening dust and grit"),
        ("Wipe with a damp cloth · Save this for before winter", "a hand wiping the window track with a damp cloth, ending on a clean track and a bright window with softly blurred buildings outside"),
    ],
        "Window tracks collect dust and grit, and they are easy to forget.\nLoosen it with a soft brush, then wipe with a damp cloth.\nSave this for before winter.\n\n" + TAGS_REEL,
        "Window tracks collect dust and grit, and they are easy to forget. Loosen it with a soft brush, then wipe with a damp cloth.\n\nWhen did you last clean yours? Tell us in the comments.\n\n" + TAGS_FB),
    "11-27": ("Guest room reset in 3 steps", [
        ("Guest room reset in 3 steps · 1. Strip the bed", "hands pulling used sheets off a bed in a bright guest room in morning light"),
        ("2. Wipe the nightstand", "a hand wiping a wooden nightstand with a cloth next to a small lamp in a bright room"),
        ("3. Remake the bed · Send this to someone with a guest room", "hands smoothing fresh white sheets over a bed, ending on a neatly made bed with folded towels at its foot"),
    ],
        "Guests heading home after the long weekend? Reset the guest room in three steps: strip the bed, wipe the nightstand, remake with fresh sheets.\nSend this to someone with a guest room.\n\n" + TAGS_REEL,
        "Guests heading home after the long weekend? Reset the guest room in three steps: strip the bed, wipe the nightstand, remake with fresh sheets.\n\nWhat is the first thing you do after guests leave?\n\n" + TAGS_FB),
    "12-04": ("Wipe the spots everyone touches", [
        ("Before the holiday visits · 1. Door handles", "a hand wiping a brushed-steel apartment door handle with a leaf-green microfiber cloth in a bright entryway"),
        ("2. Light switches", "a hand wiping a white wall light switch plate with a cloth in a bright hallway"),
        ("3. Remote controls · Save this for the weekend", "a hand wiping a TV remote control with a cloth on a coffee table, no readable button labels"),
    ],
        "Before the holiday visits, wipe the spots everyone touches: door handles, light switches and remote controls.\nSave this for the weekend.\n\n" + TAGS_REEL,
        "Before the holiday visits, wipe the spots everyone touches: door handles, light switches and remote controls.\n\nWhich one do you forget most often? Tell us in the comments.\n\n" + TAGS_FB),
    "12-06": ("Winter entryway: 3 quick fixes", [
        ("Winter entryway · 1. Wipe the salt", "close-up of a hand wiping white road-salt marks off a dark slate entryway floor with a damp leaf-green microfiber cloth, the floor ending clean"),
        ("2. Boots on a tray", "a hand setting a pair of wet winter boots on a black rubber boot tray beside an apartment door, a few drops of melted snow falling onto the tray"),
        ("3. Shake out the mat · Send this to someone in a walk-up", "two hands lifting a rubber doormat, shaking it once and laying it back square at the door of a tidy winter entryway"),
    ],
        "Winter entryways take a beating: salt, wet boots and a gritty mat.\nThree quick habits: wipe the salt, put wet boots on a tray, shake out the mat.\nSend this to someone who lives in a walk-up.\n\n#NYCCleaning #CleaningTips #ApartmentCleaning #WinterHome #CleaningReel",
        None),
}

# key -> (headline, body, photo scene, Instagram text, Facebook text)
SING = {
    "11-14": ("First clean? Send us these 4 details",
              "The person sits on a sofa in a bright New York apartment living room, writing in a blank open notebook with a pen and a phone resting on the coffee table beside him; Clover sits next to him looking at the phone, soft morning light",
              CAST["11-14"][1] + " writes in a notebook on a sofa while a gray tabby cat with a green collar looks at a phone on the coffee table.",
              "Booking a first clean? Four details help us give you an accurate estimate: rooms and bathrooms, pets at home, how we get in, and what matters most to you.\nMessage us for a free estimate.\n\n" + TAGS_SAT,
              "Booking a first clean? Four details help us give you an accurate estimate: rooms and bathrooms, pets at home, how we get in, and what matters most to you.\n\nRequest a free estimate: " + UTM_FB + "nov2026_first_clean\n\n" + TAGS_FB),
    "11-21": ("How often should we clean?",
              "The person leans on a kitchen counter with a leaf-green mug of coffee, looking thoughtfully at a plain wall calendar with an empty grid and no writing; Clover sleeps curled up in a round cat bed on the clean hardwood floor nearby, soft morning light",
              CAST["11-21"][1] + " holds a coffee mug and looks at a blank wall calendar in a kitchen while a gray tabby cat sleeps in a round bed nearby.",
              "Weekly, every two weeks or monthly? It depends on how many people live in the home, whether there are pets and how you use the space.\nTell us about your home and we will suggest a rhythm.\n\n" + TAGS_SAT,
              "Weekly, every two weeks or monthly? It depends on how many people live in the home, whether there are pets and how you use the space.\n\nTell us about your home and we will suggest a rhythm: " + UTM_FB + "nov2026_frequency\n\n" + TAGS_FB),
    "11-28": ("Guests coming in December?",
              "The person smooths the fresh white sheet of a guest bed and places folded towels at its foot, a small plant on the nightstand; Clover sits on the floor beside a small closed suitcase, looking toward the door as if welcoming a guest, soft daylight",
              CAST["11-28"][1] + " makes a guest bed with fresh white sheets while a gray tabby cat with a green collar sits beside a small suitcase.",
              "Guests coming in December? Tell us the dates and we will plan the clean before they arrive.\nMessage us for a free estimate.\n\n" + TAGS_SAT,
              "Guests coming in December? Tell us the dates and we will plan the clean before they arrive.\n\nRequest a free estimate: " + UTM_FB + "nov2026_guests\n\n" + TAGS_FB),
    "11-18": ("Guests in 20 minutes?",
              "The person places a fresh folded hand towel on a shelf in a tidy apartment entry, a minimalist wall clock with no numerals on the wall behind her and shoes lined up on a rack; Clover sits upright on the entry bench facing the front door, as if waiting for guests, warm light",
              CAST["11-18"][1] + " places a folded towel in a tidy apartment entry while a gray tabby cat with a green collar waits on a bench facing the door.",
              IGC["11-18"], FBC["11-18"]),
    "11-29": ("Sunday reset after the long weekend",
              "The person vacuums a clean rug in a quiet Sunday-morning living room, tidy shelves in the background; Clover sits on the sofa watching the vacuum cleaner with curiosity, soft daylight",
              CAST["11-29"][1] + " vacuums a rug in a living room while a gray tabby cat with a green collar watches from the sofa.",
              IGC["11-29"], None),
    "12-05": ("Starting January with a clean home?",
              "The person stands at a window in a tidy, uncluttered living room with a leaf-green mug of coffee, looking out at softly blurred snowy rooftops in soft winter morning light; Clover sits on the wide windowsill beside a green plant",
              CAST["12-05"][1] + " holds a mug at a window while a gray tabby cat with a green collar sits on the sill beside a plant, looking at snowy rooftops.",
              "Starting January with a clean home? Send us your preferred dates and we will plan it with you.\nMessage us for a free estimate.\n\n" + TAGS_SAT,
              "Starting January with a clean home? Send us your preferred dates and we will plan it with you.\n\nRequest a free estimate: " + UTM_FB + "dec2026_january\n\n" + TAGS_FB),
}


# key -> (continuity block, [(subject and action, camera, sound)])
SEED = {}

SEED["11-13"] = (
    "a small, bright New York apartment bathroom with white subway tile, chrome fixtures and a frosted window on the left. "
    "Soft natural daylight at about 5500 K, no harsh shadows. Props: one leaf-green microfiber cloth, a white hand towel and a small green plant on the shelf. "
    "Palette: warm whites, chrome and leaf green. The same hand in every scene: a young adult's hand with medium-brown skin, short natural nails, no jewelry, no watch.",
    [
        ("The hand wipes a chrome bathroom faucet with the leaf-green microfiber cloth in two slow, even strokes; water spots disappear and the metal turns bright.",
         "macro close-up at faucet height, locked-off camera with a very slow push-in of about 5%, shallow depth of field.",
         "soft cloth-on-metal friction and a faint water drip."),
        ("The hand wipes the bathroom mirror from top to bottom with the cloth in one smooth stroke, leaving a clear, streak-free reflection of the bright bathroom.",
         "medium close-up from the side at hand height, slow lateral slide of about 20 cm to the right.",
         "a gentle squeak of cloth on glass."),
        ("The hand wipes a white ceramic sink basin in a slow circular motion; the surface ends clean and glossy, and the hand leaves the cloth folded on the edge of the sink.",
         "high angle over the sink looking down at about 45 degrees, slow pull-back that ends on a wide, tidy view of the sink and mirror.",
         "soft circular wiping, then calm quiet."),
    ],
)

SEED["11-20"] = (
    "a bright New York apartment living room with a large double-hung window, a white sill and softly blurred brick buildings outside. "
    "Soft daylight from the window at about 5500 K, clean and even. Props: a small soft-bristle brush with a pale wooden handle and a damp leaf-green microfiber cloth. "
    "Palette: warm whites, pale wood and leaf green. The same hand in every scene: an older adult's hand with pale skin, visible knuckles and a few freckles, short natural nails, no jewelry, no watch.",
    [
        ("A window track holds a light layer of dust and grit; raking sunlight makes the texture visible and a few dust specks float in the light. Nothing else moves.",
         "macro close-up at track height, slow slide along the track from left to right, shallow depth of field.",
         "very quiet room tone."),
        ("The hand brushes the window track with the soft-bristle brush in short strokes, loosening the dust and grit toward the front of the track.",
         "close-up from the front at track height, locked off.",
         "soft brush bristles on a hard surface."),
        ("The hand wipes the track with the damp leaf-green cloth in one slow stroke; the track ends clean and bright.",
         "close-up that ends with a slow rack focus from the clean track to the bright window and the softly blurred buildings outside.",
         "a soft, damp wipe, then calm quiet."),
    ],
)

SEED["11-27"] = (
    "a bright New York guest room with white walls, a wooden nightstand with a small lamp, and a window with sheer curtains. "
    "Soft morning daylight at about 5500 K. Props: white linens, a stack of folded white towels, a small green plant on the nightstand and a damp leaf-green microfiber cloth. "
    "Palette: warm whites, natural wood and leaf green. The same hands in every scene: adult hands with deep brown skin, short natural nails, no jewelry, no watch.",
    [
        ("Two hands pull the used sheets off a bed in one smooth motion and gather them into a bundle.",
         "medium shot from the foot of the bed at a slightly high angle, locked off.",
         "a soft rustle of fabric."),
        ("A hand wipes the wooden nightstand around the small lamp with the damp cloth in a slow arc.",
         "close-up from the side, slow push-in of about 5%.",
         "a soft wipe on wood."),
        ("Two hands smooth a fresh white sheet over the bed, then place folded white towels at its foot; the room ends tidy and calm.",
         "wide shot from the doorway, slow pull-back that ends on the made bed with the folded towels.",
         "the crisp rustle of clean sheets, then quiet."),
    ],
)

SEED["12-04"] = (
    "a bright New York apartment entryway that opens onto a living room, with white walls, a brushed-steel door handle and a wooden coffee table. "
    "Soft daylight at about 5500 K. Props: a damp leaf-green microfiber cloth and a TV remote control with no readable button labels. "
    "Palette: warm whites, brushed steel, natural wood and leaf green. The same hand in every scene: an adult hand with olive skin, short natural nails, no jewelry, no watch.",
    [
        ("The hand wipes a brushed-steel apartment door handle with the leaf-green cloth, top to bottom, leaving the steel gleaming.",
         "close-up at the handle, locked off with a very slow push-in of about 5%.",
         "a soft wipe on metal."),
        ("The hand wipes a white wall light switch plate with the cloth in one short stroke.",
         "close-up at the switch, slow lateral slide of about 15 cm to the right.",
         "a short, soft wipe."),
        ("The hand wipes a TV remote control on the coffee table, then sets it down square to the table edge.",
         "top-down shot of the coffee table, slow pull-up (the camera rises) that reveals the tidy living room.",
         "a soft wipe, then the small click of the remote on wood."),
    ],
)


SEED["12-06"] = (
    "a small, bright New York apartment entryway in winter with a dark slate floor, white walls, a wooden bench and a window with soft overcast daylight. "
    "Soft daylight at about 6000 K, clean and even. Props: a damp leaf-green microfiber cloth, a black rubber boot tray, a pair of dark winter boots with a little melted snow, and a black rubber doormat. "
    "Palette: warm whites, slate gray, black rubber and leaf green. The same hands in every scene: a young adult's hands with light-beige skin and warm undertones, short natural nails, no jewelry, no watch.",
    [
        ("A hand wipes white road-salt marks off the dark slate floor with the damp leaf-green cloth in one slow stroke; the floor ends clean and dark.",
         "close-up at floor level, locked off with a very slow push-in of about 5%.",
         "a soft, damp wipe on stone."),
        ("A hand sets a pair of wet winter boots square on the black rubber boot tray beside the door; a few drops of melted snow fall onto the tray.",
         "medium close-up from the side at low height, locked off.",
         "a soft rubber thud and a few water drops."),
        ("Two hands lift the rubber doormat, give it one firm shake and lay it back square at the door; the entryway ends tidy.",
         "wide shot from inside the entryway, slow pull-back that ends on the tidy entry with the mat at the door.",
         "a soft shake of rubber, then calm quiet."),
    ],
)


# Voiceover: one short line per 4-second scene (about 2.5 words per second). Audio tags in square brackets are for Eleven v4:
# free-form words placed right before the words they color; a tag holds until the next one. The tags are directions, not spoken text.
VO = {
    "11-13": ["[curious] Be honest... [chuckles] when did you last wipe your faucet?",
              "[excited] Now the mirror. One swipe, and boom, clear.",
              "[warmly] Then the sink. Three wipes, bathroom reset. Save this!"],
    "11-20": ["[curious] Take a look at your window tracks. [chuckles] Yep... THAT.",
              "[warmly] Don't scrub yet. Soft brush first, it loosens the grit.",
              "[excited] Then one damp wipe. Done! [warmly] Save this before winter."],
    "11-27": ["[sighs] Guests just left, and... wow. [warmly] Strip the bed first.",
              "Wipe down the nightstand, lamp and all.",
              "[excited] Fresh sheets, and it's guest-ready! [warmly] Send this to a host."],
    "12-06": ["[curious] White marks by the door? [short pause] That's road salt. Wipe it up.",
              "[warmly] Wet boots go straight on a tray.",
              "[excited] Shake out the mat, and done! [warmly] Send this to a walk-up friend."],
    "12-04": ["[curious] What's the first thing guests touch? [short pause] Your door handle.",
              "[warmly] Then the light switch. Everyone taps it.",
              "[excited] And the remote! Wipe all three, then save this."],
}


def untag(t):
    return re.sub(r"\s+", " ", re.sub(r"\[[^\]]+\]", "", t)).strip()


def vo_boxes(key):
    tagged = VO[key]
    clean = [untag(t) for t in tagged]
    timed = "\n".join(f"{i * SD_SECS - SD_SECS}-{i * SD_SECS} s  Scene {i}: {t}" for i, t in enumerate(clean, 1))
    plain = " ".join(clean)
    words = len(plain.split())
    eleven = "\n".join(tagged)
    notes = meta_box([
        f"About {words} words for {len(tagged) * SD_SECS} seconds: relaxed pace, with a short pause between scenes. If it feels rushed, drop the first sentence of the scene.",
        "The first line is the hook: say it like a question to a friend, within the first two seconds. Smile on the last line, the call to action.",
        "Tone: talk, don't read. Like telling a friend something you just noticed, in casual American English, with contractions and a little humor.",
    ])
    eleven_notes = meta_box([
        "Model: **Eleven v4**. The tags in square brackets are directions, not spoken text. Paste the whole block as it is.",
        "A tag holds until the next one, so tags change only where the delivery changes. One emotion per phrase works best.",
        "Generate the three lines as one take so the tone stays continuous, then cut it to the scenes in the video editor.",
        "If a line does not land, change the tag instead of rewriting the words: [warmly], [excited], [curious], [softly], [chuckles], [short pause]. Capitals mark emphasis, and \"...\" a longer beat.",
        "Voice matters as much as the text: pick a warm, natural American voice before iterating. Keep the phone number and web address out of the voiceover.",
        *([f"This Reel uses **{CH.name(REEL_CHAR[key])}'s voice**: create it once with the voice description in the Characters section of the Overview and reuse it for every voiceover and lip sync of {CH.name(REEL_CHAR[key])}."] if key in REEL_CHAR else []),
    ])
    return (
        notes
        + B.copybox("Voiceover by scene, with timing", timed)
        + eleven_notes
        + B.copybox("Script with audio tags for Eleven v4 (paste into ElevenLabs)", eleven)
        + B.copybox("Plain script, without tags, to record yourself", plain)
    )


def reel_piece(key, day, hour):
    title, clips, ig, fb = REEL[key]
    anchor, scenes = SEED[key]
    n = len(scenes)
    ch = REEL_CHAR.get(key)
    cons = SD_CONSTRAINTS_CHAR if ch else None
    if ch:
        CH.use(ch, REEL_DATE[key], "Reel", title)
    boxes = "".join(
        B.copybox(f"Scene {i} of {n}: {ov}", seedance_scene(title, i, n, anchor, a, c, snd, cons))
        for i, ((a, c, snd), (ov, _sc)) in enumerate(zip(scenes, clips), 1)
    )
    overlay = "\n".join(f"Scene {i}: {ov}" for i, (ov, _sc) in enumerate(clips, 1))
    draft = meta_box([
        f"Saved in Metricool as an Instagram **Reel** draft for {hour}, with the caption, hashtags and Brooklyn location. It carries the logo as a placeholder image, because Metricool does not accept a Reel without a file.",
        "To finish it: open the draft, remove the logo image and upload the video. The type is already Reel; the \"Images are not supported\" warning disappears once the video replaces the logo.",
        *(["The Facebook draft is text only, with the Brooklyn location. Add the same video there and, if you want it as a Reel, change its type to Reel."] if fb else ["This Reel is Instagram only: there is no Facebook draft for this day."]),
        "The Instagram draft is already marked as AI-generated content.",
    ])
    needs = meta_box([
        f"Vertical 9:16, 1080 x 1920 px. {n} scenes of {SD_SECS} seconds each, about {n * SD_SECS} seconds in total.",
        "Add the on-screen text, the voiceover (script below) and licensed music in the video editor: generators garble text inside video.",
        *([f"**{CH.name(ch)}** is the person in this Reel (the face shows in some scenes, only the hands in the close-ups). Attach {CH.name(ch)}'s reference portrait to every scene prompt. {CH.ai_video_note([ch], True)}"] if ch else []),
        "Cover: use a frame from scene 1 and add the title in Canva, in Cormorant Garamond bold on the off-white #F7F6F1.",
        "The settings and the way the prompts are built are explained in the Overview, under \"Video prompts for Seedance\".",
    ])
    body = (
        det("Metricool draft: what is left to do", draft, True)
        + det("What the video needs", needs, False)
        + det("Continuity block: paste it at the start of every scene", B.copybox("Continuity block", anchor[0].upper() + anchor[1:]), False)
        + det(f"Seedance prompts: {n} scenes, one prompt per scene", boxes, False)
        + det("All scenes in one prompt (optional)", B.copybox("Single prompt with three labeled shots", seedance_combo(title, anchor, scenes, cons, f"{CH.name(ch)} is the through-line" if ch else "the same hand is the through-line")), False)
        + det("On-screen text by scene", B.copybox("On-screen text (add in the video editor)", overlay), False)
        + det("Voiceover script (audio)", vo_boxes(key), False)
        + det("Instagram text", B.copybox("Instagram text", ig), True)
        + (det("Facebook text", B.copybox("Facebook text", fb), False)
           + det("Facebook title (Metricool, Facebook presets)",
                 meta_box(["In the Metricool editor, open **Facebook presets** and paste this in **Title**. It is optional and only applies to video posts and Reels.",
                           "It is a short headline for the video, separate from the caption text above."])
                 + B.copybox("Facebook title", title), False) if fb else "")
    )
    return piece(day, hour, "Reel: " + title, "Instagram and Facebook" if fb else "Instagram", "Reel, about 12 seconds", S_VID, body)


def thanks_piece(day, hour):
    draft = meta_box([
        "Two text-only drafts in Metricool, both for 11 AM: LinkedIn (no link) and Facebook (with the Brooklyn location).",
        "This piece is new: it replaces the empty Thursday of the long weekend. Review the wording before scheduling.",
        "An image is optional. If you add one, use the prompt below (4:5, 1080 x 1350 px, no text on the image). It shows only Clover, the cat: a thank-you to clients should not use a fictional person as if she were part of the team.",
    ])
    img = B.copybox(
        "Optional image prompt (complete, paste into the generator)",
        single_photo_prompt("a warm, tidy New York apartment dining room with a table set for a family dinner, plates and glasses, a small green plant as the centerpiece, soft late-afternoon window light; "
                            "Clover sits on the rug a short distance from the table, looking up at it", person=False),
    )
    body = (
        det("Metricool drafts: status", draft, True)
        + det("LinkedIn text", B.copybox("LinkedIn text", LI["2026-11-26"]), True)
        + det("Facebook text", B.copybox("Facebook text", FB_THANKS), False)
        + det("Optional image: prompt", img, False)
    )
    return piece(day, hour, "Thanksgiving thank-you", "LinkedIn and Facebook", "Text with optional image", S_DRAFT, body)


def single_piece(key, day, hour):
    head, scene, alt, ig, fb = SING[key]
    ch = CAST_CHAR.get(key)
    if ch:
        CH.use(ch, SING_DATE[key], "Single image", head)
        who = [
            f"**{CH.name(ch)}** is the person in this image, with Clover, the cat. The prompt already includes both descriptions. Attach the {CH.name(ch)} portrait from the Characters section of the Overview and the Clover reference image (section \"Maya, Daniel and Clover in single images\") to the prompt, so both look the same each time.",
            CH.tag_ai_note([ch]),
        ]
    else:
        who = [f"{CHAR_NAME} (a gray tabby cat) is the only recurring character. The person is different in every image, on purpose. In this one: {CAST[key][1]}. The prompt already includes both descriptions. Attach the Clover reference image from the Overview (section \"Maya, Daniel and Clover in single images\") to every prompt so the cat looks the same each time."]
    needs = meta_box([
        "4:5 format, 1080 x 1350 px, one image with no text on it: the caption carries the message.",
        *who,
        "Leave the bottom-left corner empty: the logo is added afterward.",
    ])
    alt_box = meta_box(["Paste this in the image's alt text field when you add the image in Metricool. It describes the photo, since the image has no text."]) + B.copybox("Alt text", alt)
    body = (
        det("What the image needs", needs, False)
        + det("Image: prompt", B.copybox("Image prompt (complete, paste into the generator)", single_photo_prompt(scene, CAST[key][0], ch)), False)
        + det("Alt text", alt_box, False)
        + det("Instagram text", B.copybox("Instagram text", ig), True)
        + (det("Facebook text", B.copybox("Facebook text", fb), False) if fb else "")
        + (page_img_det("contact") if fb and "https://" in fb else "")
    )
    return piece(day, hour, "Single image: " + head, "Instagram and Facebook" if fb else "Instagram", "Single image", S_IMG, body)


def sched_piece(key):
    """Weeks 1 and 2: the post is already scheduled in Metricool with its finished media. Only the text changes."""
    d = SCHED[key]
    day, hour = key
    notes = meta_box([
        "**Already scheduled in Metricool** with its finished media. Nothing has been changed there.",
        d["media"],
        "To apply it after your approval: edit the text of the scheduled post in Metricool. Do not delete and recreate it, so its time and media stay.",
    ])
    parts = [det("Status and media", notes, True)]
    parts.append(det("Proposed text (replaces the scheduled one)", "".join(B.copybox(lab, txt) for lab, txt in d["new"]), True))
    parts.append(det("Scheduled today (unchanged until you approve)", "".join(B.copybox(lab, txt) for lab, txt in d["old"]), False))
    for summary, bullets, boxes in d["extra"]:
        parts.append(det(summary, meta_box(bullets) + "".join(B.copybox(lab, txt) for lab, txt in boxes), False))
    return piece(day, hour, d["title"], d["nets"], d["formato"], S_SCHED, "".join(parts))


import kn_timeback  # noqa: E402  (time-back strategy: applies new texts and per-piece metadata)

kn_timeback.apply(globals())

W = {}

W[1] = "".join(sched_piece(k) for k in [
    ("Mon, Nov 9", "10 AM"), ("Tue, Nov 10", "11 AM"), ("Wed, Nov 11", "12 PM"), ("Thu, Nov 12", "11 AM"),
    ("Fri, Nov 13", "12 PM"), ("Sat, Nov 14", "11 AM"), ("Sun, Nov 15", "6 PM"),
])

W[2] = "".join(sched_piece(k) for k in [
    ("Mon, Nov 16", "10 AM"), ("Tue, Nov 17", "11 AM"), ("Wed, Nov 18", "12 PM"), ("Thu, Nov 19", "11 AM"),
    ("Fri, Nov 20", "12 PM"), ("Sat, Nov 21", "11 AM"), ("Sun, Nov 22", "6 PM"),
])

W[3] = (
    gbp_piece("2026-11-23", "Office cleaning before the holidays")
    + li_car_piece("2026-11-24", "Tue, Nov 24", "11 AM", "Year-end office checklist")
    + ig_piece("11-25", "Wed, Nov 25", "12 PM", "After dinner: the kitchen in 30 minutes", "Instagram and Facebook", "7-slide carousel",
               [SLIDES_FMT.format(n=7), "The minutes on slides 2 to 6 add up to 30. The post goes out on Wednesday, before Thanksgiving."])
    + thanks_piece("Thu, Nov 26", "11 AM")
    + reel_piece("11-27", "Fri, Nov 27", "12 PM")
    + single_piece("11-28", "Sat, Nov 28", "11 AM")
    + single_piece("11-29", "Sun, Nov 29", "6 PM")
)

W[4] = (
    gbp_piece("2026-11-30", "Recurring home cleaning")
    + li_piece("2026-12-01", "Tue, Dec 1", "11 AM", "Year-end calendar for property managers")
    + ig_piece("12-02", "Wed, Dec 2", "12 PM", "Before and after of a real job", "Instagram and Facebook", "6-slide carousel",
               ["4:5 format, 1080 x 1350 px, 6 slides with real photos.", "Fill in the bracketed details with the real job."],
               status=S_PHOTOS)
    + li_car_piece("2026-12-03", "Thu, Dec 3", "11 AM", "What property management cleaning includes")
    + reel_piece("12-04", "Fri, Dec 4", "12 PM")
    + single_piece("12-05", "Sat, Dec 5", "11 AM")
    + reel_piece("12-06", "Sun, Dec 6", "6 PM")
)

# ---------------------------------------------------------------------------
# OVERVIEW
# ---------------------------------------------------------------------------
BOARD = [
    ("Mon, Nov 9", "10 AM", "Google", "What Klean N Green NYC does"),
    ("Tue, Nov 10", "11 AM", "LinkedIn", "Turnover week: 5 checks"),
    ("Wed, Nov 11", "12 PM", "Instagram and Facebook", "Carousel: Kitchen, 6 spots people miss"),
    ("Thu, Nov 12", "11 AM", "LinkedIn", "What office cleaning includes"),
    ("Fri, Nov 13", "12 PM", "Instagram and Facebook", "Reel: 3 quick bathroom wipes"),
    ("Sat, Nov 14", "11 AM", "Instagram and Facebook", "Single image: First clean, 4 details"),
    ("Sun, Nov 15", "6 PM", "Instagram", "Carousel: Sunday reset"),
    ("Mon, Nov 16", "10 AM", "Google", "Cleans between tenants or guests"),
    ("Tue, Nov 17", "11 AM", "LinkedIn", "How a unit is verified"),
    ("Wed, Nov 18", "12 PM", "Instagram and Facebook", "Single image: Guests in 20 minutes"),
    ("Thu, Nov 19", "11 AM", "LinkedIn", "Customer review"),
    ("Fri, Nov 20", "12 PM", "Instagram and Facebook", "Reel: Window tracks"),
    ("Sat, Nov 21", "11 AM", "Instagram and Facebook", "Single image: How often to clean"),
    ("Sun, Nov 22", "6 PM", "Instagram", "Carousel: Entryway in 5 points"),
    ("Mon, Nov 23", "10 AM", "Google", "Office cleaning before the holidays"),
    ("Tue, Nov 24", "11 AM", "LinkedIn", "Carousel: Year-end office checklist"),
    ("Wed, Nov 25", "12 PM", "Instagram and Facebook", "Carousel: Kitchen in 30 minutes after dinner"),
    ("Thu, Nov 26", "11 AM", "LinkedIn and Facebook", "Thanksgiving thank-you"),
    ("Fri, Nov 27", "12 PM", "Instagram and Facebook", "Reel: Guests leave, your afternoon stays yours"),
    ("Sat, Nov 28", "11 AM", "Instagram and Facebook", "Single image: Guests in December"),
    ("Sun, Nov 29", "6 PM", "Instagram", "Single image: The Sunday after the long weekend"),
    ("Mon, Nov 30", "10 AM", "Google", "Recurring home cleaning"),
    ("Tue, Dec 1", "11 AM", "LinkedIn", "Year-end calendar"),
    ("Wed, Dec 2", "12 PM", "Instagram and Facebook", "Carousel: Before and after of a real job"),
    ("Thu, Dec 3", "11 AM", "LinkedIn", "Carousel: What property management cleaning includes"),
    ("Fri, Dec 4", "12 PM", "Instagram and Facebook", "Reel: High-touch spots"),
    ("Sat, Dec 5", "11 AM", "Instagram and Facebook", "Single image: January weekends"),
    ("Sun, Dec 6", "6 PM", "Instagram", "Reel: Winter entryway, already handled"),
]


def board_status(day, hour):
    m = PIECE_META[(day, hour)]
    return chipx(m["type"], m["tk"]) + " " + chipx(S_SCHED if m["mode"] == "sched" else S_NEW, "hip")


board = (
    '<div class="tablewrap"><table class="rev"><thead><tr><th>Date</th><th>Network</th><th>Piece</th><th>Status</th></tr></thead><tbody>'
    + "".join(
        f"<tr><th scope='row'>{e(d)} · {e(h)}</th><td>{e(n)}</td><td>{e(t)}</td><td>{board_status(d, h)}</td></tr>"
        for d, h, n, t in BOARD
    )
    + "</tbody></table></div>"
)

formats = (
    '<div class="tablewrap"><table class="rev"><thead><tr><th>Piece</th><th>Size</th><th>Notes</th></tr></thead><tbody>'
    "<tr><th scope='row'>Instagram and Facebook carousel</th><td>1080 x 1350 px (4:5)</td><td>Between 6 and 8 slides, PNG or JPG. The same images work on Facebook. Nov 11, Nov 15, Nov 22, Nov 25 and Dec 2.</td></tr>"
    "<tr><th scope='row'>Reel</th><td>1080 x 1920 px (9:16)</td><td>About 12 seconds, made of 3 Seedance scenes of about 4 seconds. Fridays: same video on Instagram and Facebook. Sunday, Dec 6: Instagram only.</td></tr><tr><th scope='row'>Single image</th><td>1080 x 1350 px (4:5)</td><td>Saturdays, plus Wednesday, Nov 18 (Instagram and Facebook) and Sunday, Nov 29 (Instagram only). No text on the image.</td></tr><tr><th scope='row'>Page featured image</th><td>1200 x 630 px (1.91:1)</td><td>Only for website pages. No text. It is the preview card when a page link is shared; it is not a size for LinkedIn posts.</td></tr>"
    "<tr><th scope='row'>LinkedIn</th><td>1080 x 1350 px (4:5)</td><td>Every LinkedIn image, including the review card and the carousel slides: the same size as Instagram, so the Canva design can be reused. For single posts the image is optional and the texts work on their own; if you attach an image, LinkedIn shows it instead of the link preview card. The two carousels (Nov 24, 8 slides, and Dec 3, 6 slides) are published as one PDF document.</td></tr>"
    "<tr><th scope='row'>Google Business Profile</th><td>1200 x 900 px (4:3)</td><td>A real photo is better; the generated image is the alternative. Added in the Metricool draft.</td></tr>"
    "</tbody></table></div>"
)

confirm = [
    "**Time-back wording.** The copy says the service gives the reader time and asks what they would do with it. It promises no hours saved and never says what clients did with their time. Confirm you are comfortable with that line.",
    "**Weeks 1 and 2.** Replacing the text of a scheduled post does not touch its image or video. Check that each new text still agrees with its media (the Nov 15 slides, for example, still say 20 minutes).",
    "**Dec 2 before and after.** The text says \"The client's time spent on it: none.\" Keep that line only if the client did nothing for that job, and fill in the bracketed details first.",
    "**Services named in the new copy.** Recurring plans (weekly, every two weeks, monthly), turnover and vacation-rental cleans, a clean planned before guests arrive, and holiday scheduling for offices and property managers. Confirm each is offered as written.",
    "**Vacant-unit service for property managers.** The LinkedIn texts talk about cleaning units between tenants. The website mentions vacation rentals and corporate housing, but not in those words.",
    "**Handover photos.** The texts for Nov 10, Nov 17 and Dec 3 say photos of the key areas are taken at handover. If that is not the case, remove those lines.",
    "**Service areas.** The Google post for Monday, Nov 9 mentions Manhattan, Brooklyn and Queens. The website also cites Jersey City and Hoboken.",
    "**Saturday posts.** They invite people to send their dates and details for an estimate. Confirm that the team can reply to messages on weekends and in the first days of January.",
    "**/new-clients/ offer.** Not used. If it is still valid, add it with an end date.",
    "**Customer review (Nov 19).** It is a public Google review, quoted word for word and without the client's name. Confirm you are comfortable using it; if you prefer, ask the client first.",
    "**Real photos (Dec 2).** That draft's text still contains bracketed placeholders: fill them with the real job before scheduling, and get the customer's authorization for the photos.",
    "**Thanksgiving post (Nov 26).** New content, not in the original plan. Review the wording and decide whether it goes out.",
    "**Reel drafts.** Instagram holds the logo as a placeholder because Metricool does not accept a Reel without a file. Remove the logo and upload the video before scheduling.",
    "**Brooklyn location.** The Meta place \"Brooklyn, New York\" shows that name in the draft, but its stored map coordinates point to Colorado. If that matters, swap it for a Brooklyn business or neighborhood page.",
    "**Typography roles.** The website lists Jost and Cormorant Garamond without saying which is which. The prompts use Cormorant Garamond for headlines and Jost for body text and labels; tell me if it is the other way round and I will swap them.",
    "**Google buttons in Metricool.** Nov 9 and Nov 16 are scheduled with their images; Nov 23 and Nov 30 are text-only drafts. Metricool has no button field for Google, so the link sits in the text; the button (Book or Learn more) is only set if you publish directly in Google.",
    "**Phone number.** No post text includes it, because Google can reject posts with a phone number in the text. The website footer shows (347) 833-4766 and the closing-slide design shows (347) 883-4766: confirm which one is correct before publishing.",
    "**People in the images.** Maya and Daniel are the two recurring AI characters of the brand; Clover (a gray tabby cat) is the recurring animal. They appear in the draft pieces from Nov 12 on: TikToks, LinkedIn videos, the Reels of Nov 27, Dec 4 and Dec 6, the single images of Nov 28, Nov 29 and Dec 5, and as hands in three carousels. The finished images and videos of weeks 1 and 2, and the Nov 10 TikTok, keep the one-off people they already have. The captions never mention the characters or speak in their name. If you prefer real team members, tell me and the prompts are updated.",
    "**LinkedIn carousels.** Nov 24 and Dec 3 are text drafts that already have the PDF carousel option on. They need their images before they can go out; if the images are not ready in time, remove the \"Swipe through.\" sentence and publish them as text. Nov 17 is not a carousel: it is already scheduled with its image.",
    "**LinkedIn links.** Each post that links to the website now points to the page that matches its topic (checklist, testimonials, commercial, Brooklyn); only Nov 10 still links to Contact. Every link keeps its UTM tag and is shortened by Metricool.",
]

n_new_slides = sum(len(v[1]) for k, v in list(CAR.items()) + list(LICAR.items()) if k in ("11-25", "2026-11-24", "2026-12-03"))
STRAT = B.section(
    "Strategy: time back",
    B.callout("Hiring Klean N Green NYC gives you time for what you could not fit in before. Every piece either shows what that time can become, or gives a useful tip and ends with a bridge to the service.", "The idea.")
    + B.tiles([
        ("25", "pieces show what you can do with the time: a Saturday, a host's evening, a property manager's week", "dato"),
        ("13", "pieces stay as tips and close with a bridge to the service", "dato"),
        ("15", "pieces are already scheduled with finished images or videos (weeks 1 and 2, plus the Nov 10 TikTok): only their text changes", "dato"),
        ("23", "pieces are drafts: new text, and new scenes, scripts and prompts where the idea changed", "dato"),
    ])
    + '<div class="tablewrap"><table class="rev"><thead><tr><th>Audience</th><th>What the time is for</th><th>Where it shows up</th></tr></thead><tbody>'
    "<tr><th scope='row'>Families and homes</th><td>Weekends, a slow breakfast, a walk, the call you keep postponing</td><td>Saturday and Sunday posts, Reels, Google</td></tr>"
    "<tr><th scope='row'>Hosts</th><td>The door, the drinks and the guests, not the sponge</td><td>Nov 18, Nov 27, Nov 28, TikTok</td></tr>"
    "<tr><th scope='row'>Rental hosts and landlords</th><td>Guest messages, showings and the listing</td><td>Google, Nov 16</td></tr>"
    "<tr><th scope='row'>Property managers</th><td>Tenants, showings and inspections, instead of coordinating crews</td><td>LinkedIn: Nov 10, Nov 17, Dec 1, Dec 3</td></tr>"
    "<tr><th scope='row'>Office managers and teams</th><td>People, vendors, projects and the year-end close</td><td>LinkedIn: Nov 12 and Nov 24; Google, Nov 23</td></tr>"
    "</tbody></table></div>"
    + '<ul class="checks">' + "".join(
        f"<li>{fmt(x)}</li>"
        for x in [
            "**Lead with the moment, then the service.** Open with what the person gets: a Saturday, a quiet evening, an open calendar. The service is how they get there.",
            "**Ask, do not claim.** \"What would you do with your Saturday?\" invites the reader. The copy never says what clients did with their time: no invented clients, stories or testimonials. The only client voice is the Nov 19 Google review, word for word.",
            "**No hours-saved numbers.** The numbers that remain (5 checks, 20 minutes, 30 minutes) are steps inside tips, not promises.",
            "**Tips stay, with a bridge.** One piece in three is a tip. It ends with one bridge line from the bank below.",
            "**One call to action per piece:** a free estimate, a message or a scope.",
            "**Scenes show the free time, not the work.** Maya, Daniel and Clover appear after the work is done: reading, a mug at the window, waiting for guests.",
            "**Weeks 1 and 2 keep their media.** Those posts are scheduled with finished images and videos, so the proposal changes only the text. Tip carousels and Reels carry the bridge in the caption, and three carousels have an optional extra closing slide.",
        ]
    ) + "</ul>"
    + B.copybox("Bridge lines for tips (pick one per piece)", "\n".join(kn_timeback.BRIDGES)),
    "The mix: about two pieces in three show the time, and one in three teaches and bridges.",
)
rs = STRAT
rs += B.section(
    "What is ready and what is missing",
    B.tiles(
        [
            ("15", "pieces already scheduled in Metricool with finished media: 14 posts in weeks 1 and 2 plus the Nov 10 TikTok. Only the text changes", "dato"),
            ("23", "drafts hold the previous text. They get the new text, and the media is still to be made", "dato"),
            ("%d" % n_new_slides, "slide prompts rewritten or kept for the three carousels of weeks 3 and 4 (Nov 24, Nov 25, Dec 3), plus 3 optional extra closing slides for the scheduled carousels", "dato"),
            ("3", "Reels still to produce, all in weeks 3 and 4 (Nov 27, Dec 4, Dec 6); the Nov 13 and Nov 20 Reels are done", "dato"),
            ("9", "scripts rewritten for AI-presenter videos: 7 TikToks (Nov 12 to Dec 3) and 2 LinkedIn videos; the Nov 10 TikTok keeps its finished video and changes only its caption", "dato"),
        ]
    )
    + B.callout(
        "Nothing in Metricool has changed. After you approve a piece I update it there: scheduled posts are edited in place, so their time and media stay, and drafts are replaced with the new text. A piece you do not approve stays as it is.",
        "Next step.",
    ),
    "Klean N Green NYC, Monday, November 9 to Sunday, December 6, 2026. All times are New York time.",
)
rs += B.section("Four-week board", board)

# ---------------------------------------------------------------------------
# Overview sections: brand look and Seedance video prompts
# ---------------------------------------------------------------------------
def swatches():
    cells = "".join(
        f"<div class='sw'><i style='background:{hx};{'border-bottom:1px solid #DCEBD5;' if hx in ('#FFFFFF', '#F7F6F1') else ''}'></i>"
        f"<b>{e(nm)}</b><code>{hx}</code><span>{e(note)}</span></div>"
        for nm, hx, note in PALETTE
    )
    return f"<div class='swatches'>{cells}</div>"


SPECIMEN = (
    "<div class='specimen'>"
    "<div class='bar'></div>"
    "<h4>Green cleaning for New York homes</h4>"
    "<p>Recurring, one-time and move-out cleans, with a clear scope and a free estimate.</p>"
    "<small>Headline: Cormorant Garamond bold, #1E2A23. Body: Jost, #55645B.</small>"
    "</div>"
)

SCHEMA = (
    "<div class='schem'><svg viewBox='0 0 270 340' role='img' aria-label='Layout of a 1080 by 1350 post: photo behind, off-white text panel inside a safe margin, empty logo square at the bottom left' xmlns='http://www.w3.org/2000/svg'>"
    "<rect x='1' y='1' width='268' height='338' rx='4' fill='#E6E3D8' stroke='#54595F'/>"
    "<line x1='90' y1='1' x2='90' y2='339' stroke='#54595F' stroke-dasharray='3 4' opacity='.45'/>"
    "<line x1='180' y1='1' x2='180' y2='339' stroke='#54595F' stroke-dasharray='3 4' opacity='.45'/>"
    "<line x1='1' y1='113' x2='269' y2='113' stroke='#54595F' stroke-dasharray='3 4' opacity='.45'/>"
    "<line x1='1' y1='226' x2='269' y2='226' stroke='#54595F' stroke-dasharray='3 4' opacity='.45'/>"
    "<rect x='22' y='22' width='226' height='296' fill='none' stroke='#2E7D32' stroke-dasharray='5 4'/>"
    "<circle cx='200' cy='64' r='20' fill='#C9C4B2'/>"
    "<text x='200' y='99' font-family='Jost,sans-serif' font-size='9' text-anchor='middle' fill='#1E2A23'>subject on a third</text>"
    "<rect x='22' y='118' width='226' height='142' rx='9' fill='#F7F6F1' stroke='#DCEBD5'/>"
    "<rect x='36' y='132' width='30' height='2.5' fill='#4CB748'/>"
    "<rect x='36' y='144' width='150' height='11' rx='2' fill='#1E2A23'/>"
    "<rect x='36' y='160' width='112' height='11' rx='2' fill='#1E2A23'/>"
    "<rect x='36' y='184' width='170' height='5' rx='2' fill='#55645B'/>"
    "<rect x='36' y='195' width='150' height='5' rx='2' fill='#55645B'/>"
    "<rect x='36' y='206' width='120' height='5' rx='2' fill='#55645B'/>"
    "<rect x='22' y='276' width='42' height='42' fill='none' stroke='#2E7D32' stroke-dasharray='3 3'/>"
    "<text x='43' y='301' font-family='Jost,sans-serif' font-size='9' text-anchor='middle' fill='#1E2A23'>logo</text>"
    "<text x='74' y='294' font-family='Jost,sans-serif' font-size='9' fill='#1E2A23'>photo stays visible around panel</text>"
    "</svg></div>"
)

PRINCIPLES = [
    "**Hierarchy.** The headline is at least 1.8 times larger than the body text: cover 96 px or more, content slides about 64 px and 36 px. One idea per slide.",
    "**Contrast.** Ink #1E2A23 on the off-white panel reads at 13.8:1, paragraph text #55645B at 5.8:1 and white on forest green at 5.1:1. Bright green #4CB748 is decoration only (2.6:1 on white) and never carries text.",
    "**Alignment and grid.** Everything is left-aligned to one edge, inside a 90 px safe margin, and the panel sits in the same place on every slide so the set reads as one piece.",
    "**White space and proximity.** Generous padding inside the panel; the accent line, headline and body are grouped tightly, with more space between that group and the photo.",
    "**Repetition and consistency.** Same panel, same two fonts, same colors, same light and color grading across the set. The closing slide switches to a forest-green panel with white text as the end signal.",
    "**Focal point and rule of thirds.** The subject of the photo sits on one third of the frame and at least half of the image stays visible as photo around the panel.",
    "**Color proportion (60-30-10).** About 60% warm off-white and white, 30% photo tones and ink, 10% green.",
]

rs += B.section(
    "Brand look: palette, typography and layout",
    B.callout("These values come from the website's global settings. Every image prompt in this pack already carries them, so you do not need to add anything when you paste a prompt.", "Source.")
    + swatches()
    + SPECIMEN
    + "<p class='note'>The website lists Jost and Cormorant Garamond without saying which is which. The prompts use Cormorant Garamond for headlines and Jost for body text and labels. If that is reversed, tell me and the prompts are updated.</p>"
    + SCHEMA
    + '<ul class="checks">' + "".join(f"<li>{fmt(x)}</li>" for x in PRINCIPLES) + "</ul>"
    + B.copybox("Brand block that every image prompt includes", BRAND + "\n\n" + TYPE + "\n\n" + DESIGN),
)

DUO_IDEAS = [
    ("Sat, Nov 14", "First clean: 4 details (already scheduled, optional)", "11-14", "He takes notes on a sofa while Clover looks at the phone."),
    ("Wed, Nov 18", "Guests in 20 minutes", "11-18", "She sets a fresh towel in the entry; Clover waits at the door under a clock."),
    ("Sat, Nov 21", "How often to clean", "11-21", "He studies a blank calendar over coffee; Clover sleeps nearby."),
    ("Thu, Nov 26", "Thanksgiving thank-you (optional image)", None, "Clover only, on the rug near the set table."),
    ("Sat, Nov 28", "Guests in December", "11-28", "Maya sits on the made guest bed with a mug; Clover waits beside a suitcase."),
    ("Sun, Nov 29", "The Sunday after the long weekend", "11-29", "Daniel reads on the sofa; Clover curls up at the other end."),
    ("Sat, Dec 5", "January clean", "12-05", "Maya stands at the window with a coffee; Clover sits on the sill, looking at the winter light."),
]
duo_table = (
    '<div class="tablewrap"><table class="rev"><thead><tr><th>Date</th><th>Post</th><th>Person</th><th>What happens in the photo</th></tr></thead><tbody>'
    + "".join(
        f"<tr><th scope='row'>{e(a)}</th><td>{e(b)}</td><td>{e((CH.name(CAST_CHAR[k]) + ': ' if k in CAST_CHAR else '') + CAST[k][1] if k else 'None (Clover only)')}</td><td>{e(c)}</td></tr>"
        for a, b, k, c in DUO_IDEAS
    )
    + "</tbody></table></div>"
)
REF_PROMPT = (
    "Photorealistic character reference image, vertical 4:5 format, 1080 x 1350 px, on a plain warm light-gray seamless studio background with soft, even daylight. "
    "One character, full body, sitting upright in a three-quarter view with space around it, no props: Clover, the cat. "
    + CHAR_CAT + " No text, no logos, no people and no other animals."
)
rs += B.section(
    "Maya, Daniel and Clover in single images",
    B.callout("Single images carry no text: the caption says the message and the image is a photo. Clover, a gray tabby cat with a leaf-green collar, is the recurring animal. From Nov 28 the person in each image is one of the two recurring characters, Maya or Daniel, so the feed is recognizable; their reference portraits and descriptions are in the Characters section above. The finished images of weeks 1 and 2 are already scheduled with one-off people and stay as they are. Generators also tend to garble text inside images, so removing it avoids the most common failure.", "The idea.")
    + duo_table
    + B.copybox("Step 1: Clover reference image (generate it first and attach it to every single-image prompt)", REF_PROMPT)
    + B.copybox("Character block for Clover (already included in every single-image prompt)", CHAR_CAT)
    + '<ul class="checks">'
    + "".join(
        f"<li>{fmt(x)}</li>"
        for x in [
            "**Two people, one cat.** Each prompt carries the fixed description of Maya or Daniel and the block for Clover. Attach both reference images to the prompt: the person's portrait and the cat.",
            "**Hands match the character.** In the three carousels of the draft weeks, the hands are Maya's or Daniel's; elsewhere the hands stay varied. The same hands stay through a whole set.",
            "**Check each result.** Compare the person with the portrait (face, hair, age, clothes) and the cat with the reference (markings and collar). Check that the hands have five fingers.",
            "**The characters are fictional and AI-generated.** Do not present them as real employees, customers or testimonials, and do not write captions as if they were on the team. The Instagram drafts are already marked as AI-generated.",
            "**No claims.** Captions and images do not say anything about pets or pet-safe products unless the business confirms it first.",
            "**Clover stays out of the way of the work.** Never on food, dishes, a sink or fresh linens; that is written into its block.",
            "**Real people instead?** Use a photo of that person as the reference image, with their written permission, and replace the person block in that prompt. Real photos of the team and of jobs are always better than generated ones for Google and for the Dec 2 before and after.",
        ]
    )
    + "</ul>",
    "Applies to the single images: the Saturday posts and the Sunday post of the draft weeks, each with Maya or Daniel and Clover, and the optional Thanksgiving image, with Clover only. Carousels and Reels keep their layout; LinkedIn images with no people stay as they are.",
)
rs += B.section(
    "Video prompts for Seedance",
    B.callout("Each Reel is split into three scenes of 4 seconds. Generate them one by one in Seedance, then join and edit them in your video editor. The prompts do not ask for text, voice or music inside the video.", "How it works.")
    + '<ul class="checks">' + "".join(f"<li>{fmt(x)}</li>" for x in SD_SETTINGS) + "</ul>"
    + B.copybox(
        "Scene template (how every scene prompt is built)",
        seedance_scene("[Reel title]", 1, 3, "[continuity block: place, light, props, the same hand]", "[one action, one sentence]", "[one camera move: shot size, angle, movement]", "[ambient sound]"),
    )
    + "<p class='note'>Order inside each prompt: continuity, subject and action, camera, style, sound, constraints. One action and one camera move per scene keeps the motion clean. Each Reel card also has the three scenes as one labeled prompt (Shot 1, Shot 2, Shot 3) in case you prefer to generate the whole piece at once.</p>",
)
rs += B.section(
    "How to generate the images",
    '<ul class="checks">'
    + "".join(
        f"<li>{fmt(x)}</li>"
        for x in [
            "**One prompt generates one image.** Each carousel has one prompt per slide, and each already carries the brand block (palette, typography and layout rules) and the exact text. Copy and paste one at a time.",
            "**Single images: one prompt, one finished image, no text on it.** Each prompt includes the description of that image's person (Maya or Daniel from Nov 28) and of Clover, the recurring cat; attach the person's portrait and the Clover reference image to every prompt so both stay the same (see \"Maya, Daniel and Clover in single images\").",
            "**No slide numbers on the images.** The prompts name the role of the slide (cover, content, closing) and tell the generator not to print counters, arrows or dots. The \"Slide 3 of 7\" labels in this pack are only for finding the prompt.",
            "**All slides of a carousel in the same chat**, so light, panel and color grading stay identical from one slide to the next.",
            "**Check the spelling of the text in every image.** If it comes out wrong, ask for another version, or keep only the photo: copy the sentence that follows \"Photo scene:\" in the prompt, generate the photo without text and set the text in Canva with Cormorant Garamond for the headline and Jost for the body, using the brand block in the Overview.",
            "**The logo is added afterward.** Every prompt leaves a 160 x 160 px square empty at the bottom left, because generators do not reproduce a logo well.",
            "**Reels: one scene per prompt, for Seedance.** Generate each 4-second scene separately with the continuity block, join them in a video editor and add on-screen text and music there. The Reels of Nov 27, Dec 4 and Dec 6 show Maya or Daniel: attach the portrait to every scene. The \"Video prompts for Seedance\" section explains the settings.",
            "**Linked pages.** Pieces with a link include the prompt for that page's featured image. Generate each page image once, upload it to the page and check the link preview before the piece goes out.",
            "**The prompts ask for photorealistic images.** They are generic illustrative photos, not Klean's real work: do not present them as real jobs. Flag them as AI-generated so that option is set on Instagram when the drafts are created.",
        ]
    )
    + "</ul>",
)
rs += B.section(
    "Featured images of linked pages",
    B.callout("Every piece that carries a link has, inside its card, the prompt for the featured image of the page it points to, except the two LinkedIn carousels (Nov 24 and Dec 3), which show a document instead of a link preview. That image is also the preview card of the link, which LinkedIn shows only when the post has no image of its own. It is a website image: the posts themselves are 4:5, 1080 x 1350 px. Generate each page image once and reuse it.")
    + '<div class="tablewrap"><table class="rev"><thead><tr><th>Page</th><th>Pieces that link to it</th><th>Needed before</th><th>File name</th></tr></thead><tbody>'
    "<tr><th scope='row'>Contact (/contact-us/)</th><td>Google: Nov 9, Nov 23 and Nov 30. LinkedIn: Nov 10. Facebook: Nov 14, 21, 28 and Dec 5.</td><td>Mon, Nov 9</td><td>klean-nyc-contact.jpg</td></tr>"
    "<tr><th scope='row'>Vacation rentals (/vacation-rentals-cleaning/)</th><td>Google: Nov 16.</td><td>Mon, Nov 16</td><td>klean-nyc-vacation-rental-cleaning.jpg</td></tr>"
    "<tr><th scope='row'>Post-construction checklist (/post-construction-cleaning-checklist/)</th><td>LinkedIn: Nov 17 (already scheduled with its own image).</td><td>Optional</td><td>klean-nyc-post-construction-cleaning-checklist.jpg</td></tr>"
    "<tr><th scope='row'>Testimonials (/testimonials/)</th><td>LinkedIn: Nov 19.</td><td>Thu, Nov 19</td><td>klean-nyc-testimonials.jpg</td></tr>"
    "<tr><th scope='row'>Commercial cleaning (/commercial)</th><td>LinkedIn: Nov 24 (carousel: LinkedIn shows the document, not the link preview).</td><td>Optional</td><td>klean-nyc-commercial-cleaning.jpg</td></tr>"
    "<tr><th scope='row'>Cleaning service in Brooklyn (/professional-cleaning-service-in-brooklyn/)</th><td>LinkedIn: Dec 3 (carousel: LinkedIn shows the document, not the link preview).</td><td>Optional</td><td>klean-nyc-cleaning-service-brooklyn.jpg</td></tr>"
    "</tbody></table></div>"
    "<p class='note'>If a LinkedIn post later links to a blog article instead of the contact page, that article needs its own featured image. Ask for its prompt when the article is defined.</p>",
)
OTHER_PAGES = [
    ("Home", "kleannyc.com", "home",
     "a wide view of a bright, spotless New York apartment living room with large windows, a sofa with a folded throw, a plant and softly blurred brownstone buildings outside",
     "Bright, clean apartment living room with large windows in New York"),
    ("Residential cleaning (homes and apartments)", "/residential", "residential-cleaning",
     "a clean modern apartment kitchen with white cabinets, freshly wiped light counters, a bowl of lemons and a folded leaf-green microfiber cloth, morning light",
     "Clean apartment kitchen with wiped counters and a green microfiber cloth"),
    ("Post-construction cleaning (service page)", "Services menu, Post-construction", "post-construction-cleaning",
     "an empty, freshly renovated apartment kitchen with new white cabinets, clean stone counters, large windows and an unlabeled microfiber mop and bucket in a corner, no visible dust",
     "Newly renovated apartment kitchen, clean and empty"),
    ("Blog (index page)", "/blog/", "blog",
     "a top-down flat lay on a light wooden table of folded leaf-green microfiber cloths, a small soft brush, an unlabeled glass spray bottle, a small plant and a closed notebook, with calm empty space on the right",
     "Cleaning essentials on a wooden table: microfiber cloths, a soft brush and a spray bottle"),
]
other_cards = "".join(
    det(
        f"{name}",
        meta_box([
            f"Page: **{name}** ({where}).",
            f"File name: **klean-nyc-{fname}.jpg**. Alt text: **{alt}**.",
            "Horizontal 1.91:1, 1200 x 630 px, no text.",
        ]) + B.copybox("Featured image prompt (complete, paste into the generator)", web_prompt(scene)),
        False,
    )
    for name, where, fname, scene, alt in OTHER_PAGES
)
rs += B.section(
    "Featured images for other site pages",
    B.callout("No post in these four weeks links to these pages, so they are not tied to a date. Every page that a post does link to is in the section above. They carry the same palette as the rest of the pack. Use only the pages that exist on the site; if the real page list differs, the prompts are adjusted.", "Optional.")
    + other_cards,
)
rs += B.section("Sizes by format", formats)
rs += B.section("Before approving: facts to confirm", '<ul class="checks">' + "".join(f"<li>{fmt(x)}</li>" for x in confirm) + "</ul>")
rs += B.section(
    "Hashtags",
    B.tagbox("LinkedIn, property management", TAGS_LI_PM)
    + B.tagbox("LinkedIn, offices", TAGS_LI_OF)
    + B.tagbox("Instagram, base", TAGS_IG)
    + B.tagbox("Instagram, Reels", TAGS_REEL)
    + B.tagbox("Instagram, Saturday single images", TAGS_SAT)
    + B.tagbox("Facebook", TAGS_FB)
    + "<p class='note'>On Wednesdays, Instagram swaps the last hashtag for a topical one (#KitchenCleaning, #HostingTips, #KitchenReset). The Sunday, Dec 6 Reel uses #WinterHome in place of #SatisfyingClean. Check new hashtags in Instagram search before using them. The strategy sets three hashtags on LinkedIn and five on Instagram.</p>",
)

# ---------------------------------------------------------------------------
# ASSEMBLY
# ---------------------------------------------------------------------------
PANELS = [
    ("resumen", "b-all", "Overview"),
    ("sem1", "b-klean", "Week 1"),
    ("sem2", "b-klean", "Week 2"),
    ("sem3", "b-klean", "Week 3"),
    ("sem4", "b-klean", "Week 4"),
]
tabs = "".join(
    f'<button type="button" role="tab" id="tab-{i}" class="tab {c}" aria-controls="panel-{i}" '
    f'aria-selected="{"true" if k == 0 else "false"}" data-tab="{i}"><i class="dot"></i>{e(n)}</button>'
    for k, (i, c, n) in enumerate(PANELS)
)
WEEK_TXT = {
    1: ("Week 1", "November 9 to 15. Already scheduled with finished media: only the text changes."),
    2: ("Week 2", "November 16 to 22. Already scheduled with finished media: only the text changes."),
    3: ("Week 3", "November 23 to 29. Drafts with new text and prompts. Thursday the 26th is Thanksgiving: a short thank-you post goes out on LinkedIn and Facebook."),
    4: ("Week 4", "November 30 to December 6. Drafts with new text and prompts."),
}
panels = B.panel("resumen", "b-all", "Overview", "Image prompts, texts and hashtags for Klean N Green NYC over four weeks.", rs)
for n in (1, 2, 3, 4):
    panels += B.panel(f"sem{n}", "b-klean", WEEK_TXT[n][0], WEEK_TXT[n][1], f'<div class="pieces">{W[n]}</div>', True)

JS = B.JS.replace(
    "['resumen','kg-market','klean-nyc','jdet-capital','klean-peru']",
    "['resumen','sem1','sem2','sem3','sem4']",
).replace("'Copiado'", "'Copied'").replace("'Seleccione y copie'", "'Select and copy'")
assert "sem1" in JS and "Copied" in JS

EXTRA_CSS = """
.pieces{display:grid;gap:16px;margin-top:14px}
.piece{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:10px 10px 12px}
.piece>.slot{border:0;padding:6px 6px 8px;background:none}
.dt{margin-top:6px;border-top:1px solid var(--line);padding-top:8px}
.dt>summary{cursor:pointer;font-weight:600;font-size:14.5px;padding:6px 4px;color:var(--brand);list-style-position:inside}
.dt .copybox{margin-top:8px}
.checks.mini{margin:8px 0 0;padding-left:20px;font-size:14.5px;gap:6px}
.rev{min-width:560px}
.rev tbody th{white-space:nowrap}
.rev td{font-size:14px}
.slot{grid-template-columns:104px 1fr}
.swatches{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin:14px 0}
.sw{border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--surface);display:flex;flex-direction:column}
.sw i{display:block;height:52px}
.sw b{font-size:14px;padding:8px 10px 0}
.sw code{font-size:13px;padding:2px 10px 0;color:var(--ink)}
.sw span{font-size:12.5px;line-height:1.4;padding:4px 10px 10px;color:var(--muted)}
.specimen{background:#F7F6F1;border:1px solid var(--line);border-radius:14px;padding:20px;margin:14px 0}
.specimen .bar{width:60px;height:4px;background:#4CB748;margin-bottom:12px}
.specimen h4{font-family:'Cormorant Garamond',Georgia,serif;font-weight:700;font-size:32px;line-height:1.1;color:#1E2A23;margin:0 0 8px}
.specimen p{font-family:Jost,system-ui,sans-serif;font-size:16px;line-height:1.5;color:#55645B;margin:0 0 10px}
.specimen small{font-family:Jost,system-ui,sans-serif;font-size:12.5px;color:#54595F}
.schem svg{display:block;width:100%;max-width:260px;margin:14px auto}
.when b{font-size:13px;letter-spacing:.03em}
.angle{margin:2px 8px 8px;font-size:14px;color:var(--muted)}
.angle b{color:var(--ink)}
"""

TOP = """<header class="top">
<p class="eyebrow">Klean N Green NYC · November 9 to December 6, 2026 · time-back strategy</p>
<h1>Posts for weeks 1 to 4</h1>
<p class="lead">A post every day for 28 days, rewritten around one message: hiring Klean N Green NYC gives you time for what you could not fit in before. Weeks 1 and 2 are already scheduled in Metricool with finished media, so only their text changes; weeks 3 and 4 are drafts and change completely. Nothing in Metricool has been touched yet. Dates and times are New York time.</p>
</header>"""

FOOT = """<footer>
<div class="fnt">
<p><b>How to use it.</b> Each card has copy-ready text with a Copy button. All times are New York time.</p>
<p><b>Limits.</b> The texts are based on the strategy and on what the website shows. The palette and fonts come from the website settings. Items that depend on the business are listed under "Before approving". Cleaning tips are general and do not name products.</p>
</div>
</footer>"""

DOC = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Klean N Green NYC: posts for weeks 1 to 4</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{B.FONTS}" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">
<style>{B.CSS}{EXTRA_CSS}</style>
</head>
<body>
{TOP}
<nav class="tabs" id="tabs"><div class="tablist" role="tablist" aria-label="Weeks">{tabs}</div></nav>
<main>
{panels}
</main>
{FOOT}
<script>{JS}</script>
</body>
</html>
"""

# Etiquetas fijas de build_estrategia (español) -> inglés
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
    drafts = [{"date": k, "text": t} for k, t in LI.items()]
    json.dump(drafts, open("li_drafts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
