# GEMIS Studio — brand & marketing assets

Everything here matches the studio site: the same palette, the same two
typefaces, and the same ladder mark that sits in the site nav.

## Palette

| Token | Hex | Used for |
| --- | --- | --- |
| Ink | `#16161a` | dark grounds, body text on light |
| Field | `#eef0f3` | primary light ground |
| Panel | `#f5f6f8` | second light ground, text on ink |
| Pink | `#ff1f7a` | primary accent — one emphasis per layout |
| Orange | `#ff7a12` | secondary accent, rules and eyebrows |
| Body | `#3a3b41` | supporting copy on light |
| Mute | `#6a6b73` | mono captions on light |

## Type

- **Manrope** — display and body. 600 for headlines at `-0.045em` tracking, 700 for the wordmark.
- **JetBrains Mono** — captions, prices, labels. Always uppercase, `0.1em`–`0.16em` tracking.

Both ship as variable `.woff2` in `src/`.

## Logo

The mark is three descending bars — the ladder from "one ladder, four fixed
steps". The wordmark is outlined to paths, so the SVGs render correctly
without Manrope or JetBrains Mono installed.

| File | Use |
| --- | --- |
| `logo/gemis-studio-lockup.svg` | default — horizontal, mark + wordmark |
| `logo/gemis-studio-lockup-light.svg` | same, for ink and photographic grounds |
| `logo/gemis-studio-stacked.svg` | narrow placements, square-ish spaces |
| `logo/gemis-studio-mark.svg` | mark alone, where the name is already present |
| `logo/gemis-studio-mark-pink.svg` | accent use only, never beside the wordmark |
| `logo/gemis-studio-avatar.svg` | square badge for social profile pictures |

PNG exports at 1x and 2x are in `logo/png/` for tools that can't take SVG.

**Rules.** Clear space on every side is the height of one bar in the mark.
Minimum width for the horizontal lockup is 96px — below that use the mark
alone. Don't recolour the lockup (ink or off-white only), don't restack it,
and don't set the wordmark in another face.

## LinkedIn

| File | Size | Where |
| --- | --- | --- |
| `linkedin/gemis-studio-linkedin-banner-1584x396.png` | 1584×396 | personal profile background |
| `linkedin/gemis-studio-linkedin-banner-ink-1584x396.png` | 1584×396 | same, dark alternative |
| `linkedin/gemis-studio-linkedin-cover-1128x191.png` | 1128×191 | company page cover |
| `linkedin/gemis-studio-linkedin-avatar-400x400.png` | 400×400 | profile picture / company logo |

LinkedIn covers part of every banner with the profile photo and crops the
sides on narrow screens, so all copy sits inside a safe band. The renders in
`linkedin/safe-area-guides/` draw those zones — the pink outline is where the
profile photo lands, the orange lines are the narrow-viewport crop. They are
for checking, not for upload.

## Regenerating

Sources are in `src/` — plain HTML and CSS, rendered headlessly at 2x and
downsampled, so what you see in a browser is what ships.

```bash
cd brand/src
python3 mklogo.py     # logo SVGs (needs: pip install fonttools brotli)
node render.js        # LinkedIn artwork -> ../out/raw
node logopng.js       # logo PNG exports
```

Edit copy and layout directly in `src/*.html`; `brand.css` holds the shared
tokens. `facets.jpg` is the 3D render used across the site hero, the services
section and these banners.
