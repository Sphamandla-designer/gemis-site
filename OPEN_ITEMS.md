# Open items

Every unconfirmed fact on branch `site-update/gemis-stories`, marked in the HTML
with `data-tbc="<id>"` and rendered with a visible TBC pill.

`node scripts/check-tbc.mjs` lists them from the markup and exits 1 while any
remain. **That is the go-live gate: this branch must not merge to `main` while it
fails**, because the brief allows placeholders in the build and never on the live
site.

Owners are taken from the brief's open-items list.

## Dates

| id | Page(s) | What is needed | Who |
|---|---|---|---|
| `homeassist-start-year` | home, timeline, work, story | Start year of the HomeAssist relationship. The video confirms "more than ten years" but no year. | Leon |
| `wastemart-start-year` | home, timeline, work, story | Start year of the WasteMart relationship. Video confirms "more than ten years" only. | Leon |
| `sonke-year` | timeline, work, story | Year of the Sonke Gender Justice project. | Leon |
| `tores-year` | timeline, work, story | Year of the Tore's Foundation project. | Leon |
| `managem-launch-year` | timeline, solutions/managem | ManaGEM launch year. | Leon |

SBS Waterproofing needs no placeholder: the video confirms 2014, system from 2015.
Trans Hex is confirmed as 2017.

## Endorsements

No line is written anywhere. The brief's "theme" column is layout context only and
is never turned into a quote.

| id | What is needed | Who |
|---|---|---|
| `endorsement-nazier-line` | Approved endorsement line from Nazier Mathinus, and whether it is a direct quote or a paraphrase | Leon |
| `endorsement-nazier-portrait` | Portrait photo or 20–30s clip | Leon |
| `endorsement-nazier-title` | Job title, and confirmed spelling of the name | Leon |
| `endorsement-kehan-line` | Approved line from Kehan Patel, quote or paraphrase | Leon |
| `endorsement-kehan-portrait` | Portrait or clip | Leon |
| `endorsement-kehan-title` | Job title, and confirmed spelling | Leon |
| `endorsement-ryan-line` | Approved line from Ryan Smith, quote or paraphrase | Leon |
| `endorsement-ryan-portrait` | Portrait or clip | Leon |
| `endorsement-ryan-title` | Job title | Leon |

## Logos

None supplied. Each renders as a brand-coloured "Image TBC" block.

| id | Who |
|---|---|
| `logo-wastemart`, `logo-homeassist`, `logo-sbs-waterproofing` | Leon |
| `logo-trans-hex`, `logo-sonke`, `logo-tores-foundation` | Leon |

Permission to use each logo is needed as well as the file.

## Metrics and figures

| id | Page | What is needed | Who |
|---|---|---|---|
| `metric-wastemart-depot-hours` | work/wastemart | Client sign-off on "six hours a week back, per depot", or remove | Leon |
| `metric-managem-month-end` | solutions/managem | Client sign-off on "month-end close: nine days to two", or remove | Leon |
| `stat-systems-delivered` | our-story | Is "50+ systems" accurate? | Leon |
| `stat-sectors` | our-story | Is "5+ sectors" accurate? | Leon |

Sonke's "40 countries" and Tore's "24 schools, 430+ learners" are **confirmed** by
the video narration and carry no placeholder.

## Classification

| id | What is needed | Who |
|---|---|---|
| `entry-finos-status` | Is FINOS a client system or a concept? | Leon |
| `entry-smartstart-status` | Client system or concept? | Leon |
| `entry-rentflow-status` | Client system or concept? | Leon |
| `entry-nuracoach-status` | Client system or concept? | Leon |
| `entry-lungelo-status` | Client system or concept? | Leon |

## Screenshots and photos

| id | What is needed | Who |
|---|---|---|
| `then-now-screenshots` | Early and current screenshots for SBS, HomeAssist and WasteMart. **The "Then and now" blocks are omitted entirely** until these exist — the prompt forbids mock-ups. | GEMIS dev team |
| `team-photos` | Team photos for Our Story | GEMIS |

## Decisions

| id | What is needed | Who |
|---|---|---|
| `footer-linkedin` | Does the footer keep the personal LinkedIn profile as a designer credit, or point at the GEMIS company page? | Leon |
| `managem-free-trial` | Is a ManaGEM free trial live? The "Start a free trial" CTA is omitted until confirmed. | Leon |
| `managem-external-site` | Should `solutions/managem/` link out to the separate ManaGEM site as a secondary CTA? | Leon |
| `eighth-video` | Is there an eighth video? None was supplied, so no entry exists for it. | Leon |
| `brand-tokens` | The brief's palette and fonts are not the ones in the CSS. See `IMPLEMENTATION_NOTES.md`. Confirm the repository's tokens are correct. | Leon / Sphamandla |

## Blocking the bundle

| id | What is needed | Who |
|---|---|---|
| `standalone-bundle` | `gemis-site-standalone.html` is **stale**: it still carries the old flat site. `tools/build-site-standalone.py` models the site as flat `name.html` files at the root with `assets/…` paths, and asserts every internal link matches that shape. The new structure uses folder URLs (`work/`, `solutions/managem/`) and `../` asset paths, so the build now fails its own assertion. Teaching it nested pages is a separate piece of work; it was not half-fixed. | Sphamandla |
