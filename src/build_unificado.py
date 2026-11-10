#!/usr/bin/env python3
# Joins the calendar (4 brands) and the posts pack (2 brands) into a single English HTML.
# Structure: brand tabs on top; inside each brand, inner tabs.
#   Summary | K&G Market | Klean NYC | JDET Capital | Klean Peru
#   K&G Market and Klean NYC: Calendar, Overview, Week 1 to 4. JDET and Peru: Calendar only.
import os
import re

os.environ.setdefault("CONTENT_LANG", "en")

CAL = "calendario-contenidos.html"
PACK = "publicaciones-marcas-sem1-4.html"
OUT = "contenidos-por-marca.html"

cal = open(CAL, encoding="utf-8").read()
pack = open(PACK, encoding="utf-8").read()

OPEN = '<section role="tabpanel" id="panel-'


def panels(html, stops):
    """Returns {id: (brand_class, inner_content)} for every tab panel."""
    out = {}
    starts = [m.start() for m in re.finditer(re.escape(OPEN), html)]
    for i, a in enumerate(starts):
        m = re.match(r'<section role="tabpanel" id="panel-([^"]+)" class="panel (b-[a-z]+)" aria-labelledby="[^"]+"( hidden)?>', html[a:])
        pid, bcls = m.group(1), m.group(2)
        body_start = a + m.end()
        nxt = [s for s in starts if s > a]
        limit = nxt[0] if nxt else len(html)
        for stop in stops:
            k = html.find(stop, body_start)
            if k != -1:
                limit = min(limit, k)
        seg = html[body_start:limit]
        end = seg.rfind("</section>")
        assert end != -1, pid
        rest = re.sub(r"\s+", "", seg[end + len("</section>"):])
        assert re.fullmatch(r"(</div>)*", rest), (pid, rest[:80])
        out[pid] = (bcls, seg[:end])
    return out


cp = panels(cal, ["</main>", "<footer"])
pp = panels(pack, ['<div class="brandpane"', "<footer"])
assert set(cp) == {"resumen", "kg-market", "klean-nyc", "jdet-capital", "klean-peru"}, set(cp)
assert {k for k in pp} == {f"{b}-{t}" for b in ("kg", "kn") for t in ("resumen", "sem1", "sem2", "sem3", "sem4")}, set(pp)

# The calendar's Copy buttons use cbNNN ids that clash with the pack's: they get an extra "c" prefix.
def reid(s):
    return re.sub(r'\bcb(\d+)\b', r'ccb\1', s)


# brand -> (brand tab label, color class, [(inner id, label, class, content)])
BR = {}
BR["res"] = ("Summary", "b-all", [("cal", "Summary", "b-all", reid(cp["resumen"][1]))])
BR["kg"] = ("K&amp;G Market", "b-kg", [("cal", "Calendar", "b-kg", reid(cp["kg-market"][1]))]
            + [(t, lab, "b-kg", pp[f"kg-{t}"][1]) for t, lab in
               (("resumen", "Overview"), ("sem1", "Week 1"), ("sem2", "Week 2"), ("sem3", "Week 3"), ("sem4", "Week 4"))])
BR["kn"] = ("Klean NYC", "b-klean", [("cal", "Calendar", "b-klean", reid(cp["klean-nyc"][1]))]
            + [(t, lab, "b-klean", pp[f"kn-{t}"][1]) for t, lab in
               (("resumen", "Overview"), ("sem1", "Week 1"), ("sem2", "Week 2"), ("sem3", "Week 3"), ("sem4", "Week 4"))])
BR["jd"] = ("JDET Capital", "b-jdet", [("cal", "Calendar", "b-jdet", reid(cp["jdet-capital"][1]))])
BR["kp"] = ("Klean Peru", "b-peru", [("cal", "Calendar", "b-peru", reid(cp["klean-peru"][1]))])
ORDER = ["res", "kg", "kn", "jd", "kp"]
FIRST = "cal"

# ------------------------------------------------------------------ header, CSS and JS
head = pack[:pack.index("<body")]
css_pack = re.search(r"<style>(.*?)</style>", pack, re.S).group(1)
css_cal = re.search(r"<style>(.*?)</style>", cal, re.S).group(1)


