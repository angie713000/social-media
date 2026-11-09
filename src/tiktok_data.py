#!/usr/bin/env python3
# TikTok con personajes IA recurrentes (dos por marca): 8 piezas por marca, martes y jueves 18:00 (hora de Nueva York)
import json

KG_PIN = "\U0001F4CD 9420 Church Ave, Brooklyn, NY 11212"
AI_LINE = "AI-generated video."

PLACEHOLDER = {
    "kg": "https://kngmarket.com/wp-content/uploads/cropped-Recurso-2.png",
    "kn": "https://static.metricool.com/brand-logo/202610/7768295-file-16678417109044158180.jpg",
}
BLOG = {"kg": "7762750", "kn": "7768295"}
HANDLE = {"kg": "@kngmarket", "kn": "@kleanandgreen"}

# id, marca, fecha, hora, titulo, gancho en pantalla, presentador, escenario, 3 frases, caption, hashtags
P = []


def add(id_, brand, date, title, hook, presenter, setting, beats, cap_lines, tags, extra=None):
    P.append(dict(id=id_, brand=brand, date=date, time="18:00", title=title, hook=hook,
                  presenter=presenter, setting=setting, beats=beats,
                  cap_lines=cap_lines, tags=tags, extra=extra or []))


# ---------------- K&G Market ----------------
add("KG1", "kg", "2026-11-10", "Ají amarillo: the yellow pepper behind Peruvian flavor",
    "The yellow pepper behind Peruvian flavor",
    "Woman in her 60s, short silver hair, warm brown skin, denim apron",
    "a bright home kitchen with a wooden counter and a small bowl of yellow pepper paste next to a cutting board",
    ["This is ají amarillo, the yellow pepper behind Peruvian flavor.",
     "It's bright and fruity with a medium heat, and it's the base of huancaína sauce and ají de gallina.",
     "Ask for it at K&G Market in Brooklyn. Pásate por la tienda."],
    ["The yellow pepper behind Peruvian flavor. \U0001F336️ / El ají amarillo, base de la cocina peruana.", "",
     "Bright, fruity, medium heat. Ask us at K&G Market.", KG_PIN],
    "#KGMarket #AjiAmarillo #PeruvianFood #BrooklynEats")

add("KG2", "kg", "2026-11-12", "Plantains: green, yellow or black?",
    "Green, yellow or black plantain?",
    "Man in his 30s, short beard, light brown skin, black T-shirt",
    "a sunny outdoor produce table with plantains in three stages of ripeness",
    ["Green, yellow or black plantain? It depends on what you're cooking.",
     "Green ones are firm and starchy, great for tostones. Very ripe ones with black skin are sweet, perfect for maduros.",
     "Not sure which is ready today? Ask us at K&G Market."],
    ["Green, yellow or black? \U0001F34C / ¿Verde, amarillo o negro?", "",
     "Green for tostones, very ripe for maduros.", KG_PIN],
    "#KGMarket #Plantains #CaribbeanFood #BrooklynEats")

add("KG3", "kg", "2026-11-17", "Rice and peas: keep the scotch bonnet whole",
    "Rice and peas: don't cut the scotch bonnet",
    "Woman in her 20s, long braids, dark brown skin, yellow hoodie",
    "a small apartment kitchen, a pot on the stove and one whole orange scotch bonnet on the counter",
    ["Making rice and peas? Don't cut the scotch bonnet.",
     "Add it whole and it gives flavor without the burn. Cut it, and the heat takes over. Take it out before serving, and wash your hands after touching it.",
     "Find the ingredients for the pot at K&G Market."],
    ["Rice and peas tip: keep the scotch bonnet whole. \U0001F336️ / No cortes el scotch bonnet.", "",
     "Whole for flavor, cut for heat.", KG_PIN],
    "#KGMarket #RiceAndPeas #CaribbeanFood #BrooklynEats")

