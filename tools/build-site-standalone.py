# The corporate site in one file: every page in its own frame, site.css, site.js, the fonts and the images carried once.
import re, base64, os, json, sys, html as H
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=sys.argv[1] if len(sys.argv)>1 else R+'/gemis-site-standalone.html'   # python3 tools/build-site-standalone.py
LIVE='https://sphamandla-designer.github.io/gemis-site/'
PAGES=['index','about','services','industries','case-studies','contact','managem','wastemart','insights','privacy','404']
mime={'.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.svg':'image/svg+xml','.webp':'image/webp','.woff2':'font/woff2','.woff':'font/woff','.js':'text/javascript'}
pat=re.compile(r'assets/(?:img|fonts)/[A-Za-z0-9_./-]+?\.(?:jpg|jpeg|png|svg|webp|woff2|woff)|assets/js/(?:gsap|ScrollTrigger|lenis)\.min\.js')
A={}
def asset(path):
    if path not in A:
        f=os.path.join(R,path)
        if not os.path.exists(f): raise SystemExit('missing asset '+path)
        A[path]='data:'+mime[os.path.splitext(f)[1]]+';base64,'+base64.b64encode(open(f,'rb').read()).decode()
    return path
tokens=open(R+'/assets/css/tokens.css',encoding='utf8').read()
tokens=re.sub(r"url\(\s*['\"]?\.\./(img|fonts)/([^'\")]+)['\"]?\s*\)", lambda m: 'url("'+asset('assets/'+m.group(1)+'/'+m.group(2))+'")', tokens)
css=open(R+'/assets/css/site.css',encoding='utf8').read()
css=re.sub(r"url\(\s*['\"]?\.\./(img|fonts)/([^'\")]+)['\"]?\s*\)", lambda m: 'url("'+asset('assets/'+m.group(1)+'/'+m.group(2))+'")', css)
js=open(R+'/assets/js/site.js',encoding='utf8').read(); assert '</script' not in js

def bundle(entry):
    """The page's ES modules as one classic script: motion → common → the page, imports and exports stripped.
       No three.js in the single file; common.js sees window.__SINGLE_FILE and shows the stills instead."""
    out=[]
    for name in ['motion','common',entry]:
        src=open(f'{R}/assets/js/{name}.js',encoding='utf8').read()
        src=re.sub(r"^import .*?;\n", '', src, flags=re.M)
        src=re.sub(r"^export \{[^}]*\};?\n", '', src, flags=re.M)
        src=re.sub(r"^export (async function|function|const|let)", r"\1", src, flags=re.M)
        src=src.replace("({ mountGem } = await import('./gem.js'))", "(() => { throw new Error('no gem in the single-file build'); })()")
        assert 'import ' not in re.sub(r"//.*|/\*.*?\*/", '', src, flags=re.S).replace("import(", ''), (name, 'an import survived')
        out.append(f'/* ── {name}.js ── */\n'+src)
    code='window.__SINGLE_FILE = true;\n(function () {\n'+'\n'.join(out)+'\n})();'
    assert '</script' not in code
    return code
bundles={'index':bundle('home')}
for p_ in PAGES:
    if p_!='index': bundles[p_]=bundle('page')
PAGE_RE=re.compile(r'^(?:'+'|'.join(re.escape(p) for p in PAGES)+r')\.html(?:#.*)?$')
BRIDGE = """<script>
/* Bridge to the enclosing single-file document: links to the other pages switch frames there;
   same-page anchors scroll here (inside a srcdoc frame they would resolve against the outer file). */
(function () {
  'use strict';
  if (window.parent === window) return;
  var goto = function (frag) { var el = frag && document.getElementById(frag); if (el) el.scrollIntoView(); else window.scrollTo(0, 0); };
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href]'); if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.charAt(0) === '#') { e.preventDefault(); goto(href.slice(1)); return; }
    var m = /^(PAGES)\\.html(?:#(.*))?$/.exec(href);
    if (!m) return;
    e.preventDefault();
    window.parent.postMessage({ type: 'nav', page: m[1] + '.html', frag: m[2] || '' }, '*');
  }, true);
  window.addEventListener('message', function (e) { if (e.data && e.data.type === 'goto') goto(e.data.frag || ''); });
})();
</script>
""".replace('PAGES','|'.join(re.escape(p) for p in PAGES))
pages={}; titles={}
for p in PAGES:
    h=open(f'{R}/{p}.html',encoding='utf8').read()
    titles[p+'.html']=H.unescape(re.search(r'<title>(.*?)</title>',h,flags=re.S).group(1).strip())
    h,k=re.subn(r'<link rel="stylesheet" href="assets/css/tokens\.css[^"]*"\s*/?>', lambda m: '<style>\n'+tokens+'\n</style>', h); assert k==1, (p,'tokens')
    h,k=re.subn(r'<link rel="stylesheet" href="assets/css/site\.css[^"]*"\s*/?>', lambda m: '<style>\n'+css+'\n</style>', h); assert k==1, (p,'css')
    h=re.sub(r'\s*<link rel="modulepreload"[^>]*>', '', h)
    h=re.sub(r'\s*<link rel="preload" as="image"[^>]*>', '', h)
    h,k=re.subn(r'<script src="assets/js/site\.js[^"]*" defer></script>', '', h); assert k==1, (p,'js')
    h,k=re.subn(r'\s*<script type="module" src="assets/js/(?:home|page)\.js[^"]*"></script>', '', h); assert k==1, (p,'module')
    h=h.replace('</body>', '<script>\n'+js+'\n</script>\n'+BRIDGE+'<script>\n'+bundles[p]+'\n</script>\n</body>')
    # the studio and anything else outside these pages goes to the live site
    h=re.sub(r'href="studio/([^"]*)"', lambda m: f'href="{LIVE}studio/{m.group(1)}"', h)
    h=re.sub(r'href="(brand-studio|solutions|work|wastemart-driver)\.html([^"]*)"', lambda m: f'href="{LIVE}{m.group(1)}.html{m.group(2)}"', h)
    # every asset path becomes a token, filled from the shared map at load time
    for m in set(pat.findall(h)): asset(m)
    h=h.replace('href="assets/img/favicon.svg"','href="'+A['assets/img/favicon.svg']+'"')
    left=[x for x in re.findall(r'(?<![\w-])(?:src|href)="([^"]+)"',h) if not (x.startswith(('data:','#','https://','http://','mailto:','tel:','assets/')) or PAGE_RE.match(x))]
    assert not left, (p,left)
    pages[p+'.html']=h
