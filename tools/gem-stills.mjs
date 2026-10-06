// Renders the gem's fallback stills from design/gem-states.html into assets/img/gem/*.png.
//   python3 -m http.server 8079 --bind 127.0.0.1   (from the repository root, in another shell)
//   node tools/gem-stills.mjs
// Needs Playwright's Chromium (set CHROME to its path) and Python 3 with Pillow for the crop + quantise step.
const pw = await import('/opt/node22/lib/node_modules/playwright/index.mjs').catch(() => import('/opt/node22/lib/node_modules/playwright/index.js'));
const { chromium } = pw.default ?? pw;
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const browser = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 900, height: 900 } });
page.on('console', (m) => console.log('[page]', m.text()));
await page.goto((process.env.BASE || 'http://127.0.0.1:8079/') + 'design/gem-states.html');
await page.addStyleTag({ content: 'html,body{background:transparent!important}canvas{width:800px!important;height:800px!important}' });
await page.waitForFunction(() => window.gemReady, null, { timeout: 60000 });
await page.waitForTimeout(300);
for (const st of ['whole', 'fractured', 'reassembled', 'small', 'missing']) {
  const data = await page.evaluate((s) => window.showState(s), st);
  fs.writeFileSync(`${root}/assets/img/gem/${st}.raw.png`, Buffer.from(data.split(',')[1], 'base64'));
  console.log('rendered', st);
}
await browser.close();
// crop each still to a square around the stone, resize, quantise to PNG-8 (flat facets compress well)
execFileSync('python3', ['-c', `
from PIL import Image
import os
d='${root}/assets/img/gem'
for n in ['whole','fractured','reassembled','small','missing']:
    im=Image.open(f'{d}/{n}.raw.png').convert('RGBA'); l,t,r,b=im.getbbox(); cx,cy=(l+r)//2,(t+b)//2; half=int(max(r-l,b-t)*.56)
    im=im.crop((cx-half,cy-half,cx+half,cy+half)); size=400 if n=='small' else 800
    im=im.resize((size,size), Image.LANCZOS).quantize(colors=256, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG); im.save(f'{d}/{n}.png', optimize=True); os.remove(f'{d}/{n}.raw.png')
    print(n, os.path.getsize(f'{d}/{n}.png'), 'bytes')
`], { stdio: 'inherit' });
