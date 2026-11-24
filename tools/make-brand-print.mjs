// The GEMIS print and social pieces: letterhead (PDF + Word), LinkedIn banner, business cards.
//
//   node tools/make-brand-print.mjs
//
// Writes:
//   brand/letterhead/GEMIS-Letterhead.pdf        A4, page 1 + continuation page, vector
//   brand/letterhead/GEMIS-Letterhead.docx       Word template on the same artwork, Montserrat embedded
//   brand/letterhead/letterhead-page-{1,2}.png   previews
//   brand/linkedin/GEMIS-LinkedIn-Banner.png     1128×191 (LinkedIn's company cover size)
//   brand/linkedin/GEMIS-LinkedIn-Banner@2x.png  2256×382, for sharp high-density screens
//   brand/business-cards/<slug>.pdf              print file: front + back, 90×50 mm trim + 3 mm bleed
//   brand/business-cards/<slug>-front.png / -back.png   previews at trim
//   brand/business-cards/all.png                 every card on one sheet
//
// The language is the site's: midnight navy #0a1230 and white, Montserrat, the vertical
// hatch, the dotted field, the light streaks, the isometric block cluster (cluster() in
// scripts/build-stories.py), stepped blocks with a notch, "+" lists on hairlines and
// uppercase light headings. Every fact is from the site: the legal name, the address
// and info@ from contact.html, the slogan, the figures from scripts/facts.md. No phone
// number anywhere (the owner's rule). The team comes from brand/staff.json.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const R = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const STAFF = JSON.parse(fs.readFileSync(path.join(R, 'brand/staff.json'), 'utf8'));

const NAVY = '#0a1230', INK = '#1b2038', MUTE = '#4a5068', FAINT = '#7a7f93', LINE = '#d9dce5', SOFT = '#aeb3c7';
const CO = {
  legal: 'GEM Information Systems (Pty) Ltd',
  street: '9 Tapiola Way, Edgemead',
  city: 'Cape Town',
  email: 'info@gemis.co.za',
  web: 'www.gemis.co.za',
  slogan: ['Systems built to last.', 'Partners built to stay.'],
};

// ---- the shared art ---------------------------------------------------------------
const inner = (f) => fs.readFileSync(path.join(R, f), 'utf8').replace(/<svg[^>]*>/, '').replace('</svg>', '').trim();
const MARK = inner('assets/img/logos/gemis-mark.svg');      // viewBox 0 0 64 64
const LOGO = inner('assets/img/logos/gemis-logo.svg');      // viewBox 0 0 234.6 40
const CLUSTER = execFileSync('python3', ['-c', `
import importlib.util
s = importlib.util.spec_from_file_location('B', 'scripts/build-stories.py'); B = importlib.util.module_from_spec(s); s.loader.exec_module(B)
print(B.cluster())`], { cwd: R, encoding: 'utf8' }).replace(/<svg[^>]*>/, '').replace('</svg>', '').replace(/ class="[^"]*"/g, '').trim();
// the static cuts in brand/fonts, so the print PDFs embed TrueType rather than Type 3 outlines
const FACES = [[200, 'ExtraLight'], [300, 'Light'], [400, 'Regular'], [500, 'Medium'], [600, 'SemiBold']]
  .map(([w, n]) => `@font-face{font-family:Montserrat;src:url(${pathToFileURL(path.join(R, 'brand/fonts', `Montserrat-${n}.ttf`)).href}) format("truetype");font-weight:${w}}`).join('');

