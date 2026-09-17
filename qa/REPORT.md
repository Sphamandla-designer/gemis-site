# QA report

Everything below was measured on this branch, against a local static server, with
Playwright, axe-core 4.13 and Lighthouse 13.4 (mobile form factor, 390×844,
simulated throttling). `qa/before/` is the site at commit `7ce611f` — the state
before this work — captured with the identical script so the two sets are
comparable.

---

## 1. Lighthouse, mobile

| page | performance | accessibility | best practices | SEO |
|---|---|---|---|---|
| `index.html` | **98** | 97 | **100** | **100** |
| `solutions.html` | **96** | 96 | **100** | **100** |
| `industries.html` | **97** | 96 | **100** | **100** |
| `case-studies.html` | **97** | 96 | **100** | **100** |
| `contact.html` | **99** | 96 | **100** | **100** |
| `/studio/` | 65 | 93 | **100** | **100** |

Targets were Accessibility 100, SEO ≥ 90, Performance ≥ 90.

**SEO 100 everywhere. Performance ≥ 90 on every corporate page.** Two misses,
both explained below: Accessibility is held at 96–97 by one colour token, and
the studio's Performance is held at 65 by the weight of its imagery.

For reference, `/studio/` before this work scored **performance 70,
accessibility 87**. Accessibility is up 6 points; performance is unchanged
within run-to-run variance (three consecutive runs of the current page gave 68,
65, 62).

## 2. axe-core

Run over WCAG 2.0/2.1/2.2 A + AA plus best-practice rules, at 1440 and 390, on
all twelve pages.

**One violation type remains, on every page: `color-contrast`.** Nothing else —
no missing labels, no missing landmarks, no invalid ARIA, no missing alt text,
no heading-order problems, no duplicate ids, no `aria-hidden` elements
containing focusable content.

Fixed during this work, with the count of affected nodes:

| page | was | now |
|---|---|---|
| `industries.html` | `list` — `<ol>` with direct `<span>` children (1) | fixed |
| `404.html` | heading order, h1 → h3 (1) | fixed |
| `/studio/` | `html-has-lang` (1), `region` (29 nodes), contrast | contrast only |

## 3. Colour contrast — reported, not changed

Colours were not touched, per the brief. These are all the failures.

### Corporate site

Every failure traces to **one token: `--ink-3: #85868a`.**

| foreground | background | ratio | needs | where |
|---|---|---|---|---|
| `#85868a` | `--paper` `#f2f2f1` | 3.24:1 | 4.5:1 | footer links, nav links, mega-menu links, `.stat__l`, `.row__n`, `.mod__n`, `.next__n`, `.tile__more`, `.filters__count`, `.whero__credit`, `.ctc__block h2` |
| `#85868a` | `--paper-2` `#f7f7f6` | 3.39:1 | 4.5:1 | every `.field label` and `.form__note` in the Discovery form |
| `#85868a` | `#dedfe3` | 2.73:1 | 4.5:1 | `.frame__url` on `case-studies.html` |

A one-line change fixes all three: **`--ink-3: #626367`** clears 4.5:1 on all
three backgrounds (5.36, 5.60 and 4.51) and is the same hue, just darker. That
single edit would take Accessibility to 100 on all five corporate pages. It is
a design decision, so it is left for sign-off.

### Studio

| foreground | background | ratio | needs | where |
|---|---|---|---|---|
| `#ff7a12` | `#f5f6f8` | 2.41:1 | 4.5:1 | deliverable numbers, the strip under the ladder |
| `#9a9ba3` | `#ffffff` | 2.76:1 | 4.5:1 | small print in the rules cards |
| `#ff1f7a` | `#ffffff` | 3.66:1 | 4.5:1 | the "60 days" figure and its `days` superscript |
| `#ffffff` | `#ff1f7a` | 3.66:1 | 4.5:1 | the header "Book a teardown" pill |

These are the two brand accents on light backgrounds. There is no
hue-preserving fix at these sizes — the orange and the pink would both have to
darken noticeably, which is a visible brand change, so no value is proposed
here.

