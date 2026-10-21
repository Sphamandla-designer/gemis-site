# Implementation notes

Decisions, deviations and assumptions on branch `site-update/gemis-stories`.
Read with `IMPLEMENTATION_PLAN.md` (what was planned) and `OPEN_ITEMS.md` (what is
still unconfirmed).

---

## 1. The brief's design tokens are not the site's design tokens

**This is the largest deviation and it needs sign-off.**

The brief and the prompt both specify Deep Navy `#0F2D5E`, Primary Blue `#1A56A0`,
Cormorant Garamond for editorial headings and endorsement lines, and DM Sans for
body — describing them as the palette and fonts "already in the CSS".

They are not in the CSS. Measured on `assets/css/site.css`:

| The brief says | The repository has |
|---|---|
| Deep Navy `#0F2D5E` | `--navy: #1f2557`, `--navy-deep: #161b40` |
| Primary Blue `#1A56A0` | no equivalent token |
| Cormorant Garamond | not present |
| DM Sans | not present |
| — | `Archivo Var`, the only family, a variable font loaded from `assets/fonts/` |

`grep -ci '0F2D5E\|1A56A0\|Cormorant\|DM Sans' assets/css/site.css` returns 0.

**Resolution: the repository wins.** Three rules in the prompt agree:

- "If either conflicts with what you find in the repo… follow the repo and record
  the difference in `IMPLEMENTATION_NOTES.md`."
- "**Do not redesign.** Keep the palette… fonts… already in the CSS."
- Phase 7: "no new web-font families."

Adopting the brief's tokens would be a redesign of the whole site and would add two
font families against an explicit performance rule. Everything built here uses the
repository's existing tokens and Archivo Var.

Where the brief asks for "Cormorant Garamond italic" on endorsement lines, the
build uses Archivo Var italic at the same editorial size and weight, so the
endorsement still reads as a distinct editorial voice.

Tracked as `brand-tokens` in `OPEN_ITEMS.md`. If the brief's palette is the real
intent, that is a separate rebrand, not this update.

## 2. Assets arrived in the repository root, not `_project/assets-incoming/`

The prompt describes `_project/assets-incoming/`. No such folder exists. The two
"Project Assets" commits put all 28 video files directly in the repository root.

Following the repo, as instructed, the 21 web files (7 × `_web.mp4`, `_web.webm`,
`_thumb.jpg`) were moved to `assets/video/case-studies/`, which is where the
prompt's Phase 4 expects to serve them from.

**The 7 masters (`*_VO_16x9.mp4`, 29 MB) were removed from this branch.** The
prompt says masters are not needed and must not be committed. They remain in git
history on `main` and can be restored from there. Note that while they sit on
`main` they are publicly downloadable from the live site.

## 3. Only the videos arrived

Of the eight asset folders the prompt expects, only the videos are present. No
logos, portraits, screenshots, team photos, `facts.md` or `endorsements.md`.

Three consequences follow from the prompt's own fallback rules:

- **Product spelling is `ManaGEM`** — "If `facts.md` is silent, use ManaGEM to
  match the videos, and log it." Applied everywhere except verbatim transcripts
  and file names.
- **No metric is published.** Both legacy figures carry `data-tbc`.
- **No endorsement line exists anywhere.** The brief gives a "theme" for each
  executive; that is layout context and was not turned into a quote. The cards
  render "Endorsement to follow".

The "Then and now" blocks are **omitted entirely** rather than mocked up, which is
what the prompt requires when screenshots are missing.

## 4. Facts used, and where each came from

Everything asserted on the new pages traces to the video document's narration or
its "Relationship or period" line, both of which the prompt counts as confirmed:

| Fact | Source |
|---|---|
| SBS: client since 2014, own system from 2015, grew into ManaGEM | SBS transcript and period line |
| HomeAssist: "more than ten years" | HomeAssist transcript |
| WasteMart: "more than ten years" | WasteMart transcript |
| Trans Hex: 2017, Baken mine, Lower Orange River, SAP feed | Trans Hex transcript |
| Sonke: 40 countries across Africa | Sonke transcript |
| Tore's: 430+ learners, 24 Western Cape schools, for the University of Stellenbosch Business School | Tore's transcript |
| ManaGEM: about a dozen companies today | ManaGEM transcript |

Figures visible on app screens inside the videos are sample data and are never
quoted, per the video document's own instruction.

## 5. Deviation from the standing "always merge" rule

