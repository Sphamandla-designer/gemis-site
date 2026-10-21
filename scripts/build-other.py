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


def original(path):
    """A page as it was before it became a redirect stub."""
    rev = subprocess.run(['git', 'log', '--format=%H', '-1', '--', path],
                         cwd=ROOT, capture_output=True, text=True).stdout.strip()
    # the commit that stubbed it is phase 1; take the parent
    out = subprocess.run(['git', 'show', f'{rev}~1:{path}'], cwd=ROOT,
                         capture_output=True, text=True)
    if out.returncode:
        raise SystemExit(f'could not recover {path}')
    return out.stdout


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
    block = block.replace(f'{base}services.html', f'{base}solutions/bespoke-software/')
    block = block.replace(f'{base}about.html', f'{base}our-story/')
    block = block.replace(f'{base}case-studies.html', f'{base}work/')
    block = block.replace(f'{base}wastemart.html', f'{base}work/wastemart/')
    block = block.replace(f'{base}managem.html', f'{base}solutions/managem/')
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
     'solutions/bespoke-software/', 'Explore Bespoke Software',
     'wastemart', 'See it in production — WasteMart'),
    ('ManaGEM',
     'A proven business management platform, ready to run on: sales, stock, payroll, projects '
     'and multi-company accounting in one place. It began as one client’s system.',
     'solutions/managem/', 'Explore ManaGEM',
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
        <a class="arrow-link" href="{base}index.html#discovery" data-reveal style="--d:140ms">Book a Discovery Session {ARROW}</a>
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
        <a class="arrow-link" href="{base}index.html#discovery" data-reveal style="--d:140ms">Book a Discovery Session {ARROW}</a>
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
    body = f'''
    <section class="chero" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>ManaGEM</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">A business management platform, born in a real business</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">Sales, stock, payroll, projects and multi-company accounting in one place. About a dozen companies run their day-to-day operations on it.</p>
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
          {B.endorsement_html('ryan-smith', base, 'Client since 2014')}
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
      </div>
    </section>

    <section class="chap band band-tint" aria-labelledby="resultsHeading">
      <div class="shell">
        <p class="eyebrow" data-reveal>Results</p>
        <h2 class="display" id="resultsHeading" data-reveal style="--d:80ms">In use today</h2>
        <div class="story__prose" data-reveal style="--d:140ms">
          <p>About a dozen companies run their day-to-day operations on ManaGEM.</p>
          <p class="story__metric">Month-end close: nine days to two</p>
        </div>
      </div>
    </section>

    <section class="endnote">
      <div class="shell">
        <h2 class="display" data-reveal>See whether ManaGEM fits your business.</h2>
        <a class="arrow-link" href="{base}index.html#discovery" data-reveal style="--d:140ms">Book a Discovery Session {ARROW}</a>
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
    page('solutions/managem/index.html', base,
         'ManaGEM — a business management platform born in a real business | GEMIS®',
         'ManaGEM began as the system GEMIS built for SBS Waterproofing. Sales, stock, payroll, '
         'projects and multi-company accounting in one platform, used by about a dozen companies.',
         body)


# ── Our Story ────────────────────────────────────────────────────────────
def our_story():
    base = '../'
    src = original('about.html')
    blocks = sections(src, ['story', 'team'])
    story = rebase(blocks.get('story', ''), base)
    # it follows the wash band above, so it takes the paper ground
    story = story.replace('class="sec band band-wash" id="story"', 'class="sec band" id="story"')
    team = rebase(blocks.get('team', ''), base)

    founders = '\n'.join(
        f'''          <li class="hist__client">
            <h3>{esc(S.BY_SLUG[k]['client'])}</h3>
            <p>{B.since_html(S.BY_SLUG[k])}</p>
            <p>{esc(S.BY_SLUG[k]['headline'])}</p>
            <a class="arrow-link arrow-link--quiet" href="{base}work/{k}/">Read the story {ARROW}</a>
          </li>''' for k in S.FOUNDING)

    body = f'''
    <section class="chero" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>Our Story</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">Technology changes. Businesses evolve. Good partnerships endure.</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">GEM Information Systems has been building business systems in South Africa since 2014 — and still works with the businesses it started with.</p>
      </div>
    </section>

    <section class="sec band band-wash" id="founding" aria-labelledby="foundingHeading">
      <div class="shell">
        <p class="eyebrow" data-reveal>Where it started</p>
        <h2 class="display" id="foundingHeading" data-reveal style="--d:80ms">Three relationships that have not ended</h2>
        <ul class="hist__clients" data-reveal style="--d:140ms">
{founders}
        </ul>
      </div>
    </section>

{story}

    <!-- moved off the homepage, where it sat under a heading the brief retired -->
    <section class="sec band band-ink" id="numbers" aria-labelledby="numbersHeading">
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
        <h2 class="display" data-reveal>We learn your business. We build around it. We stay.</h2>
        <a class="arrow-link" href="{base}index.html#discovery" data-reveal style="--d:140ms">Book a Discovery Session {ARROW}</a>
      </div>
    </section>
'''
    page('our-story/index.html', base,
         'Our Story — a business technology partner since 2014 | GEMIS®',
         'GEM Information Systems has built business systems in South Africa since 2014, and '
         'still works with the businesses it started with. Our history, approach and team.',
         body)


if __name__ == '__main__':
    solutions_index()
    bespoke()
    managem()
    our_story()
