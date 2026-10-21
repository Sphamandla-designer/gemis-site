#!/usr/bin/env python3
"""
Generate the Solutions page, the nine service pages, the Products page and the
News & Insights pages from scripts/services.py.

    python3 scripts/build-services.py

The page shell comes from scripts/build-pages.py (lifted from index.html), so
every page here carries the same head, header and footer as the rest of the
site, and scripts/apply-chrome.py keeps the navigation in step afterwards.
"""
import importlib.util
import os
import re
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
B = load('build_stories', 'build-stories.py')
P = load('build_pages', 'build-pages.py')
O = load('build_other', 'build-other.py')

esc, ARROW = B.esc, B.ARROW
CANON = S.CANONICAL


def icon(slug):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{SV.ICONS[slug]}</svg>')


def page(path, base, title, desc, body):
    head, tail = P.shell(base, title, desc, f'{CANON}{path}'.replace('index.html', ''))
    full = head + body + tail
    os.makedirs(os.path.join(ROOT, os.path.dirname(path)), exist_ok=True)
    open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(full)
    print(path)


def endnote(base, title='Tell us what your business needs to do better.'):
    return f'''
    <section class="endnote">
      <div class="shell">
        <h2 class="display" data-reveal>{esc(title)}</h2>
        <a class="arrow-link" href="{base}index.html#discovery" data-reveal style="--d:140ms">Book a Discovery Session {ARROW}</a>
      </div>
    </section>
'''


# ── the services grid, shared by the homepage and the Solutions page ─────
def services_grid(base=''):
    tiles = []
    for i, s in enumerate(SV.SERVICES):
        lead = ' svc--lead' if i == 0 else ''
        tiles.append(f'''          <a class="svc{lead}" href="{base}solutions/{s['slug']}/" data-reveal style="--d:{i * 60}ms">
            <span class="svc__n" aria-hidden="true">{i + 1:02d}</span>
            <span class="svc__icon" aria-hidden="true">{icon(s['slug'])}</span>
            <span class="svc__name">{esc(s['name'])}</span>
            <span class="svc__line">{esc(s['short'])}</span>
            <span class="svc__go" aria-hidden="true">{ARROW}</span>
          </a>''')
    return '\n'.join(tiles)


# ── the services rows, for the homepage: the first six, numbered ─────────
def services_rows(base='', limit=6):
    rows = []
    for i, s in enumerate(SV.SERVICES[:limit]):
        chips = '\n'.join(f'                <li>{esc(c)}</li>' for c in s['caps'][:4])
        rows.append(f'''          <li class="srow" data-reveal style="--d:{i * 60}ms">
            <span class="srow__n" aria-hidden="true">{i + 1:02d}</span>
            <h3 class="srow__name"><a href="{base}solutions/{s['slug']}/">{esc(s['name'])}</a></h3>
            <div class="srow__body">
              <p>{esc(s['intro'])}</p>
              <ul class="srow__chips">
{chips}
              </ul>
              <a class="arrow-link arrow-link--quiet srow__go" href="{base}solutions/{s['slug']}/">See details {ARROW}</a>
            </div>
          </li>''')
    return '\n'.join(rows)


# ── Solutions (the services page) ────────────────────────────────────────
def solutions_index():
    base = '../'
    src = O.original('services.html')
    blocks = O.sections(src, ['process'])
    process = O.rebase(blocks.get('process', ''), base).replace('band band-warm', 'band band-wash')
    body = f'''
    <section class="chero" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>Solutions</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">Nine disciplines, one accountable team</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">Open any solution to see exactly what we deliver. Most engagements draw on several at once — you deal with one partner throughout.</p>
      </div>
    </section>

    <section class="svcs band" aria-labelledby="svcsHeading">
      <div class="shell">
        <h2 class="vh" id="svcsHeading">The nine solutions</h2>
        <div class="svcs__grid">
{services_grid(base)}
        </div>
      </div>
    </section>

{process}

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
{endnote(base)}'''
    page('solutions/index.html', base, 'Solutions — nine disciplines, one team | GEMIS®',
         'Custom software, Microsoft Cloud, SaaS platforms, mobile, business intelligence, '
         'integration, UX, modernisation and support — from one accountable partner since 2014.',
         body)


