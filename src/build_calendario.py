#!/usr/bin/env python3
# Builds calendario-contenidos.html (English), reusing styles and scripts from build_estrategia.py
import datetime as dt
import io
import contextlib
import os

os.environ.setdefault("CONTENT_LANG", "en")

with contextlib.redirect_stdout(io.StringIO()):
    import build_estrategia as B

OUT = "calendario-contenidos.html"
e, fmt, chip = B.e, B.fmt, B.chip

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONF = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
START = dt.date(2026, 11, 9)


def D(m, d):
    return dt.date(2026 if m >= 11 else 2027, m, d)


def h12(h):
    """'18:00' -> '6 PM'; '11:30' -> '11:30 AM'."""
    hh, mm = (int(x) for x in h.split(":"))
    suf = "AM" if hh < 12 else "PM"
    h2 = hh % 12 or 12
    return f"{h2} {suf}" if mm == 0 else f"{h2}:{mm:02d} {suf}"


def week_range(n):
    a = START + dt.timedelta(days=7 * (n - 1))
    b = a + dt.timedelta(days=6)
    if a.month == b.month:
        return f"{MONF[a.month-1]} {a.day} to {b.day}"
    return f"{MONF[a.month-1]} {a.day} to {MONF[b.month-1]} {b.day}"


def short_range(n):
    a = START + dt.timedelta(days=7 * (n - 1))
    b = a + dt.timedelta(days=6)
    if a.month == b.month:
        return f"{MON[a.month-1]} {a.day} to {b.day}"
    return f"{MON[a.month-1]} {a.day} to {MON[b.month-1]} {b.day}"


def row(wd, m, d, hour, title, meta, kind, note=""):
    date = D(m, d)
    assert DAYS[date.weekday()] == wd, f"Inconsistent date: {wd} {MON[m-1]} {d} is {DAYS[date.weekday()]}"
    return B.slot(f"{wd} {MON[m-1]} {d}", h12(hour), title, meta, kind, note)


def week_block(n, rows, note=""):
    body = "".join(rows)
    n_html = f'<p class="note">{fmt(note)}</p>' if note else ""
    return (
        f'<h4 class="wkh">Week {n}<span>{e(week_range(n))}</span></h4>'
        f'<ul class="slots">{body}</ul>{n_html}'
    )


def wrow(n, theme, text, key="", phase=""):
    ph = {1: "Base", 2: "Season", 3: "Consolidation"}[1 if n <= 4 else 2 if n <= 8 else 3]
    k = f'<p class="wk">{fmt(key)}</p>' if key else ""
    return (
        '<li class="wrow">'
        f'<div><p class="wn">W{n}</p><p class="wd">{e(short_range(n))}</p></div>'
        f'<div><p class="wt">{fmt(theme)} <span class="ph">{ph}</span></p><p class="wp">{fmt(text)}</p>{k}</div></li>'
    )


def wlist(items):
    return '<ul class="wlist">' + "".join(items) + "</ul>"


section, callout, tagbox, kpis = B.section, B.callout, B.tagbox, B.kpis

import sys as _sys
_sys.path.insert(0, ".")
import tiktok_data as T
import characters as CH

TT_EN = {
    "KG1": "Ají amarillo: the yellow pepper behind Peruvian flavor",
    "KG2": "Green, yellow or black plantain: what each one is for",
    "KG3": "Rice and peas: keep the scotch bonnet whole",
    "KG4": "Is your mango ripe? Skip the color test",
    "KG5": "A new side for the Thanksgiving table",
    "KG6": "How to pick a sweet pineapple",
    "KG7": "How to pick yuca (and never eat it raw)",
    "KG8": "Five products to start cooking Peruvian and Caribbean",
    "KN1": "Myth: more cleaner means cleaner",
    "KN2": "What would you do with your Saturday?",
    "KN3": "Turnover day: the order that saves time",
    "KN4": "Never mix these two cleaners",
    "KN5": "Hosting this week: 15 minutes before guests arrive",
    "KN6": "Four questions to ask a cleaning company",
    "KN7": "Three mistakes that spread dirt",
    "KN8": "Four spots to clean once a month",
}


def tt(pid):
    p = next(x for x in T.P if x["id"] == pid)
    y, m, d = (int(v) for v in p["date"].split("-"))
    wd = DAYS[dt.date(y, m, d).weekday()]
    return row(wd, m, d, "18:00", f"TikTok: {TT_EN[pid]}",
               f"TikTok ({T.HANDLE[p['brand']]}), video of about 18 s" + (f" with {CH.name(p['char'])}, a recurring AI character" if p.get("char") else ", finished video made before the characters"),
               "hip",
               _kn_note(p, "Draft in Metricool with a placeholder photo: upload the video and mark it as AI-generated content. Script and prompt are in the Week 1 to Week 4 tabs of this brand."))


EST_PROG = "Already scheduled in Metricool with its finished media: only a text change is proposed, pending your approval."
EST_BORR = "Draft in Metricool with the previous text: new text is proposed, pending your approval."


def _kn_note(p, base):
    """Note for a TikTok or LinkedIn video: piece type and status; K&G keeps the standard text."""
    if not p.get("type"):
        return base
    tipo = p["type"]
    if p["id"] == "KN1":
        return f"**{tipo}.** Scheduled in Metricool with its finished video (phone reminder, no automatic publishing): only a caption change is proposed, pending your approval."
    return f"**{tipo}.** {base} New script proposed; if the video is already made, it is kept and only the caption changes."


