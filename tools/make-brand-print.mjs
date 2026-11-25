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
const face = (fam, file, w) => `@font-face{font-family:'${fam}';src:url(${pathToFileURL(path.join(R, 'brand/fonts', `${file}.ttf`)).href}) format("truetype");font-weight:${w}}`;
const FACES = [[200, 'ExtraLight'], [300, 'Light'], [400, 'Regular'], [500, 'Medium'], [600, 'SemiBold']].map(([w, n]) => face('Montserrat', `Montserrat-${n}`, w)).join('')
  + [[300, 'Light'], [400, 'Regular'], [500, 'Medium'], [600, 'SemiBold']].map(([w, n]) => face('Manrope', `Manrope-${n}`, w)).join('')
  + [[400, 'Regular'], [500, 'Medium']].map(([w, n]) => face('JetBrains Mono', `JetBrainsMono-${n}`, w)).join('');

let uid = 0;
/** The pattern defs, sized for the unit the drawing uses (mm for print, px for screen). */
function defs(u) {
  const id = ++uid;
  const ids = { hatch: `h${id}`, dots: `d${id}`, streak: `s${id}` };
  const svg = `<defs>
    <pattern id="${ids.hatch}" width="${u.hatch}" height="${u.hatch}" patternUnits="userSpaceOnUse"><rect width="${u.line}" height="${u.hatch}" fill="${u.ink ?? '#fff'}" opacity="${u.hatchOp ?? .085}"/></pattern>
    <pattern id="${ids.dots}" width="${u.dot}" height="${u.dot}" patternUnits="userSpaceOnUse"><circle cx="${u.dot / 6}" cy="${u.dot / 6}" r="${u.dotR}" fill="${u.ink ?? '#fff'}" opacity=".34"/></pattern>
    <linearGradient id="${ids.streak}" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="${u.ink ?? '#fff'}" stop-opacity="0"/><stop offset=".5" stop-color="${u.ink ?? '#fff'}" stop-opacity=".5"/><stop offset="1" stop-color="${u.ink ?? '#fff'}" stop-opacity="0"/></linearGradient>
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

// ---- meeting backgrounds (Zoom, Teams: 1920×1080) -----------------------------------------
// The person sits in the middle third and covers it from the shoulders down, so the brand
// lives at the edges: the logo top left (with the name and role on a personal copy), the
// block cluster bleeding off the right, the slogan bottom left, the site bottom right.
// Video compression shimmers on hairlines, so the hatch here is coarse and faint and every
// stroke is at least 2px. Navy is the team standard; light is for dark rooms or dark clothes.
function meeting(p, tone) {
  const dark = tone === 'navy';
  const d = defs({ hatch: 16, line: 2, dot: 22, dotR: 2, hatchOp: .045 });
  const fg = dark ? '#fff' : NAVY, sub = dark ? SOFT : MUTE;
  // the light version carries a navy stepped block on the right, which holds the cluster
  const block = 'M1460 0H1920V1080H1330V150H1460Z';
  const who = p ? `<span style="position:absolute;left:100px;top:224px;width:48px;height:3px;background:${fg}"></span>
  <p class="t" style="left:99px;top:248px;font-size:40px;font-weight:300;letter-spacing:.08em;text-transform:uppercase;color:${fg}">${p.name}</p>
  <p class="t lab" style="left:102px;top:308px;font-size:19px;color:${sub}">${p.role}</p>` : '';
  return `<div class="pg"><svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">${d.svg}
    <rect width="1920" height="1080" fill="${dark ? NAVY : '#f4f5f8'}"/>
    ${dark ? `<rect width="1920" height="1080" fill="url(#${d.hatch})"/>` : `<path d="${block}" fill="${NAVY}"/><clipPath id="mb${uid}"><path d="${block}"/></clipPath>`}
    <g ${dark ? '' : `clip-path="url(#mb${uid})"`}>
      ${dark ? '' : `<rect width="1920" height="1080" fill="url(#${d.hatch})"/>`}
      <g fill="none" stroke="url(#${d.streak})" stroke-width="2.5"><path d="M1060 1180L2040 260"/><path d="M1210 1200L2080 380" opacity=".5"/></g>
      ${cluster(1380, 250, 700, dark ? .9 : 1)}
    </g>
    ${dark ? `<rect x="0" y="640" width="330" height="264" fill="url(#${d.dots})" opacity=".5"/>` : ''}
    ${dark ? `<path d="M1808 0H1920V60H1808Z" fill="#fff" opacity=".92"/>` : ''}
    ${logo(100, 92, 440, fg)}
  </svg>
  ${who}
  <p class="t lab" style="left:102px;top:950px;font-size:16px;line-height:1.75;color:${fg};font-weight:600">${CO.slogan[0]}<br><span style="color:${sub};font-weight:400">${CO.slogan[1]}</span></p>
  <p class="t lab" style="right:96px;top:994px;font-size:16px;color:${dark ? SOFT : '#fff'};font-weight:500">${CO.web}</p>
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

// ---- the studio letterhead (A4, millimetres) ---------------------------------------------
// The studio's own language: white paper, the coloured stone and GEMIS STUDIO, Manrope
// for words and JetBrains Mono for labels, the pink and orange faceted shards and the
// outlined triangle from its hero, the dot grid, and the "E." / "W." / "A." contact keys.
const ST = { ink: '#16161a', ink2: '#6a6b73', line: '#dcdee3', ground: '#eef0f3', pink: '#ff1f7a', orange: '#ff7a12', deepPink: '#d70057' };
const STUDIO_LOGO = inner('studio/assets/gemis-studio-logo.svg');   // viewBox 0 0 240.1 72
const STUDIO_MARK = inner('studio/assets/mark-colour.svg');         // viewBox 0 0 64 64
const studioLogo = (x, y, w) => `<svg x="${x}" y="${y}" width="${w}" height="${w * 72 / 240.1}" viewBox="0 0 240.1 72">${STUDIO_LOGO}</svg>`;
const studioMark = (x, y, w) => `<svg x="${x}" y="${y}" width="${w}" height="${w}" viewBox="0 0 64 64">${STUDIO_MARK}</svg>`;
function shardDefs(k) {
  return `<defs>
    <linearGradient id="so${k}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffb27a"/><stop offset="1" stop-color="${ST.orange}"/></linearGradient>
    <linearGradient id="sp${k}" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${ST.pink}"/><stop offset="1" stop-color="#ff8fbb"/></linearGradient>
    <linearGradient id="sw${k}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#d9dbe1"/></linearGradient>
    <linearGradient id="sg${k}" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${ST.ground}"/><stop offset="1" stop-color="${ST.ground}" stop-opacity="0"/></linearGradient>
    <pattern id="sd${k}" width="5" height="5" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r=".42" fill="#c9cad1"/></pattern>
  </defs>`;
}
const studioFoot = (y) => {
  const key = (k, v) => `<span style="font-family:'JetBrains Mono';color:${ST.pink};margin-right:1.8mm">${k}</span>${v}`;
  return `<p class="t" style="left:20mm;top:${y}mm;font-family:Manrope;font-size:7.6pt;color:${ST.ink}">${key('E.', CO.email)}<span style="display:inline-block;width:7mm"></span>${key('W.', CO.web)}<span style="display:inline-block;width:7mm"></span>${key('A.', `${CO.street}, ${CO.city}`)}</p>`;
};
function studioFirst() {
  const k = ++uid;
  return `<div class="pg"><svg viewBox="0 0 210 297" xmlns="http://www.w3.org/2000/svg">${shardDefs(k)}
    <path d="M104 0H210V92Z" fill="url(#sg${k})"/>
    <rect x="186" y="62" width="20" height="44" fill="url(#sd${k})"/>
    <g>
      <polygon points="132,14 194,40 166,52" fill="url(#so${k})"/>
      <polygon points="166,52 194,40 186,66" fill="url(#sw${k})"/>
      <polygon points="176,0 210,0 210,44 194,40" fill="url(#sp${k})"/>
      <polygon points="194,40 210,44 210,70" fill="#ffc2da"/>
      <polygon points="146,0 176,0 160,12" fill="url(#sw${k})"/>
      <polygon points="138,44 156,70 128,64" fill="none" stroke="${ST.pink}" stroke-opacity=".55" stroke-width=".3"/>
      <polygon points="112,6 124,24 104,20" fill="none" stroke="${ST.orange}" stroke-opacity=".45" stroke-width=".25"/>
      <circle cx="122" cy="40" r="1.7" fill="${ST.orange}"/>
    </g>
    ${studioLogo(20, 16, 52)}
    <rect x="20" y="51" width="12" height=".7" fill="${ST.orange}"/>
    <g stroke="${ST.ink}" stroke-opacity=".3" stroke-width=".25"><path d="M0 99H5"/><path d="M0 148.5H3"/><path d="M0 198H5"/></g>
    <g>
      <polygon points="0,264 15,297 0,297" fill="url(#sp${k})"/>
      <polygon points="0,284 6,297 0,297" fill="#ffc2da"/>
      <polygon points="7,244 14,256 3,255" fill="none" stroke="${ST.orange}" stroke-opacity=".5" stroke-width=".25"/>
    </g>
    <path d="M20 274H190" stroke="${ST.line}" stroke-width=".25"/>
    ${studioMark(183, 278.2, 7)}
  </svg>
  <p class="t" style="left:20mm;top:37.4mm;font-family:Manrope;font-weight:600;font-size:11.5pt;letter-spacing:-.02em;color:${ST.ink}">Designed to be <span style="color:${ST.pink}">built.</span></p>
  <p class="t" style="left:20mm;top:44.2mm;font-family:'JetBrains Mono';font-size:6pt;letter-spacing:.08em;text-transform:uppercase;color:${ST.ink2}">The design practice of GEM Information Systems</p>
  ${studioFoot(278.4)}
  <p class="t" style="left:20mm;top:285.6mm;font-family:'JetBrains Mono';font-size:5.6pt;letter-spacing:.08em;text-transform:uppercase;color:${ST.ink2}">GEMIS Studio&nbsp;&nbsp;·&nbsp;&nbsp;${CO.legal}</p>
  </div>`;
}
function studioNext() {
  const k = ++uid;
  return `<div class="pg"><svg viewBox="0 0 210 297" xmlns="http://www.w3.org/2000/svg">${shardDefs(k)}
    <polygon points="182,0 210,0 210,24" fill="url(#sp${k})"/>
    <polygon points="170,0 182,0 176,8" fill="url(#so${k})"/>
    <polygon points="196,12 210,24 210,36" fill="#ffc2da"/>
    ${studioLogo(20, 12, 34)}
    <path d="M20 27H190" stroke="${ST.line}" stroke-width=".25"/>
    <g stroke="${ST.ink}" stroke-opacity=".3" stroke-width=".25"><path d="M0 99H5"/><path d="M0 148.5H3"/><path d="M0 198H5"/></g>
    <path d="M20 282H190" stroke="${ST.line}" stroke-width=".25"/>
    ${studioMark(184, 285.4, 6)}
  </svg>
  ${studioFoot(285.8)}
  </div>`;
}

// ---- personal LinkedIn banners (a profile cover is 1584×396 px) ---------------------------
// Built to the published guidance for profile covers (docs/LINKEDIN-BANNERS.md):
//  · one message, not a business card. LinkedIn prints the name and the headline under the
//    cover, so the cover does not repeat them and carries no contact details. The message is
//    what this person does at GEMIS (their confirmed line on Our Story, `focus` in
//    brand/staff.json), set in the slogan's two-line rhythm, with the slogan beneath.
//  · the safe zone. The profile photo covers the lower left (about 568×264 px of it, more on
//    a phone) and narrow screens trim the ends, so the logo, the message and the slogan sit
//    between x 620 and 1270, in the upper three quarters. The left carries only the pattern;
//    the white stepped block on the right holds the person's pictogram and the site, and
//    nothing is lost if it is trimmed.
//  · legible small. A phone shows the cover about 400 px wide, so the message is set large
//    (up to 46 px here) and shrinks only to fit the column.
const PICTOS = JSON.parse(execFileSync('python3', ['-c', `
import importlib.util, json
s = importlib.util.spec_from_file_location('B', 'scripts/build-stories.py'); B = importlib.util.module_from_spec(s); s.loader.exec_module(B)
print(json.dumps(B.PICTO))`], { cwd: R, encoding: 'utf8' }));
function personalBanner(p, tone = 'navy') {
  // navy: the midnight ground with a white block. light: the page's off-white with a navy block,
  // for a profile whose photo is dark or that wants a brighter page.
  const dark = tone === 'navy';
  const bg = dark ? NAVY : '#eef0f5', fg = dark ? '#fff' : NAVY, sub = dark ? SOFT : '#6a7088';
  const blockBg = dark ? '#fff' : NAVY, blockFg = dark ? NAVY : '#fff';
  const d = defs({ hatch: 7, line: 1.2, dot: 11, dotR: 1.1, ink: fg, hatchOp: dark ? .085 : .06 });
  const k = ++uid;
  const block = 'M1340 36H1548V360H1296V88H1340Z';   // the stepped block, inside a frame of the ground
  return `<div class="pg"><svg viewBox="0 0 1584 396" xmlns="http://www.w3.org/2000/svg">${d.svg}
    <pattern id="ph${k}" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="1.3" height="4" fill="${blockFg}"/></pattern>
    <pattern id="bh${k}" width="7" height="7" patternUnits="userSpaceOnUse"><rect width="1.2" height="7" fill="#fff" opacity=".085"/></pattern>
    <rect width="1584" height="396" fill="${bg}"/><rect width="1584" height="396" fill="url(#${d.hatch})"/>
    <rect x="0" y="0" width="550" height="396" fill="url(#${d.dots})" opacity="${dark ? .45 : .5}"/>
    <g fill="none" stroke="url(#${d.streak})" stroke-width="1.6"><path d="M60 470L640 -60"/><path d="M170 480L750 -50" opacity=".5"/></g>
    ${logo(620, 44, 250, fg)}
    <path d="${block}" fill="${blockBg}"/>
    ${dark ? `<path d="M1340 36V88H1296" fill="none" stroke="#fff" stroke-opacity=".35"/>` : `<path d="${block}" fill="url(#bh${k})"/>`}
    <svg x="1346" y="96" width="152" height="152" viewBox="0 0 120 120"><path d="${PICTOS[p.picto]}" fill="url(#ph${k})" fill-rule="evenodd"/></svg>
    <path d="M1326 286H1518" stroke="${dark ? LINE : '#fff'}" stroke-opacity="${dark ? 1 : .3}"/>
    ${dark ? '' : `<rect x="0" y="392" width="1584" height="4" fill="${NAVY}"/>`}
  </svg>
  <p class="t fit" data-max="650" style="left:618px;top:116px;font-size:46px;line-height:1.2;font-weight:300;letter-spacing:.06em;text-transform:uppercase;color:${fg}">${p.focus[0]}<br><span style="color:${sub};font-weight:${dark ? 200 : 300}">${p.focus[1]}</span></p>
  <span style="position:absolute;left:620px;top:252px;width:44px;height:2px;background:${fg}"></span>
  <p class="t lab" style="left:620px;top:272px;font-size:16px;letter-spacing:.15em;color:${fg};font-weight:600">${CO.slogan[0]}&nbsp; <span style="color:${sub};font-weight:${dark ? 400 : 500}">${CO.slogan[1]}</span></p>
  <p class="t lab" style="left:1326px;top:304px;width:192px;text-align:center;font-size:13.5px;letter-spacing:.13em;color:${blockFg};font-weight:600">${CO.web}</p>
  <script>document.fonts.ready.then(() => document.querySelectorAll('.fit').forEach((el) => { let s = parseFloat(el.style.fontSize); while (el.offsetWidth > +el.dataset.max && s > 28) el.style.fontSize = (s -= 1) + 'px'; }));</script>
  </div>`;
}

// ---- the studio LinkedIn banner (its showcase page, 1128×191 px) --------------------------
// The studio site's hero in a strip: the light ground, the mono label in the deep orange,
// "Designed to be built." with *built.* in pink, the shards and outlined triangles on the
// right with the dot grid, the coloured stone. The lower left stays quiet for the page logo.
function studioBanner() {
  const k = ++uid;
  return `<div class="pg"><svg viewBox="0 0 1128 191" xmlns="http://www.w3.org/2000/svg">${shardDefs(k)}
    <pattern id="bd${k}" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="8" cy="8" r="1.6" fill="#ffffff"/></pattern>
    <linearGradient id="bg${k}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${ST.ground}"/><stop offset="1" stop-color="#e2e4ea"/></linearGradient>
    <rect width="1128" height="191" fill="url(#bg${k})"/>
    <rect x="1048" y="14" width="64" height="150" fill="url(#bd${k})"/>
    <g>
      <polygon points="760,191 862,58 948,191" fill="url(#so${k})"/>
      <polygon points="862,58 948,191 980,108" fill="url(#sw${k})"/>
      <polygon points="940,0 1040,0 1004,96" fill="url(#sp${k})"/>
      <polygon points="1004,96 1040,0 1128,0 1128,70" fill="url(#sw${k})"/>
      <polygon points="1000,191 1088,120 1128,191" fill="url(#sp${k})"/>
      <polygon points="1088,120 1128,100 1128,191" fill="#ffc2da"/>
      <polygon points="792,22 838,60 776,72" fill="none" stroke="${ST.pink}" stroke-opacity=".55" stroke-width="1.5"/>
      <polygon points="880,14 920,40 872,46" fill="none" stroke="${ST.orange}" stroke-opacity=".5" stroke-width="1.5"/>
      <circle cx="748" cy="150" r="5" fill="${ST.orange}"/>
      <circle cx="986" cy="30" r="3.5" fill="${ST.pink}" opacity=".8"/>
    </g>
    ${studioMark(36, 30, 40)}
  </svg>
  <p class="t" style="left:84px;top:34px;font-family:Manrope;font-weight:600;font-size:15px;letter-spacing:.02em;color:${ST.ink};line-height:1.1">GEMIS<br><span style="font-family:'JetBrains Mono';font-weight:400;font-size:9px;letter-spacing:.28em;color:${ST.ink2}">STUDIO</span></p>
  <p class="t" style="left:240px;top:38px;font-family:'JetBrains Mono';font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:#b34e00">UX/UI and product design for digital products that work.</p>
  <p class="t" style="left:237px;top:58px;font-family:Manrope;font-weight:600;font-size:56px;letter-spacing:-.045em;line-height:1;color:${ST.ink}">Designed to be <span style="color:${ST.pink}">built.</span></p>
  <p class="t" style="left:240px;top:136px;font-family:'JetBrains Mono';font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;color:${ST.ink2}">The design practice of GEM Information Systems&nbsp;&nbsp;·&nbsp;&nbsp;Cape Town</p>
  <p class="t" style="left:240px;top:156px;font-family:'JetBrains Mono';font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;color:${ST.ink}">${CO.web.replace('www.', '')}&nbsp;&#8599;</p>
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

// the studio letterhead
const SL = page(210, 297, 'mm', studioFirst() + studioNext());
await load(tab, SL);
await tab.pdf({ path: out('letterhead', 'GEMIS-Studio-Letterhead.pdf'), width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true });
const SART1 = path.join(TMP, 'sl1.png'), SART2 = path.join(TMP, 'sl2.png');
await shot(page(210, 297, 'mm', studioFirst()), SART1, mm(210), mm(297), 300 / 96, { omitBackground: true });
await shot(page(210, 297, 'mm', studioNext()), SART2, mm(210), mm(297), 300 / 96, { omitBackground: true });
await shot(page(210, 297, 'mm', studioFirst(), 'body{background:#fff}'), out('letterhead', 'studio-letterhead-page-1.png'), mm(210), mm(297), 1.5);
await shot(page(210, 297, 'mm', studioNext(), 'body{background:#fff}'), out('letterhead', 'studio-letterhead-page-2.png'), mm(210), mm(297), 1.5);

// meeting backgrounds: the team standard, then a personal copy for each person
for (const tone of ['navy', 'light']) {
  await shot(page(1920, 1080, 'px', meeting(null, tone)), out('meeting-backgrounds', `GEMIS-Meeting-Background-${tone === 'navy' ? 'Navy' : 'Light'}.jpg`), 1920, 1080, 1, { type: 'jpeg', quality: 92 });
  for (const p of STAFF) await shot(page(1920, 1080, 'px', meeting(p, tone)), out('meeting-backgrounds', 'people', `${p.slug}-${tone}.jpg`), 1920, 1080, 1, { type: 'jpeg', quality: 92 });
}

// LinkedIn
await shot(page(1128, 191, 'px', studioBanner()), out('linkedin', 'GEMIS-Studio-LinkedIn-Banner.png'), 1128, 191, 1);
await shot(page(1128, 191, 'px', studioBanner()), out('linkedin', 'GEMIS-Studio-LinkedIn-Banner@2x.png'), 1128, 191, 2);
// personal banners: exactly 1584×396, the size LinkedIn asks for on a profile
for (const p of STAFF) for (const tone of ['navy', 'light']) await shot(page(1584, 396, 'px', personalBanner(p, tone)), out('linkedin', 'people', `${p.slug}-${tone}.png`), 1584, 396, 1);
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
const fontFile = (f) => fs.readFileSync(path.join(R, 'brand/fonts', `${f}.ttf`));
const art = (f, name) => new ImageRun({
  type: 'png', data: fs.readFileSync(f), transformation: { width: 794, height: 1123 },
  floating: {
    horizontalPosition: { relative: HorizontalPositionRelativeFrom.PAGE, offset: 0 },
    verticalPosition: { relative: VerticalPositionRelativeFrom.PAGE, offset: 0 },
    behindDocument: true, allowOverlap: true, lockAnchor: true, wrap: { type: TextWrappingType.NONE },
  },
  altText: { name, description: `${name} artwork`, title: name },
});
const tw = (v) => Math.round(v * 1440 / 25.4);
const JSZip = createRequire(require.resolve('docx'))('jszip');

/** A Word letter template on full-page artwork: page 1 opens at `first` mm (a spacer in its header pushes
 *  the text down), continuation pages at `next` mm under their slim head; the fonts are embedded. */
async function writeWord(file, { title, art1, art2, fonts, run, first, next, bottom, children }) {
  const doc = new Document({
    creator: 'GEM Information Systems', title, description: `${title} template`,
    fonts: fonts.map(([name, f]) => ({ name, data: fontFile(f), characterSet: CharacterSet.ANSI })),
    styles: { default: { document: { run, paragraph: { spacing: { line: 300, after: 160 } } } } },
    sections: [{
      properties: {
        titlePage: true,
        page: { size: { width: tw(210), height: tw(297) }, margin: { top: tw(next), bottom: tw(bottom), left: tw(20.8), right: tw(20), header: 0, footer: 0 } },
      },
      headers: {
        first: new Header({ children: [new Paragraph({ children: [art(art1, title)] }), new Paragraph({ spacing: { before: tw(first - 5), after: 0, line: 240 }, children: [] })] }),
        default: new Header({ children: [new Paragraph({ children: [art(art2, title)] })] }),
      },
      footers: { first: new Footer({ children: [new Paragraph('')] }), default: new Footer({ children: [new Paragraph('')] }) },
      children,
    }],
  });
  // keep the fonts embedded when someone saves an edited letter (embedTrueTypeFonts sits right after
  // displayBackgroundShape in the settings schema), and write the archive without folder entries
  const zip = await JSZip.loadAsync(await Packer.toBuffer(doc));
  zip.file('word/settings.xml', (await zip.file('word/settings.xml').async('string')).replace('<w:displayBackgroundShape/>', '<w:displayBackgroundShape/><w:embedTrueTypeFonts/>'));
  // the schema's ST_Guid is upper-case hex; docx-js writes lower case (the key bytes are the same),
  // and with lower case LibreOffice ignores the embedded fonts
  zip.file('word/fontTable.xml', (await zip.file('word/fontTable.xml').async('string')).replace(/w:fontKey="(\{[^}]+\})"/g, (m, k) => `w:fontKey="${k.toUpperCase()}"`));
  const flat = new JSZip();
  for (const [n, f] of Object.entries(zip.files)) if (!f.dir) flat.file(n, await f.async('uint8array'), { createFolders: false });
  fs.writeFileSync(file, await flat.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' }));
}

// the GEMIS letter
const P = (text, o = {}) => new Paragraph({ spacing: { after: o.after ?? 0, before: o.before ?? 0, line: o.line ?? 300 }, children: [new TextRun({ text, font: o.font ?? 'Montserrat', size: o.size ?? 19, color: o.color ?? INK.slice(1), characterSpacing: o.cs, allCaps: o.caps })] });
await writeWord(out('letterhead', 'GEMIS-Letterhead.docx'), {
  title: 'GEMIS letterhead', art1: ART1, art2: ART2, first: 62, next: 36, bottom: 42,
  fonts: [['Montserrat', 'Montserrat-Regular'], ['Montserrat Light', 'Montserrat-Light'], ['Montserrat SemiBold', 'Montserrat-SemiBold'], ['Montserrat Medium', 'Montserrat-Medium']],
  run: { font: 'Montserrat', size: 19, color: INK.slice(1) },
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
});

// the studio letter: Manrope for words, JetBrains Mono for the labels, the pink for the one accent
const S = (text, o = {}) => new Paragraph({ spacing: { after: o.after ?? 0, before: o.before ?? 0, line: o.line ?? 300 }, children: [].concat(o.runs ?? [new TextRun({ text, font: o.font ?? 'Manrope', size: o.size ?? 19, color: o.color ?? ST.ink.slice(1), characterSpacing: o.cs, allCaps: o.caps })]) });
const mono = (text, color = ST.ink2.slice(1)) => new TextRun({ text, font: 'JetBrains Mono', size: 15, color, characterSpacing: 12, allCaps: true });
await writeWord(out('letterhead', 'GEMIS-Studio-Letterhead.docx'), {
  title: 'GEMIS Studio letterhead', art1: SART1, art2: SART2, first: 64, next: 36, bottom: 30,
  fonts: [['Manrope', 'Manrope-Regular'], ['Manrope SemiBold', 'Manrope-SemiBold'], ['Manrope Medium', 'Manrope-Medium'], ['JetBrains Mono', 'JetBrainsMono-Regular']],
  run: { font: 'Manrope', size: 19, color: ST.ink.slice(1) },
  children: [
    S('', { after: 360, runs: [mono('[Date]')] }),
    S('[Recipient name]', { font: 'Manrope SemiBold' }),
    S('[Position]'), S('[Company]'), S('[Street address]'), S('[City, postal code]', { after: 440 }),
    S('', { after: 80, runs: [mono('Re.', ST.deepPink.slice(1))] }),
    S('[Subject of the letter]', { after: 360, size: 24, font: 'Manrope SemiBold', cs: -6 }),
    S('Dear [Name],', { after: 200 }),
    S('[Write the letter here. The body is Manrope at 9.5 pt on generous leading, set flush with the logo, the same voice as the studio site.]', { after: 200, line: 320 }),
    S('[A second paragraph. Keep to one subject per paragraph, and let the white space do the work.]', { after: 440, line: 320 }),
    S('Kind regards,', { after: 720 }),
    S('[Your name]', { font: 'Manrope SemiBold', size: 21 }),
    S('', { after: 60, runs: [mono('[Your role]  ·  GEMIS Studio')] }),
    S('[you]@gemis.co.za', { size: 17 }),
  ],
});
fs.rmSync(TMP, { recursive: true, force: true });
console.log('letterheads (GEMIS, studio), meeting backgrounds, linkedin, business cards:', STAFF.map((p) => p.slug).join(', '));
