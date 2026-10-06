# GEMIS corporate site — redesign report

Branch `claude/gemis-studio-homepage-8apw4o`. Everything below was built and measured in this
session; nothing in the content is new. Where the brief asked for something the repository
cannot truthfully supply, a `TODO:` marker is in the markup and listed at the end.

## What was built

**One object.** A procedural cut stone in three.js (`assets/js/gem.js`): a pentagon table, a
decagonal girdle and a pavilion to a point — the favicon in glass. It is built as four wedges
(Sales, Stock, Payroll, Projects) so the same stone can fracture, show one problem per shard,
and lock back together. Four states: whole, fractured, small, missing. Each state also exists
as a still (`assets/img/gem/*.png`, 9–22 KB) that stands in when WebGL is unavailable, when
`prefers-reduced-motion` is set, in the single-file build, and as the first paint on phones.

**Home page**, top to bottom: the mega menu's three live mini-visuals · hero with the whole
stone, line-by-line headline, a primary button and one quiet link · the fracture, pinned and
scrubbed, four problems each with its own shard behaviour (legacy greys, the blind spot is a
wireframe) · the workaround cost estimator, in place of the three unmeasured statistics, with
its result carried into the enquiry form · the reassembly, where the shards lock and ManaGem
rises through the stone · services with a sticky diagram stage that follows the row · a trust
bar that says only what is true · selected work as living recreations of ManaGem and WasteMart
· how we work as a loop, not a line · the enquiry form in navy with floating labels, inline
validation, two steps on a phone and a real finish · the footer with a facet rule and the
quiet wordmark · a progress spine on wide screens · a page wipe between pages (the browser's
own view transition where supported) · a first-visit loader that draws the mark, once per session.

**Every other page** has one signature moment: About, the timeline draws its line · Services,
a diagram stage follows the open discipline and the process is shown as a loop · Industries,
a pictogram per sector drawn as the row arrives · Case studies, ManaGem and WasteMart as
living recreations · ManaGem, the dashboard in the hero and a module tour where the device
follows the module you read · WasteMart, the operations view and driver app in the hero ·
Insights, typographic facet covers · Contact, a schematic of where we are (no map service) ·
Privacy, contents that follow the reader with a progress line · 404, the stone with a facet missing.

**System.** `tokens.css` (palette kept, four gem colours added, one type scale, one motion
vocabulary) · `motion.js` (easings, line splitting, reveals, magnetic buttons, spine, wipe) ·
`common.js` (shared behaviours, lazy gem mounting) · `home.js`, `page.js`. Static ES modules,
no bundler. GSAP + ScrollTrigger drive only the two scrubbed scenes; Lenis runs on pointer
devices only. Both are vendored and loaded on demand.

**Deliverables.** Source + `README.md` build notes · `design/art-direction.html` (palette,
type scale, the gem's key frames, sitemap with each page's moment) · `gemis-site-standalone.html`
(every page in one 3.3 MB file; stills instead of three.js) · `tools/gem-stills.mjs` · this report.

## Measured

Lighthouse 13.5, mobile preset (Moto G Power emulation, 4× CPU slowdown, simulated 4G), served
from a local server that gzips and caches like GitHub Pages. The container has no GPU: WebGL
runs on a software renderer, which is why the desktop number for the home page carries a
large blocking time that a real GPU would not.

| Page | Performance | Accessibility | Best practices | SEO | FCP | LCP | TBT | CLS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Home (mobile) | 81 | 100 | 100 | 100 | 1.6 s | 2.3 s | 670 ms | 0 |
| Home (mobile, WebGL unavailable) | 90 | — | — | — | 2.5 s | 3.2 s | 0 ms | 0 |
| Home (desktop, software WebGL) | 68 | 97 | 100 | 100 | 0.4 s | 0.6 s | 2 270 ms | 0 |
| About (mobile) | 81 | 100 | 100 | 100 | 1.2 s | 2.0 s | 770 ms | 0 |
| Services (mobile) | 81 | 100 | 100 | 100 | 1.6 s | 2.4 s | 640 ms | 0 |
| Case studies (mobile) | 81 | 100 | 100 | 100 | 1.6 s | 2.3 s | 650 ms | 0 |
| ManaGem (mobile) | 96 | 100 | 100 | 100 | 1.4 s | 2.1 s | 180 ms | 0 |
| Contact (mobile) | 90 | 100 | 100 | 100 | 1.4 s | 2.0 s | 380 ms | 0 |