# ── one service page ─────────────────────────────────────────────────────
def service_page(s):
    base = '../../'
    others = [o for o in SV.SERVICES if o['slug'] != s['slug']]
    caps = '\n'.join(f'          <li>{esc(c)}</li>' for c in s['caps'])
    why = '\n'.join(f'''          <div class="why__col" data-reveal style="--d:{i * 80}ms">
            <h3 class="why__t">{esc(t)}</h3>
            <p>{esc(b)}</p>
          </div>''' for i, (t, b) in enumerate(s['body']))
    proof = ''
    if s.get('proof'):
        st = S.BY_SLUG[s['proof']]
        proof = f'''
    <section class="sec band band-wash" aria-labelledby="proofHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>In production</p>
            <h2 class="display" id="proofHeading" data-reveal style="--d:80ms">Where this has run</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">A system in use today, not a mock-up.</p>
        </div>
        <article class="pf" data-reveal style="--d:160ms">
          <a class="pf__media" href="{base}work/{st['slug']}/" tabindex="-1" aria-hidden="true">
            <img src="{base}{S.VIDEO_DIR}{st['video']}_thumb.jpg" alt="" loading="lazy" width="1280" height="720" />
          </a>
          <div class="pf__body">
            <p class="sty__period">{B.period_html(st)}</p>
            <h3 class="sty__client">{esc(st['client'])}</h3>
            <p class="sty__headline">{esc(st['headline'])}</p>
            <p class="sty__challenge">{esc(st['challenge'])}.</p>
            <a class="arrow-link" href="{base}work/{st['slug']}/">Read the story {ARROW}</a>
          </div>
        </article>
      </div>
    </section>'''
    more = '\n'.join(f'''          <li><a class="more__link" href="{base}solutions/{o['slug']}/">
            <span class="more__icon" aria-hidden="true">{icon(o['slug'])}</span>
            <span>{esc(o['name'])}</span>
          </a></li>''' for o in others)
    body = f'''
    <section class="chero" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>Solutions</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">{esc(s['name'])}</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">{esc(s['intro'])}</p>
      </div>
    </section>

    <section class="sec band" aria-labelledby="deliverHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>What we deliver</p>
            <h2 class="display" id="deliverHeading" data-reveal style="--d:80ms">{esc(s['short'])}</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">The work this solution covers. Each one is delivered by the same team, on the Microsoft Cloud, and supported after go-live.</p>
        </div>
        <ul class="caps" data-reveal style="--d:160ms">
{caps}
        </ul>
      </div>
    </section>

    <section class="sec band band-tint" aria-labelledby="whyHeading">
      <div class="shell">
        <h2 class="vh" id="whyHeading">Why it matters, how we work, what you get</h2>
        <div class="why">
{why}
        </div>
      </div>
    </section>
{proof}
    <section class="sec band" aria-labelledby="moreHeading">
      <div class="shell">
        <p class="eyebrow" data-reveal>Other solutions</p>
        <h2 class="display" id="moreHeading" data-reveal style="--d:80ms">Usually part of a larger whole</h2>
        <ul class="more" data-reveal style="--d:140ms">
{more}
        </ul>
      </div>
    </section>
{endnote(base, f"Talk to us about {s['name'].lower()}.")}'''
    page(f"solutions/{s['slug']}/index.html", base,
         f"{s['name']} — Solutions | GEMIS®", s['intro'][:180], body)


# ── Products ─────────────────────────────────────────────────────────────
def products_index():
    base = '../'
    cards = []
    for i, p in enumerate(SV.PRODUCTS):
        ext = p['href'].startswith('http')
        href = p['href'] if ext else base + p['href']
        extra = ' target="_blank" rel="noopener"' if ext else ''
        cards.append(f'''          <article class="pcard" data-reveal style="--d:{i * 80}ms">
            <a class="pcard__media" href="{href}"{extra} tabindex="-1" aria-hidden="true">
              <img src="{base}{p['image']}" alt="" loading="lazy" width="760" height="475" />
            </a>
            <div class="pcard__body">
              <p class="eyebrow">{i + 1:02d}</p>
              <h2 class="pcard__name">{esc(p['name'])}</h2>
              <p class="pcard__short">{esc(p['short'])}</p>
              <p class="pcard__copy">{esc(p['body'])}</p>
              <a class="arrow-link" href="{href}"{extra}>{esc(p['cta'])} {ARROW}</a>
            </div>
          </article>''')
    body = f'''
    <section class="chero" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>Products</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">A platform, a studio and an academy</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">Three things GEMIS makes that are ready today: a business management platform to run on, a design studio to design with, and training that keeps your team ahead of the systems they use.</p>
      </div>
    </section>

    <section class="sec band" aria-labelledby="productsHeading">
      <div class="shell">
        <h2 class="vh" id="productsHeading">The three products</h2>
        <div class="pcards">
{chr(10).join(cards)}
        </div>
      </div>
    </section>
{endnote(base, 'Not sure which one fits? Ask us.')}'''
    page('products/index.html', base, 'Products — ManaGEM, Design Studio and the Technical Academy | GEMIS®',
         'ManaGEM, a business management platform; GEMIS Design Studio; and the Technical Academy at '
         'gemis.tech. Three products from a business systems partner operating since 2014.', body)


