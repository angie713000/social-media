#!/usr/bin/env python3
# TikTok con presentadores IA: piezas y secciones para integrarlas en el HTML de publicaciones por marca
import contextlib
import datetime as dt
import io
import re
import sys

sys.path.insert(0, ".")
with contextlib.redirect_stdout(io.StringIO()):
    import build_estrategia as B
    import build_publicaciones as K
import tiktok_data as T
import characters as CH

e, fmt = B.e, B.fmt
chipx, meta_box, det = K.chipx, K.meta_box, K.det

WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MO = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
NAME = {"kg": "K&G Market", "kn": "Klean N Green NYC"}


def _date(p):
    y, m, d = (int(v) for v in p["date"].split("-"))
    return dt.date(y, m, d)


def dlabel(p):
    d = _date(p)
    return f"{WD[d.weekday()]}, {MO[d.month-1]} {d.day}"


def week_of(p):
    return (_date(p) - dt.date(2026, 11, 9)).days // 7 + 1


def tchip(p):
    if not p.get("type"):
        return ""
    return chipx(p["type"], "dato" if p["type"] == "Time back" else "ref") + " "


def vchip(p):
    """Media status plus the proposal status (only Klean N Green NYC pieces carry a proposal)."""
    if p.get("chip") == "Scheduled · caption change proposed":
        return chipx(p["chip"], "hip")
    base = chipx("Draft · add video", "hip")
    return base + (" " + chipx(p["chip"], "hip") if p.get("chip") else "")


def cchip(p):
    return chipx(CH.name(p["char"]), "ref") + " " if p.get("char") else ""


def pmeta(p):
    """Presenter lines for the 'Presenter and settings' box."""
    if p.get("char"):
        x = CH.c(p["char"])
        return [
            f"**Presenter:** {CH.name(p['char'])}, {x['role'].lower()}, a recurring AI character. {p['presenter'].split(' (', 1)[1].rstrip(')').capitalize()}.",
            f"**Reference image:** attach the {CH.name(p['char'])} portrait from the Characters section in the Overview to the video prompt.",
        ]
    return [f"**Presenter:** {p['presenter']}. This finished video was made before the recurring characters and stays as it is."]


def angle(p):
    return f'<p class="angle"><b>Angle:</b> {e(p["angle"])}</p>' if p.get("angle") else ""


def piece(p):
    day, hour = dlabel(p), "6 PM"
    spoken_lines = "\n".join(p["beats"])
    extra = meta_box(p["extra"]) if p["extra"] else ""
    meta = meta_box(pmeta(p) + [
        f"**Setting:** {p['setting']}.",
        f"**Length:** about 18 seconds, vertical 9:16, 1080 x 1920 px. Spoken script of {len(T.spoken(p).split())} words.",
    ])
    if p.get("status_lines"):
        status = meta_box(p["status_lines"])
    else:
        status = meta_box([
            f"Draft saved in Metricool for {NAME[p['brand']]} on TikTok ({T.HANDLE[p['brand']]}), {day} at 6 PM New York time. It holds a placeholder photo, so TikTok treats it as a photo post until you replace it.",
            "In the editor: remove the photo, upload the video and switch on the AI-generated content label. Nothing is published.",
        ] + (["If the video for this day is already made, keep it and only change the caption."] if p.get("type") else []))
    body = (
        det("Script, on-screen text and video prompt", (
            B.copybox("Spoken script (3 beats)", spoken_lines)
            + B.copybox("On-screen text for the first 3 seconds (add in the editor)", p["hook"])
            + B.copybox("Video prompt (Seedance or similar)", T.prompt(p))
        ), True)
        + det("Caption and hashtags (already in the Metricool draft)", B.copybox("TikTok caption", T.caption(p)), False)
        + det("Character and setting", meta + extra, False)
        + det("Metricool draft: status", status, False)
    )
    return (
        '<article class="piece">'
        '<div class="slot"><div class="when">'
        f"<b>{e(day)}</b><span>{e(hour)}</span></div>"
        f'<div class="what"><p class="what-t">TikTok: {e(p["title"])}</p>'
        f'<p class="what-m">TikTok {e(T.HANDLE[p["brand"]])} · AI video, about 18 s {cchip(p)}{tchip(p)}{vchip(p)}</p></div></div>'
        f"{angle(p)}{body}</article>"
    )


