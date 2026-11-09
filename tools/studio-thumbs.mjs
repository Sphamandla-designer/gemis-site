#!/usr/bin/env node
/**
 * Renders the studio's case-study thumbnails.
 *
 *   node tools/studio-thumbs.mjs
 *
 * Reads  studio/src/thumbs.html — one .scene per case: the app window and phone cut
 *                                 from the case-study video (assets/img/ui/) mounted
 *                                 in a laptop and a phone on a studio backdrop
 * Writes studio/assets/cases/<slug>.jpg — 1400 × 963 (the Work card's 16:11), JPEG q86
 *
 * Nothing on a screen is drawn here: the screens are the repository's own
 * sample-data interfaces, the only real product imagery it holds.
 */
import { mkdir } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(fileURLToPath(new URL('..', import.meta.url)));
const SRC = join(ROOT, 'studio/src/thumbs.html');
const OUT = join(ROOT, 'studio/assets/cases');
const PLAYWRIGHT = process.env.PLAYWRIGHT_MODULE || '/opt/node22/lib/node_modules/playwright/index.js';

const { chromium } = await import(PLAYWRIGHT).then((m) => m.default ?? m);
await mkdir(OUT, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 1 });
await page.goto('file://' + SRC, { waitUntil: 'load' });
await page.evaluate(async () => { for (const i of document.images) { try { await i.decode(); } catch (e) { throw new Error('image failed: ' + i.getAttribute('src')); } } });
await page.waitForTimeout(300);
const scenes = await page.$$('.scene');
for (const scene of scenes) {
  const slug = await scene.getAttribute('data-slug');
  await scene.scrollIntoViewIfNeeded();
  await scene.screenshot({ path: join(OUT, slug + '.jpg'), type: 'jpeg', quality: 86 });
  console.log(`studio/assets/cases/${slug}.jpg written`);
}
await browser.close();
