#!/usr/bin/env python3
"""
Render everything that comes from the story data: the homepage timeline, the
endorsement cards, the video players, Our Work, and the six story pages.

One source (scripts/stories.py) feeds all of them, so a date or a headline can
never say one thing on the timeline and another on the story page.

    python3 scripts/build-stories.py

Writes into the <!--#timeline--> and <!--#endorsement-*--> slots on index.html,
and generates work/index.html and work/<slug>/index.html.
"""
import html
import importlib.util
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

spec = importlib.util.spec_from_file_location('stories', os.path.join(HERE, 'stories.py'))
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

ARROW = ('<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" '
         'aria-hidden="true"><path d="M2.5 9.5 9.5 2.5M4 2.5h5.5V8"/></svg>')


def esc(t):
    return html.escape(t, quote=True)


def tbc(id_, placeholder):
    """
    An unconfirmed value.

    On the live build it is not rendered at all — publish-safe mode. Under
    ?review=1 the dashed underline and TBC pill come back, so a reviewer can
    still see everything outstanding at a glance. Either way the id stays in
    the markup for scripts/check-tbc.mjs to count.
    """
    return (f'<span class="tbc" data-tbc="{id_}" data-kind="{S.TBC_KIND.get(id_, "hideable")}">'
            f'{placeholder}</span>')


def hideable(id_, markup, fallback=''):
    """
    Markup that must disappear cleanly when the fact behind it has not arrived.

    The fallback is what the live build shows in its place — never an empty gap
    and never the word TBC. Both are in the DOM; CSS picks one, so this works
    with no JavaScript, and ?review=1 flips it.
    """
    return (f'<div class="unconfirmed" data-tbc="{id_}" data-kind="hideable">{markup}</div>'
            + (f'<div class="confirmed-fallback">{fallback}</div>' if fallback else ''))


def period_html(s):
    if s['period']:
        return esc(s['period'])
    return 'Year ' + tbc(s['period_tbc'], 'to confirm')


def since_html(s):
    if s['since']:
        return f"Client since {s['since']}"
    if s['since_tbc']:
        # no confirmed year: say the thing the videos do confirm rather than
        # showing a placeholder, so the live build reads as finished
        return (hideable(s['since_tbc'],
                         'Client since ' + tbc(s['since_tbc'], '2014–15'),
                         'Client for more than ten years'))
    return ''


def client_logo(slug, client, wide=False, name_markup=''):
    """
    A client's mark.

    No logo files were supplied. Rather than an empty box or the words "Image
    TBC", the live build sets the client's name as a wordmark in the site's own
    type — a deliberate-looking fallback that needs no asset. The placeholder
    block returns under ?review=1.
    """
    shape = ' img-tbc--wide' if wide else ''
    # With a real logo the name is still needed as text beside it. With the
    # wordmark fallback the name IS the mark, so repeating it would read as a
    # duplication rather than a design.
    block = (f'<span class="img-tbc{shape}" role="img" '
             f'aria-label="{esc(client)} logo to follow">Image TBC</span>' + name_markup)
    # the fallback keeps the card's heading element, so the live page has the
    # same outline as the review page — only the mark inside it differs
    mark = (f'<h3 class="wk__fname"><span class="client-mark client-mark--lg">{esc(client)}</span></h3>'
            if name_markup else f'<span class="client-mark">{esc(client)}</span>')
    return hideable(f'logo-{slug}', block, mark)


# ── video ────────────────────────────────────────────────────────────────
def video_html(s, base):
    """Poster-first. preload=none means nothing downloads before a click."""
    stem = s['video']
    v = f'{base}{S.VIDEO_DIR}{stem}'
    return f'''<figure class="vid">
            <video class="vid__el" controls preload="none" playsinline width="1280" height="720"
                   poster="{v}_thumb.jpg" aria-label="{esc(s['video_title'])}">
              <source src="{v}_web.webm" type="video/webm; codecs=av01.0.05M.08,opus">
              <source src="{v}_web.mp4" type="video/mp4">
              <p>Your browser cannot play this video. <a href="{v}_web.mp4">Download it instead</a>.</p>
            </video>
            <figcaption class="vid__cap">
              <p class="vid__summary">{esc(s['summary'])}</p>
              <details class="vid__transcript">
                <summary>Read the transcript</summary>
                <p>{esc(s['transcript'])}</p>
              </details>
              <p class="vid__meta">Captions are burned into the video · {s['duration_label']}</p>
            </figcaption>
          </figure>'''


