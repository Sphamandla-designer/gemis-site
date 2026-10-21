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
    cards = []
    for i, (name, role, where, quote, stars) in enumerate(SV.TESTIMONIALS):
        initials = ''.join(w[0] for w in name.split()[:2])
        cards.append(f'''          <li class="tcard" data-reveal style="--d:{i * 70}ms">
            <span class="tcard__mark" aria-hidden="true">&ldquo;</span>
            <p class="tcard__stars" role="img" aria-label="{stars} out of 5 stars">{STAR * stars}</p>
            <blockquote class="tcard__q"><p>{esc(quote)}</p></blockquote>
            <p class="tcard__by">
              <span class="tcard__face" aria-hidden="true">{initials}</span>
              <span><strong>{esc(name)}</strong><br />{esc(role)}, {esc(where)}</span>
            </p>
          </li>''')
    return '\n'.join(cards)


if __name__ == '__main__':
    index = os.path.join(ROOT, 'index.html')
    B.fill_slot(index, 'services', BS.services_rows('', 6))
    B.fill_slot(index, 'testimonials', testimonials_html())
    B.fill_slot(index, 'insights', BS.post_cards(''))
    print(f'index.html: services (6 of {len(SV.SERVICES)}), testimonials ({len(SV.TESTIMONIALS)}) '
          f'and insights ({len(SV.ARTICLES)}) written')
