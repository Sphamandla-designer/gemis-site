#!/usr/bin/env python3
"""
Apply the canonical header navigation and footer columns to every page.

The site has no include mechanism — header and footer markup is duplicated in
every .html file — so the only way to keep 24 copies identical is to generate
them from one definition. This is not a site generator: it rewrites files in
place and the plain static HTML stays committed to the repository.

    python3 scripts/apply-chrome.py            # rewrite every page
    python3 scripts/apply-chrome.py --check    # fail if any page is out of date

Pages at different depths get different relative prefixes, because the site is
served under /gemis-site/ and must never use root-absolute paths.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pages that carry the corporate chrome. Redirect stubs, the studio (its own
# chrome), generated bundles and the uploaded design exports are all excluded.
SKIP = {
    'solutions.html', 'work.html', 'managem.html', 'brand-studio.html',
    'wastemart-driver.html', 'ManaGem.html',
}
SKIP_PREFIX = ('GEMIS ',)
SKIP_CONTAINS = ('standalone',)

ARROW = ('<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" '
         'aria-hidden="true"><path d="M2.5 9.5 9.5 2.5M4 2.5h5.5V8"/></svg>')

# The two drop-downs are generated from scripts/services.py, so a service or a
# product added there appears in the navigation on every page.
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location('services', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'services.py'))
SV = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(SV)


def _service_items():
    out = []
    for i, s in enumerate(SV.SERVICES, 1):
        out.append(
            f'                <li><a class="msvc" href="{{B}}solutions/{s["slug"]}/">'
            f'<span class="msvc__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{SV.ICONS[s["slug"]]}</svg></span>'
            f'<span class="msvc__body"><span class="msvc__name">{s["name"]}</span>'
            f'<span class="msvc__line">{s["short"]}</span></span></a></li>')
    return '\n'.join(out)


def _product_items():
    out = []
    for p in SV.PRODUCTS:
        ext = p['href'].startswith('http')
        href = p['href'] if ext else '{B}' + p['href']
        extra = ' target="_blank" rel="noopener"' if ext else ''
        out.append(f"""              <article class="prod">
                <a class="prod__media" href="{href}"{extra} tabindex="-1" aria-hidden="true">
                  <img src="{{B}}{p['image']}" alt="" loading="lazy" width="760" height="475" />
                </a>
                <div class="prod__body">
                  <h3 class="prod__name">{p['name']}</h3>
                  <p class="prod__desc">{p['short']}</p>
                  <a class="prod__cta" href="{href}"{extra}>{p['cta']} {{ARROW}}</a>
                </div>
              </article>""")
    return '\n\n'.join(out)


NAV = """<ul class="nav__links" id="navLinks">
        <li><a href="{B}index.html">Home</a></li>
        <li><a href="{B}work/">Case Studies</a></li>
        <li class="nav__item nav__item--mega" data-mega>
          <button class="nav__trigger" id="solutionsTrigger" aria-expanded="false" aria-controls="solutionsMenu">
            Solutions
            <svg class="nav__chev" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 1.5 5 5 9 1.5"/></svg>
          </button>

        <div class="mega" id="solutionsMenu" aria-labelledby="solutionsTrigger">
          <div class="shell mega__in">
            <div class="mega__head">
              <p class="eyebrow">Solutions</p>
              <p class="mega__lede">Nine disciplines, one accountable team. Most engagements draw on several at once.</p>
              <a class="arrow-link" href="{B}solutions/">All solutions {ARROW}</a>
            </div>

            <ul class="mega__svcs">
""" + _service_items() + """
            </ul>
          </div>
        </div>
        </li>
        <li class="nav__item nav__item--mega" data-mega>
          <button class="nav__trigger" id="productsTrigger" aria-expanded="false" aria-controls="productsMenu">
            Products
            <svg class="nav__chev" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 1.5 5 5 9 1.5"/></svg>
          </button>

        <div class="mega" id="productsMenu" aria-labelledby="productsTrigger">
          <div class="shell mega__in">
            <div class="mega__head">
              <p class="eyebrow">Products</p>
              <p class="mega__lede">A platform ready to run on, a studio to design with, and training to keep your team ahead.</p>
              <a class="arrow-link" href="{B}products/">All products {ARROW}</a>
            </div>

            <div class="mega__grid">
