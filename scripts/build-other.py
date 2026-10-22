#!/usr/bin/env python3
"""
Generate the remaining pages: Solutions, Bespoke Software, ManaGEM and Our Story.

Bespoke Software and Our Story carry the content of the old services.html and
about.html, which are now redirect stubs, so the content is read out of git
(HEAD of the commit before they were stubbed) rather than retyped.

    python3 scripts/build-other.py
"""
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

for name, fname in (('stories', 'stories.py'), ('build_stories', 'build-stories.py'),
                    ('build_pages', 'build-pages.py')):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    globals()[name.upper()[0] if name == 'stories' else name] = mod

S = globals()['S']
B = globals()['build_stories']
P = globals()['build_pages']
esc, tbc, ARROW = B.esc, B.tbc, B.ARROW
CANON = S.CANONICAL
sv_spec = importlib.util.spec_from_file_location('services', os.path.join(HERE, 'services.py'))
SV = importlib.util.module_from_spec(sv_spec)
sv_spec.loader.exec_module(SV)


def original(path):
    """A page as it was before it became a redirect stub."""
    revs = subprocess.run(['git', 'log', '--format=%H', '--', path],
                          cwd=ROOT, capture_output=True, text=True).stdout.split()
    # walk back past every commit that only touched the stub
    for rev in revs:
        out = subprocess.run(['git', 'show', f'{rev}:{path}'], cwd=ROOT,
                             capture_output=True, text=True)
        if out.returncode == 0 and 'http-equiv="refresh"' not in out.stdout:
            return out.stdout
    raise SystemExit(f'could not recover {path}')


def sections(html_text, ids):
    """Pull whole <section> blocks out of an old page by id, in order."""
    found = {}
    for sid in ids:
        m = re.search(r'(<section[^>]*id="' + re.escape(sid) + r'".*?\n    </section>)',
                      html_text, re.S)
        if m:
            found[sid] = m.group(1)
    return found


def rebase(block, base):
    """Old pages lived at the root; these live two levels down."""
    block = re.sub(r'(href|src)="(?!https?:|#|mailto:|tel:|data:)([^"]+)"',
                   lambda m: f'{m.group(1)}="{base}{m.group(2)}"', block)
    # links to pages that moved
    block = block.replace(f'{base}services.html', f'{base}solutions/')
    block = block.replace(f'{base}about.html', f'{base}our-story/')
    block = block.replace(f'{base}case-studies.html', f'{base}work/')
    block = block.replace(f'{base}wastemart.html', f'{base}work/wastemart/')
    block = block.replace(f'{base}managem.html', f'{base}products/managem/')
    return block


def page(path, base, title, desc, body):
    head, tail = P.shell(base, title, desc, f'{CANON}{path}')
    full = head + body + tail
    d = os.path.join(ROOT, os.path.dirname(path))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(full)
    print(path)


# ── Solutions overview ───────────────────────────────────────────────────
CARDS = [
    ('Bespoke Software',
     'A system designed and built around your operation, then supported for the long term. '
     'We start with how the business actually runs, not with a template, and we stay after go-live.',
     'solutions/', 'Explore our solutions',
     'wastemart', 'See it in production — WasteMart'),
    ('ManaGEM',
     'A proven business management platform, ready to run on: enquiries, quotes, deposit '
     'invoices, project profit, stock and staff records in one place. It began as one client’s system.',
     'products/managem/', 'Explore ManaGEM',
     'sbs-waterproofing', 'See where it came from — SBS Waterproofing'),
    ('GEMIS Studio',
     'Product and interface design from the team that can also build it — research, prototypes '
     'and design systems.',
     'studio/', 'See the Studio', None, None),
    ('Technical Academy',
     'Practical AI and technical training for professionals and teams, so the people using the '
     'systems keep pace with them.',
     'https://gemis.tech/', 'Visit gemis.tech', None, None),
]