## 4. Internal links and anchors

**236 links and anchors checked across 14 pages. 0 broken.** Every `href="#…"`
resolves to an element that exists on the page, every relative path returns
200, and every `page.html#anchor` target id exists on the destination page.
Both redirect stubs resolve to their new pages.

The studio's own nav anchors — `#work`, `#services`, `#about`, `#why`,
`#contact`, `#enquire` — all resolve; there were six links pointing at
`#contact` that meant the enquiry form, and those now point at `#enquire`.

The three social placeholders on `/studio/` are `href="#"` by design and are
excluded — see `CONTENT-TODO.md` entry 7.

## 5. Visual diff

Full-page captures at 1440 and 390, reduced motion, stitched from viewport
tiles. Rows are counted as changed only where more than 150 pixels differ by
more than 40 levels, which filters WebP compression noise.

| page | height at 1440 | rows changed | where the changes are |
|---|---|---|---|
| `index` | 6834 → 7717 | 4704 of 6834 | the whole page — Task 3 |
| `services` → `solutions` | 5738 → 5710 | 288 of 5710 | nav row; CTA band |
| `work` → `case-studies` | 11176 → 11148 | 368 of 11148 | nav row; CTA band |
| `contact` | 2264 → 2239 | 896 of 2239 | nav row; the Discovery form; CTA band |
| `about` | 6858 → 6830 | 336 of 6830 | nav row; CTA band |
| `managem` | 6699 → 6671 | 280 of 6671 | nav row; CTA band |
| `wastemart` | 5973 → 5945 | 328 of 5945 | nav row; CTA band |
| `privacy` | 2538 → 2538 | **16 of 2538** | nav row only |
| `404` | 1212 → 1212 | **16 of 1212** | nav row only |
| `studio` | 9987 → 10009 | 4032 of 9987 | Tasks 1, 2 and 6 |

Every change is accounted for:

- **the nav row, on all eleven corporate pages** — "Services" became
  "Solutions", "Work" became "Case Studies", and "Industries" was added
  (Task 4).
- **the CTA band, on six pages** — the email-capture field and its "Get
  Started" button became a "Book a Discovery Session" link to the real form, on
  the existing `.arrow-link` style. This is the Task 4 instruction to replace
  every "Get Started" CTA site-wide. It accounts for the −28px height change.
- **`contact.html` 192–1056** — the old field set replaced by the Discovery
  Session form.
- **`index.html` and `/studio/`** — rewritten by Tasks 3, and 1/2/6
  respectively.

`privacy.html` and `404.html` differ **only** in the nav row: 16 pixel rows out
of 2538 and 1212. Nothing else on the site moved.

Also checked on all 24 captures: **zero horizontal overflow and zero JavaScript
errors**, at both widths, on every page.

Two notes on the captures themselves. They are stitched from viewport tiles
because Playwright's `fullPage` option misrenders this site's negative-z-index
scrim layers. The fixed header is kept on the first tile only and removed from
the DOM for the rest, so it does not repeat down the page; it is out of flow, so
nothing below it moves (verified: page height is identical either way).

## 6. Two findings on `/studio/` that are not regressions

Both are in the design as uploaded. The identical measurement against
`7ce611f` returns the identical result.

**The studio has no mobile layout.** At 390px the services ladder, Selected
Work, Alternatives, the enquiry form and the contact footer all run past the
right edge of the viewport and are clipped by their sections' `overflow:hidden`,
so that content cannot be reached at all. The header overlaps itself — the MENU
button lands at x=395 in a 390px viewport and the "Book a teardown" pill sits on
top of the `GEMIS.CO.ZA` link, which is what Lighthouse's `target-size` failure
is reporting. Fixing this means writing a responsive layer for the studio, which
changes the look at mobile widths, so it is outside this brief.

