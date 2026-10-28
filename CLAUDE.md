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
| `solutions/`, `solutions/<service>/` ×9 | `scripts/solutions.py` (all page copy, evidence, FAQs, section order; every claim sourced in `docs/SOLUTIONS-EVIDENCE.md`) rendered by `scripts/build-solutions.py` | `python3 scripts/build-services.py` (calls it) |
| `products/`, `insights/`, `insights/<article>/` ×3 | `scripts/services.py` | `python3 scripts/build-services.py` |
| `products/managem/`, `our-story/` | `scripts/stories.py`, old pages in git history | `python3 scripts/build-other.py` |
| `work/`, `work/<story>/` ×6 | `scripts/stories.py`, `scripts/cases.py` (record + `DETAIL`: basis, flow, walkthrough, decisions, validation) | `python3 scripts/build-pages.py` |
| the header nav and footer columns on every page | `scripts/apply-chrome.py` (+ `services.py` for the two drop-downs) | `python3 scripts/apply-chrome.py` (`--check` in CI) |
| `gemis-site-standalone.html` | every chrome page at any depth, `site.css`, the scripts, the font, images (the walkthrough stills included) and the MP4 videos | `python3 tools/build-site-standalone.py` — one 19 MB file; pages run in frames, videos reach them as blob URLs |
| `gemis-studio-standalone.html` | the five studio pages, their runtime (`react.js`, `react-dom.js`, `dc-runtime.js`, `dc-template.js`, `dc-boot.js`), the twelve font files, every image and the mark | `python3 tools/build-studio-standalone.py` — one 3.3 MB file; pages run in frames, fonts as data URIs, **images as blob URLs** (the Design Canvas runtime splits inline style strings on `;`, so a `data:` image URI in a hero layer would be cut at `data:image/jpeg`); links to the corporate site open the live addresses |
| `assets/img/cases/<slug>/*.jpg` (37 stills) | frames of the case study videos, picked by scene | the ffmpeg commands in `docs/REDESIGN-REPORT.md` |

Full rebuild, in order: `build-home` → `build-services` → `build-pages` →
`build-other` → `apply-chrome`. (`build-stories.py` is the shared markup library
the others import; running it alone only prints a summary.)

Rebuild the standalone bundle after **any** change to a root page or to
`assets/css/site.css` or `assets/js/site.js`, or it silently goes stale; rebuild
the studio bundle after any change under `studio/`.

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

## One design system — Brand v3, at the tail of `site.css`

