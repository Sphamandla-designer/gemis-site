#!/usr/bin/env python3
"""
Generate the homepage's <main> from the site's data.

    python3 scripts/build-home.py

index.html keeps its hand-written head, header and footer (the chrome every
generated page lifts). Everything between the #home sentinels is built here,
in the order the case-study-led brief sets:

    01 proposition hero        06 long-term partnership proof
    02 featured case study     07 how GEMIS works
    03 selected projects       08 the company
    04 the thinking            09 the enquiry
    05 capabilities, demonstrated

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
# the reference's thin right-pointing arrow on the monospace links
MONO_ARROW = '<svg viewBox="0 0 14 10" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M1 5h11M8.5 1.5 12 5l-3.5 3.5"/></svg>'

# the owner-supplied client logos, one grey version each (PR #77)
LOGOS = [
    ('wastemart', 'WasteMart'), ('managem', 'ManaGEM'), ('smartstart', 'SmartStart'),
    ('ecd-connect', 'ECD Connect'), ('homeassist', 'HomeAssist'),
    ('sbs-waterproofing', 'SBS Waterproofing'), ('trans-hex', 'Trans Hex Group'),
    ('sonke', 'Sonke Gender Justice'), ('tores-foundation', "Tore's Foundation"),
]

# 05 · capabilities a visitor can engage GEMIS for, each tied to the projects
# that demonstrate it. Only capabilities with evidence on the site are listed.
CAPABILITIES = [
    ('Business systems and ERP',
     'One system for enquiries, quotes, jobs, deposits, stock and staff, designed around the sequence the business actually follows rather than a package’s.',
     ['custom-software', 'enterprise-saas'], ['sbs-waterproofing', 'wastemart', 'managem']),
    ('Custom software and digital platforms',
     'Web platforms built for a specific programme or operation: a schools debating competition with its claims and payments, a national plumbing-claims operation.',
     ['custom-software'], ['tores-foundation', 'homeassist']),
    ('Mobile and field operations',
     'Apps for the people doing the work: offline session capture, automatic dispatch, scan confirmation at the point of collection, photographic evidence on site.',
     ['mobile-apps'], ['sonke', 'wastemart', 'homeassist']),
    ('System integration and reporting',
     'Feeds between the systems a business already runs — SAP, accounting, insurers and manufacturers — and the management reports built on top of them.',
     ['system-integration', 'business-intelligence'], ['trans-hex', 'sbs-waterproofing', 'homeassist']),
    ('Digital product and UX design',
     'Interface and product design from GEMIS Studio, the design practice inside the company, for systems people have to use every day.',
     ['ux-design'], []),
    ('Ongoing support and system evolution',
     'We stay after go-live. The three founding clients from 2014 still run on the systems we built them, and the Trans Hex report went to a second version.',
     ['support', 'modernisation'], ['sbs-waterproofing', 'homeassist', 'wastemart', 'trans-hex']),
]

def nl_join(it):
    return chr(10).join(it)


def link_for(slug, base=''):
    return f'{base}products/managem/' if S.BY_SLUG[slug].get('is_product') else f'{base}work/{slug}/'


def hero():
    # the hero as it was before the redesign (restored at the owner's request):
    # the tagline leads, the partner line sits in the corner, no mock-ups
    return '''    <section class="hero" id="hero">
      <img class="hero__bg" src="assets/img/home/hero-bg.jpg" alt="" aria-hidden="true" />

      <div class="shell hero__in">
        <p class="eyebrow eyebrow--light" data-reveal>Business systems partner since 2014</p>
        <h1 class="hero__title" data-reveal style="--d:80ms">Systems built to last. Partners built to stay.</h1>
        <p class="hero__copy" data-reveal style="--d:160ms">
          We build software around how your business actually works, and we stay to
          support it as you grow. Some of our clients have been with us for more than
          a decade.
        </p>
        <div class="hero__ctas" data-reveal style="--d:240ms">
          <a class="arrow-link" href="#discovery">
            Book a Discovery Session
            <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M2.5 9.5 9.5 2.5M4 2.5h5.5V8"/></svg>
          </a>
          <a class="arrow-link arrow-link--quiet" href="#selected">
            See our work
            <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M2.5 9.5 9.5 2.5M4 2.5h5.5V8"/></svg>
          </a>
        </div>
      </div>

        <!-- The Microsoft four-square mark is drawn inline. The exact partner
             designation and official badge artwork are still to be supplied —
             see OPEN_ITEMS.md (microsoft-partner-badge). -->
        <aside class="hero__partner" data-reveal style="--d:320ms" aria-label="Microsoft partnership" data-tbc="microsoft-partner-badge" data-kind="hideable">
          <svg viewBox="0 0 21 21" aria-hidden="true"><rect x="0" y="0" width="10" height="10" fill="#f25022"/><rect x="11" y="0" width="10" height="10" fill="#7fba00"/><rect x="0" y="11" width="10" height="10" fill="#00a4ef"/><rect x="11" y="11" width="10" height="10" fill="#ffb900"/></svg>
          <span class="hero__partner-name">Microsoft Partner</span>
          <span class="hero__partner-line">Systems built and run on the Microsoft Cloud <span class="tbc" data-tbc="microsoft-partner-badge" data-kind="hideable">designation to confirm</span></span>
        </aside>
    </section>

    <!-- ═══════════════════ 02 · ABOUT / TRUST ═══════════════════
         The design reference: eyebrow and a two-line headline on the left, a
         paragraph and three figures on the right, a faint plus-grid top-left.
         The figures are the ones Our Story carries. Below it, the marquee of
         every client with a story on the site plus our own product — on
         wordmarks, since no logo files exist (OPEN_ITEMS.md). -->
'''

def trust():
    # the stats section as it was: About GEMIS, the three confirmed figures, the
    # owner's client logos
    return '''
    <section class="trust band plusgrid" aria-labelledby="trustHeading">
      <div class="shell">
        <div class="trust__grid">
          <div class="trust__lead">
            <p class="eyebrow" data-reveal>About GEMIS</p>
            <h2 class="display" id="trustHeading" data-reveal style="--d:80ms">Trusted by South African businesses.</h2>
            <a class="btn" href="our-story/" data-reveal style="--d:140ms">Learn more about us <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M2.5 9.5 9.5 2.5M4 2.5h5.5V8"/></svg></a>
          </div>
          <div class="trust__body">
            <p class="trust__copy" data-reveal style="--d:140ms">
              GEM Information Systems has been building business systems in South Africa since
              2014 — and still works with the businesses it started with. We design around how a
              business actually runs, build on the Microsoft Cloud, and stay after go-live.
            </p>
            <ul class="trust__stats" data-reveal style="--d:200ms">
              <li class="stat"><span class="stat__n" data-count="12" data-sup="+">12<sup>+</sup></span><span class="stat__l">Years building business systems</span></li>
              <li class="stat"><span class="stat__n" data-count="50" data-sup="+">50<sup>+</sup></span><span class="stat__l">Systems delivered into production</span></li>
              <li class="stat"><span class="stat__n" data-count="5" data-sup="+">5<sup>+</sup></span><span class="stat__l">Sectors served nationally</span></li>
            </ul>
          </div>
        </div>

        <div class="marquee" data-reveal style="--d:260ms">
          <ul class="marquee__track">
            <li class="marquee__item"><img src="assets/img/logos/clients/wastemart-grey.png" alt="WasteMart" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img src="assets/img/logos/clients/managem-grey.png" alt="ManaGEM" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img src="assets/img/logos/clients/smartstart-grey.png" alt="SmartStart" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img src="assets/img/logos/clients/ecd-connect-grey.png" alt="ECD Connect" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img src="assets/img/logos/clients/homeassist-grey.png" alt="HomeAssist" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img src="assets/img/logos/clients/sbs-waterproofing-grey.png" alt="SBS Waterproofing" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img src="assets/img/logos/clients/trans-hex-grey.png" alt="Trans Hex Group" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img src="assets/img/logos/clients/sonke-grey.png" alt="Sonke Gender Justice" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img src="assets/img/logos/clients/tores-foundation-grey.png" alt="Tore&#x27;s Foundation" height="56" loading="lazy" /></li>
          </ul>
          <ul class="marquee__track" aria-hidden="true">
            <li class="marquee__item"><img aria-hidden="true" src="assets/img/logos/clients/wastemart-grey.png" alt="WasteMart" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img aria-hidden="true" src="assets/img/logos/clients/managem-grey.png" alt="ManaGEM" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img aria-hidden="true" src="assets/img/logos/clients/smartstart-grey.png" alt="SmartStart" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img aria-hidden="true" src="assets/img/logos/clients/ecd-connect-grey.png" alt="ECD Connect" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img aria-hidden="true" src="assets/img/logos/clients/homeassist-grey.png" alt="HomeAssist" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img aria-hidden="true" src="assets/img/logos/clients/sbs-waterproofing-grey.png" alt="SBS Waterproofing" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img aria-hidden="true" src="assets/img/logos/clients/trans-hex-grey.png" alt="Trans Hex Group" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img aria-hidden="true" src="assets/img/logos/clients/sonke-grey.png" alt="Sonke Gender Justice" height="56" loading="lazy" /></li>
            <li class="marquee__item"><img aria-hidden="true" src="assets/img/logos/clients/tores-foundation-grey.png" alt="Tore&#x27;s Foundation" height="56" loading="lazy" /></li>
          </ul>
        </div>
      </div>
    </section>
'''

def selected():
    """
    Selected work & case studies: the site's shared section header, then the
    horizontal travel — a white band pinned to the viewport while four
    equal-height case study cards, two to a screen on desktop, travel across
    as the page scrolls (home.js, [data-hscroll]); on tablets and phones the
    cards sit on a plain grid instead. Every card plays its case study video.
    The band closes on the transition statement, which scales up as it is
    scrolled to the centre of the viewport, holds, then releases
    ([data-scaleup]; static under reduced motion and without JavaScript).
    """
    picks = ['managem', 'wastemart', 'homeassist', 'sonke']
    cards = []
    for i, k in enumerate(picks):
        st = S.BY_SLUG[k]
        c = C.CASES.get(k, {})
        line = (c.get('value') or st['summary']).split('. ')[0].rstrip('.') + '.'
        cards.append(f'''          <li class="selw__card" data-reveal style="--d:{(i % 2) * 80}ms">
            <div class="selw__media">
              <img src="{S.VIDEO_DIR}{st['video']}_thumb.jpg" alt="" loading="lazy" width="1280" height="720" />
              <a class="selw__play" {B.play_attrs(st, '')} aria-label="Play the {esc(st['client'])} story">{PLAY}<span>Play story</span></a>
              <span class="selw__len" aria-hidden="true">{st['duration_label']}</span>
            </div>
            <div class="selw__body">
              <p class="selw__tag">{esc(st['industry'])}</p>
              <h3 class="selw__name"><a href="{link_for(k)}">{esc(st['client'])}</a></h3>
              <p class="selw__line">{esc(line)}</p>
              <a class="arrow-link arrow-link--quiet selw__go" href="{link_for(k)}">Explore project {ARROW}</a>
            </div>
          </li>''')
    nl = chr(10)
    return f'''
    <!-- ═══════════════════ 03 · SELECTED WORK ═══════════════════
         The shared header, then four case study cards on a horizontal travel
         pinned to the viewport (home.js, [data-hscroll]; a grid on tablets and
         phones), then the transition statement that scales up on scroll
         ([data-scaleup]). Static under reduced motion and without JavaScript. -->
    <section class="selw" id="selected" aria-labelledby="selectedHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>Selected work</p>
            <h2 class="display" id="selectedHeading" data-reveal style="--d:80ms">Selected work &amp; case studies</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">Four systems in production, each with the story of what the business needed and what was built. <a class="arrow-link" href="work/">View all projects {ARROW}</a></p>
        </div>
      </div>
      <div class="selw__travel" data-hscroll>
        <div class="selw__pin">
          <ol class="selw__track" data-track>
{nl.join(cards)}
          </ol>
        </div>
      </div>
      <div class="selw__out" data-scaleup>
        <div class="selw__out-pin">
          <p class="selw__statement">Discover the complete collection of systems, platforms and products GEMIS has built.</p>
          <a class="arrow-link selw__out-link" href="work/">View all projects {ARROW}</a>
        </div>
      </div>
    </section>
'''



def in_their_words():
    """The home's In their words: the shared stage from build-stories, links from the root."""
    if not any(S.ENDORSERS[k].get('line') for k in S.ENDORSEMENT_ORDER):
        print('home: no quotation in endorsements.md yet — "In their words" shows "Quotation to follow." (owner\'s instruction)')
    return B.in_their_words('')

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

