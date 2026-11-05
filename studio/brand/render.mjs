import { chromium } from '/opt/node22/lib/node_modules/playwright/index.js';
(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME || chromium.executablePath() });
  const B = new URL('./', import.meta.url).pathname;
  let page = await browser.newPage({ viewport: { width: 1400, height: 440 }, deviceScaleFactor: 1 });
  await page.goto('file://' + B + 'sheet.html'); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(300);
  await page.screenshot({ path: B + 'logo-sheet.png', fullPage: true }); await page.close();
  for (const [scale, name] of [[2, 'linkedin-banner@2x.png'], [1, 'linkedin-banner.png']]) {
    page = await browser.newPage({ viewport: { width: 1128, height: 191 }, deviceScaleFactor: scale });
    await page.goto('file://' + B + 'banner.html'); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(400);
    await page.screenshot({ path: B + name }); await page.close();
  }
  // the link-share thumbnail: 1200 × 627 at 1× (PNG + JPEG) and 2×
  for (const [scale, name, type] of [[1, 'linkedin-thumbnail-1200x627.png', 'png'], [1, 'linkedin-thumbnail-1200x627.jpg', 'jpeg'], [2, 'linkedin-thumbnail-1200x627@2x.png', 'png']]) {
    page = await browser.newPage({ viewport: { width: 1200, height: 627 }, deviceScaleFactor: scale });
    await page.goto('file://' + B + 'linkedin-thumbnail.html'); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(500);
    await page.screenshot({ path: B + name, type, ...(type === 'jpeg' ? { quality: 88 } : {}) }); await page.close();
  }
  await browser.close();
})();