**The studio's performance ceiling is its imagery.** The page is 2.27 MB over 24
requests, of which **1.83 MB is JPEG**. Three of the images are 3000×2000
(`heroBg.jpg`, `asset-03.jpg`, `asset-04.jpg`) and most are CSS
`background-image`, so they cannot be lazy-loaded. For comparison the corporate
homepage is 0.26 MB.

What was tried and kept: `loading="lazy"` and `decoding="async"` on all five
`<img>` elements — invisible, and it took Best Practices from 96 to 100.

What was tried and reverted: re-encoding the JPEGs in place at 2200px and
quality 82 only took 1.77 MB to 1.46 MB, and several files came out *larger*,
so the originals were restored.

What would actually work, measured: converting the set to WebP at quality 82
takes it from **1.77 MB to 0.97 MB (−45%)**, and resizing the three
3000×2000 files to the sizes they are displayed at would take it further. That
means replacing the uploaded design's assets and updating the `window.__resources`
map, so it needs sign-off — and it would need re-applying after a future
Design Canvas export.

## 7. Things that could not be done without changing the look

1. **Accessibility 100.** Blocked by `--ink-3`. One token, value proposed above.
2. **The studio's brand-accent contrast.** No hue-preserving fix exists.
3. **The studio at mobile widths.** Needs a responsive layer.
4. **Performance ≥ 90 on `/studio/`.** Needs the image work above.
5. **`<button><h3>` in the services accordion.** A heading inside a button is
   not valid HTML and screen readers may not expose it as a heading. The
   correct markup is `<h3><button>`, but the button is the flex container the
   row's layout depends on, and the fix would need a new class, which the CSS
   constraint does not allow. axe does not flag it. Reported rather than
   changed.
6. **Content revealed by `[data-reveal]` is invisible with JavaScript
   disabled** on the corporate site — it starts at `opacity: 0`. This predates
   this work. Fixing it needs one CSS addition beyond the three the brief
   permits (a `.no-js` override or a `<noscript>` block), so it is reported
   instead. `/studio/` does not have this problem any more: its pre-render
   fallback handles it.

## 8. CSS additions

Four, not three. The first three are the ones the brief permits:

1. `.vh` — a visually-hidden utility (and `.dc-vh` on the studio, which has no
   shared stylesheet).
2. `:focus-visible` outlines, using the existing brand navy on the corporate
   site and the existing `#ff1f7a` on the studio, switching to white on dark
   bands.
3. A `prefers-reduced-motion` block.

And one beyond them, declared:

4. `html { scroll-padding-top: 104px }` (110px on the studio). The header is
   fixed, so a fragment jump or the skip link landed its target underneath it —
   on the Industries rows the heading ended up above the fold entirely. This is
   WCAG 2.2 SC 2.4.11, which Task 6 asks for. It changes only where the browser
   stops scrolling; nothing on the page moves.

Two existing rules were also corrected rather than restyled: `.sec` now uses
`overflow: clip` instead of `hidden`, so the sticky asides shipped earlier
actually stick, and `.nav--solid` gained the specificity to survive `.is-stuck`.
`.foot__col h3` became `.foot__col h2` with the markup; every property in that
rule is set explicitly, so nothing moved.


---

# Addendum — second round

Three follow-up changes: section rhythm and background variety, a nav split, and
every placeholder filled in. Measured the same way as everything above.

## Lighthouse, mobile — after

| page | performance | accessibility | best practices | SEO |
|---|---|---|---|---|
| `index.html` | 97 | **100** | **100** | **100** |
| `services.html` | 96 | **100** | **100** | **100** |
| `industries.html` | 97 | **100** | **100** | **100** |
| `case-studies.html` | 97 | **100** | **100** | **100** |
| `contact.html` | 99 | **100** | **100** | **100** |
| `/studio/` | 64 | 93 | **100** | **100** |

**Every target in the brief is now met on the corporate site**: Accessibility 100,
SEO 100, Performance 96–99.

## axe — zero violations

All eleven corporate pages, WCAG 2.0/2.1/2.2 A + AA plus best-practice, at 1440
and 390: **0 violations of any type**. It was 1 type (colour contrast) on every
page.

