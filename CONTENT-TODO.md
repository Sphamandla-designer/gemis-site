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

### 9. The studio has no mobile layout ⚠️

At 390px the services ladder, Selected Work, Alternatives, the enquiry form and the
contact footer all run past the right edge of the viewport and are clipped by their
sections' `overflow:hidden`, so that content cannot be reached at all. The header
overlaps itself.

The same measurement against the page as uploaded returns an identical result, so this
is the design as delivered. Fixing it means writing a responsive layer for the studio.

### 10. Colour contrast on the corporate site

Every contrast failure traces to one token, `--ink-3: #85868a` — 3.24:1 on `--paper`,
3.39:1 on `--paper-2`, 2.73:1 behind `.frame__url`. Changing it to **`#626367`** — the
same hue, darker — clears 4.5:1 on all three and takes Lighthouse Accessibility to 100
on every corporate page. It is a design decision, so it is waiting for sign-off.

See `qa/REPORT.md` for the full measurements, including the studio's own contrast
failures, which have no hue-preserving fix.
