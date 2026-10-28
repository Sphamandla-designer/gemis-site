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
# the pictogram sprite (symbols and the two hatch patterns) rides in the
# footer, so every page can draw a hatch pictogram with <use href="#px-…">
_bspec = _ilu.spec_from_file_location('build_stories', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build-stories.py'))
_B = _ilu.module_from_spec(_bspec)
_bspec.loader.exec_module(_B)
SPRITE = _B.picto_sprite()


def _service_items():
    out = []
    for i, s in enumerate(SV.SERVICES, 1):
        out.append(
            f'                <li><a class="msvc" href="{{B}}solutions/{s["slug"]}/">'
            f'<span class="msvc__icon" aria-hidden="true">{_B.picto(s["slug"], "hx-picto--w")}</span>'
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
        <li><a href="{B}insights/">Insights</a></li>
        <li><a href="{B}our-story/">Our Story</a></li>
        <li><a href="{B}contact.html">Contact</a></li>
        </ul>"""

# ── the footer: ported from the efferd footer-3 block (React/Tailwind) into
#    the site's own markup — brand column, four link sections (the last carries
#    icons), a gradient hairline, a centred legal line; a top glow and a
#    blur-and-rise reveal per section (site.js adds .is-in; static without JS and
#    under reduced motion). Expanded to the site's shell width on the navy ground.
LINKEDIN = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>'
GLOBE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.7 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.7-3.8-9S9.5 5.6 12 3Z"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="2.5" y="4.5" width="19" height="15" rx="2"/><path d="m3 6.5 9 6.5 9-6.5"/></svg>'

def _col(label, items, delay):
    lis = '\n'.join(f'              <li>{a}</li>' for a in items)
    return f"""        <div class="foot__col" data-reveal style="--d:{delay}ms">
            <h2>{label}</h2>
            <ul>
{lis}
            </ul>
          </div>"""

FOOTER = """<footer class="foot">
    """ + SPRITE + """
    <span class="foot__glow" aria-hidden="true"></span>
    <div class="shell foot__in">
      <div class="foot__grid">
        <div class="foot__brand" data-reveal>
          <a class="foot__logo" href="{B}index.html" aria-label="GEMIS home"><svg class="logo" viewBox="0 0 187 34" aria-hidden="true" focusable="false"><use href="#gemisLogo"/></svg></a>
          <p class="foot__blurb">Bringing ideas and innovation to life through technology &mdash; secure, scalable systems built on the Microsoft Cloud.</p>
          <address class="foot__addr">9 Tapiola Way, Edgemead, Cape Town<br /><a href="mailto:info@gemis.co.za">info@gemis.co.za</a></address>
        </div>
        <div class="foot__cols">
  """ + _col('Solutions', [f'<a href="{{B}}solutions/{s["slug"]}/">{s["name"]}</a>' for s in SV.SERVICES[:4]] + ['<a href="{B}solutions/">All solutions</a>'], 100) + """
  """ + _col('Products', ['<a href="{B}products/managem/">ManaGEM</a>', '<a href="{B}studio/">Design Studio</a>',
                           '<a href="https://gemis.tech/" target="_blank" rel="noopener">Technical Academy</a>', '<a href="{B}products/">All products</a>'], 200) + """
  """ + _col('Company', ['<a href="{B}our-story/">Our Story</a>', '<a href="{B}work/">Case Studies</a>', '<a href="{B}insights/">Insights</a>',
                          '<a href="{B}industries.html">Industries</a>', '<a href="{B}contact.html">Contact</a>'], 300) + """
  """ + _col('Connect', ['<a href="https://www.linkedin.com/company/gem-information-systems-pty-ltd/" target="_blank" rel="noopener">' + LINKEDIN + 'LinkedIn</a>',
                          '<a href="https://www.gemis.co.za" target="_blank" rel="noopener">' + GLOBE + 'gemis.co.za</a>',
                          '<a href="mailto:info@gemis.co.za">' + MAIL + 'info@gemis.co.za</a>'], 400) + """
        </div>
      </div>
      <div class="foot__rule" aria-hidden="true"></div>
      <div class="foot__bar">
        <p>&copy; 2026 GEM Information Systems (PTY) LTD. All rights reserved.</p>
        <a href="{B}privacy.html">Privacy Policy</a>
      </div>
    </div>
  </footer>"""

NAV_RE = re.compile(r'<ul class="nav__links" id="navLinks">.*?\n        </ul>', re.S)
FOOTER_RE = re.compile(r'<footer class="foot">.*?</footer>', re.S)


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
        if FOOTER_RE.search(out):
            out = FOOTER_RE.sub(lambda m: render(FOOTER, base), out, count=1)
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
