#!/usr/bin/env python3
# Videos de LinkedIn con presentador IA para Klean N Green NYC: 2 piezas, miércoles 11:00 (hora de Nueva York).
# Datos + piezas HTML + inyección en el HTML de publicaciones por marca.
import datetime as dt
import re
import sys

sys.path.insert(0, ".")
import tiktok_html as TH
import tiktok_data as T

B, K = TH.B, TH.K
e, fmt = B.e, B.fmt
chipx, meta_box, det = TH.chipx, TH.meta_box, TH.det

BLOG = "7768295"
AI_LINE = "AI-generated video."
CONTACT = "https://kleannyc.com/contact-us/?utm_source=linkedin&utm_medium=social&utm_campaign={c}"

L = []


def add(id_, date, title, hook, presenter, setting, beats, cap_lines, tags, campaign, extra=None):
    L.append(dict(id=id_, brand="kn", date=date, time="11:00", title=title, hook=hook,
                  presenter=presenter, setting=setting, beats=beats, cap_lines=cap_lines,
                  tags=tags, campaign=campaign, extra=extra or []))


add("LI1", "2026-11-25", "Four details to send before booking a cleaning crew",
    "Booking a cleaning crew? Send these 4 details",
    "Woman in her 40s, olive skin, dark wavy shoulder-length hair, charcoal blazer over a white top",
    "a bright small-office reception area with a plant, a wooden desk and a window with soft daylight behind her",
    ["Booking a cleaning crew for a unit or an office? Four details help avoid rework.",
     "One: access, meaning keys, codes and building rules. Two: scope, meaning which rooms and what is included. "
     "Three: the deadline, including move-in or inspection dates. Four: the condition today, with a few photos.",
     "Send those four and the estimate is clearer, and the first visit runs smoother.",
     "Planning ahead? Message Klean N Green NYC."],
    ["Booking a cleaning crew for a unit or an office? Send these four details first:", "",
     "1. Access: keys, codes and building rules.",
     "2. Scope: which rooms and what is included.",
     "3. Deadline: move-in, inspection or reopening dates.",
     "4. Condition today: a few photos.", "",
     "With those, the estimate is clearer and the first visit runs smoother.", "",
     "Request a free estimate: {link}"],
    "#NYCCleaning #PropertyManagement #FacilitiesManagement",
    "nov2026_brief",
    extra=["Wednesday Nov 25 is the day before Thanksgiving. If you prefer another date, tell me and I move the draft."])

add("LI2", "2026-12-02", "A unit that will sit empty over the holidays: four things to do first",
    "Vacant over the holidays? 4 things to do first",
    "Man in his 60s, short gray beard, tan skin, light blue oxford shirt with the sleeves rolled up",
    "an empty apartment living room with a few closed moving boxes, bare walls and winter daylight from a large window",
    ["A unit that will sit empty over the holidays? Do four things first.",
     "Take out the trash and anything perishable. Wipe and dry the kitchen and bathroom surfaces. "
     "Sweep or vacuum the floors. And photograph the unit, so you have a record of its condition.",
     "In January, you start with a unit that is ready to show or turn over.",
     "Need the clean scheduled? Message Klean N Green NYC."],
    ["A unit that will sit empty over the holidays? Four things to do first:", "",
     "1. Take out the trash and anything perishable.",
     "2. Wipe and dry the kitchen and bathroom surfaces.",
     "3. Sweep or vacuum the floors.",
     "4. Photograph the unit, so its condition is documented.", "",
     "Starting January with a unit that is ready to show or turn over makes the first week easier.", "",
     "Need the clean scheduled? Request a free estimate: {link}"],
    "#NYCCleaning #PropertyManagement #Turnover",
    "dic2026_unidad_vacia",
    extra=["It comes one day after the Dec 1 year-end calendar post. The two are complementary: the calendar says when, this video says what."])


def spoken(p):
    return " ".join(p["beats"])


def clip_text(p, n):
    return " ".join(p["beats"][:2]) if n == 1 else " ".join(p["beats"][2:])


def link(p):
    return CONTACT.format(c=p["campaign"])


def caption(p):
    body = "\n".join(p["cap_lines"]).replace("{link}", link(p))
    return body + "\n\n" + p["tags"] + "\n" + AI_LINE