""" + _product_items() + """
            </div>
          </div>
        </div>
        </li>
        <li><a href="{B}our-story/">About</a></li>
        <li><a href="{B}contact.html">Contact</a></li>
        </ul>"""

FOOTER_COLS = """<div class="foot__col">
          <h2>Solutions</h2>
          <ul>
""" + '\n'.join(f'            <li><a href="{{B}}solutions/{s["slug"]}/">{s["name"]}</a></li>' for s in SV.SERVICES[:5]) + """
            <li><a href="{B}solutions/">All solutions</a></li>
          </ul>
        </div>

        <div class="foot__col">
          <h2>Products</h2>
          <ul>
            <li><a href="https://sphamandla-designer.github.io/ManaGEM/" target="_blank" rel="noopener">ManaGEM</a></li>
            <li><a href="{B}studio/">Design Studio</a></li>
            <li><a href="https://gemis.tech/" target="_blank" rel="noopener">Technical Academy</a></li>
            <li><a href="{B}work/">Case Studies</a></li>
            <li><a href="{B}insights/">News &amp; Insights</a></li>
          </ul>
        </div>

        <div class="foot__col">
          <h2>Support &amp; Resources</h2>
          <ul>
            <li><a href="{B}our-story/">About GEMIS</a></li>
            <li><a href="{B}contact.html">Contact Us</a></li>
            <li><a href="{B}solutions/support/">Ongoing Support</a></li>
            <li><a href="{B}industries.html">Industries</a></li>
            <li><a href="{B}privacy.html">Privacy Policy</a></li>
          </ul>
        </div>"""

NAV_RE = re.compile(r'<ul class="nav__links" id="navLinks">.*?\n        </ul>', re.S)
FOOT_RE = re.compile(r'<div class="foot__col">\s*<h2>(?:Products|Solutions)</h2>.*?'
                     r'<h2>Support &amp; Resources</h2>.*?</ul>\s*</div>', re.S)


def pages():
    """Every page that carries the corporate chrome, at any depth."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in {'.git', 'node_modules', 'studio', 'assets', 'scripts', 'tools', 'qa', '_project'}]
        for name in sorted(filenames):
            if not name.endswith('.html'):
                continue
            if name in SKIP or name.startswith(SKIP_PREFIX) or any(s in name for s in SKIP_CONTAINS):
                continue
            yield os.path.join(dirpath, name)


def base_for(path):
    """Relative prefix back to the site root, e.g. '' , '../' , '../../'."""
    depth = os.path.relpath(path, ROOT).count(os.sep)
    return '../' * depth


def render(template, base):
    return template.replace('{ARROW}', ARROW).replace('{B}', base)


def main():
    check = '--check' in sys.argv
    changed, stale = [], []
    for path in pages():
        html = open(path, encoding='utf-8').read()
        base = base_for(path)
        out = html
        if NAV_RE.search(out):
            out = NAV_RE.sub(lambda m: render(NAV, base), out, count=1)
        if FOOT_RE.search(out):
            out = FOOT_RE.sub(lambda m: render(FOOTER_COLS, base), out, count=1)
        rel = os.path.relpath(path, ROOT)
        if out != html:
            (stale if check else changed).append(rel)
            if not check:
                open(path, 'w', encoding='utf-8').write(out)
    if check:
        if stale:
            print('chrome out of date in:\n  ' + '\n  '.join(stale))
            return 1
        print('chrome: every page matches the canonical header and footer.')
        return 0
    print(f'chrome applied to {len(changed)} page(s):\n  ' + '\n  '.join(changed) if changed
          else 'chrome: nothing to change.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