add("KG4", "kg", "2026-11-19", "Is your mango ripe? Skip the color test",
    "Is your mango ripe? Skip the color test",
    "Man in his 50s, bald, round glasses, fair skin, green flannel shirt",
    "a sunny kitchen counter with a bowl of mangoes",
    ["Is your mango ripe? Don't trust the color.",
     "Press it gently: it should give a little. Smell near the stem: sweet and fruity means it's ready. Not ready? Leave it on the counter for a day or two.",
     "Ask us what's ripe today at K&G Market."],
    ["Skip the color test. \U0001F96D / No te fíes del color.", "",
     "Press gently, smell near the stem.", KG_PIN],
    "#KGMarket #Mango #FreshProduce #BrooklynEats")

add("KG5", "kg", "2026-11-24", "A new side for the Thanksgiving table",
    "Add one new side to Thanksgiving",
    "Woman in her 30s wearing a hijab, light brown skin, cream sweater",
    "a warm dining room with a set table, candles and serving dishes",
    ["Want something new on the Thanksgiving table?",
     "Try sweet plantains, rice and peas, or huancaína over boiled potatoes. All easy to share, and some can be made ahead.",
     "Ask us what's fresh this week at K&G Market."],
    ["A new side for the Thanksgiving table. \U0001F983 / Un acompañante nuevo para Thanksgiving.", "",
     "Sweet plantains, rice and peas, huancaína over potatoes.", KG_PIN,
     "\U0001F558 Special hours: [hours] / Horario especial: [horario]"],
    "#KGMarket #ThanksgivingFood #HolidayTable #BrooklynEats",
    extra=["Fill in [hours] in the caption before scheduling."])

add("KG6", "kg", "2026-11-25", "How to pick a sweet pineapple",
    "Pick a sweet pineapple in 3 seconds",
    "Young man in his 20s with East Asian features, black hair, white T-shirt and apron",
    "an outdoor patio table with a whole pineapple and a knife",
    ["How to pick a sweet pineapple.",
     "Smell the bottom: it should smell sweet, not sour. Look for green leaves and a fruit that feels heavy. And keep the peel: it's the base of chicha morada.",
     "Ask us at K&G Market."],
    ["Smell the bottom. \U0001F34D / Huele la base.", "",
     "Sweet smell, green leaves, heavy fruit. Keep the peel for chicha morada.", KG_PIN,
     "\U0001F558 Special hours: [hours] / Horario especial: [horario]"],
    "#KGMarket #Pineapple #FreshProduce #BrooklynEats",
    extra=["Fill in [hours] in the caption before scheduling."])

add("KG7", "kg", "2026-12-01", "How to pick yuca (and never eat it raw)",
    "Yuca: never eat it raw",
    "Woman in her 70s, white hair in a bun, deep brown skin, floral blouse",
    "a farmhouse kitchen with yuca roots on a wooden cutting board",
    ["How to pick yuca.",
     "Choose firm roots with no soft spots or dark streaks. The flesh should be bright white. Always cook it, never eat it raw.",
     "Ask for yuca at K&G Market. Boil it, then fry or mash it."],
    ["Pick yuca like this. / Así se escoge la yuca.", "",
     "Firm, no soft spots, white inside. Always cook it.", KG_PIN],
    "#KGMarket #Yuca #CaribbeanFood #BrooklynEats")

add("KG8", "kg", "2026-12-03", "Five things to start Peruvian and Caribbean cooking",
    "5 things to start Peruvian + Caribbean cooking",
    "Man in his 40s, short black hair graying at the temples, medium-tan skin, gray henley shirt",
    "a kitchen table with five ingredients laid out on a linen cloth",
    ["New to Peruvian and Caribbean cooking? Start with five things.",
     "Ají amarillo. Ripe plantains. A scotch bonnet. Purple corn. And yuca. Each one unlocks a classic dish.",
     "Take this list to K&G Market and ask us."],
    ["Five things to start. / Cinco cosas para empezar.", "",
     "Ají amarillo, ripe plantains, scotch bonnet, purple corn, yuca.", KG_PIN],
    "#KGMarket #PeruvianFood #CaribbeanFood #BrooklynEats")

