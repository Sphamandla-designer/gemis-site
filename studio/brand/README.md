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
| `avatar-400.svg` | square profile picture (LinkedIn and the like), on ink |
| `linkedin-cover-1584x396.png` · `.jpg` | the LinkedIn Company Page cover, exactly 1584 × 396: the three lines of copy on the left, a hairline design-system composition on the right, everything inside the 120 / 45 px safe area and clear of the lower-left profile-image overlap. Source: `linkedin-cover-1584.html` |
| `linkedin-banner.png` · `linkedin-banner@2x.png` | the earlier 1128 × 191 cover from the hero facets image |
| `logo-sheet.png` | one image of every variant, for review |

Type in the lock-ups is the site's own: Manrope 700 tracked for GEMIS, JetBrains
Mono tracked for STUDIO. Clear space around the mark is the width of its table;
minimum size 16px. The pink always sits above the orange.

The banner keeps its bottom-left corner empty because LinkedIn lays the page's
square logo over it, and keeps the message centre-left so phones, which show the
middle of the cover, still read it. `banner.html` and `sheet.html` are the
sources; `render.mjs` re-exports the PNGs with Chromium.

The site's header still carries the earlier three-bar glyph. Swapping it for the
stone is a small change in `studio/src/index.html` followed by a rebuild.
