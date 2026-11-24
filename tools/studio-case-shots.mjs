// Captures the real screens of the two prototypes in the repository, for the
// studio's ManaGEM and WasteMart case studies.
//
//   ManaGem.html          — the 2026 ManaGEM redesign, a clickable desktop prototype
//   wastemart-driver.html — the WasteMart driver app, a clickable phone prototype
//
// Both carry sample data. Before each capture the sample data is made neutral:
// real company names in the prototypes' demo records become generic ones, real
// people become sample names, and the one phone number goes (the site carries
// none). Nothing else on a screen is altered.
//
// usage: node tools/studio-case-shots.mjs <out-dir>
// then:  node tools/studio-case-mocks.mjs <out-dir>   (mounts them in device mockups)
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const OUT = process.argv[2];
if (!OUT) { console.error('usage: node tools/studio-case-shots.mjs <out-dir>'); process.exit(1); }
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || '/opt/node22/lib/node_modules/playwright');

// sample data made neutral — [find, replace], applied to every text node and attribute value
const NEUTRAL = [
  // ManaGEM: the demo workspace is named after a real client, and its user list names a real person
  ['SBS Waterproofing', 'Demo Contracting'], ['sbswaterproofing.co.za', 'example.co.za'],
  ['Ryan Smith', 'Thabo Nkosi'], ['@rsmith', '@tnkosi'], ['ryan@', 'thabo@'],
  // WasteMart: the demo route is made of real retailers and brands
  ['Pick n Pay', 'Retail Park'], ['Engen Garage', 'Fuel Station'], ['Engen', 'Fuel Station'],
  ['Tygervalley Mall', 'Shopping Centre'], ['Mediclinic', 'Private Clinic'], ['Shoprite', 'Supermarket'],
  ['Cape Union Mart', 'Outdoor Retail'], ['Builders Warehouse', 'Hardware Warehouse'],
  ['Vergelegen Wine Estate', 'Wine Estate'], ['Vodacom Distribution', 'Telecoms Distribution'], ['Vodacom', 'Telecoms'],
  // no phone number anywhere on either site
  [/ ?· ?0\d{2} ?\d{3} ?\d{4}/g, ''],
];

const neutralise = (page) => page.evaluate((pairs) => {
  const rx = pairs.map(([a, b]) => [a.re ? new RegExp(a.re, a.flags) : a, b]);
  const fix = (s) => rx.reduce((t, [a, b]) => (typeof a === 'string' ? t.split(a).join(b) : t.replace(a, b)), s);
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) { const v = fix(n.nodeValue); if (v !== n.nodeValue) n.nodeValue = v; }
  for (const el of document.querySelectorAll('input, textarea')) if (el.value) el.value = fix(el.value);
}, NEUTRAL.map(([a, b]) => [a instanceof RegExp ? { re: a.source, flags: a.flags } : a, b]));

const browser = await chromium.launch();