let uid = 0;
/** The pattern defs, sized for the unit the drawing uses (mm for print, px for screen). */
function defs(u) {
  const id = ++uid;
  const ids = { hatch: `h${id}`, dots: `d${id}`, streak: `s${id}` };
  const svg = `<defs>
    <pattern id="${ids.hatch}" width="${u.hatch}" height="${u.hatch}" patternUnits="userSpaceOnUse"><rect width="${u.line}" height="${u.hatch}" fill="#fff" opacity="${u.hatchOp ?? .085}"/></pattern>
    <pattern id="${ids.dots}" width="${u.dot}" height="${u.dot}" patternUnits="userSpaceOnUse"><circle cx="${u.dot / 6}" cy="${u.dot / 6}" r="${u.dotR}" fill="#fff" opacity=".34"/></pattern>
    <linearGradient id="${ids.streak}" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  </defs>`;
  return { svg, ...ids };
}
const logo = (x, y, w, fill) => `<svg x="${x}" y="${y}" width="${w}" height="${w * 40 / 234.6}" viewBox="0 0 234.6 40" fill="${fill}">${LOGO}</svg>`;
const mark = (x, y, w, fill) => `<svg x="${x}" y="${y}" width="${w}" height="${w}" viewBox="0 0 64 64" fill="${fill}">${MARK}</svg>`;
const cluster = (x, y, w, op = 1) => `<svg x="${x}" y="${y}" width="${w}" height="${w * 560 / 600}" viewBox="0 0 600 560" opacity="${op}">${CLUSTER}</svg>`;
const initials = (p) => p.name.split(/\s+/).slice(0, 2).map((w) => w[0]).join('').toUpperCase();

const page = (w, h, unit, body, extra = '') => `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
${FACES}
@page{size:${w}${unit} ${h}${unit};margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:transparent}
body{font-family:Montserrat,Arial,sans-serif;color:${INK};-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{position:relative;width:${w}${unit};height:${h}${unit};overflow:hidden;break-after:page}
.pg:last-child{break-after:auto}
.pg>svg{position:absolute;inset:0;width:100%;height:100%}
.t{position:absolute;margin:0;white-space:nowrap}
.lab{text-transform:uppercase;letter-spacing:.18em;font-weight:500}
${extra}
</style></head><body>${body}</body></html>`;

// ---- letterhead (A4, millimetres) ----------------------------------------------------
function letterFirst(withWhite = true) {
  const d = defs({ hatch: 1.5, line: .2, dot: 2.4, dotR: .2 });
  // the corner block bleeds off the top and the right; its step is cut bottom left
  const corner = 'M126 0H210V54H142V44H126Z';
  // the foot band bleeds off three edges; its right end steps up
  const foot = 'M0 271H128V262H210V297H0Z';
  return `<div class="pg">${withWhite ? '' : ''}<svg viewBox="0 0 210 297" xmlns="http://www.w3.org/2000/svg">${d.svg}
    <clipPath id="lc1"><path d="${corner}"/></clipPath><clipPath id="lf1"><path d="${foot}"/></clipPath>
    <g clip-path="url(#lc1)">
      <rect width="210" height="297" fill="${NAVY}"/><rect width="210" height="297" fill="url(#${d.hatch})"/>
      <rect x="126" y="30" width="34" height="14" fill="url(#${d.dots})"/>
      ${cluster(166, 2, 50)}
      <g fill="none" stroke="url(#${d.streak})" stroke-width=".3"><path d="M120 62L216 -6"/><path d="M134 66L222 4" opacity=".55"/></g>
    </g>
    <path d="${corner}" fill="none" stroke="${NAVY}" stroke-width=".01"/>
    ${logo(20, 17, 66, NAVY)}
    <rect x="20" y="36.5" width="10" height=".7" fill="${NAVY}"/>
    <g stroke="${NAVY}" stroke-opacity=".35" stroke-width=".25"><path d="M0 99H5"/><path d="M0 148.5H3"/><path d="M0 198H5"/></g>
    <g clip-path="url(#lf1)">
      <rect width="210" height="297" fill="${NAVY}"/><rect width="210" height="297" fill="url(#${d.hatch})"/>
      <rect x="96" y="281" width="32" height="16" fill="url(#${d.dots})"/>
      ${cluster(156, 250, 48, .8)}
      <g fill="none" stroke="url(#${d.streak})" stroke-width=".3"><path d="M110 300L196 252"/></g>
    </g>
  </svg>
  <p class="t lab" style="left:20mm;top:39.6mm;font-size:6.2pt;color:${FAINT}">${CO.city}&nbsp;&nbsp;·&nbsp;&nbsp;Since 2014</p>
  <p class="t lab" style="left:132mm;top:13mm;font-size:6.2pt;color:#fff;font-weight:600;line-height:1.7">${CO.slogan[0]}<br><span style="color:${SOFT};font-weight:400">${CO.slogan[1]}</span></p>
  <p class="t" style="left:20mm;top:277.6mm;font-size:7.6pt;color:#fff;letter-spacing:.01em">
    <span style="font-weight:300;margin-right:1.6mm">+</span>${CO.street}, ${CO.city}<span style="display:inline-block;width:7mm"></span><span style="font-weight:300;margin-right:1.6mm">+</span>${CO.email}<span style="display:inline-block;width:7mm"></span><span style="font-weight:300;margin-right:1.6mm">+</span>${CO.web}</p>
  <p class="t lab" style="left:20mm;top:286.2mm;font-size:5.6pt;color:${SOFT}">${CO.legal}</p>
  </div>`;
}

