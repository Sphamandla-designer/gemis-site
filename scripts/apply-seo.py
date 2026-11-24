#!/usr/bin/env python3
"""
Write the SEO layer into every corporate page, from scripts/seo.py.

For each page in seo.PAGES:
  - the <head> metadata: <title>, description, robots, canonical, Open Graph
    (with en_ZA locale and the image's size and alt) and Twitter/X tags, as one
    managed block between <!--#seo:head--> and <!--#seo:head-end-->;
  - the H1's words (its element, classes and rising spans are kept);
  - one JSON-LD graph between <!--#seo:ld--> and <!--#seo:ld-end-->:
    Organization and WebSite (the same @ids on every page), the page itself
    (WebPage / CollectionPage / AboutPage / ContactPage), its BreadcrumbList,
    and Service, Article or SoftwareApplication where the page is one.
    The generators keep emitting what is page content and correct — FAQPage,
    ItemList and VideoObject — and no longer emit what this replaces.
And sitemap.xml: every indexable page of both sites, with lastmod from git.

Run it last in the full rebuild (after apply-chrome). `--check` writes nothing
and fails if any page or the sitemap would change, or seo.py fails validation.
"""
import datetime
import html
import importlib.util
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SEO = _load('seo', 'seo.py')
B = _load('build_stories', 'build-stories.py')
SV = _load('services', 'services.py')
SOLS = _load('solutions', 'solutions.py')

CANON = SEO.CANON
ORG_ID, SITE_ID = CANON + '#organization', CANON + '#website'
esc = lambda s: html.escape(s, quote=True)

HEAD_RE = re.compile(r'\n?[ \t]*<!--#seo:head-->.*?<!--#seo:head-end-->', re.S)
LD_RE = re.compile(r'\n?[ \t]*<!--#seo:ld-->.*?<!--#seo:ld-end-->', re.S)
# what the managed head block owns; any stray copy elsewhere in <head> goes
OWNED = [
    re.compile(r'\n?[ \t]*<title>.*?</title>', re.S),
    re.compile(r'\n?[ \t]*<meta name="(description|robots|google-site-verification)"[^>]*>'),
    re.compile(r'\n?[ \t]*<link rel="canonical"[^>]*>'),
    re.compile(r'\n?[ \t]*<meta property="og:[^"]*"[^>]*>'),
    re.compile(r'\n?[ \t]*<meta name="twitter:[^"]*"[^>]*>'),
]
# structured data this script now writes; generators must not emit it too
REPLACED_TYPES = {'Organization', 'WebSite', 'BreadcrumbList', 'Service', 'Article', 'SoftwareApplication'}
LD_BLOCK = re.compile(r'\n?[ \t]*<script type="application/ld\+json">(.*?)</script>', re.S)


def image_of(v):
    if v.get('image'):
        return CANON + v['image'], 1280, 720, v.get('image_alt') or f"{v.get('client') or v.get('product')} — a frame from the case study video"
    return CANON + SEO.CARD, 1200, 630, SEO.CARD_ALT


def crumb_name(path, given):
    if given:
        return given
    slug = path.rstrip('/').split('/')[-1]
    if path.startswith('solutions/'):
        return SV.BY_SLUG[slug]['name']
    if path.startswith('insights/'):
        return SV.ARTICLE_BY_SLUG[slug]['title']
    return slug


def head_block(path, v):
    url = SEO.url(path)
    img, w, h, alt = image_of(v)
    article = v['kind'] in ('article', 'case')
    robots = 'noindex, follow' if v['kind'] == 'notfound' else 'index, follow, max-image-preview:large'
    lines = [
        '<!--#seo:head-->',
        f'<title>{esc(v["title"])}</title>',
        f'<meta name="description" content="{esc(v["description"])}" />',
        f'<meta name="robots" content="{robots}" />',
    ]
    if v['kind'] != 'notfound':
        lines.append(f'<link rel="canonical" href="{url}" />')
    if v['kind'] == 'home' and SEO.GSC_VERIFICATION:
        lines.append(f'<meta name="google-site-verification" content="{esc(SEO.GSC_VERIFICATION)}" />')
    lines += [
        f'<meta property="og:type" content="{"article" if article else "website"}" />',
        '<meta property="og:site_name" content="GEM Information Systems" />',
        '<meta property="og:locale" content="en_ZA" />',
        f'<meta property="og:title" content="{esc(v["title"])}" />',
        f'<meta property="og:description" content="{esc(v["description"])}" />',
        f'<meta property="og:url" content="{url}" />',
        f'<meta property="og:image" content="{img}" />',
        f'<meta property="og:image:width" content="{w}" />',
        f'<meta property="og:image:height" content="{h}" />',
        f'<meta property="og:image:alt" content="{esc(alt)}" />',
        '<meta name="twitter:card" content="summary_large_image" />',
        f'<meta name="twitter:title" content="{esc(v["title"])}" />',
        f'<meta name="twitter:description" content="{esc(v["description"])}" />',
        f'<meta name="twitter:image" content="{img}" />',
        f'<meta name="twitter:image:alt" content="{esc(alt)}" />',
        '<!--#seo:head-end-->',
    ]
    return '\n'.join('  ' + l for l in lines)


