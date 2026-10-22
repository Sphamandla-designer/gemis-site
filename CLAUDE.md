# gemis-site

Two sites in one repository, served by GitHub Pages from `main` at
`https://sphamandla-designer.github.io/gemis-site/`:

- the **corporate site** — `index.html` and the other pages at the repository root
- **GEMIS Studio** — `/studio/`

## Shipping

**Every piece of work ends merged.** Do not stop at a pushed branch and wait to be
asked: commit, open the pull request, and merge it. Then confirm the Pages deploy
succeeded for the merge commit before reporting back.

```sh
gh run list --repo Sphamandla-designer/gemis-site --limit 1 \
  --json headSha,status,conclusion
```

A merged pull request cannot carry new work. If the branch's last PR is already
merged, restart the branch from the latest `main` under the same name; if it still
holds unmerged commits, rebase them onto `main` rather than discarding them.

`main` moves between sessions, sometimes mid-task. Fetch and rebase before opening
a PR, and re-run the checks on the rebased base — not just before the rebase.

## Generated files — never edit these directly

| Generated | Source | Rebuild with |
|---|---|---|
| `studio/index.html`, `studio/work.html`, `studio/about.html`, `studio/services.html`, `studio/contact.html`, `studio/assets/dc-template.js` | `studio/src/index.html`, `studio/src/work.html` | `node tools/build-studio.mjs` |
| `index.html` sections 03, 04, 06, 07 (between `<!--#services:start-->`, `<!--#stories:start-->`, `<!--#testimonials:start-->`, `<!--#insights:start-->` sentinels) | `scripts/services.py`, `scripts/stories.py` | `python3 scripts/build-stories.py && python3 scripts/build-home.py` |
| `solutions/`, `solutions/<service>/` ×9, `products/`, `insights/`, `insights/<article>/` ×3 | `scripts/services.py` | `python3 scripts/build-services.py` |
| `products/managem/`, `our-story/` | `scripts/stories.py`, old pages in git history | `python3 scripts/build-other.py` |
| `work/`, `work/<story>/` ×6 | `scripts/stories.py` | `python3 scripts/build-pages.py` |
| the header nav and footer columns on every page | `scripts/apply-chrome.py` (+ `services.py` for the two drop-downs) | `python3 scripts/apply-chrome.py` (`--check` in CI) |
| `gemis-site-standalone.html` | every chrome page at any depth, `site.css`, the scripts, the font, images and the MP4 videos | `python3 tools/build-site-standalone.py` — one 17 MB file; pages run in frames, videos reach them as blob URLs |

Full rebuild, in order: `build-stories` → `build-home` → `build-services` →
`build-pages` → `build-other` → `apply-chrome`.

Rebuild the standalone bundle after **any** change to a root page or to
`assets/css/site.css` or `assets/js/site.js`, or it silently goes stale.

Two traps in these builds:

- The studio build bakes a live SAST clock into every page it writes, so a rebuild
  always dirties five files with a one-line timestamp change. Restore that line in
  the files you did not otherwise touch, so the diff is only the real work.
- `build-site-standalone.py` takes its page list from `apply-chrome.pages()` and
  skips anything carrying a meta refresh, so redirect stubs never enter the
  bundle; a link to one is routed to the live site instead. It carries MP4 only
  (iOS needs it); the WebM sources are dropped at build time.

## Redirect stubs

`solutions.html`, `work.html`, `managem.html`, `brand-studio.html`, `services.html`,
`about.html`, `case-studies.html`, `wastemart.html`, `insights.html`,
`solutions/bespoke-software/` and `solutions/managem/` are redirect stubs, not pages —
they keep old bookmarks and search results working. They carry
`<meta name="robots" content="noindex">`, stay out of `sitemap.xml`, and stay out
of the standalone bundle's `PAGES`.

Auditing one in a sandbox reports `document-title` and `html-has-lang` falsely: the
meta-refresh fires before axe runs, so it measures the failed navigation. Re-run
against the file's own bytes with the refresh stripped.

## One design system — the tail of `site.css` decides

The stylesheet was written page by page and the layers contradict each other.
The last block, **TIDY — one system for the whole corporate site**, is where the
decisions now live; put a change to colour, type or spacing there, not in the
layer that first introduced the component.

- **Grounds are the hero photograph, never flat navy.** `assets/img/home/hero-bg.jpg`
  is the ground of every band that is not paper — `.chero`, `.endnote`, `.go`,
  `.built`, `.band-ink`, `.convert` — through the rules at the tail of `site.css`;
  only the gradient over it (`--scrim`) changes per band. It pans slowly and the
  gradient breathes (still under reduced motion); type on it is white. Pages that
  open on it get `nav--photo` (set by `build-pages.shell()`); the light-hero pages
  (`contact.html`, `privacy.html`) keep `nav--solid`. No hero carries image mockups.
- **Case study pages** are built from `scripts/cases.py` (hero with status and
  Play story, overview, business challenge, strategy and approach, outcomes split
  into delivered / verified / intended, related work, tailored enquiry). Only the
  client-confirmed metric is a number; a section with nothing verified is omitted.
- **Colour** comes from the hero photograph (`assets/img/home/hero-bg.jpg`):
  `--navy-deep #0b2642`, `--navy #16395e`, `--blue #2a5c8a`, `--wash #e6edf4`.
  No indigo, no warm grey — `band-warm` is retired and maps to `--paper-2`.