def operating_logic():
    """
    "Operating principles": the four principles that connect the seven systems,
    as a sticky index and a ruled list. The left column holds the label, the
    statement and a large index numeral; the right column lists the four
    principles as numbered ruled rows — statement, evidence, "Seen in" links.
    As the visitor scrolls, the row at the reading line is the one in full
    white and the numeral follows it (home.js, [data-principles]); without
    JavaScript, under reduced motion and on narrow screens every row is full
    and nothing moves. Every statement and line of copy is verbatim.
    """
    rows, nums, ticks = [], [], []
    for i, p in enumerate(OPERATING):
        seen = ' '.join(f'<li><a href="{link_for(k)}">{esc(S.BY_SLUG[k]["client"])}</a></li>' for k in p['seen'])
        rows.append(f'''          <li class="prin__row{' is-active' if i == 0 else ''}" data-prin-row data-reveal style="--d:{i * 70}ms">
            <span class="prin__n" aria-hidden="true">{p['n']}</span>
            <div class="prin__body">
              <h3 class="prin__statement">{esc(p['statement'])}</h3>
              <p class="prin__copy">{esc(p['copy'])}</p>
              <div class="prin__seen"><span class="prin__seen-label">Seen in</span><ul class="prin__seen-list">{seen}</ul></div>
            </div>
          </li>''')
        nums.append(f'<span class="prin__num{" is-on" if i == 0 else ""}" data-prin-num>{p["n"]}</span>')
        ticks.append(f'<span class="prin__tick{" is-on" if i == 0 else ""}" data-prin-tick></span>')
    reads = ' '.join(f'<li><a href="insights/{a["slug"]}/">{esc(a["title"])}</a></li>' for a in SV.ARTICLES)
    nl = chr(10)
    return f'''
    <!-- ═══════════════════ 05 · OPERATING PRINCIPLES ═══════════════════
         Four principles connecting seven systems: a sticky index on the left,
         four numbered ruled rows on the right; the row at the reading line is
         the live one (home.js, [data-principles]). Verbatim copy. -->
    <section class="prin band-ink" id="thinking" aria-labelledby="opHeading" data-principles>
      <div class="shell prin__in">
        <div class="prin__side">
          <div class="prin__sticky">
            <p class="prin__label" data-reveal>GEMIS <span aria-hidden="true">/</span> Operating principles</p>
            <h2 class="prin__title" id="opHeading" data-reveal style="--d:80ms">Seven systems. The same four decisions.</h2>
            <div class="prin__index" aria-hidden="true" data-reveal style="--d:160ms">
              <span class="prin__nums">{''.join(nums)}</span>
              <span class="prin__ticks">{''.join(ticks)}</span>
              <span class="prin__of">of 04</span>
            </div>
          </div>
        </div>
        <ol class="prin__list">
{nl.join(rows)}
        </ol>
        <footer class="prin__foot" data-reveal>
          <p class="prin__foot-label">Read more of our thinking:</p>
          <ul class="prin__reads">{reads}</ul>
        </footer>
      </div>
    </section>
'''


