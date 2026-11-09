#!/usr/bin/env python3
# Klean N Green NYC: estrategia "tiempo recuperado" (nov 2026).
# Mensaje central: contratar a Klean N Green NYC da tiempo para hacer lo que antes no se podia.
# Mezcla: unas 2 de cada 3 piezas muestran lo que el cliente puede hacer con el tiempo ganado;
# el resto sigue siendo consejo, con un cierre que lleva al servicio.
#
# Semanas 1 y 2: ya estan programadas en Metricool con sus imagenes y videos terminados. Solo se propone cambiar el texto.
# Semanas 3 y 4: son borradores sin medios. Se reescribe todo (texto, escenas, guiones, prompts).
#
# Este modulo no importa nada de los builders: recibe los globals (g) de build_publicaciones y los modulos de TikTok / LinkedIn.
import copy

TB = "Time back"
TIP = "Tip + bridge"
S_SCHED = "Scheduled · text change proposed"
S_NEW = "Draft · new text proposed"
S_NEWSCRIPT = "Draft · new script proposed"

# (day, hour) -> (tipo, angulo)
META = {
    # Week 1
    ("Mon, Nov 9", "10 AM"): (TB, "The Saturday you get back."),
    ("Tue, Nov 10", "11 AM"): (TB, "Property managers: turnover week without the chase."),
    ("Wed, Nov 11", "12 PM"): (TIP, "Tip first. The bridge to the service is in the caption."),
    ("Thu, Nov 12", "11 AM"): (TB, "Office managers: the team's time goes to the work."),
    ("Fri, Nov 13", "12 PM"): (TIP, "Tip first. The bridge to the service is in the caption."),
    ("Sat, Nov 14", "11 AM"): (TB, "Four details from you, and the rest of the Saturday is yours."),
    ("Sun, Nov 15", "6 PM"): (TB, "The caption leads with the time: the Sunday you get back."),
    # Week 2
    ("Mon, Nov 16", "10 AM"): (TB, "Hosts and landlords: guest messages and showings, not mops."),
    ("Tue, Nov 17", "11 AM"): (TB, "Property managers get the photos and the sign-off without walking the unit."),
    ("Wed, Nov 18", "12 PM"): (TB, "Hosting: the door and the drinks, not the sponge."),
    ("Thu, Nov 19", "11 AM"): (TB, "The real review stays word for word; only the framing line carries the time angle."),
    ("Fri, Nov 20", "12 PM"): (TIP, "Tip first. The bridge to the service is in the caption."),
    ("Sat, Nov 21", "11 AM"): (TB, "Start from the weekend you want, then pick the rhythm."),
    ("Sun, Nov 22", "6 PM"): (TB, "Coming home to an entryway that is already done."),
    # Week 3
    ("Mon, Nov 23", "10 AM"): (TB, "Office managers: close the year with the team, not with a cleaning list."),
    ("Tue, Nov 24", "11 AM"): (TIP, "Checklist first. The bridge is the last slide and the last paragraph."),
    ("Wed, Nov 25", "12 PM"): (TIP, "Tip first. The bridge is the last slide and the last line."),
    ("Thu, Nov 26", "11 AM"): (TB, "Thanksgiving: a day at the table with nothing else on the list."),
    ("Fri, Nov 27", "12 PM"): (TB, "Guests leave, the reset is handled and the afternoon is yours."),
    ("Sat, Nov 28", "11 AM"): (TB, "Spend the visit, not the prep."),
    ("Sun, Nov 29", "6 PM"): (TB, "The Sunday after the long weekend is yours."),
    # Week 4
    ("Mon, Nov 30", "10 AM"): (TB, "A steady rhythm gives weekends you can plan."),
    ("Tue, Dec 1", "11 AM"): (TB, "Property managers: December with cleaning off the plate."),
    ("Wed, Dec 2", "12 PM"): (TB, "Our time on site, and the client's time left alone."),
    ("Thu, Dec 3", "11 AM"): (TB, "Property managers: time for tenants, not for coordinating crews."),
    ("Fri, Dec 4", "12 PM"): (TIP, "Tip first. The bridge is the last scene and the caption."),
    ("Sat, Dec 5", "11 AM"): (TB, "The January weekends you wanted."),
    ("Sun, Dec 6", "6 PM"): (TB, "A winter evening that is already yours."),
}
SCHEDULED_DAYS = {  # semanas 1 y 2: ya programadas con medios
    "Nov 9", "Nov 10", "Nov 11", "Nov 12", "Nov 13", "Nov 14", "Nov 15",
    "Nov 16", "Nov 17", "Nov 18", "Nov 19", "Nov 20", "Nov 21", "Nov 22",
}


def is_scheduled(day):
    return day.split(", ")[1] in SCHEDULED_DAYS


# Frases puente para los consejos (banco para reutilizar)
BRIDGES = [
    "Prefer to spend that time elsewhere? We handle it. Message us for a free estimate.",
    "Save the list, or hand it to us and keep the time.",
    "Or let us take it off your list.",
    "Want the whole day back? Message us for a free estimate.",
]