def krow(wd, m, d, hour, title, meta, tipo, extra=""):
    """Klean N Green NYC row: piece type (time-back strategy) and Metricool status."""
    date = D(m, d)
    prog = (date - START).days < 14
    kind = "ref" if tipo == "TB" else "hip"
    nota = f"**{'Time back' if tipo == 'TB' else 'Tip + bridge'}.** " + (EST_PROG if prog else EST_BORR) + (" " + extra if extra else "")
    return row(wd, m, d, hour, title, meta, kind, nota)


import linkedin_video as LV

LI_EN = {
    "LI1": "Video: four details to send before booking a cleaning crew",
    "LI2": "Video: a unit that will sit empty over the holidays: four things to do first",
}


def li(pid):
    p = next(x for x in LV.L if x["id"] == pid)
    y, m, d = (int(v) for v in p["date"].split("-"))
    wd = DAYS[dt.date(y, m, d).weekday()]
    return row(wd, m, d, "11:00", LI_EN[pid],
               f"LinkedIn, square video of about 30 s with {CH.name(p['char'])}, a recurring AI character, B2B",
               "hip",
               _kn_note(p, "Draft in Metricool with the text only (it already includes “AI-generated video.”): upload the video and turn on captions. Script and prompts are in the Week 3 and Week 4 tabs of this brand."))


# ---------------------------------------------------------------------------
# K&G MARKET
# ---------------------------------------------------------------------------
kg = ""
kg += section(
    "Weeks 1 to 4: day by day (New York time)",
    callout(
        "Three posts per week, Saturday stories and two TikToks (Tuesday and Thursday at 6 PM; in week 3, Tuesday and Wednesday because of Thanksgiving). Rosa and Dre, the two recurring AI characters, host the TikToks and the Reels and appear in five single images; the Google posts, the Stories and the team photo have no generated people. Products in brackets are confirmed with the store. Ají amarillo and chicha morada already appear in the account's posts.",
        "Pace.",
    )
    + week_block(
        1,
        [
            row("Mon", 11, 9, "10:00", "Just in: ají amarillo", "Facebook and Instagram, photo", "ref", "Just in. Set “Peruvian product”."),
            tt("KG1"),
            row("Wed", 11, 11, "12:00", "Reel: three ways to use ají amarillo", "Facebook and Instagram, 15 to 30 s Reel", "ref", "How to use it. Set “Peruvian product”."),
            tt("KG2"),
            row("Fri", 11, 13, "10:00", "Who runs the store", "Facebook and Instagram, team photo with their permission", "ref", "People and neighborhood. Set “Local base”."),
            row("Sat", 11, 14, "10:00", "Stories: store open, product of the week and hours", "Instagram and Facebook, 3 stories", "ref", "Useful info."),
        ],
    )
    + week_block(
        2,
        [
            row("Mon", 11, 16, "10:00", "Just in: [Caribbean product]", "Facebook and Instagram, photo", "ref", "Just in. Set “Caribbean product”."),
            tt("KG3"),
            row("Wed", 11, 18, "12:00", "Reel: [Caribbean dish] with ingredients from the store", "Facebook and Instagram, Reel", "ref", "How to use it. Set “Caribbean product”."),
            tt("KG4"),
            row("Fri", 11, 20, "10:00", "Notice: Thanksgiving orders and hours", "Facebook and Instagram, single image", "ref", "Offers and seasonal. Set “Seasonal”."),
            row("Sat", 11, 21, "10:00", "Stories: what's in today and how to order ahead", "Instagram and Facebook, 3 stories", "ref", "Useful info."),
        ],
        "Review 1 on Friday, November 20.",
    )
    + week_block(
        3,
        [
            row("Mon", 11, 23, "10:00", "Thanksgiving: products for your table", "Facebook and Instagram, 3-image carousel", "ref", "Offers and seasonal. Set “Seasonal”."),
            tt("KG5"),
            row("Wed", 11, 25, "12:00", "Reel: [dish] for the Thanksgiving table", "Facebook and Instagram, Reel", "ref", "How to use it. Set “Seasonal”."),
            tt("KG6"),
            row("Fri", 11, 27, "10:00", "Small Business Saturday: come meet us", "Facebook and Instagram, single image", "ref", "People and neighborhood. Set “Local base”."),
            row("Sat", 11, 28, "10:00", "Stories: Small Business Saturday at the store", "Instagram and Facebook, 3 stories", "ref", "People and neighborhood."),
        ],
        "Thursday 26 (Thanksgiving): no fixed post; a greeting story if wanted. Confirm the store's hours for Thursday 26 and Friday 27.",
    )
    + week_block(
        4,
        [
            row("Mon", 11, 30, "10:00", "Just in: [product], restock after Thanksgiving", "Facebook and Instagram, photo", "ref", "Just in. Set “Peruvian product”."),
            tt("KG7"),
            row("Wed", 12, 2, "12:00", "Reel: chicha morada at home, step by step", "Facebook and Instagram, Reel", "ref", "How to use it. Set “Drinks and traditions”."),
            tt("KG8"),
            row("Fri", 12, 4, "10:00", "December at K&G: hours and Christmas orders", "Facebook and Instagram, single image", "ref", "Offers and seasonal. Set “Seasonal”."),
            row("Sat", 12, 5, "10:00", "Stories: store open and product of the week", "Instagram and Facebook, 3 stories", "ref", "Useful info."),
        ],
        "Review 2 on Friday, December 4. Its results shape the detail of weeks 5 to 8.",
    ),
)
kg += section(
    "Weeks 5 to 13: topic of each week",
    callout("From week 5 the two weekly TikToks continue, hosted by Rosa and Dre. Their topics are set at each review, based on what worked.") + wlist(
        [
            wrow(5, "Christmas table, part one", "Product for holiday dishes, a Reel of a Christmas dish and the hours notice.", "Tuesday 8: holiday in Peru."),
            wrow(6, "Christmas orders and hours", "Deadline for advance orders and special hours, product by product.", "Review 3 on Friday, December 18."),
            wrow(7, "Christmas Eve and Christmas", "Two posts plus stories with a greeting and the hours for the 24th and 25th. No fixed post on the 25th.", "Thursday 24 and Friday 25."),
            wrow(8, "Year-end and New Year", "Ideas for the New Year's Eve dinner, a year in store photos and a January 1 greeting.", "Thursday 31 and Friday, January 1."),
            wrow(9, "Three Kings Day and the year's pantry", "Product of the week, a Kings Day post with the available products and a recipe Reel.", "Wednesday 6: Three Kings Day."),
            wrow(10, "Winter dishes", "Broths and stews with ingredients from the store. One Reel per week, or two if it passed the 150-view threshold."),
            wrow(11, "People and neighborhood", "Customers and community recipes with their permission, and the team's story.", "Monday 18: US federal holiday; confirm hours."),
            wrow(12, "Repeat what worked", "The three formats with the most reach from the first two months.", "Review 4 on Friday, January 29."),
            wrow(13, "Bridge to the next quarter", "First pieces of the February to April plan defined at review 4."),
        ]
    ),
)
kg += section(
    "Hashtag sets used in the calendar",
    '<p class="lead-s">Five per post on Instagram and up to three on Facebook.</p>'
    + tagbox("Local base", "#KGMarket #BrooklynEats #BrooklynFood #NYCFood")
    + tagbox("Peruvian product", "#KGMarket #BrooklynEats #PeruvianFood #AjiAmarillo #ComidaPeruana")
    + tagbox("Caribbean product", "#KGMarket #BrooklynEats #CaribbeanFood #CaribbeanCuisine #BrooklynFood")
    + tagbox("Drinks and traditions", "#KGMarket #ChichaMorada #PeruvianFood #NYCFood #BrooklynFood")
    + tagbox("Seasonal", "#KGMarket #ThanksgivingFood #HolidayTable #BrooklynEats #NYCFood"),
)

