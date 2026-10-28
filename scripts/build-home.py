#!/usr/bin/env python3
"""
Generate the homepage's <main> from the site's data.

    python3 scripts/build-home.py

index.html keeps its hand-written head, header and footer (the chrome every
generated page lifts). Everything between the #home sentinels is built here,
in the language of the owner's reference (2026-10-28): midnight navy and
white, stepped blocks, huge light uppercase section words with a numbered
badge, giant numerals, "+" lists on hairlines, pictograms drawn as vertical
hatch lines, a carousel with a counter, statements with a hanging first line.
No photographs and no product mockups: the objects are vector art and motion.

    01 the opener (white L-block, the animated block cluster)
    02 the statement           06 in their words
    03 the numbers             07 the principles, as stepped blocks
    04 Solutions (hover panel) 08 our thinking
    05 Case studies (carousel) 09 the enquiry

Every project, figure and quotation comes from scripts/stories.py, cases.py
and services.py; nothing is written here that is not already evidenced there.
Run after build-stories.py.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


S = load('stories', 'stories.py')
SV = load('services', 'services.py')
C = load('cases', 'cases.py')
B = load('build_stories', 'build-stories.py')
esc, ARROW, PLAY = B.esc, B.ARROW, B.PLAY
NL = chr(10)

# the owner-supplied client logos, one grey version each (PR #77)
LOGOS = [
    ('wastemart', 'WasteMart'), ('managem', 'ManaGEM'), ('smartstart', 'SmartStart'),
    ('ecd-connect', 'ECD Connect'), ('homeassist', 'HomeAssist'),
    ('sbs-waterproofing', 'SBS Waterproofing'), ('trans-hex', 'Trans Hex Group'),
    ('sonke', 'Sonke Gender Justice'), ('tores-foundation', "Tore's Foundation"),
]


def link_for(slug, base=''):
    return f'{base}products/managem/' if S.BY_SLUG[slug].get('is_product') else f'{base}work/{slug}/'


# ── the pictograms: silhouettes filled with vertical hatch lines ──────────
# Drawn on a 120-unit box. The fill is a <pattern> of 1.6px lines every 5px —
# navy on white cards, white on navy blocks (chosen from CSS on the <svg>).
PICTO = {
    'custom-software': 'M44 20 8 60l36 40 10-9L23 60l31-31Zm32 0-10 9 31 31-31 31 10 9 36-40Z',
    'microsoft-cloud': 'M34 96a22 22 0 0 1-2.4-43.9A32 32 0 0 1 93.6 46 25 25 0 0 1 92 96Z',
    'enterprise-saas': 'M60 18 112 42 60 66 8 42Zm-52 40 12-5.5L60 76l40-21.5 12 5.5L60 86Zm0 20 12-5.5L60 96l40-21.5 12 5.5L60 106Z',
    'mobile-apps': 'M38 6h44a10 10 0 0 1 10 10v88a10 10 0 0 1-10 10H38a10 10 0 0 1-10-10V16A10 10 0 0 1 38 6Zm12 94h20v6H50Z',
    'business-intelligence': 'M14 64h20v44H14Zm36-26h20v70H50Zm36-26h20v96H86Z',
    'system-integration': 'M30 44a16 16 0 1 1 0 32 16 16 0 0 1 0-32Zm60 0a16 16 0 1 1 0 32 16 16 0 0 1 0-32ZM46 56h28v8H46Z',
    'ux-design': 'M28 14 98 62 66 68 86 96l-10 6-20-28-20 24Z',
    'modernisation': 'M8 106V82h28V58h28V34h28V10h20v96Z',
    'support': 'M60 8 104 24v34c0 26-18 46-44 56C34 104 16 84 16 58V24Z',
    'leak': 'M60 10c20 30 34 46 34 66a34 34 0 0 1-68 0c0-20 14-36 34-66Z',
    'capture': 'M60 8a36 36 0 0 1 36 36c0 26-36 68-36 68S24 70 24 44A36 36 0 0 1 60 8Zm0 20a16 16 0 1 0 0 32 16 16 0 0 0 0-32Z',
    'handoff': 'M8 44h60V24l44 36-44 36V76H8Z',
    'evolve': 'M54 70h12v42H54ZM60 8c22 0 38 18 38 38S82 78 60 78 22 68 22 46 38 8 60 8Z',
    'gem': 'M32 14h56l24 30-52 66L8 44Zm8 10L24 44h72L80 24Z',
}


def picto_sprite():
    syms = ''.join(f'<symbol id="px-{k}" viewBox="0 0 120 120"><path d="{d}" fill-rule="evenodd"/></symbol>'
                   for k, d in PICTO.items())
    return ('    <svg class="sprite" aria-hidden="true" focusable="false" width="0" height="0"><defs>'
            '<pattern id="hxHatchN" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="1.3" height="4" fill="#0a1230"/></pattern>'
            '<pattern id="hxHatchW" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="1.3" height="4" fill="#ffffff"/></pattern>'
            f'</defs>{syms}</svg>' + NL)


def picto(key, cls=''):
    return f'<svg class="hx-picto {cls}" aria-hidden="true" focusable="false"><use href="#px-{key}"/></svg>'


# ── the hero's object: an isometric cluster of blocks in thin white lines ──
# Generated here so the drawing is in code; the three layers drift apart at
# different speeds in CSS (static under reduced motion).
BOXES = [  # x, y, z, w, d, h in iso units
    (0, 0, 0, 4, 4, 3), (4, 0, 0, 3, 4, 5), (0, 4, 0, 4, 3, 4), (4, 4, 0, 3, 3, 2), (7, 0, 0, 3, 3, 4),
    (7, 3, 0, 3, 4, 6), (0, 7, 0, 3, 3, 2), (3, 7, 0, 4, 3, 5), (10, 2, 0, 2, 2, 3), (4, 0, 5, 3, 2, 2),
    (7, 3, 6, 2, 2, 2), (1, 1, 3, 2, 2, 2),
]


def cluster():
    cx, cy = 300, 320

    def P(x, y, z):
        return (cx + (x - y) * 26, cy + (x + y) * 13 - z * 26)

    def pts(q):
        return ' '.join(f'{a:.1f},{b:.1f}' for a, b in q)

    layers = {0: [], 1: [], 2: []}
    for i, (x, y, z, w, d, h) in enumerate(sorted(BOXES, key=lambda b: b[0] + b[1] + b[2])):
        top = [P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)]
        left = [P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)]
        right = [P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)]
        layers[i % 3].append(f'<polygon points="{pts(top)}" fill="rgba(255,255,255,.1)"/>'
                             f'<polygon points="{pts(left)}" fill="rgba(255,255,255,.03)"/>'
                             f'<polygon points="{pts(right)}" fill="rgba(255,255,255,.06)"/>')
    gs = ''.join(f'<g class="hx-cluster__l hx-cluster__l--{g + 1}" stroke="rgba(255,255,255,.62)" '
                 f'stroke-width="1" stroke-linejoin="round">{"".join(layers[g])}</g>' for g in (0, 1, 2))
    return f'<svg class="hx-cluster" viewBox="0 0 600 560" aria-hidden="true" focusable="false">{gs}</svg>'


def opener(word, n, aside, heading_id, ink=False):
    """The section opener: the huge light uppercase word in a block with a numbered badge, a tracked line beside it."""
    tone = ' hx-open__block--ink' if ink else ''
    return f'''        <div class="hx-open__row">
          <div class="hx-open__block{tone}" data-reveal>
            <h2 class="hx-open__word" id="{heading_id}">{word}</h2>
            <span class="hx-badge" aria-hidden="true">{n}</span>
          </div>
          <p class="hx-open__aside hx-label" data-reveal style="--d:120ms">{aside}</p>
        </div>'''


# ── 01 · the opener ────────────────────────────────────────────────────────
def hero():
    return f'''    <!-- ═══════════════════ 01 · THE OPENER ═══════════════════
         A white strip under the bar and a white L-block hanging from it with
         the wordmark, over a midnight field: a hatch of fine lines, the
         isometric block cluster drifting in three layers, two light streaks.
         Static under reduced motion. -->
    <section class="hx hx-hero" id="hero" aria-labelledby="heroHeading">
      <div class="hx-hero__field" aria-hidden="true">
        <div class="hx-hero__hatch"></div>
        {cluster()}
        <span class="hx-streak hx-streak--1"></span>
        <span class="hx-streak hx-streak--2"></span>
      </div>
      <div class="hx-hero__strip">
        <div class="shell hx-hero__strip-in">
          <p class="hx-label hx-hero__strip-label">Business systems <span aria-hidden="true">·</span> Cape Town <span aria-hidden="true">·</span> since 2014</p>
        </div>
      </div>
      <div class="hx-hero__block" data-reveal>
        <p class="hx-hero__word" aria-hidden="true">GEMIS<span class="hx-hero__dot"></span></p>
        <p class="hx-label hx-hero__sub">GEM Information Systems</p>
      </div>
      <div class="hx-hero__tag" data-reveal style="--d:200ms">
        <h1 class="hx-label hx-hero__h1" id="heroHeading">Systems built to last.<br />Partners built to stay.</h1>
      </div>
      <div class="hx-hero__foot">
        <div class="shell hx-hero__foot-in">
          <p class="hx-hero__copy" data-reveal style="--d:300ms">We build software around how your business actually works, and we stay to support it as you grow.</p>
          <div class="hx-hero__ctas" data-reveal style="--d:380ms">
            <a class="hx-btn hx-btn--light" href="#discovery">Book a Discovery Session</a>
            <a class="hx-btn hx-btn--ghost" href="#selected">See our work</a>
          </div>
          <span class="hx-scroll" aria-hidden="true"><span></span></span>
        </div>
      </div>
    </section>
'''


# ── 02 · the statement ─────────────────────────────────────────────────────
def statement():
    return f'''
    <!-- ═══════════════════ 02 · THE STATEMENT ═══════════════════
         The tagline as the reference sets its statements: uppercase, light,
         the first line hanging to the right; the gem pictogram beside the
         founding-client line. -->
    <section class="hx hx-state" aria-labelledby="stateHeading">
      <div class="shell">
        <div class="hx-state__head" data-reveal>
          <p class="hx-label">Business systems partner since 2014</p>
          <span class="hx-badge" aria-hidden="true">1</span>
        </div>
        <h2 class="hx-statement" id="stateHeading" data-reveal style="--d:100ms">We build software around how your business actually works, and we stay to support it as you grow.</h2>
        <div class="hx-state__row">
          <figure class="hx-state__obj" aria-hidden="true" data-reveal style="--d:200ms">{picto('gem', 'hx-picto--w hx-picto--lg')}</figure>
          <div class="hx-state__copy" data-reveal style="--d:260ms">
            <p>GEM Information Systems has been building business systems in South Africa since 2014 — and still works with the businesses it started with. We design around how a business actually runs, build on the Microsoft Cloud, and stay after go-live.</p>
            <p>Some of our clients have been with us for more than a decade.</p>
            <a class="hx-btn hx-btn--ghost" href="our-story/">Our story</a>
          </div>
        </div>
      </div>
    </section>
'''


# ── 03 · the numbers ───────────────────────────────────────────────────────
def numbers():
    stats = [('12', 'Years building business systems'), ('50', 'Systems delivered into production'),
             ('5', 'Sectors served nationally')]
    cells = NL.join(f'''          <li class="hx-num__cell" data-reveal style="--d:{i * 90}ms">
            <p class="hx-label">{esc(l)}</p>
            <p class="hx-num__n"><span class="stat__n" data-count="{n}" data-sup="+">{n}<sup>+</sup></span></p>
          </li>''' for i, (n, l) in enumerate(stats))
    logos = NL.join(f'            <li><img src="assets/img/logos/clients/{k}-grey.png" alt="{esc(n)}" height="40" loading="lazy" /></li>'
                    for k, n in LOGOS)
    return f'''
    <!-- ═══════════════════ 03 · THE NUMBERS ═══════════════════
         Three confirmed figures (scripts/facts.md) as giant light numerals in
         three hairlined columns, the label small above each; then the client
         marks. -->
    <section class="hx hx-num" aria-label="GEMIS in numbers">
      <div class="shell">
        <ul class="hx-num__grid">
{cells}
        </ul>
        <div class="hx-logos" data-reveal>
          <p class="hx-label">Trusted by</p>
          <ul class="hx-logos__row">
{logos}
          </ul>
        </div>
      </div>
    </section>
'''


# ── 04 · Solutions ─────────────────────────────────────────────────────────
def solutions():
    first = SV.SERVICES[0]
    items = NL.join(
        f'''          <li><a href="solutions/{s['slug']}/" data-svc-item="{s['slug']}" data-svc-name="{esc(s['name'])}" data-svc-line="{esc(s['short'])}"{' class="is-on"' if i == 0 else ''}><span class="hx-plus__mark" aria-hidden="true">+</span><span class="hx-plus__t">{esc(s['name'])}</span></a></li>'''
        for i, s in enumerate(SV.SERVICES))
    return f'''
    <!-- ═══════════════════ 04 · SOLUTIONS ═══════════════════
         The opener over a dotted field, then the reference's list panel: a
         white card carrying the discipline in view as a hatch pictogram, and
         the nine disciplines as a "+" list on hairlines. Hover or focus a
         line to bring it into the card (home.js, [data-svc]); without
         JavaScript the first discipline is shown and every line is a link. -->
    <section class="hx hx-open hx-open--sol" id="solutions" aria-labelledby="solHeading">
      <div class="hx-open__field" aria-hidden="true"><div class="hx-dots"></div><span class="hx-streak hx-streak--3"></span></div>
      <div class="shell hx-open__in">
{opener('Solutions', 2, 'Nine disciplines. One accountable team.', 'solHeading')}
        <p class="hx-open__copy" data-reveal style="--d:200ms">GEMIS combines the technical and design disciplines a business system needs — to build it, connect it, improve it and support it. Most engagements draw on several at once, and you deal with one team throughout.</p>
      </div>
    </section>
    <section class="hx hx-svc" aria-label="The nine disciplines" data-svc>
      <div class="shell hx-svc__grid">
        <div class="hx-svc__card" data-reveal>
          <p class="hx-label hx-svc__name" data-svc-name aria-live="polite">{esc(first['name'])}</p>
          <div class="hx-svc__pic" data-svc-pic>{picto(first['slug'], 'hx-picto--n')}</div>
          <p class="hx-svc__line" data-svc-line>{esc(first['short'])}</p>
          <a class="hx-btn hx-btn--ink" data-svc-link href="solutions/{first['slug']}/">Explore</a>
        </div>
        <ul class="hx-plus hx-plus--2" data-reveal style="--d:120ms">
{items}
        </ul>
      </div>
      <p class="shell hx-svc__all"><a class="hx-btn hx-btn--ghost" href="solutions/">All solutions</a></p>
    </section>
'''


# ── 05 · Case studies ──────────────────────────────────────────────────────
def cases():
    order = ['sbs-waterproofing', 'homeassist', 'wastemart', 'trans-hex', 'sonke', 'tores-foundation', 'managem']
    tiles = []
    for i, k in enumerate(order):
        st = S.BY_SLUG[k]
        c = C.CASES.get(k, {})
        out = c.get('status_short') or st.get('outcome', '')
        tiles.append(f'''          <li class="hx-tile" data-rail-item data-reveal style="--d:{(i % 3) * 80}ms">
            <p class="hx-label hx-tile__ind">{esc(st['industry'])}</p>
            <h3 class="hx-tile__name"><a href="{link_for(k)}">{esc(st['client'])}</a></h3>
            <p class="hx-tile__line">{esc(st['headline'])}</p>
            <p class="hx-tile__out">{esc(out)}</p>
            <div class="hx-tile__foot">
              <a class="hx-circle" href="{link_for(k)}" aria-label="Read the {esc(st['client'])} case study"><span aria-hidden="true">+</span></a>
              <a class="hx-circle" {B.play_attrs(st, '')} aria-label="Play the {esc(st['client'])} story">{PLAY}</a>
            </div>
          </li>''')
    return f'''
    <!-- ═══════════════════ 05 · CASE STUDIES ═══════════════════
         Seven systems as typographic navy tiles on a carousel with a counter
         and circle controls (home.js, [data-rail]); no stills. Each tile reads
         its case study or plays the video in the overlay. -->
    <section class="hx hx-cases" id="selected" aria-labelledby="casesHeading">
      <div class="shell">
{opener('Case studies', 3, 'Systems in production, each with its story on video.', 'casesHeading', ink=True)}
      </div>
      <div class="hx-rail" data-rail>
        <div class="shell hx-rail__head">
          <p class="hx-rail__count hx-label" aria-live="polite"><span data-rail-cur>1</span> <span aria-hidden="true">/</span> {len(order)}</p>
          <div class="hx-rail__ctl">
            <button class="hx-circle hx-circle--btn" type="button" data-rail-prev aria-label="Previous case studies"><svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M10.5 6h-9M5 2.5 1.5 6 5 9.5"/></svg></button>
            <button class="hx-circle hx-circle--btn" type="button" data-rail-next aria-label="Next case studies"><svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M1.5 6h9M7 2.5 10.5 6 7 9.5"/></svg></button>
          </div>
        </div>
        <ol class="hx-rail__track" data-rail-track aria-label="Case studies">
{NL.join(tiles)}
        </ol>
      </div>
      <p class="shell hx-rail__all"><a class="hx-btn hx-btn--ink" href="work/">All case studies</a></p>
    </section>
'''


# ── 06 · In their words ────────────────────────────────────────────────────
def in_their_words():
    """The shared stage from build-stories, restyled by the home block."""
    if not any(S.ENDORSERS[k].get('line') for k in S.ENDORSEMENT_ORDER):
        print('home: no quotation in endorsements.md yet — "In their words" shows "Quotation to follow." (owner\'s instruction)')
    html = B.in_their_words('')
    return html.replace('<section class="words testi band"', '<section class="hx hx-words words testi band"', 1)


# ── 07 · the principles ────────────────────────────────────────────────────
OPERATING = [
    {
        'n': '01', 'motif': 'leak',
        'statement': 'Start where the work leaks, not where the software is.',
        'copy': 'Enquiries lost between apps at SBS. Quotes, terms and payments chased by hand at WasteMart. We fix the leak before we design a screen.',
        'seen': ['sbs-waterproofing', 'wastemart'],
    },
    {
        'n': '02', 'motif': 'capture',
        'statement': 'Capture it once, where it happens, even with no signal.',
        'copy': 'Sonke’s facilitators log sessions offline. HomeAssist plumbers photograph each step on site. WasteMart drivers confirm with a scan.',
        'seen': ['sonke', 'homeassist', 'wastemart'],
    },
    {
        'n': '03', 'motif': 'handoff',
        'statement': 'Automate the hand-off nobody owns.',
        'copy': 'SBS deposit invoices go straight into accounting. WasteMart operations are alerted the moment payment lands. Tore’s claims are checked against the sessions actually run.',
        'seen': ['sbs-waterproofing', 'wastemart', 'tores-foundation'],
    },
    {
        'n': '04', 'motif': 'evolve',
        'statement': 'Build for year ten, not launch day.',
        'copy': 'SBS still runs on the system from 2015. Trans Hex’s version two added forecasts and live exchange rates. The SBS system grew into ManaGEM.',
        'seen': ['sbs-waterproofing', 'trans-hex', 'managem'],
    },
]


def principles():
    blocks = []
    for i, p in enumerate(OPERATING):
        seen = ' '.join(f'<a href="{link_for(k)}">{esc(S.BY_SLUG[k]["client"])}</a>' for k in p['seen'])
        blocks.append(f'''          <li class="hx-blk" data-reveal style="--d:{(i % 2) * 90}ms">
            <p class="hx-label hx-blk__n">{p['n']}</p>
            <h3 class="hx-blk__t">{esc(p['statement'])}</h3>
            <div class="hx-blk__pic" aria-hidden="true">{picto(p['motif'], 'hx-picto--w')}</div>
            <p class="hx-blk__copy">{esc(p['copy'])}</p>
            <p class="hx-blk__seen"><span class="hx-label">Seen in</span> {seen}</p>
          </li>''')
    return f'''
    <!-- ═══════════════════ 07 · THE PRINCIPLES ═══════════════════
         The four operating principles, verbatim, as stepped navy blocks with
         a hatch pictogram each — the reference's service blocks. -->
    <section class="hx hx-prin" id="thinking" aria-labelledby="prinHeading">
      <div class="shell">
{opener('Principles', 4, 'Seven systems. The same four decisions.', 'prinHeading', ink=True)}
        <ol class="hx-prin__grid">
{NL.join(blocks)}
        </ol>
      </div>
    </section>
'''


# ── 08 · our thinking ──────────────────────────────────────────────────────
def thinking():
    items = NL.join(
        f'''          <li><a href="insights/{a['slug']}/"><span class="hx-plus__mark" aria-hidden="true">+</span><span class="hx-plus__t">{esc(a['title'])}</span><span class="hx-label hx-plus__meta">{esc(a['tag'])} <span aria-hidden="true">·</span> {a['read']}</span></a></li>'''
        for a in SV.ARTICLES)
    return f'''
    <!-- ═══════════════════ 08 · OUR THINKING ═══════════════════ -->
    <section class="hx hx-think" aria-labelledby="thinkHeading">
      <div class="shell hx-think__grid">
        <div class="hx-think__head" data-reveal>
          <p class="hx-label">Insights</p>
          <h2 class="hx-think__t" id="thinkHeading">Notes from building systems that have to work</h2>
          <a class="hx-btn hx-btn--ink" href="insights/">All insights</a>
        </div>
        <ul class="hx-plus hx-plus--ink" data-reveal style="--d:120ms">
{items}
        </ul>
      </div>
    </section>
'''


# ── 09 · the enquiry ───────────────────────────────────────────────────────
def enquiry():
    # Book a Discovery Session: the form hands off to the visitor's email client (this site is static); nothing is stored.
    return r'''
    <!-- ═══════════════════ 09 · GET STARTED ═══════════════════
         The opener on navy, the three steps as a "+" list, the form in a
         white stepped block. The form hands off to the visitor's email client
         (this site is static); nothing is stored. -->
    <section class="hx hx-go" id="discovery" aria-labelledby="goHeading">
      <div class="shell hx-go__grid">
        <div class="hx-go__intro">
          <div class="hx-open__row">
            <div class="hx-open__block hx-open__block--ink hx-open__block--flush" data-reveal>
              <h2 class="hx-open__word" id="goHeading">Contact</h2>
              <span class="hx-badge" aria-hidden="true">5</span>
            </div>
          </div>
          <p class="hx-go__lede" data-reveal style="--d:120ms">Book a Discovery Session. Tell us what you're trying to fix. We'll come back within two working days with a short written view and a time to talk. No obligation.</p>
          <ol class="hx-plus hx-plus--steps" data-reveal style="--d:200ms">
            <li><span class="hx-plus__mark" aria-hidden="true">+</span><span class="hx-plus__t">We read it properly</span><span class="hx-plus__sub">Your enquiry reaches a monitored GEMIS mailbox, not a personal address. A person who has read it replies.</span></li>
            <li><span class="hx-plus__mark" aria-hidden="true">+</span><span class="hx-plus__t">A discovery conversation</span><span class="hx-plus__sub">We map how your organisation actually works — the goals, the friction and the constraints — before anyone proposes a system.</span></li>
            <li><span class="hx-plus__mark" aria-hidden="true">+</span><span class="hx-plus__t">A scoped way forward</span><span class="hx-plus__sub">You get an architecture, a plan and a cost you can act on. If we're not the right fit, we'll say so.</span></li>
          </ol>
          <p class="hx-go__contact" data-reveal style="--d:260ms"><span class="hx-label">Email</span><a href="mailto:info@gemis.co.za">info@gemis.co.za</a><span class="hx-label">Cape Town</span><span>9 Tapiola Way, Edgemead</span></p>
        </div>

        <div class="hx-go__panel" data-reveal style="--d:160ms">
          <form class="form" id="discoveryForm" novalidate>
            <div class="form__rows">
              <div class="field">
                <label for="d-name">Name <em aria-hidden="true">*</em><span class="vh"> (required)</span></label>
                <input id="d-name" name="name" type="text" placeholder="Jane Dlamini" autocomplete="name" required aria-describedby="d-name-err" />
                <p class="form__note" id="d-name-err" hidden>Please enter your name.</p>
              </div>

              <div class="field">
                <label for="d-email">Work email <em aria-hidden="true">*</em><span class="vh"> (required)</span></label>
                <input id="d-email" name="email" type="email" placeholder="jane@company.co.za" autocomplete="email" required aria-describedby="d-email-err" />
                <p class="form__note" id="d-email-err" hidden>Please enter a valid work email address.</p>
              </div>

              <div class="field field--wide">
                <label for="d-company">Company <em aria-hidden="true">*</em><span class="vh"> (required)</span></label>
                <input id="d-company" name="company" type="text" placeholder="Company name" autocomplete="organization" required aria-describedby="d-company-err" />
                <p class="form__note" id="d-company-err" hidden>Please enter your company name.</p>
              </div>

              <div class="field">
                <label for="d-goal">What are you looking to do? <em aria-hidden="true">*</em><span class="vh"> (required)</span></label>
                <select id="d-goal" name="goal" autocomplete="off" required aria-describedby="d-goal-err">
                  <option value="">Select one…</option>
                  <option>Replace a legacy system</option>
                  <option>Build a new platform or app</option>
                  <option>Connect existing systems</option>
                  <option>Reporting and business intelligence</option>
                  <option>Not sure yet</option>
                </select>
                <p class="form__note" id="d-goal-err" hidden>Please choose what you're looking to do.</p>
              </div>

              <div class="field">
                <label for="d-timeline">Rough timeline</label>
                <select id="d-timeline" name="timeline" autocomplete="off">
                  <option value="">Select one…</option>
                  <option>Within 3 months</option>
                  <option>3–6 months</option>
                  <option>6+ months</option>
                  <option>Just exploring</option>
                </select>
              </div>

              <div class="field field--wide">
                <label for="d-notes">Anything we should know?</label>
                <textarea id="d-notes" name="notes" placeholder="The system you're replacing, the process that's breaking, or the thing you want to build." autocomplete="off"></textarea>
              </div>
            </div>

            <div class="consent">
              <input id="d-consent" name="consent" type="checkbox" required aria-describedby="d-consent-err" />
              <label for="d-consent">
                I consent to GEM Information Systems processing the information above in
                order to respond to this enquiry, as described in the
                <a href="privacy.html">privacy notice</a>. I can withdraw this consent at
                any time.
              </label>
            </div>
            <p class="form__note" id="d-consent-err" hidden>Please confirm your consent before sending.</p>

            <button class="form__send hx-btn hx-btn--ink" type="submit">
              Book a Discovery Session
            </button>

            <p class="form__note" id="discoveryNote" role="status" aria-live="polite">
              This site is static, so sending opens a pre-filled message in your email
              client addressed to info@gemis.co.za — nothing is submitted or stored here.
            </p>
          </form>
        </div>
      </div>
    </section>

''' + B.video_modal() + NL


def home_main():
    return (picto_sprite() + hero() + statement() + numbers() + solutions() + cases()
            + in_their_words() + principles() + thinking() + enquiry())


if __name__ == '__main__':
    index = os.path.join(ROOT, 'index.html')
    B.fill_slot(index, 'home', home_main())
    print('index.html: the nine homepage sections written')