The stylesheet was written page by page and the layers contradict each other.
The last block, **BRAND v3 — the GEMIS design system** (2026-10-28, from the
owner's Apple-like brief, kept on the GEMIS dark blue), and the short blocks
after it are where the decisions live; put a change to colour, type or spacing
there. Its selectors carry `:not(#_)` to beat older, more specific rules without
`!important`; a rule that must outrank another v3 rule doubles it (`:not(#_):not(#_)`).

- **Tiles.** Every section is an edge-to-edge tile and the colour change is the
  divider: white (`.band`), parchment `#f5f5f7` (`.band-wash`, `.band-tint`,
  `.trust`, `.words`) and deep navy `--tile-1 #0b2642` (`.band-ink`, `.prin`,
  `.sq`, `.built`, `.convert`, `.endnote`, the story and ManaGEM heroes). The
  footer is navy too; after a navy closing tile it steps to `--tile-3` so the
  two read apart. No gradients, no corner accents, no shadows on cards or type.
- **One accent.** The dark blue `--primary #16395e` is every link and every
  filled pill on light surfaces; on navy tiles links are `--primary-on-dark
  #8fc1f5` and the filled pill is white with navy text. Ink `#1d1d1f`, ink-2
  `#424245`, ink-3 `#6e6e73` (4.66:1 on parchment — do not lighten it).
  Hairline `#e0e0e0`. The old tokens are remapped (`--navy`, `--navy-deep`,
  `--wash`, `--rule`), so older components follow.
- **Type.** Inter (variable, self-hosted, OFL) standing in for SF Pro: headlines
  600 with tight tracking (hero 56px → 40px at 1068px → 34px → 28px under 420px),
  body 17px/400/1.44 with `-.022em`, taglines 21px. Eyebrows are 14px/600 in
  ink-3, normal case. Weight 500 does not exist in the ladder; `strong` is 600.
  Tabular figures on every number read as a number.
- **Heroes are centred product tiles**: eyebrow, a two-line title
  (`two_lines()`), the tagline, two pills (filled + ghost), and the product
  beneath — `composite()` in `build-stories.py`, app windows and a phone cut
  from the case-study video stills in `assets/img/ui/` (each marked sample data
  in its video), resting on the tile with the system's single shadow
  `rgba(0,0,0,.22) 3px 5px 30px`. Never invent a dashboard. The Solutions
  drawings sit in a white window card the same way. Industries, Contact, 404 and
  Privacy open on plain white.
- **The chrome.** The global nav is a 48px navy bar (`--nav-bar #071b31`),
  sticky and in flow (so no page needs `--hero-top` clearance); 13px white
  links; the Solutions and Products flyouts are navy sheets with 19px/600
  entries. Story pages, the Case Studies index, the nine service pages and
  ManaGEM carry a frosted **sub-nav** (`subnav()` in `build-stories.py`,
  emitted first in `<main>`): the page's name, its chapters, one small pill;
  sticky under the bar, parchment at 80% with blur, navy over a navy hero
  (`:has()`); under 900px only the name and the pill remain. Anchors carry
  `scroll-margin-top: 112px`. The footer is the efferd `footer-3` port in
  `FOOTER` in `apply-chrome.py`, on navy, 14px links at 2.2 leading.
- **Surfaces.** Cards (`.cscard`, `.selw__card`, `.post`, `.prod`, `.dec`,
  `.flow__step`, `.sol__card`, `.sd__item`, `.cs__main` …) are white, 1px
  hairline, radius 18, 24px padding, no shadow, no hover lift. Tags are 12px
  hairline pills. Play controls are the translucent grey chip
  `rgba(210,210,215,.64)` with blur. Inputs are 17px, `#d2d2d7` border, radius
  11, a 3px focus ring. Buttons press with `transform: scale(.95)`. Section
  heads (`.sec__head` and the `*__head` variants) are centred stacks.
- **The logo** is the flat traced sprite in `currentColor` (the gem at .34
  opacity), white on navy, ink on light.
- **Rhythm** is `--sec-y` (56–80px) on both edges of every tile. Shell 1440px.
- **Case study pages** are built from `scripts/cases.py` (navy hero with
  status, composite and Play story, overview, business challenge, strategy and
  approach, outcomes split into delivered / verified / intended, related work,
  tailored enquiry). Only the client-confirmed metric is a number; a section
  with nothing verified is omitted.
- **Every hero title is two lines**: the generators pass the title through
  `two_lines()` in `build-stories.py`, which breaks it once where the halves are
  most even (after a full stop, colon or comma when close) with a
  `<br class="h1-br">`; the title does not wrap on its own above 620px, where the
  break is dropped and it wraps naturally. `contact.html` and `industries.html`
  carry the break by hand. A single-word title (HomeAssist, WasteMart) stays one
  line. A story page's endorsement chapter is itself `.unconfirmed`, so an
  unapproved line removes the whole band rather than leaving an empty one.

- **The reference kit** (from the owner's screenshots in `qa/design-refs/`) runs on
  every page: `.srows/.srow` numbered ruled rows for anything ordered (services,
  steps, founders, reasons), `.feats/.post` ruled features for anything with an
  image (articles, case studies, products), `.rlist` ruled link lists, `.plusgrid`
  (`--tr`, `--br`) corner accents (hidden under Brand v3), and `.endnote` as the closing band. The
  helpers `srows()` and `feat()` in `scripts/build-stories.py` emit the markup.
- **Three more references** (`qa/design-refs/stories-panel.png`, `timeline.png`,
  `testimonials.png`) set: the stories panel (`stories_section()` — on the home's
  partnership section, on a navy tile, never black) and the horizontal
  timeline (`tline(steps, label)` — How we work, the six stages, Contact's next
  steps, About's milestones). The old "Client stories" stage is gone with its
  invented entries; the homepage carries **In their words** instead. Any tabbed stage is a
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
  (`.selw`, pure white: the shared section header, then four equal-height
  case study cards on a horizontal travel pinned to the viewport, two to a
  screen on desktop and one at 901–1100px (`[data-hscroll]` in `home.js`,
  which follows the scroll with inertia — each frame closes 11 % of the
  distance — and sets `--hs-d` per card and `--hs-v` on the travel so the
  pictures drift and lean with the motion; keyboard focus snaps),
  a two-column grid on tablets and one column under 620px; each card plays
  its video; then the transition statement `[data-scaleup]` that scales up
  as it is scrolled to the centre of the viewport, holds, and releases;
  both static without JS and
  under reduced motion; the band's bottom padding lives on the statement's
  pin (`.selw__out-pin`), so when the pin releases the statement is exactly
  `--sec-y` from the next section) → **In their words** on the Client stories stage
  (names on the left, one quotation at a time, the three lines from
  `scripts/endorsements.md`) → **Operating principles** (`operating_logic()`,
  section `.prin`: the four principles, verbatim in `OPERATING`, on the
  standard dark band as a sticky index and a ruled list — left, the label,
  the statement on `--fs-display` and one large index numeral with four
  ticks; right, four numbered ruled rows (statement on `--fs-title`,
  evidence, "Seen in" links to the chapter pages), then "Read more of our
  thinking" with the three articles. On wide screens with scripts,
  `[data-principles]` in `home.js` makes the row at 42 % of the viewport the
  live one — full white, the others at half — and the numeral follows it;
  hover or focus lifts any row. Under 1000px, without JS and under reduced
  motion every row is full and nothing moves. The earlier drawn-line
  composition is gone; its `.op` rules are dormant in `site.css`) → **Book a Discovery
  Session** with the
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
does not confirm — team titles, the partner designation — is a hideable TBC in
`scripts/stories.py`, shown only under `?review=1`. **There is no phone number
anywhere on either site** (the owner removed it, 2026-10-23): no `tel:` link,
no number in copy, on the corporate pages or in `studio/src/`.

**Endorsements are quotations, never written here.** `scripts/stories.py` reads
them character for character from `_project/assets-incoming/content/endorsements.md`
(or `scripts/endorsements.md`) — direct quotes from gemis.co.za — into
`ENDORSERS[...]['line']`. The three lines are in `scripts/endorsements.md` now
(supplied by the owner, 2026-10-22). A person with no line in that file has no
card on the story and ManaGEM pages, and their homepage slide shows the italic
"Quotation to follow." (`.cs__pending`, a hideable TBC). Names, titles and companies come from `scripts/facts.md`
(Keshan Patel, CEO, HomeAssist (Pty) Ltd · Ryan Smith, SBS Waterproofing, no
title · Philippine Francke, Managing Director, HashTopic). Never use the word
"testimonial" in visible copy or in class names.

## Site map (navigation)

**Solutions** (`docs/SOLUTIONS-REPORT.md`): the directory is a nine-into-one hero
drawing, a numbered index (what each discipline is for, when to choose it), an
illustrative six-stage "work together" track, evidence from three projects, seven
"start from the problem" pathways, a quotation and a centred close. Each service
page picks its own section order from the components in `build-solutions.py` and
has its own CSS-only hero drawing (`DIAGRAMS`). Evidence modules must say why the
project is relevant **on that page** and only cite what its case record states —
Trans Hex and Sonke record no Azure and no Power BI. Service CTAs link to
`contact.html?service=<slug>`, which `site.js` uses to pre-select the topic.
`scripts/services.py` now holds only slug, name and the navigation line.

Run axe with the page list — `SP=<scratch> node axe-all.mjs <page> <page> …` takes
its pages as arguments and silently checks nothing without them.

Home · Case Studies (`work/` — hero, stats, the filtered card grid with
Read/Play, **How GEMIS approaches projects** as the four-stage ledger
(`stages(SV.WAYS)` in `build-stories.py`: one ruled line, four hairlined
columns, a light numeral, the stage, the copy), **In their words** (the shared
`in_their_words(base)` stage, the same as the home's), then the centred
"Your project" conversion band (`.convert` is centred everywhere); the
ManaGEM featured block is gone; the video overlay is `#videoModal`, opened by
any `[data-watch]`) · Solutions ▾ (`solutions/` + nine `solutions/<slug>/`
service pages, built from `scripts/solutions.py`) · Products ▾ (`products/`: ManaGEM at `products/managem/`, Design
Studio at `studio/`, Technical Academy at gemis.tech) · Insights (`insights/`, three
articles, each linking the case study behind it) · Our Story (`our-story/`; the nav
label and the page name match — keep them that way) · Contact. `solutions/bespoke-software/`, `solutions/managem/` and
`insights.html` are redirect stubs now.