# ---------------------------------------------------------------------------
# KLEAN N GREEN NYC
# ---------------------------------------------------------------------------
kn = ""
kn += section(
    "Content strategy: time back",
    callout(
        "Hiring Klean N Green NYC gives people time to do what they couldn't before. Each piece either shows what the person can do with that time (about 2 in 3) or is a useful tip that ends with a bridge to the service (1 in 3). None promises hours saved or tells what real clients did with their time.",
        "Core message.",
    )
    + B.tiles(
        [
            ("25 of 38", "pieces show the time back (the mix is about 2 in 3)", "dato"),
            ("13 of 38", "pieces stay as tips and close with a bridge to the service", "dato"),
            ("15", "pieces already scheduled with their media: only the text changes", "dato"),
            ("23", "drafts: new text and, where the idea changed, new scenes, scripts and prompts", "dato"),
        ]
    )
    + callout(
        "Nothing in Metricool has changed. When you approve each piece, it is updated: scheduled posts are edited in place (they keep their time and media) and drafts are replaced with the new text. A piece that is not approved stays as it is.",
        "Approval.",
    ),
)
kn += section(
    "Weeks 1 to 4: day by day (New York time)",
    callout(
        "Full 7-day plan: Monday Google, Tuesday LinkedIn, Wednesday Instagram and Facebook (carousel), Thursday LinkedIn, Friday Reel, Saturday single image on Instagram and Facebook, Sunday Instagram. On top of that, two TikToks per week at 6 PM (Tuesday and Thursday; in week 3, Tuesday and Friday) and two LinkedIn videos, on Wednesday, November 25 and December 2 at 11 AM. Maya and Daniel, the two recurring AI characters, host the TikToks from Nov 12 and the LinkedIn videos, and appear in the Reels of Nov 27, Dec 4 and Dec 6 and in the single images of Nov 28, Nov 29 and Dec 5. Weeks 1 and 2 are already scheduled with their media and keep it; weeks 3 and 4 are drafts.",
        "Pace.",
    )
    + week_block(
        1,
        [
            krow("Mon", 11, 9, "10:00", "Google: what would you do with your Saturday if the cleaning was already done?", "Google Business Profile, post with button", "TB"),
            krow("Tue", 11, 10, "11:00", "Turnover week without chasing crews: the 5 checks", "LinkedIn", "TB"),
            tt("KN1"),
            krow("Wed", 11, 11, "12:00", "Carousel: the kitchen in 6 spots people miss", "Instagram and Facebook, carousel", "TIP", "The bridge goes in the text; optional: a ninth slide."),
            krow("Thu", 11, 12, "11:00", "What office cleaning includes and what it frees up", "LinkedIn", "TB"),
            tt("KN2"),
            krow("Fri", 11, 13, "12:00", "Reel: 3 quick bathroom wipes", "Instagram and Facebook, Reel of about 12 seconds", "TIP", "The bridge goes in the text."),
            krow("Sat", 11, 14, "11:00", "Single image: four details and the rest of your Saturday is yours", "Instagram and Facebook, single image", "TB"),
            krow("Sun", 11, 15, "18:00", "“Sunday reset”: the text opens with the Sunday you get back", "Instagram, carousel", "TB", "The images don't change; optional: a ninth slide."),
        ],
    )
    + week_block(
        2,
        [
            krow("Mon", 11, 16, "10:00", "Google: cleans between tenants or guests, with time for messages and showings", "Google Business Profile, post with button", "TB"),
            krow("Tue", 11, 17, "11:00", "Verifying a unit: you get photos and sign-off without walking it", "LinkedIn", "TB"),
            tt("KN3"),
            krow("Wed", 11, 18, "12:00", "Single image: guests on their way and the home is already ready", "Instagram and Facebook, single image", "TB"),
            krow("Thu", 11, 19, "11:00", "Real client review, word for word", "LinkedIn", "TB", "Only the line that frames the review changes."),
            tt("KN4"),
            krow("Fri", 11, 20, "12:00", "Reel: window tracks, the spot nobody cleans", "Instagram and Facebook, Reel of about 12 seconds", "TIP", "The bridge goes in the text."),
            krow("Sat", 11, 21, "11:00", "Single image: how often to clean? Start from the weekend you want", "Instagram and Facebook, single image", "TB"),
            krow("Sun", 11, 22, "18:00", "Entryway: coming home with everything done", "Instagram, carousel", "TB", "The images don't change; optional: an eighth slide."),
        ],
        "Review 1 on Friday, November 20: compare the Friday Reels with the Wednesday carousels.",
    )
    + week_block(
        3,
        [
            krow("Mon", 11, 23, "10:00", "Google: the team closes the year, not the cleaning list", "Google Business Profile, post with button", "TB"),
            krow("Tue", 11, 24, "11:00", "Office checklist before the year-end close, with a bridge", "LinkedIn, PDF carousel", "TIP"),
            tt("KN5"),
            li("LI1"),
            krow("Wed", 11, 25, "12:00", "Carousel: after dinner, the kitchen in 30 minutes", "Instagram and Facebook, carousel", "TIP"),
            krow("Thu", 11, 26, "11:00", "Thanksgiving: a short thank-you, a day with nothing else on the list", "LinkedIn and Facebook", "TB"),
            krow("Fri", 11, 27, "12:00", "Reel: guests leave and the afternoon is yours", "Instagram and Facebook, Reel of about 12 seconds", "TB"),
            tt("KN6"),
            krow("Sat", 11, 28, "11:00", "Single image: guests in December? The visit, not the prep", "Instagram and Facebook, single image", "TB"),
            krow("Sun", 11, 29, "18:00", "Single image: the Sunday after the long weekend is yours", "Instagram, single image", "TB"),
        ],
        "Thursday 26 is Thanksgiving: only the short thank-you goes out on LinkedIn and Facebook, with no TikTok. On Friday 27 the pace returns with the Reel.",
    )
    + week_block(
        4,
        [
            krow("Mon", 11, 30, "10:00", "Google: recurring home cleaning, weekends you can plan", "Google Business Profile, post with button", "TB"),
            krow("Tue", 12, 1, "11:00", "Property managers: a year-end calendar with the cleaning off their list", "LinkedIn", "TB"),
            tt("KN7"),
            li("LI2"),
            krow("Wed", 12, 2, "12:00", "Before and after of a real job: our time on site, yours untouched", "Instagram and Facebook, 6-image carousel", "TB", "Requires real photos and client authorization."),
            krow("Thu", 12, 3, "11:00", "What cleaning for property management includes and what it gives back", "LinkedIn, PDF carousel", "TB"),
            tt("KN8"),
            krow("Fri", 12, 4, "12:00", "Reel: the spots everyone touches, before the visits, with a bridge", "Instagram and Facebook, Reel of about 12 seconds", "TIP"),
            krow("Sat", 12, 5, "11:00", "Single image: the January weekends you wanted", "Instagram and Facebook, single image", "TB"),
            krow("Sun", 12, 6, "18:00", "Reel: the winter entryway already handled and the evening yours", "Instagram, Reel of about 12 seconds", "TB"),
        ],
        "Review 2 on Friday, December 4. Its results shape the detail of weeks 5 to 8.",
    ),
)
kn += section(
    "Weeks 5 to 13: topic of each week",
    callout("From week 5 the Friday Reel and the Saturday single image continue. Their topics are set at each review, based on what worked. The two weekly TikToks continue, hosted by Maya and Daniel.") + wlist(
        [
            wrow(5, "Before and after the holidays", "Checklist for hosting guests and a next-day checklist for homes; on LinkedIn, the office in the last week of the year."),
            wrow(6, "Year-end for offices and buildings", "Deep clean before the break and an invitation to book January dates with a single action: request an estimate.", "Review 3 on Friday, December 18."),
            wrow(7, "Low week", "Two pieces: LinkedIn on Tuesday 22 with a thank-you and year-end hours, and Instagram on Sunday 27 with a post-holiday “Sunday reset”.", "No post on Thursday 24 or Friday 25."),
            wrow(8, "New year reset", "LinkedIn on Tuesday 29: the office ready before the team returns. Instagram on Wednesday 30 and Sunday, January 3: “New year reset” for homes.", "Thursday 31 and Friday, January 1."),
            wrow(9, "Back to the office", "Two LinkedIn posts (Tuesday 5 and Thursday 7), Instagram and Facebook on Wednesday 6 and Instagram on Sunday 10."),
            wrow(10, "Social proof", "Reviews and real jobs with authorization, on LinkedIn and Instagram."),
            wrow(11, "Education for property managers", "Quarterly upkeep of units and common areas, in three steps.", "Monday 18: US federal holiday; offices closed. Post on Tuesday 19."),
            wrow(12, "Repeat what worked", "The formats and topics with the most impressions from the first two months, in a new version.", "Review 4 on Friday, January 29."),
            wrow(13, "Bridge to the next quarter", "First pieces of the February to April plan, with spring-cleaning prep."),
        ]
    ),
)
kn += section(
    "Blog on kleannyc.com",
    callout(
        "The site's blog exists but has stalled. It restarts with one article every two weeks, each on a single concrete search and with a closing button to request an estimate. LinkedIn posts link to the article instead of the contact page when there is a related one. The effect on Google takes months and is not guaranteed.",
        "Proposal.",
    )
    + '<div class="tablewrap"><table class="rev"><thead><tr><th>Publish</th><th>Article</th><th>Linked from</th></tr></thead><tbody>'
    "<tr><th scope='row'>Fri Nov 20 (W2)</th><td>Office checklist before the year-end close</td><td>LinkedIn, Tuesday, November 24</td></tr>"
    "<tr><th scope='row'>Wed Dec 2 (W4)</th><td>What cleaning for property management includes</td><td>LinkedIn, Thursday, December 3</td></tr>"
    "<tr><th scope='row'>Week 6</th><td>How a unit is verified before handover</td><td>LinkedIn and Google</td></tr>"
    "<tr><th scope='row'>Week 8</th><td>Turnover checklist for property managers</td><td>LinkedIn</td></tr>"
    "</tbody></table></div>"
    '<p class="note">The LinkedIn drafts for November 24 and December 3 currently point to the contact page with UTM parameters. If the article is published in time, the link is changed; if not, they stay as they are.</p>'
    '<ul class="rules">'
    "<li><b>Site status (Nov 9).</b> Done: /dtut/ and /new-clients/ are now noindex, so they no longer compete with the main pages. The robots.txt lines without a User-agent are ignored by Google and block nothing, so they were left as they are. Every service page has its own title, description and a single H1, and the old addresses (/air-bnb/, /commercial-cleaning-nyc/, /residential-cleaning-nyc/, /post-construction-cleaning-nyc/) redirect with a 301. <b>Still open:</b> /post-renovation-cleaning/ repeats the full text of /post-construction-cleaning/. Decide whether to rewrite one, redirect one or mark one as canonical before linking articles to either.</li>"
    "<li><b>Each article.</b> A single question, a clear title, a featured image and the closing button to request an estimate with UTM parameters.</li></ul>",
)
kn += section(
    "Featured images for the site",
    callout(
        "One realistic image per page, in 1.91:1 horizontal format and without text. It serves as the featured image and as the preview card on LinkedIn, Facebook and Google. The prompts are in the file klean-nyc-imagenes-web.html. They are generated, illustrative images: replace them with real photos of the team or a job when they exist.",
        "What it is.",
    )
    + '<div class="tablewrap"><table class="rev"><thead><tr><th>Before</th><th>Image</th><th>Suggested file</th></tr></thead><tbody>'
    "<tr><th scope='row'>Mon Nov 9</th><td>Contact, destination of the Google buttons and of the LinkedIn and Facebook links</td><td>klean-nyc-contact.jpg</td></tr>"
    "<tr><th scope='row'>Mon Nov 16</th><td>Vacation rentals, destination of the Google button</td><td>klean-nyc-vacation-rental-cleaning.jpg</td></tr>"
    "<tr><th scope='row'>Week 1</th><td>Home</td><td>klean-nyc-home.jpg</td></tr>"
    "<tr><th scope='row'>Week 2</th><td>Residential cleaning, offices, property management and post-construction (the pages that exist)</td><td>klean-nyc-residential-cleaning.jpg and the others</td></tr>"
    "<tr><th scope='row'>Before the first article</th><td>Blog index</td><td>klean-nyc-blog.jpg</td></tr>"
    "</tbody></table></div>",
)
kn += section(
    "Hashtag sets used in the calendar",
    '<p class="lead-s">Three on LinkedIn, five on Instagram and up to three on Facebook.</p>'
    + tagbox("LinkedIn, property management", "#NYCCleaning #PropertyManagement #CommercialCleaning")
    + tagbox("LinkedIn, offices", "#NYCCleaning #OfficeCleaning #FacilitiesManagement")
    + tagbox("Instagram, homes", "#NYCCleaning #ResidentialCleaning #CleaningTips #ApartmentCleaning #SundayReset")
    + tagbox("Instagram, Reels", "#NYCCleaning #CleaningTips #ApartmentCleaning #SatisfyingClean #CleaningReel")
    + tagbox("Instagram, Saturdays", "#NYCCleaning #ResidentialCleaning #CleaningService #ApartmentCleaning #NYCHome")
    + tagbox("Facebook", "#NYCCleaning #ResidentialCleaning #CleaningTips"),
)

