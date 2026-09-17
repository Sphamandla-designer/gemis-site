# CONTENT-TODO

Every placeholder shipped in the markup, and why. Each one renders in the existing
style and is wrapped in an `<!-- CONTENT-TODO: ... -->` comment at its location.

Nothing in this list was invented. Where real content was needed and none existed in
the repo, a placeholder was inserted rather than a plausible-sounding fabrication.

---

## 1. Homepage — case study outcomes (`index.html`, Proof section)

| Placeholder | Location |
|---|---|
| `[PLACEHOLDER: measurable outcome, e.g. hours saved per week]` | ManaGem story card |
| `[PLACEHOLDER: measurable outcome, e.g. hours saved per week]` | WasteMart story card |

The brief asked for an outcome line above each case study's feature bullets. The repo
contains no measured outcomes for either platform — no hours saved, error rates,
throughput or cost figures. **Needs a real, defensible number from the client
engagement.** Uses the existing `.story__k` text style.

## 2. Homepage — client logo row (`index.html`, Proof section)

Six `[PLACEHOLDER: client name]` entries in the marquee.

The brief asked for a client logo row "using an existing image-row/marquee pattern if
one exists". **No image-row pattern exists in the codebase.** The only marquee is
`.mq` on the case studies page, which is text-based, so that was reused and filled
with placeholders. Real client names in `assets/img/logos/` (AX-Channels, NeuraUX,
KiY Trucking, CMaxx) were **not** used, because there is nothing in the repo
confirming they consent to being listed as clients on the homepage.

**Decision needed:** confirm which clients may be named, then either swap the text in
or supply logo files and ask for an image-row pattern.

## 3. Industries — further sectors (`industries.html`)

`[PLACEHOLDER: further sector]` plus problem and solution lines.

Only three sectors are included, because those are the only ones the site currently
evidences with delivered work: NGOs (Sonke Gender Justice), waste and field operations
(WasteMart), and multi-company business/finance operations (ManaGem). Add a fourth
only when there is a case study to link to.

## 4. Insights — the whole page (`insights.html`)

Three placeholder cards, plus `[PLACEHOLDER: intro line for the insights index]`.

**This page is hidden from the navigation.** The gate is a single constant:

```js
// assets/js/site.js
var SHOW_INSIGHTS = false;
```

Set it to `true` once real articles exist. The nav item is `<li data-nav="insights" hidden>`
on every page; the flag unhides it. Leave it `false` until the placeholder cards are
replaced — shipping it visible would put three empty articles in the main navigation.

## 5. Privacy notice — field list is now out of date (`privacy.html`) ⚠️

**This one is a correctness issue, not a placeholder.**

`privacy.html` states the enquiry form collects:

> your name, work email address, company name, the service you are interested in, your
> indicative budget band, and your message

The Discovery Session form that replaced it collects **name, work email, company, what
you're looking to do, rough timeline, and notes**. There is no budget band and no
service field any more.

The "What we collect" section of the privacy notice must be updated to match before
launch. It is a POPIA notice, so it is not something to reword on a guess — it needs
whoever owns that copy to approve the new wording.

Note also that `privacy.html` still carries its own **DRAFT — pending approval** banner.

## 6. Consent checkbox added beyond the brief's field list

The brief's Discovery form field list did not include a consent checkbox. One was added
anyway, reusing the existing `.consent` markup, because `privacy.html` states that the
form "asks for your explicit consent before submission" and that "your consent is
recorded with your enquiry". Shipping a form that collects personal information without
it would contradict the published notice.

Remove it only if the privacy notice is changed to match.

## 7. Studio social profiles (`studio/index.html`) ⚠️

The footer and the slide-out menu listed LinkedIn, Dribbble, Behance and Instagram as
plain text — they were never links. They are links now:

| Profile | Href |
|---|---|
| LinkedIn | `https://www.linkedin.com/in/sphamandla-xaba-ba1602287/` — the URL the corporate footer already uses |
| Dribbble | `#` placeholder |
| Behance | `#` placeholder |
| Instagram | `#` placeholder |

**Needs the three real profile URLs.** Until then those three links go nowhere.

One deliberate deviation from the brief: the placeholders do **not** carry
`target="_blank"`. On an `href="#"` that would open a blank second copy of the studio
page in a new tab. Add `target="_blank" rel="noopener"` at the same time as the real
URLs — the LinkedIn link already has both.

## 8. The studio enquiry form does not submit anywhere ⚠️

`submitForm` in `studio/index.html` is:

```js
const submitForm = (e) => { e.preventDefault(); this.setState({ sent: true }); };
```

It shows the visitor a success state — "Received. Reply within 2 working days" — and
**discards what they typed**. Nobody at GEMIS ever sees it.

The brief's hosting constraint says to keep the existing submission mechanism and flag
it rather than change it, so it is untouched. It needs a decision before launch. On
static hosting the options are a `mailto:` hand-off (what the corporate Discovery form
does), or a third-party form endpoint.

## 9. Studio mobile layout ⚠️

Not a content item, but it belongs with the launch blockers. At 390px the studio page
has no mobile layout: the services ladder, Selected Work, Alternatives, the enquiry
form and the contact footer all run past the right edge of the viewport and are
clipped by their sections' `overflow:hidden`, so the content cannot be reached at all.
The same measurement against the page as uploaded returns an identical list, so this
is the design as delivered, not something introduced here. Fixing it means writing a
responsive layer for the studio, which is a change to the look at mobile widths and so
outside this brief's constraints.
