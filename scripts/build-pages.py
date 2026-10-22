#!/usr/bin/env python3
"""
Generate Our Work and the six story pages.

The page shell — head, header, footer, scripts — is lifted from index.html so
there is one source for the chrome. scripts/apply-chrome.py then keeps the nav
and footer of every generated page in step with the rest of the site.

    python3 scripts/build-pages.py
"""
import html
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

spec = importlib.util.spec_from_file_location('stories', os.path.join(HERE, 'stories.py'))
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

bs_spec = importlib.util.spec_from_file_location('build_stories', os.path.join(HERE, 'build-stories.py'))
B = importlib.util.module_from_spec(bs_spec)
bs_spec.loader.exec_module(B)

esc, tbc, ARROW = B.esc, B.tbc, B.ARROW
CANON = S.CANONICAL


def shell(base, title, description, canonical, extra_head=''):
    """head + header and footer + scripts, taken from the homepage."""
    src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    head_open, rest = src.split('<main>', 1)
    _, tail = rest.split('</main>', 1)

    # per-page metadata
    head_open = re.sub(r'<title>[^<]*</title>', f'<title>{esc(title)}</title>', head_open, count=1)
    for key in ('name="description"', 'property="og:title"', 'property="og:description"',
                'name="twitter:title"', 'name="twitter:description"'):
        value = title if 'title' in key else description
        head_open = re.sub(r'(<meta ' + re.escape(key) + r' content=")[^"]*(")',
                           lambda m: m.group(1) + esc(value) + m.group(2), head_open, count=1)
    head_open = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
                       lambda m: m.group(1) + canonical + m.group(2), head_open, count=1)
    head_open = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
                       lambda m: m.group(1) + canonical + m.group(2), head_open, count=1)

    # the homepage's Organization block belongs only to the homepage
    head_open = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', '', head_open, flags=re.S)
    if extra_head:
        head_open = head_open.replace('</head>', extra_head + '\n</head>', 1)

    # relative paths, since the site lives under /gemis-site/ and must never
    # use root-absolute ones
    def rebase(text):
        text = re.sub(r'(href|src)="(?!https?:|#|mailto:|tel:|data:|\.\./)([^"]+)"',
                      lambda m: f'{m.group(1)}="{base}{m.group(2)}"', text)
        return text

    return rebase(head_open) + '<main>\n', '</main>\n' + rebase(tail)


def video_schema(s, indent='  '):
    import json
    v = S.BASE_URL + s['video']
    data = {
        "@context": "https://schema.org", "@type": "VideoObject",
        "name": s['video_title'], "description": s['summary'],
        "duration": s['duration'], "inLanguage": "en", "uploadDate": "2026-10-21",
        "contentUrl": f"{v}_web.mp4", "thumbnailUrl": f"{v}_thumb.jpg",
        "transcript": s['transcript'], "keywords": s['keywords'],
        "publisher": {"@type": "Organization", "name": "GEM Information Systems (GEMIS)",
                      "url": CANON},
        "about": {"@type": s.get('about_type', 'Organization'), "name": s['about']},
    }
    return (f'{indent}<script type="application/ld+json">\n'
            f'{json.dumps(data, ensure_ascii=False, indent=2)}\n{indent}</script>')