# ---------------- Klean N Green NYC ----------------
KN_CTA = "Questions? Send us a message."

add("KN1", "kn", "2026-11-10", "Myth: more cleaner means cleaner",
    "More cleaner ≠ cleaner",
    "Black man in his 40s, short fade, gray sweatshirt",
    "a modern white kitchen with a spray bottle and a folded cloth on the counter",
    ["Myth: more cleaner means a cleaner home.",
     "Too much product leaves a sticky film that attracts dirt. Use a little, let it sit for a minute, then wipe with a damp cloth.",
     "Less product, better result. Klean N Green NYC."],
    ["Myth: more cleaner means cleaner.", "",
     "Use a little, wait a minute, wipe with a damp cloth.", KN_CTA],
    "#NYCCleaning #CleaningTips #CleaningMyths")

add("KN2", "kn", "2026-11-12", "Clean in the right order",
    "Clean top to bottom",
    "White woman in her 30s, red hair, freckles, white T-shirt",
    "a bright living room with shelves and a vacuum cleaner in the background",
    ["Cleaning order matters.",
     "Start high: shelves and surfaces first, floors last. Dust falls down, so you clean the floor only once. Dry tasks first, wet tasks after.",
     "Same time, better result. Klean N Green NYC."],
    ["Clean top to bottom, dry before wet.", "",
     "Dust falls down, so floors come last.", KN_CTA],
    "#NYCCleaning #CleaningTips #HomeTips")

add("KN3", "kn", "2026-11-17", "Turnover day: the order that saves time",
    "Turnover day? Do it in this order",
    "Latino man in his 50s, salt-and-pepper hair, navy polo shirt",
    "a bright apartment bedroom with a freshly made bed",
    ["Turnover day? Do it in this order.",
     "Strip the bed and start the laundry. Bathroom next, because it needs time to sit. Then kitchen and floors. Finish with a walk-through.",
     "Need a hand between guests or tenants? Message Klean N Green NYC."],
    ["Turnover day? Do it in this order.", "",
     "Laundry, bathroom, kitchen and floors, walk-through.", KN_CTA],
    "#NYCCleaning #PropertyManagement #ApartmentCleaning")

add("KN4", "kn", "2026-11-19", "Never mix these two cleaners",
    "Never mix these two cleaners",
    "South Asian woman in her 20s, long dark hair, denim shirt",
    "a bathroom with a small window open and two plain spray bottles on the counter",
    ["Never mix bleach with ammonia. And never mix bleach with vinegar.",
     "They can release toxic gas. Use one product at a time, rinse between products, and open a window.",
     "Clean safely. Klean N Green NYC."],
    ["Never mix bleach with ammonia or vinegar.", "",
     "One product at a time, rinse between, open a window.", KN_CTA],
    "#NYCCleaning #CleaningTips #CleaningSafety")

add("KN5", "kn", "2026-11-24", "Hosting this week: 15 minutes before guests arrive",
    "Hosting tomorrow? 15 minutes",
    "Woman in her 70s, white hair, glasses, soft green cardigan",
    "a home entryway with a coat rack and a console table",
    ["Hosting this week? Three things in fifteen minutes.",
     "Clear the entry so guests have room. Wipe the bathroom counter and put out a fresh hand towel. Empty the trash before anyone arrives.",
     "Need a reset after the party? Message Klean N Green NYC."],
    ["Hosting this week? Three things in 15 minutes.", "",
     "Clear the entry, wipe the bathroom counter, empty the trash.", KN_CTA],
    "#NYCCleaning #CleaningTips #HostingTips")

