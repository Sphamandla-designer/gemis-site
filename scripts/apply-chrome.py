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
    'wastemart-driver.html', 'ManaGem.html', 'insights.html',
}
SKIP_PREFIX = ('GEMIS ',)
SKIP_CONTAINS = ('standalone',)

ARROW = ('<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" '
         'aria-hidden="true"><path d="M2.5 9.5 9.5 2.5M4 2.5h5.5V8"/></svg>')

NAV = '''<ul class="nav__links" id="navLinks">
        <li><a href="{B}index.html">Home</a></li>
        <li><a href="{B}work/">Our Work</a></li>
        <li class="nav__item nav__item--mega" data-mega>
          <button class="nav__trigger" id="productsTrigger" aria-expanded="false" aria-controls="productsMenu">
            Solutions
            <svg class="nav__chev" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 1.5 5 5 9 1.5"/></svg>
          </button>

        <div class="mega" id="productsMenu" aria-labelledby="productsTrigger">
          <div class="shell mega__in">
            <div class="mega__head">
              <p class="eyebrow">Our Solutions</p>
              <p class="mega__lede">Four ways to work with GEMIS — a system built around your operation, a platform ready to run on, a studio to design it, and training to keep your team ahead.</p>
              <a class="arrow-link" href="{B}solutions/">All solutions {ARROW}</a>
            </div>

            <div class="mega__grid mega__grid--4">
              <article class="prod">
                <a class="prod__media" href="{B}solutions/bespoke-software/" tabindex="-1" aria-hidden="true">
                  <img src="{B}assets/img/portfolio/hero-wastemart.jpg" alt="" loading="lazy" width="760" height="475" />
                </a>
                <div class="prod__body">
                  <h3 class="prod__name">Bespoke Software</h3>
                  <p class="prod__desc">A system designed and built around your operation, then supported for the long term.</p>
                  <a class="prod__cta" href="{B}solutions/bespoke-software/">Discuss your project {ARROW}</a>
                </div>
              </article>

              <article class="prod">
                <a class="prod__media" href="{B}solutions/managem/" tabindex="-1" aria-hidden="true">
                  <img src="{B}assets/img/menu/managem.jpg" alt="" loading="lazy" width="760" height="475" />
                </a>
                <div class="prod__body">
                  <h3 class="prod__name">ManaGEM</h3>
                  <p class="prod__desc">A proven business management platform, ready to run on — sales, stock, payroll, projects and accounting in one place.</p>
                  <a class="prod__cta" href="{B}solutions/managem/">Explore ManaGEM {ARROW}</a>
                </div>
              </article>

              <article class="prod">
                <a class="prod__media" href="{B}studio/" tabindex="-1" aria-hidden="true">
                  <img src="{B}assets/img/menu/design-studio.jpg" alt="" loading="lazy" width="760" height="475" />
                </a>
                <div class="prod__body">
                  <h3 class="prod__name">GEMIS Studio</h3>
                  <p class="prod__desc">Product and interface design from the team that can also build it.</p>
                  <a class="prod__cta" href="{B}studio/">See the Studio {ARROW}</a>
                </div>
              </article>

              <article class="prod">
                <a class="prod__media" href="https://gemis.tech/" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">
                  <img src="{B}assets/img/menu/gemis-tech.jpg" alt="" loading="lazy" width="760" height="475" />
                </a>
                <div class="prod__body">
                  <h3 class="prod__name">Technical Academy</h3>
                  <p class="prod__desc">Practical AI and technical training for professionals and teams.</p>
                  <a class="prod__cta" href="https://gemis.tech/" target="_blank" rel="noopener">Visit gemis.tech {ARROW}</a>
                </div>
              </article>
            </div>
          </div>
        </div>
        </li>
        <li><a href="{B}our-story/">Our Story</a></li>
        <li><a href="{B}contact.html">Contact</a></li>
        </ul>'''

FOOTER_COLS = '''<div class="foot__col">
          <h2>Solutions</h2>
          <ul>
            <li><a href="{B}solutions/bespoke-software/">Bespoke Software</a></li>
            <li><a href="{B}solutions/managem/">ManaGEM</a></li>
            <li><a href="{B}studio/">GEMIS Studio</a></li>
            <li><a href="https://gemis.tech/" target="_blank" rel="noopener">Technical Academy</a></li>
          </ul>
        </div>

        <div class="foot__col">
          <h2>About GEMIS</h2>
          <ul>
            <li><a href="{B}our-story/">Our Story</a></li>
            <li><a href="{B}work/">Our Work</a></li>
            <li><a href="{B}industries.html">Industries</a></li>
          </ul>
        </div>

        <div class="foot__col">
          <h2>Support &amp; Resources</h2>
          <ul>
            <li><a href="{B}contact.html">Contact Us</a></li>
            <li><a href="{B}solutions/bespoke-software/#process">Ongoing Support</a></li>
            <li><a href="{B}privacy.html">Privacy Policy</a></li>
          </ul>
        </div>'''

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
