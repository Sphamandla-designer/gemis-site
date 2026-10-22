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
    if s['period'] and s['period'].startswith('Client '):
        # no year at all: the period line already says what is confirmed
        return esc(s['period'])
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


# ── the stories panel ────────────────────────────────────────────────────
def stories_html(base=''):
    """
    "Built together. Still working." reproduced from the owner's reference
    (qa/design-refs/stories-panel.png): a ruled top edge marked by two plus
    signs, a left column (blue glow at its head, the headline, a paragraph,
    one bordered button, then the list with the active row marked by a bar
    and an arrow) divided by a vertical rule from the right column (a
    bordered panel on a faint grid — the video, in place of the illustration
    — then a bold line and grey copy). The ground is the hero photograph.

    The markup is a plain <ol> of stories that reads top to bottom with no
    JavaScript; assets/js/home.js turns it into the tabbed stage.
    """
    GO = ('<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">'
          '<path d="M1.5 6h9M7 2.5 10.5 6 7 9.5"/></svg>')
    tabs, slides = [], []
    for i, s in enumerate(S.STORIES):
        product = s.get('is_product')
        href = f'{base}products/managem/' if product else f'{base}work/{s["slug"]}/'
        cta = 'Explore ManaGEM' if product else 'Read the story'
        v = f'{base}{S.VIDEO_DIR}{s["video"]}'
        pressed = 'true' if i == 0 else 'false'
        hidden = '' if i == 0 else ' aria-hidden="true"'
        founding = s['slug'] in S.FOUNDING
        tag = ''
        if founding:
            since = f'since {s["since"]}' if s.get('since') else 'more than ten years'
            tag = f'\n              <span class="stories__tab-p">Founding client &middot; {since}</span>'
        cls = 'stories__tab stories__tab--founding' if founding else 'stories__tab'
        tabs.append(f'''            <li><button class="{cls}" type="button" data-tab data-go="{i}" aria-pressed="{pressed}">
              <span class="stories__tab-name">{esc(s['client'])}</span>{tag}
              <span class="stories__tab-go" aria-hidden="true">{GO}</span>
            </button></li>''')
        slides.append(f'''            <li class="sty" id="sty-{s['slug']}" data-slide{hidden}>
              <div class="sty__panel">
                <video class="sty__video" controls preload="none" playsinline width="1280" height="720" poster="{v}_thumb.jpg" aria-label="{esc(s['video_title'])}">
                  <source src="{v}_web.webm" type="video/webm">
                  <source src="{v}_web.mp4" type="video/mp4">
                  <a href="{v}_web.mp4">Download the video</a>
                </video>
              </div>
              <p class="sty__title">{esc(s['client'])}: {esc(s['headline'][0].lower() + s['headline'][1:])}.</p>
              <p class="sty__copy">{esc(s['challenge'])}. {esc(s['outcome'])}. <a class="sty__link" href="{href}">{cta} &rarr;</a></p>
            </li>''')
    n = len(S.STORIES)
    tabs.append(f'''            <li><button class="stories__tab" type="button" data-tab data-go="{n}" aria-pressed="false">
              <span class="stories__tab-name">Today</span>
              <span class="stories__tab-go" aria-hidden="true">{GO}</span>
            </button></li>''')
    slides.append(f'''            <li class="sty sty--today" id="sty-today" data-slide aria-hidden="true">
              <div class="sty__panel sty__panel--today"><p class="sty__big">Still building together.</p></div>
              <p class="sty__title">Today: the founding relationships continue.</p>
              <p class="sty__copy">All three founding clients still run on the systems we built them, and those systems have kept growing with the businesses. <a class="sty__link" href="{base}contact.html">Discuss a project &rarr;</a></p>
            </li>''')
    nl = chr(10)
    return f'''        <div class="stories__frame" data-stage>
          <div class="stories__intro">
            <span class="stories__glow" aria-hidden="true"></span>
            <h2 class="stories__title" id="storiesHeading" data-reveal>Built together.<br />Still working.</h2>
            <p class="stories__lede" data-reveal style="--d:80ms">More than a decade of real systems: the problems our clients brought us, what we built, and how those systems have grown since.</p>
            <a class="stories__cta" href="{base}work/" data-reveal style="--d:140ms"><span>See all case studies</span><span class="stories__cta-go" aria-hidden="true">{GO}</span></a>
            <ol class="stories__rail" aria-label="Choose a story" data-reveal style="--d:200ms">
{nl.join(tabs)}
            </ol>
          </div>
          <div class="stories__stage" data-reveal style="--d:140ms">
            <ol class="stories__list" data-list>
{nl.join(slides)}
            </ol>
            <div class="stories__ctl" data-ctl hidden>
              <button class="stories__btn" type="button" data-prev aria-label="Previous story"><svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M6 10V2M2.5 5.5 6 2l3.5 3.5"/></svg></button>
              <button class="stories__btn" type="button" data-pause aria-pressed="false" aria-label="Pause"><svg viewBox="0 0 12 12" fill="currentColor" aria-hidden="true"><rect x="2.5" y="2" width="2.4" height="8" rx=".6"/><rect x="7.1" y="2" width="2.4" height="8" rx=".6"/></svg></button>
              <button class="stories__btn" type="button" data-next aria-label="Next story"><svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M6 2v8M2.5 6.5 6 10l3.5-3.5"/></svg></button>
              <span class="stories__count" aria-live="polite"><b data-cur>1</b> / {n + 1}</span>
              <span class="stories__bar" data-bar aria-hidden="true"><i></i></span>
            </div>
          </div>
        </div>'''


