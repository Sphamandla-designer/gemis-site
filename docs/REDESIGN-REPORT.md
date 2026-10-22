# Case-study-led redesign — final report (Phase H)

Date: 2026-10-22 · Branch: `claude/awesome-albattani-a8q6hu` · Base: `main` at `2752432`

The audit, evidence register and plan are in `docs/REDESIGN-AUDIT.md`. This is
what was changed, what was decided, what was tested, and what still needs the
owner.

**Not deployed.** Per the brief, nothing was merged and no pull request was
opened. The branch is pushed so the work survives the session container and can
be reviewed at any depth; the Pages site on `main` is unchanged.

---

## 1. What changed

### Homepage (`index.html`, generated whole by `scripts/build-home.py`)

The page now runs in the brief's order. Every section is built from the data
files, so nothing on it is written that is not already evidenced in
`scripts/stories.py`, `cases.py`, `services.py` or `facts.md`.

| # | Section | What it shows | Source |
|---|---|---|---|
| 1 | Proposition hero | "Systems your operation can run on — not work around." with the tagline as its support line; *Explore our work* / *Discuss a project*; the hero photograph; the partner line | — |
| 2 | Featured case study | ManaGEM with its SBS Waterproofing origin: context, challenge, contribution, solution, the two verified facts, video, links to the ManaGEM and SBS pages | ManaGEM and SBS videos, facts.md |
| 3 | Selected projects | WasteMart (operations chain), HomeAssist (national claims workflow), Sonke (M&E) in an editorial two-column grid, each with role, status, capabilities | videos, cases.py |
| 4 | The thinking | Three workflow diagrams drawn from the narration — the SBS pipeline, the WasteMart hand-off chain, the Trans Hex data flow — each with what it solved and a link | transcripts |
| 5 | Capabilities, demonstrated | Six capability groups, each tied to the projects that demonstrate it and to its solution page | services.py, stories.py |
| 6 | Long-term partnership | The three confirmed figures, the two client-confirmed results, the owner's client logos, then the stories panel (video of the founding relationships, with the founding tags) | facts.md, logos, videos |
| 7 | How GEMIS works | Understand · Design · Build · Evolve on the horizontal timeline | services.py |
| 8 | The company | Founded 2014, Cape Town; the Microsoft stack; GEMIS Studio; ManaGEM; the office — no unconfirmed titles | company profile 2025, facts.md |
| 9 | The enquiry | "Have a business challenge worth solving?" → Contact | — |

Removed: the six invented testimonials; the second copy of the enquiry form
(the form lives on Contact only); the generic trust strip (its confirmed figures
moved into section 6).

### Case Studies index (`work/`)

Every card now carries the business context, GEMIS's role, the project status
and capability labels, through one shared card (`cscard()` in
`scripts/build-stories.py`). The filters, Read / Play actions, featured ManaGEM
block, approach timeline and conversion band were verified working.

### Case study template (`scripts/build-pages.py` + `scripts/cases.py`)

Each of the six pages now runs: hero (status, Play, *Discuss a similar
challenge*) → project snapshot (industry, users, role, scope, timeframe, status,
key deliverables) → business challenge → **discovery and evidence** (what the
design was based on; states that no research report exists) → strategy and
system structure (principles, prose, the video, the **workflow diagram**) →
**the system, step by step** (four to six stills from the case study video with
captions) → **key decisions** (three or four, each with challenge / decision /
rationale / evidence) → **validation, delivery and iteration** ("on record" and
"not documented", side by side) → outcomes split into delivered / verified /
intended → client proof (hidden until a line is approved) → related work →
project-specific CTA. Sections are optional; a project without a given record
omits the section.

### ManaGEM product page

Gains the workflow diagram and a six-still walkthrough from the ManaGEM video,
and a results block that says exactly which single figure is confirmed and that
nothing else has been measured.

### Supporting pages

- **Solutions.** Every service page lists the case studies that demonstrate it
  (one to three cards, "Where this has run") and opens with *Discuss a project*.
- **Insights.** Each article links the case study its argument comes from.
- **Our Story.** The founding section links through to the case studies; the
  closing invitation matches the rest of the site.
