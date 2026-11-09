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


def piece(p):
    day, hour = dlabel(p), "6 PM"
    spoken_lines = "\n".join(p["beats"])
    extra = meta_box(p["extra"]) if p["extra"] else ""
    meta = meta_box([
        f"**Presenter:** {p['presenter']}.",
        f"**Setting:** {p['setting']}.",
        f"**Length:** about 18 seconds, vertical 9:16, 1080 x 1920 px. Spoken script of {len(T.spoken(p).split())} words.",
    ])
    status = meta_box([
        f"Draft saved in Metricool for {NAME[p['brand']]} on TikTok ({T.HANDLE[p['brand']]}), {day} at 6 PM New York time. It holds a placeholder photo, so TikTok treats it as a photo post until you replace it.",
        "In the editor: remove the photo, upload the video and switch on the AI-generated content label. Nothing is published.",
    ])
    body = (
        det("Script, on-screen text and video prompt", (
            B.copybox("Spoken script (3 beats)", spoken_lines)
            + B.copybox("On-screen text for the first 3 seconds (add in the editor)", p["hook"])
            + B.copybox("Video prompt (Seedance or similar)", T.prompt(p))
        ), True)
        + det("Caption and hashtags (already in the Metricool draft)", B.copybox("TikTok caption", T.caption(p)), False)
        + det("Presenter and settings", meta + extra, False)
        + det("Metricool draft: status", status, False)
    )
    return (
        '<article class="piece">'
        '<div class="slot"><div class="when">'
        f"<b>{e(day)}</b><span>{e(hour)}</span></div>"
        f'<div class="what"><p class="what-t">TikTok: {e(p["title"])}</p>'
        f'<p class="what-m">TikTok {e(T.HANDLE[p["brand"]])} · AI presenter video, about 18 s {chipx("Draft · add video", "hip")}</p></div></div>'
        f"{body}</article>"
    )


def board_row(p):
    return (
        f"<tr><th scope='row'>{e(dlabel(p))} · 6 PM</th><td>TikTok</td>"
        f"<td>{e(p['title'])}</td><td>{chipx('Draft · add video', 'hip')}</td></tr>"
    )


def overview_sections(brand):
    name = NAME[brand]
    handle = T.HANDLE[brand]
    topics = (
        "product and produce tips: how to choose, how to use, what to cook"
        if brand == "kg" else
        "practical cleaning tips: myths, order of work, safety and what to ask a provider"
    )
    rs = B.section(
        "TikTok with AI presenters",
        B.callout(
            f"Eight TikToks for {name} ({handle}), two per week, Tuesday and Thursday at 6 PM New York time (week 3 moves for Thanksgiving). Each one is a video of about 18 seconds in which a different AI-generated presenter talks to the camera. The topics are {topics}. The scripts, prompts and captions are inside each week, among the other pieces.",
            "Format.",
        )
        + B.tiles([
            ("8", f"TikToks for {name}, each with its own presenter, script, video prompt and caption", "dato"),
            ("8", "drafts saved in Metricool, with a placeholder photo until you add the video", "dato"),
            ("18 s", "about, per video: 3 beats of 35 to 47 words", "dato"),
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
        "**A different presenter in every video.** Different ages, skin tones and settings. No presenter returns, and none should resemble a real person.",
        "**The presenter is a host, not a customer or an employee.** The scripts give tips and information. None says \"I shop here\" or \"I have been cleaning for years\", because an invented person cannot give a real testimonial.",
        "**Always labeled as AI.** Every caption ends with \"AI-generated video.\" and the TikTok AI-generated content label must be on when the video is uploaded.",
        "**Avoid in every prompt:** subtitles, logos, watermarks, music, extra people, readable brand names and text on screen.",
    ])
    rs += B.section("TikTok: presenter rules", rules)
    if brand == "kg":
        checks = [
            "**Products.** Every video mentions products the store should have on that date. Confirm stock before scheduling, or change the line. The scripts say \"ask us\" where stock is not certain.",
            "**Hours.** The captions of Nov 24 and Nov 25 contain [hours]. Fill them in or delete the line.",
            "**Thursday, November 26.** It is Thanksgiving, so there is no TikTok that day. Week 3 moves to Tuesday and Wednesday.",
            "**Facts.** The produce tips are general and common (ripeness, storage, safe cooking of yuca). If the store prefers different advice, change the script.",
            "**Spanish.** The scripts are in English, with one short Spanish line in the first video. The captions carry the Spanish. Tell me if the store wants more Spanish in the voice.",
            "**People in images.** The image rules for K&G Market posts (no generated people) do not change. These AI presenters exist only in the TikTok videos.",
            "**Commercial content label.** Metricool left TikTok's \"your brand\" option off. Decide when scheduling whether to turn it on.",
        ]
    else:
        checks = [
            "**Claims.** The tips are general and safe. No script promises results, certifications or product performance.",
            "**Safety tip (Nov 19).** Never mixing bleach with ammonia or vinegar is standard guidance. Keep the line as written.",
            "**Contact.** The captions invite a message and give no phone number, because the number differs between sources. Confirm the number before adding one.",
            "**Friday, November 27.** Week 3 uses Tuesday and Friday because Thursday the 26th is Thanksgiving.",
            "**Services mentioned.** Turnover cleaning and property management appear in the Klean N Green NYC pack. Confirm the company offers what the scripts imply.",
            "**Presenters.** The Klean rule of varying the people in the images also applies here: every TikTok has a different presenter.",
            "**Commercial content label.** Metricool left TikTok's \"your brand\" option off. Decide when scheduling whether to turn it on.",
        ]
    rs += B.section("TikTok: before approving", "<ul class='checks'>" + "".join(f"<li>{fmt(x)}</li>" for x in checks) + "</ul>")
    return rs


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
    # 3) secciones del Overview, antes del cierre del panel
    assert seg.rstrip().endswith("</section>")
    k = seg.rstrip().rfind("</section>")
    seg = seg[:k] + overview_sections(brand) + seg[k:]
    return html[:a] + seg + html[b:]
