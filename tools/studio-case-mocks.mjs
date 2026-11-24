// Mounts the prototype screens (tools/studio-case-shots.mjs) in device mockups,
// in the studio's language — the #eef0f3 / #16161a grounds, the pink and orange
// glow — for the ManaGEM and WasteMart case studies.
//
//   studio/assets/cases/<slug>/<scene>.jpg   one image per case-study section
//   studio/assets/cases/<slug>.jpg           the card image (Work grid, homepage)
//
// usage: node tools/studio-case-mocks.mjs <shots-dir>
import { mkdirSync, statSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SHOTS = process.argv[2];
if (!SHOTS) { console.error('usage: node tools/studio-case-mocks.mjs <shots-dir>'); process.exit(1); }
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || '/opt/node22/lib/node_modules/playwright');
const src = (slug, name) => pathToFileURL(join(SHOTS, slug, name + '.png')).href;

// ── the pieces ────────────────────────────────────────────────────────────
const GROUND = {
  light: `background:#eef0f3;`,
  dark: `background:#16161a;`,
};
const glow = (dark) => `
  <div style="position:absolute;left:-12%;top:-30%;width:70%;height:120%;border-radius:50%;background:radial-gradient(circle,rgba(255,31,122,${dark ? .26 : .16}) 0%,transparent 62%);filter:blur(40px)"></div>
  <div style="position:absolute;right:-14%;bottom:-40%;width:70%;height:130%;border-radius:50%;background:radial-gradient(circle,rgba(255,122,18,${dark ? .22 : .14}) 0%,transparent 62%);filter:blur(40px)"></div>`;
const shadow = (dark) => dark ? '0 60px 120px -30px rgba(0,0,0,.75), 0 18px 40px -18px rgba(0,0,0,.6)' : '0 60px 110px -40px rgba(22,22,26,.45), 0 18px 40px -20px rgba(22,22,26,.25)';

// a browser window: the desktop screens, shown as the web app they are
const browser = (img, w, dark, extra = '') => `
  <div style="width:${w}px;border-radius:14px;overflow:hidden;background:#fff;box-shadow:${shadow(dark)};${extra}">
    <div style="height:${Math.round(w * .028)}px;background:${dark ? '#26262c' : '#e4e6ea'};display:flex;align-items:center;gap:${Math.round(w * .006)}px;padding:0 ${Math.round(w * .012)}px">
      ${['#ff5f57', '#febc2e', '#28c840'].map((c) => `<i style="display:block;width:${Math.round(w * .008)}px;height:${Math.round(w * .008)}px;border-radius:50%;background:${c}"></i>`).join('')}
      <span style="margin-left:${Math.round(w * .02)}px;flex:1;max-width:46%;height:${Math.round(w * .014)}px;border-radius:99px;background:${dark ? '#34343b' : '#f5f6f8'}"></span>
    </div>
    <img src="${img}" style="display:block;width:100%">
  </div>`;
// a laptop
const laptop = (img, w, dark) => `
  <div style="width:${w}px;filter:drop-shadow(0 50px 60px rgba(22,22,26,${dark ? .7 : .32}))">
    <div style="margin:0 auto;width:${w * .84}px;background:#1b1b1f;border-radius:${w * .018}px ${w * .018}px 0 0;padding:${w * .012}px ${w * .012}px ${w * .02}px">
      <img src="${img}" style="display:block;width:100%;border-radius:3px">
    </div>
    <div style="height:${w * .022}px;background:linear-gradient(#d7d9de,#b9bcc3);border-radius:0 0 ${w * .03}px ${w * .03}px;position:relative">
      <span style="position:absolute;left:50%;top:0;transform:translateX(-50%);width:${w * .12}px;height:${w * .008}px;background:#a9acb3;border-radius:0 0 8px 8px"></span>
    </div>
  </div>`;
// a phone: the screen in a dark rounded body
const phone = (img, w, dark, extra = '') => `
  <div style="width:${w}px;padding:${w * .035}px;border-radius:${w * .15}px;background:#141417;box-shadow:${shadow(dark)}, inset 0 0 0 ${Math.max(2, w * .006)}px #2c2c33;${extra}">
    <img src="${img}" style="display:block;width:100%;border-radius:${w * .115}px">
  </div>`;
