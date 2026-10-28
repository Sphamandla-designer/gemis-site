#!/usr/bin/env python3
"""
The Solutions section: the directory at /solutions/ and the nine service pages.

    python3 scripts/build-services.py     (calls this module)

Content lives in scripts/solutions.py (every claim sourced in
docs/SOLUTIONS-EVIDENCE.md); names, slugs and the navigation one-liners in
scripts/services.py. This module holds the components:

  hero()        service hero: breadcrumb, label + two-line headline, copy,
                CTAs and a diagram drawn for that service (DIAGRAMS)
  problem()     the situation, as a statement and the signs of it
  deliver()     capabilities, each with what it involves
  approach()    four styles: track (a drawn line), columns (the stage
                ledger), frames (increasing fidelity), loop (a cycle)
  compare()     a two-column comparison table
  kinds()       the kinds of system connected
  timeline()    client relationships by year (verified dates only)
  evidence()    case studies, each with why it is relevant here
  quote()       an approved endorsement, verbatim
  related()     complementary services, each with the reason
  faq()         <details> accordion + matching FAQPage data
  cta()         a closing enquiry specific to the service

Each page sets its own order of sections in solutions.PAGES[slug]['order'].
Grounds are assigned in sequence (paper → wash → paper → tint), so two
washes never touch whatever the order.
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


S = load('stories', 'stories.py')
SV = load('services', 'services.py')
SOL = load('solutions', 'solutions.py')
B = load('build_stories', 'build-stories.py')
P = load('build_pages', 'build-pages.py')
C = load('cases', 'cases.py')

esc, ARROW = B.esc, B.ARROW
CANON = S.CANONICAL
NL = chr(10)
INDEX = {s['slug']: i + 1 for i, s in enumerate(SV.SERVICES)}

GROUNDS = ['band', 'band band-wash', 'band', 'band band-tint']


def icon(slug):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{SV.ICONS[slug]}</svg>')


def name(slug):
    return SV.BY_SLUG[slug]['name']


# ══ the hero diagrams ═════════════════════════════════════════════════════
# White strokes on the photographic hero, one accent (#8fc3f3). Lines carry
# pathLength="1" and draw in on load (CSS only); nodes fade in. Each is a
# conceptual drawing of what the service does — no data, no screenshots.

def _svg(inner, label):
    return (f'<svg class="dg" viewBox="0 0 520 320" role="img" aria-label="{esc(label)}" '
            f'fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">'
            f'{inner}</svg>')


def _t(x, y, text, cls='dg-t', anchor='start'):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{esc(text)}</text>'


def _line(d, i, cls='dg-l'):
    return f'<path class="{cls}" d="{d}" pathLength="1" style="--i:{i}"/>'


def _box(x, y, w, h, i, cls='dg-n', rx=3):
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" style="--i:{i}"/>'


def dg_directory():
    labels = ['Custom software', 'Microsoft Cloud', 'SaaS platforms', 'Mobile apps', 'Reporting',
              'Integration', 'UX & design', 'Modernisation', 'Support']
    out = []
    for i, lab in enumerate(labels):
        y = 26 + i * 33
        out.append(f'<circle class="dg-n" cx="152" cy="{y}" r="3" fill="currentColor" style="--i:{i}"/>')
        out.append(_t(140, y + 4, f'{i + 1:02d}  {lab}', anchor='end'))
        out.append(_line(f'M156 {y} C 280 {y}, 300 160, 388 160', i))
    out.append('<circle class="dg-n dg-a" cx="420" cy="160" r="32" style="--i:9"/>')
    out.append('<circle class="dg-n" cx="420" cy="160" r="3.5" fill="currentColor" style="--i:9"/>')
    out.append(_t(420, 214, 'One accountable team', anchor='middle'))
    out.append(_line('M452 160 H 512', 10, 'dg-l dg-a'))
    return _svg(''.join(out), 'Nine disciplines converging into one accountable team')


def dg_converge():
    srcs = [('Spreadsheet', 24), ('Email', 98), ('Off-the-shelf app', 172), ('Paper forms', 246)]
    rows = ['Enquiry', 'Quote', 'Job', 'Invoice']
    out = []
    for i, (lab, y) in enumerate(srcs):
        out.append(_box(10, y, 128, 34, i, 'dg-n dg-dim'))
        out.append(_t(74, y + 21, lab, anchor='middle'))
        ty = 110 + i * 40
        out.append(_line(f'M138 {y + 17} C 220 {y + 17}, 220 {ty}, 312 {ty}', i))
    out.append(_box(300, 40, 210, 240, 4, 'dg-n dg-a'))
    out.append(_t(318, 70, 'One system', 'dg-t dg-h'))
    for i, lab in enumerate(rows):
        y = 96 + i * 40
        out.append(_box(318, y, 160, 28, 5 + i))
        out.append(_t(332, y + 18, lab))
    out.append(_line('M492 110 V 230', 9, 'dg-l dg-a'))
    for i in range(4):
        out.append(f'<circle class="dg-n" cx="492" cy="{110 + i * 40}" r="3" fill="currentColor" style="--i:{9 + i}"/>')
    return _svg(''.join(out), 'Scattered tools and spreadsheets converging into one system')


def dg_layers():
    layers = ['Applications', 'Data · Azure SQL', 'Identity & access', 'Microsoft Azure']
    out = []
    for i, lab in enumerate(layers):
        y = 30 + i * 66
        out.append(_box(90, y, 300, 44, i, 'dg-n' + (' dg-a' if i == 3 else '')))
        out.append(_t(108, y + 27, lab))
        out.append(_line(f'M390 {y + 22} H 430', 5 + i, 'dg-l dg-dash'))
        if i < 3:
            out.append(_line(f'M240 {y + 44} V {y + 66}', 4 + i))
    out.append(_box(430, 30, 80, 242, 4, 'dg-n dg-dashbox'))
    out.append(_t(470, 150, 'Backup', anchor='middle'))
    out.append(_t(470, 166, '& recovery', anchor='middle'))
    for i, y in enumerate((40, 60, 80)):
        out.append(f'<circle class="dg-n" cx="30" cy="{y}" r="6" style="--i:{i}"/>')
        out.append(_line(f'M38 {y} C 64 {y}, 64 52, 90 52', i))
    out.append(_t(14, 108, 'People'))
    return _svg(''.join(out), 'Applications, data, identity and Azure infrastructure as layers, with backup and recovery alongside')


def dg_tenants():
    out = [_t(20, 22, 'Conceptual', 'dg-t dg-k')]
    for i, (x, lab) in enumerate(((20, 'Organisation A'), (185, 'Organisation B'), (350, 'Organisation C'))):
        out.append(_box(x, 40, 150, 132, i))
        out.append(_t(x + 14, 64, lab, 'dg-t dg-h'))
        for j, r in enumerate(('Users', 'Data', 'Settings')):
            out.append(_box(x + 14, 80 + j * 26, 122, 18, 3 + j, 'dg-n dg-dim', 2))
            out.append(_t(x + 24, 93 + j * 26, r, 'dg-t dg-s'))
        out.append(_line(f'M{x + 75} 172 V 232', 6 + i))
    out.append(_box(20, 232, 480, 58, 9, 'dg-n dg-a'))
    out.append(_t(260, 266, 'One platform · shared core', 'dg-t dg-h', 'middle'))
    return _svg(''.join(out), 'Three organisations, each with their own users, data and settings, on one shared platform')


def dg_field():
    out = [_box(30, 30, 100, 260, 0, 'dg-n', 14)]
    for j in range(3):
        out.append(_box(44, 70 + j * 34, 72, 22, 1 + j, 'dg-n dg-dim', 2))
    out.append(_box(44, 236, 72, 26, 4, 'dg-n dg-a', 13))
    out.append(_t(80, 253, 'Capture', 'dg-t dg-s', 'middle'))
    out.append(_line('M130 160 H 225', 5))
    out.append(_line('M225 160 H 335', 6, 'dg-l dg-dash'))
    out.append(_line('M335 160 H 400', 7))
    # a signal glyph, struck through
    for k, h in enumerate((8, 14, 20)):
        out.append(f'<rect class="dg-n" x="{268 + k * 9}" y="{124 - h}" width="5" height="{h}" rx="1" style="--i:6"/>')
    out.append(_line('M262 128 L 298 98', 6, 'dg-l dg-a'))
    out.append(_t(280, 190, 'No signal: held on device', 'dg-t dg-s', 'middle'))
    out.append(_t(368, 148, 'Sync', 'dg-t dg-s', 'middle'))
    out.append(_box(400, 90, 110, 140, 8, 'dg-n dg-a'))
    out.append(_t(414, 114, 'Business system', 'dg-t dg-h'))
    for j in range(3):
        out.append(_box(414, 128 + j * 28, 82, 18, 9 + j, 'dg-n dg-dim', 2))
    out.append(_t(455, 256, 'Office & reporting', 'dg-t dg-s', 'middle'))
    return _svg(''.join(out), 'Work captured on a phone in the field, held offline, then synced to the business system')


def dg_provenance():
    out = []
    for i, (lab, y) in enumerate((('Finance', 40), ('Operations', 130), ('People', 220))):
        out.append(_box(10, y, 112, 40, i, 'dg-n dg-dim'))
        out.append(_t(66, y + 25, lab, anchor='middle'))
        out.append(_line(f'M122 {y + 20} C 150 {y + 20}, 150 150, 172 150', i))
    out.append(_box(172, 110, 128, 80, 3))
    out.append(_t(236, 145, 'Agreed', 'dg-t dg-h', 'middle'))
    out.append(_t(236, 162, 'definitions', 'dg-t dg-h', 'middle'))
    out.append(_line('M300 150 H 340', 4))
    out.append(_box(340, 80, 110, 140, 5, 'dg-n dg-a'))
    out.append(_t(354, 104, 'Report', 'dg-t dg-h'))
    for j in range(4):
        out.append(_line(f'M354 {126 + j * 22} H {436 - j * 14}', 6 + j, 'dg-l dg-dim'))
    out.append(_line('M450 150 H 466', 10))
    out.append('<circle class="dg-n dg-a" cx="490" cy="150" r="22" style="--i:11"/>')
    out.append(_t(490, 196, 'Decision', anchor='middle'))
    return _svg(''.join(out), 'Figures from finance, operations and people systems, through agreed definitions, into a report and a decision')


def dg_beforeafter():
    out = [_line('M260 16 V 304', 0, 'dg-l dg-dim'), _t(20, 26, 'Before', 'dg-t dg-k'), _t(280, 26, 'After', 'dg-t dg-k')]
    for i, (x, y, lab) in enumerate(((20, 56, 'Accounting'), (140, 56, 'Operations'), (80, 222, 'Payments'))):
        out.append(_box(x, y, 100, 36, i, 'dg-n dg-dim'))
        out.append(_t(x + 50, y + 23, lab, anchor='middle'))
    out.append('<circle class="dg-n" cx="130" cy="150" r="9" style="--i:3"/>')
    out.append(_line('M114 184 C 114 166, 146 166, 146 184', 3))
    out.append(_line('M70 92 L 122 142', 4, 'dg-l dg-dash'))
    out.append(_line('M190 92 L 138 142', 4, 'dg-l dg-dash'))
    out.append(_line('M130 188 L 130 222', 4, 'dg-l dg-dash'))
    out.append(_t(130, 290, 'Retyped by hand', 'dg-t dg-s', 'middle'))
    for i, (x, y, lab) in enumerate(((280, 56, 'Accounting'), (400, 56, 'Operations'), (340, 236, 'Payments'))):
        out.append(_box(x, y, 100, 36, 5 + i))
        out.append(_t(x + 50, y + 23, lab, anchor='middle'))
    out.append(_box(290, 146, 210, 32, 8, 'dg-n dg-a'))
    out.append(_t(395, 167, 'Integration layer', 'dg-t dg-h', 'middle'))
    out.append(_line('M330 92 V 146', 9))
    out.append(_line('M450 92 V 146', 9))
    out.append(_line('M390 178 V 236', 9))
    out.append(_t(395, 210, 'Logged · monitored', 'dg-t dg-s', 'start'))
    return _svg(''.join(out), 'Before: information retyped between systems. After: systems connected through a monitored integration layer')


def dg_frames():
    out = []
    frames = ((10, 150, 'Observe'), (120, 110, 'Map'), (230, 70, 'Prototype'), (340, 30, 'Interface'))
    for i, (x, y, lab) in enumerate(frames):
        out.append(f'<rect class="dg-n dg-fill{" dg-a" if i == 3 else ""}" x="{x}" y="{y}" width="170" height="140" rx="6" style="--i:{i * 2}"/>')
        out.append(_t(x + 14, y + 24, lab, 'dg-t dg-h'))
    # observe: notes
    for j, (cx, cy) in enumerate(((40, 210), (70, 232), (110, 205), (60, 262))):
        out.append(f'<circle class="dg-n" cx="{cx}" cy="{cy}" r="3" fill="currentColor" style="--i:1"/>')
    out.append(_line('M34 250 q 14 -10 28 0 t 28 0 t 28 0', 1, 'dg-l dg-dim'))
    # map: a flow
    out.append(_box(140, 160, 34, 22, 3, 'dg-n', 2))
    out.append(_box(200, 160, 34, 22, 3, 'dg-n', 2))
    out.append(_box(170, 210, 34, 22, 3, 'dg-n', 2))
    out.append(_line('M174 171 H 200', 3))
    out.append(_line('M217 182 L 195 210', 3))
    # prototype: outlined wireframe
    out.append(_box(248, 110, 134, 14, 5, 'dg-n dg-dim', 2))
    out.append(_box(248, 132, 60, 56, 5, 'dg-n dg-dim', 2))
    out.append(_box(316, 132, 66, 24, 5, 'dg-n dg-dim', 2))
    out.append(_box(316, 164, 66, 24, 5, 'dg-n dg-dim', 2))
    # interface: resolved
    out.append(f'<rect class="dg-n dg-solid" x="358" y="70" width="134" height="16" rx="2" style="--i:7"/>')
    for j in range(3):
        out.append(_box(358, 96 + j * 22, 134, 14, 7, 'dg-n', 2))
    return _svg(''.join(out), 'Design moving from observing the work, to a map, to a prototype, to a resolved interface')


def dg_stages():
    out = [_line('M40 262 H 500', 0, 'dg-l dg-dim')]
    out.append(f'<rect class="dg-n" x="40" y="18" width="12" height="12" rx="2" style="--i:0"/>')
    out.append(_t(60, 28, 'Existing system', 'dg-t dg-s'))
    out.append(f'<rect class="dg-n dg-solid" x="200" y="18" width="12" height="12" rx="2" style="--i:0"/>')
    out.append(_t(220, 28, 'Improved system', 'dg-t dg-s'))
    for i, c in enumerate((100, 220, 340, 460)):
        new = 30 + i * 46
        old = 184 - new
        x = c - 34
        out.append(f'<rect class="dg-n dg-solid" x="{x}" y="{256 - new}" width="68" height="{new}" rx="2" style="--i:{1 + i * 2}"/>')
        out.append(f'<rect class="dg-n dg-old" x="{x}" y="{252 - new - old}" width="68" height="{old}" rx="2" style="--i:{1 + i * 2};--o:{1 - i * .26:.2f}"/>')
        out.append(_t(c, 288, f'Stage {i + 1}', 'dg-t dg-s', 'middle'))
    return _svg(''.join(out), 'Four stages: the existing system gives way to the improved one, both running side by side between')


def dg_loop():
    out = ['<circle class="dg-n" cx="320" cy="160" r="110" style="--i:0"/>']
    nodes = ((320, 50, 'Monitor', 320, 34, 'middle'), (430, 160, 'Maintain', 446, 164, 'start'),
             (320, 270, 'Improve', 320, 298, 'middle'), (210, 160, 'Support', 196, 182, 'end'))
    for i, (x, y, lab, tx, ty, a) in enumerate(nodes):
        out.append(f'<circle class="dg-n dg-a" cx="{x}" cy="{y}" r="9" style="--i:{2 + i}"/>')
        out.append(_t(tx, ty, lab, 'dg-t dg-h', a))
    # direction marks on the circle
    for i, (x, y, rot) in enumerate(((398, 82, 45), (398, 238, 135), (242, 238, 225), (242, 82, 315))):
        out.append(f'<path class="dg-n" d="M-5 -4 L 0 0 L -5 4" transform="translate({x} {y}) rotate({rot})" style="--i:{6 + i}"/>')
    out.append(_line('M20 160 H 200', 1, 'dg-l dg-a'))
    out.append(_t(24, 148, 'Go-live', 'dg-t dg-k'))
    out.append(_t(320, 166, 'Year after year', 'dg-t dg-s', 'middle'))
    return _svg(''.join(out), 'After go-live, a continuing cycle of monitoring, maintenance, improvement and support')


DIAGRAMS = {'converge': dg_converge, 'layers': dg_layers, 'tenants': dg_tenants, 'field': dg_field,
            'provenance': dg_provenance, 'beforeafter': dg_beforeafter, 'frames': dg_frames,
            'stages': dg_stages, 'loop': dg_loop}


# ══ components ════════════════════════════════════════════════════════════

def sec_head(eyebrow, heading, hid, lede=''):
    lede_html = f'\n          <p class="lede" data-reveal style="--d:140ms">{lede}</p>' if lede else ''
    return f'''        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>{esc(eyebrow)}</p>
            <h2 class="display" id="{hid}" data-reveal style="--d:80ms">{esc(heading)}</h2>
          </div>{lede_html}
        </div>'''


def hero(slug, p, base):
    n = INDEX[slug]
    sec_label, sec_href = p['second']
    return f'''
    <section class="chero svh" id="hero">
      <div class="shell">
        <nav class="svh__crumbs" aria-label="Breadcrumb" data-reveal>
          <ol><li><a href="{base}solutions/">Solutions</a></li><li aria-current="page"><span class="svh__n">{n:02d}</span> of 09</li></ol>
        </nav>
        <h1 class="chero__title svh__title" data-reveal style="--d:80ms"><span class="svh__label">{esc(name(slug))}</span> {B.two_lines(esc(p['headline']))}</h1>
        <div class="svh__grid">
          <div class="svh__copy">
            <p class="chero__copy" data-reveal style="--d:140ms">{esc(p['copy'])}</p>
            <div class="cshero__ctas" data-reveal style="--d:200ms">
              <a class="btn" href="{base}contact.html?service={slug}">Discuss a project {ARROW}</a>
              <a class="arrow-link" href="{sec_href}">{esc(sec_label)} {ARROW}</a>
            </div>
          </div>
          <figure class="svh__visual">
{DIAGRAMS[p['visual']]()}
          </figure>
        </div>
      </div>
    </section>'''


def problem(p, ground):
    pr = p['problem']
    signs = NL.join(f'              <li data-reveal style="--d:{160 + i * 60}ms">{esc(x)}</li>' for i, x in enumerate(pr['signs']))
    return f'''
    <section class="{ground} sp" id="situation" aria-labelledby="spHeading">
      <div class="shell sp__in">
        <div class="sp__head">
          <p class="eyebrow" data-reveal>The situation</p>
          <h2 class="display" id="spHeading" data-reveal style="--d:80ms">{esc(pr['heading'])}</h2>
        </div>
        <div class="sp__body">
          <p class="sp__statement" data-reveal style="--d:120ms">{esc(pr['statement'])}</p>
          <div class="sp__signs">
            <p class="sp__signs-label" data-reveal style="--d:140ms">Signs you may recognise</p>
            <ul>
{signs}
            </ul>
          </div>
        </div>
      </div>
    </section>'''


def deliver(p, ground, slug):
    d = p['deliver']
    items = NL.join(f'''          <li class="sd__item" data-reveal style="--d:{i * 60}ms">
            <span class="sd__n" aria-hidden="true">{i + 1:02d}</span>
            <h3 class="sd__name">{esc(a)}</h3>
            <p class="sd__text">{esc(b)}</p>
          </li>''' for i, (a, b) in enumerate(d['items']))
    return f'''
    <section class="{ground} sd" id="deliver" aria-labelledby="sdHeading">
      <div class="shell">
{sec_head('What GEMIS delivers', d['heading'], 'sdHeading', esc(d['lede']))}
        <ol class="sd__list">
{items}
        </ol>
      </div>
    </section>'''


FRAME_GLYPHS = [
    # observe, map, prototype, interface — the same vocabulary as the UX hero
    '<circle cx="14" cy="20" r="2.4" fill="currentColor"/><circle cx="34" cy="14" r="2.4" fill="currentColor"/><circle cx="52" cy="24" r="2.4" fill="currentColor"/><path d="M8 34q8-6 16 0t16 0t16 0"/>',
    '<rect x="4" y="8" width="16" height="12" rx="2"/><rect x="40" y="8" width="16" height="12" rx="2"/><rect x="22" y="28" width="16" height="12" rx="2"/><path d="M20 14h20M48 20L36 28"/>',
    '<rect x="4" y="6" width="52" height="8" rx="2"/><rect x="4" y="18" width="22" height="22" rx="2"/><rect x="30" y="18" width="26" height="9" rx="2"/><rect x="30" y="31" width="26" height="9" rx="2"/>',
    '<rect x="4" y="6" width="52" height="8" rx="2" fill="currentColor"/><rect x="4" y="18" width="52" height="6" rx="2"/><rect x="4" y="27" width="52" height="6" rx="2"/><rect x="4" y="36" width="34" height="6" rx="2"/>',
]


def approach(p, ground, slug):
    a = p['approach']
    style = p.get('approach_style', 'columns')
    steps = a['steps']
    if style == 'columns':
        body = B.stages(steps).replace('<ol class="stages" data-reveal>', f'<ol class="stages" data-reveal style="--n:{len(steps)}">', 1)
    elif style == 'track':
        items = NL.join(f'''          <li class="trk__step" data-reveal style="--d:{200 + i * 140}ms">
            <span class="trk__dot" aria-hidden="true">{i + 1:02d}</span>
            <h3 class="trk__name">{esc(t)}</h3>
            <p class="trk__copy">{esc(c)}</p>
          </li>''' for i, (t, c) in enumerate(steps))
        body = f'''        <ol class="trk" data-reveal style="--n:{len(steps)}">
{items}
        </ol>'''
    elif style == 'frames':
        items = NL.join(f'''          <li class="frm__step" data-reveal style="--d:{i * 110}ms">
            <svg class="frm__glyph" viewBox="0 0 60 46" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">{FRAME_GLYPHS[i % 4]}</svg>
            <span class="frm__n" aria-hidden="true">{i + 1:02d}</span>
            <h3 class="frm__name">{esc(t)}</h3>
            <p class="frm__copy">{esc(c)}</p>
          </li>''' for i, (t, c) in enumerate(steps))
        body = f'''        <ol class="frm">
{items}
        </ol>'''
    else:  # loop
        items = NL.join(f'''          <li class="lp__step lp__step--{i + 1}" data-reveal style="--d:{i * 110}ms">
            <span class="lp__n" aria-hidden="true">{i + 1:02d}</span>
            <h3 class="lp__name">{esc(t)}</h3>
            <p class="lp__copy">{esc(c)}</p>
          </li>''' for i, (t, c) in enumerate(steps))
        body = f'''        <div class="lp">
          <ol class="lp__list">
{items}
          </ol>
        </div>'''
    return f'''
    <section class="{ground} sa sa--{style}" id="approach" aria-labelledby="saHeading">
      <div class="shell">
{sec_head('How the engagement works', a['heading'], 'saHeading', esc(a['lede']))}
{body}
      </div>
    </section>'''


def compare(p, ground):
    c = p['compare']
    a, b = c['cols']
    rows = NL.join(f'''            <tr>
              <th scope="row">{esc(r[0])}</th>
              <td data-label="{esc(a)}">{esc(r[1])}</td>
              <td data-label="{esc(b)}">{esc(r[2])}</td>
            </tr>''' for r in c['rows'])
    return f'''
    <section class="{ground} scmp" id="compare" aria-labelledby="scmpHeading">
      <div class="shell">
{sec_head('The difference', c['heading'], 'scmpHeading')}
        <div class="scmp__wrap" data-reveal>
          <table class="scmp__table">
            <caption class="vh">{esc(c['heading'])}</caption>
            <thead><tr><td></td><th scope="col">{esc(a)}</th><th scope="col">{esc(b)}</th></tr></thead>
            <tbody>
{rows}
            </tbody>
          </table>
        </div>
      </div>
    </section>'''


def kinds(p, ground):
    k = p['kinds']
    chips = NL.join(f'          <li>{esc(x)}</li>' for x in k['items'])
    return f'''
    <section class="{ground} skd" id="systems" aria-labelledby="skdHeading">
      <div class="shell skd__in">
        <div>
          <p class="eyebrow" data-reveal>Systems</p>
          <h2 class="display" id="skdHeading" data-reveal style="--d:80ms">{esc(k['heading'])}</h2>
        </div>
        <div>
          <ul class="skd__list" data-reveal style="--d:120ms">
{chips}
          </ul>
          <p class="skd__note" data-reveal style="--d:160ms">{esc(k['note'])}</p>
        </div>
      </div>
    </section>'''


def timeline(p, ground, base):
    t = p['timeline']
    start, end = t['start'], 2026
    span = end - start
    ticks = NL.join(f'            <li style="--x:{(y - start) / span:.4f}">{y if y < end else "Today"}</li>'
                    for y in range(start, end + 1) if (y - start) % 2 == 0 or y == end)
    rows = NL.join(f'''          <li class="stl__row" data-reveal style="--d:{i * 120}ms">
            <a class="stl__name" href="{base}work/{slug}/">{esc(label)}</a>
            <span class="stl__since">{esc(note)}</span>
            <span class="stl__track" aria-hidden="true"><span class="stl__bar" style="--x:{(year - start) / span:.4f}"></span></span>
          </li>''' for i, (slug, label, year, note) in enumerate(t['rows']))
    return f'''
    <section class="{ground} stl" id="timeline" aria-labelledby="stlHeading">
      <div class="shell">
{sec_head('Continuity', t['heading'], 'stlHeading', esc(t['lede']))}
        <div class="stl__chart">
          <ol class="stl__ticks" aria-hidden="true">
{ticks}
          </ol>
          <ol class="stl__rows">
{rows}
          </ol>
        </div>
      </div>
    </section>'''


def _evidence_item(e, base, i, shows=None):
    s = S.BY_SLUG[e['slug']]
    d = C.DETAIL.get(e['slug'], {}) if hasattr(C, 'DETAIL') else {}
    product = s.get('is_product')
    href = f'{base}products/managem/' if product else f'{base}work/{e["slug"]}/'
    role = d.get('role_short') or ('GEMIS’s own product' if product else '')
    status = d.get('status_short') or (s.get('outcome') if product else '')
    read = 'Read about ManaGEM' if product else 'Read the case study'
    still = f'{base}assets/img/cases/{e["slug"]}/{e["still"]}'
    shows_html = ''
    if shows:
        links = ' '.join(f'<li><a href="{base}solutions/{k}/">{esc(name(k))}</a></li>' for k in shows)
        shows_html = f'''
              <div class="sev__shows"><span>Disciplines shown</span><ul>{links}</ul></div>'''
    meta = ''
    if role or status:
        meta = f'''
              <dl class="sev__meta">
                {f'<div><dt>GEMIS’s role</dt><dd>{esc(role)}</dd></div>' if role else ''}
                {f'<div><dt>Status</dt><dd>{esc(status)}</dd></div>' if status else ''}
              </dl>'''
    return f'''          <article class="sev__item{' sev__item--lead' if i == 0 else ''}" data-reveal style="--d:{i * 90}ms">
            <figure class="sev__media">
              <img src="{still}" alt="{esc(e['alt'])}" width="1280" height="720" loading="lazy" decoding="async" />
              <a class="sev__play" {B.play_attrs(s, base)} aria-label="Play the {esc(s['client'])} story">{B.PLAY}</a>
              <figcaption>From the case study video</figcaption>
            </figure>
            <div class="sev__body">
              <p class="sev__ctx">{esc(s['industry'])}</p>
              <h3 class="sev__name"><a href="{href}">{esc(s['client'])}</a></h3>
              <p class="sev__why">{esc(e['why'])}</p>{shows_html}{meta}
              <a class="arrow-link sev__go" href="{href}">{read} {ARROW}</a>
            </div>
          </article>'''


def evidence(items, ground, base, heading='Where this has been done', lede='', note='', shows=False, sid='evidence'):
    arts = NL.join(_evidence_item(e, base, i, e.get('shows') if shows else None) for i, e in enumerate(items))
    note_html = f'\n        <p class="sev__note" data-reveal>{esc(note)}</p>' if note else ''
    lede = lede or f'Projects whose recorded scope shows this work. <a class="arrow-link" href="{base}work/">All case studies {ARROW}</a>'
    return f'''
    <section class="{ground} sev{' sev--one' if len(items) == 1 else ''}" id="{sid}" aria-labelledby="sevHeading">
      <div class="shell">
{sec_head('Evidence from real projects', heading, 'sevHeading', lede)}{note_html}
        <div class="sev__grid">
{arts}
        </div>
      </div>
    </section>'''


def quote(key, base):
    e = S.ENDORSERS[key]
    if not e.get('line'):
        return ''
    title = f"{esc(e['title'])} · " if e.get('title') else ''
    link = ''
    if e.get('slug'):
        link = f'\n          <a class="arrow-link" href="{base}work/{e["slug"]}/">Read the {esc(S.BY_SLUG[e["slug"]]["client"])} story {ARROW}</a>'
    return f'''
    <section class="band-ink sq" aria-label="In their words">
      <div class="shell sq__in">
        <p class="eyebrow" data-reveal>In their words</p>
        <blockquote class="sq__q" data-reveal style="--d:80ms"><p>{esc(e['line'])}</p></blockquote>
        <p class="sq__by" data-reveal style="--d:140ms"><strong>{esc(e['name'])}</strong> <span>{title}{esc(e['company'])}</span></p>{link}
      </div>
    </section>'''


def related(p, ground, base):
    rows = NL.join(f'''          <li data-reveal style="--d:{i * 60}ms">
            <a class="srel__link" href="{base}solutions/{k}/">
              <span class="srel__icon">{icon(k)}</span>
              <span class="srel__name">{esc(name(k))}</span>
              <span class="srel__why">{esc(why)}</span>
              <span class="srel__go" aria-hidden="true">{ARROW}</span>
            </a>
          </li>''' for i, (k, why) in enumerate(p['related']))
    aside = ''
    if p.get('aside'):
        q, label, href = p['aside']
        aside = f'''
        <p class="srel__aside" data-reveal>{esc(q)} <a class="arrow-link" href="{base}{href}">{esc(label)} {ARROW}</a></p>'''
    return f'''
    <section class="{ground} srel" id="related" aria-labelledby="srelHeading">
      <div class="shell">
{sec_head('Connected disciplines', 'Often part of the same engagement', 'srelHeading', f'Services that tend to work alongside this one. Not every engagement needs them. <a class="arrow-link" href="{base}solutions/">All nine solutions {ARROW}</a>')}
        <ul class="srel__list">
{rows}
        </ul>{aside}
      </div>
    </section>'''


def faq(slug, p, ground):
    items = NL.join(f'''          <details class="faq__item" data-reveal style="--d:{i * 50}ms">
            <summary class="faq__q"><span class="faq__n" aria-hidden="true">{i + 1:02d}</span><span class="faq__text">{esc(q)}</span><span class="post__plus" aria-hidden="true">+</span></summary>
            <div class="faq__a"><p>{esc(a)}</p></div>
          </details>''' for i, (q, a) in enumerate(p['faq']))
    return f'''
    <section class="{ground}" id="faq" aria-labelledby="faqHeading">
      <div class="shell">
{sec_head('Questions', 'Common questions', 'faqHeading', f'The questions that come up first about {esc(name(slug))}. Anything not answered here is worth raising in a discovery conversation.')}
        <div class="faq">
{items}
        </div>
      </div>
    </section>'''


def cta(slug, p, base):
    c = p['cta']
    return f'''
    <section class="convert" id="discuss" aria-labelledby="convertHeading">
      <div class="shell convert__in">
        <p class="eyebrow" data-reveal>{esc(name(slug))}</p>
        <h2 class="display" id="convertHeading" data-reveal style="--d:80ms">{esc(c['heading'])}</h2>
        <p class="lede" data-reveal style="--d:140ms">{esc(c['copy'])}</p>
        <div class="convert__ctas" data-reveal style="--d:200ms">
          <a class="btn" href="{base}contact.html?service={slug}">Discuss a project {ARROW}</a>
          <a class="arrow-link" href="{base}solutions/">All solutions {ARROW}</a>
        </div>
      </div>
    </section>'''


def jsonld(obj):
    return ('  <script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2).replace('</', '<\\/') + '\n  </script>')


def write(path, base, title, desc, body, extra_head):
    head, tail = P.shell(base, title, desc, f'{CANON}{path}'.replace('index.html', ''), extra_head=extra_head)
    os.makedirs(os.path.join(ROOT, os.path.dirname(path)), exist_ok=True)
    open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(head + body + tail)
    print(path)


# ══ a service page ════════════════════════════════════════════════════════

def service_page(slug):
    base = '../../'
    p = SOL.PAGES[slug]
    chapters = {'problem': ('The situation', '#situation'), 'deliver': ('What you get', '#deliver'),
                'approach': ('How we work', '#approach'), 'evidence': ('Evidence', '#evidence'), 'faq': ('FAQ', '#faq')}
    links = [chapters[k] for k in p['order'] if k in chapters]
    out = [B.subnav(name(slug), '#hero', links, f'Discuss a project {ARROW}', f'href="{base}contact.html?service={slug}"', name(slug)),
           hero(slug, p, base)]
    g = 0
    for key in p['order']:
        if key == 'quote':
            out.append(quote(p['quote'], base))
            continue
        ground = GROUNDS[g % len(GROUNDS)]
        g += 1
        if key == 'problem':
            out.append(problem(p, ground))
        elif key == 'deliver':
            out.append(deliver(p, ground, slug))
        elif key == 'approach':
            out.append(approach(p, ground, slug))
        elif key == 'compare':
            out.append(compare(p, ground))
        elif key == 'kinds':
            out.append(kinds(p, ground))
        elif key == 'timeline':
            out.append(timeline(p, ground, base))
        elif key == 'evidence':
            n = len(p['evidence'])
            out.append(evidence(p['evidence'], ground, base,
                                heading='Where this has been done' if n > 1 else 'The closest evidence',
                                note=p.get('evidence_note', '')))
        elif key == 'related':
            out.append(related(p, ground, base))
        elif key == 'faq':
            out.append(faq(slug, p, ground))
    out.append(cta(slug, p, base))
    out.append(NL + B.video_modal() + NL)
    url = f'{CANON}solutions/{slug}/'
    extra = NL.join([
        jsonld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Solutions", "item": f'{CANON}solutions/'},
            {"@type": "ListItem", "position": 2, "name": name(slug), "item": url}]}),
        jsonld({"@context": "https://schema.org", "@type": "Service", "name": name(slug),
                "serviceType": name(slug), "description": p['copy'], "url": url,
                "provider": {"@type": "Organization", "name": "GEM Information Systems (GEMIS)", "url": CANON},
                "areaServed": "ZA"}),
        jsonld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]}),
    ])
    write(f'solutions/{slug}/index.html', base, p['title'], p['desc'], ''.join(out), extra)


# ══ the directory ═════════════════════════════════════════════════════════

def directory():
    base = '../'
    rows = []
    for i, s in enumerate(SV.SERVICES):
        d = SOL.DIRECTORY[s['slug']]
        rows.append(f'''          <li class="sdir__row" data-reveal style="--d:{(i % 3) * 60}ms">
            <a class="sdir__link" href="{base}solutions/{s['slug']}/">
              <span class="sdir__n" aria-hidden="true">{i + 1:02d}</span>
              <span class="sdir__icon">{icon(s['slug'])}</span>
              <span class="sdir__main">
                <span class="sdir__name">{esc(s['name'])}</span>
                <span class="sdir__what">{esc(d['what'])}</span>
              </span>
              <span class="sdir__when"><span class="sdir__when-label">Choose it when</span> {esc(d['when'])}</span>
              <span class="sdir__go" aria-hidden="true">{ARROW}</span>
            </a>
          </li>''')
    together = []
    for i, (stage, line, keys) in enumerate(SOL.TOGETHER):
        links = NL.join(f'                <li><a href="{base}solutions/{k}/">{esc(name(k))}</a></li>' for k in keys)
        together.append(f'''          <li class="tog__step" data-reveal style="--d:{200 + i * 120}ms">
            <span class="tog__dot" aria-hidden="true"></span>
            <h3 class="tog__name">{esc(stage)}</h3>
            <p class="tog__copy">{esc(line)}</p>
            <ul class="tog__links">
{links}
            </ul>
          </li>''')
    paths = []
    for i, (problem_text, keys) in enumerate(SOL.PATHWAYS):
        links = NL.join(f'              <li><a class="arrow-link arrow-link--quiet" href="{base}solutions/{k}/">{esc(name(k))} {ARROW}</a></li>' for k in keys)
        paths.append(f'''          <li class="path__row" data-reveal style="--d:{(i % 4) * 60}ms">
            <p class="path__problem">{esc(problem_text)}</p>
            <div class="path__start">
              <span class="path__label">Start with</span>
              <ul>
{links}
              </ul>
            </div>
          </li>''')
    body = f'''
    <section class="chero svh svh--dir" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>Solutions</p>
        <h1 class="chero__title svh__title" data-reveal style="--d:80ms">{B.two_lines("Nine disciplines. One accountable team.")}</h1>
        <div class="svh__grid">
          <div class="svh__copy">
            <p class="chero__copy" data-reveal style="--d:140ms">GEMIS combines the technical and design disciplines a business system needs — to build it, connect it, improve it and support it. Most engagements draw on several at once, and you deal with one team throughout.</p>
            <div class="cshero__ctas" data-reveal style="--d:200ms">
              <a class="btn" href="{base}contact.html">Discuss a project {ARROW}</a>
              <a class="arrow-link" href="{base}work/">Explore the work {ARROW}</a>
            </div>
          </div>
          <figure class="svh__visual">
{dg_directory()}
          </figure>
        </div>
      </div>
    </section>

    <section class="band sdir" id="services" aria-labelledby="sdirHeading">
      <div class="shell">
{sec_head('The nine disciplines', 'What each one is for', 'sdirHeading', 'Each discipline has its own page: the problem it addresses, what GEMIS delivers, how the work runs and the projects that show it.')}
        <ol class="sdir__list">
{NL.join(rows)}
        </ol>
      </div>
    </section>

    <section class="band band-wash tog" id="process" aria-labelledby="togHeading">
      <div class="shell">
{sec_head('How the disciplines work together', 'One engagement, several disciplines', 'togHeading', 'A business system is rarely one discipline’s work. This is how they can combine — an illustration, not a fixed sequence: many engagements use only some of them, in a different order.')}
        <ol class="tog__track" data-reveal style="--n:{len(SOL.TOGETHER)}">
{NL.join(together)}
        </ol>
      </div>
    </section>
{evidence(SOL.DIRECTORY_EVIDENCE, 'band', base, heading='Three projects, several disciplines each', lede=f'Chosen because between them they show most of the disciplines in use. Each names what GEMIS actually did. <a class="arrow-link" href="{base}work/">All case studies {ARROW}</a>', shows=True)}

    <section class="band band-tint path" id="start" aria-labelledby="pathHeading">
      <div class="shell">
{sec_head('Choosing where to start', 'Start from the problem', 'pathHeading', 'Pick the line closest to your situation. The paths overlap — that is normal, and a discovery conversation sorts out the rest.')}
        <ol class="path__list">
{NL.join(paths)}
        </ol>
      </div>
    </section>
{quote('philippine-francke', base)}
    <section class="convert" id="discuss" aria-labelledby="convertHeading">
      <div class="shell convert__in">
        <p class="eyebrow" data-reveal>Your project</p>
        <h2 class="display" id="convertHeading" data-reveal style="--d:80ms">Let&rsquo;s work out what your business needs.</h2>
        <p class="lede" data-reveal style="--d:140ms">Tell us about your current system, the operational challenge or the project you are planning. We come back within two working days with a short written view and a time to talk.</p>
        <div class="convert__ctas" data-reveal style="--d:200ms">
          <a class="btn" href="{base}contact.html">Discuss a project {ARROW}</a>
          <a class="arrow-link" href="{base}work/">Explore the work {ARROW}</a>
        </div>
      </div>
    </section>

{B.video_modal()}
'''
    extra = NL.join([
        jsonld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Solutions", "item": f'{CANON}solutions/'}]}),
        jsonld({"@context": "https://schema.org", "@type": "ItemList", "name": "GEMIS solutions",
                "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s['name'],
                                     "url": f"{CANON}solutions/{s['slug']}/"} for i, s in enumerate(SV.SERVICES)]}),
    ])
    write('solutions/index.html', base, 'Solutions — nine disciplines, one accountable team | GEMIS®',
          'The nine GEMIS disciplines — custom software, Microsoft Cloud, SaaS platforms, mobile, reporting, '
          'integration, UX, modernisation and support — and how to choose where to start.',
          body, extra)


def build():
    directory()
    for s in SV.SERVICES:
        service_page(s['slug'])


if __name__ == '__main__':
    build()
