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

### 4. The Insights page (`insights.html`)

Three cards with topics, standfirsts and tags. **None of these articles has been
written.** They are outlines that show what the page will look like.

The page is still **hidden from the navigation**, behind a single constant:

```js
// assets/js/site.js
var SHOW_INSIGHTS = false;
```

The nav item is `<li data-nav="insights" hidden>` on every page; the flag unhides it.
Leave it `false` until the articles exist and each card links to one — three
outlines in the main navigation would be worse than no Insights page at all.

### 5. Studio social profiles (`studio/src/index.html`)

| Profile | Href |
|---|---|
| LinkedIn | `https://www.linkedin.com/in/sphamandla-xaba-ba1602287/` — the URL the corporate footer already uses |
| Dribbble | `#` placeholder |
| Behance | `#` placeholder |
| Instagram | `#` placeholder |

**Needs the three real profile URLs.** Until then those three links go nowhere.

The placeholders deliberately do **not** carry `target="_blank"` — on an `href="#"`
that opens a blank second copy of the studio page. Add `target="_blank" rel="noopener"`
at the same time as the real URLs; the LinkedIn link already has both.

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

### 8. The studio enquiry form does not submit anywhere ⚠️

`submitForm` in `studio/src/index.html` is:

```js
const submitForm = (e) => { e.preventDefault(); this.setState({ sent: true }); };
```

It shows the visitor a success state — "Received. Reply within 2 working days" — and
**discards what they typed**. Nobody at GEMIS ever sees it.

It was left untouched under the "keep the existing submission mechanism" constraint.
It needs a decision before launch. On static hosting the options are a `mailto:`
hand-off (what the corporate Discovery form does), or a third-party form endpoint.

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

### 10. The studio work page (`studio/work.html`) ⚠️

The page lists **six projects**, every one of them already in this repository —
nothing was invented and the grid was not padded.

| project | name from | description from | image | evidences |
|---|---|---|---|---|
| ManaGem | studio carousel | studio carousel | `studio/assets/managem.jpg` | Interface Refresh Sprint |
| WasteMart | studio carousel | studio carousel | `studio/assets/wastemart.jpg` | Product Teardown |
| FINOS | studio carousel | studio carousel | `studio/assets/finosWide.jpg` | Embedded Designer ⚠️ |
| RentFlow | services ladder | `case-studies.html` | `studio/assets/shotRentflow.jpg` | Embedded Designer |
| NuraCoach | studio `shots` data | `case-studies.html` | `studio/assets/shotNura.jpg` | **placeholder** |
| Lungelo | studio `shots` data | `case-studies.html` | `assets/img/shots/lungelo.jpg` ⚠️ | **placeholder** |

Four things to settle:

1. **FINOS is claimed by two services.** The homepage carousel says it evidences
   *Embedded Designer*; the services ladder says *Web Experience — Evidence — FINOS*,
   and gives *Embedded Designer* to RentFlow. Both are in the design as uploaded.
   The page follows the carousel, because that is where a project's own description
   lives. Decide which is right and fix it in `studio/src/index.html`.
2. **NuraCoach and Lungelo evidence nothing yet.** Both render
   `[PLACEHOLDER: service evidenced]`. The homepage line — "Every case study
   evidences a named service — never the studio in general" — is the page's own
   standard, so these two do not meet it until someone names their service.
3. **Lungelo's image lives on the corporate side**, at
   `assets/img/shots/lungelo.jpg`; every other project has a copy under
   `studio/assets/`. It loads fine, but if the studio ever moves it will break.
4. **No project detail pages exist.** "Explore project" on both the homepage
   carousel and this page links to the project's own card here
   (`work.html#managem` and so on). When detail pages exist, point them there —
   the slug is already the card id.

The three **NuraCoach / Lungelo / RentFlow** descriptions come from
`case-studies.html`, which is corporate copy about the same products. Confirm the
studio is happy to describe them that way.

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
