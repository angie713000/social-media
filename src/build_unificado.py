#!/usr/bin/env python3
# Une el calendario (español, 4 marcas) y el pack de publicaciones (inglés, 2 marcas) en un solo HTML.
# Estructura: pestañas de marca arriba; dentro de cada marca, pestañas internas.
#   Resumen | K&G Market | Klean NYC | JDET Capital | Klean Perú
#   K&G Market y Klean NYC: Calendario, Overview, Week 1 a 4. JDET y Perú: solo Calendario.
import re

CAL = "calendario-contenidos.html"
PACK = "publicaciones-marcas-sem1-4.html"
OUT = "contenidos-por-marca.html"

cal = open(CAL, encoding="utf-8").read()
pack = open(PACK, encoding="utf-8").read()

OPEN = '<section role="tabpanel" id="panel-'


def panels(html, stops):
    """Devuelve {id: (clase_de_marca, contenido_interno)} de todos los paneles de pestaña."""
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

# Los botones «Copiar» del calendario usan ids cbNNN que chocan con los del pack: se les antepone una «c».
def reid(s):
    return re.sub(r'\bcb(\d+)\b', r'ccb\1', s)


# marca -> (etiqueta de la pestaña de marca, clase de color, [(id interno, etiqueta, clase, contenido)])
BR = {}
BR["res"] = ("Resumen", "b-all", [("cal", "Resumen", "b-all", reid(cp["resumen"][1]))])
BR["kg"] = ("K&amp;G Market", "b-kg", [("cal", "Calendario", "b-kg", reid(cp["kg-market"][1]))]
            + [(t, lab, "b-kg", pp[f"kg-{t}"][1]) for t, lab in
               (("resumen", "Overview"), ("sem1", "Week 1"), ("sem2", "Week 2"), ("sem3", "Week 3"), ("sem4", "Week 4"))])
BR["kn"] = ("Klean NYC", "b-klean", [("cal", "Calendario", "b-klean", reid(cp["klean-nyc"][1]))]
            + [(t, lab, "b-klean", pp[f"kn-{t}"][1]) for t, lab in
               (("resumen", "Overview"), ("sem1", "Week 1"), ("sem2", "Week 2"), ("sem3", "Week 3"), ("sem4", "Week 4"))])
BR["jd"] = ("JDET Capital", "b-jdet", [("cal", "Calendario", "b-jdet", reid(cp["jdet-capital"][1]))])
BR["kp"] = ("Klean Perú", "b-peru", [("cal", "Calendario", "b-peru", reid(cp["klean-peru"][1]))])
ORDER = ["res", "kg", "kn", "jd", "kp"]
FIRST = "cal"

# ------------------------------------------------------------------ cabecera, CSS y JS
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
/* Unificación: barra de marcas con desplazamiento horizontal (hay cinco marcas) */
.brandlist{overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.brandlist::-webkit-scrollbar{display:none}
.btab{flex:0 0 auto;white-space:nowrap}
.btab.b-all .dot{background:var(--muted)}
"""
css = css_pack + "\n/* Reglas del calendario */\n" + "\n".join(extra) + "\n" + OVERRIDES
head = head.replace(css_pack, css)
head = re.sub(r"<title>.*?</title>", "<title>Contenidos por marca: calendario y publicaciones</title>", head, flags=re.S)
head = head.replace('<html lang="en">', '<html lang="es">')
assert 'lang="es"' in head and "Contenidos por marca" in head and "Reglas del calendario" in head

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
    var es=/^Copiar/i.test(label);
    function done(ok){
      btn.textContent=ok?(es?'Copiado':'Copied'):(es?'Seleccione y copie':'Select and copy');
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

# ------------------------------------------------------------------ cuerpo
body = []
body.append('<body>\n<header class="top">\n'
            '<p class="eyebrow">9 de noviembre de 2026 al 7 de febrero de 2027</p>\n'
            '<h1>Contenidos por marca</h1>\n'
            '<p class="lead">Una pestaña por marca. En K&amp;G Market y Klean NYC, «Calendario» es el plan de 3 meses en español, y '
            '«Overview» y «Week 1» a «Week 4» son los posts de 4 semanas listos para copiar (en inglés), con guiones, prompts y TikToks. '
            'JDET Capital y Klean Perú tienen su calendario.</p>\n</header>')
body.append('<nav class="brands" id="brands"><div class="brandlist" role="tablist" aria-label="Marcas">')
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
        body.append(f'<nav class="tabs" id="tabs-{b}"><div class="tablist" role="tablist" aria-label="Secciones de {lab}">')
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
            '<p><b>Cómo usarlo.</b> Elige la marca arriba y luego una pestaña. Los botones «Copiar» y «Copy» copian el texto de cada caja. '
            'Las horas son de Nueva York, salvo las de Klean Perú, que son de Lima.</p>\n'
            '<p>Las etiquetas Referencia e Hipótesis tienen el mismo significado que en la página de estrategia. Los datos entre corchetes se completan con información real de cada negocio. '
            'Salvo el ají amarillo y la chicha morada, que ya aparecen en publicaciones de la cuenta, los productos y platos se confirman con la tienda.</p>\n'
            '<p>Los posts en inglés salen de la estrategia y del calendario de cada marca. Lo que depende del negocio está en «Before approving» de cada Overview. '
            'Las semanas 5 a 13 se detallan día por día en cada revisión. JDET Capital y Klean Perú dependen de las definiciones de la semana 1. '
            'No se publica nada sin aprobación.</p>\n</div>\n</footer>')
body.append(f"<script>{js}</script>\n</body>\n</html>\n")

html = head + "\n".join(body)
open(OUT, "w", encoding="utf-8").write(html)
n_art = len(re.findall(r'<article class="piece">', html))
ids = re.findall(r'\bid="([^"]+)"', html)
dups = {i for i in ids if ids.count(i) > 1}
print("ok", len(html), "bytes;", n_art, "piezas;", len(ids), "ids; duplicados:", sorted(dups))