# ── story page ───────────────────────────────────────────────────────────
def story_page(s):
    base = '../../'
    idx = S.STORY_PAGES.index(s)
    nxt = S.STORY_PAGES[(idx + 1) % len(S.STORY_PAGES)]
    founding = s['slug'] in S.FOUNDING

    since = B.since_html(s)
    endo = ''
    if founding and s['endorser']:
        # The card inside is hideable, and so is the section around it: until a
        # line is approved the live page skips the chapter entirely rather than
        # showing an empty band where it would go. ?review=1 brings both back.
        endo = f'''
    <section class="chap band band-wash unconfirmed" data-kind="hideable" aria-labelledby="endoHeading-{s['slug']}">
      <div class="shell">
        <h2 class="vh" id="endoHeading-{s['slug']}">What {esc(s['client'])} says</h2>
        {B.endorsement_html(s['endorser'], base, since)}
      </div>
    </section>'''

    caps = '\n'.join(f'            <li>{c}</li>' for c in s['capabilities'])

    outcome = f'<p>{esc(s["outcome"])}</p>'
    if s.get('metric'):
        # confirmed by the client in facts.md, so it publishes plainly
        outcome += f'\n          <p class="story__metric">{esc(s["metric"])}</p>'

    head = shell(
        base,
        f"{s['client']} — {s['headline']} | GEMIS®",
        s['summary'][:180],
        f"{CANON}work/{s['slug']}/",
        extra_head=video_schema(s),
    )

    body = f'''
    <!-- ═══════════ {s['client'].upper()} ═══════════ -->
    <section class="chero" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>{esc(s['industry'])}</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">{esc(s['client'])}</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">{esc(s['headline'])}</p>
        <dl class="story__meta" data-reveal style="--d:200ms">
          <div><dt>Period</dt><dd>{B.period_html(s)}</dd></div>
          {f'<div><dt>Relationship</dt><dd>{since}</dd></div>' if since else ''}
          <div><dt>Outcome</dt><dd>{esc(s['outcome'])}</dd></div>
        </dl>
      </div>
    </section>
{endo}
    <section class="chap band plusgrid plusgrid--tr" aria-labelledby="challengeHeading">
      <div class="shell">
        <p class="eyebrow" data-reveal>The challenge</p>
        <h2 class="display" id="challengeHeading" data-reveal style="--d:80ms">What the business needed</h2>
        <div class="story__prose" data-reveal style="--d:140ms">
          <p>{esc(s['challenge'])}.</p>
          <p>{esc(s['summary'])}</p>
        </div>
      </div>
    </section>

    <section class="chap band band-wash" aria-labelledby="builtHeading">
      <div class="shell">
        <p class="eyebrow" data-reveal>What we built</p>
        <h2 class="display" id="builtHeading" data-reveal style="--d:80ms">{esc(s['video_title'].split(':', 1)[-1].strip().capitalize())}</h2>
        <div class="story__build" data-reveal style="--d:140ms">
          {B.video_html(s, base)}
          <ul class="story__caps">
{caps}
          </ul>
        </div>
      </div>
    </section>

    <!-- "Then and now" is omitted deliberately: it needs an early and a current
         screenshot, neither of which has been supplied, and the prompt forbids a
         mock-up in their place. Tracked as then-now-screenshots in OPEN_ITEMS.md. -->

    <section class="chap band" aria-labelledby="outcomeHeading">
      <div class="shell">
        <p class="eyebrow" data-reveal>Outcome</p>
        <h2 class="display" id="outcomeHeading" data-reveal style="--d:80ms">Where it stands</h2>
        <div class="story__prose" data-reveal style="--d:140ms">
          {outcome}
        </div>
        <p class="story__tech" data-reveal style="--d:200ms">{esc(s['tech'])}</p>
      </div>
    </section>

    <section class="endnote" aria-labelledby="nextHeading">
      <div class="shell story__next">
        <div>
          <p class="eyebrow" data-reveal>Next story</p>
          <h2 class="display" id="nextHeading" data-reveal style="--d:80ms">{esc(nxt['client'])}</h2>
          <p data-reveal style="--d:140ms">{esc(nxt['headline'])}</p>
          <a class="arrow-link" href="{base}work/{nxt['slug']}/" data-reveal style="--d:200ms">Read the story {ARROW}</a>
        </div>
        <div>
          <p class="eyebrow" data-reveal>Start something</p>
          <h2 class="display" data-reveal style="--d:80ms">Tell us what your business needs to do better.</h2>
          <a class="arrow-link" href="{base}index.html#discovery" data-reveal style="--d:200ms">Book a Discovery Session {ARROW}</a>
        </div>
      </div>
    </section>
'''
    return head[0] + body + head[1]


# ── Our Work ─────────────────────────────────────────────────────────────
UNCLASSIFIED = [
    ('FINOS', 'entry-finos-status'), ('SmartStart', 'entry-smartstart-status'),
    ('RentFlow', 'entry-rentflow-status'), ('NuraCoach', 'entry-nuracoach-status'),
    ('Lungelo', 'entry-lungelo-status'),
]


