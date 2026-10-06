# GEMIS® — corporate site

The public site of GEM Information Systems, built around one object: a procedural
cut stone that is whole when a business runs on one system and fractures into four
shards when it does not. Static HTML, CSS and ES modules — no framework, no build
step, no analytics, nothing loaded from a third party.

The design studio's site lives in `studio/` and has its own `README.md`.

## Run it

Any static file server from the repository root:

```bash
python3 -m http.server 8080
# open http://localhost:8080/
```

The ES modules need `http://`, not `file://`. Everything degrades: with scripts
off or `prefers-reduced-motion` set, every page is complete and still, and the
gem is shown as a still image.

## Structure

```
index.html, about.html, …       the pages, one file each
assets/css/tokens.css           colour, type scale, rhythm, motion — loaded before site.css on every page
assets/css/site.css             every component, including the gem system (search "THE GEM SYSTEM")
assets/js/site.js               nav, mega menu, reveals, accordion, filters, form hand-off (classic script)
assets/js/motion.js             shared easings, line splitting, reveals, magnetic buttons, spine, page wipe
assets/js/common.js             behaviours every page shares; mounts the gem only when WebGL and motion are allowed
assets/js/home.js               the home page: fracture, estimator, reassembly, services stage, form
assets/js/page.js               every other page's signature moment (timeline, services stage, module tour, …)
assets/js/gem.js                the stone: three.js, procedural, four wedges, whole / fractured / small / missing
assets/js/three.module.min.js   three r185 (+ three.core.min.js), gsap.min.js, ScrollTrigger.min.js, lenis.min.js — vendored
assets/img/gem/*.png            the gem's stills: the reduced-motion and no-WebGL fallbacks, and the first paint on phones
assets/img/**                   brand facet images (generated, see tools/facets)
assets/fonts/                   Archivo (width axis) and JetBrains Mono, self-hosted
design/art-direction.html       palette, type scale, the gem's key frames, sitemap with each page's signature moment
design/gem-states.html          harness that renders the gem's states; used by tools/gem-stills.mjs
tools/                          generators (below)
```

## Regenerate things

| What | Command |
| --- | --- |
| Gem stills (`assets/img/gem/*.png`) | `python3 -m http.server 8079 --bind 127.0.0.1` in one shell, then `node tools/gem-stills.mjs` (Playwright Chromium + Python Pillow) |
| Brand facet images | `python3 tools/facets/gen.py && node tools/facets/render.mjs` |
| The whole corporate site as one HTML file | `python3 tools/build-site-standalone.py` → `gemis-site-standalone.html` |
| The studio site | `node tools/build-studio.mjs` |

The single-file build carries every page, stylesheet, script, font and image in one
document. It does not carry three.js: the gem is shown as its stills there.

## Conventions

- Colour, type and spacing come from `tokens.css`. Components never invent a value.
- One blue, `--signal`, means "live": the active thing, focus, the packet of data.
- Motion is scroll-driven or state-driven; nothing loops forever, and every loop
  pauses when out of view. `prefers-reduced-motion` turns it all off.
- Nothing on the site is invented: no clients, figures, testimonials or
  certifications that are not in the repository already. Provisional content is
  marked `CONTENT-TODO` in the markup and listed in `CONTENT-TODO.md`; the product
  recreations are marked `TODO: validate against the live product`.