def org_node():
    o = SEO.ORG
    return {
        '@type': 'Organization', '@id': ORG_ID, 'name': o['name'], 'alternateName': o['alternateName'],
        'legalName': o['legalName'], 'url': CANON,
        'logo': {'@type': 'ImageObject', 'url': CANON + o['logo']},
        'email': o['email'], 'foundingDate': o['foundingDate'], 'slogan': o['slogan'],
        'address': {'@type': 'PostalAddress', **o['address']},
        'contactPoint': {'@type': 'ContactPoint', 'contactType': 'sales', 'email': o['email'],
                         'areaServed': 'ZA', 'availableLanguage': 'en'},
        'sameAs': o['sameAs'],
    }


def graph(path, v):
    url = SEO.url(path)
    img, w, h, _ = image_of(v)
    page_type = {'home': 'WebPage', 'collection': 'CollectionPage', 'about': 'AboutPage',
                 'contact': 'ContactPage'}.get(v['kind'], 'WebPage')
    page = {'@type': page_type, '@id': url + '#webpage', 'url': url, 'name': v['title'],
            'description': v['description'], 'inLanguage': 'en-ZA', 'isPartOf': {'@id': SITE_ID},
            'about': {'@id': ORG_ID} if v['kind'] in ('home', 'about', 'contact') else None,
            'primaryImageOfPage': {'@type': 'ImageObject', 'url': img}}
    nodes = [org_node(),
             {'@type': 'WebSite', '@id': SITE_ID, 'url': CANON, 'name': 'GEMIS — GEM Information Systems',
              'inLanguage': 'en-ZA', 'publisher': {'@id': ORG_ID}},
             page]
    if v.get('crumbs'):
        bc = {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': crumb_name(p, n), 'item': SEO.url(p or 'index.html')}
            for i, (n, p) in enumerate(v['crumbs'])]}
        nodes.append(bc)
        page['breadcrumb'] = {'@id': bc['@id']}
    slug = path.rstrip('/').split('/')[-1]
    if v['kind'] == 'service':
        s = SV.BY_SLUG[slug]
        nodes.append({'@type': 'Service', '@id': url + '#service', 'name': s['name'], 'serviceType': s['name'],
                      'description': SOLS.PAGES[slug]['copy'], 'url': url, 'provider': {'@id': ORG_ID},
                      'areaServed': {'@type': 'Country', 'name': 'South Africa'}})
        page['mainEntity'] = {'@id': url + '#service'}
    elif v['kind'] in ('article', 'case'):
        art = {'@type': 'Article', '@id': url + '#article', 'headline': v['h1'], 'description': v['description'],
               'image': img, 'author': {'@id': ORG_ID}, 'publisher': {'@id': ORG_ID},
               'mainEntityOfPage': {'@id': url + '#webpage'}, 'inLanguage': 'en-ZA'}
        if v['kind'] == 'article':
            art['datePublished'] = SV.ARTICLE_BY_SLUG[slug]['date']
        else:
            art['about'] = {'@type': 'Organization', 'name': v['client']}
        nodes.append(art)
        page['mainEntity'] = {'@id': art['@id']}
    elif v['kind'] == 'product':
        # no published price, platform or reviews, so none are stated: this
        # describes ManaGEM but does not qualify for a software rich result
        nodes.append({'@type': 'SoftwareApplication', '@id': url + '#software', 'name': v['product'],
                      'applicationCategory': 'BusinessApplication', 'description': v['description'],
                      'url': url, 'image': img, 'publisher': {'@id': ORG_ID}})
        page['mainEntity'] = {'@id': url + '#software'}
    page.update({k: x for k, x in page.items() if x is not None})
    for k in [k for k, x in page.items() if x is None]:
        del page[k]
    data = {'@context': 'https://schema.org', '@graph': nodes}
    body = json.dumps(data, ensure_ascii=False, indent=2).replace('</', '<\\/')
    return f'  <!--#seo:ld-->\n  <script type="application/ld+json">\n{body}\n  </script>\n  <!--#seo:ld-end-->'


