# CONTENT-TODO

Every placeholder has been filled in, on request, so the site reads complete. **Some
of what is now on the page is provisional** — written to hold the layout, not
confirmed with anyone. This file is the list of what to check before launch.

Each item is marked in the markup with an `<!-- CONTENT-TODO: ... -->` comment at its
location, so you can find it from the page.

Nothing invented a client, a testimonial or an industry the site could not already
evidence. The two figures below are the only numbers that were not measured.

---

## ⚠️ Provisional — confirm or replace before launch

### 1. Two outcome figures on the homepage (`index.html`, Selected Work)

| Case study | What the page now says |
|---|---|
| ManaGem | **Month-End Close: Nine Days To Two** |
| WasteMart | **Six Hours A Week Back, Per Depot** |

**Neither figure has been measured.** They are plausible for the kind of work each
platform does, and they read correctly in the existing `.story__k` style, but they
are not evidence. Replace them with real numbers from the engagements, or cut the
line — the section works without it.

### 2. The client row on the homepage (`index.html`, Selected Work)

AX-Channels · Sonke Gender Justice · NeuraUX · KiY Trucking · CMaxx WiFi Solutions ·
Hive Creative Studio

None of these is invented — five already appear in the marquee on
`case-studies.html`, and Sonke Gender Justice is named on `industries.html`.
**What still needs checking is consent**: being listed in a case-study credit is not
the same as being named as a client on the homepage.

Supply logo files if you would rather show marks than names. There is no image-row
pattern in the codebase, so one would have to be built; the row currently reuses the
existing `.mq` text marquee.

### 3. The fourth industry (`industries.html`, row 04)

**Property & Facilities Management.** Drawn from the "Property Technology Solutions"
capability already listed on the About page, so the claim is consistent with the rest
of the site — but unlike the three sectors above it, **it has no case study behind
it**, which is why it is the only row without a "read the story" link. Either add one,
or remove the row.

### 4. News & Insights (`insights/`)

Live. Three articles, written for this site, generated from `ARTICLES` in
`scripts/services.py` by `scripts/build-services.py`; the homepage shows the
same three. Add an article there and rebuild. The old `insights.html` is a
redirect stub.

### 5. Studio social profiles (`studio/src/index.html`)

| Profile | Href |
|---|---|
| LinkedIn | `https://www.linkedin.com/showcase/gemis-design-studio` — the studio's showcase page |
| Dribbble | `#` placeholder |
| Behance | `#` placeholder |
| Instagram | `#` placeholder |

**Needs the three real profile URLs.** The `#` placeholders have been removed from
the drawer and the footer, so only LinkedIn shows until they are supplied. Add
each back with `target="_blank" rel="noopener"`, like the LinkedIn link.

Edit `studio/src/index.html`, then run `node tools/build-studio.mjs`.

---

## ⚠️ Correctness issues, not content

### 6. The privacy notice no longer matches the form (`privacy.html`)

`privacy.html` states the enquiry form collects:

> your name, work email address, company name, the service you are interested in, your
> indicative budget band, and your message

The Discovery Session form that replaced it collects **name, work email, company, what
you're looking to do, rough timeline, and notes**. There is no budget band and no
service field any more.

The "What we collect" section must be updated to match before launch. It is a POPIA
notice, so it is not something to reword on a guess — it needs whoever owns that copy
to approve the new wording. `privacy.html` also still carries its own
**DRAFT — pending approval** banner.

### 7. The consent checkbox goes beyond the brief's field list

The Discovery form's specified fields did not include a consent checkbox. One was added
anyway, reusing the existing `.consent` markup, because `privacy.html` states that the
form "asks for your explicit consent before submission" and that "your consent is
recorded with your enquiry". Shipping a form that collects personal information without
it would contradict the published notice.

Remove it only if the privacy notice is changed to match.

### 8. The studio enquiry form — now a `mailto:` hand-off

`submitForm` in `studio/src/index.html` used to show a success state and discard
what the visitor typed. It now does what the corporate Discovery form does on
static hosting: opens a pre-addressed message to info@gemis.co.za with every
field filled in, then shows the success state with a fallback address. The
Contact page (`studio/src/contact.html`) carries the same form in plain HTML
with the same hand-off; every "Book a teardown" button on the studio lands there. A
third-party form endpoint would remove the dependency on the visitor's email
client; that is still a decision to make.