def solutions_index():
    base = '../'
    cards = []
    for name, body, href, cta, proof, proof_label in CARDS:
        ext = ' target="_blank" rel="noopener"' if href.startswith('http') else ''
        link = href if href.startswith('http') else base + href
        pl = (f'\n            <a class="arrow-link arrow-link--quiet" href="{base}work/{proof}/">'
              f'{esc(proof_label)} {ARROW}</a>' if proof else '')
        cards.append(f'''          <article class="sol__card" data-reveal>
            <h2 class="sol__name">{esc(name)}</h2>
            <p class="sol__body">{esc(body)}</p>
            <a class="arrow-link" href="{link}"{ext}>{esc(cta)} {ARROW}</a>{pl}
          </article>''')
    body = f'''
    <section class="chero" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>Solutions</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">Four ways to work with GEMIS</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">A system built around your operation, a platform ready to run on, a studio to design it, or training to keep your team ahead.</p>
      </div>
    </section>

    <section class="sol band" aria-labelledby="solHeading">
      <div class="shell">
        <h2 class="vh" id="solHeading">The four solutions</h2>
        <div class="sol__grid">
{chr(10).join(cards)}
        </div>
      </div>
    </section>

    <section class="endnote">
      <div class="shell">
        <h2 class="display" data-reveal>Not sure which one you need?</h2>
        <p data-reveal style="--d:80ms">Tell us what the business needs to do better and we will come back with a view.</p>
        <a class="arrow-link" href="{base}contact.html" data-reveal style="--d:140ms">Discuss a project {ARROW}</a>
      </div>
    </section>
'''
    page('solutions/index.html', base, 'Solutions — four ways to work with GEMIS | GEMIS®',
         'Bespoke software, the ManaGEM platform, GEMIS Studio design and the Technical '
         'Academy. Four ways to work with a business technology partner operating since 2014.',
         body)


# ── Bespoke Software ─────────────────────────────────────────────────────
PROOF_LINKS = {
    'Custom software development': ('wastemart', 'WasteMart'),
    'Microsoft Cloud solutions': ('trans-hex', 'Trans Hex Group'),
    'Enterprise SaaS': ('homeassist', 'HomeAssist'),
    'Business intelligence': ('sonke', 'Sonke Gender Justice'),
}


def bespoke():
    base = '../../'
    src = original('services.html')
    blocks = sections(src, ['problems', 'services', 'process'])
    missing = [k for k in ('services', 'process') if k not in blocks]
    if missing:
        raise SystemExit(f'services.html no longer has: {missing}')

    services = rebase(blocks['services'], base)
    process = rebase(blocks['process'], base)
    process = process.replace('band band-warm', 'band band-wash')  # the warm ground is retired

    # "See it in production" goes at the end of each capability's panel, after its
    # chips list. It must never land inside .acc__btn: a link inside a button is a
    # nested interactive control, which axe fails outright.
    PANEL_END = '</ul>\n            </div></div></div>'

    def add_proof(m):
        item = m.group(0)
        heading = re.search(r'<h3 class="acc__name">([^<]*)</h3>', item)
        if not heading or PANEL_END not in item:
            return item
        name = heading.group(1).lower()
        for key, (slug, label) in PROOF_LINKS.items():
            if key.split()[0].lower() in name:
                link = ('\n              <p class="svc__proof">'
                        f'<a class="arrow-link arrow-link--quiet" href="{base}work/{slug}/">'
                        f'See it in production — {label} {ARROW}</a></p>')
                return item.replace(PANEL_END, '</ul>' + link + '\n            </div></div></div>')
        return item

    # anchored on the item's own indentation: a bare .*?</li> stops at the first
    # chip's closing tag inside the panel
    services = re.sub(r'<li class="acc__item".*?\n          </li>', add_proof, services, flags=re.S)

    body = f'''
    <section class="chero" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>Bespoke Software</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">A system built around your operation</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">When off-the-shelf software holds the business back, we design and build around how it actually works — then stay to support it.</p>
      </div>
    </section>

{services}

{process}

    <!-- moved off the homepage, where it sat below the fold doing nothing -->
    <section class="sec band band-tint" id="stack" aria-labelledby="stackHeading">
      <div class="shell">
        <p class="eyebrow" data-reveal>The stack</p>
        <h2 class="display" id="stackHeading" data-reveal style="--d:80ms">Built on the Microsoft Cloud</h2>
        <ul class="stack__row" data-reveal style="--d:140ms">
          <li>Microsoft Azure</li>
          <li>Azure SQL</li>
          <li>.NET</li>
          <li>Power BI</li>
          <li>Identity management</li>
          <li>Disaster recovery</li>
        </ul>
      </div>
    </section>

    <section class="endnote">
      <div class="shell">
        <h2 class="display" data-reveal>Tell us what your business needs to do better.</h2>
        <a class="arrow-link" href="{base}contact.html" data-reveal style="--d:140ms">Discuss a project {ARROW}</a>
      </div>
    </section>
'''
    page('solutions/bespoke-software/index.html', base,
         'Bespoke Software — systems built around your operation | GEMIS®',
         'Custom software, Microsoft Cloud, enterprise SaaS and mobile, business intelligence '
         'and integration — designed around how your business works and supported long after go-live.',
         body)