def stories_section(base=''):
    """The whole "Built together" section, for any page that carries it."""
    return f'''    <section class="built" id="our-story" aria-labelledby="storiesHeading">
      <img class="built__bg" src="{base}assets/img/home/hero-bg.jpg" alt="" aria-hidden="true" loading="lazy" />
      <div class="shell">
{stories_html(base)}
      </div>
    </section>'''


# ── the horizontal timeline ──────────────────────────────────────────────
def tline(steps, label='Step'):
    """
    A horizontal timeline after the owner's infographic reference
    (qa/design-refs/timeline.png): a numbered disc for each step on one
    connecting line, and beneath each a tinted plate with a chevron, an
    uppercase title and copy, the plates stepping through the site's blues.
    steps: (title, copy). Animated by assets/js/home.js (.is-drawn); static
    under reduced motion and with JavaScript off.
    """
    items = []
    for i, (t, c) in enumerate(steps):
        items.append(f'''          <li class="tline__step" style="--i:{i}">
            <span class="tline__disc" aria-hidden="true"><b>{i + 1:02d}</b><i>{esc(label)}</i></span>
            <div class="tline__plate">
              <span class="tline__chev" aria-hidden="true"><svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 2.5 7.5 6 4 9.5"/></svg></span>
              <h3 class="tline__t">{esc(t)}</h3>
              <p class="tline__c">{esc(c)}</p>
            </div>
          </li>''')
    nl = chr(10)
    return f'''        <ol class="tline tline--{len(steps)}" style="--n:{len(steps)}">
          <span class="tline__runner" aria-hidden="true"></span>
{nl.join(items)}
        </ol>'''


PLAY = ('<svg viewBox="0 0 12 12" fill="currentColor" aria-hidden="true"><path d="M3 1.8v8.4L10 6 3 1.8Z"/></svg>')


def play_attrs(s, base):
    """The data attributes home.js reads to open a story's video in the overlay."""
    v = f'{base}{S.VIDEO_DIR}{s["video"]}'
    return (f'href="{v}_web.mp4" data-watch data-mp4="{v}_web.mp4" data-webm="{v}_web.webm" '
            f'data-poster="{v}_thumb.jpg" data-title="{esc(s["video_title"])}"')