- **Contact.** The heading is *Discuss a project*; the submit button says *Send
  the enquiry by email*, which is what happens (see §3).
- **Navigation.** *Insights* joins the primary nav; every enquiry CTA on the site
  reads *Discuss a project* and leads to `contact.html`.

### Assets

37 stills were extracted from the seven case study videos into
`assets/img/cases/<slug>/` (30–68 KB each, lazy-loaded). They are captioned
"Illustrated in the case study video" wherever they appear, so an illustration
is never presented as a production screenshot. To regenerate one:

```sh
ffmpeg -ss <seconds> -i assets/video/case-studies/<stem>_web.mp4 -frames:v 1 \
  -vf scale=1200:-1 -q:v 4 assets/img/cases/<slug>/<nn>-<key>.jpg
```

The scene times used, checked against a contact sheet of each video:

| Case | Video | Stills and seconds |
|---|---|---|
| `sbs-waterproofing` | `SBS_explainer_web.mp4` | 01-enquiry @ 26.6s, 02-pipeline @ 34.6s, 03-deposit @ 46.6s, 04-profit @ 50.6s, 05-stock @ 54.6s, 06-system @ 62.6s |
| `wastemart` | `WasteMart_explainer_web.mp4` | 01-quote @ 30.6s, 02-payment @ 42.6s, 03-schedule @ 50.6s, 04-collection @ 66.6s, 05-overview @ 74.6s |
| `homeassist` | `HomeAssist_explainer_web.mp4` | 01-intake @ 14.6s, 02-dispatch @ 26.6s, 03-updates @ 38.6s, 04-evidence @ 54.6s, 05-insurers @ 66.6s, 06-overview @ 78.6s |
| `managem` | `ManaGEM_explainer_web.mp4` | 01-pipeline @ 26.6s, 02-quotes @ 34.6s, 03-profit @ 38.6s, 04-stock @ 42.6s, 05-modules @ 50.6s, 06-companies @ 54.6s |
| `trans-hex` | `TransHex_explainer_web.mp4` | 01-stabilise @ 26.5s, 02-sap-feed @ 42.6s, 03-budget @ 54.6s, 04-filter @ 58.6s, 05-forecast @ 66.6s, 06-operations @ 70.6s |
| `sonke` | `Sonke_explainer_web.mp4` | 01-capture @ 30.6s, 02-approve @ 42.6s, 03-roles @ 58.6s, 04-donor @ 70.6s |
| `tores-foundation` | `Tores_debating_platform_web.mp4` | 01-competitions @ 30.6s, 02-standings @ 42.6s, 03-claims @ 54.6s, 04-approval @ 66.6s |

### Owner's revision (same day)

After reviewing the first build the owner asked for: the hero and the stats
section restored as they were; "Selected projects" rebuilt to the Trionn
"Selected work & explorations" reference in the repository (a white band
pinned to the viewport, four large project cards travelling across as the page
scrolls, a closing "view all" panel; vertical without JavaScript, on phones and
under reduced motion, and keyboard focus scrolls a card into view); "The
thinking behind the work" made the overall thinking (the pattern every system
follows, six principles, each with the projects where it runs); then
"Capabilities, demonstrated". The featured-case-study and partnership-proof
sections were folded into these; the stories panel, how we work, the company
and the enquiry band follow as before.

### Owner's second revision

With the reference screenshots now in the repository (commit 4440697), Selected
work was rebuilt to them: a soft grey band divided into panels by thin rules,
the heading panel, four large rounded project cards each with a play button
that opens the case study video, monospace EXPLORE PROJECT links, and a closing
"view all" panel. At the owner's instruction the Client stories section (the
placeholder testimonials) returns after it, the Book a Discovery Session form
returns at the end, and the capabilities, stories-panel, how-we-work and
company sections leave the homepage. The brief's rule against invented
testimonials is therefore overridden by the owner for the homepage only;
`OPEN_ITEMS.md` tracks the placeholders.

### Owner's third revision — the section refined

