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
        <a class="arrow-link" href="{base}contact.html" data-reveal style="--d:140ms">Book a discovery session {ARROW}</a>
      </div>
    </section>
'''


# the case study each article's argument comes from
# the disciplines each article discusses (internal linking; checked against the text:
# POPIA — custom systems and where data is hosted; load-shedding — cloud hosting
# and offline-capable mobile apps; spreadsheets — moving to a system and its reporting)
ARTICLE_SOLUTIONS = {
    'popia-business-systems-checklist': ['custom-software', 'microsoft-cloud'],
    'load-shedding-operations-resilience': ['microsoft-cloud', 'mobile-apps'],
    'spreadsheets-to-a-system': ['custom-software', 'business-intelligence'],
}

ARTICLE_STORY = {
    'spreadsheets-to-a-system': ('sbs-waterproofing', 'SBS Waterproofing moved from a spreadsheet and three apps to one system in 2015, and still runs on it.'),
    'load-shedding-operations-resilience': ('sonke', 'Sonke’s field app was designed for no signal at all: it captures offline and syncs when it can.'),
    'popia-business-systems-checklist': ('homeassist', 'HomeAssist’s system holds homeowner, insurer and plumber data on one job record, with each party seeing only its side.'),
}

# The visual that heads each article's card (2026-11-26, the owner's instruction:
# the top of the card is all image, not a pictogram): a still from the case study
# behind the article (ARTICLE_STORY), from that project's own video.
ARTICLE_STILL = {
    'spreadsheets-to-a-system': 'assets/img/cases/sbs-waterproofing/01-enquiry.jpg',
    'load-shedding-operations-resilience': 'assets/img/cases/sonke/01-capture.jpg',
    'popia-business-systems-checklist': 'assets/img/cases/homeassist/01-intake.jpg',
}


# ── Products ─────────────────────────────────────────────────────────────
def products_index():
    base = '../'
    cards = []
    for i, p in enumerate(SV.PRODUCTS):
        ext = p['href'].startswith('http')
        href = p['href'] if ext else base + p['href']
        cards.append(f'''          <article class="post post--picto" data-reveal style="--d:{i * 80}ms">
            <p class="post__meta hx-label">{i + 1:02d} · {esc(p["short"])}</p>
            <a class="post__media post__media--picto" href="{href}" tabindex="-1" aria-hidden="true">{B.picto(B.PICTO_FOR_PRODUCT[p['slug']], 'hx-picto--w')}</a>
            <h3 class="post__t"><a href="{href}">{esc(p['name'])}</a></h3>
            <p class="post__x">{esc(p['body'])}</p>
            <a class="arrow-link" href="{href}">{esc(p["cta"])} {ARROW}</a>
          </article>''')
    cards = '\n'.join(cards)
    if True:
        # the external product opens in a new tab
        cards = cards.replace('href="https://gemis.tech/"', 'href="https://gemis.tech/" target="_blank" rel="noopener"')
        cards = cards.replace('href="https://sphamandla-designer.github.io/ManaGEM/"', 'href="https://sphamandla-designer.github.io/ManaGEM/" target="_blank" rel="noopener"')
    body = f'''
{B.hero_block('Products', B.two_lines("A platform, a studio and an academy"),
              'Three things GEMIS makes that are ready today: a business management platform to run on, a design studio to design with, and training that keeps your team ahead of the systems they use.',
              ctas=f'<a class="hx-btn hx-btn--light" href="{base}products/managem/">Explore ManaGEM</a><a class="hx-btn hx-btn--ghost" href="{base}contact.html">Book a discovery session</a>',
              visual=f'<div class="hx-phero__picto">{B.picto("blocks", "hx-picto--w hx-picto--xl")}</div>', strip='ManaGEM · Design Studio · Technical Academy')}

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
    # image on top, then the meta, the title and the standfirst (clamped to two
    # lines). The tag chips are off the card: they made it read as text, not a picture
    cards = []
    for i, a in enumerate(articles or SV.ARTICLES):
        still = ARTICLE_STILL.get(a['slug'])
        media = (f'<img src="{base}{still}" alt="" loading="lazy" decoding="async" width="1200" height="675">' if still
                 else B.picto(B.PICTO_FOR_TAG.get(a['tag'], 'letter'), 'hx-picto--w'))
        cards.append(f'''          <article class="post post--img" data-reveal style="--d:{i * 80}ms">
            <a class="post__media post__media--img" href="{base}insights/{a['slug']}/" tabindex="-1" aria-hidden="true">{media}</a>
            <p class="post__meta"><span class="post__tag">{esc(a['tag'])}</span> · <time datetime="{a['date']}">{pretty_date(a['date'])}</time> · {a['read']}</p>
            <h3 class="post__t"><a href="{base}insights/{a['slug']}/"><span class="post__plus" aria-hidden="true">+</span><span>{esc(a['title'])}</span></a></h3>
            <p class="post__x">{esc(a['standfirst'])}</p>
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
{B.hero_block('News &amp; Insights', B.two_lines("Notes from building systems that have to work"),
              'What we have learned building and running business systems in South Africa — written for the operations and finance leads who have to live with the result.',
              ctas=f'<a class="hx-btn hx-btn--light" href="{base}contact.html">Book a discovery session</a><a class="hx-btn hx-btn--ghost" href="{base}work/">See the case studies</a>',
              visual=f'<div class="hx-phero__picto">{B.picto("letter", "hx-picto--w hx-picto--xl")}</div>', strip='Three articles · each with the case study behind it')}

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
    schema = ''   # the Article node is written by scripts/apply-seo.py
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
          <p class="lede" data-reveal style="--d:140ms">{esc(line)} Related solutions: {' and '.join(f'<a href="{base}solutions/{k}/">{esc(SV.BY_SLUG[k]["name"])}</a>' for k in ARTICLE_SOLUTIONS.get(a['slug'], []))}.</p>
        </div>
        <div class="cscards cscards--2">
{B.cscard(S.BY_SLUG[k], base, 0)}
        </div>
      </div>
    </section>
'''
    pk = B.PICTO_FOR_TAG.get(a['tag'], 'letter')
    body = f'''
{B.hero_block(esc(a['tag']), B.two_lines(esc(a['title'])), esc(a['standfirst']),
              ctas=f'<a class="hx-btn hx-btn--ghost" href="{base}insights/">All insights</a>',
              visual=f'<div class="hx-phero__picto">{B.picto(pk, "hx-picto--w hx-picto--xl")}</div>',
              strip=f'<p class="hx-label hx-hero__strip-label art__meta"><time datetime="{a["date"]}">{pretty_date(a["date"])}</time> · {a["read"]} · GEMIS</p>')}

    <section class="art band" aria-label="Article">
      <div class="shell art__in">
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