# ---------------------------------------------------------------------------
# JDET CAPITAL
# ---------------------------------------------------------------------------
jd = ""
jd += section(
    "Weeks 1 to 4: day by day (New York time)",
    callout(
        "If the four definitions are not settled by Friday, November 13, the whole calendar shifts one week. Topics in brackets are filled in once the activity is confirmed.",
        "Condition.",
    )
    + '<h4 class="wkh">Week 1<span>' + e(week_range(1)) + "</span></h4>"
    + '<p class="note">No posts. Settle the four definitions (what it offers and to whom, where the audience is reached, who speaks and what limits the texts have) and complete the profile on Friday 13.</p>'
    + week_block(
        2,
        [
            row("Tue", 11, 17, "11:00", "Industry perspective #1", "LinkedIn", "ref", "Industry perspective."),
            row("Thu", 11, 19, "11:00", "How we work #1", "LinkedIn", "ref", "How we work."),
        ],
        "Review 1 on Friday, November 20.",
    )
    + week_block(
        3,
        [
            row("Tue", 11, 24, "11:00", "FAQ #1", "LinkedIn", "ref", "Frequently asked questions."),
            row("Wed", 11, 25, "11:00", "Industry perspective #2", "LinkedIn", "ref", "Moved up to Wednesday because of Thanksgiving. In the Metricool reference, Wednesday at 11 AM beats Tuesday."),
        ],
    )
    + week_block(
        4,
        [
            row("Tue", 12, 1, "11:00", "How we work #2", "LinkedIn", "ref", "How we work."),
            row("Thu", 12, 3, "11:00", "Team: introducing [person]", "LinkedIn", "ref", "Team."),
        ],
        "Review 2 on Friday, December 4.",
    ),
)
jd += section(
    "Weeks 5 to 13: topic of each week",
    wlist(
        [
            wrow(5, "Perspective and FAQs", "Tuesday: industry perspective. Thursday: FAQ."),
            wrow(6, "How we work and team", "Tuesday: process. Thursday: team.", "Review 3 on Friday, December 18."),
            wrow(7, "Low week", "One post on Tuesday 22 with a year-end greeting.", "No post on Thursday 24 or Friday 25."),
            wrow(8, "Looking at the new year", "One post on Tuesday 29 about what to watch in 2027, without promising results.", "Thursday 31 and Friday, January 1."),
            wrow(9, "Back to the pace", "Tuesday 5: industry perspective. Thursday 7: FAQ."),
            wrow(10, "How we work and team", "Tuesday: process. Thursday: team."),
            wrow(11, "Perspective and FAQs", "Tuesday 19: perspective. Thursday 21: FAQ.", "Monday 18: US federal holiday."),
            wrow(12, "Repeat what worked", "The topics with the most impressions, in a new version.", "Review 4 on Friday, January 29."),
            wrow(13, "Bridge to the next quarter", "First pieces of the February to April plan."),
        ]
    ),
)

