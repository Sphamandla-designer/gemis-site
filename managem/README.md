# /managem/ — ManaGem landing page, v1 draft

Built from the **ManaGem Landing Page — UI/UX Design Brief v1** (1 Oct 2026).
A first visual draft for Graeme to react to, not a final page.

**Visual direction:** the Flowzy reference design (`Screenshot 2026-10-01 185927.png`
at the repo root): centred hero over a lavender sky gradient, the product in a
browser frame, a highlighted "about" statement with a grey logo row, a
three-step strip, bento feature cards, a stage list beside a product shot,
three-card pricing with a segmented Monthly / Yearly toggle, a testimonial grid,
a two-column numbered FAQ and a soft lavender CTA band. Violet is the one accent.

**Product screenshots are real.** They are exported from the ManaGem prototype
(`ManaGem.html` at the repo root, signed in, 1440×900 at 2×) into
`assets/img/managem/`: the dashboard (hero), open enquiries, the enquiry with its
quote lines, Sage-synced invoices, products & pricing, current jobs, the factory
pipeline and stock control. The `-content` variants have the sidebar cropped off
for the feature cards. Re-export them when the prototype changes.

| File | What it is |
|---|---|
| `index.html` | The whole long-scroll page, all 13 blocks in the brief's order, plus the signup, demo and setup modals. |
| `managem.css` | Standalone stylesheet (does not load `site.css`). Inter, white sheet on a pale grey ground, lavender sky gradients, violet accent. |
| `managem-standalone.html` | Generated single-file build: the page with the stylesheet, script, font, favicon and screenshots inlined, and site links made absolute. Open or share it on its own. Rebuild with `node tools/build-managem-standalone.mjs` after editing the sources. |
| `managem.js` | Header state, mobile menu, flow stages and scroll pulse, industry tabs, pricing toggle, modals, forms, CTA tracking. No dependencies. |

The page is static. Open it through any file server from the repo root
(`python3 -m http.server 8000`, then `/managem/`). Fonts load from `../assets/fonts/`.

## Assumptions are marked in the markup

Anything the brief lists as unconfirmed carries `data-assume="A#"` and a
`title` saying what it is (prices [A13], add-ons [A14], customer count and
testimonials [A11], credentials [A5], contact details [A15], and so on).
The **Draft v1 · show assumptions** pill in the footer outlines every one of
them on the page. Remove the pill, the `data-assume` attributes and the
`body.show-assumptions` rule when the page goes live.

## What v2 replaces

- **Product visuals.** Real prototype screenshots are already in place. The
  customer-side "Accept quote" phone, the acceptance confirmation and the
  setup strip are mock UIs drawn in HTML, since the prototype has no customer
  view or onboarding screens yet.
- **Industry photos.** The four `.photo` panels are labelled placeholders,
  not stock photos. Real South African workshop photography goes here.
- **Testimonials, stats, team line.** Clearly labelled placeholders.
- **Forms.** The signup and demo forms validate and show a thank-you state
  but post nowhere yet. Wire them to the ManaGem endpoints, or swap the demo
  form for an embedded calendar.
- **Setup video.** The "See how setup works" modal shows a step walkthrough
  with a slot for the 60–90 second video.
- **Feature pages.** The "See more" links on the feature cards jump to the
  matching flow stage until the feature pages exist.
- **Tracking.** Every CTA has a unique `data-track` id and pushes a
  `cta_click` event to `dataLayer` (and `gtag` if present). Point this at the
  real analytics container.

## Headline variants (for A/B testing)

- A (used): "From enquiry to invoice to job card, without retyping a thing."
- B: "Quote faster. Track every job. Know what you made."
- C: "The system your spreadsheets wish they were."