def apply(g):
    """Aplica la estrategia a los datos de build_publicaciones (g = globals())."""
    link, link_to = g["link"], g["link_to"]
    UTM_FB = g["UTM_FB"]
    T = g
    old = {k: copy.deepcopy(g[k]) for k in ("LI", "GBP", "IGC", "FBC", "REEL", "SING", "LI_REVIEW", "FB_THANKS")}
    g["OLD"] = old

    # ------------------------------------------------------------------ chips y metadatos por pieza
    g["S_SCHED"], g["S_NEW"] = S_SCHED, S_NEW
    g["KIND"][S_SCHED] = "hip"
    g["KIND"][S_NEW] = "hip"
    for k, (typ, angle) in META.items():
        g["PIECE_META"][k] = dict(type=typ, tk=("dato" if typ == TB else "ref"), angle=angle,
                                  mode=("sched" if is_scheduled(k[0]) else "draft"))

    TAGS_IG, TAGS_IG_WED, TAGS_IG_WED2, TAGS_IG_WED3 = g["TAGS_IG"], g["TAGS_IG_WED"], g["TAGS_IG_WED2"], g["TAGS_IG_WED3"]
    TAGS_FB, TAGS_SAT, TAGS_REEL = g["TAGS_FB"], g["TAGS_SAT"], g["TAGS_REEL"]
    TAGS_LI_PM, TAGS_LI_OF, TAGS_LI_REV, TAGS_IG_BA = g["TAGS_LI_PM"], g["TAGS_LI_OF"], g["TAGS_LI_REV"], g["TAGS_IG_BA"]

    # ================================================================== SEMANAS 1 Y 2: SOLO TEXTO (ya programadas)
    NEW = {}  # (day, hour) -> lista de (rotulo, texto nuevo)
    OLDT = {}  # (day, hour) -> lista de (rotulo, texto programado hoy)

    # --- Mon Nov 9, Google
    GBP_NEW = {
        "2026-11-09": (
            "What would you do with your Saturday if the cleaning was already done? "
            "Klean N Green NYC cleans homes, offices, rentals and post-construction sites in Manhattan, Brooklyn and Queens, so your time goes where you want it.\n\n"
            "Book now to request a free estimate: https://kleannyc.com/contact-us/?utm_source=google&utm_medium=gbp&utm_campaign=nov2026_overview&utm_content=book_now"
        ),
        "2026-11-16": (
            "Turnover cleans for rentals and vacation properties. Between tenants or guests, we get the unit ready for the next arrival, "
            "so your time goes to guest messages, showings and everything else on your list.\n\n"
            "Learn more about how it works: https://kleannyc.com/vacation-rentals-cleaning/?utm_source=google&utm_medium=gbp&utm_campaign=nov2026_turnover&utm_content=learn_more\n\n"
            "Then send us your dates and the number of units."
        ),
    }
    NEW[("Mon, Nov 9", "10 AM")] = [("Google Business Profile text", GBP_NEW["2026-11-09"])]
    OLDT[("Mon, Nov 9", "10 AM")] = [("Google Business Profile text", old["GBP"]["2026-11-09"])]
    NEW[("Mon, Nov 16", "10 AM")] = [("Google Business Profile text", GBP_NEW["2026-11-16"])]
    OLDT[("Mon, Nov 16", "10 AM")] = [("Google Business Profile text", old["GBP"]["2026-11-16"])]

    # --- LinkedIn Nov 10, 12, 17, 19
    g["LI"]["2026-11-10"] = (
        "Turnover week should not take over your week.\n\n"
        "Between tenants, a unit needs five checks:\n"
        "1. Kitchen: inside the oven, fridge and cabinets.\n"
        "2. Bathrooms: grout, fixtures and exhaust fans.\n"
        "3. Windows: glass, tracks and sills.\n"
        "4. Floors: edges and corners, not only the center.\n"
        "5. Final walkthrough with photos.\n\n"
        "Done by you, that is a list to run and re-run. Done by us, it is a handover with photos, and your hours go to tenants, showings and the next unit.\n\n"
        "Property managers in NYC: tell us how many units you turn over each month and we will scope it. "
        "Request a free estimate: " + link("linkedin", "social", "nov2026_turnover") + "\n\n" + TAGS_LI_PM
    )
    g["LI"]["2026-11-12"] = (
        "What does office cleaning actually include? And what does it free up?\n\n"
        "The scope changes with the space, but a regular office clean usually covers:\n"
        "• Desks and shared surfaces, including high-touch points like handles and switches\n"
        "• Kitchenette and break room\n"
        "• Restrooms, cleaned and restocked\n"
        "• Trash and recycling\n"
        "• Floors, vacuumed and mopped\n"
        "• Entrance, glass and common areas\n\n"
        "That is a list nobody on your team should have to think about. When it is handled, office managers spend their time on people, vendors and projects, and everyone else on their actual work.\n\n"
        "The right frequency depends on headcount and how the space is used. A 3-person studio and a 40-person floor need different plans.\n\n"
        "Message us the size of your space and how often you would like service, and we will send a scope.\n\n" + TAGS_LI_OF
    )
    g["LI"]["2026-11-17"] = (
        "A unit is not done until it is verified. Here is how we do it, in 3 steps:\n\n"
        "1. A room-by-room checklist, so nothing depends on memory.\n"
        "2. Photos of the key areas: kitchen, bathrooms, floors and windows.\n"
        "3. A final walkthrough before we call it done.\n\n"
        "For property managers, that is the point: you receive the photos and the sign-off, and you do not have to walk the unit yourself. "
        "That time goes to your next showing, your next tenant, your next call.\n\n"
        "See the full cleaning checklist: " + link_to("/post-construction-cleaning-checklist/", "linkedin", "social", "nov2026_verificacion") + "\n\n" + TAGS_LI_PM
    )
    g["LI_REVIEW"] = old["LI_REVIEW"].replace(
        "What stood out for this client: a next-day visit, on a Sunday.\n\n",
        "What stood out for this client: a next-day visit, on a Sunday. Fast help means the rest of your day stays yours.\n\n",
    )
    assert g["LI_REVIEW"] != old["LI_REVIEW"]
    for day, key in (("Tue, Nov 10", "2026-11-10"), ("Thu, Nov 12", "2026-11-12"), ("Tue, Nov 17", "2026-11-17")):
        hour = "11 AM"
        NEW[(day, hour)] = [("LinkedIn text", g["LI"][key])]
        OLDT[(day, hour)] = [("LinkedIn text", old["LI"][key])]
    NEW[("Thu, Nov 19", "11 AM")] = [("LinkedIn text", g["LI_REVIEW"])]
    OLDT[("Thu, Nov 19", "11 AM")] = [("LinkedIn text", old["LI_REVIEW"])]

    # --- Instagram / Facebook: Nov 11 (carrusel, tip), Nov 13 (reel, tip), Nov 15 (carrusel, tiempo)
    NEW[("Wed, Nov 11", "12 PM")] = [
        ("Instagram text",
         "Six kitchen spots that get skipped, even in a weekly clean. \U0001F9FD\n"
         "Swipe through and count how many you did this week.\n"
         "Save it for your cleaning day, or hand the list to us and spend that time on something else.\n\n" + TAGS_IG_WED),
        ("Facebook text",
         "Six kitchen spots that get skipped, even when the counters look clean: the microwave ceiling, the range hood filter, "
         "cabinet handles, the space behind small appliances, the faucet base and the fridge door seal.\n\n"
         "Which one do you skip most often? And if you would rather spend that time elsewhere, message us for a free estimate.\n\n" + TAGS_FB),
    ]
    OLDT[("Wed, Nov 11", "12 PM")] = [("Instagram text", old["IGC"]["11-11"]), ("Facebook text", old["FBC"]["11-11"])]

    NEW[("Fri, Nov 13", "12 PM")] = [
        ("Instagram text",
         "Three quick bathroom wipes: faucet, mirror, sink.\n"
         "A cloth and a minute each.\n"
         "Save this, or hand the bathroom to us and spend those minutes elsewhere.\n\n" + TAGS_REEL),
        ("Facebook text",
         "Three quick bathroom wipes: faucet, mirror and sink. A cloth and a minute each.\n\n"
         "Which one do you skip most often? And if you would rather spend that minute elsewhere, message us for a free estimate.\n\n" + TAGS_FB),
    ]
    OLDT[("Fri, Nov 13", "12 PM")] = [("Instagram text", old["REEL"]["11-13"][2]), ("Facebook text", old["REEL"]["11-13"][3])]

    NEW[("Sun, Nov 15", "6 PM")] = [
        ("Instagram text",
         "Twenty minutes, six spots: that is a Sunday reset.\n"
         "Now picture the other version: the reset already done, and the whole Sunday yours.\n"
         "Save the list, or message us for a free estimate and take the Sunday.\n\n" + TAGS_IG),
    ]
    OLDT[("Sun, Nov 15", "6 PM")] = [("Instagram text", old["IGC"]["11-15"])]

    # --- Singles: Nov 14, 18, 21
    NEW[("Sat, Nov 14", "11 AM")] = [
        ("Instagram text",
         "Booking a first clean? Send us four details: rooms and bathrooms, pets at home, how we get in, and what matters most to you.\n"
         "That is all it takes on your side. The rest of your Saturday is yours.\n"
         "Message us for a free estimate.\n\n" + TAGS_SAT),
        ("Facebook text",
         "Booking a first clean? Send us four details: rooms and bathrooms, pets at home, how we get in, and what matters most to you.\n\n"
         "That is all it takes on your side. The rest of your Saturday is yours.\n\n"
         "Request a free estimate: " + UTM_FB + "nov2026_first_clean\n\n" + TAGS_FB),
    ]
    OLDT[("Sat, Nov 14", "11 AM")] = [("Instagram text", old["SING"]["11-14"][3]), ("Facebook text", old["SING"]["11-14"][4])]

    NEW[("Wed, Nov 18", "12 PM")] = [
        ("Instagram text",
         "Guests are on their way, and the home is already ready.\n"
         "That is the best way to host: time to set the table, pour a drink and open the door with nothing left to do.\n"
         "Message us for a free estimate.\n\n" + TAGS_IG_WED2),
        ("Facebook text",
         "Guests are on their way, and the home is already ready. That is the best way to host: time to set the table, pour a drink and open the door with nothing left to do.\n\n"
         "What would you do with that time? Message us for a free estimate.\n\n" + TAGS_FB),
    ]
    OLDT[("Wed, Nov 18", "12 PM")] = [("Instagram text", old["IGC"]["11-18"]), ("Facebook text", old["FBC"]["11-18"])]

    NEW[("Sat, Nov 21", "11 AM")] = [
        ("Instagram text",
         "Weekly, every two weeks or monthly? Start from the other end: what do you want your weekends to look like?\n"
         "Tell us about your home and we will suggest a rhythm that gets you there.\n\n" + TAGS_SAT),
        ("Facebook text",
         "Weekly, every two weeks or monthly? It depends on how many people live in the home, whether there are pets and how you use the space. "
         "But start from the other end: what do you want your weekends to look like?\n\n"
         "Tell us about your home and we will suggest a rhythm: " + UTM_FB + "nov2026_frequency\n\n" + TAGS_FB),
    ]
    OLDT[("Sat, Nov 21", "11 AM")] = [("Instagram text", old["SING"]["11-21"][3]), ("Facebook text", old["SING"]["11-21"][4])]

    # --- Reel Nov 20 y carrusel Nov 22
    NEW[("Fri, Nov 20", "12 PM")] = [
        ("Instagram text",
         "Window tracks collect dust and grit, and they are easy to forget.\n"
         "Loosen it with a soft brush, then wipe with a damp cloth. Or let us do the tracks and keep that time.\n"
         "Save this for before winter.\n\n" + TAGS_REEL),
        ("Facebook text",
         "Window tracks collect dust and grit, and they are easy to forget. Loosen it with a soft brush, then wipe with a damp cloth.\n\n"
         "When did you last clean yours? And if you would rather spend that time elsewhere, message us for a free estimate.\n\n" + TAGS_FB),
    ]
    OLDT[("Fri, Nov 20", "12 PM")] = [("Instagram text", old["REEL"]["11-20"][2]), ("Facebook text", old["REEL"]["11-20"][3])]

    NEW[("Sun, Nov 22", "6 PM")] = [
        ("Instagram text",
         "Coming home should feel like the day is over.\n"
         "Five entryway points make it happen: a few minutes a week, or none at all if we do them.\n"
         "Save the list, or message us for a free estimate.\n\n" + TAGS_IG),
    ]
    OLDT[("Sun, Nov 22", "6 PM")] = [("Instagram text", old["IGC"]["11-22"])]

    g["SCHED"] = {}
    media_keep = "Image unchanged: the post is scheduled with its image, and the new text works with it."
    media_vid = "Video unchanged: the post is scheduled with its finished video. Only the caption changes."
    media_car = "Images unchanged: the carousel is scheduled with all its slides. Only the caption changes."
    base = {
        ("Mon, Nov 9", "10 AM"): ("What Klean N Green NYC does", "Google Business Profile", "Post with image and button", media_keep),
        ("Tue, Nov 10", "11 AM"): ("Turnover week: 5 checks", "LinkedIn", "Text with image", media_keep + " The image headline, \"Turnover week: 5 checks\", still fits."),
        ("Wed, Nov 11", "12 PM"): ("Kitchen: 6 spots people miss", "Instagram and Facebook", "8-slide carousel", media_car),
        ("Thu, Nov 12", "11 AM"): ("What office cleaning includes", "LinkedIn", "Text with image", media_keep),
        ("Fri, Nov 13", "12 PM"): ("Reel: 3 quick bathroom wipes", "Instagram and Facebook", "Reel, about 12 seconds", media_vid),
        ("Sat, Nov 14", "11 AM"): ("Single image: First clean, 4 details", "Instagram and Facebook", "Single image", media_keep),
        ("Sun, Nov 15", "6 PM"): ("Sunday reset: 20 minutes, 6 spots", "Instagram", "8-slide carousel", media_car + " The slides still say 20 minutes and 6 spots; the caption turns that into the time you get back."),
        ("Mon, Nov 16", "10 AM"): ("Cleans between tenants or guests", "Google Business Profile", "Post with image and button", media_keep),
        ("Tue, Nov 17", "11 AM"): ("How a unit is verified before handover", "LinkedIn", "Text with image", media_keep),
        ("Wed, Nov 18", "12 PM"): ("Single image: Guests in 20 minutes", "Instagram and Facebook", "Single image", media_keep + " The photo shows the entry ready and Clover waiting at the door, which fits the new caption."),
        ("Thu, Nov 19", "11 AM"): ("Customer review", "LinkedIn", "Text with image", "Quote card unchanged. The quote and the attribution are not touched: only the framing line after the quote changes."),
        ("Fri, Nov 20", "12 PM"): ("Reel: Window tracks", "Instagram and Facebook", "Reel, about 12 seconds", media_vid),
        ("Sat, Nov 21", "11 AM"): ("Single image: How often to clean", "Instagram and Facebook", "Single image", media_keep + " The photo (a coffee, a blank wall calendar) fits \"what do you want your weekends to look like\"."),
        ("Sun, Nov 22", "6 PM"): ("Entryway: first impression in 5 points", "Instagram", "7-slide carousel", media_car),
    }
    for k, (title, nets, fmt_, media) in base.items():
        g["SCHED"][k] = dict(title=title, nets=nets, formato=fmt_, media=media, new=NEW[k], old=OLDT[k], extra=[])

    # Cierre opcional (slide extra) para los tres carruseles ya programados
    ex = {
        ("Wed, Nov 11", "12 PM"): ("11-11", "Want the kitchen handled?", "Message us for a free estimate. We handle the kitchen, you keep the time."),
        ("Sun, Nov 15", "6 PM"): ("11-15", "Want your Sundays back?", "Message us for a free estimate. We handle the reset."),
        ("Sun, Nov 22", "6 PM"): ("11-22", "Want to come home to this?", "Message us for a free estimate."),
    }
    for k, (ckey, head, body) in ex.items():
        title_c, slides = g["CAR"][ckey]
        n = len(slides) + 1
        scene = slides[-1][2]
        prompt = g["slide_prompt"](title_c, n, n, head, body, scene)
        g["SCHED"][k]["extra"].append((
            f"Optional extra slide {n}: the bridge",
            [f"Instagram allows more slides than the {n - 1} already scheduled. This extra closing slide makes the time-back bridge visible in the image too.",
             "It is optional: the caption already carries the bridge. If you use it, add it after the current closing slide in the Metricool post."],
            [(f"Slide {n} of {n}: closing", prompt)],
        ))

    # ================================================================== SEMANAS 3 Y 4: REESCRITURA COMPLETA
    # --- Google, lunes
    g["GBP"]["2026-11-23"] = (
        "The week before the holidays is short. Hand the pre-break office clean to us, and your team spends its last days closing the year, not clearing desks and fridges.\n\n"
        "Tell us the size of your space and how often you want service: https://kleannyc.com/contact-us/?utm_source=google&utm_medium=gbp&utm_campaign=nov2026_office&utm_content=request_scope"
    )
    g["GBP"]["2026-11-30"] = (
        "Recurring home cleaning: weekly, every two weeks or monthly. Pick a rhythm and the home is ready on its own schedule, "
        "so your weekends go to the things you keep postponing.\n\n"
        "Book now to request a free estimate: https://kleannyc.com/contact-us/?utm_source=google&utm_medium=gbp&utm_campaign=nov2026_recurring&utm_content=book_now"
    )
    g["GBPIMG"]["2026-11-23"] = g["gbp_prompt"]("a tidy open office on a quiet afternoon with four clear desks, closed laptops, a plant and a wall calendar with no readable writing, soft winter light")
    g["GBPIMG"]["2026-11-30"] = g["gbp_prompt"]("a bright living room in morning light with a folded throw, an open book lying face down and a mug on the coffee table, suggesting a free weekend")

    # --- LinkedIn: 11-24 (carrusel, consejo), 12-01 (calendario, tiempo), 12-03 (carrusel, tiempo), 11-26 (gracias)
    g["LI"]["2026-11-24"] = (
        "Before the office closes for the holidays: a 6-point cleaning checklist. Swipe through.\n\n"
        "1. Clear and wipe desks, so nothing sits for two weeks.\n"
        "2. Empty the break room fridge and microwave.\n"
        "3. Restrooms: deep clean and restock.\n"
        "4. Trash and recycling: empty everything and replace liners.\n"
        "5. Floors: vacuum and mop, including corners and under desks.\n"
        "6. Glass, entrance and high-touch points.\n\n"
        "Coming back to a clean office on the first Monday of January sets the tone for the quarter. "
        "If your last week is already full, hand the list to us and let your team spend it closing the year.\n\n"
        "Planning a pre-break deep clean? Request a free estimate: " + link_to("/commercial", "linkedin", "social", "nov2026_cierre_oficina") + "\n\n" + TAGS_LI_OF
    )
    sl = list(g["LICAR"]["2026-11-24"][1])
    sl[-1] = ("Rather spend the last week on the year-end?", "Send us your space and dates. We handle the clean.", sl[-1][2])
    g["LICAR"]["2026-11-24"] = (g["LICAR"]["2026-11-24"][0], sl)

    g["LI"]["2026-11-26"] = (
        "Happy Thanksgiving from all of us at Klean N Green NYC.\n\n"
        "Thank you to the property managers, office teams and families in New York City who trust us with their spaces, and with their time.\n\n"
        "Wishing you a day at the table with the people you love, and nothing else on your list.\n\n"
        "#NYCCleaning #Thanksgiving #PropertyManagement"
    )
    g["FB_THANKS"] = (
        "Happy Thanksgiving from Klean N Green NYC.\n\n"
        "Thank you to the families, offices and property managers who trust us with their spaces, and with their time. "
        "Wishing you a day at the table with the people you love, and nothing else on your list.\n\n"
        "#NYCCleaning #Thanksgiving #CleaningTips"
    )

    g["LI"]["2026-12-01"] = (
        "Property managers: December fills up fast. Here is a year-end cleaning calendar, so cleaning stays off your plate.\n\n"
        "Dec 1-6: schedule cleans for units that will sit vacant over the holidays.\n"
        "Dec 7-13: common areas, including lobby, hallways and entrances.\n"
        "Dec 14-20: confirm access, keys and building rules for the holiday week.\n"
        "Dec 21-27: only what cannot wait, like move-outs.\n"
        "Early January: plan turnovers for the new year.\n\n"
        "Send us the units and dates once and we run the sequence. You keep the holiday week for tenants, owners and your own time off.\n\n"
        "Planning your December? Message us the units and dates and we will help you put them in order.\n\n" + TAGS_LI_PM
    )

    g["LI"]["2026-12-03"] = (
        "What does cleaning for property management include? And what does it give back? Swipe through.\n\n"
        "• Turnover cleans for vacant units between tenants\n"
        "• Vacation rental and corporate housing cleans between guests\n"
        "• Post-renovation cleaning before a unit goes back on the market\n"
        "• Photos of the key areas at handover\n\n"
        "Every building is different. Tell us the type of property and the number of units, and we will put together a plan, "
        "so your time goes to your tenants and not to coordinating crews.\n\n"
        "Request a free estimate: " + link_to("/professional-cleaning-service-in-brooklyn/", "linkedin", "social", "dic2026_administracion") + "\n\n" + TAGS_LI_PM
    )
    sl = list(g["LICAR"]["2026-12-03"][1])
    sl[0] = (sl[0][0], "Four things we take off your list", sl[0][2])
    sl[-1] = ("Your time belongs to your tenants", "Share the property type and number of units for a free estimate.", sl[-1][2])
    g["LICAR"]["2026-12-03"] = (g["LICAR"]["2026-12-03"][0], sl)

    # --- Instagram / Facebook, carruseles 11-25 (consejo) y 12-02 (antes y despues)
    sl = list(g["CAR"]["11-25"][1])
    sl[-1] = ("Want your next big meal to end at the table?", "Message us for a free estimate and plan ahead.", sl[-1][2])
    g["CAR"]["11-25"] = (g["CAR"]["11-25"][0], sl)
    g["IGC"]["11-25"] = (
        "Tomorrow is the big meal. Here is a 30-minute plan for the kitchen afterward. \U0001F9FD\n"
        "Five steps, with the minutes for each.\n"
        "Save this for Thursday night. And for your next big meal, message us for a free estimate and end the evening at the table.\n\n" + TAGS_IG_WED3
    )
    g["FBC"]["11-25"] = (
        "Tomorrow is the big meal. Here is a 30-minute plan for the kitchen afterward: clear and stack (5 min), soak the pots (2), "
        "dishes (10), counters and stovetop (8), floor and trash (5).\n\n"
        "Share it with whoever is doing the dishes. \U0001F609 And for your next big meal, message us for a free estimate and end the evening at the table.\n\n" + TAGS_FB
    )

    g["IGC"]["12-02"] = (
        "A real job, before and after. [Type of space] in [neighborhood], cleaned by our team in [hours].\n"
        "What we did: [short list].\n"
        "The client's time spent on it: none. Message us for a free estimate.\n\n" + TAGS_IG_BA
    )
    g["FBC"]["12-02"] = (
        "Before and after: [type of space] in [neighborhood], cleaned by our team in [hours]. What we did: [short list]. The client's time spent on it: none.\n\n"
        "Want the same for your place? Message us for a free estimate.\n\n" + TAGS_FB
    )
    g["BA_CLOSING"] = (
        g["style"]() + " This is the closing slide of a carousel about a real cleaning job. "
        "Write exactly this text on the image, in English, spelled exactly as given, and add no other text: "
        "headline \"What we did\"; body \"[short list of what was done]. Our time on site: [hours]. Your time: yours.\"; "
        "call to action \"Message us for a free estimate\". "
        "Put the headline and body on the off-white panel and the call to action on a forest-green #2E7D32 band under it, with white Jost medium text, so the set ends with a clear signal. "
        "Photo scene: a clipboard with a blank checklist on a clean kitchen counter in soft daylight, no readable text on the clipboard. "
        + g["NO_NUM"] + " Write \"@kleanngreen\" in small Jost text at the bottom right."
    )

    # --- Reels 11-27 (tiempo), 12-04 (consejo), 12-06 (tiempo)
    g["REEL"]["11-27"] = (
        "Guests leave. Your afternoon stays yours",
        [
            ("Guests just left", "hands pulling used sheets off a bed in a bright guest room in morning light"),
            ("The reset is handled", "a wide view of the same guest room now tidy, with a made bed in fresh white sheets and folded towels at its foot, the nightstand wiped, soft morning light"),
            ("Your afternoon is yours · Send this to someone who hosts", "a hand wrapped around a leaf-green mug on a windowsill beside an open book, with the made bed softly blurred behind"),
        ],
        "Guests heading home after the long weekend?\nImagine the room already reset, and your afternoon yours.\nSend this to someone who hosts.\n\n" + TAGS_REEL,
        "Guests heading home after the long weekend? Imagine the guest room already reset, and your afternoon yours.\n\nWhat would you do with it?\n\n" + TAGS_FB,
    )
    g["SEED"]["11-27"] = (
        "a bright New York guest room with white walls, a wooden nightstand with a small lamp, and a window with sheer curtains. "
        "Soft morning daylight at about 5500 K. Props: white linens, a stack of folded white towels, a small green plant on the nightstand, a damp leaf-green microfiber cloth, "
        "an open book with no readable text and a leaf-green ceramic mug on the windowsill. "
        "Palette: warm whites, natural wood and leaf green. The same hands in every scene: adult hands with deep brown skin, short natural nails, no jewelry, no watch.",
        [
            ("Two hands pull the used sheets off a bed in one smooth motion and gather them into a bundle.",
             "medium shot from the foot of the bed at a slightly high angle, locked off.",
             "a soft rustle of fabric."),
            ("The same room appears finished: the bed is made with fresh white sheets, folded white towels sit at its foot, the nightstand is wiped and the lamp is in place; nothing moves except a slow drift of light.",
             "wide shot from the doorway, locked off with a very slow push-in of about 5%.",
             "quiet room tone."),
            ("A hand lifts a leaf-green mug from the windowsill beside an open book and holds it, steam rising; the made bed is softly blurred behind.",
             "medium close-up on the windowsill, slow rack focus from the mug to the made bed.",
             "a soft ceramic touch, then calm quiet."),
        ],
    )
    g["VO"]["11-27"] = [
        "[sighs] Guests just left. [short pause] And there's the bed.",
        "[warmly] Now imagine the whole room, already reset.",
        "[excited] And your afternoon is yours! Send this to a host.",
    ]

    t, clips, ig, fb = g["REEL"]["12-04"]
    clips = list(clips)
    clips[2] = ("3. Remote controls · Or let us do it", clips[2][1])
    g["REEL"]["12-04"] = (
        t, clips,
        "Before the holiday visits, wipe the spots everyone touches: door handles, light switches and remote controls.\n"
        "Save this for the weekend, or let us handle it and keep the weekend.\n\n" + TAGS_REEL,
        "Before the holiday visits, wipe the spots everyone touches: door handles, light switches and remote controls.\n\n"
        "Which one do you forget most often? Or message us for a free estimate and skip the list.\n\n" + TAGS_FB,
    )
    g["VO"]["12-04"][2] = "[excited] And the remote! Wipe all three, or let us do it."

    g["REEL"]["12-06"] = (
        "Winter entryway: already handled",
        [
            ("Winter in the city · Salt on the floor", "close-up of a hand wiping white road-salt marks off a dark slate entryway floor with a damp leaf-green microfiber cloth, the floor ending clean"),
            ("Handled", "a wide view of the tidy winter entryway: a clean dark slate floor, wet boots set square on a black rubber tray and a rubber doormat lying square at the door, soft overcast daylight"),
            ("Your evening is yours · Send this to someone in a walk-up", "a hand wrapped around a leaf-green mug on the sill of a window beside the entryway, snow falling softly outside"),
        ],
        "Winter entryways take a beating: salt, wet boots, a gritty mat.\nImagine it already handled, and your evening yours.\nSend this to someone who lives in a walk-up.\n\n#NYCCleaning #CleaningTips #ApartmentCleaning #WinterHome #CleaningReel",
        None,
    )
    anchor, scenes = g["SEED"]["12-06"]
    anchor = anchor.replace("a black rubber doormat.", "a black rubber doormat and a leaf-green ceramic mug.")
    scenes = list(scenes)
    scenes[1] = (
        "The entryway appears finished: the slate floor is clean and dark, wet boots sit square on the black rubber boot tray and the doormat lies square at the door; nothing moves except a slow drift of light.",
        "wide shot from inside the entryway, locked off with a very slow push-in of about 5%.",
        "quiet room tone with a faint hum of the city.",
    )
    scenes[2] = (
        "A hand lifts a leaf-green mug from the sill of the window beside the entryway, snow falling softly outside; steam rises.",
        "close-up on the mug and the sill, slow rack focus to the falling snow.",
        "a soft ceramic touch, then calm quiet.",
    )
    g["SEED"]["12-06"] = (anchor, scenes)
    g["VO"]["12-06"] = [
        "[curious] Salt on the floor again? [short pause] Winter does that.",
        "[warmly] Now picture it already clean.",
        "[excited] And your evening is yours! Send this to a friend in a walk-up.",
    ]

    # --- Singles 11-28, 11-29, 12-05
    cast = g["CAST"]
    g["SING"]["11-28"] = (
        "Guests coming in December? Spend the visit, not the prep",
        "The person sits on the edge of a freshly made guest bed with crisp white sheets and folded towels at its foot, holding a leaf-green mug and glancing toward the open door as if hearing guests arrive, a small plant on the nightstand; "
        "Clover sits on the floor beside a small closed suitcase, looking toward the door, soft daylight",
        cast["11-28"][1] + " sits on a made guest bed with a mug while a gray tabby cat with a green collar waits beside a small suitcase.",
        "Guests coming in December? Tell us the dates and we will plan the clean before they arrive.\nThen the visit is yours: time at the table, not time with a sponge.\nMessage us for a free estimate.\n\n" + TAGS_SAT,
        "Guests coming in December? Tell us the dates and we will plan the clean before they arrive. Then the visit is yours: time at the table, not time with a sponge.\n\nRequest a free estimate: " + UTM_FB + "nov2026_guests\n\n" + TAGS_FB,
    )
    g["SING"]["11-29"] = (
        "The Sunday after the long weekend is yours",
        "The person lies back on a clean sofa in a tidy Sunday-morning living room with feet up, reading a paperback with a plain cover, a mug on the side table and sunlight on the freshly vacuumed rug; "
        "Clover curls up at the other end of the sofa, soft daylight",
        cast["11-29"][1] + " reads on a sofa in a tidy living room while a gray tabby cat with a green collar curls up at the other end.",
        "The long weekend is wrapping up. Next Sunday could look like this: a book, a walk, a nap, and the cleaning already done.\nMessage us for a free estimate and make it every weekend.\n\n" + TAGS_IG,
        None,
    )
    s = g["SING"]["12-05"]
    g["SING"]["12-05"] = (
        "Start January with the weekends you wanted",
        s[1], s[2],
        "What do you want your January weekends to look like?\nSend us your preferred dates for a clean and we will plan it with you.\nMessage us for a free estimate.\n\n" + TAGS_SAT,
        "What do you want your January weekends to look like?\n\nSend us your preferred dates for a clean and we will plan it with you. Request a free estimate: " + UTM_FB + "dec2026_january\n\n" + TAGS_FB,
    )