def capabilities():
    rows = []
    for name, copy, services, projects in CAPABILITIES:
        chips = [f'<a href="{link_for(k)}">{esc(S.BY_SLUG[k]["client"])}</a>' for k in projects]
        if not projects:
            chips = ['<a href="studio/">GEMIS Studio</a>']
        links = ' &middot; '.join(
            f'<a class="arrow-link arrow-link--quiet" href="solutions/{k}/">{esc(SV.BY_SLUG[k]["name"])} {ARROW}</a>'
            for k in services)
        rows.append((esc(name), f'<p>{esc(copy)}</p>', chips, f'<p class="srow__links">{links}</p>'))
    # chips are already markup, so the helper must not escape them
    out = []
    for i, (name, body, chips, link) in enumerate(rows):
        chip_html = ('\n              <ul class="srow__chips">\n'
                     + '\n'.join(f'                <li>{c}</li>' for c in chips)
                     + '\n              </ul>')
        out.append(f'''          <li class="srow" data-reveal style="--d:{i * 60}ms">
            <span class="srow__n" aria-hidden="true">{i + 1:02d}</span>
            <h3 class="srow__name">{name}</h3>
            <div class="srow__body">
              {body}{chip_html}
              {link}
            </div>
          </li>''')
    nl = chr(10)
    return f'''
    <!-- ═══════════════════ 05 · CAPABILITIES, DEMONSTRATED ═══════════════════
         What a visitor can engage GEMIS for, each tied to the projects that
         show it running. Only capabilities with evidence on the site. -->
    <section class="capmap band plusgrid plusgrid--br" id="capabilities" aria-labelledby="capHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>Capabilities, demonstrated</p>
            <h2 class="display" id="capHeading" data-reveal style="--d:80ms">What you can engage GEMIS for, and where each has run</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">Every capability below is tied to a system in production. <a class="arrow-link" href="solutions/">All solutions {ARROW}</a></p>
        </div>
        <ol class="srows">
{nl.join(out)}
        </ol>
      </div>
    </section>
'''


