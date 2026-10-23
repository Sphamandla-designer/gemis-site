#!/usr/bin/env python3
"""
GEMIS Studio in one file.

    python3 tools/build-studio-standalone.py [out.html]

The five studio pages — the home, Work, About, Services and Contact — run in
their own frames inside one HTML document, exactly as on the live site. The
React runtime, the Design Canvas runtime and template, the twelve font files,
every image and the mark are carried once, as data, so the file works with no
network at all, on any device. Links between the five pages switch frames;
links to the corporate site and to external sites open the live addresses.
"""
import base64
import html as H
import json
import os
import re
import sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(R, 'studio')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(R, 'gemis-studio-standalone.html')
LIVE = 'https://sphamandla-designer.github.io/gemis-site/'
PAGES = ['index.html', 'work.html', 'about.html', 'services.html', 'contact.html']

MIME = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml',
        '.webp': 'image/webp', '.woff2': 'font/woff2', '.woff': 'font/woff'}
ASSET = re.compile(r'assets/[A-Za-z0-9_.-]+?\.(?:jpg|jpeg|png|svg|webp|woff2|woff)')

A = {}


def asset(path):
    if path not in A:
        f = os.path.join(ST, path)
        if not os.path.exists(f):
            raise SystemExit('missing asset ' + path)
        A[path] = 'data:' + MIME[os.path.splitext(f)[1]] + ';base64,' + base64.b64encode(open(f, 'rb').read()).decode()
    return path


# the scripts, carried once; a page refers to them by token
for name in ('react.js', 'react-dom.js', 'dc-runtime.js', 'dc-template.js', 'dc-boot.js'):
    js = open(os.path.join(ST, 'assets', name), encoding='utf8').read()
    assert '</script' not in js, name
    A['js:' + name] = js

pages, titles = {}, {}
for key in PAGES:
    h = open(os.path.join(ST, key), encoding='utf8').read()
    titles[key] = H.unescape(re.search(r'<title>(.*?)</title>', h, flags=re.S).group(1).strip())
    # the scripts become tokens, filled when the frame is built
    h = re.sub(r'<script src="assets/([a-z-]+\.js)"( defer)?></script>',
               lambda m: '<script' + (m.group(2) or '') + '>@@js:' + m.group(1) + '@@</script>', h)
    assert '<script src=' not in h, (key, 'script left')
    # no network hints, no canonical: the file is its own address
    h = re.sub(r'\s*<link rel="preconnect"[^>]*>', '', h)
    h = re.sub(r'\s*<link rel="canonical"[^>]*>', '', h)
    # the corporate site and anything outside the studio goes to the live address
    h = re.sub(r'href="\.\./([^"]*)"', lambda m: f'href="{LIVE}{m.group(1)}"', h)
    for m in set(ASSET.findall(h)):
        asset(m)
    pages[key] = h

for name in ('js:dc-template.js', 'js:dc-runtime.js', 'js:dc-boot.js'):
    for m in set(ASSET.findall(A[name])):
        asset(m)

# every internal link lands on one of the five pages, or on the live site
for key, h in pages.items():
    for href in set(re.findall(r'href="([^"]+)"', h)):
        p = href.split('?')[0].split('#')[0]
        if not p or p.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:', 'assets/')):
            continue
        if p not in pages:
            pages[key] = pages[key].replace(f'href="{href}"', f'href="{LIVE}studio/{href}"')

BRIDGE = """<script>
/* Bridge to the enclosing single-file document: links to the other studio pages switch frames there;
   same-page anchors scroll here (inside a srcdoc frame they would resolve against the outer file). */
(function () {
  'use strict';
  if (window.parent === window) return;
  var goto = function (frag) { var el = frag && document.getElementById(frag); if (el) el.scrollIntoView(); else window.scrollTo(0, 0); };
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href]'); if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.charAt(0) === '#') { e.preventDefault(); goto(href.slice(1)); return; }
    if (/^(https?:|mailto:|tel:|data:)/.test(href)) return;
    var page = href.split('?')[0].split('#')[0]; var frag = (href.split('#')[1] || '');
    if (!page) page = 'index.html';
    e.preventDefault();
    window.parent.postMessage({ type: 'nav', page: page, frag: frag }, '*');
  }, true);
  window.addEventListener('message', function (e) { if (e.data && e.data.type === 'goto') goto(e.data.frag || ''); });
})();
</script>
"""
for key in pages:
    pages[key] = pages[key].replace('</body>', BRIDGE + '</body>')

fav = A['assets/favicon.svg']
jb = lambda o: json.dumps(o, ensure_ascii=False).replace('</', '<\\/')
shell = f'''<!DOCTYPE html>
<!-- GEMIS Studio — the studio site in one file.
     Pages: {', '.join(PAGES)}.
     The runtime, the fonts, every image and the mark are carried once below, as data (images become blob
     URLs when the file opens), so this file needs no network. Each page runs in its own frame exactly as on the live site; links between pages switch frames.
     Links to the corporate site and to external sites open the live addresses. -->
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{H.escape(titles['index.html'])}</title>
<link rel="icon" type="image/svg+xml" href="{fav}">
<style>
html,body{{margin:0;height:100%;background:#0b0b0c;color:#f3f4f6;font-family:system-ui,sans-serif}}
.pg{{position:fixed;inset:0;width:100%;height:100%;border:0;display:block;background:#0b0b0c}}
.pg[hidden]{{display:none}}
noscript div{{max-width:44ch;margin:20vh auto;padding:0 24px;line-height:1.5}}
noscript a{{color:#fff}}
</style>
</head>
<body>
<noscript><div><strong>GEMIS Studio.</strong> This single-file copy needs JavaScript to show its pages. The live site is at <a href="{LIVE}studio/">{LIVE}studio/</a>.</div></noscript>
<script id="site-assets" type="application/json">{jb(A)}</script>
<script id="site-pages" type="application/json">{jb(pages)}</script>
<script>
(function () {{
  'use strict';
  var assets = JSON.parse(document.getElementById('site-assets').textContent);
  var pages = JSON.parse(document.getElementById('site-pages').textContent);
  var titles = {jb(titles)};
  var frames = {{}};
  // Images become blob URLs, made once and shared by every frame: the Design Canvas runtime
  // splits inline style strings on ";" and would cut a data URI at "data:image/jpeg". The
  // fonts stay as data URIs — they live in <style> blocks, which the runtime leaves alone.
  var urls = {{}};
  function blobUrl(key) {{
    if (urls[key]) return urls[key];
    var d = assets[key]; if (!d || d.indexOf('data:') !== 0) return key;
    var head = d.slice(5, d.indexOf(';')), bin = atob(d.slice(d.indexOf(',') + 1));
    var u8 = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
    urls[key] = URL.createObjectURL(new Blob([u8], {{ type: head }}));
    return urls[key];
  }}
  function build(page) {{
    return pages[page]
      .replace(/@@(js:[a-z-]+\\.js)@@/g, function (m, k) {{ return assets[k] || ''; }})
      .replace(/assets\\/[A-Za-z0-9_.-]+?\\.(?:jpg|jpeg|png|svg|webp)/g, function (m) {{ return blobUrl(m); }})
      .replace(/assets\\/[A-Za-z0-9_.-]+?\\.(?:woff2|woff)/g, function (m) {{ return assets[m] || m; }});
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
    var m = /^#([a-z]+\\.html)(?:#(.*))?$/.exec(location.hash);
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
print(f'{OUT}  {mb:.1f} MB; pages: {len(pages)}; assets: {len([k for k in A if not k.startswith("js:")])}; scripts: {len([k for k in A if k.startswith("js:")])}')
