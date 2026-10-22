#!/usr/bin/env python3
"""
The corporate site in one file.

    python3 tools/build-site-standalone.py [out.html]

Every page that carries the corporate chrome — at any depth: the home, Case
Studies and the six case study pages, Solutions and the nine service pages,
Products, ManaGEM, About, Contact, Industries, News & Insights and its three
articles, Privacy, 404 — runs in its own frame inside one HTML document, exactly
as on the live site. The stylesheet, the scripts, the font, every image and
every case study video (MP4) are carried once, as data, so the file works with
no network at all, on any device. Links between pages switch frames; links to
the studio and to external sites open the live addresses.

Redirect stubs are left out (they only forward to pages that are already here).
"""
import base64
import html as H
import importlib.util
import json
import os
import re
import sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(R, 'gemis-site-standalone.html')
LIVE = 'https://sphamandla-designer.github.io/gemis-site/'

spec = importlib.util.spec_from_file_location('chrome', os.path.join(R, 'scripts', 'apply-chrome.py'))
CH = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CH)

MIME = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml',
        '.webp': 'image/webp', '.woff2': 'font/woff2', '.woff': 'font/woff', '.mp4': 'video/mp4'}
ASSET = re.compile(r'assets/(?:img|fonts|video)/[A-Za-z0-9_./-]+?\.(?:jpg|jpeg|png|svg|webp|woff2|woff|mp4)')

A = {}      # images, the font, the stylesheet and the scripts: inlined into each frame as data
V = {}      # the videos: turned into blob URLs once by the shell, so no page carries 1.5 MB per reference


def asset(path):
    """Register a file under its root-relative path; the value is its data URI."""
    store = V if path.endswith('.mp4') else A
    if path not in store:
        f = os.path.join(R, path)
        if not os.path.exists(f):
            raise SystemExit('missing asset ' + path)
        store[path] = 'data:' + MIME[os.path.splitext(f)[1]] + ';base64,' + base64.b64encode(open(f, 'rb').read()).decode()
    return path


# ── the stylesheet and the scripts, carried once ─────────────────────────
css = open(os.path.join(R, 'assets/css/site.css'), encoding='utf8').read()
css = re.sub(r"url\(\s*['\"]?\.\./(img|fonts)/([^'\")]+)['\"]?\s*\)",
             lambda m: 'url("' + asset('assets/' + m.group(1) + '/' + m.group(2)) + '")', css)
A['css'] = css

JS = {}
for name in ('site.js', 'home.js', 'review-mode.js', 'work-filters.js'):
    js = open(os.path.join(R, 'assets/js', name), encoding='utf8').read()
    assert '</script' not in js, name
    # the bundle carries MP4 only, so the overlay's WebM source becomes a second MP4 one
    js = js.replace("webm.type = 'video/webm'", "webm.type = 'video/mp4'")
    JS[name] = js
    A['js:' + name] = js

# ── the pages ────────────────────────────────────────────────────────────
pages, titles = {}, {}
for path in CH.pages():
    key = os.path.relpath(path, R).replace(os.sep, '/')
    base = CH.base_for(path)
    h = open(path, encoding='utf8').read()
    if 'http-equiv="refresh"' in h:
        continue    # a redirect stub: it only forwards to a page that is already here
    titles[key] = H.unescape(re.search(r'<title>(.*?)</title>', h, flags=re.S).group(1).strip())

    # every path becomes root-relative, so one asset map serves every depth
    if base:
        h = re.sub(r'((?:href|src|poster|data-mp4|data-webm|data-poster)=")' + re.escape(base), r'\1', h)

    # the stylesheet and the scripts become tokens, filled when the frame is built
    h, k = re.subn(r'<link rel="stylesheet" href="assets/css/site\.css[^"]*"\s*/?>', '<style>@@css@@</style>', h)
    assert k == 1, (key, 'css')
    h = re.sub(r'<link rel="preload"[^>]*>\s*', '', h)
    h = re.sub(r'<script src="assets/js/([a-z-]+\.js)[^"]*" defer></script>',
               lambda m: '<script>@@js:' + m.group(1) + '@@</script>', h)
    assert '<script src=' not in h, (key, 'script left')

    # MP4 only: drop the WebM sources and point the overlay's WebM slot at the MP4
    h = re.sub(r'\s*<source src="assets/video/[^"]+\.webm" type="video/webm">', '', h)
    h = re.sub(r'data-webm="([^"]+)\.webm"', r'data-webm="\1.mp4"', h)

    # the studio and anything outside the bundle goes to the live site
    h = re.sub(r'href="studio/([^"]*)"', lambda m: f'href="{LIVE}studio/{m.group(1)}"', h)

    for m in set(ASSET.findall(h)):
        asset(m)
    h = h.replace('href="assets/img/favicon.svg"', 'href="' + A['assets/img/favicon.svg'] + '"')
    pages[key] = h

KEYS = set(pages)


def resolve(frm, href):
    """A link as written in a page → the page key it points at, or None."""
    href = href.split('?')[0].split('#')[0]
    if not href or href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:', 'assets/')):
        return None
    if href.endswith('/'):
        href += 'index.html'
    return href if href in KEYS else 'LIVE'