function letterNext() {
  const d = defs({ hatch: 1.5, line: .2, dot: 2.4, dotR: .2 });
  const tab = 'M174 0H210V20H186V12H174Z';
  return `<div class="pg"><svg viewBox="0 0 210 297" xmlns="http://www.w3.org/2000/svg">${d.svg}
    <clipPath id="ln1"><path d="${tab}"/></clipPath>
    <g clip-path="url(#ln1)"><rect width="210" height="297" fill="${NAVY}"/><rect width="210" height="297" fill="url(#${d.hatch})"/>
      <g fill="none" stroke="url(#${d.streak})" stroke-width=".3"><path d="M170 24L214 -4"/></g></g>
    ${logo(20, 12, 42, NAVY)}
    <path d="M20 26H190" stroke="${LINE}" stroke-width=".25"/>
    <g stroke="${NAVY}" stroke-opacity=".35" stroke-width=".25"><path d="M0 99H5"/><path d="M0 148.5H3"/><path d="M0 198H5"/></g>
    <rect x="0" y="287" width="210" height="10" fill="${NAVY}"/><rect x="0" y="287" width="210" height="10" fill="url(#${d.hatch})"/>
  </svg>
  <p class="t" style="left:20mm;top:290.3mm;font-size:6.6pt;color:#fff">
    <span style="font-weight:300;margin-right:1.4mm">+</span>${CO.street}, ${CO.city}<span style="display:inline-block;width:6mm"></span><span style="font-weight:300;margin-right:1.4mm">+</span>${CO.email}<span style="display:inline-block;width:6mm"></span><span style="font-weight:300;margin-right:1.4mm">+</span>${CO.web}</p>
  </div>`;
}

// ---- LinkedIn banner (pixels) ----------------------------------------------------------
function banner() {
  const d = defs({ hatch: 6, line: 1, dot: 9, dotR: .9 });
  // the white stepped block on the right carries the confirmed figures; its notch is top left
  const block = 'M846 0H1128V191H812V34H846Z';
  const fig = (x, n, l1, l2) => `<p class="t" style="left:${x}px;top:62px;font-size:34px;font-weight:200;color:${NAVY};letter-spacing:-.02em;line-height:1">${n}</p>
    <p class="t lab" style="left:${x + 1}px;top:106px;font-size:8.5px;line-height:1.55;color:${MUTE}">${l1}<br>${l2}</p>`;
  return `<div class="pg"><svg viewBox="0 0 1128 191" xmlns="http://www.w3.org/2000/svg">${d.svg}
    <rect width="1128" height="191" fill="${NAVY}"/><rect width="1128" height="191" fill="url(#${d.hatch})"/>
    <rect x="0" y="0" width="250" height="191" fill="url(#${d.dots})" opacity=".55"/>
    <g fill="none" stroke="url(#${d.streak})" stroke-width="1.2"><path d="M80 230L560 -40"/><path d="M150 236L640 -40" opacity=".5"/></g>
    ${cluster(632, -40, 236, .85)}
    <path d="${block}" fill="#fff"/>
    <path d="M846 0V34H812" fill="none" stroke="#fff" stroke-opacity=".35"/>
    <path d="M840 150H1100" stroke="${LINE}"/>
  </svg>
  <p class="t lab" style="left:232px;top:52px;font-size:10px;color:${SOFT}">GEM Information Systems&nbsp;&nbsp;·&nbsp;&nbsp;Cape Town</p>
  <p class="t" style="left:230px;top:74px;font-size:28px;line-height:1.18;font-weight:300;letter-spacing:.07em;text-transform:uppercase;color:#fff">${CO.slogan[0]}<br><span style="color:${SOFT};font-weight:200">${CO.slogan[1]}</span></p>
  ${fig(840, '50+', 'Systems', 'delivered')}${fig(934, '5+', 'Sectors', 'served')}${fig(1018, '2014', 'Founded', 'Cape Town')}
  <p class="t lab" style="left:840px;top:160px;font-size:9px;color:${NAVY};font-weight:600">${CO.web}</p>
  </div>`;
}