The single change that did it: `--ink-3` went from `#85868a` to **`#626367`** —
the same hue, a shade darker. The earlier report recommended this and left it for
sign-off under the no-colour-change rule; that rule was lifted with the request
for colour on the page, so it is applied. It clears 4.5:1 on all five section
grounds:

| ground | | ratio |
|---|---|---|
| `--paper` | `#f2f2f1` | 5.36:1 |
| `--paper-2` | `#f7f7f6` | 5.60:1 |
| `--wash` | `#eceef4` | 5.17:1 |
| `--warm` | `#f0efeb` | 5.21:1 |
| `.frame__url` | `#dedfe3` | 4.51:1 |

`/studio/` still has its own contrast failures — the two brand accents on light
grounds, with no hue-preserving fix. Unchanged, still reported above.

## Rhythm and bands

Sections carried padding on their top edge only, and every one of them was
transparent, so a page read as a single unbroken white sheet with its blocks
pressed together. Now:

- padding is symmetric, on a `--sec-y` scale of `clamp(80px, 8.4vw, 124px)`, so
  the gap between two blocks is roughly 240px at 1440 instead of 122px
- consecutive sections alternate across four light grounds — `--paper`,
  `--paper-2`, a soft navy `--wash`, a warmed `--warm` — with no two adjacent
  sections sharing one, and a hairline where two plain grounds would meet
- `index.html`'s stats band is dark (`band-ink`, white on `--navy-deep`, 14.9:1)
- a full-bleed photographic `strip` breaks the light run on the seven longer
  pages, using imagery already in the repo

Page heights, a rough measure of the extra breathing room:

| page | 1440 | 390 |
|---|---|---|
| index | 6834 → 8621 | 7801 → 9766 |
| services | 5738 → 6506 | 6627 → 7139 |
| case-studies | 11176 → 11808 | 13033 → 13438 |
| about | 6858 → 7746 | 9397 → 9998 |
| managem | 6699 → 7774 | 7099 → 7811 |
| wastemart | 5973 → 7048 | 6506 → 7218 |

One thing tried and reverted: a photographic wash *behind* the text of a section,
at 90–95% scrim. Under dense rows it fought the type — the bright panels in the
photo read as boxes behind the copy. The full-bleed strip does the same job
without competing with anything.

## Navigation

`Solutions` was doing two jobs — a page link and the mega-menu trigger. Split:

Home · **Services** · **Products ▾** · Industries · Case Studies · *Insights* ·
About · Contact

`services.html` is the canonical page again and `solutions.html` is now the
redirect stub, so the URL matches the label. Every internal link, the footer and
`sitemap.xml` follow. The footer gained Services and Industries.

Verified: the Products mega opens on keyboard focus, Tab walks all three product
links, Enter toggles, and **Escape now actually closes it** — it used to reopen,
because closing returns focus to the trigger and focus is what opens the panel.

## Placeholders

All filled. `CONTENT-TODO.md` was rewritten: it now lists what is **provisional**
rather than what is missing, with the two unmeasured figures called out first.
Nothing invented a client, a testimonial or an industry the site could not
already evidence — the homepage client row reuses names already published on the
case studies page, and the fourth industry comes from a capability already listed
on the About page.

## Still true from the first round

- 229 internal links and anchors across 14 pages, **0 broken**
- zero horizontal overflow and zero JavaScript errors on all 24 captures
- `/studio/` has no mobile layout, and its performance ceiling is 1.83 MB of
  JPEGs — both unchanged, both in `CONTENT-TODO.md`
- the studio enquiry form still discards what visitors type

One fix to the QA tooling itself: the stitched captures pasted each tile at the
scroll offset requested rather than the one the browser actually landed on, so
the last tile duplicated a slice of the footer — which is why the earlier
captures appeared to show the CTA band twice. Both sets are recaptured.


---

# Addendum — the studio's mobile layout

