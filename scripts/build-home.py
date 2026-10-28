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
    04 Case studies (carousel) 08 our thinking
    05 Solutions (hover panel) 09 the enquiry

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


# the pictograms, the cluster and the opener come from the shared library
PICTO, picto, cluster, opener = B.PICTO, B.picto, B.cluster, B.opener


def sec_head(kicker, title, heading_id, lede='', cta='', ink=False, stack=False):
    """The site's section head on the home: the tracked kicker and the uppercase light title left, the lede (and an action) right, a hairline beneath."""
    cls = 'hx-sec' + (' hx-sec--ink' if ink else '') + (' hx-sec--stack' if stack else '')
    right = ''
    if lede or cta:
        right = (f'\n          <div class="hx-sec__r">' + (f'<p class="hx-sec__lede">{lede}</p>' if lede else '') + cta + '</div>')
    return f'''        <div class="{cls}" data-reveal>
          <div class="hx-sec__l"><p class="hx-label hx-sec__k">{kicker}</p><h2 class="hx-sec__t" id="{heading_id}">{title}</h2></div>{right}
        </div>'''


# ── 01 · the opener ────────────────────────────────────────────────────────
def hero():
    return f'''    <!-- ═══════════════════ 01 · THE OPENER ═══════════════════
         A white strip under the bar and a white L-block hanging from it with
         the wordmark, over a midnight field: a hatch of fine lines, the
         isometric block cluster drifting in three layers, two light streaks.
         Static under reduced motion. -->
    <section class="hx hx-hero" id="hero" aria-labelledby="heroHeading">
      <div class="hx-hero__field" aria-hidden="true" data-px=".12">
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
        <h1 class="hx-hero__title" id="heroHeading"><span class="hx-rise" style="--i:0">Systems built to last.</span><br /><span class="hx-rise" style="--i:1">Partners built to stay.</span></h1>
        <p class="hx-label hx-hero__sub">GEM Information Systems <span aria-hidden="true">·</span> Business systems partner since 2014</p>
      </div>
      <!-- The exact partner designation and badge artwork are still to be
           supplied — see OPEN_ITEMS.md (microsoft-partner-badge). -->
      <aside class="hx-hero__tag hx-hero__ms" data-reveal style="--d:260ms" aria-label="Microsoft partnership" data-tbc="microsoft-partner-badge" data-kind="hideable">
        <svg class="hx-hero__ms-mark" viewBox="0 0 21 21" aria-hidden="true"><rect x="0" y="0" width="10" height="10" fill="#f25022"/><rect x="11" y="0" width="10" height="10" fill="#7fba00"/><rect x="0" y="11" width="10" height="10" fill="#00a4ef"/><rect x="11" y="11" width="10" height="10" fill="#ffb900"/></svg>
        <span class="hx-label hx-hero__ms-line">Microsoft partner <span aria-hidden="true">·</span> Systems built and run on the Microsoft Cloud <span class="tbc" data-tbc="microsoft-partner-badge" data-kind="hideable">designation to confirm</span></span>
      </aside>
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
{sec_head('01 · Business systems partner since 2014', 'We build software around how your business actually works, and we stay to support it as you grow.', 'stateHeading', lede='GEM Information Systems has been building business systems in South Africa since 2014 — and still works with the businesses it started with. We design around how a business actually runs, build on the Microsoft Cloud, and stay after go-live.', ink=True)}
        <div class="hx-state__row">
          <figure class="hx-state__obj" aria-hidden="true" data-reveal style="--d:200ms" data-px=".08">{picto('gem', 'hx-picto--w hx-picto--lg')}</figure>
          <div class="hx-state__copy" data-reveal style="--d:260ms">
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
    logos = NL.join(f'            <li class="marquee__item"><img src="assets/img/logos/clients/{k}-grey.png" alt="{esc(n)}" height="40" loading="lazy" /></li>'
                    for k, n in LOGOS)
    logos2 = NL.join(f'            <li class="marquee__item"><img aria-hidden="true" src="assets/img/logos/clients/{k}-grey.png" alt="" height="40" loading="lazy" /></li>'
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
          <div class="marquee hx-marquee">
            <ul class="marquee__track">
{logos}
            </ul>
            <ul class="marquee__track" aria-hidden="true">
{logos2}
            </ul>
          </div>
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
    <section class="hx hx-svc" id="solutions" aria-labelledby="solHeading" data-svc>
      <div class="shell">
{sec_head('03 · Solutions', 'Nine disciplines. One accountable team.', 'solHeading', lede='GEMIS combines the technical and design disciplines a business system needs — to build it, connect it, improve it and support it. Most engagements draw on several at once, and you deal with one team throughout.', ink=True)}
      </div>
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
        v = f"{S.VIDEO_DIR}{st['video']}"
        tiles.append(f'''          <li class="hx-tile" data-rail-item data-reveal style="--d:{(i % 3) * 80}ms">
            <div class="hx-tile__media" data-preview data-src="{v}_web.mp4" data-webm="{v}_web.webm">
              <img src="{v}_thumb.jpg" alt="" loading="lazy" width="1280" height="720" />
              <video class="hx-tile__video" muted playsinline loop preload="none" tabindex="-1" aria-hidden="true"></video>
              <a class="hx-circle hx-tile__play" {B.play_attrs(st, '')} aria-label="Play the {esc(st['client'])} story">{PLAY}</a>
              <span class="hx-label hx-tile__len" aria-hidden="true">{st['duration_label']}</span>
            </div>
            <div class="hx-tile__body">
              <p class="hx-label hx-tile__ind">{esc(st['industry'])}</p>
              <h3 class="hx-tile__name"><a href="{link_for(k)}">{esc(st['client'])}</a></h3>
              <p class="hx-tile__line">{esc(st['headline'])}</p>
              <p class="hx-tile__out">{esc(out)}</p>
              <a class="hx-tile__more" href="{link_for(k)}"><span class="hx-plus__mark" aria-hidden="true">+</span><span class="hx-label">Read the case study</span></a>
            </div>
          </li>''')
    return f'''
    <!-- ═══════════════════ 05 · CASE STUDIES ═══════════════════
         Seven systems as typographic navy tiles on a carousel with a counter
         and circle controls (home.js, [data-rail]); no stills. Each tile reads
         its case study or plays the video in the overlay. -->
    <section class="hx hx-cases" id="selected" aria-labelledby="casesHeading">
      <div class="shell">
{sec_head('02 · Case studies', 'Systems in production, each with its story on video', 'casesHeading', lede='Seven systems GEMIS designed, built and supports. Each tile reads its case study or plays the video it was recorded from.')}
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
    """
    The three endorsements, copied exactly from endorsements.md, on the
    home's stage: the voices as a numbered rail with a counter and a running
    bar on the left, the quotation large on navy under a hatch quotation mark
    on the right; it advances on its own (home.js, [data-stage]) and every
    control still works without it. A person with no line yet shows
    "Quotation to follow." (a hideable TBC the gate still lists).
    """
    if not any(S.ENDORSERS[k].get('line') for k in S.ENDORSEMENT_ORDER):
        print('home: no quotation in endorsements.md yet — "In their words" shows "Quotation to follow." (owner\'s instruction)')
    keys = S.ENDORSEMENT_ORDER
    tabs, slides = [], []
    for i, k in enumerate(keys):
        e = S.ENDORSERS[k]
        pressed = 'true' if i == 0 else 'false'
        hidden = '' if i == 0 else ' aria-hidden="true"'
        meta = ' · '.join(x for x in (e.get('title'), e.get('company')) if x)
        tabs.append(f'''          <li><button class="hx-words__tab" type="button" data-tab data-go="{i}" aria-pressed="{pressed}"><span class="hx-label hx-words__n">{i + 1:02d}</span><span class="hx-words__who">{esc(e['name'])}</span><span class="hx-label hx-words__co">{esc(meta)}</span></button></li>''')
        quote = esc(e['line']) if e.get('line') else f'<span class="cs__pending" data-tbc="{e["line_tbc"]}" data-kind="hideable">Quotation to follow.</span>'
        since = f' · {esc(e["since"])}' if e.get('since') else ''
        link = ''
        if e.get('slug'):
            link = f'<a class="hx-btn hx-btn--ghost hx-words__more" href="{link_for(e["slug"])}">Read the {esc(S.BY_SLUG[e["slug"]]["client"])} story</a>'
        slides.append(f'''          <li class="hx-words__item" data-slide{hidden}>
            <blockquote class="hx-words__q"><p>{quote}</p></blockquote>
            <p class="hx-words__by"><span class="hx-words__face" aria-hidden="true">{e['initials']}</span><span class="hx-words__sig"><strong>{esc(e['name'])}</strong><span class="hx-label">{esc(meta)}{since}</span></span></p>
            {link}
          </li>''')
    return f'''
    <!-- ═══════════════════ 06 · IN THEIR WORDS ═══════════════════
         The three endorsements, copied exactly from endorsements.md, on the
         stage: a rail of voices with a counter and a running bar, the
         quotation large on navy. Advances on its own; static and complete
         without JavaScript. -->
    <section class="hx hx-words" id="in-their-words" aria-labelledby="wordsHeading">
      <div class="shell">
{sec_head('04 · Clients', 'In their words', 'wordsHeading', lede='Some of the businesses we work with today first trusted GEMIS more than a decade ago.', ink=True)}
        <div class="hx-words__stage" data-stage>
          <div class="hx-words__side">
            <ol class="hx-words__rail" aria-label="Choose a voice" data-reveal>
{NL.join(tabs)}
            </ol>
            <div class="hx-words__ctl" data-ctl hidden>
              <p class="hx-label hx-words__count"><span data-cur>01</span> <span aria-hidden="true">/</span> {len(keys):02d}</p>
              <span class="hx-words__bar" aria-hidden="true"><span data-bar></span></span>
              <div class="hx-words__btns">
                <button class="hx-circle hx-circle--btn" type="button" data-prev aria-label="Previous"><svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M10.5 6h-9M5 2.5 1.5 6 5 9.5"/></svg></button>
                <button class="hx-circle hx-circle--btn" type="button" data-next aria-label="Next"><svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M1.5 6h9M7 2.5 10.5 6 7 9.5"/></svg></button>
              </div>
            </div>
          </div>
          <div class="hx-words__main" data-reveal style="--d:120ms">
            <span class="hx-words__mark-wrap" data-px=".06">{picto('quote', 'hx-picto--w hx-words__mark')}</span>
            <ol class="hx-words__list" data-list>
{NL.join(slides)}
            </ol>
          </div>
        </div>
      </div>
    </section>
'''


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
{sec_head('05 · Principles', 'Seven systems. The same four decisions.', 'prinHeading', lede='The four operating principles behind every system on this site, each with the case studies it is seen in.')}
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
      <div class="shell hx-think__in">
{sec_head('Insights', 'Notes from building systems that have to work', 'thinkHeading', lede='What we have learned building and running business systems in South Africa — written for the operations and finance leads who have to live with the result.', cta='<a class="hx-btn hx-btn--ink" href="insights/">All insights</a>')}
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
'''+ sec_head('06 · Contact', 'Book a discovery session', 'goHeading', ink=True, stack=True) + r'''
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
    return (hero() + statement() + numbers() + cases() + solutions()
            + in_their_words() + principles() + thinking() + enquiry())


if __name__ == '__main__':
    index = os.path.join(ROOT, 'index.html')
    B.fill_slot(index, 'home', home_main())
    print('index.html: the nine homepage sections written')
