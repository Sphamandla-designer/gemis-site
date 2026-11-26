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
        <li class="nav__cta-item"><a class="nav__cta" href="{B}contact.html">Book a discovery session</a></li>
        </ul>"""

def _col(label, items, delay):
    lis = '\n'.join(f'              <li>{a}</li>' for a in items)
    return f"""          <div class="ftr__col" data-reveal style="--d:{delay}ms">
            <h2 class="ftr__label">{label}</h2>
            <ul>
{lis}
            </ul>
          </div>"""

OUT = '<span class="ftr__out" aria-hidden="true">&#8599;</span>'

# FOOTER v6 (2026-11-24) — after the owner's reference: a statement and the one
# action across the top, four plain link columns and a legal bar. Light ground, so it reads apart from the navy closing
# tile above it on nearly every page.
FOOTER = """<footer class="ftr">
    """ + SPRITE + """
    <div class="shell ftr__in">
      <div class="ftr__top">
        <div class="ftr__brand" data-reveal>
          <a class="ftr__logo" href="{B}index.html" aria-label="GEMIS home"><svg class="logo" viewBox="{LOGO_VB}" aria-hidden="true" focusable="false"><use href="#gemisLogo"/></svg></a>
          <p class="ftr__say">Systems built to last.<br />Partners built to stay.</p>
        </div>
        <div class="ftr__act" data-reveal style="--d:100ms">
          <p class="ftr__lede">Tell us what your operation needs to do better. A discovery session is where it starts.</p>
          <a class="ftr__go" href="{B}contact.html"><span>Book a discovery session</span><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg></a>
          <p class="ftr__or">Or write to <a href="mailto:info@gemis.co.za">info@gemis.co.za</a></p>
        </div>
      </div>
      <div class="ftr__cols">
""" + _col('Solutions', [f'<a href="{{B}}solutions/{s["slug"]}/">{s["name"]}</a>' for s in SV.SERVICES[:4]] + ['<a href="{B}solutions/">All solutions</a>'], 0) + """
""" + _col('Products', ['<a href="{B}products/managem/">ManaGEM</a>', '<a href="{B}studio/">Design Studio</a>',
                         '<a href="https://gemis.tech/" target="_blank" rel="noopener">Technical Academy' + OUT + '</a>', '<a href="{B}products/">All products</a>'], 80) + """
""" + _col('Company', ['<a href="{B}our-story/">Our Story</a>', '<a href="{B}work/">Case Studies</a>', '<a href="{B}insights/">Insights</a>',
                        '<a href="{B}industries.html">Industries</a>', '<a href="{B}contact.html">Contact</a>'], 160) + """
""" + _col('Connect', ['<a href="https://www.linkedin.com/company/gem-information-systems-pty-ltd/" target="_blank" rel="noopener">LinkedIn' + OUT + '</a>',
                        '<a href="https://www.gemis.co.za" target="_blank" rel="noopener">gemis.co.za' + OUT + '</a>',
                        '<a href="mailto:info@gemis.co.za">info@gemis.co.za</a>'], 240) + """
      </div>
    </div>
    <div class="shell ftr__bar">
      <nav class="ftr__legal" aria-label="Legal"><a href="{B}privacy.html">Privacy notice</a><a href="{B}terms.html">Terms of use</a><a href="{B}privacy.html#cookies" data-cookie-settings>Cookie settings</a></nav>
      <address class="ftr__addr">9 Tapiola Way, Edgemead, Cape Town</address>
      <p class="ftr__copy">&copy; 2026 GEM Information Systems (PTY) LTD</p>
    </div>
  </footer>"""

# The few <head> lines every page shares, kept here so no page drifts: the
# icons, the HTTPS upgrade for any stray http:// subresource, and the consent
# loader (analytics run only after the visitor accepts — assets/js/consent.js).
HEAD = """<!--#head:start-->
  <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests" />
  <link rel="icon" type="image/png" sizes="32x32" href="{B}assets/img/favicon-32.png" />
  <link rel="apple-touch-icon" href="{B}assets/img/apple-touch-icon.png" />
  <script src="{B}assets/js/consent.js" defer></script>
  <!--#head:end-->"""
HEAD_RE = re.compile(r'<!--#head:start-->.*?<!--#head:end-->', re.S)

NAV_RE = re.compile(r'<ul class="nav__links" id="navLinks">.*?\n        </ul>', re.S)

# The logo (2026-11-26): the stone and GEM INFORMATION SYSTEMS on one line, no
# GEMIS wordmark — assets/img/logos/gemis-logo-name.svg, drawn by
# tools/make-logo.py. Every page carries it as the #gemisLogo symbol, used by
# the bar and the footer; both the symbol and every <svg class="logo"> viewBox
# follow that file.
_LOGO = open(os.path.join(ROOT, 'assets/img/logos/gemis-logo-name.svg'), encoding='utf-8').read()
LOGO_VB = re.search(r'viewBox="([^"]+)"', _LOGO).group(1)
LOGO_SYMBOL = (f'<symbol id="gemisLogo" viewBox="{LOGO_VB}" fill="currentColor">'
               + re.search(r'<svg[^>]*>(.*)</svg>', _LOGO, re.S).group(1) + '</symbol>')
LOGO_SYMBOL_RE = re.compile(r'<symbol id="gemisLogo".*?</symbol>', re.S)
LOGO_VB_RE = re.compile(r'(<svg class="logo" viewBox=")[^"]*(")')
FOOTER_RE = re.compile(r'<footer class="(?:foot|ftr)">.*?</footer>', re.S)


def pages():
    """Every page that carries the corporate chrome, at any depth."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in {'.git', 'node_modules', 'studio', 'assets', 'scripts', 'tools', 'qa', '_project', 'brand'}]
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
    return template.replace('{ARROW}', ARROW).replace('{LOGO_VB}', LOGO_VB).replace('{B}', base)


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
        out = LOGO_SYMBOL_RE.sub(lambda m: LOGO_SYMBOL, out)
        out = LOGO_VB_RE.sub(lambda m: m.group(1) + LOGO_VB + m.group(2), out)
        # redirect stubs leave before anything loads; they need none of it
        if 'http-equiv="refresh"' not in out:
            if HEAD_RE.search(out):
                out = HEAD_RE.sub(lambda m: render(HEAD, base), out, count=1)
            elif '</head>' in out:
                out = out.replace('</head>', '  ' + render(HEAD, base) + '\n</head>', 1)
        rel = os.path.relpath(path, ROOT)
        if out != html:
            (stale if check else changed).append(rel)
            if not check:
                open(path, 'w', encoding='utf-8').write(out)
    if check:
        if stale:
            print('chrome out of date in:\n  ' + '\n  '.join(stale))
            return 1
        print('chrome: every page matches the canonical head block, header, logo and footer.')
        return 0
    print(f'chrome applied to {len(changed)} page(s):\n  ' + '\n  '.join(changed) if changed
          else 'chrome: nothing to change.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
