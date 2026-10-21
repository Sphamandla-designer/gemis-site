// UI audit: distinct font sizes in use, heading sizes by tag, and the padding and
// ground of every section on every page. Run after any change to site.css:
//     node tools/audit-ui.mjs          (add --shots to save full-page screenshots to qa/tidy/)
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const b = await chromium.launch();
const pages = ['index.html','work/index.html','work/wastemart/index.html','solutions/index.html','solutions/bespoke-software/index.html','solutions/managem/index.html','our-story/index.html','contact.html'];
const fontSizes = {}, headingSizes = {}, sectionPads = {};
for (const page of pages) {
  const p = await b.newPage({ viewport:{width:1440,height:900} });
  await p.goto('file://' + process.cwd() + '/' + page, { waitUntil:'load' });
  await p.evaluate(()=>document.querySelectorAll('[data-reveal]').forEach(e=>e.classList.add('is-in')));
  await p.waitForTimeout(600);
  const r = await p.evaluate(() => {
    const out = { fs:{}, h:{}, pads:[] };
    for (const el of document.querySelectorAll('main *')) {
      if (!el.innerText || !el.innerText.trim() || el.children.length > 3) continue;
      const cs = getComputedStyle(el); const fs = Math.round(parseFloat(cs.fontSize));
      out.fs[fs] = (out.fs[fs]||0)+1;
      if (/^H[1-6]$/.test(el.tagName)) { out.h[el.tagName] = out.h[el.tagName]||new Set(); }
    }
    for (const h of document.querySelectorAll('main h1, main h2, main h3')) {
      const fs = Math.round(parseFloat(getComputedStyle(h).fontSize));
      out.h[h.tagName] = out.h[h.tagName] || {}; out.h[h.tagName][fs] = (out.h[h.tagName][fs]||0)+1;
    }
    for (const s of document.querySelectorAll('main > section')) {
      const cs = getComputedStyle(s);
      out.pads.push({ cls: s.className.split(' ')[0], top: Math.round(parseFloat(cs.paddingTop)), bot: Math.round(parseFloat(cs.paddingBottom)), bg: cs.backgroundColor });
    }
    return out;
  });
  for (const [k,v] of Object.entries(r.fs)) fontSizes[k]=(fontSizes[k]||0)+v;
  for (const [tag,m] of Object.entries(r.h)) { headingSizes[tag]=headingSizes[tag]||{}; for (const [k,v] of Object.entries(m)) headingSizes[tag][k]=(headingSizes[tag][k]||0)+v; }
  sectionPads[page] = r.pads;
  if (process.argv.includes('--shots')) await p.screenshot({ path: `qa/tidy/after-${page.replace(/[\/.]/g,'_')}.png`, fullPage: true });
  await p.close();
}
console.log('DISTINCT BODY FONT SIZES in use (px: count):'); console.log('  ' + Object.entries(fontSizes).sort((a,b)=>a[0]-b[0]).map(([k,v])=>`${k}:${v}`).join('  '));
console.log('HEADING SIZES by tag:'); for (const [t,m] of Object.entries(headingSizes)) console.log(`  ${t}: ` + Object.entries(m).sort((a,b)=>a[0]-b[0]).map(([k,v])=>`${k}px×${v}`).join(', '));
console.log('SECTION PADDING (top/bottom) and background per page:');
for (const [pg,pads] of Object.entries(sectionPads)) { console.log('  '+pg); for (const s of pads) console.log(`      ${s.cls.padEnd(10)} ${String(s.top).padStart(3)}/${String(s.bot).padEnd(3)}  ${s.bg}`); }
await b.close();