Against the brief's budget (mobile ≥ 90 / 100 / ≥ 95 / 100): accessibility, best practices
and SEO are met on every page. Performance is met on ManaGem and Contact and sits at 81 on
the four pages with the most markup. On those pages a CPU profile shows under 100 ms of script
self-time; the blocking time is the page's first style-and-layout pass under the 4× slowdown,
attributed to whichever script triggers it. Layout shift is zero everywhere. What would close
the gap: minifying `site.css` (Lighthouse estimates 32 KB, and 81 KB of rules unused per page)
and trimming the shared stylesheet per page — both reasonable follow-ups, not done here so the
site keeps its no-build-step promise.

**Accessibility.** axe-core (WCAG 2.2 AA + best-practice rules) on all eleven pages with
transitions settled: no violations. The findings it raised during the build were fixed: heading
order in the product recreations, inactive fracture cards below 4.5:1, spine numerals, the
fracture lede, and mailto links distinguishable by underline. Every interactive element is
reachable by keyboard; focus is the one blue; `aria-live` on the estimator result and the form.

**Verified by hand (Playwright).** Every page at 375, 768, 1280 and 1920 px, with and without
reduced motion: no horizontal overflow, no console errors, no failed requests. Interactions:
mega menu minis, nav hide/show, fracture scrub, reassembly rise, estimator maths and hand-off
into the form, inline validation, the two-step phone form, the success state, the services
stage following the row and the accordion, module tour, scrollspy, the 404 stone, the
single-file build's cross-page navigation.

## Reduced motion and fallbacks

With `prefers-reduced-motion`: no gem (stills), nothing pins or scrubs, headlines simply appear,
loops do not run, the loader and the wipe are skipped, Lenis is off. Without WebGL: the same
stills, everything else alive. Without JavaScript: every page complete and readable; the
fracture cards all show; the form posts as before. On phones the still is the first paint and
the live stone arrives on the first touch or scroll, so the hero costs nothing before the visitor moves.

## Known limits

- The gem's glass (transmission + dispersion) is desktop-only; phones get a lit, flat-shaded stone.
- Lenis intercepts programmatic `window.scrollTo` for about a second after load; in-page anchors go through Lenis, so this only affects test scripts.
- The single-file build carries no three.js; its gem is the stills.
- Lighthouse numbers come from software-rendered WebGL; desktop blocking time on a real GPU will be lower, but that could not be measured here.

## TODO — every placeholder in the markup

Content that could not be supplied truthfully and must be confirmed or replaced before launch:

- `index.html` — ManaGem dashboard and payroll recreations, WasteMart operations/driver recreation: **validate layout, labels and module names against the live products.**
- `index.html` — selected work metrics "Month-end close: nine days to two" and "Six hours a week back, per depot": **provisional, unmeasured** (carried over, marked `CONTENT-TODO`).
- `index.html` — trust bar names (AX-Channels, Sonke Gender Justice, NeuraUX, KiY Trucking, CMaxx WiFi Solutions, Hive Creative Studio): already published elsewhere on the site; **confirm consent and supply logo files if marks are wanted**.
- `case-studies.html` — the two recreations: **validate against the live products.**
- `managem.html` — the module tour's ten module names and the dashboard recreation: **validate against ManaGem.**
- `industries.html` — provisional fourth sector (carried over, `CONTENT-TODO`).
- `insights.html` — three article outlines (carried over, `CONTENT-TODO`; page stays out of the nav).
- `privacy.html` — draft notice pending approval (carried over).
- `contact.html` — the schematic map is deliberately not geographic; **confirm it is acceptable or supply a map**.
- The estimator's defaults (25 people, 3 h/week, R 350/h) are illustrative starting positions, not claims; the copy says so.

Not added, by the brief's rule: no testimonials, no certifications, no client logos, no statistics beyond "since 2014".
