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
import json
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
SOLB = load('build_solutions', 'build-solutions.py')

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
        <a class="arrow-link" href="{base}contact.html" data-reveal style="--d:140ms">Discuss a project {ARROW}</a>
      </div>
    </section>
'''


# the case study each article's argument comes from
ARTICLE_STORY = {
    'spreadsheets-to-a-system': ('sbs-waterproofing', 'SBS Waterproofing moved from a spreadsheet and three apps to one system in 2015, and still runs on it.'),
    'load-shedding-operations-resilience': ('sonke', 'Sonke’s field app was designed for no signal at all: it captures offline and syncs when it can.'),
    'popia-business-systems-checklist': ('homeassist', 'HomeAssist’s system holds homeowner, insurer and plumber data on one job record, with each party seeing only its side.'),
}


# ── Products ─────────────────────────────────────────────────────────────
def products_index():
    base = '../'
    cards = []
    for i, p in enumerate(SV.PRODUCTS):
        ext = p['href'].startswith('http')
        href = p['href'] if ext else base + p['href']
        cards.append(B.feat(esc(p['name']), href, f"{base}{p['image']}", f'{i + 1:02d} · {esc(p["short"])}',
                            esc(p['body']), link=f'<a class="arrow-link" href="{href}">{esc(p["cta"])} {ARROW}</a>',
                            extra_attrs=f' data-reveal style="--d:{i * 80}ms"'))
    cards = '\n'.join(cards)
    if True:
        # the external product opens in a new tab
        cards = cards.replace('href="https://gemis.tech/"', 'href="https://gemis.tech/" target="_blank" rel="noopener"')
        cards = cards.replace('href="https://sphamandla-designer.github.io/ManaGEM/"', 'href="https://sphamandla-designer.github.io/ManaGEM/" target="_blank" rel="noopener"')
    body = f'''
    <section class="chero" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>Products</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">{B.two_lines("A platform, a studio and an academy")}</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">Three things GEMIS makes that are ready today: a business management platform to run on, a design studio to design with, and training that keeps your team ahead of the systems they use.</p>
      </div>
    </section>

    <section class="sec band plusgrid plusgrid--tr" aria-labelledby="productsHeading">
      <div class="shell">
        <h2 class="vh" id="productsHeading">The three products</h2>
        <div class="feats">
{cards}
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
        <h1 class="chero__title" data-reveal style="--d:80ms">{B.two_lines("Notes from building systems that have to work")}</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">What we have learned building and running business systems in South Africa — written for the operations and finance leads who have to live with the result.</p>
      </div>
    </section>

    <section class="news band plusgrid plusgrid--tr" aria-labelledby="newsHeading">
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
    practice = ''
    if a['slug'] in ARTICLE_STORY:
        k, line = ARTICLE_STORY[a['slug']]
        practice = f'''
    <section class="sec band band-wash" aria-labelledby="practiceHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>In practice</p>
            <h2 class="display" id="practiceHeading" data-reveal style="--d:80ms">The case study behind this article</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">{esc(line)}</p>
        </div>
        <div class="cscards cscards--2">
{B.cscard(S.BY_SLUG[k], base, 0)}
        </div>
      </div>
    </section>
'''
    body = f'''
    <section class="chero chero--art" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>{esc(a['tag'])}</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">{B.two_lines(esc(a['title']))}</h1>
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

{practice}
    <section class="news band" aria-labelledby="moreHeading">
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
    SOLB.build()          # /solutions/ and the nine service pages
    products_index()
    insights_index()
    for a in SV.ARTICLES:
        article_page(a)