add("KN6", "kn", "2026-11-27", "Four questions to ask a cleaning company",
    "Hiring a cleaner? Ask these 4 things",
    "East Asian man in his 30s, glasses, navy blazer",
    "a tidy home office with a laptop on the desk",
    ["Hiring a cleaning company? Ask four things.",
     "What's included? Who brings the supplies? How are keys and access handled? And what happens if something is missed?",
     "A good company answers clearly. Questions? Message Klean N Green NYC."],
    ["Hiring a cleaner? Ask these four questions.", "",
     "Scope, supplies, access, and what happens if something is missed.", KN_CTA],
    "#NYCCleaning #CleaningService #CleaningTips")

add("KN7", "kn", "2026-12-01", "Three mistakes that spread dirt",
    "3 mistakes that spread dirt",
    "Black woman in her 50s, short natural hair with gray streaks, linen shirt",
    "a living room with a bookshelf, a microfiber cloth in her hand",
    ["Three cleaning mistakes that spread dirt.",
     "One: a dirty cloth. Two: dry dusting, which just pushes dust around, so use a damp microfiber. Three: skipping the corners.",
     "Fix these and a room looks cleaner fast. Klean N Green NYC."],
    ["Three mistakes that spread dirt.", "",
     "Dirty cloth, dry dusting, skipped corners.", KN_CTA],
    "#NYCCleaning #CleaningTips #ResidentialCleaning")

add("KN8", "kn", "2026-12-03", "Four spots to clean once a month",
    "4 spots to clean once a month",
    "Man in his 20s, light brown skin, curly dark hair, beard, gray hoodie",
    "a bright kitchen with the fridge door open and a sponge in his hand",
    ["Four spots to clean once a month.",
     "Baseboards. Fridge shelves. The area under the sink. And fan or vent covers. One per week keeps it easy.",
     "Set a ten-minute timer and start. Klean N Green NYC."],
    ["Four spots to clean once a month.", "",
     "Baseboards, fridge shelves, under the sink, vent covers.", KN_CTA],
    "#NYCCleaning #CleaningTips #ApartmentCleaning")


import sys as _sys
import kn_timeback as _KT
import characters as CH

_KT.apply_tiktok(_sys.modules[__name__])
CH.apply_tiktok(_sys.modules[__name__])


def spoken(p):
    return " ".join(p["beats"])


def caption(p):
    return "\n".join(p["cap_lines"]) + "\n\n" + p["tags"] + "\n" + AI_LINE


def prompt(p):
    return (
        "Vertical 9:16 smartphone-style video, about 18 seconds, one continuous take. "
        f"{p['presenter']} speaks directly to the camera in {p['setting']}. "
        + (CH.ref_sentence(p["char"]) + " " if p.get("char") else "")
        + "Natural, friendly, conversational delivery with small hand gestures, chest-up handheld selfie framing, "
        "soft natural light, realistic skin and hair, accurate lip sync. "
        f"Spoken dialogue in English: \"{spoken(p)}\" "
        "No on-screen text, no subtitles, no logos, no watermark, no music. "
        "A realistic fictional person, not the likeness of any real person."
    )


def draft_info(p):
    d = p["date"]
    return {
        "autoPublish": False, "draft": True, "descendants": [], "firstCommentText": "",
        "hasNotReadNotes": False, "media": [PLACEHOLDER[p["brand"]]], "mediaAltText": [],
        "providers": [{"network": "tiktok"}],
        "publicationDate": {"dateTime": f"{d}T18:00:00", "timezone": "America/New_York"},
        "shortener": False, "smartLinkData": {"ids": []},
        "text": caption(p),
        "tiktokData": {"title": p["hook"][:90], "disableComment": False, "disableDuet": False, "disableStitch": False,
                       "privacyOption": "PUBLIC_TO_EVERYONE", "commercialContentThirdParty": False,
                       "commercialContentOwnBrand": False, "autoAddMusic": False, "isAigc": True},
    }


if __name__ == "__main__":
    for p in P:
        print(p["id"], p["date"], len(spoken(p).split()), "words")
        print(json.dumps(draft_info(p), ensure_ascii=False))
        print()
