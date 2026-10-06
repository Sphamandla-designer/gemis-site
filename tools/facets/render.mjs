const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || '/opt/node22/lib/node_modules/playwright/index.js');
import fs from 'node:fs';
const OUT = new URL('./', import.meta.url).pathname;
const IMG = new URL('../../assets/img/', import.meta.url).pathname;
(async () => {
  const jobs = JSON.parse(fs.readFileSync(OUT + 'jobs.json', 'utf8'));
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [name, w, h] of jobs) {
    const svg = fs.readFileSync(OUT + 'svg/' + name.replace('/', '__').replace('.jpg', '.svg'), 'utf8');
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.setContent(`<!doctype html><html><head><style>html,body{margin:0;width:${w}px;height:${h}px;overflow:hidden}svg{display:block}</style></head><body>${svg}</body></html>`);
    fs.mkdirSync(IMG + name.split('/')[0], { recursive: true });
    await page.screenshot({ path: IMG + name, type: 'jpeg', quality: 84 }); await page.close();
  }
  await browser.close(); console.log('rendered', jobs.length);
})();
