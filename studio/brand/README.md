# GEMIS® Studio — brand assets

The mark is a cut stone: table and crown above the girdle, pavilion below. It is
GEM Information Systems reduced to one gem, in the studio's two accents — pink
(#ff1f7a) above, orange (#ff7a12) below — with a hairline of background between
them. Two flat shapes, so it survives 16px, single-colour print and a favicon.

| file | use |
|---|---|
| `mark-colour.svg` · `mark-ink.svg` · `mark-white.svg` | the stone alone: favicons, avatars, UI |
| `logo-colour-on-light.svg` · `logo-colour-on-dark.svg` | the horizontal lock-up, mark + GEMIS / STUDIO |
| `logo-ink.svg` · `logo-white.svg` | single-colour lock-ups for print and photography |
| `avatar-400.svg` · `.png` · `.jpg` | square profile picture (LinkedIn and the like), on ink |
| `*.png` · `*.jpg` beside each SVG | the same mark and lock-ups rasterised: PNG with a transparent background (marks 1024 px, lock-ups 1408 × 256), JPEG on the background each is meant for. `gemis-studio-logos.zip` bundles them all |
| `linkedin-banner.png` · `linkedin-banner.jpg` | the LinkedIn showcase cover at exactly 1128 × 191 px, from the hero facets image (PNG 117 KB, JPEG 37 KB; LinkedIn allows up to 3 MB). Source: `banner.html` |
| `linkedin-banner@2x.png` | the same cover at 2256 × 382, for anywhere that wants a sharper copy |
| `linkedin-cover-1584x396.png` · `.jpg` | an alternative cover at the 1584 × 396 Company Page size, with a different, hairline composition. Source: `linkedin-cover-1584.html` |
| `logo-sheet.png` | one image of every variant, for review |

Type in the lock-ups is the site's own: Manrope 700 tracked for GEMIS, JetBrains
Mono tracked for STUDIO. Clear space around the mark is the width of its table;
minimum size 16px. The pink always sits above the orange.

The banner keeps its bottom-left corner empty because LinkedIn lays the page's
square logo over it, and keeps the message centre-left so phones, which show the
middle of the cover, still read it. `banner.html` and `sheet.html` are the
sources; `render.mjs` re-exports the PNGs with Chromium.

On the site the stone sits in the header of every studio page (white, inside the
header's difference blend, so it reads ink on light sections and white on dark),
in the hero's country card, beside the copyright in the closing band, and as the
tab icon and touch icon. The copies the pages use live in `studio/assets/`.