def video_modal():
    return '''        <dialog class="vmodal" id="videoModal" aria-label="Case study video">
          <button class="vmodal__close" type="button" data-close aria-label="Close video"><svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2.5 2.5l7 7M9.5 2.5l-7 7"/></svg></button>
          <video class="vmodal__video" controls playsinline preload="none" width="1280" height="720"></video>
          <p class="vmodal__title" data-vtitle></p>
        </dialog>'''


# ── the design-reference kit, shared by every generated page ─────────────
def srows(items, numbered=True):
    """
    Numbered ruled rows — the "What we do" pattern from the design references.
    items: (name, body_html, chips, link_html). body_html is already escaped.
    """
    out = []
    for i, (name, body, chips, link) in enumerate(items):
        chip_html = ''
        if chips:
            chip_html = ('\n              <ul class="srow__chips">\n'
                         + '\n'.join(f'                <li>{esc(c)}</li>' for c in chips)
                         + '\n              </ul>')
        n = f'<span class="srow__n" aria-hidden="true">{i + 1:02d}</span>' if numbered else ''
        out.append(f'''          <li class="srow" data-reveal style="--d:{i * 60}ms">
            {n}
            <h3 class="srow__name">{name}</h3>
            <div class="srow__body">
              {body}{chip_html}{('' if not link else chr(10) + '              ' + link)}
            </div>
          </li>''')
    return '\n'.join(out)


def feat(title, href, img, meta, body, chips=(), extra_attrs='', link=''):
    """A ruled feature: title row with a plus, image, meta, copy, chips."""
    chip_html = ''
    if chips:
        chip_html = ('\n            <ul class="post__chips">\n'
                     + '\n'.join(f'              <li>{esc(c)}</li>' for c in chips)
                     + '\n            </ul>')
    return f'''          <article class="post"{extra_attrs}>
            <h3 class="post__t"><a href="{href}"><span class="post__plus" aria-hidden="true">+</span><span>{title}</span></a></h3>
            <a class="post__media" href="{href}" tabindex="-1" aria-hidden="true">
              <img src="{img}" alt="" loading="lazy" width="1280" height="720" />
            </a>
            <p class="post__meta">{meta}</p>
            <p class="post__x">{body}</p>{chip_html}{('' if not link else chr(10) + '            ' + link)}
          </article>'''


# ── the redesign kit: diagram, walkthrough, decisions, case card ─────────
def flow(steps, label=''):
    """
    A workflow drawn from verified information — the case study narration —
    as a chain of labelled steps. steps: (title, note). It is a plain <ol>,
    so it reads top to bottom without CSS and with no JavaScript.
    """
    items = '\n'.join(f'''          <li class="flow__step">
            <span class="flow__n" aria-hidden="true">{i + 1:02d}</span>
            <span class="flow__t">{esc(t)}</span>
            <span class="flow__c">{esc(c)}</span>
          </li>''' for i, (t, c) in enumerate(steps))
    aria = f' aria-label="{esc(label)}"' if label else ''
    return f'''        <ol class="flow"{aria} style="--n:{len(steps)}">
{items}
        </ol>'''


def walk(items, base, slug):
    """
    The walkthrough: stills from the case study video, each with what the user
    is doing and how the system supports it. items: (file, title, caption).
    The caption says where the picture comes from, so an illustration is never
    taken for a production screenshot.
    """
    rows = []
    for i, (img, title, caption) in enumerate(items):
        rows.append(f'''          <li class="walk__row" data-reveal style="--d:{(i % 2) * 60}ms">
            <figure class="walk__fig">
              <img src="{base}assets/img/cases/{slug}/{img}" alt="{esc(title)} — illustrated in the {esc(S.BY_SLUG[slug]['client'])} case study video" loading="lazy" width="1200" height="675" />
              <figcaption class="walk__src">Illustrated in the case study video</figcaption>
            </figure>
            <div class="walk__text">
              <span class="walk__n" aria-hidden="true">{i + 1:02d}</span>
              <h3 class="walk__t">{esc(title)}</h3>
              <p class="walk__c">{esc(caption)}</p>
            </div>
          </li>''')
    nl = chr(10)
    return f'''        <ol class="walk">
{nl.join(rows)}
        </ol>'''