# ====================================================================== TikTok (modulo tiktok_data)
def apply_tiktok(m):
    by = {p["id"]: p for p in m.P if p["brand"] == "kn"}
    cta = m.KN_CTA

    def upd(i, typ, angle, chip, **kw):
        p = by[i]
        p.update(type=typ, angle=angle, chip=chip)
        p.update(kw)

    # KN1: programado con su video terminado (10 nov). Solo cambia la descripcion.
    upd("KN1", TIP, "Tip first. The bridge is in the caption; the finished video does not change.", "Scheduled · caption change proposed",
        cap_lines=["Myth: more cleaner means cleaner.", "",
                   "Use a little, wait a minute, wipe with a damp cloth. Or hand it to us and spend that time elsewhere.", cta],
        status_lines=["Scheduled in Metricool for Tue, Nov 10 at 6 PM New York time, with its video already uploaded. It is set so TikTok sends a push notification to your phone instead of auto-publishing.",
                      "The video is finished, so the script below stays as recorded. Only the caption changes: the bridge line moves into the text.",
                      "Keep the AI-generated content label on."])

    upd("KN2", TB, "What would you do with your Saturday?", m_chip(),
        title="What would you do with your Saturday?", hook="What would you do with your Saturday?",
        beats=["What would you do with your Saturday, if the cleaning was already done?",
               "A long breakfast. A walk. That project you keep pushing back. The weekend usually goes to the apartment instead.",
               "Klean N Green NYC takes the cleaning. You take the day."],
        cap_lines=["What would you do with your Saturday?", "", "Klean N Green NYC takes the cleaning. You take the day.", "Free estimate: send us a message."],
        tags="#NYCCleaning #CleaningService #NYCLife")

    upd("KN3", TIP, "Tip first. The last beat hands the list to Klean N Green NYC.", m_chip(),
        beats=["Turnover day? Do it in this order.",
               "Strip the bed and start the laundry. Bathroom next, because it needs time to sit. Then kitchen and floors. Finish with a walk-through.",
               "Or send the whole list our way and keep your day for guests and tenants. Klean N Green NYC."],
        cap_lines=["Turnover day? Do it in this order.", "",
                   "Laundry, bathroom, kitchen and floors, walk-through. Or send the list our way and keep your day.", cta])

    upd("KN4", TIP, "Safety tip first. The last beat offers to do it for them.", m_chip(),
        beats=["Never mix bleach with ammonia. And never mix bleach with vinegar.",
               "They can release toxic gas. Use one product at a time, rinse between products, and open a window.",
               "Clean safely, or let Klean N Green NYC do it while you do something else."],
        cap_lines=["Never mix bleach with ammonia or vinegar.", "",
                   "One product at a time, rinse between, open a window. Or let us do it and do something else.", cta])

    upd("KN5", TIP, "Tip first. The last beat is about spending the day with guests.", m_chip(),
        beats=["Hosting this week? Three things in fifteen minutes.",
               "Clear the entry so guests have room. Wipe the bathroom counter and put out a fresh hand towel. Empty the trash before anyone arrives.",
               "Want the whole day with your guests? Message Klean N Green NYC for the cleanup."],
        cap_lines=["Hosting this week? Three things in 15 minutes.", "",
                   "Clear the entry, wipe the bathroom counter, empty the trash. Want the whole day with your guests? Message us.", cta])

    upd("KN6", TB, "Hiring a cleaner is about getting your time back.", m_chip(),
        beats=["Hiring a cleaning company is about getting your time back.",
               "So ask four things. What's included? Who brings the supplies? How are keys and access handled? And what happens if something is missed?",
               "A good company answers clearly, and then you stop thinking about it. Questions? Message Klean N Green NYC."],
        cap_lines=["Hiring a cleaner is about getting your time back. Ask these four questions.", "",
                   "Scope, supplies, access, and what happens if something is missed. Then you stop thinking about it.", cta])

    upd("KN7", TIP, "Tip first. The last beat offers to take it off their list.", m_chip(),
        beats=["Three cleaning mistakes that spread dirt.",
               "One: a dirty cloth. Two: dry dusting, which just pushes dust around, so use a damp microfiber. Three: skipping the corners.",
               "Fix these and a room looks cleaner fast. Or hand it to Klean N Green NYC."],
        cap_lines=["Three mistakes that spread dirt.", "",
                   "Dirty cloth, dry dusting, skipped corners. Or hand it to us and keep your time.", cta])

    upd("KN8", TIP, "Tip first. The last beat swaps the ten minutes for the service.", m_chip(),
        beats=["Four spots to clean once a month.",
               "Baseboards. Fridge shelves. The area under the sink. And fan or vent covers. One per week keeps it easy.",
               "Ten minutes a week, or let Klean N Green NYC take it off your list."],
        cap_lines=["Four spots to clean once a month.", "",
                   "Baseboards, fridge shelves, under the sink, vent covers. Or let us take it off your list.", cta])


