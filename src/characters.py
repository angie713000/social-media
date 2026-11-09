#!/usr/bin/env python3
"""Recurring AI characters: two per brand.

K&G Market: Rosa and Dre.  Klean N Green NYC: Maya and Daniel (plus Clover the cat, defined in build_publicaciones.py).

This module holds only data and text helpers (no HTML), so any pack module can import it.
Every prompt that shows a character builds the description from identity(), so the face, hair, skin and clothes
never drift from one piece to the next. The reference portraits (portrait_prompt) are generated once and
attached to every video and image prompt.
"""

CHARS = {
    "rosa": dict(
        name="Rosa", brand="kg", pron="she",
        role="Pantry and produce guide",
        age="a woman in her 60s",
        look="short silver hair, warm brown skin, soft laugh lines and small gold hoop earrings",
        outfit="a denim apron over a cream blouse",
        personality="Patient, warm and a little playful. Explains a product the way a neighbor would: slowly, with one clear tip.",
        speech="Short, calm sentences in clear English. Product and dish names keep their own names, and a short Spanish phrase is welcome. Starts from the product, not from herself.",
        voice="A warm, unhurried woman's voice in her 60s. Clear American English at a relaxed pace, with natural, gentle pronunciation of Spanish words. Friendly and reassuring, like a neighbor explaining a recipe.",
        topics="Peruvian pantry (ají amarillo, yuca, purple corn), how to choose produce, the holiday table.",
        hands="warm brown skin with a few fine age spots, short natural nails, no rings, the cuffs of a cream blouse",
        intro="Hi, I'm Rosa.",
    ),
    "dre": dict(
        name="Dre", brand="kg", pron="he",
        role="Caribbean kitchen guide",
        age="a man in his early 30s",
        look="a short trimmed beard, light brown skin, short black hair and a thin silver chain",
        outfit="a black T-shirt",
        personality="Upbeat, quick and practical. Gives the tip first and the reason second, like a friend leaning over the counter.",
        speech="Short, punchy sentences in everyday English. Names the product and the dish in the first five words. Dish names keep their own names (tostones, maduros, scotch bonnet).",
        voice="A friendly, upbeat man's voice in his early 30s. Clear American English at an easy, quick pace, with light Caribbean warmth and a smiling tone. Sounds like a friend giving a quick tip.",
        topics="Caribbean cooking (plantains, rice and peas, scotch bonnet), mangoes and pineapples, quick kitchen tips.",
        hands="light brown skin, short natural nails, no rings, bare forearms",
        intro="Hi, I'm Dre.",
    ),
    "maya": dict(
        name="Maya", brand="kn", pron="she",
        role="Time-back host",
        age="a woman in her early 30s",
        look="warm tan skin, dark brown wavy hair in a loose low bun and small silver stud earrings",
        outfit="a soft sage-green sweater",
        personality="Calm, bright and easygoing. Talks about the free time first and the cleaning second, and never lectures.",
        speech="Opens with a question or the moment, not with a claim. Sentences of about ten words. Ends by handing the day back to the viewer.",
        voice="A calm, bright woman's voice in her early 30s. Clear American English, relaxed and conversational, with a smiling tone, like a friend inviting you to take your weekend back.",
        topics="Homes and apartments: what to do with the time you get back, cleaning order and quick tips, hosting.",
        hands="warm tan skin, short natural nails, no rings, the cuff of a soft sage-green sweater",
        intro="Hi, I'm Maya.",
    ),
    "daniel": dict(
        name="Daniel", brand="kn", pron="he",
        role="Property and office host",
        age="a man in his late 40s",
        look="light brown skin, short dark hair and a trimmed salt-and-pepper beard",
        outfit="a navy quarter-zip sweater over a white collared shirt",
        personality="Steady, practical and reassuring. Explains a checklist the way a property manager would: in order, with no drama.",
        speech="Numbered steps and plain words. Names the situation first (turnover, vacant unit, office), then the steps. Never says he cleans or manages anything himself.",
        voice="A calm, steady man's voice in his late 40s. Clear American English at a measured pace, professional and reassuring, like a property manager walking through a checklist.",
        topics="Property managers and office teams: turnovers, vacant units, what to ask a provider, what to send before booking.",
        hands="light brown skin, short natural nails, no rings, the cuff of a navy quarter-zip sweater",
        intro="Hi, I'm Daniel.",
    ),
}

ORDER = {"kg": ["rosa", "dre"], "kn": ["maya", "daniel"]}

# Where each character appears: filled by the pack modules while they build their pieces.
USES = {k: [] for k in CHARS}


def use(k, date, fmt, title):
    """Register one appearance. date is YYYY-MM-DD, fmt is a short label such as 'TikTok'."""
    if (date, fmt, title) not in USES[k]:
        USES[k].append((date, fmt, title))


def c(k):
    return CHARS[k]


def name(k):
    return CHARS[k]["name"]


def names(keys):
    n = [CHARS[k]["name"] for k in keys]
    return " and ".join(n)