// ---- business cards (90×50 mm trim + 3 mm bleed = 96×56; trim box starts at 3,3) ----
function cardFront() {
  const d = defs({ hatch: 1.1, line: .14, dot: 1.8, dotR: .15 });
  return `<div class="pg"><svg viewBox="0 0 96 56" xmlns="http://www.w3.org/2000/svg">${d.svg}
    <rect width="96" height="56" fill="${NAVY}"/><rect width="96" height="56" fill="url(#${d.hatch})"/>
    <rect x="0" y="36" width="34" height="20" fill="url(#${d.dots})"/>
    <g fill="none" stroke="url(#${d.streak})" stroke-width=".22"><path d="M40 62L102 0"/><path d="M50 64L110 4" opacity=".5"/></g>
    ${cluster(56, 12, 42)}
    <path d="M77 0H96V14H77Z" fill="#fff"/>
    ${logo(11, 21, 44, '#fff')}
  </svg>
  <p class="t lab" style="left:11.4mm;top:40.6mm;font-size:4.3pt;line-height:1.75;color:#fff;font-weight:600;letter-spacing:.2em">${CO.slogan[0]}<br><span style="color:${SOFT};font-weight:400">${CO.slogan[1]}</span></p>
  </div>`;
}

function cardBack(p) {
  const d = defs({ hatch: 1.1, line: .14, dot: 1.8, dotR: .15 });
  // the navy column bleeds off the top, right and bottom; its notch is cut top left
  const col = 'M77 0H96V56H67V11H77Z';
  const row = (top, txt) => `<p class="t" style="left:11mm;top:${top}mm;width:52mm;font-size:6.1pt;color:${NAVY};border-top:.2mm solid ${LINE};padding-top:1.5mm"><span style="font-weight:300;display:inline-block;width:3mm">+</span>${txt}</p>`;
  return `<div class="pg"><svg viewBox="0 0 96 56" xmlns="http://www.w3.org/2000/svg">${d.svg}
    <rect width="96" height="56" fill="#fff"/>
    <clipPath id="cb${uid}"><path d="${col}"/></clipPath>
    <g clip-path="url(#cb${uid})"><rect width="96" height="56" fill="${NAVY}"/><rect width="96" height="56" fill="url(#${d.hatch})"/>
      <rect x="67" y="34" width="12" height="22" fill="url(#${d.dots})"/>
      <g fill="none" stroke="url(#${d.streak})" stroke-width=".22"><path d="M64 60L100 22"/></g>
      ${mark(81.5, 4.6, 7.6, '#fff')}
    </g>
  </svg>
  <p class="t" style="left:68.6mm;top:31mm;width:25mm;text-align:center;font-size:25pt;font-weight:200;letter-spacing:-.05em;color:#fff;line-height:1">${initials(p)}</p>
  <p class="t" style="left:11mm;top:10.6mm;font-size:10.2pt;font-weight:300;letter-spacing:.08em;text-transform:uppercase;color:${NAVY}">${p.name}</p>
  <span style="position:absolute;left:11mm;top:16.9mm;width:6mm;height:.55mm;background:${NAVY}"></span>
  <p class="t lab" style="left:11mm;top:18.9mm;font-size:5pt;color:${MUTE}">${p.role}</p>
  ${row(25.8, p.email)}${row(31.2, CO.web)}${row(36.6, `${CO.street}, ${CO.city}`)}
  </div>`;
}

// ---- render -----------------------------------------------------------------------------
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'brand-'));
const b = await chromium.launch();
const ctx = await b.newContext({ deviceScaleFactor: 1 });
const tab = await ctx.newPage();
async function load(p, html) {
  const f = path.join(TMP, `p${++uid}.html`);
  fs.writeFileSync(f, html);
  await p.goto(pathToFileURL(f).href);
  await p.evaluate(() => document.fonts.ready);
}
async function shot(html, out, w, h, scale, opts = {}) {
  const c = await b.newContext({ viewport: { width: Math.round(w), height: Math.round(h) }, deviceScaleFactor: scale });
  const p = await c.newPage(); await load(p, html);
  await p.screenshot({ path: out, clip: { x: 0, y: 0, width: w, height: h }, ...opts });
  await c.close();
}
const mm = (v) => v * 96 / 25.4;
const out = (...a) => { const f = path.join(R, 'brand', ...a); fs.mkdirSync(path.dirname(f), { recursive: true }); return f; };