// a close-up: one region of a screen, enlarged, in a white card
const detail = (img, region, w, dark, label) => {
  const [x, y, rw, rh] = region; // fractions of the screen
  const h = Math.round(w * rh / rw * (900 / 1440));
  return `<figure style="margin:0;width:${w}px">
    <div style="width:${w}px;height:${h}px;border-radius:12px;overflow:hidden;background:#fff;box-shadow:${shadow(dark)};position:relative">
      <img src="${img}" style="position:absolute;width:${w / rw}px;left:${-x / rw * w}px;top:${-y * (w / rw) * (900 / 1440)}px">
    </div>
    ${label ? `<figcaption style="margin-top:18px;font:500 22px/1.3 'JetBrains Mono',monospace;letter-spacing:.04em;text-transform:uppercase;color:${dark ? '#c9cad1' : '#6a6b73'}">${label}</figcaption>` : ''}
  </figure>`;
};
const detailPhone = (img, region, w, dark, label) => {
  const [x, y, rw, rh] = region;
  const h = Math.round(w * rh / rw * (872 / 392));
  return `<figure style="margin:0;width:${w}px">
    <div style="width:${w}px;height:${h}px;border-radius:18px;overflow:hidden;background:#fff;box-shadow:${shadow(dark)};position:relative">
      <img src="${img}" style="position:absolute;width:${w / rw}px;left:${-x / rw * w}px;top:${-y * (w / rw) * (872 / 392)}px">
    </div>
    ${label ? `<figcaption style="margin-top:18px;font:500 22px/1.3 'JetBrains Mono',monospace;letter-spacing:.04em;text-transform:uppercase;color:${dark ? '#c9cad1' : '#6a6b73'}">${label}</figcaption>` : ''}
  </figure>`;
};

// ── the layouts ───────────────────────────────────────────────────────────
const W = 2000, H = 1250;
const stage = (dark, inner, extra = '') => `<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0}body{width:${W}px;height:${H}px;overflow:hidden;position:relative;${dark ? GROUND.dark : GROUND.light}${extra}}</style></head><body>${glow(dark)}${inner}</body></html>`;
const center = (html, style = '') => `<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;${style}">${html}</div>`;

const L = {
  // one desktop screen, in a laptop
  laptop: (s, d) => stage(d, center(laptop(s[0], 1560, d), 'padding-top:40px')),
  // one desktop screen in a window, turned into the light
  tilt: (s, d) => stage(d, center(`<div style="transform:perspective(2600px) rotateY(-16deg) rotateX(7deg) rotateZ(1deg);transform-origin:60% 50%">${browser(s[0], 1500, d)}</div>`, 'padding-left:60px')),
  // two windows, one over the other
  stack: (s, d) => stage(d, `
    <div style="position:absolute;left:110px;top:120px;opacity:.96">${browser(s[1], 1280, d)}</div>
    <div style="position:absolute;right:110px;bottom:110px">${browser(s[0], 1280, d)}</div>`),
  // three windows fanned in depth — the hero
  fan: (s, d) => stage(d, center(`<div style="position:relative;width:1700px;height:1000px;transform:perspective(3000px) rotateX(10deg) rotateY(-14deg);transform-style:preserve-3d">
      <div style="position:absolute;left:0;top:30px;transform:translateZ(-260px);opacity:.9">${browser(s[2], 1180, d)}</div>
      <div style="position:absolute;right:-40px;top:0;transform:translateZ(-140px)">${browser(s[1], 1180, d)}</div>
      <div style="position:absolute;left:220px;top:190px">${browser(s[0], 1280, d)}</div></div>`)),
  // four close-ups of desktop screens, in a grid
  details: (s, d, opt) => stage(d, `<div style="position:absolute;inset:110px 120px;display:grid;grid-template-columns:1fr 1fr;gap:70px 80px;align-content:center">
      ${opt.crops.map(([i, region, label]) => detail(s[i], region, 840, d, label)).join('')}</div>`),
  // one phone, upright, with a close-up beside it
  phoneDetail: (s, d, opt) => stage(d, `
      <div style="position:absolute;left:330px;top:50%;transform:translateY(-50%)">${phone(s[0], 470, d)}</div>
      <div style="position:absolute;right:250px;top:50%;transform:translateY(-50%)">${detailPhone(s[0], opt.crop, 760, d, opt.label)}</div>`),
  // two phones, the second a step behind
  phones2: (s, d) => stage(d, center(`<div style="position:relative;width:1100px;height:1120px">
      <div style="position:absolute;left:60px;top:90px;transform:rotate(-4deg)">${phone(s[1], 420, d)}</div>
      <div style="position:absolute;right:60px;top:40px;transform:rotate(3deg)">${phone(s[0], 440, d)}</div></div>`)),
  // three phones: one in front, two turned away — the hero
  phones3: (s, d) => stage(d, center(`<div style="position:relative;width:1600px;height:1150px;transform:perspective(2600px) rotateX(6deg)">
      <div style="position:absolute;left:120px;top:150px;transform:perspective(2000px) rotateY(24deg) scale(.9);opacity:.95">${phone(s[1], 420, d)}</div>
      <div style="position:absolute;right:120px;top:150px;transform:perspective(2000px) rotateY(-24deg) scale(.9);opacity:.95">${phone(s[2], 420, d)}</div>
      <div style="position:absolute;left:50%;top:60px;transform:translateX(-50%)">${phone(s[0], 460, d)}</div></div>`)),
  // four close-ups of phone screens
  phoneDetails: (s, d, opt) => stage(d, `<div style="position:absolute;inset:100px 130px;display:grid;grid-template-columns:1fr 1fr;gap:60px 90px;align-content:center">
      ${opt.crops.map(([i, region, label]) => detailPhone(s[i], region, 820, d, label)).join('')}</div>`),
};