def board_row(p):
    return (
        f"<tr><th scope='row'>{e(dlabel(p))} · 6 PM</th><td>TikTok</td>"
        f"<td>{e(p['title'])}{(' · ' + CH.name(p['char'])) if p.get('char') else ''}</td><td>{tchip(p)}{p.get('chip') and chipx(p['chip'], 'hip') or chipx('Draft · add video', 'hip')}</td></tr>"
    )


def overview_sections(brand):
    name = NAME[brand]
    handle = T.HANDLE[brand]
    topics = (
        "product and produce tips: how to choose, how to use, what to cook"
        if brand == "kg" else
        "the time you get back (what would you do with your Saturday, what to ask a provider) and practical cleaning tips that end with a bridge to the service"
    )
    chars_txt = CH.names(CH.ORDER[brand])
    ps_ = [p for p in T.P if p["brand"] == brand and p.get("char")]
    wc = [len(T.spoken(p).split()) for p in ps_]
    n_by = {k: sum(1 for p in ps_ if p["char"] == k) for k in CH.ORDER[brand]}
    rs = B.section(
        "TikTok with recurring characters",
        B.callout(
            f"Eight TikToks for {name} ({handle}), two per week, Tuesday and Thursday at 6 PM New York time (week 3 moves for Thanksgiving). Each one is a video of about 18 seconds in which one of the brand's two recurring AI characters, {chars_txt}, talks to the camera. The topics are {topics}. The scripts, prompts and captions are inside each week, among the other pieces. The characters, their reference portraits and their rules are in the Characters section above.",
            "Format.",
        )
        + B.tiles([
            ("8", f"TikToks for {name}, each with its script, video prompt and caption: " + ", ".join(f"{n_by[k]} with {CH.name(k)}" for k in CH.ORDER[brand]) + (" and the finished Nov 10 video, made before the characters" if brand == "kn" else ""), "dato"),
            ("8" if brand == "kg" else "7", "drafts saved in Metricool, with a placeholder photo until you add the video" if brand == "kg" else "drafts saved in Metricool, with a placeholder photo until you add the video (the Nov 10 TikTok is scheduled with its video)", "dato"),
            ("18 s", f"about, per video: 3 beats of {min(wc)} to {max(wc)} words", "dato"),
        ]),
        "Posting times come from Metricool's general TikTok reference, because the account is new and has no history yet.",
    )
    how = meta_box([
        "**1. Generate.** Copy the video prompt in Seedance or a similar tool. If it does not produce a voice with accurate lip sync, record the script in ElevenLabs and apply lip sync to the video.",
        "**2. Clips.** If your generator caps a clip below 18 seconds, generate beats 1 and 2 as one clip and beat 3 as another, with the same presenter and setting, and join them in the editor.",
        "**3. Check.** The face, hands and mouth look natural, the words match the script, and nothing on screen is garbled. Regenerate otherwise.",
        "**4. Edit.** Add the on-screen text and subtitles in the TikTok or video editor. Generators garble text inside video, so the prompts ask for none.",
        "**5. Upload.** Open the Metricool draft, remove the placeholder photo, upload the video and switch on the AI-generated content label.",
        "**6. Schedule.** Only after you have checked it. Nothing here is published without your approval.",
    ])
    rs += B.section("TikTok: how each video is made", how)
    rules = meta_box([
        f"**Two recurring characters.** {chars_txt} are the only presenters. The same face, hair, skin tone and clothes in every video, so viewers recognize them; the settings change from video to video. The look is fixed in the Characters section and repeated word for word in every prompt.",
        "**Reference image first.** Generate each character's portrait once, keep the best one and attach it to every video prompt. Check each result against the portrait before using it; regenerate if the face or hair drifted.",
        "**The character is a host, not a customer or an employee.** The scripts give tips and information. None says \"I shop here\" or \"I have been cleaning for years\", because an invented person cannot give a real testimonial or speak as staff.",
        "**Always labeled as AI.** Every caption ends with \"AI-generated video.\" and the TikTok AI-generated content label must be on when the video is uploaded. Each character introduces themself by name in the first video only.",
        "**Avoid in every prompt:** subtitles, logos, watermarks, music, extra people, readable brand names and text on screen. The characters never resemble a real person.",
    ])
    rs += B.section("TikTok: character rules", rules)
    if brand == "kg":
        checks = [
            "**Products.** Every video mentions products the store should have on that date. Confirm stock before scheduling, or change the line. The scripts say \"ask us\" where stock is not certain.",
            "**Hours.** The captions of Nov 24 and Nov 25 contain [hours]. Fill them in or delete the line.",
            "**Thursday, November 26.** It is Thanksgiving, so there is no TikTok that day. Week 3 moves to Tuesday and Wednesday.",
            "**Facts.** The produce tips are general and common (ripeness, storage, safe cooking of yuca). If the store prefers different advice, change the script.",
            "**Spanish.** The scripts are in English, with one short Spanish line in the first video. The captions carry the Spanish. Tell me if the store wants more Spanish in the voice.",
            "**Where Rosa and Dre appear.** In the TikToks, the four Reels and five single images. Google posts, Stories and the team photo stay free of generated people.",
            "**Commercial content label.** Metricool left TikTok's \"your brand\" option off. Decide when scheduling whether to turn it on.",
        ]
    else:
        checks = [
            "**Claims.** The tips are general and safe. No script promises results, certifications or product performance.",
            "**Safety tip (Nov 19).** Never mixing bleach with ammonia or vinegar is standard guidance. Keep the line as written.",
            "**Contact.** The captions invite a message and give no phone number, because the number differs between sources. Confirm the number before adding one.",
            "**Friday, November 27.** Week 3 uses Tuesday and Friday because Thursday the 26th is Thanksgiving.",
            "**Services mentioned.** Turnover cleaning and property management appear in the Klean N Green NYC pack. Confirm the company offers what the scripts imply.",
            "**Nov 10 TikTok.** It is scheduled with a finished video of a different presenter, made before the characters. It stays as it is; Maya and Daniel start on Nov 12.",
            "**Commercial content label.** Metricool left TikTok's \"your brand\" option off. Decide when scheduling whether to turn it on.",
        ]
    rs += B.section("TikTok: before approving", "<ul class='checks'>" + "".join(f"<li>{fmt(x)}</li>" for x in checks) + "</ul>")
    return rs


