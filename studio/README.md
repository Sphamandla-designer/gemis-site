# /studio/ — how this page is built

`studio/index.html` is **generated**. Do not edit it.

| File | What it is |
|---|---|
| `src/index.html` | The authored homepage. This is the Design Canvas export, with the `<x-dc>` template and the component script. **Edit this.** |
| `src/work.html` | The authored listing page — its own content plus slots the build fills from the homepage. **Edit this.** |
| `index.html` | Generated. The fully rendered homepage, served to visitors. Contains no `{{ }}`. |
| `work.html` | Generated. The listing page. No runtime, no `{{ }}`. |
| `assets/dc-template.js` | Generated. The `<x-dc>` template, as a JavaScript string. |
| `assets/dc-boot.js` | Hand-written. Hands the template back to the runtime at load time. |
| `assets/dc-runtime.js`, `react.js`, `react-dom.js` | The Design Canvas runtime, unmodified. |

## Rebuilding

```sh
node tools/build-studio.mjs
```

Run it after **any** edit to `src/index.html` or `src/work.html`, and after any
new export from Design Canvas. It writes both pages, or neither. It needs Playwright's Chromium; set `PLAYWRIGHT_MODULE` if
Playwright is not at the default path in the script.

The script fails rather than writing a broken page if a binding does not
resolve, if the component throws while rendering, or if any `{{` survives into
the output.

## Why

The page is a client-rendered Design Canvas component. Before this, the served
HTML contained the template — `{{ activeStep.price }}`, `{{ w.name }}`,
`{{ rotator }}` — so crawlers, link previews and anyone without JavaScript got
placeholder syntax instead of the pricing ladder, the case studies and the
comparison table.

The build renders the page in a headless browser exactly as a visitor's browser
would, then writes the result into `index.html` inside
`<div id="dc-prerender">`. At load time `dc-boot.js` runs during parsing,
swaps that static markup for the `<x-dc>` element the runtime expects, and the
runtime takes over as before — so the interactive page is the same component it
always was, and nothing is ever on screen twice.

With JavaScript off, neither script runs and the static markup simply stays.
A small stylesheet in `<head>` makes that copy readable: it reveals the
scroll-reveal elements and shows all four ladder steps and all five comparison
panels at once, since without JavaScript there is nothing to switch between
them. That stylesheet only ever applies inside `#dc-prerender`, which is gone
before anything is painted when scripts do run.

## studio/work.html

The listing page behind "View all projects". It carries **no runtime at all** —
no React, no dc-runtime — which is why it scores 100 on Lighthouse performance
where the homepage scores 64.

`src/work.html` holds only what is unique to it: the head, the page heading, the
three projects the homepage does not carry, and twenty lines of script for the
menu. Everything else is slotted in at build time out of the homepage that was
just rendered, so the two cannot drift:

| slot | filled with |
|---|---|
| `<!--#studio-css-->` | the homepage's `<style>` blocks — fonts, keyframes, the mobile layer |
| `<!--#header-->` | the rendered `<header>`, including the fixed action pill |
| `<!--#drawer-->` | the rendered `#studioMenu`, captured open and then shut |
| `<!--#contact-->` | the rendered closing band |
| `<!--#cards-->` | one work card per project, in the homepage's own card markup |

The three projects on the homepage carousel are read out of that carousel, not
copied — change a name or a description in `src/index.html` and the listing
follows on the next build. The other three live in the `extra-projects` JSON at
the foot of `src/work.html`, each with a `source` field saying where its content
came from.

Every in-page link in the lifted chrome is rewritten from `#enquire` to
`index.html#enquire`, since on this page those sections are elsewhere. The build
fails if a slot is left unfilled, if a lifted part is missing, if the header
stops having exactly one button, or if the drawer stops being shuttable.

## The mobile layout

The export had no breakpoints, so below about 900px its two-, three- and
four-column grids kept their desktop track sizes and whole sections ran off the
right edge, clipped by their own `overflow:hidden`. The layer that fixes that
lives at the end of the page's `<style>` block in `src/index.html`, in two
queries: **900px** for the grids and **700px** for the header.

It hangs off `data-m` hooks in the markup, **not** substring matches on the
`style` attribute. That matters: the browser rewrites an inline style — what you
author as `repeat(3,minmax(0,1fr))` comes back as
`repeat(3, minmax(0px, 1fr))` — so `[style*="…"]` selectors look correct and
silently never match.

| hook | what it is | at ≤900px |
|---|---|---|
| `head` | two-column section headings | one column |
| `split` | the ladder, Alternatives, the enquiry form, the footer | one column |
| `cards` | the three rule cards, the work grid, the four reasons | one column |
| `fields` | the form's paired inputs | one column |
| `spec` | the label/value rows in a ladder panel | label above value |
| `tab` | a ladder tab's number / name / duration | duration wraps under |
| `rail` | the two sticky asides | static |
| `about2` | the About split, which had `margin: 80px 8%` | full width |
| `wide` | the Alternatives section's 10% side padding | 18px |
| `note` | the pricing note placed at `left:180px; top:160px` | in flow |
| `rightrow`, `footcol` | things aligned to the right of a column | aligned left |
| `rules8` | the eight decorative footer columns | four |
| `data-desk` | the corporate link and the pill's 150px slot | hidden at ≤700 |
| `data-cta` | the fixed "Book a teardown" pill | a bar across the bottom, at ≤700 |

`tools/build-studio.mjs` checks every hook the stylesheet asks for is present in
the rendered page and **fails the build** if one is missing, so an export that
drops them cannot ship a broken phone layout quietly.

## After a new Design Canvas export

A new export overwrites `src/index.html` and will drop the accessibility work
that lives in that file. Re-apply, then rebuild:

- `lang="en"` on `<html>`; the `<meta name="robots" content="noindex">` that
  keeps this source file out of search results (the build strips it)
- the skip link, the `<header>` and the `<main id="main" data-motion>` wrapper
- the accessibility block at the end of the page's own `<style>`: `.dc-vh`,
  `.dc-skip`, `scroll-padding-top`, `:focus-visible`, and the marquee
  pause rules
- the complete `<h1>` text with the rotator as `aria-hidden` decoration, and
  the motion control beside the hero CTAs
- `role="tablist"/"tab"/"tabpanel"` plus arrow keys on the services ladder and
  on Alternatives, and the panel lists that put every step and every
  comparison in the DOM
- `aria-expanded` / `aria-controls` on the menu button, `aria-hidden` on the
  clock and on the decorative marquee
- capitals written as sentence case with `text-transform: uppercase`
- the mobile layer and its `data-m` hooks — the build will tell you which are
  missing, and the table above says where each one goes