// letterhead
const LH = page(210, 297, 'mm', letterFirst() + letterNext());
await load(tab, LH);
await tab.pdf({ path: out('letterhead', 'GEMIS-Letterhead.pdf'), width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true });
const ART1 = path.join(TMP, 'lh1.png'), ART2 = path.join(TMP, 'lh2.png');
await shot(page(210, 297, 'mm', letterFirst()), ART1, mm(210), mm(297), 300 / 96, { omitBackground: true });
await shot(page(210, 297, 'mm', letterNext()), ART2, mm(210), mm(297), 300 / 96, { omitBackground: true });
await shot(page(210, 297, 'mm', letterFirst(), 'body{background:#fff}'), out('letterhead', 'letterhead-page-1.png'), mm(210), mm(297), 1.5);
await shot(page(210, 297, 'mm', letterNext(), 'body{background:#fff}'), out('letterhead', 'letterhead-page-2.png'), mm(210), mm(297), 1.5);

// LinkedIn
await shot(page(1128, 191, 'px', banner()), out('linkedin', 'GEMIS-LinkedIn-Banner.png'), 1128, 191, 1);
await shot(page(1128, 191, 'px', banner()), out('linkedin', 'GEMIS-LinkedIn-Banner@2x.png'), 1128, 191, 2);

// business cards
const trim = { x: mm(3), y: mm(3), width: mm(90), height: mm(50) };
const previews = [];
for (const p of STAFF) {
  const html = page(96, 56, 'mm', cardFront() + cardBack(p));
  await load(tab, html);
  await tab.pdf({ path: out('business-cards', `${p.slug}.pdf`), width: '96mm', height: '56mm', printBackground: true, preferCSSPageSize: true });
  for (const [side, body] of [['front', cardFront()], ['back', cardBack(p)]]) {
    const f = out('business-cards', `${p.slug}-${side}.png`);
    const c = await b.newContext({ viewport: { width: Math.ceil(mm(96)), height: Math.ceil(mm(56)) }, deviceScaleFactor: 600 / 96 });
    const pg = await c.newPage(); await load(pg, page(96, 56, 'mm', body));
    await pg.screenshot({ path: f, clip: trim }); await c.close();
    previews.push(f);
  }
}
// one sheet with every card, front and back, for review
const cells = previews.map((f) => `<img src="${pathToFileURL(f).href}" style="width:450px;height:250px;display:block;box-shadow:0 10px 30px rgba(10,18,48,.18)">`).join('');
await shot(`<!DOCTYPE html><html><body style="margin:0;background:#e9ebf1"><div style="display:grid;grid-template-columns:450px 450px;gap:40px;padding:60px">${cells}</div></body></html>`,
  out('business-cards', 'all.png'), 1060, 60 * 2 + STAFF.length * 250 + (STAFF.length - 1) * 40, 1);
await b.close();

// ---- Word letterhead --------------------------------------------------------------------
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, ImageRun, Header, Footer, AlignmentType, CharacterSet,
  HorizontalPositionRelativeFrom, VerticalPositionRelativeFrom, TextWrappingType } = D;