# ---------------------------------------------------------------------------
# KLEAN N GREEN PERU
# ---------------------------------------------------------------------------
pe = ""
pe += section(
    "Weeks 1 to 4: day by day (Lima time)",
    callout(
        "All times are hypotheses and are replaced by the account's best time once there is data. If the network is not connected by November 20, posting shifts one week.",
        "Condition.",
    )
    + '<h4 class="wkh">Week 1<span>' + e(week_range(1)) + "</span></h4>"
    + '<p class="note">No posts. Settle the four prior decisions (brand, starting segment, starting network and services with service areas) on Friday 13.</p>'
    + '<h4 class="wkh">Week 2<span>' + e(week_range(2)) + "</span></h4>"
    + '<p class="note">No posts. Create and complete the Instagram profile and the Google Business Profile, and connect Instagram to Metricool. Review 1 on Friday, November 20.</p>'
    + week_block(
        3,
        [
            row("Mon", 11, 23, "12:00", "Service introduction: what it includes and in which areas", "Instagram, carousel", "hip", "Service introduction."),
            row("Wed", 11, 25, "19:00", "Cleaning guide: [topic]", "Instagram, carousel", "hip", "Cleaning guides."),
            row("Fri", 11, 27, "12:00", "Before and after, or a review if there are no publishable jobs yet", "Instagram, carousel or single image", "hip", "Before and after or reviews."),
        ],
    )
    + week_block(
        4,
        [
            row("Mon", 11, 30, "12:00", "Services by client type", "Instagram, carousel", "hip", "Service introduction."),
            row("Wed", 12, 2, "19:00", "Cleaning guide: [topic 2]", "Instagram, Reel or carousel", "hip", "Cleaning guides."),
            row("Fri", 12, 4, "12:00", "Before and after, or a review", "Instagram, carousel or single image", "hip", "Before and after or reviews."),
        ],
        "Review 2 on Friday, December 4.",
    ),
)
pe += section(
    "Weeks 5 to 13: topic of each week",
    wlist(
        [
            wrow(5, "Home ready for the holidays", "Checklist for hosting visitors at Christmas and New Year.", "Tuesday 8: holiday in Peru (it doesn't fall on a Monday, Wednesday or Friday)."),
            wrow(6, "Offices: year-end", "Cleaning before the break and an invitation to book January dates.", "Review 3 on Friday, December 18."),
            wrow(7, "Christmas", "Two posts (Monday 21 and Wednesday 23) with a greeting and hours.", "No post on Friday 25."),
            wrow(8, "New Year", "Monday 28 and Wednesday 30: post-holiday checklist and greeting.", "No post on Friday, January 1."),
            wrow(9, "Summer: back from vacation", "Cleaning homes and offices after the break, in three steps."),
            wrow(10, "Before and after", "Real jobs with authorization."),
            wrow(11, "Reviews", "Exact text of each review, with permission."),
            wrow(12, "Repeat what worked", "The formats with the most reach from the first weeks of data.", "Review 4 on Friday, January 29."),
            wrow(13, "Bridge to the next quarter", "First pieces of the February to April plan."),
        ]
    ),
)

# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------
rs = ""
rs += section(
    "How it is built",
    callout(
        "The first four weeks are detailed day by day because there is already starting data. The other nine are planned by topic. At each review Metricool is checked, compared against the baseline, and the next block is detailed. Planning all 13 weeks piece by piece would get ahead of data that doesn't exist yet.",
    )
    + '<div class="cards">'
    '<article class="card"><h4>Base · weeks 1 to 4</h4><p>November 9 to December 6. Set the pace, organize each brand\'s identity and measure. Includes Thanksgiving.</p></article>'
    '<article class="card"><h4>Season · weeks 5 to 8</h4><p>December 7 to January 3. Christmas, year-end and New Year, with one low week.</p></article>'
    '<article class="card"><h4>Consolidation · weeks 9 to 13</h4><p>January 4 to February 7. Repeat what worked and prepare the next quarter.</p></article>'
    "</div>",
)
rs += section(
    "The 13 weeks",
    wlist(
        [
            wrow(1, "First week of posting", "K&G Market and Klean N Green NYC start. JDET Capital and Klean N Green Peru settle their definitions."),
            wrow(2, "First signals", "JDET Capital starts on LinkedIn and the Klean N Green Peru profile comes in.", "Review 1 on Friday, November 20."),
            wrow(3, "Thanksgiving", "Short week for Klean N Green NYC and JDET Capital. Klean N Green Peru starts posting.", "Thursday 26 Thanksgiving, Friday 27 Black Friday, Saturday 28 Small Business Saturday."),
            wrow(4, "Close of the base", "Four weeks against the baseline.", "Review 2 on Friday, December 4."),
            wrow(5, "Christmas table and holidays", "Seasonal content on all four brands.", "Tuesday 8: holiday in Peru."),
            wrow(6, "Orders and year-end", "Order deadlines and January bookings.", "Review 3 on Friday, December 18."),
            wrow(7, "Low week", "Fewer pieces and more stories with greetings and hours.", "Thursday 24 and Friday 25."),
            wrow(8, "New Year", "New-year reset and a look at 2027.", "Thursday 31 and Friday, January 1."),
            wrow(9, "Back to the pace", "Resume the full pace.", "Wednesday 6: Three Kings Day (K&G Market)."),
            wrow(10, "Winter dishes and social proof", "Winter content and reviews."),
            wrow(11, "People, neighborhood and education", "Community at K&G Market and education for property managers at Klean N Green NYC.", "Monday 18: US federal holiday."),
            wrow(12, "Repeat what worked", "Formats and topics with the most reach.", "Review 4 on Friday, January 29."),
            wrow(13, "Bridge to the next quarter", "First pieces of the February to April plan."),
        ]
    ),
)
rev = [
    ("Fri Nov 20", "Pace compliance, impressions per post and first readings on format and time.", "Adjust times. Keep the plan or drop to the minimum."),
    ("Fri Dec 4", "Four weeks against the baseline: followers, impressions, Reel, Google clicks and LinkedIn.", "Result of the Instagram window, formats to repeat and the detail of weeks 5 to 8."),
    ("Fri Dec 18", "Holiday season: reach and messages.", "January detail (weeks 9 to 12) and the pace of the low week."),
    ("Fri Jan 29", "Full quarter against the proposed targets.", "February to April plan."),
]
rev_rows = "".join(
    f"<tr><th scope='row'>{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in rev
)
rs += section(
    "Review points",
    '<div class="tablewrap"><table class="rev"><thead><tr><th>Date</th><th>What is reviewed</th><th>What is decided</th></tr></thead>'
    f"<tbody>{rev_rows}</tbody></table></div>"
    '<p class="note">On each date it is enough to ask for the review: Metricool data is checked and this calendar is updated.</p>',
)
rs += section(
    "Adjustment rules",
    '<p class="lead-s">Proposed thresholds, to confirm with the first data.</p>'
    '<ul class="rules">'
    "<li><b>K&amp;G Market Reel.</b> If it exceeds 150 views two weeks in a row, go from one Reel to two per week.</li>"
    "<li><b>Klean N Green NYC Reels.</b> At review 1 they are compared with the Wednesday carousels. If they have less reach, Friday becomes a single image.</li>"
    "<li><b>Instagram time.</b> If the 6 PM to 8 PM window beats the 10 AM to 12 PM window in impressions for two weeks, move Instagram to the evening.</li>"
    "<li><b>LinkedIn doing well.</b> If a post exceeds 50 impressions, repeat the topic in another format over the next two weeks.</li>"
    "<li><b>LinkedIn with low reach.</b> If it stays under 15 impressions per post after four weeks, strengthen connections and shares from personal profiles before increasing the pace.</li>"
    "<li><b>TikTok.</b> The accounts are new and there is no data of their own: the Tuesday and Thursday 6 PM times come from Metricool's general reference. At review 1, views and full plays are compared between Tuesday and Thursday and between topics; the type of topic that beats the others is repeated and the time is moved if another slot performs better.</li>"
    "<li><b>Team capacity.</b> If less than 80% of what is scheduled is met two weeks in a row, go back to the minimum plan.</li></ul>",
)
dates = [
    ("Thu Nov 26", "Thanksgiving", "All", "K&G Market with special hours. Klean N Green NYC only posts a short thank-you on LinkedIn and Facebook; JDET Capital doesn't post that day."),
    ("Fri Nov 27 and Sat Nov 28", "Black Friday and Small Business Saturday", "K&G Market", "Post and stories about local commerce."),
    ("Tue Dec 8", "Immaculate Conception (holiday in Peru)", "Klean N Green Peru", "Doesn't fall on a posting day."),
    ("Thu Dec 24 and Fri Dec 25", "Christmas Eve and Christmas", "All", "Greeting in stories. No fixed post on the 25th."),
    ("Thu Dec 31 and Fri Jan 1", "Year-end and New Year", "All", "Greeting and hours. No fixed post on the 1st."),
    ("Wed Jan 6", "Three Kings Day", "K&G Market", "Post with the available products, if applicable."),
    ("Mon Jan 18", "Martin Luther King Jr. Day (federal holiday)", "Klean N Green NYC and JDET Capital", "Offices closed. Post on Tuesday 19."),
]
dr = "".join(
    f"<tr><th scope='row'>{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>"
    for a, b, c, d in dates
)
rs += section(
    "Key dates",
    '<div class="tablewrap"><table class="rev wide"><thead><tr><th>Date</th><th>What</th><th>Brands</th><th>What to do</th></tr></thead>'
    f"<tbody>{dr}</tbody></table></div>",
)