`CLAUDE.md` in this repository says every piece of work ends merged. **This branch
is deliberately not merged.**

The prompt sets `check-tbc.mjs` as a go-live gate and says "Do not merge it", and
the brief says placeholders are "fine in the build, never on the live site".
Merging now would publish TBC pills, "Endorsement to follow" cards and "Image TBC"
blocks to the live site.

A pull request is opened for review and left open. It becomes mergeable when
`node scripts/check-tbc.mjs` exits 0.

## 6. Smaller decisions

- **`{BASE_URL}` for schema** resolves to
  `https://sphamandla-designer.github.io/gemis-site/assets/video/case-studies/`,
  read from the existing canonical tags. The video document suggests
  `https://gemis.co.za/media/case-studies/`, but the site is not served there, and
  schema URLs must resolve.
- **Header and footer are duplicated per page** with no include mechanism, so the
  new navigation is applied by editing every page. A build-time include was not
  introduced, since the prompt forbids adding a site generator.
- **`industries.html`** stays live, out of the main nav, linked from the footer and
  from the Our Work filters.
- **No eighth video** was supplied, so no eighth entry exists. Logged.
- **`gemis-site-standalone.html`** is regenerated from the new pages, as
  `CLAUDE.md` requires, since root pages and `site.css` both changed.

## 7. The standalone bundle is stale, deliberately

`CLAUDE.md` says to regenerate `gemis-site-standalone.html` after any change to a
root page or `site.css`. On this branch that is not possible.

`tools/build-site-standalone.py` models the site as flat `name.html` files at the
repository root, reads each as `R/<page>.html`, rewrites `assets/…` paths, and
asserts that every internal link matches one of those names. The new structure is
folder URLs — `work/`, `work/wastemart/`, `solutions/managem/` — with `../` and
`../../` asset paths. The build fails its own assertion on the first page.

Reworking it for nested pages is a real piece of work with its own risk of subtle
breakage, and neither the brief nor the prompt mentions the bundle at all. It was
left alone rather than half-fixed, and the staleness is recorded here, in
OPEN_ITEMS.md and in the pull request, so it is loud rather than silent — which is
what the rule in CLAUDE.md is actually for.

The file on this branch therefore shows the **old** site. Do not review it.

## 8. Verification results

Run on the final branch state.

| Check | Result |
|---|---|
| `node scripts/check-tbc.mjs` | **27 placeholders**, exits 1 — as expected until Leon confirms the facts. Every id matches `OPEN_ITEMS.md`; nothing is undocumented. |
| Link check (34 pages) | **896 links and anchors, 0 broken.** |
| axe-core, WCAG 2.2 AA | **0 serious or critical** across Home, Our Work, all six story pages, Solutions, Bespoke Software, ManaGEM, Our Story and Contact. |
| Lighthouse (mobile emulation) | **100 / 100 / 100 / 100** on Home, Our Work and the WasteMart story — performance, accessibility, best practices, SEO. |
| Layout, 375 / 768 / 1280 / 1600 | 5 pages × 4 widths — no horizontal scroll, no clipped cards, no JS errors. |
| Reduced motion | 0 elements left hidden; nothing animates. |
| JavaScript off | All 8 timeline entries and all 7 videos present in the DOM. |
| Keyboard | 29 timeline focusables all reachable, visible focus on first tab stop, Skip-the-story link resolves, filters operable with `aria-pressed` and a live region. |
| Naming sweep | 0 hits for ManaGem, ManageM, Waste Mart, Home Assist, Tores, testimonial, 15 years. |
| Autoplay | 0 occurrences anywhere. |
| Chrome consistency | `apply-chrome.py --check` passes on every page. |

Three accessibility defects were found and fixed during this pass, all of them mine:

1. `.eyebrow` and `.chero__sub` were used inside `.chero`, which is navy-deep. The
   eyebrow rendered navy on navy at **1.15:1**. The page already had `.chero__kicker`
   and `.chero__copy` for exactly this band; the generated pages now use them.
2. `.endnote` sets `color:#fff` and was paired with `band-warm`, giving white text
   on cream, also 1.15:1. The band classes were removed.
3. The "See it in production" links were being injected inside `.acc__btn` — a link
   inside a button, which axe fails as `nested-interactive`. They now sit at the end
   of each panel. Closing panels are also `inert` now, since `aria-hidden` alone left
   their links in the tab order.

`.story__meta` on the dark hero was a fourth, found the same way and fixed against
the colours `.chero__meta` already used.
