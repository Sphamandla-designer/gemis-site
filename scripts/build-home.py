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

# 04 · the thinking: three workflows as implemented, drawn from the case studies
THINKING = [
    ('sbs-waterproofing', 'The enquiry as the root record',
     'Leads were being lost between a website, a spreadsheet and three apps. Making the enquiry the one record that every call, quote, deposit and job hangs off is what let SBS Waterproofing keep up with its own growth — and the same structure became ManaGEM.'),
    ('wastemart', 'Each step triggers the next',
     'Four manual jobs sat behind one phone call at WasteMart. The design removes every hand-off that depended on someone remembering: the quote carries its terms, payment puts the job on the schedule, the driver’s scan closes the loop.'),
    ('trans-hex', 'Make the feed reliable, and make failure visible',
     'A management report assembled by hand from several sources took weeks and collected errors. Stabilise the foundation first, automate the SAP feed so that it logs every run and emails the team when it fails, then build the report into the system itself.'),
]


def link_for(slug, base=''):
    return f'{base}products/managem/' if S.BY_SLUG[slug].get('is_product') else f'{base}work/{slug}/'


def hero():
    return f'''    <!-- ═══════════════════ 01 · HERO ═══════════════════
         The proposition leads; the brand promise is its support line. The
         ground is the owner's hero photograph; no mock-ups in any hero. -->
    <section class="hero" id="hero">
      <img class="hero__bg" src="assets/img/home/hero-bg.jpg" alt="" aria-hidden="true" />

      <div class="shell hero__in">
        <p class="hero__tag" data-reveal>Systems built to last. Partners built to stay.</p>
        <h1 class="hero__title" data-reveal style="--d:80ms">Systems your operation can run on &mdash; not work around.</h1>
        <p class="hero__copy" data-reveal style="--d:160ms">
          GEMIS builds business systems around how an organisation actually works &mdash; the
          enquiry, the job, the claim, the report &mdash; and stays to support them as the
          business changes. Three of our first clients, from 2014, still run on the systems
          we built them.
        </p>
        <div class="hero__ctas" data-reveal style="--d:240ms">
          <a class="btn" href="work/">Explore our work {ARROW}</a>
          <a class="arrow-link arrow-link--quiet" href="contact.html">Discuss a project {ARROW}</a>
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
'''


def featured():
    m = S.BY_SLUG['managem']
    v = f'{S.VIDEO_DIR}{m["video"]}'
    return f'''
    <!-- ═══════════════════ 02 · FEATURED CASE STUDY ═══════════════════
         The strongest evidence first: ManaGEM, with its documented origin at
         SBS Waterproofing. Every line is from the two case study videos and
         facts.md; the one figure is client-confirmed. -->
    <section class="featured band plusgrid plusgrid--tr" id="featured" aria-labelledby="featuredHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>Featured case study</p>
            <h2 class="display" id="featuredHeading" data-reveal style="--d:80ms">ManaGEM: the system one business needed, now run by about a dozen</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">A Cape Town waterproofing contractor had outgrown its apps. The system GEMIS built for it in 2015 was designed from day one to work for other businesses too, and became a product.</p>
        </div>
        <div class="featured__grid">
          <div class="featured__visual" data-reveal>
            <img src="{v}_thumb.jpg" alt="A frame from the ManaGEM case study video: quotes accepted online, deposit invoices sent automatically" width="1280" height="720" loading="lazy" />
            <a class="featured__play" {B.play_attrs(m, '')} aria-label="Play the ManaGEM story">{PLAY}</a>
            <span class="featured__len" aria-hidden="true">{m['duration_label']}</span>
          </div>
          <dl class="featured__facts" data-reveal style="--d:80ms">
            <div><dt>Business context</dt><dd>Business management software for growing SMEs. Developed from the system built for SBS Waterproofing in 2015.</dd></div>
            <div><dt>The challenge</dt><dd>Most growing businesses hit the same wall: enquiries, quotes, jobs and stock scattered across tools and spreadsheets. Off-the-shelf packages did not fit how SBS worked.</dd></div>
            <div><dt>GEMIS&rsquo;s contribution</dt><dd>Designed and built the system around SBS&rsquo;s own pipeline, generalised it into a platform, and runs and supports it today.</dd></div>
            <div><dt>The solution</dt><dd>Every enquiry followed to the sale with SMS and email updates; quotes accepted online with deposit invoices raised automatically; profit per project; stock alerts; products, prices and staff in one place.</dd></div>
            <div><dt>Verified</dt><dd>About a dozen companies run their day-to-day operations on ManaGEM. One client confirms its month-end close went from nine days to two.</dd></div>
          </dl>
          <div class="featured__actions" data-reveal style="--d:140ms">
            <a class="btn" href="products/managem/">Read the case study {ARROW}</a>
            <a class="btn btn--ghost" {B.play_attrs(m, '')}>{PLAY} Play story</a>
            <a class="arrow-link arrow-link--quiet" href="work/sbs-waterproofing/">Where it came from: SBS Waterproofing {ARROW}</a>
          </div>
        </div>
      </div>
    </section>
'''


