# Open items

What is still outstanding on branch `site-update/gemis-stories`, in two kinds.

`node scripts/check-tbc.mjs` sorts them using `scripts/tbc-kinds.json`, which is
generated from `scripts/stories.py`. It **fails only on blocking items** and lists
hideable ones as a warning, so the branch can merge while content is still coming
as long as nothing on the live build would be *wrong*.

- **Blocking** — publishing it would be incorrect, not merely incomplete.
- **Hideable** — publishing without it is fine. It is **absent from the live
  build**, replaced by a fallback that looks deliberate, and visible only at
  `?review=1`.

Everything confirmed in `scripts/facts.md` has been
applied and is no longer listed here.

---

## Placeholders the owner asked for — 2

These are on the live build **by instruction**, not by the publish-safe rule.
Replace them before the site is presented as fact.

### `testimonials-placeholder`

The homepage "In their words" section carries **six invented testimonials** —
South African names, roles and wording written to stand in until approved
quotes arrive. None of the people exist and no company is named. The owner
asked for them explicitly ("please for now use south africa names, invent the
wording"). They live in `scripts/services.py` → `TESTIMONIALS`; replace each
entry with an approved line and rebuild with `python3 scripts/build-home.py`.

### `microsoft-partner-badge`

The hero carries a "Microsoft Partner" line with the four-square mark drawn
inline, at the owner's instruction ("please keep them"). `facts.md` does not
confirm the partnership, so the line is also registered as a hideable item: it
stays on the live build, and `?review=1` marks it "designation to confirm". The exact partner designation (for example
"Solutions Partner" or "Cloud Solution Provider") and the official badge
artwork from Partner Center have not been supplied; swap them in when they are.


## Blocking — 2

### `timeline-order`

Tore's Foundation is now **2014**, which places it after Trans Hex (2017) and
Sonke (2018) in the brief's running order. The prompt says to order the timeline
by confirmed year, and the brief fixes this order; they now disagree.

**To clear it:** confirm whether to reorder by year, or keep the brief's grouping
and label the later entries as something other than a chronology.

### `managem-trial-url`

`facts.md` confirms the free trial **is live** but gives no URL for it, and leaves
the separate ManaGEM site as "FILL". A trial CTA with nowhere to point is worse
than no CTA, so it is held back.

**To clear it:** the trial URL. (`managem-external-site` below covers whether the
page also links to the separate ManaGEM site.)

---

## Hideable — absent from the live build until they arrive

None of these stop a merge. Each has a fallback that reads as finished.

| id | What is missing | What the live build shows instead | Who |
|---|---|---|---|
| `endorsement-{ryan,kehan,nazier}-line` | The approved endorsement line, and whether it is a quote or a paraphrase | **No card at all.** The founding timeline card shows its video full-width. | Leon |
| `endorsement-{ryan,kehan,nazier}-portrait` | Portrait or 20–30s clip | — (the whole card is absent) | Leon |
| `endorsement-{ryan,kehan,nazier}-title` | Job title. Names and companies are confirmed. | — (the whole card is absent) | Leon |
| `logo-wastemart`, `logo-homeassist`, `logo-sbs-waterproofing`, `logo-trans-hex`, `logo-sonke`, `logo-tores-foundation` | Logo files, and permission to use them | The client's name set as a **wordmark** in the site's own type | Leon |
| `then-now-screenshots` | Early and current screenshots for the three founding clients | **The Then/Now block is omitted entirely** — no mock-up | GEMIS dev team |
| `team-photos` | Team photos for Our Story | The team section renders without portraits | GEMIS |
| `entry-finos-status`, `entry-smartstart-status`, `entry-rentflow-status`, `entry-nuracoach-status`, `entry-lungelo-status` | Whether each is a client system or a concept | **Not listed on Our Work.** Listing them with a "to confirm" note would publish our uncertainty. | Leon |
| `managem-external-site` | Whether `solutions/managem/` links out to the separate ManaGEM site | No secondary link | Leon |
| `eighth-video` | Whether an eighth video exists | No eighth entry | Leon |
| `standalone-bundle` | `gemis-site-standalone.html` is a review copy of the whole site; it goes stale after any change unless `python3 tools/build-site-standalone.py` is re-run | Not part of the site | Sphamandla |
| `phone-number` | `facts.md` gives no phone number; the one the old site carried (`+27 11 219 5008`) is unverified | **No phone line** in Get started; Contact says "Number to follow. Email is the quickest way to reach us." | Sphamandla |
| `team-titles` | Titles and surnames for the Our Story team other than Sphamandla Xaba (UI/UX designer, head of GEMIS Studio — confirmed) | First names only, no title line | Sphamandla |

---

## Confirmed and applied

From `facts.md`, now live on the branch:

- Product spelling **ManaGEM**; client names as written.
- **SBS Waterproofing** client since 2014, system since 2015.
- **HomeAssist** client since 2014.
- **WasteMart** "client for more than ten years" — `facts.md` has no confirmed year, so no year is published.
- **Trans Hex Group** 2017 · **Sonke Gender Justice** 2018 · **Tore's Foundation**
  2014 · **ManaGEM** described as developed from the SBS Waterproofing system of
  2015 — the 2013 launch and 2026 redesign dates are no longer published, which
  closes `chronology-2013`. *(See `timeline-order`.)*
- Executive names and companies: Nazier Mathinus (WasteMart), Kehan Patel
  (HomeAssist), Ryan Smith (SBS Waterproofing).
- Metrics, all client-confirmed and now published: WasteMart "six hours a week
  back, per depot"; ManaGEM "month-end close: nine days to two"; "50+ systems
  delivered"; "5+ sectors".
- Footer now links the **GEMIS company LinkedIn page**, replacing the personal
  profile.
- Design tokens: the repository's own, confirmed as the intent. No value from the
  brief's palette was introduced — verified by grep.