- **Type** is eight steps: `--fs-hero / display / lead / title / name / copy /
  small / eyebrow`. Every heading resolves to one; no literal px sizes.
- **Rhythm** is `--sec-y` on both edges of every section; the proof strip takes
  `--sec-y-s`. `.endnote` carries no top margin — that margin was the bare strip of
  page that used to show between sections.
- **Grounds** alternate paper → wash → paper → tint, one `band-ink` per long page,
  then the footer. Two washes never touch.
- **Page heroes** (`.chero`) are the home hero's photograph under the same scrim,
  type set left. A story page's endorsement chapter is itself `.unconfirmed`, so an
  unapproved line removes the whole band rather than leaving an empty one.

- **The reference kit** (from the owner's screenshots in `qa/design-refs/`) runs on
  every page: `.srows/.srow` numbered ruled rows for anything ordered (services,
  steps, founders, reasons), `.feats/.post` ruled features for anything with an
  image (articles, case studies, products), `.rlist` ruled link lists, `.plusgrid`
  (`--tr`, `--br`) corner accents, and `.endnote` as the photographic band. The
  helpers `srows()` and `feat()` in `scripts/build-stories.py` emit the markup.
- **Three more references** (`qa/design-refs/stories-panel.png`, `timeline.png`,
  `testimonials.png`) set: the stories panel (`stories_section()` — on the home
  and Case Studies, over the hero photograph, never black), the horizontal
  timeline (`tline(steps, label)` — How we work, the six stages, Contact's next
  steps, About's milestones) and "Client stories" (`testimonials_html()` in
  `build-home.py`). Any tabbed stage is a `[data-stage]` driven by
  `assets/js/home.js`; `data-auto="0"` turns off the auto-advance. Section
  headers (`.sec__head`) carry the ruled, plus-marked bottom edge the
  references share. The homepage no longer carries News & Insights; the
  `insights/` pages remain, linked from the footer.

Re-run the audit after a change: `node tools/audit-ui.mjs` prints the distinct
font sizes in use and the padding/ground of every section on every page.

## CSS is shared across pages — scope restyles

Several component classes are used by more than one page. Restyling one page's
instance without scoping silently changes the others:

- `.rows` / `.row` — `index.html` **and** `industries.html`
- `.chips` — `index.html`, `about.html`, `services.html`, `insights.html`
- `.strip` — six pages

The homepage service rows and the services accordion are scoped as `.rows--svc`
and `.acc` for exactly this reason. Before restyling a class, grep for which pages
carry it, then check the other pages match none of the new rules.

## Scroll reveal

`[data-reveal]` is `opacity: 0` until `site.js` adds `.is-in`; `--d` staggers it.
There is a `<noscript>` fallback that reveals everything. Anything that must be
readable without JavaScript has to work with the class never arriving — decorative
accents may stay undrawn, but content may not stay invisible.

The studio's sibling pages carry no React runtime, so `tools/build-studio.mjs`
injects the same observer as `SIBLING_JS`. A `data-reveal` added to a sibling page
without that is permanently invisible.

## Checks worth running before a PR

Chromium is at `/opt/node22/lib/node_modules/playwright`; `PLAYWRIGHT_BROWSERS_PATH`
is already set, so never run `playwright install`.

- axe across the changed pages, with reveals forced in and accordions forced open
- widths 360 / 620 / 900 / 1024 / 1440 / 1920: no horizontal overflow, no clipped
  text, no JS errors
- the internal link graph — `node tools/check-links.mjs` (every page at any depth), 0 broken
- JavaScript off, and reduced motion, on anything that animates

Every page is axe-clean at serious/critical. The `mailto:` link inside a paragraph
that used to fail `link-in-text-block` is underlined now (`main p > a:not([class])`),
so a prose link never depends on colour alone — keep it that way.

Measure contrast from rendered pixels when the mark is a stroke rather than a fill
— a `-webkit-text-stroke` numeral reads as a meaningless 1:1 from its `color`.

## Content

`CONTENT-TODO.md` lists what is provisional and what still needs a decision. The
open one that keeps mattering: the studio enquiry form at `/studio/#enquire` shows
a success state and **discards what the visitor typed**. Do not route new calls to
action into it until that is fixed.

Never invent a client, a testimonial, a statistic or a case study. Everything on
the site has to be traceable to something already in the repository.

**One standing exception, at the owner's instruction:** the homepage testimonials
(`TESTIMONIALS` in `scripts/services.py`) are invented placeholders — South
African names, no company named — until approved quotes arrive. OPEN_ITEMS.md
tracks them as `testimonials-placeholder`. Do not add more invented content on
the strength of that exception.

## Site map (navigation)

Home · Case Studies (`work/` — hero, stats, the ManaGEM featured project, the
filtered card grid with Read/Play, the approach timeline and a conversion band;
the video overlay is `#videoModal`, opened by any `[data-watch]`) · Solutions ▾ (`solutions/` + nine `solutions/<slug>/`
service pages) · Products ▾ (`products/`: ManaGEM at `products/managem/`, Design
Studio at `studio/`, Technical Academy at gemis.tech) · About (`our-story/`) ·
Contact. News & Insights lives at `insights/` (three articles), linked from the
homepage and footer. `solutions/bespoke-software/`, `solutions/managem/` and
`insights.html` are redirect stubs now.