def rules(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, depth, cur = [], 0, ""
    for ch in css:
        cur += ch
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                out.append(cur.strip())
                cur = ""
    return out


known = {re.sub(r"\s+", " ", r) for r in rules(css_pack)}
extra = [r for r in rules(css_cal) if re.sub(r"\s+", " ", r) not in known]
assert 5 <= len(extra) <= 30, len(extra)
OVERRIDES = """
/* Unification: brand bar with horizontal scrolling (there are five brands) */
.brandlist{overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.brandlist::-webkit-scrollbar{display:none}
.btab{flex:0 0 auto;white-space:nowrap}
.btab.b-all .dot{background:var(--muted)}
"""
css = css_pack + "\n/* Calendar rules */\n" + "\n".join(extra) + "\n" + OVERRIDES
head = head.replace(css_pack, css)
head = re.sub(r"<title>.*?</title>", "<title>Content by brand: calendar and posts</title>", head, flags=re.S)
head = head.replace('<meta name="viewport" content="width=device-width, initial-scale=1">', '<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="robots" content="noindex, nofollow">', 1)
assert 'lang="en"' in head and "Content by brand" in head and "Calendar rules" in head

JS = """
(function(){
  var BR=%(br)s;
  var ORDER=%(order)s;
  var FIRST='cal';
  var bar=document.getElementById('brands');
  var state={brand:'res'};
  ORDER.forEach(function(b){state[b]=FIRST;});
  function showBrand(b){
    ORDER.forEach(function(k){
      var p=document.getElementById('brand-'+k),t=document.getElementById('btab-'+k),on=(k===b);
      p.hidden=!on;
      t.setAttribute('aria-selected',on?'true':'false');
      t.tabIndex=on?0:-1;
      if(on){try{t.scrollIntoView({inline:'center',block:'nearest'});}catch(e){}}
    });
    state.brand=b;
  }
  function showTab(b,id,scroll){
    if(BR[b].indexOf(id)<0){id=FIRST;}
    BR[b].forEach(function(k){
      var p=document.getElementById('panel-'+b+'-'+k),t=document.getElementById('tab-'+b+'-'+k),on=(k===id);
      p.hidden=!on;
      if(t){
        t.setAttribute('aria-selected',on?'true':'false');
        t.tabIndex=on?0:-1;
        if(on){try{t.scrollIntoView({inline:'center',block:'nearest'});}catch(e){}}
      }
    });
    state[b]=id;
    if(scroll){try{
      var nav=document.getElementById('tabs-'+b);
      var top=document.getElementById('panel-'+b+'-'+id).getBoundingClientRect().top+window.pageYOffset-bar.offsetHeight-(nav?nav.offsetHeight:0)-4;
      window.scrollTo(0,Math.max(0,top));
    }catch(e){}}
  }
  function hashOf(b,id){return b+(id===FIRST?'':'-'+id);}
  function apply(scroll){
    var m=/^(res|kg|kn|jd|kp)(?:-(.+))?$/.exec((location.hash||'').replace('#',''));
    var b=m?m[1]:state.brand,id=m&&m[2]?m[2]:(m?FIRST:state[b]);
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
      if(ev.key==='ArrowRight'){j=(i+1)%%bt.length;}
      if(ev.key==='ArrowLeft'){j=(i-1+bt.length)%%bt.length;}
      if(j>=0){ev.preventDefault();bt[j].focus();bt[j].click();}
    });
  });
  ORDER.forEach(function(b){
    var tl=document.querySelectorAll('#tabs-'+b+' .tab');
    Array.prototype.forEach.call(tl,function(t,i){
      t.addEventListener('click',function(){
        var id=t.getAttribute('data-tab');
        showTab(b,id,true);
        try{location.hash=hashOf(b,id);}catch(e){}
      });
      t.addEventListener('keydown',function(ev){
        var j=-1;
        if(ev.key==='ArrowRight'){j=(i+1)%%tl.length;}
        if(ev.key==='ArrowLeft'){j=(i-1+tl.length)%%tl.length;}
        if(j>=0){ev.preventDefault();tl[j].focus();tl[j].click();}
      });
    });
  });
  window.addEventListener('hashchange',function(){apply(false);});
  apply(false);

  document.addEventListener('click',function(ev){
    var btn=ev.target.closest?ev.target.closest('[data-copy]'):null;
    if(!btn){return;}
    var src=document.getElementById(btn.getAttribute('data-copy'));
    if(!src){return;}
    var text=src.textContent;
    var label=btn.getAttribute('data-label')||btn.textContent;
    btn.setAttribute('data-label',label);
    function done(ok){
      btn.textContent=ok?'Copied':'Select and copy';
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
import json
js = JS % {
    "br": json.dumps({b: [t[0] for t in BR[b][2]] for b in ORDER}),
    "order": json.dumps(ORDER),
}

# ------------------------------------------------------------------ body
body = []
body.append('<body>\n<header class="top">\n'
            '<p class="eyebrow">November 9, 2026 to February 7, 2027</p>\n'
            '<h1>Content by brand</h1>\n'
            '<p class="lead">One tab per brand. For K&amp;G Market and Klean NYC, “Calendar” is the 3-month plan, and '
            '“Overview” and “Week 1” to “Week 4” are the 4 weeks of posts ready to copy, with scripts, prompts and TikToks. '
            'JDET Capital and Klean Peru have their calendar.</p>\n</header>')
body.append('<nav class="brands" id="brands"><div class="brandlist" role="tablist" aria-label="Brands">')
for i, b in enumerate(ORDER):
    lab, bcls, _ = BR[b]
    body.append(f'<button type="button" role="tab" id="btab-{b}" class="btab {bcls}" aria-controls="brand-{b}" '
                f'aria-selected="{"true" if i == 0 else "false"}" data-brand="{b}"><i class="dot"></i>{lab}</button>')
body.append('</div></nav>')
for i, b in enumerate(ORDER):
    lab, bcls, tabs = BR[b]
    hid = "" if i == 0 else " hidden"
    body.append(f'<div class="brandpane" id="brand-{b}" role="tabpanel" aria-labelledby="btab-{b}"{hid}>')
    if len(tabs) > 1:
        body.append(f'<nav class="tabs" id="tabs-{b}"><div class="tablist" role="tablist" aria-label="{lab} sections">')
        for j, (tid, tlab, tcls, _) in enumerate(tabs):
            body.append(f'<button type="button" role="tab" id="tab-{b}-{tid}" class="tab {tcls}" aria-controls="panel-{b}-{tid}" '
                        f'aria-selected="{"true" if j == 0 else "false"}" data-tab="{tid}"><i class="dot"></i>{tlab}</button>')
        body.append('</div></nav>')
    body.append('<div class="main">')
    for j, (tid, tlab, tcls, content) in enumerate(tabs):
        hid2 = "" if j == 0 else " hidden"
        labelled = f"tab-{b}-{tid}" if len(tabs) > 1 else f"btab-{b}"
        body.append(f'<section role="tabpanel" id="panel-{b}-{tid}" class="panel {tcls}" aria-labelledby="{labelled}"{hid2}>{content}</section>')
    body.append('</div>\n</div>')
body.append('<footer>\n<div class="fnt">\n'
            '<p><b>How to use it.</b> Pick the brand at the top, then a tab. The “Copy” buttons copy the text of each box. '
            'Times are New York time, except those of Klean Peru, which are Lima time.</p>\n'
            '<p>The Reference and Hypothesis labels have the same meaning as on the strategy page. Items in brackets are filled in with real information from each business. '
            'Except for ají amarillo and chicha morada, which already appear in the account\'s posts, products and dishes are confirmed with the store.</p>\n'
            '<p>The posts come from each brand\'s strategy and calendar. What depends on the business is under “Before approving” in each Overview. '
            'Weeks 5 to 13 are detailed day by day at each review. JDET Capital and Klean Peru depend on the week 1 definitions. '
            'Nothing is published without approval. K&amp;G Market captions are bilingual (English and Spanish) on purpose, for the store\'s customers.</p>\n</div>\n</footer>')
body.append(f"<script>{js}</script>\n</body>\n</html>\n")

html = head + "\n".join(body)
open(OUT, "w", encoding="utf-8").write(html)
n_art = len(re.findall(r'<article class="piece">', html))
ids = re.findall(r'\bid="([^"]+)"', html)
dups = {i for i in ids if ids.count(i) > 1}
print("ok", len(html), "bytes;", n_art, "piezas;", len(ids), "ids; duplicados:", sorted(dups))