def identity(k, outfit=True):
    """One fixed description used in every prompt that shows the character."""
    x = CHARS[k]
    s = f"{x['name']}, {x['age']} with {x['look']}"
    if outfit:
        s += f", wearing {x['outfit']}"
    return s


def pron(k, form="subj"):
    he = CHARS[k]["pron"] == "he"
    return {"subj": "he" if he else "she", "obj": "him" if he else "her", "pos": "his" if he else "her"}[form]


REF_SENTENCE = (
    "Use the attached reference image of {n} for the face, hair, build and clothing; "
    "if the tool does not accept a reference image, follow this description exactly."
)


def ref_sentence(k):
    return REF_SENTENCE.format(n=CHARS[k]["name"])


def ref_sentence_many(keys):
    n = " and ".join(CHARS[k]["name"] for k in keys)
    return (
        f"Use the attached reference images of {n}, one image per person, for each face, hair, build and clothing; "
        "if the tool does not accept reference images, follow these descriptions exactly."
    )


def hands_text(k):
    x = CHARS[k]
    return f"{x['name']}'s hands ({x['hands']})"


def alt_person(k):
    """Neutral description for alt text: no name, because the photo does not show one."""
    x = CHARS[k]
    a = x["age"]
    return a[0].upper() + a[1:] + f" in {x['outfit']}"


def block_scene(k, accent):
    """'The person' block for single-image prompts: fixed identity + reference sentence + candid-photo rules."""
    x = CHARS[k]
    return (
        f"The person is {x['name']}, the recurring character of the brand: {x['age']} with {x['look']}, wearing {x['outfit']}; {accent}. "
        + ref_sentence(k)
        + f" Candid and absorbed in what {pron(k)} is doing, not looking at the camera. Natural proportions and natural hands with five fingers, no exaggerated smile. "
        f"Keep {x['name']}'s face, hair, build and clothes identical in every image of the set."
    )


def presenter(k):
    """Text for the 'presenter' field of a video prompt: the name, then the fixed description in parentheses."""
    x = CHARS[k]
    return f"{x['name']} ({x['age']} with {x['look']}, wearing {x['outfit']})"


def portrait_prompt(k):
    return (
        f"Photorealistic portrait photograph of {identity(k)}. "
        "Front-facing, chest-up, relaxed expression with a hint of a smile, looking straight at the camera. "
        "Soft diffuse daylight, plain light-gray wall, shallow depth of field, natural skin texture with fine lines and pores, true-to-life colors. "
        "Vertical 4:5 format, 1080 x 1350 px. "
        "No text, no logos, no watermark, no extra jewelry beyond what is described. "
        "A realistic fictional person, not the likeness of any real person."
    )


def sheet_prompt(k):
    return (
        f"Character reference sheet of {identity(k)}. "
        "The same person shown three times side by side on a plain light-gray background: front view, three-quarter view and side profile, all chest-up, "
        "with the same relaxed expression and identical hair, clothing and accessories in the three views. "
        "Photorealistic, soft even daylight, natural skin texture. Horizontal 3:2 format. "
        "No text, no labels, no watermark. "
        "A realistic fictional person, not the likeness of any real person."
    )


def tag_ai_note(keys):
    n = " and ".join(CHARS[k]["name"] for k in keys)
    return (
        f"{n} {'is an AI character' if len(keys) == 1 else 'are AI characters'}. When you schedule this post, switch on the platform's AI label if the app offers one; "
        "if it does not, end the caption with \"Image made with AI.\""
    )


def ai_video_note(keys, marked=False):
    n = " and ".join(CHARS[k]["name"] for k in keys)
    tail = "; the Instagram draft is already marked as AI-generated" if marked else ""
    return f"{n} {'is an AI character' if len(keys) == 1 else 'are AI characters'}. Switch on the AI label when you schedule this Reel{tail}."


# ---------------------------------------------------------------------------
# Appliers (called by the modules that own the pieces)
# ---------------------------------------------------------------------------
TT = {
    "KG1": "rosa", "KG2": "dre", "KG3": "dre", "KG4": "rosa", "KG5": "rosa", "KG6": "dre", "KG7": "rosa", "KG8": "dre",
    "KN2": "maya", "KN3": "daniel", "KN4": "maya", "KN5": "maya", "KN6": "daniel", "KN7": "maya", "KN8": "daniel",
}
LI = {"LI1": "daniel", "LI2": "daniel"}


def _apply(ps, assign, fmt_label):
    first = {}
    for p in sorted(ps, key=lambda q: q["date"]):
        k = assign.get(p["id"])
        if not k:
            continue
        p["char"] = k
        p["presenter"] = presenter(k)
        if k not in first:
            first[k] = p["id"]
            p["beats"][0] = CHARS[k]["intro"] + " " + p["beats"][0]
        use(k, p["date"], fmt_label, p["title"])


def apply_tiktok(m):
    _apply(m.P, TT, "TikTok")


def apply_linkedin(m):
    # LinkedIn is a separate audience, so Daniel introduces himself in the first LinkedIn video as well.
    _apply(m.L, LI, "LinkedIn video")