# ---------------------------------------------------------------------------
# ASSEMBLY
# ---------------------------------------------------------------------------
BRANDS = B.BRANDS
tabs = "".join(
    f'<button type="button" role="tab" id="tab-{i}" class="tab {c}" aria-controls="panel-{i}" '
    f'aria-selected="{"true" if k == 0 else "false"}" data-tab="{i}"><i class="dot"></i>{e(n)}</button>'
    for k, (i, c, n) in enumerate(BRANDS)
)

panels = ""
panels += B.panel("resumen", "b-all", "Summary", "Phases, weeks, reviews, adjustment rules and key dates for the four brands.", rs)
panels += B.panel("kg-market", "b-kg", "K&G Market", "Peruvian and Caribbean products in Brooklyn.", kg, True)
panels += B.panel("klean-nyc", "b-klean", "Klean N Green NYC", "Cleaning services for homes, offices and property management in New York.", kn, True)
panels += B.panel("jdet-capital", "b-jdet", "JDET Capital", "Provisional calendar until the activity and audience are defined.", jd, True)
panels += B.panel("klean-peru", "b-peru", "Klean N Green Peru", "Provisional calendar until the first network is connected.", pe, True)

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
<p class="eyebrow">13 weeks: November 9, 2026 to February 7, 2027</p>
<h1>3-month content calendar</h1>
<p class="lead">Four weeks detailed day by day and nine weeks by topic for K&amp;G Market, Klean N Green NYC, JDET Capital and Klean N Green Peru. Four reviews with Metricool data adjust what follows.</p>
</header>"""

FOOT = """<footer>
<div class="fnt">
<p><b>How to use it.</b> Times are New York time, except those of Klean N Green Peru, which are Lima time. The Reference and Hypothesis labels have the same meaning as on the strategy page. The text of each post and the hashtag sets are adapted from that page.</p>
<p>Items in brackets are filled in with real information from each business. Except for ají amarillo and chicha morada, which already appear in the account's posts, products and dishes are confirmed with the store.</p>
<p>Weeks 5 to 13 are detailed day by day at each review. JDET Capital and Klean N Green Peru depend on the week 1 definitions, and their dates shift if they are not settled.</p>
</div>
</footer>"""

DOC = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Content Calendar</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{B.FONTS}" rel="stylesheet">
<style>{B.CSS}{EXTRA_CSS}</style>
</head>
<body>
{TOP}
<nav class="tabs" id="tabs"><div class="tablist" role="tablist" aria-label="Brands">{tabs}</div></nav>
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
