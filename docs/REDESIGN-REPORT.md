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
| Endorsement lines (Ryan Smith, Kehan Patel, Nazier Mathinus) | `endorsement-*` | approved wording, title, permission |
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
