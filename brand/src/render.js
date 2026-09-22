/* Render the marketing assets at exact pixel sizes.
   Each canvas is shot at 2x and downsampled by make.py for clean edges. */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const SRC = __dirname;
const OUT = __dirname + '/../out/raw';
fs.mkdirSync(OUT, { recursive: true });

const JOBS = [
  { file: 'linkedin-personal.html',     out: 'linkedin-banner-1584x396',      w: 1584, h: 396 },
  { file: 'linkedin-personal-ink.html', out: 'linkedin-banner-ink-1584x396',  w: 1584, h: 396 },
  { file: 'linkedin-company.html',      out: 'linkedin-cover-1128x191',       w: 1128, h: 191 },
];

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });

  for (const j of JOBS) {
    for (const guides of [false, true]) {
      const page = await browser.newPage({
        viewport: { width: j.w, height: j.h }, deviceScaleFactor: 2,
      });
      const errs = [];
      page.on('requestfailed', r => errs.push(r.url()));
      await page.goto('file://' + path.join(SRC, j.file), { waitUntil: 'networkidle' });
      if (guides) await page.evaluate(() => document.body.classList.add('guides'));
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(400);

      const el = await page.$('#c');
      const box = await el.boundingBox();
      if (Math.round(box.width) !== j.w || Math.round(box.height) !== j.h) {
        throw new Error(`${j.out}: canvas is ${box.width}x${box.height}, expected ${j.w}x${j.h}`);
      }
      await el.screenshot({ path: `${OUT}/${j.out}${guides ? '-guides' : ''}@2x.png` });
      if (errs.length) console.log('  !! failed requests:', errs.join(', '));
      await page.close();
    }
    console.log(`${j.out}  ${j.w}x${j.h}  ✓`);
  }

  // rasterise the square avatar straight from its SVG
  const av = await browser.newPage({ viewport: { width: 400, height: 400 }, deviceScaleFactor: 2 });
  await av.setContent(
    `<style>html,body{margin:0}img{display:block;width:400px;height:400px}</style>
     <img src="file://${__dirname}/../logo/gemis-studio-avatar.svg">`);
  await av.waitForTimeout(300);
  await av.screenshot({ path: `${OUT}/linkedin-avatar-400x400@2x.png` });
  console.log('linkedin-avatar-400x400  400x400  ✓');

  await browser.close();
})();