**This now affects a second page.** The "Tell us the project you want built" band
on `studio/work.html` sends its five service chips and its primary action to
`mailto:info@gemis.co.za` rather than to `index.html#enquire`, precisely because
the form on that anchor discards what it collects — funnelling more people into
it would have made this worse. Once the form submits somewhere real, point that
band at `#enquire` instead and carry the chosen service through as the form's
preselected "What do you need?" value. The band's secondary link already goes
there for the teardown, which is the studio's own named offer.

### 9. One contrast failure left on the whole site ⚠️

`/studio/`'s "Book a teardown" pill: **white on `#ff1f7a` is 3.67:1**, and 13px
text needs 4.5:1. It is the last axe violation anywhere on the site — everything
else, both sites, is clean.

`#ea005f` would clear it at 4.51:1. That is a visibly deeper pink, and the pink
is a brand accent, so it is a decision rather than a fix. Two other routes:
apply the darker pink **only to this pill** and leave the accent alone
everywhere else, or take the label to 18.66px bold, at which size 3:1 is the
bar and the existing pink already passes.

The studio's other accents — `#ff7a12` on `#f5f6f8` at 2.41:1, `#9a9ba3` on
white at 2.76:1 — are small print rather than controls, and have no
hue-preserving fix either. See `qa/REPORT.md`.

### 10. The studio work page (`studio/work.html`) and the case studies

The studio now shows GEMIS's **real projects** — the six client stories the
corporate site carries (SBS Waterproofing, HomeAssist, WasteMart, Trans Hex
Group, Sonke Gender Justice, Tore's Foundation) plus ManaGEM, the product —
each with its own page, `studio/work-<slug>.html`, built from
`studio/src/cases.json`. FINOS, RentFlow, NuraCoach and Lungelo are gone (the
owner's instruction, 2026-11-09: they were not GEMIS's own projects).

Every line on those pages comes from `scripts/cases.py`, `scripts/stories.py`,
`scripts/facts.md` and `scripts/endorsements.md`. The thumbnails are
`studio/assets/cases/<slug>.jpg`, rendered by `tools/studio-thumbs.mjs` from the
app windows and phones cut from the case-study videos (`assets/img/ui/`,
sample data) mounted in a laptop and a phone — no invented screens.

Still to settle:

1. **Which service each project evidences.** WasteMart → Product Teardown and
   ManaGEM → Interface Refresh Sprint stand as before. SBS Waterproofing →
   Web Experience rests on the 2014 website and campaign work; HomeAssist →
   Embedded Designer rests on the ten-year design-and-support relationship.
   Both are flagged on their pages under `?review=1` — confirm or change them in
   `studio/src/index.html` (the ladder's `evidence:` lines) and `cases.json`.
   Trans Hex, Sonke and Tore's Foundation evidence no named service yet.
2. **The NDA level per client** (full · anonymised · results-only) is assumed
   Full, because the names and screens are already public on the corporate
   site. Agree it in writing and flip `ndaAgreed` in the JSON.
3. **Quotations**: Ryan Smith (SBS Waterproofing) and Keshan Patel
   (HomeAssist) appear, copied exactly from `scripts/endorsements.md`. Nazier
   Mathinus (WasteMart) is still outstanding; the other pages have none.

### 11. Done — no longer outstanding

Two earlier entries have been closed:

- **Corporate colour contrast.** `--ink-3` moved from `#85868a` to `#626367`.
  axe now reports zero violations on all eleven corporate pages, and Lighthouse
  Accessibility is 100 on all five target pages.
- **The studio's missing mobile layout.** Built. The page has no horizontal
  overflow and no overlapping text from 360px to 1920px, and its Lighthouse
  Accessibility went from 93 to 97. See `studio/README.md` for how the layer
  works and what to re-apply after a future Design Canvas export.

What is still open on `/studio/` is its **performance ceiling**: 2.27 MB over 24
requests, 1.83 MB of it JPEG, three images at 3000×2000, most of them CSS
backgrounds that cannot be lazy-loaded. Converting the set to WebP measures
1.77 MB → 0.97 MB. That replaces the uploaded design's assets, so it needs
your call.
