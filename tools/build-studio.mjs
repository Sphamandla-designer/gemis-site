#!/usr/bin/env node
/**
 * Pre-renders /studio/.
 *
 *   node tools/build-studio.mjs
 *
 * Reads   studio/src/index.html   — the authored page, the one a future Design
 *                                   Canvas export replaces wholesale
 * Writes  studio/index.html       — served; fully rendered, no {{ }}
 *         studio/assets/dc-template.js — the template, as a JS string
 *
 * How it works: the source page is served as-is to a headless Chromium, which
 * runs dc-runtime and React exactly as a visitor's browser would. The rendered
 * DOM is then written back into the page in place of the <x-dc> block, with
 * assets/dc-boot.js put in front of the runtime to hand it the template again
 * at load time. The interactive page is therefore byte-for-byte the same
 * component it always was — only the starting HTML changed.
 *
 * Re-run this after any edit to studio/src/index.html, and after any new
 * export from Design Canvas.
 */
import { createServer } from 'node:http';
import { readFile, writeFile, unlink } from 'node:fs/promises';
import { existsSync, createReadStream, statSync } from 'node:fs';
import { extname, join, resolve, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(fileURLToPath(new URL('..', import.meta.url)));
const SRC = join(ROOT, 'studio/src/index.html');
const OUT = join(ROOT, 'studio/index.html');
const TPL_OUT = join(ROOT, 'studio/assets/dc-template.js');
const WORK_SRC = join(ROOT, 'studio/src/work.html');
const WORK_OUT = join(ROOT, 'studio/work.html');
const TMP_REL = 'studio/.prerender.html';
const TMP = join(ROOT, TMP_REL);

const PLAYWRIGHT = process.env.PLAYWRIGHT_MODULE
  || '/opt/node22/lib/node_modules/playwright/index.js';

const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.woff2': 'font/woff2',
  '.woff': 'font/woff', '.ico': 'image/x-icon', '.mp4': 'video/mp4',
};

function serve(root) {
  const server = createServer((req, res) => {
    const p = decodeURIComponent(req.url.split('?')[0]);
    const file = join(root, normalize(p).replace(/^(\.\.[/\\])+/, ''));
    if (!file.startsWith(root) || !existsSync(file) || !statSync(file).isFile()) {
      res.writeHead(404).end('not found');
      return;
    }
    res.writeHead(200, { 'content-type': MIME[extname(file)] || 'application/octet-stream' });
    createReadStream(file).pipe(res);
  });
  return new Promise((ok) => server.listen(0, '127.0.0.1', () => ok(server)));
}

/** The one place that knows where the template block starts and ends. */
function sliceTemplate(html) {
  const open = /<x-dc(?:\s[^>]*)?>/.exec(html);
  if (!open) throw new Error('studio/src/index.html has no <x-dc> block');
  const close = html.lastIndexOf('</x-dc>');
  if (close < open.index) throw new Error('unterminated <x-dc> block');
  return {
    before: html.slice(0, open.index),
    template: html.slice(open.index + open[0].length, close),
    after: html.slice(close + '</x-dc>'.length),
  };
}

function sliceHelmet(template) {
  const open = template.indexOf('<helmet>');
  const close = template.indexOf('</helmet>');
  if (open === -1 || close === -1) return '';
  return template.slice(open + '<helmet>'.length, close);
}

/* The runtime hoists <helmet> into <head> and sizes #dc-root itself. Neither
   happens without JavaScript, so the static copy carries the equivalent, plus
   the one override the tab panels need: every ladder step is in the markup but
   all except the selected one are display:none, which is right for a tabpanel
   and wrong for a page being read without scripts. */
const FALLBACK_CSS = `
<style id="dc-prerender-css">
html,body{height:100%;margin:0}
#dc-prerender,#dc-prerender>.sc-host{height:auto}
#dc-prerender [role="tabpanel"]{display:grid!important}
#dc-prerender [data-reveal]{opacity:1!important;transform:none!important}
#dc-prerender [data-word]>span{transform:none!important}
#dc-prerender [data-rotator] span{visibility:hidden!important}
#dc-prerender [data-rotator] span:first-child{visibility:visible!important;animation:none!important}
</style>`;