// ── ManaGEM ──────────────────────────────────────────────────────────────
{
  const out = join(OUT, 'managem'); mkdirSync(out, { recursive: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  await page.goto(pathToFileURL(join(ROOT, 'ManaGem.html')).href);
  await page.waitForTimeout(5000);
  const shot = async (name, opts = {}) => { await neutralise(page); await page.waitForTimeout(150); await page.screenshot({ path: join(out, name + '.png'), ...opts }); console.log('managem/' + name); };
  await shot('login');
  await page.getByRole('button', { name: 'Sign in' }).click(); await page.waitForTimeout(2500);
  await page.locator('button:has-text("×"), [aria-label="Dismiss"], [aria-label="Close"]').first().click().catch(() => {});
  await page.waitForTimeout(400);
  await shot('dashboard');
  await page.locator('main').evaluate((m) => { const s = [...m.querySelectorAll('*')].find((e) => e.scrollHeight > e.clientHeight + 50 && getComputedStyle(e).overflowY !== 'visible') || document.scrollingElement; s.scrollTop = 520; });
  await page.mouse.wheel(0, 520); await page.waitForTimeout(500);
  await shot('dashboard-projects');
  const go = async (label, name) => {
    const nav = page.locator('aside, nav').getByText(label, { exact: true }).first();
    await nav.scrollIntoViewIfNeeded(); await nav.click(); await page.waitForTimeout(1300);
    await page.mouse.move(1300, 120);
    await shot(name);
  };
  await go('New Enquiry', 'enquiry-new');
  await go('Open Enquiries', 'enquiries-open');
  await go('Closed Enquiries', 'enquiries-closed');
  await go('Quote Templates', 'quote-templates');
  await go('Invoices', 'invoices');
  await go('Sage Invoices', 'accounting-sync');
  await go('Projects Module', 'projects');
  await go('Factory', 'factory');
  await go('Stock Control', 'stock');
  await go('Debtors Management', 'debtors');
  await go('Reports', 'reports');
  await go('Warranties', 'warranties');
  await go('Manage Users', 'users');
  await page.close();
}

// ── the WasteMart driver app ─────────────────────────────────────────────
{
  const out = join(OUT, 'wastemart'); mkdirSync(out, { recursive: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 }, deviceScaleFactor: 3 });
  // the app re-renders its own data, so neutralise the prototype's source, not just the screen
  let src = readFileSync(join(ROOT, 'wastemart-driver.html'), 'utf8');
  for (const [a, b] of NEUTRAL) src = typeof a === 'string' ? src.split(a).join(b) : src.replace(a, b);
  const copy = join(out, '_prototype.html'); writeFileSync(copy, src);
  await page.goto(pathToFileURL(copy).href);
  await page.waitForTimeout(5000);
  // the prototype draws its own phone; capture the screen inside the bezel
  const screen = async () => page.evaluate(() => {
    const f = [...document.querySelectorAll('body div')].find((e) => { const r = e.getBoundingClientRect(); return r.width > 380 && r.width < 440 && r.height > 820 && getComputedStyle(e).borderRadius !== '0px'; });
    const r = f.getBoundingClientRect(); const b = parseFloat(getComputedStyle(f).borderTopWidth) || 10;
    return { x: r.x + b, y: r.y + b, width: r.width - 2 * b, height: r.height - 2 * b };
  });
  // dismiss any passing notice ("Workday started …") so it does not cover the screen
  const quiet = () => page.evaluate(() => {
    const t = [...document.querySelectorAll('body *')].filter((e) => /^\s*Workday started at/.test(e.textContent) && e.getBoundingClientRect().height < 80);
    const box = t.sort((a, b) => b.getBoundingClientRect().width - a.getBoundingClientRect().width)[0];
    if (box) box.style.visibility = 'hidden';
  });
  const shot = async (name) => { await quiet(); await page.waitForTimeout(500); await neutralise(page); await page.waitForTimeout(150); await page.screenshot({ path: join(out, name + '.png'), clip: await screen() }); console.log('wastemart/' + name); };
  const tap = async (name) => {
    const b = page.getByRole('button', { name, exact: false }).first();
    if (await b.count()) await b.click(); else await page.getByText(name, { exact: false }).first().click();
    await page.waitForTimeout(1200);
  };
  await shot('login');
  await tap('Log in');
  await tap('Select Vehicle'); await shot('vehicles');
  await tap('CT-WM-422'); await tap('Use this vehicle'); await shot('start-day');
  await tap('Start Day'); await shot('start-confirm');
  await tap('Yes, Start Day'); await shot('route');
  await tap('Retail Park'); await shot('job');
  await tap('Confirm & Check In'); await shot('check-in');
  await tap('Yes, Check In'); await shot('job-on-site');
  await tap('Capture Details'); await shot('manifest');
  await page.locator('main, [class*=scroll], body').first().evaluate(() => { const s = [...document.querySelectorAll('div')].find((e) => e.scrollHeight > e.clientHeight + 100 && /auto|scroll/.test(getComputedStyle(e).overflowY)); if (s) s.scrollTop = 560; });
  await page.waitForTimeout(400); await shot('manifest-bins');
  await tap('View / Edit Sign-Off'); await shot('sign-off');
  // a signature, as a customer would write one: a looped capital, then a run of joined letters
  const pad = page.locator('canvas').first();
  if (await pad.count()) {
    const bb = await pad.boundingBox();
    const at = (x, y) => [bb.x + bb.width * x, bb.y + bb.height * y];
    const stroke = async (pts) => { await page.mouse.move(...at(...pts[0])); await page.mouse.down(); for (const p of pts.slice(1)) await page.mouse.move(...at(...p), { steps: 2 }); await page.mouse.up(); };
    // a looped capital, then a run of joined letters, then an underline — smooth, as a pen draws
    const cap = []; for (let i = 0; i <= 36; i++) { const t = i / 36 * Math.PI * 2.2; cap.push([.19 + Math.sin(t) * .045 + t * .012, .52 - Math.cos(t) * .22 * (1 - i / 60)]); }
    await stroke(cap);
    const run = []; for (let i = 0; i <= 90; i++) { const t = i / 90; run.push([.30 + t * .50, .60 - Math.pow(Math.abs(Math.sin(t * Math.PI * 7)), 1.4) * .17 * (1 - t * .35)]); }
    await stroke(run);
    const ul = []; for (let i = 0; i <= 20; i++) { const t = i / 20; ul.push([.24 + t * .60, .80 - t * .05 + Math.sin(t * 3) * .01]); }
    await stroke(ul);
    await page.waitForTimeout(300); await shot('sign-off-signed');
  }
  await page.goto(pathToFileURL(copy).href); await page.waitForTimeout(5000);
  await tap('Log in'); await tap('Select Vehicle'); await tap('CT-WM-422'); await tap('Use this vehicle'); await tap('Start Day'); await tap('Yes, Start Day');
  await tap('Activity'); await shot('activity');
  await tap('Shift Controls'); await shot('shift');
  await page.close();
}
await browser.close();