// ── the scenes, one per section ───────────────────────────────────────────
const SCENES = {
  managem: [
    ['hero', 'fan', ['dashboard', 'enquiries-open', 'projects'], false],
    ['brief', 'laptop', ['login'], false],
    ['challenge', 'stack', ['enquiries-open', 'invoices'], true],
    ['enquiry', 'tilt', ['enquiry-new'], false],
    ['pipeline', 'tilt', ['enquiries-open'], true],
    ['quotes', 'stack', ['invoices', 'quote-templates'], false],
    ['accounting', 'tilt', ['accounting-sync'], true],
    ['projects', 'stack', ['projects', 'dashboard-projects'], false],
    ['operations', 'stack', ['stock', 'factory'], true],
    ['debtors', 'stack', ['reports', 'debtors'], false],
    ['details', 'details', ['dashboard', 'enquiries-open', 'invoices'], true, { crops: [
      [0, [.18, .235, .41, .14], 'KPI cards · trend vs prior'],
      [1, [.18, .195, .49, .105], 'Pipeline stages · counts at a glance'],
      [2, [.6, .38, .39, .235], 'Amounts and status, side by side'],
      [2, [.59, .295, .4, .07], 'Period · CSV · Excel · PDF'],
    ] }],
    ['build', 'laptop', ['dashboard'], true],
    ['results', 'tilt', ['dashboard-projects'], false],
  ],
  wastemart: [
    ['hero', 'phones3', ['route', 'job', 'manifest'], false],
    ['brief', 'phones2', ['start-day', 'login'], false],
    ['challenge', 'phones2', ['route', 'activity'], true],
    ['start', 'phones2', ['start-day', 'vehicles'], false],
    ['route', 'phoneDetail', ['route'], true, { crop: [0, .1, 1, .3], label: 'Nine stops · progress · disposal site' }],
    ['on-site', 'phones2', ['check-in', 'job'], false],
    ['manifest', 'phones2', ['manifest', 'manifest-bins'], true],
    ['sign-off', 'phoneDetail', ['sign-off-signed'], false, { crop: [0, .43, 1, .28], label: 'Signed on the glass, saved with the manifest' }],
    ['shift', 'phones2', ['shift', 'activity'], true],
    ['details', 'phoneDetails', ['route', 'manifest-bins', 'check-in', 'shift'], false, { crops: [
      [0, [0, .325, 1, .12], 'Route card · status · scheduled time'],
      [1, [0, .405, 1, .26], 'Count the bins · scan the bags'],
      [2, [.08, .46, .84, .135], 'Check-in tied to time and truck'],
      [3, [0, .33, 1, .2], 'Activity · sync status · offline queue'],
    ] }],
    ['build', 'phones3', ['job-on-site', 'sign-off-signed', 'shift'], true],
    ['results', 'phones2', ['job-on-site', 'route'], false],
  ],
};

// a page set from a string cannot read file:// images, so each scene is written beside the shots
const show = async (page, html) => {
  const f = join(SHOTS, '_scene.html'); writeFileSync(f, html);
  await page.goto(pathToFileURL(f).href, { waitUntil: 'load' });
  await page.evaluate(() => Promise.all([...document.images].map((i) => i.decode().catch(() => {}))));
  const broken = await page.evaluate(() => [...document.images].filter((i) => !i.naturalWidth).length);
  if (broken) throw new Error(broken + ' screen(s) did not load — run tools/studio-case-shots.mjs first');
};

const browserApp = await chromium.launch();
const page = await browserApp.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
for (const [slug, scenes] of Object.entries(SCENES)) {
  const dir = join(ROOT, 'studio/assets/cases', slug); mkdirSync(dir, { recursive: true });
  for (const [name, layout, shots, dark, opt] of scenes) {
    await page.setViewportSize({ width: W, height: H });
    await show(page, L[layout](shots.map((s) => src(slug, s)), dark, opt || {}));
    const out = join(dir, name + '.jpg');
    await page.screenshot({ path: out, type: 'jpeg', quality: 80 });
    console.log(`studio/assets/cases/${slug}/${name}.jpg  ${(statSync(out).size / 1024) | 0} KB`);
  }
  // the card image: the hero scene at the cards' 1400×963
  const [, layout, shots, dark] = scenes[0];
  await page.setViewportSize({ width: 1400, height: 963 });
  await show(page, L[layout](shots.map((s) => src(slug, s)), dark, {}).replace(`width:${W}px;height:${H}px`, 'width:2000px;height:1376px;transform:scale(.7);transform-origin:0 0'));
  await page.screenshot({ path: join(ROOT, 'studio/assets/cases', slug + '.jpg'), type: 'jpeg', quality: 82 });
  console.log(`studio/assets/cases/${slug}.jpg  (card)`);
}
await browserApp.close();
