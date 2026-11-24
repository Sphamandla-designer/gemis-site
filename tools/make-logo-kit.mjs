// The GEMIS logo kit: every logo variant as SVG and PNG, for both brands.
//
//   node tools/make-logo-kit.mjs
//
// Reads the masters that tools/make-logo.py writes (assets/img/logos/gemis-logo.svg,
// gemis-logo-stacked.svg, gemis-mark.svg; studio/assets/gemis-studio-logo.svg,
// mark-colour.svg) and writes brand/logos/:
//
//   gemis/svg/*.svg   gemis/png/*-<width>.png   studio/svg/*.svg   studio/png/*-<width>.png
//   index.html (the preview sheet with downloads), README.md, GEMIS-logos.zip
//
// The masters fill with currentColor, which most apps show as black; every file here
// carries its real colours. Each SVG's viewBox is the artwork's tight box plus a hair
// of padding (measured in Chromium), so placing one never brings stray white space.
// The tiles (the logo on navy, the square avatar, the app icon) carry their ground.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const R = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(R, 'brand', 'logos');
const NAVY = '#0a1230', WHITE = '#ffffff', BLACK = '#000000';
const INK = '#16161a', INK2 = '#55565e', PINK = '#ff1f7a', ORANGE = '#ff7a12', SOFT = '#b9bac4';

const read = (f) => fs.readFileSync(path.join(R, f), 'utf8');
const inner = (s) => s.replace(/<svg[^>]*>/, '').replace('</svg>', '').trim();
const LOGO = inner(read('assets/img/logos/gemis-logo.svg'));
const STACKED = inner(read('assets/img/logos/gemis-logo-stacked.svg'));
const MARK = inner(read('assets/img/logos/gemis-mark.svg'));
const WORDMARK = LOGO.replace(/^<g>.*?<\/g>/, '');                 // the lockup without the stone
const STUDIO = inner(read('studio/assets/gemis-studio-logo.svg'));  // fills: pink, orange, ink, ink-2
const STUDIO_MARK = inner(read('studio/assets/mark-colour.svg'));   // fills: pink, orange

const one = (art, c) => `<g fill="${c}">${art}</g>`;
const remap = (art, map) => art.replace(/fill="(#[0-9a-f]{6})"/gi, (m, c) => `fill="${map[c.toLowerCase()] ?? c}"`);
const studio = (g, s, top = PINK, bottom = ORANGE) => remap(STUDIO, { [PINK]: top, [ORANGE]: bottom, [INK]: g, [INK2]: s });
const studioMark = (top, bottom) => remap(STUDIO_MARK, { [PINK]: top, [ORANGE]: bottom });

// [brand, name, artwork, png widths, tile]   tile: null (transparent), or how to set it on a ground
const LOCKUP = [512, 1024, 2048], MARKS = [64, 128, 256, 512, 1024], TILES = [512, 1024], BANDS = [1200, 2400];
const V = [];
for (const [c, n] of [[NAVY, 'navy'], [WHITE, 'white'], [BLACK, 'black']]) {
  V.push(['gemis', `gemis-logo-${n}`, one(LOGO, c), LOCKUP]);
  V.push(['gemis', `gemis-logo-stacked-${n}`, one(STACKED, c), LOCKUP]);
  V.push(['gemis', `gemis-wordmark-${n}`, one(WORDMARK, c), LOCKUP]);
  V.push(['gemis', `gemis-mark-${n}`, one(MARK, c), MARKS]);
}
V.push(['gemis', 'gemis-logo-on-navy', one(LOGO, WHITE), BANDS, { bg: NAVY, pad: .55 }]);
V.push(['gemis', 'gemis-logo-stacked-on-navy', one(STACKED, WHITE), TILES, { bg: NAVY, square: .78 }]);
V.push(['gemis', 'gemis-avatar', one(MARK, WHITE), TILES, { bg: NAVY, square: .6 }]);
V.push(['gemis', 'gemis-app-icon', one(MARK, WHITE), TILES, { bg: NAVY, square: .6, radius: .1875 }]);

V.push(['studio', 'gemis-studio-logo-colour', studio(INK, INK2), LOCKUP]);
V.push(['studio', 'gemis-studio-logo-reversed', studio(WHITE, SOFT), LOCKUP]);
V.push(['studio', 'gemis-studio-logo-white', studio(WHITE, WHITE, WHITE, WHITE), LOCKUP]);
V.push(['studio', 'gemis-studio-logo-black', studio(BLACK, BLACK, BLACK, BLACK), LOCKUP]);
V.push(['studio', 'gemis-studio-mark-colour', studioMark(PINK, ORANGE), MARKS]);
V.push(['studio', 'gemis-studio-mark-white', studioMark(WHITE, WHITE), MARKS]);
V.push(['studio', 'gemis-studio-mark-black', studioMark(BLACK, BLACK), MARKS]);
V.push(['studio', 'gemis-studio-logo-on-ink', studio(WHITE, SOFT), BANDS, { bg: INK, pad: .55 }]);
V.push(['studio', 'gemis-studio-avatar', studioMark(PINK, ORANGE), TILES, { bg: INK, square: .6 }]);
V.push(['studio', 'gemis-studio-app-icon', studioMark(PINK, ORANGE), TILES, { bg: INK, square: .6, radius: .1875 }]);

