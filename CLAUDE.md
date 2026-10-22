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
| the whole `<main>` of `index.html` (between the `<!--#home:start-->` / `<!--#home:end-->` sentinels) | `scripts/build-home.py` (the nine sections, in the brief's order) from `stories.py`, `cases.py`, `services.py` | `python3 scripts/build-home.py` |
| `solutions/`, `solutions/<service>/` ×9, `products/`, `insights/`, `insights/<article>/` ×3 | `scripts/services.py` | `python3 scripts/build-services.py` |
| `products/managem/`, `our-story/` | `scripts/stories.py`, old pages in git history | `python3 scripts/build-other.py` |
| `work/`, `work/<story>/` ×6 | `scripts/stories.py`, `scripts/cases.py` (record + `DETAIL`: basis, flow, walkthrough, decisions, validation) | `python3 scripts/build-pages.py` |
| the header nav and footer columns on every page | `scripts/apply-chrome.py` (+ `services.py` for the two drop-downs) | `python3 scripts/apply-chrome.py` (`--check` in CI) |
| `gemis-site-standalone.html` | every chrome page at any depth, `site.css`, the scripts, the font, images (the walkthrough stills included) and the MP4 videos | `python3 tools/build-site-standalone.py` — one 19 MB file; pages run in frames, videos reach them as blob URLs |
| `assets/img/cases/<slug>/*.jpg` (37 stills) | frames of the case study videos, picked by scene | the ffmpeg commands in `docs/REDESIGN-REPORT.md` |

Full rebuild, in order: `build-home` → `build-services` → `build-pages` →
`build-other` → `apply-chrome`. (`build-stories.py` is the shared markup library
the others import; running it alone only prints a summary.)

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
  `testimonials.png`) set: the stories panel (`stories_section()` — on the home's
  partnership section, over the hero photograph, never black) and the horizontal
  timeline (`tline(steps, label)` — How we work, the six stages, Contact's next
  steps, About's milestones). The "Client stories" testimonial stage
  (`testimonials_html()`) is no longer rendered anywhere: the invented
  placeholders were removed by the case-study-led redesign. Any tabbed stage is a
  `[data-stage]` driven by `assets/js/home.js`; `data-auto="0"` turns off the
  auto-advance. Section headers (`.sec__head`) carry the ruled, plus-marked
  bottom edge the references share. The three founding clients on the stories
  panel carry a "Founding client · since <year>" tag (`stories__tab--founding`).

- **The evidence kit** (case-study-led redesign, `docs/REDESIGN-AUDIT.md` and
  `docs/REDESIGN-REPORT.md`): `flow(steps, label)` draws a workflow as a chain of
  steps; `walk(items, base, slug)` lays out video stills with captions that say
  "Illustrated in the case study video"; `decisions(items)` renders
  challenge / decision / rationale / evidence cards; `cscard(s, base, i)` is the
  one case card (industry, name, headline, GEMIS's role, status, capability
  chips, Read / Play) used by the index, the homepage, related rows, service
  pages and articles. The homepage order (the owner's revisions of the brief's):
  the hero as it was (tagline, partner line) → the stats section as it was
  (About GEMIS, three confirmed figures, logo marquee) → **Selected work**
  (`.selw`, after the owner's reference screenshots in commit 4440697: a grey
  band pinned to the viewport, divided into panels by thin rules, four project
  cards with play buttons travelling across on scroll, a closing "view all"
  panel; `[data-hscroll]` in `home.js`, vertical without JS, on phones and
  under reduced motion) → **Client stories** (`testimonials_html()`, the
  owner's placeholder testimonials) → the overall thinking (`PRINCIPLES` +
  `OVERALL_FLOW` in `build-home.py`) → **Book a Discovery Session** with the
  form, as it was. No capabilities, stories panel, how-we-work or company
  section on the home; those live on Solutions, Case Studies and Our Story.

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
the site has to be traceable to something already in the repository, and every
figure to `scripts/facts.md` (50+ systems, 5+ sectors and ManaGEM's "nine days to
two" are confirmed there; the sector count is **5+**, not 10+). Anything facts.md
does not confirm — the phone number, team titles, the partner designation — is a
hideable TBC in `scripts/stories.py`, shown only under `?review=1`.

**One standing exception, at the owner's instruction:** the homepage "Client
stories" (`TESTIMONIALS` in `scripts/services.py`) are invented placeholders —
South African names, no company named — until approved quotes arrive. The owner
reaffirmed this after the case-study-led redesign removed them. OPEN_ITEMS.md
tracks them as `testimonials-placeholder`. Do not add more invented content on
the strength of that exception.

## Site map (navigation)

Home · Case Studies (`work/` — hero, stats, the ManaGEM featured project, the
filtered card grid with Read/Play, the approach timeline and a conversion band;
the video overlay is `#videoModal`, opened by any `[data-watch]`) · Solutions ▾ (`solutions/` + nine `solutions/<slug>/`
service pages) · Products ▾ (`products/`: ManaGEM at `products/managem/`, Design
Studio at `studio/`, Technical Academy at gemis.tech) · Insights (`insights/`, three
articles, each linking the case study behind it) · Our Story (`our-story/`; the nav
label and the page name match — keep them that way) · Contact. `solutions/bespoke-software/`, `solutions/managem/` and
`insights.html` are redirect stubs now.
