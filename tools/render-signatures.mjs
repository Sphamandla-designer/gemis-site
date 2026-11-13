// Rasterise the email-signature art panels and export every signature as a PNG.
//
//   python3 tools/make-signatures.py   # first: writes the HTML and the SVG sources
//   node tools/render-signatures.mjs   # then: assets/img/email/sig-<slug>.png (2×)
//                                      #       brand/email-signatures/<slug>.png (2×)
//
// Chromium renders the SVG with the site's Montserrat so the initials and the
// vertical label match the pages; the PNG of the whole signature is the same
// table the HTML carries, with the panel pointed at the local file.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath, pathToFileURL } from 'node:url';

const R = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.join(R, 'assets', 'img', 'email', 'src');
const OUT = path.join(R, 'brand', 'email-signatures');
const LIVE = 'https://sphamandla-designer.github.io/gemis-site/';
const FONT = `<style>@font-face{font-family:Montserrat;src:url(${pathToFileURL(path.join(R, 'assets/fonts/montserrat-latin.woff2'))}) format("woff2");font-weight:100 900}html,body{margin:0;background:transparent}</style>`;

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'sig-'));
const load = async (html) => { const f = path.join(TMP, 'page.html'); fs.writeFileSync(f, html); await p.goto(pathToFileURL(f).href); await p.evaluate(() => document.fonts.ready); };
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 700, height: 500 }, deviceScaleFactor: 2 });
const slugs = fs.readdirSync(SRC).filter(f => f.endsWith('.svg')).map(f => f.slice(0, -4));
for (const slug of slugs) {
  const svg = fs.readFileSync(path.join(SRC, slug + '.svg'), 'utf8').replace('<svg ', '<svg id="art" ');
  await load(FONT + svg);
  await (await p.$('#art')).screenshot({ path: path.join(R, 'assets', 'img', 'email', 'sig-' + slug + '.png'), omitBackground: true });
}
for (const slug of slugs) {
  const html = fs.readFileSync(path.join(OUT, slug + '.html'), 'utf8').split(LIVE).join(pathToFileURL(R + '/').href);
  await load(html.replace('</head>', FONT + '</head>'));
  await (await p.$('table')).screenshot({ path: path.join(OUT, slug + '.png') });
}
await b.close();
fs.rmSync(TMP, { recursive: true, force: true });
console.log('rendered:', slugs.join(', '));