const LABEL = {
  gemis: 'GEMIS — GEM Information Systems', studio: 'GEMIS Studio',
};
const f2 = (v) => +v.toFixed(2);

const b = await chromium.launch();
const p = await b.newPage();
await p.setContent('<!DOCTYPE html><html><body style="margin:0"></body></html>');

const made = [];
for (const [brand, name, art, widths, tile] of V) {
  // the artwork's tight box
  const box = await p.evaluate((a) => {
    document.body.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-500 -500 2000 2000" width="2000" height="2000"><g id="a">${a}</g></svg>`;
    const r = document.getElementById('a').getBBox();
    return { x: r.x, y: r.y, w: r.width, h: r.height };
  }, art);
  let svg, W, H;
  if (!tile) {
    const pad = Math.max(box.w, box.h) * .01;
    W = f2(box.w + 2 * pad); H = f2(box.h + 2 * pad);
    svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${f2(box.x - pad)} ${f2(box.y - pad)} ${W} ${H}" width="${f2(W * 4)}" height="${f2(H * 4)}" role="img" aria-label="${LABEL[brand]}">${art}</svg>`;
  } else if (tile.square) {
    // a square ground, the artwork scaled to `square` of its width, centred
    const S = 512, k = (S * tile.square) / Math.max(box.w, box.h);
    const tx = (S - box.w * k) / 2 - box.x * k, ty = (S - box.h * k) / 2 - box.y * k;
    W = H = S;
    svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${S} ${S}" width="${S}" height="${S}" role="img" aria-label="${LABEL[brand]}"><rect width="${S}" height="${S}"${tile.radius ? ` rx="${S * tile.radius}"` : ''} fill="${tile.bg}"/><g transform="translate(${f2(tx)} ${f2(ty)}) scale(${f2(k)})">${art}</g></svg>`;
  } else {
    // a band: clear space of `pad` × the artwork's height on every side
    const pad = box.h * tile.pad * 2;
    W = f2(box.w + 2 * pad); H = f2(box.h + 2 * pad);
    svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${f2(W * 4)}" height="${f2(H * 4)}" role="img" aria-label="${LABEL[brand]}"><rect width="${W}" height="${H}" fill="${tile.bg}"/><g transform="translate(${f2(pad - box.x)} ${f2(pad - box.y)})">${art}</g></svg>`;
  }
  const svgFile = path.join(OUT, brand, 'svg', `${name}.svg`);
  fs.mkdirSync(path.dirname(svgFile), { recursive: true });
  fs.writeFileSync(svgFile, svg + '\n');
  const pngs = [];
  for (const w of widths) {
    const h = Math.round(w * H / W);
    await p.setViewportSize({ width: w, height: h });
    await p.setContent(`<!DOCTYPE html><html><body style="margin:0;background:transparent">${svg.replace(/ width="[^"]+" height="[^"]+"/, ` width="${w}" height="${h}"`)}</body></html>`);
    const f = path.join(OUT, brand, 'png', `${name}-${w}.png`);
    fs.mkdirSync(path.dirname(f), { recursive: true });
    await p.screenshot({ path: f, omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
    pngs.push([w, h, path.relative(OUT, f)]);
  }
  made.push({ brand, name, svg: path.relative(OUT, svgFile), pngs, tile: !!tile, dark: /white|reversed/.test(name) });
}

// ---- the preview sheet ----------------------------------------------------------------
const card = (m) => {
  const ground = m.tile ? '#eef0f4' : m.dark ? (m.brand === 'studio' ? INK : NAVY) : '#ffffff';
  const links = [`<a href="${m.svg}" download>SVG</a>`, ...m.pngs.map(([w, h, f]) => `<a href="${f}" download>PNG ${w}</a>`)].join('');
  return `<figure class="c"><div class="g" style="background:${ground}"><img src="${m.svg}" alt="${m.name}"></div>
  <figcaption><b>${m.name}</b><span>${links}</span></figcaption></figure>`;
};
const section = (brand, title) => `<h2>${title}</h2><div class="grid">${made.filter((m) => m.brand === brand).map(card).join('')}</div>`;
fs.writeFileSync(path.join(OUT, 'index.html'), `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>GEMIS logos</title>
<link rel="icon" type="image/svg+xml" href="../../assets/img/favicon.svg">
<style>
@font-face{font-family:Montserrat;src:url(../../assets/fonts/montserrat-latin.woff2) format("woff2");font-weight:100 900;font-display:swap}
html,body{margin:0;background:#f3f4f7;color:${NAVY};font-family:Montserrat,'Segoe UI',Helvetica,Arial,sans-serif}
.wrap{max-width:1200px;margin:0 auto;padding:48px 24px 80px}
h1{margin:0 0 8px;font-size:24px;font-weight:300;letter-spacing:.06em;text-transform:uppercase}
h2{margin:48px 0 16px;font-size:12px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:#4a5068}
p{margin:0 0 20px;font-size:15px;line-height:1.6;color:#4a5068;max-width:68ch}
.all{display:inline-block;padding:14px 22px;background:${NAVY};color:#fff;text-decoration:none;font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:20px}
.c{margin:0;background:#fff;border:1px solid #d9dce5}
.g{height:170px;display:flex;align-items:center;justify-content:center;padding:24px;box-sizing:border-box;border-bottom:1px solid #d9dce5}
.g img{max-width:100%;max-height:100%}
figcaption{padding:14px 16px 16px}
figcaption b{display:block;font-size:12px;font-weight:600;letter-spacing:.02em;margin-bottom:10px;word-break:break-word}
figcaption span{display:flex;flex-wrap:wrap;gap:6px}
figcaption a{font-size:11px;letter-spacing:.06em;color:${NAVY};text-decoration:none;border:1px solid ${NAVY};padding:5px 8px}
figcaption a:hover,figcaption a:focus-visible{background:${NAVY};color:#fff}
</style></head><body><div class="wrap">
<h1>GEMIS logos</h1>
<p>Every logo as SVG (any size, for print and the web) and PNG (transparent, for slides, documents and social). Use the navy logo on light grounds and the white logo on navy or on photographs. Keep clear space of at least the stone's height around the logo, and never stretch, recolour or outline it.</p>
<a class="all" href="GEMIS-logos.zip" download>Download every file (zip)</a>
${section('gemis', 'GEMIS')}
${section('studio', 'GEMIS Studio')}
</div></body></html>
`);

// ---- README ---------------------------------------------------------------------------
fs.writeFileSync(path.join(OUT, 'README.md'), `# GEMIS logos

Generated by \`node tools/make-logo-kit.mjs\` from the masters that \`tools/make-logo.py\`
writes. Do not edit these files; change the masters and re-run both. The preview sheet
with download buttons is \`index.html\` (live at \`brand/logos/\`); \`GEMIS-logos.zip\` holds
every file.

| File | What it is | PNG widths |
|---|---|---|
| \`gemis-logo-{navy,white,black}\` | the horizontal logo: the stone, GEMIS, GEM INFORMATION SYSTEMS | 512, 1024, 2048 |
| \`gemis-logo-stacked-{navy,white,black}\` | the stone centred over the name | 512, 1024, 2048 |
| \`gemis-wordmark-{navy,white,black}\` | the name without the stone, for tight horizontal spaces | 512, 1024, 2048 |
| \`gemis-mark-{navy,white,black}\` | the stone alone | 64 to 1024 |
| \`gemis-logo-on-navy\` | the white logo on a midnight band, with clear space | 1200, 2400 |
| \`gemis-logo-stacked-on-navy\` | the stacked logo on a midnight square | 512, 1024 |
| \`gemis-avatar\` | the white stone on a midnight square: LinkedIn, social profiles | 512, 1024 |
| \`gemis-app-icon\` | the same on a rounded square | 512, 1024 |
| \`gemis-studio-logo-colour\` | the studio logo: the pink and orange stone, GEMIS in ink | 512, 1024, 2048 |
| \`gemis-studio-logo-reversed\` | the coloured stone with white type, for dark grounds | 512, 1024, 2048 |
| \`gemis-studio-logo-{white,black}\` | single colour | 512, 1024, 2048 |
| \`gemis-studio-mark-{colour,white,black}\` | the studio stone alone | 64 to 1024 |
| \`gemis-studio-logo-on-ink\` | the reversed studio logo on the studio's ink | 1200, 2400 |
| \`gemis-studio-avatar\`, \`gemis-studio-app-icon\` | the coloured stone on ink, square and rounded | 512, 1024 |

Colours: midnight navy \`${NAVY}\`; the studio's pink \`${PINK}\`, orange \`${ORANGE}\` and
ink \`${INK}\`. The PNGs are transparent except the tiles. Every SVG has its colours
written in, a tight viewBox and no dependence on a font.
`);

// ---- the zip (fixed dates, so a re-run with no change writes the same bytes) ------------
const JSZip = createRequire(createRequire(import.meta.url).resolve('/opt/node-tools/node_modules/docx/package.json'))('jszip');
const zip = new JSZip();
const date = new Date('2026-11-24T00:00:00Z');
for (const m of made) for (const f of [m.svg, ...m.pngs.map((x) => x[2])]) zip.file(`GEMIS-logos/${f}`, fs.readFileSync(path.join(OUT, f)), { date, createFolders: false });
zip.file('GEMIS-logos/README.md', fs.readFileSync(path.join(OUT, 'README.md')), { date, createFolders: false });
fs.writeFileSync(path.join(OUT, 'GEMIS-logos.zip'), await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE', platform: 'UNIX' }));
await b.close();
console.log(`${made.length} variants, ${made.reduce((n, m) => n + 1 + m.pngs.length, 0)} files`);