Selected work was refined for alignment and consistency: the site's shared
section header; four equal-height cards on a two-column grid (one column
under 620px) inside the site's shell, each with industry, name, one-line
description, the site's arrow link and a play button that opens the video;
and the closing statement as a scroll-linked transition — small as it arrives,
scaling smoothly to full size at the centre of the viewport over the first 60 %
of a 200vh travel, held for the rest, then released with the page. No library:
about twenty lines in `home.js` set three custom properties from the scroll
position. Under reduced motion and without JavaScript the statement is static.
Verified at 360, 390, 768, 1024, 1440 and 1440×700: cards level on every row,
the statement centred at every step, no overflow, no console errors.

### Owner's fourth revision

The owner chose the horizontal scrolling design over the grid: the pinned
band from the second revision returns as it was, on a pure white ground
instead of the grey gradient. The grid and the scroll-linked statement were
removed again.

### Owner's fifth revision — the refinements on the horizontal travel

The horizontal scrolling effect stays, and the refinement brief is applied to
it: the site's shared section header above the band; four equal-height cards
in the site's card style (industry, name, one-line description, arrow link,
play button) two to a screen on desktop, one to a screen between 901 and
1100px, on a two-column grid on tablets and one column under 620px; the first
card aligned to the content shell and the last pair resting on it at the end
of the travel; card width capped by viewport height so the row always fits;
pure white ground; and the transition statement scaling up to the centre of
the viewport, holding, then releasing. Verified at 1440×900, 1440×700,
1280×800, 1024×768, 768×1024, 390×844 and 360×640, on an iPhone profile with
wheel scrolling, under reduced motion, without JavaScript, and by keyboard.

### The operating logic (Fable 5.2.1 brief)

"The thinking behind the work" was rebuilt as **The operating logic**: a dark
editorial band between Selected work and the Discovery form. The hero
photograph sits under a near-black graphite scrim (the site's photographic
ground rule, darkened), type is warm white and silver, and the site's light
blue is the one accent. The opening carries the label GEMIS / OPERATING
PRINCIPLES and "Seven systems. The same four decisions." with "four decisions."
as the accent anchor. The four principles sit on an asymmetric two-by-two
(7/5 then 5/7 columns, the right-hand pair dropped), each with a ghost index,
a solid index with a hairline, the statement, the supporting copy, a SEEN IN
row of chapter links, and an abstract line motif (a line breaking and
reconnecting in a field; a point travelling into a record, OFFLINE → SYNCED;
two paths joining; layers extending from a 2015 outline). Every statement and
line of copy is verbatim from the brief, verified by a string check against
the rendered page.

Motion: one SVG line is built from the real positions of the four index nodes
and the endpoint (orthogonal route 1 → 2 → 3 → 4 → end), drawn with a dash
offset that follows the band's progress through the viewport; a principle
becomes active when the line reaches its node (and on hover or focus), which
lights its node and resolves its motif through CSS transitions; the line ends
at a single point above the insights footer, the bridge into Discovery.
Reveals use the site's `data-reveal`. An IntersectionObserver gates the scroll
handler so nothing runs offscreen; `requestAnimationFrame` coalesces scroll
events. Under reduced motion CSS shows everything resolved and the script only
builds the path; without JavaScript the band is complete and static. Narrow
screens (≤900px) stack the principles on a vertical spine whose accent fill
follows the same progress.

Links: SEEN IN resolves to the existing chapter pages (`work/sbs-waterproofing/`,
`work/wastemart/`, `work/sonke/`, `work/homeassist/`, `work/tores-foundation/`,
`work/trans-hex/`, `products/managem/`) with the chapter names as labels; the
footer links the three published articles by their real titles. The page has no
in-page `#sbs-waterproofing` / `#wastemart` anchors, so the brief's fragment
ids were resolved to those pages rather than invented.

Verified at 1920×1000, 1440×900, 1024×768, 768×1024, 390×844 and 360×640:
progress and active states sequence 1 → 2 → 3 → 4 at every size, all 14 links
reachable by keyboard with a visible accent focus ring, hover activates a
principle, no horizontal overflow, no console errors; reduced motion and no-JS
show the resolved static band. Reference browsing (Awwwards, Godly,
Pinterest) was not available in this environment; the design was developed
from the brief's direction.