# every internal link must land on a page in the bundle, or on the live site
for key, h in pages.items():
    for href in re.findall(r'href="([^"]+)"', h):
        r = resolve(key, href)
        if r == 'LIVE':
            pages[key] = pages[key].replace(f'href="{href}"', f'href="{LIVE}{href}"')

BRIDGE = """<script>
/* Bridge to the enclosing single-file document: links to the other pages switch frames there;
   same-page anchors scroll here (inside a srcdoc frame they would resolve against the outer file). */
(function () {
  'use strict';
  if (window.parent === window) return;
  var goto = function (frag) { var el = frag && document.getElementById(frag); if (el) el.scrollIntoView(); else window.scrollTo(0, 0); };
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href]'); if (!a) return;
    if (a.hasAttribute('data-watch')) return;           // the video overlay handles it
    var href = a.getAttribute('href') || '';
    if (href.charAt(0) === '#') { e.preventDefault(); goto(href.slice(1)); return; }
    if (/^(https?:|mailto:|tel:|data:)/.test(href)) return;
    var page = href.split('?')[0].split('#')[0]; var frag = (href.split('#')[1] || '');
    if (!page || page.slice(-1) === '/') page += 'index.html';
    e.preventDefault();
    window.parent.postMessage({ type: 'nav', page: page, frag: frag }, '*');
  }, true);
  window.addEventListener('message', function (e) { if (e.data && e.data.type === 'goto') goto(e.data.frag || ''); });
})();
</script>
"""
for key in pages:
    pages[key] = pages[key].replace('</body>', BRIDGE + '</body>')

fav = A['assets/img/favicon.svg']
jb = lambda o: json.dumps(o, ensure_ascii=False).replace('</', '<\\/')
page_list = ', '.join(sorted(pages))
shell = f'''<!DOCTYPE html>
<!-- GEM Information Systems — the corporate site in one file.
     Pages: {page_list}.
     The stylesheet, the scripts, the font, every image and every case study video are carried once below, as data,
     so this file needs no network. Each page runs in its own frame exactly as on the live site; links between pages
     switch frames. Links to the studio and to external sites open the live addresses. -->
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{H.escape(titles['index.html'])}</title>
<link rel="icon" type="image/svg+xml" href="{fav}">
<style>
html,body{{margin:0;height:100%;background:#f3f4f6;color:#121a26;font-family:system-ui,sans-serif}}
.pg{{position:fixed;inset:0;width:100%;height:100%;border:0;display:block;background:#f3f4f6}}
.pg[hidden]{{display:none}}
noscript div{{max-width:44ch;margin:20vh auto;padding:0 24px;line-height:1.5}}
</style>
</head>
<body>
<noscript><div><strong>GEM Information Systems.</strong> This single-file copy needs JavaScript to show its pages. The live site is at <a href="{LIVE}">{LIVE}</a>.</div></noscript>
<script id="site-assets" type="application/json">{jb(A)}</script>
<script id="site-videos" type="application/json">{jb(V)}</script>
<script id="site-pages" type="application/json">{jb(pages)}</script>
<script>
(function () {{
  'use strict';
  var assets = JSON.parse(document.getElementById('site-assets').textContent);
  var pages = JSON.parse(document.getElementById('site-pages').textContent);
  var videos = JSON.parse(document.getElementById('site-videos').textContent);
  var titles = {jb(titles)};
  var frames = {{}};
  // each video becomes one blob URL, shared by every frame that plays it
  var urls = {{}};
  function blobUrl(key) {{
    if (urls[key]) return urls[key];
    var d = videos[key]; if (!d) return key;
    var head = d.slice(5, d.indexOf(';')), bin = atob(d.slice(d.indexOf(',') + 1));
    var u8 = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
    urls[key] = URL.createObjectURL(new Blob([u8], {{ type: head }}));
    return urls[key];
  }}
  function build(page) {{
    return pages[page]
      .replace(/@@(css|js:[a-z-]+\\.js)@@/g, function (m, k) {{ return assets[k] || ''; }})
      .replace(/assets\\/video\\/[A-Za-z0-9_.\\/-]+?\\.mp4/g, function (m) {{ return blobUrl(m); }})
      .replace(/assets\\/(?:img|fonts|video)\\/[A-Za-z0-9_.\\/-]+?\\.(?:jpg|jpeg|png|svg|webp|woff2|woff)/g, function (m) {{ return assets[m] || m; }});
  }}
  function frame(page) {{
    if (frames[page]) return frames[page];
    var f = document.createElement('iframe');
    f.className = 'pg'; f.title = titles[page]; f.hidden = true;
    f.setAttribute('allowfullscreen', '');
    f.srcdoc = build(page);
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
    var m = /^#([A-Za-z0-9_\\/-]+\\.html)(?:#(.*))?$/.exec(location.hash);
    show(m ? m[1] : 'index.html', m ? m[2] : '');
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
open(OUT, 'w', encoding='utf8').write(shell)
mb = len(shell.encode()) / 1048576
print(f'{OUT}  {mb:.1f} MB; pages: {len(pages)}; assets: {len(A)}; videos: {len(V)}')
