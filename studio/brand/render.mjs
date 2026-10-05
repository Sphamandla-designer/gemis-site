import { chromium } from '/opt/node22/lib/node_modules/playwright/index.js';
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const B = new URL('./', import.meta.url).pathname;
  let page = await browser.newPage({ viewport: { width: 1400, height: 440 }, deviceScaleFactor: 1 });
  await page.goto('file://' + B + 'sheet.html'); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(300);
  await page.screenshot({ path: B + 'logo-sheet.png', fullPage: true }); await page.close();
  for (const [scale, name] of [[2, 'linkedin-banner@2x.png'], [1, 'linkedin-banner.png']]) {
    page = await browser.newPage({ viewport: { width: 1128, height: 191 }, deviceScaleFactor: scale });
    await page.goto('file://' + B + 'banner.html'); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(400);
    await page.screenshot({ path: B + name }); await page.close();
  }
  await browser.close();
})();
