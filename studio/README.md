# /studio/ — how this page is built

`studio/index.html` is **generated**. Do not edit it.

| File | What it is |
|---|---|
| `src/index.html` | The authored page. This is the Design Canvas export, with the `<x-dc>` template and the component script. **Edit this.** |
| `index.html` | Generated. The fully rendered page, served to visitors. Contains no `{{ }}`. |
| `assets/dc-template.js` | Generated. The `<x-dc>` template, as a JavaScript string. |
| `assets/dc-boot.js` | Hand-written. Hands the template back to the runtime at load time. |
| `assets/dc-runtime.js`, `react.js`, `react-dom.js` | The Design Canvas runtime, unmodified. |

## Rebuilding

```sh
node tools/build-studio.mjs
```

Run it after **any** edit to `src/index.html`, and after any new export from
Design Canvas. It needs Playwright's Chromium; set `PLAYWRIGHT_MODULE` if
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
