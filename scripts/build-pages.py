#!/usr/bin/env python3
"""
Generate Our Work and the six story pages.

The page shell — head, header, footer, scripts — is lifted from index.html so
there is one source for the chrome. scripts/apply-chrome.py then keeps the nav
and footer of every generated page in step with the rest of the site.

    python3 scripts/build-pages.py
"""
import html
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

spec = importlib.util.spec_from_file_location('stories', os.path.join(HERE, 'stories.py'))
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

bs_spec = importlib.util.spec_from_file_location('build_stories', os.path.join(HERE, 'build-stories.py'))
B = importlib.util.module_from_spec(bs_spec)
bs_spec.loader.exec_module(B)

esc, tbc, ARROW = B.esc, B.tbc, B.ARROW
c_spec = importlib.util.spec_from_file_location('cases', os.path.join(HERE, 'cases.py'))
C = importlib.util.module_from_spec(c_spec)
c_spec.loader.exec_module(C)
sv_spec = importlib.util.spec_from_file_location('services', os.path.join(HERE, 'services.py'))
SV = importlib.util.module_from_spec(sv_spec)
sv_spec.loader.exec_module(SV)
CANON = S.CANONICAL


def shell(base, title, description, canonical, extra_head=''):
    """head + header and footer + scripts, taken from the homepage."""
    src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    head_open, rest = src.split('<main>', 1)
    _, tail = rest.split('</main>', 1)

    # per-page metadata
    head_open = re.sub(r'<title>[^<]*</title>', f'<title>{esc(title)}</title>', head_open, count=1)
    for key in ('name="description"', 'property="og:title"', 'property="og:description"',
                'name="twitter:title"', 'name="twitter:description"'):
        value = title if 'title' in key else description
        head_open = re.sub(r'(<meta ' + re.escape(key) + r' content=")[^"]*(")',
                           lambda m: m.group(1) + esc(value) + m.group(2), head_open, count=1)
    head_open = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
                       lambda m: m.group(1) + canonical + m.group(2), head_open, count=1)
    head_open = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
                       lambda m: m.group(1) + canonical + m.group(2), head_open, count=1)

    # the homepage's Organization block belongs only to the homepage
    head_open = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', '', head_open, flags=re.S)
    if extra_head:
        head_open = head_open.replace('</head>', extra_head + '\n</head>', 1)

    # relative paths, since the site lives under /gemis-site/ and must never
    # use root-absolute ones
    def rebase(text):
        text = re.sub(r'(href|src)="(?!https?:|#|mailto:|tel:|data:|\.\./)([^"]+)"',
                      lambda m: f'{m.group(1)}="{base}{m.group(2)}"', text)
        return text

    # every page this shell builds opens on a light wave hero, so the bar is solid from the start
    head_open = head_open.replace('<header class="nav" id="nav">', '<header class="nav nav--photo" id="nav">', 1)
    return rebase(head_open) + '<main>\n', '</main>\n' + rebase(tail)


def video_schema(s, indent='  '):
    import json
    v = S.BASE_URL + s['video']
    data = {
        "@context": "https://schema.org", "@type": "VideoObject",
        "name": s['video_title'], "description": s['summary'],
        "duration": s['duration'], "inLanguage": "en", "uploadDate": "2026-10-21",
        "contentUrl": f"{v}_web.mp4", "thumbnailUrl": f"{v}_thumb.jpg",
        "transcript": s['transcript'], "keywords": s['keywords'],
        "publisher": {"@type": "Organization", "name": "GEM Information Systems (GEMIS)",
                      "url": CANON},
        "about": {"@type": s.get('about_type', 'Organization'), "name": s['about']},
    }
    return (f'{indent}<script type="application/ld+json">\n'
            f'{json.dumps(data, ensure_ascii=False, indent=2)}\n{indent}</script>')