# ── ManaGEM ──────────────────────────────────────────────────────────────
def managem():
    base = '../../'
    s = S.BY_SLUG['managem']
    C = P.C
    body = f'''
    <section class="chero" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>ManaGEM</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">A business management platform, born in a real business</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">Every enquiry followed to the sale, quotes accepted online, deposit invoices raised automatically, project profit, stock alerts and staff records in one place. About a dozen companies run their day-to-day operations on it.</p>
      </div>
    </section>

    <section class="origin band band-wash" id="origin" aria-labelledby="originHeading">
      <div class="shell origin__grid">
        <div class="origin__body">
          <p class="eyebrow" data-reveal>Born at SBS Waterproofing</p>
          <h2 class="display" id="originHeading" data-reveal style="--d:80ms">Built for one business. Developed into a product for many.</h2>
          <p class="lede" data-reveal style="--d:140ms">Off-the-shelf apps did not fit how SBS Waterproofing worked, so GEMIS built them a system of their own from 2015 — and designed it from day one to work for other businesses as well. Years of refining it around a real operation turned it into ManaGEM.</p>
          <p data-reveal style="--d:180ms"><a class="arrow-link arrow-link--quiet" href="{base}work/sbs-waterproofing/">Read the SBS Waterproofing story {ARROW}</a></p>
        </div>
        <div class="origin__aside" data-reveal style="--d:160ms">
          {'<p class="origin__where">Where the SBS relationship began:</p>' if S.ENDORSERS['ryan-smith'].get('line') else ''}
          {B.endorsement_html('ryan-smith', base)}
        </div>
      </div>
    </section>

    <section class="chap band" aria-labelledby="whatHeading">
      <div class="shell">
        <p class="eyebrow" data-reveal>What it does</p>
        <h2 class="display" id="whatHeading" data-reveal style="--d:80ms">One system, from enquiry to invoice</h2>
        <div class="story__build" data-reveal style="--d:140ms">
          {B.video_html(s, base)}
          <ul class="story__caps">
{chr(10).join(f'            <li>{c}</li>' for c in s['capabilities'])}
          </ul>
        </div>
        <div class="story__flow" data-reveal style="--d:200ms">
          <h3 class="out__h">The workflow as implemented</h3>
{B.flow(C.MANAGEM['flow'], C.MANAGEM['flow_label'])}
        </div>
      </div>
    </section>

    <section class="chap band band-wash" id="walkthrough" aria-labelledby="walkHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>The product, step by step</p>
            <h2 class="display" id="walkHeading" data-reveal style="--d:80ms">What the user needs to do, and how ManaGEM supports it</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">Stills from the ManaGEM video. The interfaces are illustrated for the video, not screen recordings of the product; every capability shown is one ManaGEM delivers.</p>
        </div>
{B.walk(C.MANAGEM['walk'], base, 'managem')}
      </div>
    </section>

    <section class="chap band band-tint" aria-labelledby="resultsHeading">
      <div class="shell">
        <p class="eyebrow" data-reveal>Results</p>
        <h2 class="display" id="resultsHeading" data-reveal style="--d:80ms">In use today</h2>
        <div class="story__prose" data-reveal style="--d:140ms">
          <p>About a dozen companies run their day-to-day operations on ManaGEM (confirmed).</p>
          <p class="story__metric">Month-end close: nine days to two</p>
          <p>One client&rsquo;s month-end close went from nine days to two &mdash; confirmed by that client. No other figure is published: adoption, time saved or revenue effects across the dozen companies have not been measured.</p>
        </div>
      </div>
    </section>

    <section class="endnote">
      <div class="shell">
        <h2 class="display" data-reveal>Planning a new business platform, or outgrowing the apps you have?</h2>
        <a class="arrow-link" href="{base}contact.html" data-reveal style="--d:140ms">Discuss a project {ARROW}</a>
        <a class="arrow-link arrow-link--quiet" href="{base}work/" data-reveal style="--d:180ms">View related work {ARROW}</a>
        <!-- facts.md confirms the free trial is live, but gives no URL for it and
             leaves the separate ManaGEM site as "FILL". A trial CTA with nowhere
             to point is worse than no CTA, so it is held back and the missing URL
             is a blocking item: managem-trial-url. -->
        <!-- data-tbc="managem-trial-url" data-kind="blocking"
             Held back rather than rendered: a visually-hidden note is still read
             aloud by a screen reader, and this is an internal message. The marker
             lives in the comment so check-tbc still counts it. -->
      </div>
    </section>
'''
    page('products/managem/index.html', base,
         'ManaGEM — a business management platform born in a real business | GEMIS®',
         'ManaGEM began as the system GEMIS built for SBS Waterproofing. Enquiries, quotes, deposit '
         'invoices, project profit, stock and staff records in one platform, used by about a dozen companies.',
         body)


