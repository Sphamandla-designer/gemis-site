// Renders the corporate site's link-preview card and its PNG icons.
//   tools/og-card.html      -> assets/img/og/gemis-share.jpg (1200×630)
//   assets/img/favicon.svg  -> assets/img/apple-touch-icon.png (180×180), assets/img/favicon-32.png
// usage: node tools/render-og.mjs   (set PLAYWRIGHT_MODULE if Playwright is elsewhere)
import { readFile, mkdir } from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join } from 'node:path';
import { createRequire } from 'node:module';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || '/opt/node22/lib/node_modules/playwright');

const browser = await chromium.launch();
try {
  // the card: the logo is the shipped SVG, inlined so it takes the block's colour
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(join(ROOT, 'tools/og-card.html')).href);
  const logo = await readFile(join(ROOT, 'assets/img/logos/gemis-logo.svg'), 'utf8');
  await page.evaluate((svg) => { document.getElementById('logo').outerHTML = svg.replace('<svg ', '<svg class="logo" '); }, logo);
  await page.evaluate(() => document.fonts.ready);
  await mkdir(join(ROOT, 'assets/img/og'), { recursive: true });
  await page.screenshot({ path: join(ROOT, 'assets/img/og/gemis-share.jpg'), type: 'jpeg', quality: 86 });

  // the icons, from the favicon itself
  const fav = await readFile(join(ROOT, 'assets/img/favicon.svg'), 'utf8');
  for (const [size, out] of [[180, 'assets/img/apple-touch-icon.png'], [32, 'assets/img/favicon-32.png']]) {
    const p = await browser.newPage({ viewport: { width: size, height: size }, deviceScaleFactor: 1 });
    // the touch icon is square: iOS rounds the corners itself
    const svg = size === 180 ? fav.replace(/rx="[^"]*"/, 'rx="0"') : fav;
    await p.setContent(`<body style="margin:0">${svg.replace('<svg ', `<svg width="${size}" height="${size}" `)}</body>`);
    await p.screenshot({ path: join(ROOT, out), omitBackground: size !== 180 });
  }
  console.log('wrote assets/img/og/gemis-share.jpg, assets/img/apple-touch-icon.png, assets/img/favicon-32.png');
} finally {
  await browser.close();
}