def stories():
    # the stories panel: the founding relationships on video, with their tags
    return f'''
    <!-- ═══════════════════ 06 · BUILT TOGETHER ═══════════════════ -->
{B.stories_section('')}
'''


def ways():
    return f'''
    <!-- ═══════════════════ 07 · HOW GEMIS WORKS ═══════════════════
         The company's own methodology, as the horizontal timeline. -->
    <section class="ways band" id="how" aria-labelledby="waysHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>How GEMIS works</p>
            <h2 class="display" id="waysHeading" data-reveal style="--d:80ms">Understand. Design. Build. Evolve.</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">One agreed statement of the problem before a screen is drawn; demonstrated sprints so there are no surprises at go-live; and the same team afterwards. <a class="arrow-link" href="solutions/">See how we work {ARROW}</a></p>
        </div>
{B.tline(SV.WAYS)}
      </div>
    </section>
'''


def company():
    return f'''
    <!-- ═══════════════════ 08 · THE COMPANY ═══════════════════
         Who is behind the work, from the company's own profile. Team titles
         beyond the one confirmed are held back (OPEN_ITEMS: team-titles). -->
    <section class="cred-sec band band-wash plusgrid plusgrid--tr" id="company" aria-labelledby="companyHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>The company</p>
            <h2 class="display" id="companyHeading" data-reveal style="--d:80ms">Who is behind the work</h2>
          </div>
        </div>
        <div class="cred">
          <div class="story__prose" data-reveal style="--d:120ms">
            <p>GEM Information Systems was founded in Cape Town in 2014, building systems for small and medium businesses and non-profits where budgets were tight and the system had to work from day one. The clients grew, and so did the work: ERP platforms, national field operations, monitoring and evaluation across Africa, integrated reporting for a mining group.</p>
            <p>The Microsoft Cloud has been the foundation throughout &mdash; Azure, Azure SQL, C# and Power BI &mdash; and one accountable team stays with a system from the first conversation through to support, with GEMIS Studio handling the design.</p>
            <p><a class="arrow-link" href="our-story/">Our story {ARROW}</a></p>
          </div>
          <dl class="cred__facts" data-reveal style="--d:180ms">
            <div><dt>Founded</dt><dd>2014, Cape Town</dd></div>
            <div><dt>Platform</dt><dd>Microsoft Azure, Azure SQL, C#, Power BI</dd></div>
            <div><dt>Founding clients</dt><dd>Three, from 2014, all still running on their systems</dd></div>
            <div><dt>Design practice</dt><dd><a href="studio/">GEMIS Studio</a></dd></div>
            <div><dt>Product</dt><dd><a href="products/managem/">ManaGEM</a>, run by about a dozen companies</dd></div>
            <div><dt>Office</dt><dd>9 Tapiola Way, Edgemead, Cape Town</dd></div>
          </dl>
        </div>
      </div>
    </section>
'''