const font = (n) => fs.readFileSync(path.join(R, 'brand/fonts', `Montserrat-${n}.ttf`));
const art = (f) => new ImageRun({
  type: 'png', data: fs.readFileSync(f), transformation: { width: 794, height: 1123 },
  floating: {
    horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, offset: 0 },
    verticalPosition: { relative: VerticalPositionRelativeFrom.PAGE, offset: 0 },
    behindDocument: true, allowOverlap: true, lockAnchor: true, wrap: { type: TextWrappingType.NONE },
  },
  altText: { name: 'GEMIS letterhead', description: 'GEMIS letterhead artwork', title: 'GEMIS letterhead' },
});
const tw = (v) => Math.round(v * 1440 / 25.4);
const P = (text, o = {}) => new Paragraph({ spacing: { after: o.after ?? 0, before: o.before ?? 0, line: o.line ?? 300 }, children: [new TextRun({ text, font: o.font ?? 'Montserrat', size: o.size ?? 19, color: o.color ?? INK.slice(1), characterSpacing: o.cs, allCaps: o.caps })] });
const doc = new Document({
  creator: 'GEM Information Systems', title: 'GEMIS letterhead', description: 'GEMIS letterhead template',
  fonts: ['Regular', 'Light', 'SemiBold', 'Medium'].map((n) => ({ name: n === 'Regular' ? 'Montserrat' : `Montserrat ${n}`, data: font(n), characterSet: CharacterSet.ANSI })),
  styles: { default: { document: { run: { font: 'Montserrat', size: 19, color: INK.slice(1) }, paragraph: { spacing: { line: 300, after: 160 } } } } },
  sections: [{
    properties: {
      titlePage: true,
      page: { size: { width: tw(210), height: tw(297) }, margin: { top: tw(36), bottom: tw(42), left: tw(20.8), right: tw(20), header: 0, footer: 0 } },
    },
    // page 1 opens lower, under the corner block: a spacer in its header pushes the text down to 62 mm;
    // continuation pages keep the 36 mm margin under their slim header
    headers: { first: new Header({ children: [new Paragraph({ children: [art(ART1)] }), new Paragraph({ spacing: { before: tw(57), after: 0, line: 240 }, children: [] })] }), default: new Header({ children: [new Paragraph({ children: [art(ART2)] })] }) },
    footers: { first: new Footer({ children: [new Paragraph('')] }), default: new Footer({ children: [new Paragraph('')] }) },
    children: [
      P('[Date]', { after: 360, size: 17, color: MUTE.slice(1), font: 'Montserrat Medium', cs: 30, caps: true }),
      P('[Recipient name]', { font: 'Montserrat SemiBold' }),
      P('[Position]'), P('[Company]'), P('[Street address]'), P('[City, postal code]', { after: 440 }),
      P('Re: [Subject of the letter]', { after: 360, size: 17, font: 'Montserrat SemiBold', color: NAVY.slice(1), cs: 40, caps: true }),
      P('Dear [Name],', { after: 200 }),
      P('[Write the letter here. The body is Montserrat at 9.5 pt on generous leading, set flush with the logo, so a page reads cleanly and prints sharply.]', { after: 200, line: 320 }),
      P('[A second paragraph. Keep to one subject per paragraph, and let the white space do the work.]', { after: 440, line: 320 }),
      P('Kind regards,', { after: 720 }),
      P('[Your name]', { font: 'Montserrat SemiBold', size: 21, color: NAVY.slice(1) }),
      P('[Your role]  ·  GEMIS', { size: 15, font: 'Montserrat Medium', color: MUTE.slice(1), cs: 30, caps: true, after: 60 }),
      P('[you]@gemis.co.za', { size: 17, color: NAVY.slice(1) }),
    ],
  }],
});
// keep the fonts embedded when someone saves an edited letter (embedTrueTypeFonts sits right after
// displayBackgroundShape in the settings schema), and write the archive without folder entries
const JSZip = createRequire(require.resolve('docx'))('jszip');
const zip = await JSZip.loadAsync(await Packer.toBuffer(doc));
const settings = (await zip.file('word/settings.xml').async('string')).replace('<w:displayBackgroundShape/>', '<w:displayBackgroundShape/><w:embedTrueTypeFonts/>');
zip.file('word/settings.xml', settings);
// the schema's ST_Guid is upper-case hex; docx-js writes lower case (the key bytes are the same)
const fonts = (await zip.file('word/fontTable.xml').async('string')).replace(/w:fontKey="(\{[^}]+\})"/g, (m, k) => `w:fontKey="${k.toUpperCase()}"`);
zip.file('word/fontTable.xml', fonts);
const flat = new JSZip();
for (const [n, f] of Object.entries(zip.files)) if (!f.dir) flat.file(n, await f.async('uint8array'), { createFolders: false });
fs.writeFileSync(out('letterhead', 'GEMIS-Letterhead.docx'), await flat.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' }));
fs.rmSync(TMP, { recursive: true, force: true });
console.log('letterhead, linkedin, business cards:', STAFF.map((p) => p.slug).join(', '));