/* ── studio/work.html ──────────────────────────────────────────────────────
   A listing page with no runtime: the chrome is lifted from the rendered
   homepage so the two cannot drift, and the cards are the homepage's own work
   card markup with real data written straight into it. Nothing on this page
   is a template, so there is nothing to resolve at load time and it reads
   identically with JavaScript disabled. */

const esc = (s) => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/** In-page links in the lifted chrome belong to the homepage, not to this one. */
const rehomeAnchors = (html) => html.replace(/href="#([a-z][a-z0-9-]*)"/g, (m, id) =>
  (id === 'main' ? m : `href="index.html#${id}"`));

/** The drawer is captured mid-open. Close it, in a way that survives no-JS. */
const shutDrawer = (html) => {
  let out = html.replace(/^<div /, '<div hidden ');
  const style = /style="([^"]*)"/.exec(out);
  if (!style) throw new Error('the lifted drawer has no style attribute');
  if (!/display:\s*flex/.test(style[1])) throw new Error('the lifted drawer no longer sets display:flex — check it still starts shut');
  out = out.replace(style[0], 'style="' + style[1].replace(/display:\s*flex/, 'display: none') + '"');
  if (!out.startsWith('<div hidden ')) throw new Error('could not mark the lifted drawer hidden');
  return out;
};

/** One card, in the homepage's own markup. `href` is where EXPLORE PROJECT goes. */
const workCard = (p) => `      <div id="${esc(p.slug)}" style="display:flex;flex-direction:column;gap:20px;scroll-margin-top:120px">
        <div style="aspect-ratio:16/11;overflow:hidden;border-radius:4px"><img src="${esc(p.img)}" alt="${esc(p.name)}" loading="lazy" decoding="async" style="width:100%;height:100%;object-fit:cover;display:block;transition:transform .8s cubic-bezier(.2,.7,.2,1)" style-hover="transform:scale(1.05)"></div>
        <div style="font-size:28px;letter-spacing:-0.03em;font-weight:600">${esc(p.name)}</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.04em;color:#6a6b73;text-transform:uppercase">Evidences: ${esc(p.evidences ?? '[PLACEHOLDER: service evidenced]')}</div>
        <div style="display:flex;justify-content:space-between;gap:24px;align-items:flex-end">
          <p style="margin:0;font-size:16px;line-height:1.35;max-width:300px;color:#5a5b63">${esc(p.desc)}</p>
          <a href="${esc(p.href)}" style="font-family:'JetBrains Mono',monospace;font-size:13px;display:flex;justify-content:space-between;gap:40px;border-bottom:2px solid #ff7a12;padding-bottom:8px;white-space:nowrap"><span style="text-transform:uppercase">${esc(p.cta)}</span><span>→</span></a>
        </div>
      </div>`;

/** "…Evidences: Web Experience." at the end of a homepage card's description. */
const splitEvidence = (desc) => {
  const m = /^(.*?)\s*Evidences:\s*([^.]+)\.?\s*$/.exec(desc);
  return m ? { desc: m[1].trim(), evidences: m[2].trim() } : { desc, evidences: null };
};

