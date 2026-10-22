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
          <a class="arrow-link" href="contact.html">
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
    Selected work, after the owner's reference (the Trionn "Selected work &
    explorations" screenshots): a white band pinned to the viewport while four
    large project cards travel across it as the page scrolls, then a closing
    panel that points to every case study. The markup is a plain list; without
    JavaScript, on a phone, or under reduced motion it stacks vertically.
    """
    picks = ['managem', 'wastemart', 'homeassist', 'sonke']
    cards = []
    for i, k in enumerate(picks):
        st = S.BY_SLUG[k]
        c = C.CASES.get(k, {})
        line = c.get('value') or st['summary']
        line = line.split('. ')[0].rstrip('.') + '.'
        cards.append(f'''          <li class="selw__item selw__card" data-reveal style="--d:{i * 80}ms">
            <a class="selw__media" href="{link_for(k)}" tabindex="-1" aria-hidden="true">
              <img src="{S.VIDEO_DIR}{st['video']}_thumb.jpg" alt="" loading="lazy" width="1280" height="720" />
            </a>
            <h3 class="selw__name"><a href="{link_for(k)}">{esc(st['client'])}</a></h3>
            <div class="selw__row">
              <p class="selw__line">{esc(st['headline'])}. {esc(line)}</p>
              <a class="selw__more" href="{link_for(k)}">Explore project {ARROW}</a>
            </div>
          </li>''')
    nl = chr(10)
    return f'''
    <!-- ═══════════════════ 03 · SELECTED WORK ═══════════════════
         The owner's reference: a pinned white band, the heading on the left,
         four large project cards travelling across as the page scrolls, and a
         closing panel to every case study. assets/js/home.js drives the pin;
         the list stacks without it. -->
    <section class="selw" id="selected" aria-labelledby="selectedHeading" data-hscroll>
      <div class="selw__pin">
        <ol class="selw__track" data-track>
          <li class="selw__item selw__head">
            <h2 class="display" id="selectedHeading" data-reveal>Selected work<br />&amp; case studies</h2>
            <a class="selw__more" href="work/" data-reveal style="--d:80ms">View all projects {ARROW}</a>
          </li>
{nl.join(cards)}
          <li class="selw__item selw__end">
            <p class="selw__endline" data-reveal>Discover the complete collection of systems, platforms and products GEMIS has built.</p>
            <a class="selw__more" href="work/" data-reveal style="--d:80ms">View all projects {ARROW}</a>
          </li>
        </ol>
      </div>
    </section>
'''

# 04 · the overall thinking: the principles every system here was built on,
# each with the projects where it can be seen running
PRINCIPLES = [
    ('Capture once, where the work happens',
     'The enquiry, the session, the job: recorded at the moment it happens, by the person it happens to, and never re-keyed. If capture depends on an office or a signal, the records that matter most are the ones lost.',
     ['sbs-waterproofing', 'sonke', 'homeassist']),
    ('Let each step trigger the next',
     'The hand-offs that leak time are the ones that depend on someone remembering. An accepted quote raises the invoice; a payment puts the job on the schedule; a scan closes it.',
     ['wastemart', 'sbs-waterproofing', 'managem']),
    ('Verify before you count, and make failure visible',
     'Nothing counts until it has been checked against a real activity, and automation that fails must fail loudly: a claim matched to a session, a record approved before it reaches a report, a feed that emails the team when a run is missed.',
     ['sonke', 'tores-foundation', 'trans-hex']),
    ('Build the report into the system',
     'A report assembled beside the system is late and wrong by the time it is read. Profit per job, progress against targets and the management pack come out of the same data the work is done in.',
     ['trans-hex', 'sonke', 'sbs-waterproofing']),
    ('Fit the real sequence of work, then generalise',
     'A system that follows how a business actually sells and delivers is the one it keeps using. Designed with a general core, the same system can serve others: that is how one contractor’s system became ManaGEM.',
     ['sbs-waterproofing', 'managem']),
    ('Stay after go-live',
     'A system is judged years later. Three founding clients from 2014 still run on theirs; the Trans Hex report went to a second version.',
     ['sbs-waterproofing', 'homeassist', 'wastemart', 'trans-hex']),
]

OVERALL_FLOW = [
    ('Capture', 'Once, where the work happens'),
    ('Trigger', 'Each step sets off the next'),
    ('Verify', 'Checked before it counts; failures surfaced'),
    ('Report', 'From the same data, on demand'),
    ('Evolve', 'Extended with the business, year on year'),
]


def thinking():
    rows = []
    for i, (name, copy, projects) in enumerate(PRINCIPLES):
        chips = nl_join(f'                <li><a href="{link_for(k)}">{esc(S.BY_SLUG[k]["client"])}</a></li>' for k in projects)
        rows.append(f'''          <li class="srow" data-reveal style="--d:{i * 60}ms">
            <span class="srow__n" aria-hidden="true">{i + 1:02d}</span>
            <h3 class="srow__name">{esc(name)}</h3>
            <div class="srow__body">
              <p>{esc(copy)}</p>
              <p class="srow__seen">Seen in</p>
              <ul class="srow__chips">
{chips}
              </ul>
            </div>
          </li>''')
    nl = chr(10)
    return f'''
    <!-- ═══════════════════ 04 · THE THINKING ═══════════════════
         The overall thinking: the pattern every system here follows, and the
         principles behind it, each pointing to the projects where it runs. -->
    <section class="think-sec capmap band band-wash plusgrid plusgrid--tr" id="thinking" aria-labelledby="thinkingHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>The thinking behind the work</p>
            <h2 class="display" id="thinkingHeading" data-reveal style="--d:80ms">Where work is captured, and what triggers the next step</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">Every system in the case studies follows the same pattern, decided before anything is built. The principles below are the ones the evidence supports; each names the projects where it can be seen running.</p>
        </div>
        <div class="story__flow story__flow--top" data-reveal style="--d:160ms">
{B.flow(OVERALL_FLOW, 'The pattern behind every GEMIS system')}
        </div>
        <ol class="srows">
{nl.join(rows)}
        </ol>
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
    return f'''
    <!-- ═══════════════════ 09 · THE ENQUIRY ═══════════════════
         The one conversion path. The form itself lives on contact.html. -->
    <section class="convert" id="discovery" aria-labelledby="convertHeading">
      <div class="shell convert__in">
        <p class="eyebrow" data-reveal>Your project</p>
        <h2 class="display" id="convertHeading" data-reveal style="--d:80ms">Have a business challenge worth solving?</h2>
        <p class="lede" data-reveal style="--d:140ms">Describe the operational problem &mdash; the spreadsheet that has become the system, the hand-off that keeps failing, the report that takes weeks. We come back within two working days with a short written view and a time to talk. No obligation.</p>
        <div class="convert__ctas" data-reveal style="--d:200ms">
          <a class="btn" href="contact.html">Discuss a project {ARROW}</a>
          <a class="arrow-link" href="solutions/">Explore our solutions {ARROW}</a>
        </div>
      </div>
    </section>

{B.video_modal()}
'''


def home_main():
    return (hero() + trust() + selected() + thinking() + capabilities() + stories()
            + ways() + company() + enquiry())


if __name__ == '__main__':
    index = os.path.join(ROOT, 'index.html')
    B.fill_slot(index, 'home', home_main())
    print('index.html: the nine homepage sections written')