def prompt(p, n):
    cont = (
        "This is clip 2 of 2 and continues the same scene: the same person, the same outfit, the same room, "
        "the same light and the same framing as clip 1. " if n == 2 else "This is clip 1 of 2. "
    )
    return (
        "Square 1:1 video, about 15 seconds, one continuous take, camera at eye level on a tripod. "
        f"{cont}"
        f"{p['presenter']} speaks directly to the camera in {p['setting']}. "
        "Calm, professional, conversational delivery with small hand gestures, chest-up framing, "
        "soft natural light, realistic skin and hair, accurate lip sync. "
        f"Spoken dialogue in English: \"{clip_text(p, n)}\" "
        "No on-screen text, no subtitles, no logos, no watermark, no music. "
        "A realistic fictional person, not the likeness of any real person."
    )


def draft_info(p):
    d = p["date"]
    return {
        "autoPublish": False, "draft": True, "descendants": [], "firstCommentText": "",
        "hasNotReadNotes": False, "media": [], "mediaAltText": [],
        "providers": [{"network": "linkedin"}],
        "publicationDate": {"dateTime": f"{d}T11:00:00", "timezone": "America/New_York"},
        "shortener": True, "smartLinkData": {"ids": []},
        "text": caption(p),
        "linkedinData": {"previewIncluded": True, "type": "post"},
    }


# ---------------------------------------------------------------- HTML
def dlabel(p):
    return TH.dlabel(p)


def piece(p):
    day = dlabel(p)
    words = len(spoken(p).split())
    meta = meta_box([
        f"**Presenter:** {p['presenter']}.",
        f"**Setting:** {p['setting']}.",
        f"**Length:** about 30 seconds in two clips of about 15 seconds, square 1:1, 1080 x 1080 px. Spoken script of {words} words.",
        "**Continuity:** if the tool accepts a reference image, use a frame of clip 1 for clip 2 so the person and the room match.",
    ])
    extra = meta_box(p["extra"]) if p["extra"] else ""
    status = meta_box([
        f"Draft saved in Metricool for Klean N Green NYC on LinkedIn, {day} at 11 AM New York time. It holds the text only and no media, like the other LinkedIn drafts.",
        "In the editor: upload the video, turn on captions and schedule it only after you have checked it. Nothing is published.",
    ])
    body = (
        det("Script, on-screen text and video prompts", (
            B.copybox("Spoken script (4 beats)", "\n".join(p["beats"]))
            + B.copybox("On-screen text for the first 3 seconds (add in the editor)", p["hook"])
            + B.copybox("Video prompt, clip 1 of 2 (beats 1 and 2)", prompt(p, 1))
            + B.copybox("Video prompt, clip 2 of 2 (beats 3 and 4)", prompt(p, 2))
        ), True)
        + det("Post text and hashtags (already in the Metricool draft)", B.copybox("LinkedIn text", caption(p)), False)
        + det("Presenter and settings", meta + extra, False)
        + det("Metricool draft: status", status, False)
    )
    return (
        '<article class="piece">'
        '<div class="slot"><div class="when">'
        f"<b>{e(day)}</b><span>11 AM</span></div>"
        f'<div class="what"><p class="what-t">LinkedIn video: {e(p["title"])}</p>'
        f'<p class="what-m">LinkedIn · AI presenter video, about 30 s {chipx("Draft · add video", "hip")}</p></div></div>'
        f"{body}</article>"
    )


def board_row(p):
    return (
        f"<tr><th scope='row'>{e(dlabel(p))} · 11 AM</th><td>LinkedIn</td>"
        f"<td>Video: {e(p['title'])}</td><td>{chipx('Draft · add video', 'hip')}</td></tr>"
    )