# ── News & Insights ──────────────────────────────────────────────────────
def post_cards(base='', articles=None):
    cards = []
    for i, a in enumerate(articles or SV.ARTICLES):
        chips = '\n'.join(f'              <li>{esc(c)}</li>' for c in a.get('chips', [a['tag']]))
        cards.append(f'''          <article class="post" data-reveal style="--d:{i * 80}ms">
            <h3 class="post__t"><a href="{base}insights/{a['slug']}/"><span class="post__plus" aria-hidden="true">+</span><span>{esc(a['title'])}</span></a></h3>
            <a class="post__media" href="{base}insights/{a['slug']}/" tabindex="-1" aria-hidden="true">
              <img src="{base}{a['image']}" alt="" loading="lazy" width="1200" height="675" />
            </a>
            <p class="post__meta"><span class="post__tag">{esc(a['tag'])}</span> · <time datetime="{a['date']}">{pretty_date(a['date'])}</time> · {a['read']}</p>
            <p class="post__x">{esc(a['standfirst'])}</p>
            <ul class="post__chips">
{chips}
            </ul>
          </article>''')
    return '\n'.join(cards)


MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
          'September', 'October', 'November', 'December']


def pretty_date(iso):
    y, m, d = iso.split('-')
    return f'{int(d)} {MONTHS[int(m) - 1]} {y}'


def insights_index():
    base = '../'
    body = f'''
    <section class="chero" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>News &amp; Insights</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">Notes from building systems that have to work</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">What we have learned building and running business systems in South Africa — written for the operations and finance leads who have to live with the result.</p>
      </div>
    </section>

    <section class="news band" aria-labelledby="newsHeading">
      <div class="shell">
        <h2 class="vh" id="newsHeading">Articles</h2>
        <div class="news__grid">
{post_cards(base)}
        </div>
      </div>
    </section>
{endnote(base)}'''
    page('insights/index.html', base, 'News & Insights | GEMIS®',
         'Articles on POPIA, load-shedding resilience and moving from spreadsheets to a system, '
         'from a South African business systems partner operating since 2014.', body)


NUMBERED = re.compile(r'^\d+\. ')


def article_body(a):
    out = []
    for h, paras in a['sections']:
        out.append(f'        <h2>{esc(h)}</h2>')
        for ptext in paras:
            lines = ptext.split('\n')
            if len(lines) > 1 and all(NUMBERED.match(l) for l in lines):
                out.append('        <ol>')
                out += ['          <li>' + esc(NUMBERED.sub('', l)) + '</li>' for l in lines]
                out.append('        </ol>')
            else:
                out.append(f'        <p>{esc(ptext)}</p>')
    return '\n'.join(out)


def article_page(a):
    base = '../../'
    others = [o for o in SV.ARTICLES if o['slug'] != a['slug']]
    schema = f'''  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "Article", "headline": {esc(a['title'])!r},
   "datePublished": "{a['date']}", "author": {{"@type": "Organization", "name": "GEM Information Systems (GEMIS)"}},
   "publisher": {{"@type": "Organization", "name": "GEM Information Systems (GEMIS)", "url": "{CANON}"}},
   "mainEntityOfPage": "{CANON}insights/{a['slug']}/"}}
  </script>'''.replace("'", '"')
    body = f'''
    <section class="chero chero--art" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>{esc(a['tag'])}</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">{esc(a['title'])}</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">{esc(a['standfirst'])}</p>
        <p class="art__meta" data-reveal style="--d:200ms"><time datetime="{a['date']}">{pretty_date(a['date'])}</time> · {a['read']} · GEMIS</p>
      </div>
    </section>

    <section class="art band" aria-label="Article">
      <div class="shell art__in">
        <figure class="art__cover" data-reveal>
          <img src="{base}{a['image']}" alt="" width="1200" height="675" />
        </figure>
        <div class="art__body" data-reveal style="--d:80ms">
{article_body(a)}
        </div>
      </div>
    </section>

    <section class="news band band-tint" aria-labelledby="moreHeading">
      <div class="shell">
        <p class="eyebrow" data-reveal>Keep reading</p>
        <h2 class="display" id="moreHeading" data-reveal style="--d:80ms">More from GEMIS</h2>
        <div class="news__grid news__grid--2">
{post_cards(base, others)}
        </div>
      </div>
    </section>
{endnote(base)}'''
    head, tail = P.shell(base, f"{a['title']} | GEMIS®", a['standfirst'][:180],
                         f"{CANON}insights/{a['slug']}/", extra_head=schema)
    path = f"insights/{a['slug']}/index.html"
    os.makedirs(os.path.join(ROOT, os.path.dirname(path)), exist_ok=True)
    open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(head + body + tail)
    print(path)


if __name__ == '__main__':
    solutions_index()
    for s in SV.SERVICES:
        service_page(s)
    products_index()
    insights_index()
    for a in SV.ARTICLES:
        article_page(a)