def _dlab(date_s):
    y, m, d = (int(v) for v in date_s.split("-"))
    x = dt.date(y, m, d)
    return f"{WD[x.weekday()]}, {MO[m-1]} {d}"


RULES_WHERE = {
    "kg": [
        "**Where they appear:** the TikToks, the four Wednesday Reels and five single images (Nov 9, Nov 16, Nov 20, Nov 30 and Dec 4).",
        "**Where they never appear:** the Google Business Profile posts, the Saturday Stories, the team photo post (Nov 13) and any photo of the store itself. Google prefers real photos of the business, and the team post must show the real team.",
        "**Real products:** a character can hold or present a product, but the photo or video of the shelf, the price and the stock come from the store.",
    ],
    "kn": [
        "**Where they appear:** the TikToks from Nov 12, the two LinkedIn videos, the Reels of Nov 27, Dec 4 and Dec 6, the single images of Nov 28, Nov 29 and Dec 5, and as hands in three carousels (After dinner, the office checklist and the property management carousel). Clover appears in single images, as before.",
        "**Where they never appear:** the weeks 1 and 2 posts, which are scheduled with finished media; the Nov 10 TikTok, which is scheduled with a finished video; the Dec 2 before and after (real photos); the Google posts; and the images of the website pages.",
        "**What the scenes show:** in time-back pieces Maya and Daniel appear after the work is done (a mug at the window, a book on the sofa, a checklist already ticked). In tip pieces they can demonstrate the tip. They are never shown cleaning a client's home.",
    ],
}