def decisions(items):
    """Key decisions: challenge, decision, rationale, evidence or effect."""
    cards = []
    for i, (ch, de, ra, ev) in enumerate(items):
        cards.append(f'''          <li class="dec" data-reveal style="--d:{i * 60}ms">
            <dl class="dec__l">
              <div><dt>Challenge</dt><dd>{esc(ch)}</dd></div>
              <div><dt>Decision</dt><dd>{esc(de)}</dd></div>
              <div><dt>Rationale</dt><dd>{esc(ra)}</dd></div>
              <div><dt>Evidence or effect</dt><dd>{esc(ev)}</dd></div>
            </dl>
          </li>''')
    nl = chr(10)
    return f'''        <ol class="decs">
{nl.join(cards)}
        </ol>'''


def cap_label(tag):
    return {'field-operations': 'Field operations', 'integration-reporting': 'Integration and reporting',
            'integration': 'Integration', 'platforms': 'Platforms', 'reporting': 'Reporting',
            'workflow': 'Workflow', 'mobile': 'Mobile', 'product': 'Product'}.get(tag, tag.replace('-', ' ').capitalize())


_CASES = None


def cases():
    global _CASES
    if _CASES is None:
        import importlib.util
        c_spec = importlib.util.spec_from_file_location('cases', os.path.join(HERE, 'cases.py'))
        _CASES = importlib.util.module_from_spec(c_spec)
        c_spec.loader.exec_module(_CASES)
    return _CASES.CASES


def cscard(s, base, i=0, wide=False, extra_attrs=''):
    """
    A case study card: industry, name, challenge-led headline, GEMIS's role,
    status, capability labels, and Read / Play. Used by the index, the related
    rows and the homepage's selected projects.
    """
    c = cases().get(s['slug'], {})
    product = s.get('is_product')
    href = f'{base}products/managem/' if product else f'{base}work/{s["slug"]}/'
    role = c.get('role_short', 'Designed, built and supported by GEMIS')
    status = c.get('status_short', c.get('status', ''))
    chips = ''.join(f'<li>{esc(cap_label(t))}</li>' for t in s.get('capability_tags', [])[:3])
    cls = 'cscard cscard--wide' if wide else 'cscard'
    return f'''          <article class="{cls}"{extra_attrs} data-reveal style="--d:{i * 60}ms">
            <a class="cscard__media" href="{href}" tabindex="-1" aria-hidden="true">
              <img src="{base}{S.VIDEO_DIR}{s['video']}_thumb.jpg" alt="" loading="lazy" width="1280" height="720" />
              <span class="cscard__len">{s['duration_label']}</span>
            </a>
            <div class="cscard__body">
              <p class="cscard__tag">{esc(s['industry'])}</p>
              <h3 class="cscard__name">{esc(s['client'])}</h3>
              <p class="cscard__line">{esc(s['headline'])}</p>
              <dl class="cscard__meta">
                <div><dt>GEMIS&rsquo;s role</dt><dd>{esc(role)}</dd></div>
                <div><dt>Status</dt><dd>{esc(status)}</dd></div>
              </dl>
              <ul class="cscard__chips" aria-label="Capabilities">{chips}</ul>
              <div class="cscard__actions">
                <a class="btn btn--sm" href="{href}">{'Explore ManaGEM' if product else 'Read the case study'} {ARROW}</a>
                <a class="btn btn--sm btn--ghost" {play_attrs(s, base)}>{PLAY} Play story</a>
              </div>
            </div>
          </article>'''


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
    # the homepage is generated whole by build-home.py now, stories panel
    # included; this script is the library the other builds import
    print(f'stories: {len(S.STORIES)} stories, {len(S.STORY_PAGES)} case study pages (markup helpers loaded)')


if __name__ == '__main__':
    main()