def selected():
    cards = '\n'.join([
        B.cscard(S.BY_SLUG['wastemart'], '', 0, wide=True),
        B.cscard(S.BY_SLUG['homeassist'], '', 1),
        B.cscard(S.BY_SLUG['sonke'], '', 2),
    ])
    return f'''
    <!-- ═══════════════════ 03 · SELECTED PROJECTS ═══════════════════
         Three different kinds of problem: an operations chain, a national
         service and claims workflow, and monitoring and evaluation for a
         non-profit. The same card as the Case Studies index. -->
    <section class="sel-sec band band-wash" id="selected" aria-labelledby="selectedHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>Selected projects</p>
            <h2 class="display" id="selectedHeading" data-reveal style="--d:80ms">Three different problems, one way of working</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">An operations chain from call to collection, a national claims workflow, and field data that has to be trusted by funders. <a class="arrow-link" href="work/">All case studies {ARROW}</a></p>
        </div>
        <div class="sel">
{cards}
        </div>
      </div>
    </section>
'''


def thinking():
    items = []
    for i, (slug, title, copy) in enumerate(THINKING):
        c = C.CASES[slug]
        s = S.BY_SLUG[slug]
        items.append(f'''        <div class="think__item" data-reveal style="--d:{i * 60}ms">
          <div>
            <p class="think__kicker">{esc(s['client'])}</p>
            <h3 class="think__t">{esc(title)}</h3>
            <p class="think__c">{esc(copy)}</p>
            <a class="arrow-link arrow-link--quiet" href="{link_for(slug)}">Read the case study {ARROW}</a>
          </div>
          <div>
{B.flow(c['flow'], c.get('flow_label', ''))}
          </div>
        </div>''')
    nl = chr(10)
    return f'''
    <!-- ═══════════════════ 04 · THE THINKING ═══════════════════
         Three workflows as implemented, drawn from the case study narration.
         Each is a decision about where work is captured and what triggers the
         next step. They are diagrams of verified information, not mock-ups. -->
    <section class="think-sec band" id="thinking" aria-labelledby="thinkingHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>The thinking behind the work</p>
            <h2 class="display" id="thinkingHeading" data-reveal style="--d:80ms">How the problem was structured before anything was built</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">Three workflows as they run today, drawn from the case studies. The decision in each one is where the work is captured and what triggers the next step.</p>
        </div>
        <div class="think">
{nl.join(items)}
        </div>
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
    <section class="capmap band band-tint plusgrid plusgrid--br" id="capabilities" aria-labelledby="capHeading">
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


def proof():
    logos = '\n'.join(
        f'            <li class="marquee__item"><img src="assets/img/logos/clients/{k}-grey.png" alt="{esc(n)}" height="56" loading="lazy" /></li>'
        for k, n in LOGOS)
    logos_dup = '\n'.join(
        f'            <li class="marquee__item"><img aria-hidden="true" src="assets/img/logos/clients/{k}-grey.png" alt="" height="56" loading="lazy" /></li>'
        for k, n in LOGOS)
    return f'''
    <!-- ═══════════════════ 06 · LONG-TERM PARTNERSHIP ═══════════════════
         Genuine evidence of continuity: three confirmed figures, the two
         client-confirmed results, the owner-supplied client logos, and then
         the stories panel with the founding relationships on video. No
         testimonial is shown until an approved line exists. -->
    <section class="proof band" id="proof" aria-labelledby="proofHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>Long-term partnership</p>
            <h2 class="display" id="proofHeading" data-reveal style="--d:80ms">Still running, more than a decade on</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">The age of a relationship is not the age of a system. SBS Waterproofing, HomeAssist and WasteMart have worked with GEMIS since 2014, and the systems built for them have been extended, not replaced.</p>
        </div>
        <ul class="trust__stats" data-reveal style="--d:160ms">
          <li class="stat"><span class="stat__n" data-count="12" data-sup="+">12<sup>+</sup></span><span class="stat__l">Years building business systems</span></li>
          <li class="stat"><span class="stat__n" data-count="50" data-sup="+">50<sup>+</sup></span><span class="stat__l">Systems delivered into production</span></li>
          <li class="stat"><span class="stat__n" data-count="5" data-sup="+">5<sup>+</sup></span><span class="stat__l">Sectors served nationally</span></li>
        </ul>
        <ul class="rlist" data-reveal style="--d:200ms" aria-label="Results confirmed by clients">
          <li><a href="work/wastemart/"><span class="post__plus" aria-hidden="true">+</span><span>WasteMart: six hours a week back, per depot &mdash; confirmed by the client</span></a></li>
          <li><a href="products/managem/"><span class="post__plus" aria-hidden="true">+</span><span>ManaGEM: month-end close from nine days to two &mdash; confirmed by the client</span></a></li>
        </ul>
        <p class="proof__note" data-reveal style="--d:220ms">Clients and products GEMIS has built for.</p>
        <div class="marquee" data-reveal style="--d:260ms">
          <ul class="marquee__track">
{logos}
          </ul>
          <ul class="marquee__track" aria-hidden="true">
{logos_dup}
          </ul>
        </div>
      </div>
    </section>

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
    return (hero() + featured() + selected() + thinking() + capabilities() + proof()
            + ways() + company() + enquiry())


if __name__ == '__main__':
    index = os.path.join(ROOT, 'index.html')
    B.fill_slot(index, 'home', home_main())
    print('index.html: the nine homepage sections written')