PLURAL = {
    "TikTok": ("TikTok", "TikToks"), "LinkedIn video": ("LinkedIn video", "LinkedIn videos"), "Reel": ("Reel", "Reels"),
    "Image": ("image", "images"), "Single image": ("single image", "single images"),
    "Instagram carousel": ("Instagram carousel (hands)", "Instagram carousels (hands)"),
    "LinkedIn carousel": ("LinkedIn carousel (hands)", "LinkedIn carousels (hands)"),
}


def characters_section(brand):
    keys = CH.ORDER[brand]
    name = NAME[brand]
    names = CH.names(keys)
    extra = " Clover, the gray tabby cat, stays as the non-human character in the single images." if brand == "kn" else ""
    body = B.callout(
        f"{names} are the two recurring AI characters of {name}. Each has a fixed look, voice and way of speaking, so viewers learn to recognize them from one video or image to the next. "
        "They are hosts that share tips and invite the viewer. They are not employees, customers or testimonials, and every piece that shows them is labeled as AI." + extra,
        "The idea.",
    )
    body += B.tiles([
        ("2", f"recurring characters: {names}", "dato"),
        (str(sum(len(CH.USES[k]) for k in keys)), "appearances planned across videos, Reels and images", "dato"),
        ("1", "reference portrait per character, generated once and attached to every video and image prompt", "ref"),
    ])
    steps = meta_box([
        "**1. Portrait.** Paste the portrait prompt of each character in your image generator and keep generating until the face matches the description. Save the best one as the reference.",
        "**2. Sheet (optional).** Generate the three-view sheet from the portrait. It helps when a tool drifts between front and side views.",
        "**3. Voice.** Paste the voice description in ElevenLabs Voice Design, save the voice you like and reuse it for every voiceover and lip sync of that character.",
        "**4. Attach.** Every video and image prompt that shows a character already carries its fixed description and asks for the reference image. Attach the portrait each time.",
        "**5. Check.** Compare each result with the portrait: face, hair, skin tone, age and accessories. If it drifted, regenerate instead of fixing it by hand.",
    ])
    body += '<h4 class="sub">Create each character once</h4>' + steps
    cards = ""
    for k in keys:
        x = CH.c(k)
        n_by = {}
        for _d, f, _t in CH.USES[k]:
            n_by[f] = n_by.get(f, 0) + 1
        counts = ", ".join(f"{v} {PLURAL[f][0 if v == 1 else 1]}" for f, v in n_by.items())
        facts = meta_box([
            f"**Role:** {x['role']}.",
            f"**Look (fixed):** {CH.identity(k)}.",
            f"**Personality:** {x['personality']}",
            f"**How {CH.pron(k)} speaks:** {x['speech']}",
            f"**Topics:** {x['topics']}",
            f"**First line, first video only:** \"{x['intro']}\"",
            f"**Appears in:** {counts}.",
        ])
        rows = "".join(
            f"<tr><th scope='row'>{e(_dlab(d))}</th><td>{e(f)}</td><td>{e(t)}</td></tr>" for d, f, t in sorted(CH.USES[k])
        )
        table = (
            '<div class="tablewrap"><table class="rev"><thead><tr><th>Date</th><th>Format</th><th>Piece</th></tr></thead><tbody>'
            + rows + "</tbody></table></div>"
        )
        inner = (
            facts
            + B.copybox(f"{x['name']}: reference portrait prompt (generate first)", CH.portrait_prompt(k))
            + B.copybox(f"{x['name']}: three-view sheet prompt (optional)", CH.sheet_prompt(k))
            + B.copybox(f"{x['name']}: voice description for ElevenLabs Voice Design", x["voice"])
            + det(f"Where {x['name']} appears", table, False)
        )
        cards += det(f"{x['name']} · {x['role']}", inner, True)
    body += cards
    body += '<h4 class="sub">Rules</h4>' + meta_box(RULES_WHERE[brand] + [
        f"**Labels.** Videos end the caption with \"AI-generated video.\" and use TikTok's AI label. Images that show {names} need the platform's AI label if the app offers one, or the line \"Image made with AI.\" at the end of the caption.",
        "**No testimonials, no claims.** The characters never say they bought, cooked or cleaned anything themselves, and the captions never speak in their name.",
        "**No likeness.** The descriptions are fictional. If a generated face resembles a real person you know of, regenerate it.",
    ])
    return B.section(f"Characters: {names}", body, "Two recurring AI characters, with their fixed look, voice and reference prompts.")