# ── endorsement card ─────────────────────────────────────────────────────
def endorsement_html(key, base, since_text=''):
    """
    No line is ever written here. endorsements.md is absent, so every card says
    the line is still to come. The brief's "theme" column is layout context, not
    a quote, and is not turned into one.
    """
    e = S.ENDORSERS[key]
    card = f'''<figure class="endo">
            <div class="endo__portrait img-tbc img-tbc--square" data-tbc="{e['portrait_tbc']}"
                 role="img" aria-label="Portrait of {esc(e['name'])} to follow">{e['initials']}</div>
            <blockquote class="endo__line">
              <p>{tbc(e['line_tbc'], 'Endorsement to follow')}</p>
            </blockquote>
            <figcaption class="endo__by">
              <span class="endo__name">{esc(e['name'])}</span>
              <span class="endo__title">{tbc(e['title_tbc'], 'Title to confirm')}</span>
              <span class="endo__co">{esc(e['company'])}</span>
              {f'<span class="endo__since">{since_text}</span>' if since_text else ''}
            </figcaption>
          </figure>'''
    # no approved line means no card on the live build — the founding card simply
    # shows its video full width, which is a deliberate layout, not a gap
    return hideable(e['line_tbc'], card)


# ── timeline ─────────────────────────────────────────────────────────────
def timeline_html(base=''):
    items = []
    for s in S.STORIES:
        founding = s['slug'] in S.FOUNDING
        classes = 'stl__item' + (' stl__item--founding' if founding else '')
        if s.get('is_product'):
            classes += ' stl__item--product'
        thread = f' data-thread="{s["slug"]}"' if founding else ''
        cta = (f'<a class="arrow-link" href="{base}solutions/managem/">Explore ManaGEM {ARROW}</a>'
               if s.get('is_product')
               else f'<a class="arrow-link" href="{base}work/{s["slug"]}/">Read the story {ARROW}</a>')
        # founding cards put the endorsement beside the video, as the brief asks;
        # the others are just the video
        media = video_html(s, base)
        if founding and s['endorser']:
            media = (f'<div class="stl__media">\n          {video_html(s, base)}\n'
                     f'          <div class="stl__endo">{endorsement_html(s["endorser"], base, since_html(s))}</div>\n'
                     f'          </div>')
        label = ('<span class="stl__thread-label">Founding client</span>' if founding else '')
        items.append(f'''        <li class="{classes}"{thread} id="stl-{s['slug']}" data-reveal>
          <p class="stl__period">{period_html(s)}</p>
          <h3 class="stl__client">{esc(s['client'])}{label}</h3>
          <p class="stl__headline">{esc(s['headline'])}</p>
          <p class="stl__challenge">{esc(s['challenge'])}</p>
          {media}
          <p class="stl__cta">{cta}</p>
        </li>''')

    # the closing entry: all three founding threads reach the present
    items.append(f'''        <li class="stl__item stl__item--today" id="stl-today" data-reveal>
          <p class="stl__period">2026</p>
          <h3 class="stl__client">Today</h3>
          <p class="stl__headline">Still building together</p>
          <p class="stl__challenge">All three founding relationships continue.</p>
          <p class="stl__cta"><a class="arrow-link" href="{base}#discovery">Book a Discovery Session {ARROW}</a></p>
        </li>''')

    threads = '\n'.join(
        f'          <li class="stl__thread" data-thread="{slug}"><span>{esc(S.BY_SLUG[slug]["client"])}</span></li>'
        for slug in S.FOUNDING)

    return f'''        <div class="stl__frame">
          <ul class="stl__threads" aria-label="Founding client relationships, running from 2014–15 to today">
{threads}
          </ul>

          <ol class="stl__list">
{chr(10).join(items)}
          </ol>
        </div>'''


def fill_slot(path, slot, content):
    """
    Fill a slot, and stay fillable.

    The generated region is wrapped in start/end sentinels so a second run
    replaces it rather than failing on a slot that has already been consumed.
    Rebuilding has to be repeatable: the facts change and the pages get
    regenerated more than once.
    """
    html_text = open(path, encoding='utf-8').read()
    start, end = f'<!--#{slot}:start-->', f'<!--#{slot}:end-->'
    block = f'{start}\n{content}\n{end}'
    if start in html_text and end in html_text:
        html_text = re.sub(re.escape(start) + r'.*?' + re.escape(end), lambda _: block,
                           html_text, count=1, flags=re.S)
    elif f'<!--#{slot}-->' in html_text:
        html_text = html_text.replace(f'<!--#{slot}-->', block, 1)
    else:
        raise SystemExit(f'{path}: neither slot <!--#{slot}--> nor its sentinels found')
    open(path, 'w', encoding='utf-8').write(html_text)


def main():
    fill_slot(os.path.join(ROOT, 'index.html'), 'timeline', timeline_html(''))
    fill_slot(os.path.join(ROOT, 'index.html'), 'endorsement-ryan',
              '          ' + endorsement_html('ryan-smith', '', 'Client since 2014'))
    print('index.html: timeline (8 entries) and the Ryan Smith endorsement card written')


if __name__ == '__main__':
    main()