def enquiry():
    # Book a Discovery Session, with the form, as it was before the redesign
    return '''
    <!-- ═══════════════════ 07 · GET STARTED ═══════════════════
         The form hands off to the visitor's email client (this site is static);
         nothing is stored. The three steps mirror contact.html. -->
    <section class="go" id="discovery" aria-labelledby="goHeading">
      <div class="shell go__grid">
        <div class="go__intro">
          <p class="eyebrow" data-reveal>Get started</p>
          <h2 class="display" id="goHeading" data-reveal style="--d:80ms">Book a Discovery Session</h2>
          <p class="lede" data-reveal style="--d:140ms">
            Tell us what you're trying to fix. We'll come back within two working days with a
            short written view and a time to talk. No obligation.
          </p>
          <ol class="go__steps" data-reveal style="--d:200ms">
            <li><span class="go__n">01</span><div><strong>We read it properly</strong><p>Your enquiry reaches a monitored GEMIS mailbox, not a personal address. A person who has read it replies.</p></div></li>
            <li><span class="go__n">02</span><div><strong>A discovery conversation</strong><p>We map how your organisation actually works — the goals, the friction and the constraints — before anyone proposes a system.</p></div></li>
            <li><span class="go__n">03</span><div><strong>A scoped way forward</strong><p>You get an architecture, a plan and a cost you can act on. If we're not the right fit, we'll say so.</p></div></li>
          </ol>
          <div class="go__contact" data-reveal style="--d:260ms">
            <p><span>Email</span><a href="mailto:info@gemis.co.za">info@gemis.co.za</a></p>
            <p><span>Cape Town</span>9 Tapiola Way, Edgemead</p>
          </div>
        </div>

          <form class="form" id="discoveryForm" novalidate data-reveal style="--d:160ms">
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

            <button class="form__send" type="submit">
              Book a Discovery Session
              <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M2.5 9.5 9.5 2.5M4 2.5h5.5V8"/></svg>
            </button>

            <p class="form__note" id="discoveryNote" role="status" aria-live="polite">
              This site is static, so sending opens a pre-filled message in your email
              client addressed to info@gemis.co.za — nothing is submitted or stored here.
            </p>
          </form>
      </div>
    </section>

''' + B.video_modal() + '\n'

def home_main():
    return hero() + trust() + selected() + in_their_words() + operating_logic() + enquiry()


if __name__ == '__main__':
    index = os.path.join(ROOT, 'index.html')
    B.fill_slot(index, 'home', home_main())
    print('index.html: the nine homepage sections written')