# ── story page ───────────────────────────────────────────────────────────
def story_page(s):
    base = '../../'
    c = C.CASES[s['slug']]
    founding = s['slug'] in S.FOUNDING
    since = B.since_html(s)
    v = f'{base}{S.VIDEO_DIR}{s["video"]}'

    def li(items):
        return '\n'.join(f'            <li>{esc(x)}</li>' for x in items)

    def paras(items):
        return '\n'.join(f'          <p>{esc(x)}</p>' for x in items)

    principles, approach_paras = c['approach']
    overview = [
        ('Industry', s['industry']),
        ('Target users', c['users']),
        ('GEMIS’s role', c['role']),
        ('Scope', c['scope']),
    ]
    if c.get('timeframe'):
        overview.append(('Timeframe', c['timeframe']))
    overview.append(('Status', c['status']))
    overview.append(('Key deliverables', '; '.join(c['deliverables'])))
    ov = '\n'.join(f'''          <div class="ov__item" data-reveal style="--d:{i * 50}ms"><dt>{esc(k)}</dt><dd>{esc(val)}</dd></div>''' for i, (k, val) in enumerate(overview))

    endo = ''
    if founding and s['endorser'] and s['slug'] != 'sbs-waterproofing':
        # the HomeAssist words sit with the outcomes; a person with no line in
        # endorsements.md has no card live
        endo = f'''
        <div class="out__words">
          {B.endorsement_html(s['endorser'], base, story_link=False)}
        </div>'''
    challenge_words = ''
    if s['slug'] == 'sbs-waterproofing':
        # Ryan Smith's words describe the 2014 website and Google campaign, so
        # they sit in the part of the page about that work
        challenge_words = f'''
        <div class="chap__words" data-reveal style="--d:200ms">
          {B.endorsement_html('ryan-smith', base, story_link=False)}
        </div>'''

    verified = ''
    if c['outcomes']['verified']:
        verified = f'''
          <div class="out__col" data-reveal style="--d:80ms">
            <h3 class="out__h">Verified results</h3>
            <ul class="out__list">
{li(c['outcomes']['verified'])}
            </ul>
          </div>'''

    related = '\n'.join(B.cscard(S.BY_SLUG[k], base, i) for i, k in enumerate(c['related']))

    basis = ''
    if c.get('basis'):
        basis = f'''
    <section class="chap band" aria-labelledby="basisHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>Discovery and evidence</p>
            <h2 class="display" id="basisHeading" data-reveal style="--d:80ms">What the design was based on</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">Only the evidence that exists is described here. Nothing is labelled research that was not.</p>
        </div>
        <div class="story__prose story__prose--wide" data-reveal style="--d:160ms">
{paras(c['basis'])}
        </div>
      </div>
    </section>
'''

    structure = ''
    if c.get('flow'):
        structure = f'''
        <div class="story__flow" data-reveal style="--d:220ms">
          <h3 class="out__h">The workflow as implemented</h3>
{B.flow(c['flow'], c.get('flow_label', ''))}
        </div>'''

    walkthrough = ''
    if c.get('walk'):
        walkthrough = f'''
    <section class="chap band" id="walkthrough" aria-labelledby="walkHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>The system, step by step</p>
            <h2 class="display" id="walkHeading" data-reveal style="--d:80ms">What the user needs to do, and how the system supports it</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">Stills from the case study video. The interfaces are illustrated for the video, not screen recordings of the production system; every capability shown is one the system delivers.</p>
        </div>
{B.walk(c['walk'], base, s['slug'])}
      </div>
    </section>
'''

    decided = ''
    if c.get('decisions'):
        decided = f'''
    <section class="chap band band-tint plusgrid plusgrid--br" aria-labelledby="decHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>Key decisions</p>
            <h2 class="display" id="decHeading" data-reveal style="--d:80ms">Why it was built this way</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">The decisions the evidence supports: what needed addressing, what GEMIS chose, why, and what was delivered or observed.</p>
        </div>
{B.decisions(c['decisions'])}
      </div>
    </section>
'''

    validation = ''
    if c.get('validation'):
        vr = c['validation']
        validation = f'''
    <section class="chap band" aria-labelledby="valHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>Validation, delivery and iteration</p>
            <h2 class="display" id="valHeading" data-reveal style="--d:80ms">What the record shows</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">Delivery and continued use are the validation the repository can evidence. What it cannot, it says.</p>
        </div>
        <div class="rec">
          <div class="rec__col" data-reveal>
            <h3 class="out__h">On record</h3>
            <ul class="out__list">
{li(vr['record'])}
            </ul>
          </div>
          <div class="rec__col rec__col--quiet" data-reveal style="--d:80ms">
            <h3 class="out__h">Not documented</h3>
            <ul class="out__list">
{li(vr['not_recorded'])}
            </ul>
          </div>
        </div>
      </div>
    </section>
'''

    head = shell(
        base,
        f"{s['client']} — {s['headline']} | GEMIS®",
        c['value'][:180],
        f"{CANON}work/{s['slug']}/",
        extra_head=video_schema(s),
    )

    body = f'''
    <!-- ═══════════ {s['client'].upper()} ═══════════ -->
    <section class="chero cshero cshero--story" id="hero">
      <div class="shell cshero__in">
        <div class="cshero__text">
          <p class="chero__kicker" data-reveal>Case study · {esc(s['industry'])}</p>
          <h1 class="chero__title" data-reveal style="--d:80ms">{B.two_lines(esc(s['client']))}</h1>
          <p class="cshero__headline" data-reveal style="--d:120ms">{esc(s['headline'])}</p>
          <p class="chero__copy" data-reveal style="--d:160ms">{esc(c['value'])}</p>
          <p class="cshero__status" data-reveal style="--d:200ms"><span class="cshero__dot" aria-hidden="true"></span>{esc(c['status'])}</p>
          <div class="cshero__ctas" data-reveal style="--d:240ms">
            <a class="btn" {B.play_attrs(s, base)}>{B.PLAY} Play story</a>
            <a class="arrow-link" href="{base}contact.html">Discuss a similar challenge {ARROW}</a>
          </div>
        </div>
        <div class="cshero__visual" data-reveal style="--d:200ms">
          <img src="{v}_thumb.jpg" alt="A frame from the {esc(s['client'])} case study video" width="1280" height="720" />
          <a class="featured__play" {B.play_attrs(s, base)} aria-label="Play the {esc(s['client'])} story">{B.PLAY}</a>
          <span class="featured__len" aria-hidden="true">{s['duration_label']}</span>
        </div>
      </div>
    </section>

    <section class="ov band" id="overview" aria-labelledby="overviewHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>Project overview</p>
            <h2 class="display" id="overviewHeading" data-reveal style="--d:80ms">Project snapshot</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">Responsibilities and status, stated plainly. Where the record is silent — a date, a measured result — the page says so rather than guessing.</p>
        </div>
        <dl class="ov__grid">
{ov}
        </dl>
      </div>
    </section>

    <section class="chap band band-tint plusgrid plusgrid--tr" aria-labelledby="challengeHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>The business challenge</p>
            <h2 class="display" id="challengeHeading" data-reveal style="--d:80ms">{esc(s['headline'])}</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">{esc(s['challenge'])}.</p>
        </div>
        <div class="story__prose story__prose--wide" data-reveal style="--d:160ms">
{paras(c['challenge'])}
        </div>{challenge_words}
      </div>
    </section>

{basis}
    <section class="chap band band-wash" aria-labelledby="approachHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>Strategy and system structure</p>
            <h2 class="display" id="approachHeading" data-reveal style="--d:80ms">Why this approach fits the problem</h2>
          </div>
          <ul class="caps caps--1" data-reveal style="--d:140ms">
{li(principles)}
          </ul>
        </div>
        <div class="appr">
          <div class="story__prose story__prose--wide" data-reveal style="--d:160ms">
{paras(approach_paras)}
          </div>
          <div class="appr__video" data-reveal style="--d:200ms">
            {B.video_html(s, base)}
          </div>
        </div>{structure}
      </div>
    </section>
{walkthrough}{decided}{validation}

    <section class="out band band-wash" aria-labelledby="outcomesHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>Outcomes and business value</p>
            <h2 class="display" id="outcomesHeading" data-reveal style="--d:80ms">{esc(s['outcome'])}</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">Delivered work, verified results and intended benefits are kept apart. Nothing here is a metric the client has not confirmed.</p>
        </div>
        <div class="out__cols">
          <div class="out__col" data-reveal>
            <h3 class="out__h">Delivered</h3>
            <ul class="out__list">
{li(c['outcomes']['delivered'])}
            </ul>
          </div>{verified}
          <div class="out__col" data-reveal style="--d:160ms">
            <h3 class="out__h">Intended benefits</h3>
            <ul class="out__list">
{li(c['outcomes']['intended'])}
            </ul>
          </div>
        </div>
        <p class="story__tech" data-reveal style="--d:200ms">Built on {esc(s['tech'])}</p>{endo}
      </div>
    </section>

    <section class="rel band" aria-labelledby="relatedHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>Related work</p>
            <h2 class="display" id="relatedHeading" data-reveal style="--d:80ms">Two projects that share the pattern</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms"><a class="arrow-link" href="{base}work/">All case studies {ARROW}</a></p>
        </div>
        <div class="cscards cscards--2">
{related}
        </div>
      </div>
    </section>

    <section class="convert" aria-labelledby="convertHeading">
      <div class="shell convert__in">
        <p class="eyebrow" data-reveal>Next steps</p>
        <h2 class="display" id="convertHeading" data-reveal style="--d:80ms">{esc(c['cta'])}</h2>
        <p class="lede" data-reveal style="--d:140ms">Tell us what the business needs to do better. We come back within two working days with a short written view and a time to talk — no obligation.</p>
        <div class="convert__ctas" data-reveal style="--d:200ms">
          <a class="btn" href="{base}contact.html">Discuss a project {ARROW}</a>
          <a class="arrow-link" href="{base}solutions/">Explore our solutions {ARROW}</a>
        </div>
      </div>
    </section>

{B.video_modal()}
'''
    return head[0] + body + head[1]