# ── Our Story ────────────────────────────────────────────────────────────
def our_story():
    base = '../'
    src = original('about.html')
    blocks = sections(src, ['story', 'team'])
    story = rebase(blocks.get('story', ''), base)
    # it follows the wash band above, so it takes the paper ground
    story = story.replace('class="sec band band-wash" id="story"', 'class="sec band" id="story"')
    # the About timeline becomes the horizontal timeline the whole site shares
    story = re.sub(r'<ol class="tl">.*?</ol>', lambda m: B.tline(SV.MILESTONES, 'Era').strip(), story, count=1, flags=re.S)
    team = rebase(blocks.get('team', ''), base)
    team = team.replace('UI/UX designer — head of Brand Studio', 'UI/UX designer, head of GEMIS Studio')
    # facts.md confirms no surname or title except Sphamandla Xaba's. The others
    # publish as a first name, their line held back until confirmed (?review=1
    # shows everything the old page carried).
    def flag_mate(m):
        name, role = m.group(1), m.group(2)
        if name.startswith('Sphamandla'):
            return m.group(0)
        first = name.split()[0]
        return ('<h3 class="mate__n"><span class="unconfirmed" data-tbc="team-titles" data-kind="hideable">' + name
                + '</span><span class="confirmed-fallback">' + first + '</span></h3>\n'
                '            <p class="mate__r unconfirmed" data-tbc="team-titles" data-kind="hideable">' + role + '</p>')
    team = re.sub(r'<h3 class="mate__n">(.*?)</h3>\s*<p class="mate__r">(.*?)</p>', flag_mate, team)

    founders = B.srows([
        (f'<a href="{base}work/{k}/">{esc(S.BY_SLUG[k]["client"])}</a>',
         f'<p>{esc(S.BY_SLUG[k]["headline"])}</p>', [B.since_html(S.BY_SLUG[k])],
         f'<a class="arrow-link arrow-link--quiet srow__go" href="{base}work/{k}/">Read the story {ARROW}</a>')
        for k in S.FOUNDING])

    body = f'''
    <section class="chero" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>Our Story</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">Technology changes. Businesses evolve. Good partnerships endure.</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">GEM Information Systems has been building business systems in South Africa since 2014 — and still works with the businesses it started with.</p>
      </div>
    </section>

    <section class="sec band band-wash plusgrid plusgrid--tr" id="founding" aria-labelledby="foundingHeading">
      <div class="shell">
        <div class="svcs__head">
          <div>
            <p class="eyebrow" data-reveal>Where it started</p>
            <h2 class="display" id="foundingHeading" data-reveal style="--d:80ms">Three relationships that have not ended</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">The company&rsquo;s story is told best by the systems: each of these is a case study, with the video of what was built. <a class="arrow-link" href="{base}work/">All case studies {ARROW}</a></p>
        </div>
        <ol class="srows">
{founders}
        </ol>
      </div>
    </section>

{story}

    <!-- moved off the homepage, where it sat under a heading the brief retired -->
    <section class="sec band band-ink plusgrid plusgrid--br" id="numbers" aria-labelledby="numbersHeading">
      <div class="shell">
        <p class="eyebrow" data-reveal>By the numbers</p>
        <h2 class="display" id="numbersHeading" data-reveal style="--d:80ms">Since 2014</h2>
        <ul class="stats" data-reveal style="--d:140ms">
          <li class="stat">
            <span class="stat__n">12<sup>+</sup></span>
            <span class="stat__l">Years building mission-critical systems</span>
          </li>
          <li class="stat">
            <span class="stat__n">50<sup>+</sup></span>
            <span class="stat__l">Systems delivered into production</span>
          </li>
          <li class="stat">
            <span class="stat__n">5<sup>+</sup></span>
            <span class="stat__l">Sectors served nationally</span>
          </li>
        </ul>
      </div>
    </section>

{team}

    <section class="endnote">
      <div class="shell">
        <h2 class="display" data-reveal>Have a business challenge worth solving?</h2>
        <a class="arrow-link" href="{base}contact.html" data-reveal style="--d:140ms">Discuss a project {ARROW}</a>
      </div>
    </section>
'''
    page('our-story/index.html', base,
         'Our Story — a business technology partner since 2014 | GEMIS®',
         'GEM Information Systems has built business systems in South Africa since 2014, and '
         'still works with the businesses it started with. Our history, approach and team.',
         body)


if __name__ == '__main__':
    # solutions/ and solutions/bespoke-software/ are built by build-services.py now
    managem()
    our_story()