def work_page():
    base = '../'
    import json
    items = {"@context": "https://schema.org", "@type": "ItemList",
             "name": "GEMIS case study videos", "itemListElement": []}
    for i, s in enumerate(S.STORIES, 1):
        v = S.BASE_URL + s['video']
        items["itemListElement"].append({
            "@type": "VideoObject", "position": i, "name": s['video_title'],
            "description": s['summary'], "duration": s['duration'], "inLanguage": "en",
            "uploadDate": "2026-10-21", "contentUrl": f"{v}_web.mp4",
            "thumbnailUrl": f"{v}_thumb.jpg", "transcript": s['transcript'],
            "keywords": s['keywords'],
            "publisher": {"@type": "Organization", "name": "GEM Information Systems (GEMIS)", "url": CANON},
            "about": {"@type": s.get('about_type', 'Organization'), "name": s['about']},
        })
    schema = ('  <script type="application/ld+json">\n'
              + json.dumps(items, ensure_ascii=False, indent=2) + '\n  </script>')

    head = shell(base, 'Our Work — systems in the real world | GEMIS®',
                 'Every project here is a system in production, and many have been running '
                 'for years. Case studies from GEMIS, a business systems partner since 2014.',
                 f'{CANON}work/', extra_head=schema)

    founders = B.srows([
        (f'<a href="{base}work/{s["slug"]}/">{esc(s["client"])}</a>',
         f'<p>{esc(s["headline"])}</p>', [B.since_html(s)],
         f'<a class="arrow-link arrow-link--quiet srow__go" href="{base}work/{s["slug"]}/">Read the story {ARROW}</a>')
        for s in [S.BY_SLUG[k] for k in S.FOUNDING]])

    grid = '\n'.join(B.feat(
        esc(s['client']), f"{base}work/{s['slug']}/", f"{base}{S.VIDEO_DIR}{s['video']}_thumb.jpg",
        B.period_html(s), esc(s['headline']), chips=[esc(s['industry'])] + [t.replace('-', ' ').capitalize() for t in s['capability_tags'][:2]],
        extra_attrs=f' data-reveal data-industry="{s["industry_tag"]}" data-capability="{" ".join(s["capability_tags"])}"',
    ).replace('<article class="post"', '<article class="post wk__card"') for s in S.STORY_PAGES)

    # Not confirmed as client systems, so they are not on the live build at all.
    # Listing them with a "to confirm" note would publish our uncertainty.
    unclassified = '\n'.join(
        B.hideable(tid, f'''<article class="wk__card wk__card--unclassified">
            <h3 class="wk__name">{name}</h3>
            <p class="wk__line">{tbc(tid, 'Client system or concept — to confirm')}</p>
          </article>''') for name, tid in UNCLASSIFIED)

    body = f'''
    <section class="chero" id="hero">
      <div class="shell">
        <p class="chero__kicker" data-reveal>Our Work</p>
        <h1 class="chero__title" data-reveal style="--d:80ms">Systems in the real world</h1>
        <p class="chero__copy" data-reveal style="--d:140ms">Every project here is a system in production, and many have been running for years.</p>
      </div>
    </section>

    <section class="wk band band-tint plusgrid plusgrid--tr" aria-labelledby="foundersHeading">
      <div class="shell">
        <div class="svcs__head">
          <div>
            <p class="eyebrow" data-reveal>Founding clients</p>
            <h2 class="display" id="foundersHeading" data-reveal style="--d:80ms">The relationships that started it</h2>
          </div>
        </div>
        <ol class="srows">
{founders}
        </ol>
      </div>
    </section>

{B.stories_section(base)}

    <section class="wk band" id="all" aria-labelledby="allHeading">
      <div class="shell">
        <div class="sec__head">
          <div>
            <p class="eyebrow" data-reveal>Every system</p>
            <h2 class="display" id="allHeading" data-reveal style="--d:80ms">Systems in production</h2>
          </div>
          <p class="lede" data-reveal style="--d:140ms">Filter by industry or by what the system had to do. Every project is listed whether you filter or not.</p>
        </div>
        <div class="wk__filters" data-filters hidden>
          <fieldset class="wk__fieldset"><legend class="eyebrow">Industry</legend>
            <button type="button" data-filter="industry" data-value="all" aria-pressed="true">All</button>
            <button type="button" data-filter="industry" data-value="construction" aria-pressed="false">Construction</button>
            <button type="button" data-filter="industry" data-value="insurance" aria-pressed="false">Insurance</button>
            <button type="button" data-filter="industry" data-value="waste" aria-pressed="false">Waste</button>
            <button type="button" data-filter="industry" data-value="mining" aria-pressed="false">Mining</button>
            <button type="button" data-filter="industry" data-value="non-profit" aria-pressed="false">Non-profit</button>
            <button type="button" data-filter="industry" data-value="education" aria-pressed="false">Education</button>
          </fieldset>
          <fieldset class="wk__fieldset"><legend class="eyebrow">Capability</legend>
            <button type="button" data-filter="capability" data-value="all" aria-pressed="true">All</button>
            <button type="button" data-filter="capability" data-value="field-operations" aria-pressed="false">Field operations</button>
            <button type="button" data-filter="capability" data-value="integration-reporting" aria-pressed="false">Integration and reporting</button>
            <button type="button" data-filter="capability" data-value="platforms" aria-pressed="false">Platforms</button>
          </fieldset>
        </div>
        <p class="vh" id="wkCount" aria-live="polite"></p>
        <div class="feats" data-grid>
{grid}
        </div>
        <div class="unconfirmed" data-kind="hideable">
        <h3 class="wk__sub" data-reveal>Still to classify</h3>
        <p class="wk__subnote" data-reveal>These five are in the repository but it is not yet confirmed whether each is a client system or a concept. They are listed rather than quietly dropped.</p>
        <div class="wk__grid wk__grid--quiet">
{unclassified}
        </div>
        </div>
        <p class="wk__more" data-reveal>Looking for a sector rather than a project? See <a href="{base}industries.html">Industries</a>.</p>
      </div>
    </section>

    <section class="endnote">
      <div class="shell">
        <h2 class="display" data-reveal>Tell us what your business needs to do better.</h2>
        <a class="arrow-link" href="{base}index.html#discovery" data-reveal style="--d:140ms">Book a Discovery Session {ARROW}</a>
      </div>
    </section>
'''
    html_out = head[0] + body + head[1]
    return html_out.replace('</body>',
        '  <script src="../assets/js/work-filters.js" defer></script>\n</body>')


def main():
    os.makedirs(os.path.join(ROOT, 'work'), exist_ok=True)
    open(os.path.join(ROOT, 'work', 'index.html'), 'w', encoding='utf-8').write(work_page())
    print('work/index.html')
    for s in S.STORY_PAGES:
        d = os.path.join(ROOT, 'work', s['slug'])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(story_page(s))
        print(f'work/{s["slug"]}/index.html')


if __name__ == '__main__':
    main()