const main = async () => {
  const src = await readFile(SRC, 'utf8');
  const { before, template, after } = sliceTemplate(src);
  const helmet = sliceHelmet(template);

  // render the authored page exactly as a browser would. Nothing is written
  // until this succeeds — a half-finished build that leaves index.html and
  // dc-template.js describing different pages is worse than no build.
  await writeFile(TMP, src, 'utf8');
  const server = await serve(ROOT);
  const port = server.address().port;
  const { chromium } = await import(PLAYWRIGHT).then((m) => m.default ?? m);
  const browser = await chromium.launch();
  let rendered;
  let chrome;
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const failures = [];
    page.on('pageerror', (e) => failures.push(String(e.message)));
    await page.goto(`http://127.0.0.1:${port}/${TMP_REL}`, { waitUntil: 'networkidle' });
    await page.waitForFunction(() => {
      const r = document.getElementById('dc-root');
      return r && r.children.length > 0;
    }, null, { timeout: 30000 });
    await page.waitForTimeout(1500);
    if (failures.length) throw new Error('the page threw while rendering:\n  ' + failures.join('\n  '));
    rendered = await page.evaluate(() => document.getElementById('dc-root').innerHTML);

    /* studio/work.html carries no runtime of its own. Rather than hand-copying
       the header, the action pill, the drawer and the closing band — which
       would drift the first time the homepage changed — take them straight out
       of the page that was just rendered, and take the three homepage projects
       out of its own carousel. */
    chrome = await page.evaluate(() => {
      const outer = (sel) => { const el = document.querySelector(sel); return el ? el.outerHTML : null; };
      const cards = [...document.querySelectorAll('#work [data-m="cards"] > div')].map((card) => {
        const img = card.querySelector('img');
        return {
          name: card.children[1]?.textContent.trim() ?? '',
          desc: card.querySelector('p')?.textContent.trim() ?? '',
          img: img ? img.getAttribute('src') : '',
        };
      });
      return {
        css: [...document.head.querySelectorAll('style')].map((s) => s.textContent).join('\n'),
        header: outer('header'),
        pill: outer('[data-cta]'),
        contact: outer('#contact'),
        cards,
      };
    });
    // the drawer only exists while the menu is open
    await page.click('#studioMenu ~ *, header button');
    await page.waitForTimeout(400);
    chrome.drawer = await page.evaluate(() => {
      const el = document.getElementById('studioMenu');
      return el ? el.outerHTML : null;
    });
  } finally {
    await browser.close();
    server.close();
    await unlink(TMP).catch(() => {});
  }

  if (rendered.includes('{{')) throw new Error('the rendered markup still contains {{ — a binding did not resolve');

  /* The mobile layout hangs off data-m hooks in the markup rather than
     substring matches on the style attribute, because the browser rewrites an
     inline style and those matches silently stop applying. Check every hook the
     stylesheet asks for is actually on the page, so a future Design Canvas
     export that drops one fails here instead of shipping a broken phone
     layout. */
  const wanted = new Set([...template.matchAll(/\[data-m="([a-z0-9-]+)"\]/g)].map((m) => m[1]));
  // count attributes in the markup only — the stylesheet lives in <helmet> and
  // its own [data-m="…"] selectors would otherwise satisfy this check
  const markup = template.replace(/<helmet>[\s\S]*?<\/helmet>/, '');
  const authored = new Set([...markup.matchAll(/data-m="([a-z0-9-]+)"/g)].map((m) => m[1]));
  const rendersNow = new Set([...rendered.matchAll(/data-m="([a-z0-9-]+)"/g)].map((m) => m[1]));
  // the slide-out menu lives inside an sc-if, so it is absent from a render
  // taken with the menu closed. Its hook is checked in the template only.
  const CONDITIONAL = new Set(['drawer']);
  const missing = [...wanted].filter((h) => !authored.has(h)
    || (!CONDITIONAL.has(h) && !rendersNow.has(h)));
  if (missing.length) {
    throw new Error('the mobile layout targets hooks that are not on the page: '
      + missing.map((h) => 'data-m="' + h + '"').join(', ')
      + '\n  Re-apply the hooks listed in studio/README.md, then rebuild.');
  }
  for (const attr of ['data-cta', 'data-desk']) {
    if (!rendered.includes(attr)) throw new Error(`the mobile layout needs [${attr}] and the rendered page has none — see studio/README.md`);
  }
  console.log(`mobile layout hooks present: ${[...wanted].sort().join(', ')}`);

  const slot = [
    '<!-- Pre-rendered by tools/build-studio.mjs. Edit studio/src/index.html, then re-run it. -->',
    '<div id="dc-prerender">' + rendered + '</div>',
    '<script src="assets/dc-template.js"></script>',
    '<script src="assets/dc-boot.js"></script>',
  ].join('\n');

  // the authored source carries noindex so the raw-template copy at
  // studio/src/ never competes with the built page in search results
  let out = (before + slot + after).replace('<meta name="robots" content="noindex">\n', '');
  out = out.replace('</head>', helmet + FALLBACK_CSS + '\n</head>');

  const left = out.split('{{').length - 1;
  if (left) throw new Error(`the built page still contains ${left} occurrence(s) of {{`);

  // ── studio/work.html ───────────────────────────────────────────────────
  for (const part of ['header', 'pill', 'contact', 'drawer']) {
    if (!chrome[part]) throw new Error(`could not lift the ${part} out of the rendered homepage — work.html would be missing its chrome`);
  }
  if (!chrome.cards.length) throw new Error('the homepage carousel rendered no cards, so work.html has nothing to list');

  let work = await readFile(WORK_SRC, 'utf8');
  const extra = JSON.parse(
    (/<script type="application\/json" id="extra-projects">([\s\S]*?)<\/script>/.exec(work) || [, '[]'])[1]);

  const projects = [
    ...chrome.cards.map((c) => {
      const { desc, evidences } = splitEvidence(c.desc);
      return { slug: c.name.toLowerCase().replace(/[^a-z0-9]+/g, '-'), name: c.name, desc, evidences, img: c.img };
    }),
    ...extra,
  ].map((p) => ({
    ...p,
    // no project detail pages exist yet, so EXPLORE PROJECT goes to the card
    href: `work.html#${p.slug}`,
    cta: 'Explore project',
  }));

  const cards = '  <div data-m="cards" style="position:relative;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px;margin:72px auto 0;max-width:1400px">\n'
    + projects.map(workCard).join('\n') + '\n  </div>';

  // the menu button is the only <button> in the lifted header; assert that,
  // rather than trusting that it stays the first one in the document
  if ((chrome.header.match(/<button /g) || []).length !== 1) {
    throw new Error('the studio header no longer has exactly one button — work.html cannot tell which to wire');
  }
  chrome.header = chrome.header.replace('<button ', '<button id="studioMenuBtn" ');

  work = work
    .replace('<!--#studio-css-->', '<style>' + chrome.css + '</style>')
    .replace('<!--#header-->', rehomeAnchors(chrome.header))
    // the drawer is captured open; this page starts with it shut. Its inline
    // display:flex outranks [hidden], so that has to go too or the drawer sits
    // over the page for anyone without JavaScript.
    .replace('<!--#drawer-->', shutDrawer(rehomeAnchors(chrome.drawer)))
    .replace('<!--#contact-->', rehomeAnchors(chrome.contact))
    .replace('<!--#cards-->', cards);

  if (!work.includes('id="studioMenuBtn"')) {
    throw new Error('work.html could not tag the menu button — the studio header markup changed');
  }

  if (work.includes('{{')) throw new Error('work.html still contains {{ — the chrome was lifted before the runtime resolved it');
  if (work.includes('<!--#')) throw new Error('work.html still has an unfilled slot: ' + /<!--#[a-z-]+-->/.exec(work)[0]);

  await writeFile(TPL_OUT,
    '/* Generated by tools/build-studio.mjs — do not edit.\n'
    + '   Source of truth: studio/src/index.html */\n'
    + 'window.__dcTemplate = ' + JSON.stringify(template) + ';\n', 'utf8');
  await writeFile(OUT, out, 'utf8');
  await writeFile(WORK_OUT, work, 'utf8');
  console.log(`studio/index.html written — ${(out.length / 1024).toFixed(0)} KB, 0 unresolved bindings`);
  console.log(`studio/assets/dc-template.js written — ${(template.length / 1024).toFixed(0)} KB of template`);
  console.log(`studio/work.html written — ${(work.length / 1024).toFixed(0)} KB, ${projects.length} projects: ${projects.map((p) => p.name).join(', ')}`);
};

main().catch((e) => { console.error('build-studio failed:', e.message); process.exit(1); });