_MON = {m: i + 1 for i, m in enumerate(MO)}


def _key(day_txt, hour_txt):
    m = re.match(r"\w{3}, (\w{3}) (\d+)", day_txt)
    mon, d = _MON[m.group(1)], int(m.group(2))
    h = re.match(r"(\d+)\s*(AM|PM)", hour_txt)
    hh = int(h.group(1)) % 12 + (12 if h.group(2) == "PM" else 0)
    return (mon if mon >= 11 else mon + 12, d, hh)


def _pkey(p):
    d = _date(p)
    return (d.month if d.month >= 11 else d.month + 12, d.day, 18)


def _panel_span(html, pid):
    i = html.index(f'id="panel-{pid}"')
    start = html.rfind("<section", 0, i)
    nxt = html.find('<section role="tabpanel"', i)
    end = nxt if nxt != -1 else len(html)
    return start, end


def inject(html, brand):
    """Inserta los TikToks en cada semana (por orden de día y hora), en el calendario del Overview y las secciones del Overview."""
    ps = [p for p in T.P if p["brand"] == brand]
    # 1) semanas
    for n in (1, 2, 3, 4):
        a, b = _panel_span(html, f"{brand}-sem{n}")
        seg = html[a:b]
        arts = list(re.finditer(r'<article class="piece">.*?</article>', seg, flags=re.S))
        assert arts, (brand, n)
        for x, y in zip(arts, arts[1:]):
            assert seg[x.end():y.start()] == "", (brand, n, "contenido entre piezas")
        items = []
        for m in arts:
            t = re.search(r"<b>([^<]+)</b><span>([^<]+)</span>", m.group(0))
            items.append((_key(t.group(1), t.group(2)), 0, m.group(0)))
        for p in [q for q in ps if week_of(q) == n]:
            items.append((_pkey(p), 1, piece(p)))
        items.sort(key=lambda z: (z[0], z[1]))
        new = "".join(z[2] for z in items)
        seg = seg[:arts[0].start()] + new + seg[arts[-1].end():]
        html = html[:a] + seg + html[b:]
    # 2) calendario del Overview
    a, b = _panel_span(html, f"{brand}-resumen")
    seg = html[a:b]
    i = seg.index("<h3>Four-week calendar</h3>")
    ts = seg.index("<tbody>", i) + len("<tbody>")
    te = seg.index("</tbody>", ts)
    rows = list(re.finditer(r"<tr>.*?</tr>", seg[ts:te], flags=re.S))
    items = []
    for m in rows:
        t = re.search(r"<th scope='row'>(\w{3}, \w{3} \d+) · (\d+ [AP]M)</th>", m.group(0))
        items.append((_key(t.group(1), t.group(2)), 0, m.group(0)))
    for p in ps:
        items.append((_pkey(p), 1, board_row(p)))
    items.sort(key=lambda z: (z[0], z[1]))
    seg = seg[:ts] + "".join(z[2] for z in items) + seg[te:]
    # 2b) Characters section, right before the four-week calendar
    j = seg.index("<h3>Four-week calendar</h3>")
    j = seg.rfind("<section class='blk'>", 0, j)
    seg = seg[:j] + characters_section(brand) + seg[j:]
    # 3) secciones del Overview, antes del cierre del panel
    assert seg.rstrip().endswith("</section>")
    k = seg.rstrip().rfind("</section>")
    seg = seg[:k] + overview_sections(brand) + seg[k:]
    return html[:a] + seg + html[b:]