# ── Our Work ─────────────────────────────────────────────────────────────
UNCLASSIFIED = [
    ('FINOS', 'entry-finos-status'), ('SmartStart', 'entry-smartstart-status'),
    ('RentFlow', 'entry-rentflow-status'), ('NuraCoach', 'entry-nuracoach-status'),
    ('Lungelo', 'entry-lungelo-status'),
]


def work_page():
    base = '../'
    import json
    items = {"@context": "https://schema.org", "@type": "ItemList",
             "name": "GEMIS case study videos", "itemListElement": []}
    for i, s in enumerate(S.STORIES, 1):
        v = S.BASE_URL + s['video']
        items["itemListElement"].append({
            "@type": "VideoObject", "position": i, "name": s['video_title'],
            "description": s['summary'], "duration": s['duration'], "inLanguage": "en",
            "uploadDate": "2026-10-21", "contentUrl": f"{v}_web.mp4",
            "thumbnailUrl": f"{v}_thumb.jpg", "transcript": s['transcript'],
            "keywords": s['keywords'],
            "publisher": {"@type": "Organization", "name": "GEM Information Systems (GEMIS)", "url": CANON},
            "about": {"@type": s.get('about_type', 'Organization'), "name": s['about']},
        })
    schema = ('  <script type="application/ld+json">\n'
              + json.dumps(items, ensure_ascii=False, indent=2) + '\n  </script>')

    head = shell(base, 'Case Studies — complex business challenges, thoughtfully designed digital solutions | GEMIS®',
                 'Case studies from GEMIS: the systems South African businesses run on, from field operations '
                 'and claims to reporting and the ManaGEM platform. A business systems partner since 2014.',
                 f'{CANON}work/', extra_head=schema)

    comp = [S.BY_SLUG[k] for k in ('wastemart', 'homeassist', 'managem')]
    composition = '\n'.join(
        '          <img class="cshero__shot cshero__shot--%d" src="%s%s%s_thumb.jpg" alt="" width="1280" height="720" loading="%s" />'
        % (i + 1, base, S.VIDEO_DIR, c['video'], 'eager' if i == 2 else 'lazy')
        for i, c in enumerate(comp))

    def card(i, s):
        return B.cscard(s, base, i, extra_attrs=f''' data-industry="{s['industry_tag']}" data-capability="{' '.join(s['capability_tags'])}"''').replace('<article class="cscard"', '<article class="cscard wk__card"', 1)

    cards = '\n'.join(card(i, s) for i, s in enumerate(S.STORY_PAGES))

    # Not confirmed as client systems, so they are not on the live build at all.
    unclassified = '\n'.join(
        B.hideable(tid, f'''<article class="wk__card wk__card--unclassified">
            <h3 class="wk__name">{name}</h3>
            <p class="wk__line">{tbc(tid, 'Client system or concept — to confirm')}</p>
          </article>''') for name, tid in UNCLASSIFIED)

    filters = '''        <details class="wkf" data-filters hidden>
          <summary class="wkf__btn"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M3 5h14M6 10h8M8.5 15h3"/></svg><span>Filter</span><span class="wkf__count" data-filter-count hidden></span></summary>
          <div class="wkf__panel">
            <fieldset class="wk__fieldset"><legend class="eyebrow">Industry</legend>
              <button type="button" data-filter="industry" data-value="all" aria-pressed="true">All</button>
              <button type="button" data-filter="industry" data-value="construction" aria-pressed="false">Construction</button>
              <button type="button" data-filter="industry" data-value="insurance" aria-pressed="false">Insurance</button>
              <button type="button" data-filter="industry" data-value="waste" aria-pressed="false">Waste</button>
              <button type="button" data-filter="industry" data-value="mining" aria-pressed="false">Mining</button>
              <button type="button" data-filter="industry" data-value="non-profit" aria-pressed="false">Non-profit</button>
              <button type="button" data-filter="industry" data-value="education" aria-pressed="false">Education</button>
            </fieldset>
            <fieldset class="wk__fieldset"><legend class="eyebrow">Capability</legend>
              <button type="button" data-filter="capability" data-value="all" aria-pressed="true">All</button>
              <button type="button" data-filter="capability" data-value="field-operations" aria-pressed="false">Field operations</button>
              <button type="button" data-filter="capability" data-value="integration-reporting" aria-pressed="false">Integration and reporting</button>
              <button type="button" data-filter="capability" data-value="platforms" aria-pressed="false">Platforms</button>
            </fieldset>
            <button class="wkf__clear" type="button" data-filter-clear>Clear filters</button>
          </div>
        </details>'''

    body = f'''
    <!-- ═══════════ CASE STUDIES ═══════════ -->
    <section class="chero cshero" id="hero">
      <div class="shell cshero__in">
        <div class="cshero__text">
          <p class="chero__kicker" data-reveal>Case studies</p>
          <h1 class="chero__title" data-reveal style="--d:80ms">{B.two_lines("Complex business challenges. Thoughtfully designed digital solutions.")}</h1>
          <p class="chero__copy" data-reveal style="--d:140ms">GEMIS builds the systems South African businesses run on when a spreadsheet, a legacy package or five disconnected tools can no longer keep up: field operations, claims, quoting, reporting, learning, and the platform that holds it all together.</p>
          <div class="cshero__ctas" data-reveal style="--d:200ms">
            <a class="btn" href="{base}contact.html">Discuss a project {ARROW}</a>
            <a class="arrow-link" href="{base}solutions/">Explore our solutions {ARROW}</a>
          </div>
        </div>
      </div>
    </section>

    <section class="csstats band" aria-label="GEMIS in numbers">
      <div class="shell">
        <ul class="trust__stats csstats__row" data-reveal>
          <li class="stat"><span class="stat__n" data-count="12" data-sup="+">12<sup>+</sup></span><span class="stat__l">Years building business systems</span></li>
          <li class="stat"><span class="stat__n" data-count="50" data-sup="+">50<sup>+</sup></span><span class="stat__l">Systems delivered into production</span></li>
          <li class="stat"><span class="stat__n" data-count="5" data-sup="+">5<sup>+</sup></span><span class="stat__l">Sectors served nationally</span></li>
        </ul>
      </div>
    </section>

    <section class="wk band" id="all" aria-labelledby="allHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>All case studies</p>
            <h2 class="display" id="allHeading" data-reveal style="--d:80ms">The portfolio</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">Each card names the business context, what GEMIS did, and where the project stands. Several of these systems have been running for more than a decade. Filter by industry or by what the system had to do.</p>
        </div>
        <div class="wk__bar">
{filters}
          <p class="wk__count" id="wkCount" aria-live="polite"></p>
        </div>
        <div class="cscards" data-grid>
{cards}
        </div>
        <div class="unconfirmed" data-kind="hideable">
        <h3 class="wk__sub" data-reveal>Still to classify</h3>
        <p class="wk__subnote" data-reveal>These five are in the repository but it is not yet confirmed whether each is a client system or a concept. They are listed rather than quietly dropped.</p>
        <div class="wk__grid wk__grid--quiet">
{unclassified}
        </div>
        </div>
      </div>
    </section>

    <section class="approach band band-wash" aria-labelledby="approachHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>How GEMIS approaches projects</p>
            <h2 class="display" id="approachHeading" data-reveal style="--d:80ms">Understand. Design. Build. Evolve.</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">The same four stages sit behind every project here: the enquiry record at SBS, the payment-driven schedule at WasteMart and the approval step at Sonke were each decided before anything was built. <a class="arrow-link" href="{base}solutions/">See how we work {ARROW}</a></p>
        </div>
{B.stages(SV.WAYS)}
      </div>
    </section>
{B.in_their_words(base, "workWordsHeading")}

    <section class="convert" id="discuss" aria-labelledby="convertHeading">
      <div class="shell convert__in">
        <p class="eyebrow" data-reveal>Your project</p>
        <h2 class="display" id="convertHeading" data-reveal style="--d:80ms">Have a complex business challenge? Let&rsquo;s explore the right solution.</h2>
        <p class="lede" data-reveal style="--d:140ms">Tell us what the business needs to do better. We come back within two working days with a short written view and a time to talk — no obligation.</p>
        <div class="convert__ctas" data-reveal style="--d:200ms">
          <a class="btn" href="{base}contact.html">Discuss a project {ARROW}</a>
          <a class="arrow-link" href="{base}solutions/">Explore our solutions {ARROW}</a>
        </div>
      </div>
    </section>

{B.video_modal()}
'''
    html_out = head[0] + body + head[1]
    return html_out.replace('</body>',
        '  <script src="../assets/js/work-filters.js" defer></script>\n</body>')


def main():
    os.makedirs(os.path.join(ROOT, 'work'), exist_ok=True)
    open(os.path.join(ROOT, 'work', 'index.html'), 'w', encoding='utf-8').write(work_page())
    print('work/index.html')
    for s in S.STORY_PAGES:
        d = os.path.join(ROOT, 'work', s['slug'])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(story_page(s))
        print(f'work/{s["slug"]}/index.html')


if __name__ == '__main__':
    main()
