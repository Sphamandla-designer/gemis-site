#!/usr/bin/env python3
"""
Fill the homepage's generated sections from scripts/services.py.

    python3 scripts/build-home.py

index.html is hand-written; three of its sections are lists that also appear
elsewhere (the services grid on the Solutions page, the articles on the
Insights page), so they are generated into sentinel slots the same way the
stories slider is. Run after build-stories.py.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SV = load('services', 'services.py')
B = load('build_stories', 'build-stories.py')
BS = load('build_services', 'build-services.py')
esc = B.esc

STAR = ('<svg viewBox="0 0 20 20" aria-hidden="true"><path d="m10 1.6 2.6 5.4 5.9.8-4.3 4.1 1.1 5.9L10 15l-5.3 2.8 1.1-5.9L1.5 7.8l5.9-.8Z"/></svg>')


def testimonials_html():
    """
    "Client stories", after the owner's reference (qa/design-refs/testimonials.png):
    the list of names on the left with the active one marked by an arrow and a
    pair of square arrow buttons beneath; on the right one quotation at a time,
    large, with the person beneath it. Tabbed by home.js; a plain list without it.
    """
    GO = ('<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">'
          '<path d="M1.5 6h9M7 2.5 10.5 6 7 9.5"/></svg>')
    tabs, slides = [], []
    for i, (name, role, where, quote, stars) in enumerate(SV.TESTIMONIALS):
        initials = ''.join(w[0] for w in name.split()[:2])
        pressed = 'true' if i == 0 else 'false'
        hidden = '' if i == 0 else ' aria-hidden="true"'
        tabs.append(f'''            <li><button class="cs__tab" type="button" data-tab data-go="{i}" aria-pressed="{pressed}"><span>{esc(name)}</span><span class="cs__tab-go" aria-hidden="true">{GO}</span></button></li>''')
        slides.append(f'''            <li class="cs__item" data-slide{hidden}>
              <blockquote class="cs__q"><p>{esc(quote)}</p></blockquote>
              <p class="cs__by">
                <span class="cs__face" aria-hidden="true">{initials}</span>
                <span class="cs__who"><strong>{esc(name)}</strong><span>{esc(role)} &middot; {esc(where)}</span></span>
                <span class="cs__stars" role="img" aria-label="{stars} out of 5 stars">{STAR * stars}</span>
              </p>
            </li>''')
    nl = chr(10)
    return f'''        <div class="cs" data-stage data-auto="0">
          <div class="cs__side">
            <ol class="cs__rail" aria-label="Choose a client story" data-reveal>
{nl.join(tabs)}
            </ol>
            <div class="cs__ctl" data-ctl hidden>
              <button class="cs__btn" type="button" data-prev aria-label="Previous client story"><svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M10.5 6h-9M5 2.5 1.5 6 5 9.5"/></svg></button>
              <button class="cs__btn" type="button" data-next aria-label="Next client story"><svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M1.5 6h9M7 2.5 10.5 6 7 9.5"/></svg></button>
            </div>
          </div>
          <div class="cs__main" data-reveal style="--d:80ms">
            <ol class="cs__list" data-list>
{nl.join(slides)}
            </ol>
            <a class="cs__more" href="#discovery">Become a client <span aria-hidden="true">&rarr;</span></a>
          </div>
        </div>'''


if __name__ == '__main__':
    index = os.path.join(ROOT, 'index.html')
    B.fill_slot(index, 'services', BS.services_rows('', 6))
    B.fill_slot(index, 'testimonials', testimonials_html())
    B.fill_slot(index, 'ways', B.tline(SV.WAYS))
    print(f'index.html: services (6 of {len(SV.SERVICES)}), testimonials ({len(SV.TESTIMONIALS)}) '
          f'and the {len(SV.WAYS)}-step timeline written')