def overview_section():
    rs = B.section(
        "LinkedIn videos with AI presenters",
        B.callout(
            "Two videos for LinkedIn, on top of the eight text and carousel posts: Wednesday Nov 25 and Wednesday Dec 2 at 11 AM New York time. "
            "Each video is about 30 seconds, square, with a different AI-generated presenter who talks to the camera in a B2B tone for property managers and office teams. "
            "They sit on Wednesdays so no existing draft changes, and the posts already scheduled for Nov 10 to Nov 19 are untouched. "
            "The script, video prompts and text are inside weeks 3 and 4.",
            "Format.",
        )
        + B.tiles([
            ("2", "LinkedIn videos, each with its own presenter, script, two video prompts and text", "dato"),
            ("2", "drafts saved in Metricool with the text and no media, until you add the video", "dato"),
            ("30 s", "about, per video: 4 beats and 69 words, in two clips", "dato"),
        ]),
        "Wednesday at 11 AM is the second-strongest slot of the week in Metricool's LinkedIn best-time data. Thursday at 11 AM is the strongest and is already used by the text posts.",
    )
    how = meta_box([
        "**Same process as the TikToks,** with three changes. The format is square 1:1 instead of vertical, the video is about 30 seconds, and it is made in two clips of about 15 seconds that you join in the editor.",
        "**Captions.** Many people watch LinkedIn without sound. Add subtitles in the editor or turn on LinkedIn's captions before scheduling.",
        "**Upload.** Open the Metricool LinkedIn draft, upload the video to it and check that the text and link are intact.",
    ])
    rs += B.section("LinkedIn videos: how they differ from the TikToks", how)
    checks = [
        "**Disclosure.** Both texts end with \"AI-generated video.\" Metricool has no AI label field for LinkedIn, so keep that line.",
        "**The presenter is a host.** The scripts give tips. None says \"I clean units\" or \"our team\", because an invented person cannot speak as an employee or a customer.",
        "**Claims.** The tips are general. No script promises results, timing or certifications.",
        "**Link.** Both texts point to the contact page with LinkedIn tracking tags, and the URL shortener is on, like the other LinkedIn drafts.",
        "**Dates.** Nov 25 is the day before Thanksgiving. Dec 2 follows the Dec 1 year-end calendar post. Tell me if you want either one moved.",
        "**Services.** The scripts mention estimates, photos of the unit and scheduling a clean. Confirm the company offers all of them as written.",
    ]
    rs += B.section("LinkedIn videos: before approving", "<ul class='checks'>" + "".join(f"<li>{fmt(x)}</li>" for x in checks) + "</ul>")
    return rs


def _pkey(p):
    d = TH._date(p)
    return (d.month if d.month >= 11 else d.month + 12, d.day, 11)


def inject(html, brand="kn"):
    """Inserta los videos de LinkedIn en cada semana y en el calendario del Overview, y las secciones al final del Overview."""
    ps = [p for p in L if p["brand"] == brand]
    for n in (1, 2, 3, 4):
        mine = [p for p in ps if TH.week_of(p) == n]
        if not mine:
            continue
        a, b = TH._panel_span(html, f"{brand}-sem{n}")
        seg = html[a:b]
        arts = list(re.finditer(r'<article class="piece">.*?</article>', seg, flags=re.S))
        assert arts, (brand, n)
        for x, y in zip(arts, arts[1:]):
            assert seg[x.end():y.start()] == "", (brand, n, "contenido entre piezas")
        items = []
        for m in arts:
            t = re.search(r"<b>([^<]+)</b><span>([^<]+)</span>", m.group(0))
            items.append((TH._key(t.group(1), t.group(2)), 0, m.group(0)))
        for p in mine:
            items.append((_pkey(p), 1, piece(p)))
        items.sort(key=lambda z: (z[0], z[1]))
        seg = seg[:arts[0].start()] + "".join(z[2] for z in items) + seg[arts[-1].end():]
        html = html[:a] + seg + html[b:]
    a, b = TH._panel_span(html, f"{brand}-resumen")
    seg = html[a:b]
    i = seg.index("<h3>Four-week calendar</h3>")
    ts = seg.index("<tbody>", i) + len("<tbody>")
    te = seg.index("</tbody>", ts)
    rows = list(re.finditer(r"<tr>.*?</tr>", seg[ts:te], flags=re.S))
    items = []
    for m in rows:
        t = re.search(r"<th scope='row'>(\w{3}, \w{3} \d+) · (\d+ [AP]M)</th>", m.group(0))
        items.append((TH._key(t.group(1), t.group(2)), 0, m.group(0)))
    for p in ps:
        items.append((_pkey(p), 1, board_row(p)))
    items.sort(key=lambda z: (z[0], z[1]))
    seg = seg[:ts] + "".join(z[2] for z in items) + seg[te:]
    assert seg.rstrip().endswith("</section>")
    k = seg.rstrip().rfind("</section>")
    seg = seg[:k] + overview_section() + seg[k:]
    return html[:a] + seg + html[b:]


if __name__ == "__main__":
    for p in L:
        print(p["id"], p["date"], len(spoken(p).split()), "words;", "caption chars", len(caption(p)))
        print(caption(p))
        print()