def m_chip():
    return S_NEWSCRIPT


# ====================================================================== Videos de LinkedIn (modulo linkedin_video)
def apply_linkedin(m):
    by = {p["id"]: p for p in m.L}
    p = by["LI1"]
    p.update(type=TB, angle="Four details from you; the rest is off your plate.", chip=S_NEWSCRIPT,
             title="Four details to send before booking a cleaning crew",
             beats=["Booking a cleaning crew? Send four details first, and the rest is off your plate.",
                    "One: access, like keys, codes and building rules. Two: scope, the rooms and what's included. Three: the deadline. Four: today's condition, in a few photos.",
                    "With those, the estimate is clear and the first visit runs smooth.",
                    "Then your time goes back to your tenants and your team. Message Klean N Green NYC."],
             cap_lines=["Booking a cleaning crew for a unit or an office? Send these four details first, and the rest is off your plate:", "",
                        "1. Access: keys, codes and building rules.",
                        "2. Scope: which rooms and what is included.",
                        "3. Deadline: move-in, inspection or reopening dates.",
                        "4. Condition today: a few photos.", "",
                        "With those, the estimate is clearer and the first visit runs smoother. Your time goes back to tenants, your team and the rest of your list.", "",
                        "Request a free estimate: {link}"])
    q = by["LI2"]
    q.update(type=TIP, angle="Checklist first. The last beat offers to do it so the holidays stay free.", chip=S_NEWSCRIPT,
             beats=["A unit that will sit empty over the holidays? Do four things first.",
                    "Take out the trash and anything perishable. Wipe and dry the kitchen and bathroom surfaces. "
                    "Sweep or vacuum the floors. And photograph the unit, so you have a record of its condition.",
                    "In January, the unit is ready to show or turn over.",
                    "Or skip the list and let Klean N Green NYC do it, so your holidays stay yours. Message us."],
             cap_lines=["A unit that will sit empty over the holidays? Four things to do first:", "",
                        "1. Take out the trash and anything perishable.",
                        "2. Wipe and dry the kitchen and bathroom surfaces.",
                        "3. Sweep or vacuum the floors.",
                        "4. Photograph the unit, so its condition is documented.", "",
                        "Starting January with a unit that is ready to show or turn over makes the first week easier.", "",
                        "Or skip the list: we can take it from here, so your holidays stay yours. Request a free estimate: {link}"])