fav=A['assets/img/favicon.svg']
jb=lambda o: json.dumps(o,ensure_ascii=False).replace('</','<\\/')
shell=f'''<!DOCTYPE html>
<!-- GEM Information Systems — the corporate site in one file: {', '.join(PAGES)} as served from the repository root,
     with the stylesheet, the script, the fonts and every image carried once below. Each page runs in its own frame
     exactly as on the live site; links between pages switch frames. Links to the studio and anything external go online. -->
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{H.escape(titles['index.html'])}</title>
<link rel="icon" type="image/svg+xml" href="{fav}">
<style>
html,body{{margin:0;height:100%;background:#f2f2f1;color:#16181b;font-family:system-ui,sans-serif}}
.pg{{position:fixed;inset:0;width:100%;height:100%;border:0;display:block;background:#f2f2f1}}
.pg[hidden]{{display:none}}
noscript div{{max-width:44ch;margin:20vh auto;padding:0 24px;line-height:1.5}}
</style>
</head>
<body>
<noscript><div><strong>GEM Information Systems.</strong> This single-file copy needs JavaScript to show its pages. The live site is at <a href="{LIVE}">{LIVE}</a>.</div></noscript>
<script id="site-assets" type="application/json">{jb(A)}</script>
<script id="site-pages" type="application/json">{jb(pages)}</script>
<script>
(function () {{
  'use strict';
  var assets = JSON.parse(document.getElementById('site-assets').textContent);
  var pages = JSON.parse(document.getElementById('site-pages').textContent);
  var titles = {jb(titles)};
  var frames = {{}};
  function frame(page) {{
    if (frames[page]) return frames[page];
    var f = document.createElement('iframe');
    f.className = 'pg'; f.title = titles[page]; f.hidden = true;
    f.srcdoc = pages[page].replace(/assets\\/(?:img|fonts)\\/[A-Za-z0-9_.\\/-]+?\\.(?:jpg|jpeg|png|svg|webp|woff2|woff)/g, function (m) {{ return assets[m] || m; }});
    document.body.appendChild(f); frames[page] = f; return f;
  }}
  function show(page, frag) {{
    if (!pages[page]) page = 'index.html';
    var f = frame(page);
    Object.keys(frames).forEach(function (k) {{ frames[k].hidden = k !== page; }});
    document.title = titles[page];
    var go = function () {{ f.contentWindow.postMessage({{ type: 'goto', frag: frag || '' }}, '*'); }};
    if (f.contentDocument && f.contentDocument.readyState === 'complete' && f.contentDocument.body && f.contentDocument.body.children.length) setTimeout(go, 50);
    else f.addEventListener('load', function () {{ setTimeout(go, 50); }}, {{ once: true }});
  }}
  function fromHash() {{
    var m = /^#([a-z0-9-]+)\\.html(?:#(.*))?$/.exec(location.hash);
    show(m ? m[1] + '.html' : 'index.html', m ? m[2] : '');
  }}
  window.addEventListener('message', function (e) {{
    if (!e.data || e.data.type !== 'nav') return;
    var h = '#' + e.data.page + (e.data.frag ? '#' + e.data.frag : '');
    if (location.hash === h) show(e.data.page, e.data.frag); else location.hash = h;
  }});
  window.addEventListener('hashchange', fromHash);
  fromHash();
}})();
</script>
</body></html>
'''
open(OUT,'w',encoding='utf8').write(shell)
print(OUT, len(shell.encode())//1024, 'KB; pages:', len(pages), '; assets:', len(A), '(', sum(len(v) for v in A.values())//1024, 'KB )')