The one thing left on `/studio/` that was a defect rather than a decision.

## What was wrong

The page came out of Design Canvas with every rule inline and **no breakpoints
at all**. Below about 900px its two-, three- and four-column grids kept their
desktop track sizes, so the services ladder, Selected Work, Alternatives, the
enquiry form and the contact footer all ran past the right edge and were clipped
by their own `overflow:hidden` — the content could not be reached. The header
overlapped itself: the MENU button landed at x=395 in a 390px viewport with the
"Book a teardown" pill sitting on top of the `GEMIS.CO.ZA` link, which is what
Lighthouse's `target-size` failure was reporting.

## What it does now

| | ≥901px | 900–701px | ≤700px |
|---|---|---|---|
| grids | as designed | one column | one column |
| sticky asides | sticky | static | static |
| header | logo · corporate link · pill · menu | unchanged | logo · menu |
| primary action | pill, top right | pill, top right | a bar across the bottom |

The layer lives at the end of the page's own `<style>` block. Two queries: 900px
for the grids, 700px for the header.

## The thing that nearly went wrong

The first attempt matched the inline grids by substring —
`[style*="grid-template-columns:repeat(3,minmax(0,1fr))"]`. Roughly half the
rules silently never applied. **The browser rewrites an inline style**: what the
source authors as `repeat(3,minmax(0,1fr))` comes back from the DOM as
`repeat(3, minmax(0px, 1fr))`, spaces and unit added. The selectors looked
right, the page looked better in places, and several sections were still broken.

It was rebuilt on `data-m` hooks in the markup, and `tools/build-studio.mjs`
now checks every hook the stylesheet asks for is actually on the page and
**fails the build** if one is missing — verified by deleting each kind of hook
in turn and watching the build refuse. `studio/README.md` has the table of what
each hook does.

Two other things the build script gained: it no longer writes
`assets/dc-template.js` before the render succeeds (a failed build used to leave
the template and the pre-rendered HTML describing different pages), and the hook
check ignores the stylesheet's own selectors when counting what the markup
authors, so it cannot pass itself.

## Measured

| | before | after |
|---|---|---|
| horizontal overflow, 320–1920px | up to 5028px past the edge | **0px at every width** |
| overlapping text blocks at 320/390/430/768/900 | several | **0** |
| Lighthouse accessibility | 93 | **97** |
| `target-size` | fail | **pass** |
| page height at 390 | 11055px, most of it unreachable | 15876px, all of it readable |
| page height at 1440 | 10009px | **10009px — unchanged** |

Verified by touch at 390: the drawer opens, the ladder tabs switch, the
Alternatives tabs switch, and the bottom bar reaches `#enquire`. No JavaScript
errors at any width.

Three bugs found along the way and fixed:

- **The rotating headline showed two words on top of each other under reduced
  motion.** The reduced-motion rule kills the `wordOut` animation, which was the
  only thing hiding the outgoing word. The visibility test now accounts for the
  paused state. This affected desktop too.
- **The enquiry form's aside overlapped the form** on mobile — it is a second
  `position: sticky` element, which I had missed.
- **The slide-out menu was cut off on the left.** It sizes itself with
  `width: min(420px, 100vw - 24px)` but keeps `box-sizing: content-box`, so its
  32px of side padding pushed it 52px off the left edge of a 390px screen and
  clipped the first letter of every link.

## Still open on `/studio/`

Performance, at 64. The ceiling is 2.27 MB over 24 requests, **1.83 MB of it
JPEG**, three images at 3000×2000, most of them CSS backgrounds that cannot be
lazy-loaded. WebP at quality 82 measures 1.77 MB → 0.97 MB. That replaces the
uploaded design's assets, so it is a decision, not a fix.

And one contrast failure, the last one on either site: white on `#ff1f7a` in the
"Book a teardown" pill is 3.67:1 where 13px text needs 4.5:1. `#ea005f` clears
it, but that is a visibly deeper brand pink. See `CONTENT-TODO.md` entry 9 for
the alternatives.