### Owner's harmony pass

The menu reads in the brand navy once the bar is stuck, solid or open, on
every page. The Selected work cards take the navy of the buttons with white
type and the light blue for their small label. The operating logic now sits on
the site's type steps (display for the opening statement, lead for the
principle statements, copy and eyebrow elsewhere), with the ghost numerals
reduced. "In their words" moved after The operating logic and takes the
Client stories stage the owner chose (names on the left, one quotation at a
time, a link to the founding client's story); it stays hidden on the live
build until `endorsements.md` arrives and shows its layout under `?review=1`.

### Owner's second harmony pass

The owner reversed two of the previous day's choices and corrected the order:

- The Selected work cards are white again on the pure white band; the navy
  stays on the menu and the buttons.
- The order is now Selected work → **In their words** → **The operating
  logic** → Book a Discovery Session. In their words is shown on the live
  build with the italic "Quotation to follow." (`.cs__pending`, a hideable
  TBC) on each slide until `endorsements.md` arrives, at the owner's
  instruction; the names, titles, "Client since 2014" and story links are
  real.
- The operating logic sits on the brand navy: the hero photograph under the
  standard `band-ink` scrim, white type, the title on `--fs-display` like
  every other section heading.
- The spacing after the transition statement matched no other section: the
  band kept its own bottom padding under the pin, and the earlier override
  targeted `.selw.band` while the section carries only `.selw`, so it never
  applied. The band's bottom padding now lives on the pin itself
  (`.selw__out-pin`, symmetric while pinned so the statement stays centred);
  when the pin releases the statement's link is exactly `--sec-y` from the
  next section (112px at desktop, 72px on a phone — the same as every other
  section boundary on the page), measured with `window.scrollTo` at 1440×900,
  1440×700 and 390×844.

Checks re-run after the pass: links 2,032 / 0 broken; axe 0 serious or
critical across every page; 14 pages × 4 widths with no overflow, clipping or
JS errors; reduced motion and no-JS; the functional sweep (overlay from a
card, the stage's tabs, nav links, tab order); chrome `--check`; the
standalone bundle rebuilt (19.4 MB, 29 pages, 72 assets, 7 videos).

### The endorsements arrive

The owner supplied the three quotations in chat on 2026-10-22. They are in
`scripts/endorsements.md` under each person's name, and `stories.py` reads
them character for character (the loader needed its missing `import re`,
which the empty-file path had never exercised). Verified by extracting the
text of each built page and counting the exact string: Keshan Patel on the
home and the HomeAssist outcomes; Ryan Smith on the home, the SBS 2014
chapter and the ManaGEM origin block, which now carries "Where the SBS
relationship began:"; Philippine Francke on the home. The homepage keeps the
order the earlier brief set (Keshan, Ryan, Philippine). The three
`endorsement-*-line` ids are out of the TBC table and `OPEN_ITEMS.md`; Nazier
Mathinus's stays, with no card on the WasteMart page. "Quotation to follow."
no longer appears anywhere on the live build. Checks after the change: links
2,033 / 0 broken; axe 0 serious or critical; layout sweep clean; functional
sweep clean; chrome `--check` clean; check-tbc with no blocking change.

### Owner's third harmony pass

- **The menu bar turns navy on scroll.** `.is-stuck` (and an open drop-down)
  now sets the bar's ground to `--navy-deep` with the wordmark, links,
  underline and burger in white, on every page; the contact and privacy
  pages keep their paper bar at the top and turn navy once scrolled. The
  drop-down panel stays paper under the navy bar. Under 900px the paper
  drawer slides under a cleared bar, so the wordmark and burger read navy on
  it as before.
- **The Selected work travel has inertia.** The track no longer sits at the
  exact scroll position: each frame it closes 11 % of the distance to where
  the scroll says it should be, so a flick glides to rest and a slow scroll
  feels weighted; the loop runs only while there is distance left. Each
  card's picture drifts against the direction of travel as it crosses the
  screen (`--hs-d`) and leans with the speed (`--hs-v`). Keyboard focus and
  resize snap. The transition statement eases the same way. Reduced motion
  still gets the static grid.
- **White closing bands, navy footer.** Get started on the home, the
  conversion band on the case study pages and the endnote on the service and
  Our Story pages are white with ink type and navy buttons, so every page
  ends paper → the navy footer. The footer is `--navy-deep` with white type.
- **The footer columns make sense now.** Solutions lists all nine services;
  Products is ManaGEM (the site's own page, not the external link), Design
  Studio, Technical Academy and All products; Company is Our Story, Case
  Studies, Insights, Industries and Contact; the privacy policy sits on the
  legal line beside the copyright. The "Support & Resources" column, which
  mixed company pages with one service and the policy, is gone.
  `apply-chrome.py` carries the columns and the legal line and applies them
  to every page at any depth.

Checks: links 2,149 / 0 broken; axe 0 serious or critical; 14 pages × 4
widths clean; functional sweep (overlay, stage, nav, tab order) clean; the
statement-to-next-section spacing unchanged; chrome `--check` clean.

### The footer, from the efferd footer-3 block

The owner asked for the `@efferd/footer-3` shadcn block. The sandbox's
network policy denies efferd.com and the site has no React or Tailwind, so
the owner pasted the block's source and it was ported by hand into the
site's own chrome: the block's structure (brand column; four link sections,
the last with icons; a gradient hairline; a centred copyright), its rounded
top corners, its top-centre glow and blurred hairline, and its reveal (each
section blurs in from 4px and 8px above over .8s, a tenth of a second after
the last). Expanded from the block's 1024px container to the site's shell
width, on the navy ground. Content is the site's real links only: Solutions
(nine), Products, Company, Connect (LinkedIn, gemis.co.za, email) — no
Facebook, Instagram or YouTube, which the block lists as placeholders.
`apply-chrome.py` now replaces the whole footer on every page; `site.js`
marks `<html>` with `has-js` so the blur reveal cannot strand a page without
scripts. Checks: links 2,149 / 0 broken; axe 0 serious or critical; 14 pages
× 4 widths clean; reduced motion and no-JS show the footer at once; chrome
`--check` clean; standalone rebuilt.

## 2. Decisions worth knowing

| Decision | Why |
|---|---|
| **Brand tokens unchanged.** The brief's palette and fonts were not adopted. | They are not in the repository; the owner chose the hero-photograph system in this project's history (PR #71, #83, `IMPLEMENTATION_NOTES.md` §1). The brief defers to a more recent approved system. |
| **Testimonials removed.** | Rule 1 of the brief. The owner's earlier instruction to invent them is superseded; `TESTIMONIALS` stays in the data file, unrendered, for approved quotes. |
| **Nav labels adapted:** *Our Story* and *Contact* rather than *About* and *Start a Project*. | The page names are owner decisions (PR #85); the brief allows adapting to site conventions. *Insights* was added as the brief asks. |
| **Hero keeps the photograph, no product mock-up.** | The owner's instruction in PR #83 ("no image mockups in any hero") is more recent and specific than the brief's "authentic project assets" line; the first substantive section below the hero is the featured case study. |
| **Form stays `mailto:`.** | It is the intended production behaviour of a static Pages site; the page says so and never claims a message was sent. |
| **Team titles still hidden.** | The 2025 company profile in the repository states them, but the owner's PR #85 instruction was "tbc unless facts.md confirms". One line in `facts.md` publishes them. |
| **Phone number hidden; WasteMart year not published; ManaGEM 2013/2026 not published.** | Unchanged from PR #85, for the reasons in the audit register. |
| **No new metrics.** | The only numbers on the new sections are the three facts.md figures, the two client-confirmed results, and the video's own statements (40 countries, 24 schools, 430+ learners), which are attributed to the case study, not claimed as outcomes. |

## 3. Tests performed

| Check | Result |
|---|---|
| `python3 scripts/apply-chrome.py --check` | every page matches the canonical header and footer |
| `node tools/check-links.mjs` | 2,092 internal links, **0 broken** |
| axe-core, serious/critical, every corporate page | **0** |
| Layout sweep, 14 pages × 375 / 768 / 1024 / 1440 | 0 problems (no overflow, no clipped text, no JS errors) |
| Overflow and JS errors, 20 pages × 360 / 620 / 900 / 1920 | clean at every width |
| Reduced motion | no `[data-reveal]` left hidden |
| JavaScript off | all content readable; videos present with native controls |
| Case Studies filters | 6 → 1 (mining) → 0 (mining + field operations, with "0 projects shown") → cleared to 6 |
| Video overlay | opens from a card and from the homepage feature with the right source; closes on Escape and returns focus |
| Stories stage | live, tabs and controls working |
| Keyboard order on the home | skip link → logo → nav → hero CTAs → first card's actions, all visible focus |
| Nav targets | all 22 primary nav links resolve to existing pages |
| `node scripts/check-tbc.mjs` | 28 hideable items (absent live, visible at `?review=1`); the **two pre-existing blocking items remain**: `managem-trial-url`, `timeline-order` |
| Standalone bundle | rebuilt (29 pages, 19.4 MB, the stills included) and smoke-tested in a browser: frame navigation, founding tags, no console errors |

Not measured in this session: Lighthouse / Core Web Vitals on the new homepage
(the sandbox has no network throttling harness wired up). The page adds 12
lazy-loaded stills (≈0.5 MB in total) and no new scripts; the video thumbnails it
already used are unchanged.

## 4. Still awaiting the owner

| Item | Where | What clears it |
|---|---|---|
| ManaGEM free-trial URL | `managem-trial-url` (blocking) | the URL, or "none" |
| Timeline order (Tore's 2014 after 2017/2018) | `timeline-order` (blocking) | confirm the running order or the year |
| Phone number | `phone-number` | the number, in `facts.md` |
| Team titles and surnames | `team-titles` | one line in `facts.md` confirming the 2025 profile's roles |
| Microsoft Partner designation and badge artwork | `microsoft-partner-badge` | the designation |
| Endorsement lines (Ryan Smith, Keshan Patel, Nazier Mathinus) | `endorsement-*` | approved wording, title, permission |
| Client logos permission | `logo-*` | confirmation the supplied marks may be shown |
| SmartStart, SwiftMLS, FINOS, RentFlow, NuraCoach, Lungelo, HashTopic | `entry-*-status` | client system or concept; GEMIS's role; permission |
| Sonke and Tore's current status | — | whether the systems remain in use |
| "Two working days" response commitment | contact copy | confirm it is the commitment |
| Approved testimonials | `TESTIMONIALS` | replace the unrendered placeholders and wire a render back in only then |

## 5. Known issues and notes

- The studio (`/studio/`) was not touched; its pages still carry the device
  mock-ups, which are appropriate there.
- The loose files at the repository root (design references, mock-ups, old
  exports, the two PDFs) were left in place; none is linked from the site.
- `industries.html` is reachable from the footer only and still describes
  "multi-company" operations from the old copy; it was given the new CTA wording
  but not rewritten.
- The standalone bundle grew from 16.9 MB to 19.4 MB with the stills.

## 6. Files

- Docs: `docs/REDESIGN-AUDIT.md`, `docs/REDESIGN-REPORT.md`, `CLAUDE.md`, `OPEN_ITEMS.md`
- Data: `scripts/cases.py` (`DETAIL`, `MANAGEM`), `scripts/stories.py` (unchanged)
- Generators: `scripts/build-home.py` (rewritten), `scripts/build-pages.py`,
  `scripts/build-other.py`, `scripts/build-services.py`, `scripts/build-stories.py`
  (helpers `flow`, `walk`, `decisions`, `cap_label`, `cscard`), `scripts/apply-chrome.py`
- Styles: the "CASE-STUDY-LED REDESIGN" block at the tail of `assets/css/site.css`
- Pages: `index.html`, `contact.html`, `404.html`, `industries.html`, and every generated page
- Assets: `assets/img/cases/**` (37 stills); `gemis-site-standalone.html` rebuilt