def set_h1(doc, v):
    m = re.search(r'(<h1\b[^>]*>)(.*?)(</h1>)', doc, re.S)
    if not m or not v.get('h1'):
        return doc
    inner = m.group(2)
    if 'hx-rise' in inner:
        halves = B.two_lines(esc(v['h1'])).split('<br class="h1-br">')
        # the break drops on phones (.hx-br in site.css), where the halves flow together
        new = '<br class="hx-br" />'.join(f'<span class="hx-rise" style="--i:{i}">{x.strip()}</span>' for i, x in enumerate(halves))
    else:
        new = esc(v['h1'])
    doc = doc[:m.start(2)] + new + doc[m.end(2):]
    if v.get('h1_sub'):
        doc = re.sub(r'(<p class="hx-label hx-hero__sub">).*?(</p>)', lambda s: s.group(1) + esc(v['h1_sub']) + s.group(2), doc, count=1, flags=re.S)
    return doc


def apply(path, v, doc):
    head, rest = doc.split('</head>', 1)
    head = HEAD_RE.sub('', head)
    head = LD_RE.sub('', head)
    for rx in OWNED:
        head = rx.sub('', head)

    def keep(m):
        try:
            d = json.loads(m.group(1))
        except ValueError:
            return m.group(0)
        types = {n.get('@type') for n in d.get('@graph', [d])} if isinstance(d, dict) else set()
        return '' if types and types <= REPLACED_TYPES else m.group(0)
    head = LD_BLOCK.sub(keep, head)
    # the head block goes straight after the viewport meta, before any resource
    vp = re.search(r'<meta name="viewport"[^>]*>', head)
    head = head[:vp.end()] + '\n' + head_block(path, v) + head[vp.end():]
    head = head.rstrip() + '\n' + (graph(path, v) + '\n' if v['kind'] != 'notfound' else '')
    return set_h1(head + '</head>' + rest, v)


def file_of(path):
    return os.path.join(ROOT, path + ('index.html' if path.endswith('/') else ''))


def lastmod(rel):
    dirty = subprocess.run(['git', 'status', '--porcelain', '--', rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if dirty:
        return datetime.date.today().isoformat()
    out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', rel], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return out or datetime.date.today().isoformat()


def sitemap():
    urls = []
    for path, v in SEO.PAGES.items():
        if v['kind'] == 'notfound':
            continue
        rel = os.path.relpath(file_of(path), ROOT)
        urls.append((SEO.url(path), rel))
    # the studio: every built page that is not noindex, home first
    studio = sorted(f for f in os.listdir(os.path.join(ROOT, 'studio')) if f.endswith('.html'))
    studio.sort(key=lambda f: (f != 'index.html', f.startswith('work-'), f))
    for f in studio:
        doc = open(os.path.join(ROOT, 'studio', f), encoding='utf-8').read()
        if re.search(r'<meta name="robots" content="[^"]*noindex', doc) or 'http-equiv="refresh"' in doc:
            continue
        urls.append((CANON + 'studio/' + ('' if f == 'index.html' else f), 'studio/' + f))
    rows = '\n'.join(f'  <url><loc>{u}</loc><lastmod>{lastmod(r)}</lastmod></url>' for u, r in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + '\n</urlset>\n')


def main():
    check = '--check' in sys.argv
    problems = SEO.validate()
    stale, written = [], []
    for path, v in SEO.PAGES.items():
        f = file_of(path)
        if not os.path.exists(f):
            problems.append(f'{path}: seo.py names a page that does not exist')
            continue
        doc = open(f, encoding='utf-8').read()
        out = apply(path, v, doc)
        if len(re.findall(r'<h1\b', out)) != 1:
            problems.append(f'{path}: {len(re.findall(r"<h1\\b", out))} H1 elements')
        if out != doc:
            (stale if check else written).append(path)
            if not check:
                open(f, 'w', encoding='utf-8').write(out)
    sm_path = os.path.join(ROOT, 'sitemap.xml')
    sm, old = sitemap(), open(sm_path, encoding='utf-8').read()
    # lastmod moves with every commit; --check compares the URL list only
    strip = lambda x: re.sub(r'<lastmod>[^<]*</lastmod>', '', x)
    if strip(sm) != strip(old):
        (stale if check else written).append('sitemap.xml')
    if not check and sm != old:
        open(sm_path, 'w', encoding='utf-8').write(sm)
    if problems:
        print('seo problems:\n  ' + '\n  '.join(problems))
        return 1
    if check:
        if stale:
            print('seo out of date in:\n  ' + '\n  '.join(stale))
            return 1
        print(f'seo: all {len(SEO.PAGES)} pages and the sitemap match scripts/seo.py.')
        return 0
    print(f'seo applied to {len(written)} file(s)' + (':\n  ' + '\n  '.join(written) if written else '.'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
