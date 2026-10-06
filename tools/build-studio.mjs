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
 *         studio/work.html, about.html, services.html, contact.html — the
 *                                   sibling pages, with the homepage's chrome
 *                                   lifted into their slots
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
const ABOUT_SRC = join(ROOT, 'studio/src/about.html');
const ABOUT_OUT = join(ROOT, 'studio/about.html');
const SERVICES_SRC = join(ROOT, 'studio/src/services.html');
const SERVICES_OUT = join(ROOT, 'studio/services.html');
const CONTACT_SRC = join(ROOT, 'studio/src/contact.html');
const CONTACT_OUT = join(ROOT, 'studio/contact.html');
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

/* The homepage's menu button and [data-reveal] elements are driven by React.
   The sibling pages carry no runtime, so they get the same behaviour from here:
   the drawer opens and shuts, and the reveal class arrives on scroll. */
const SIBLING_JS = `<script>
(function () {
  'use strict';
  var btn = document.getElementById('studioMenuBtn');
  var drawer = document.getElementById('studioMenu');
  if (btn && drawer) {
    // the runtime wraps the ≡ in markup of its own, so find it by what it says
    var glyph = [].slice.call(btn.querySelectorAll('span'))
      .filter(function (s) { return !s.children.length && /^[\\u2261\\u00d7]$/.test(s.textContent.trim()); })[0];
    var isOpen = false;
    var set = function (open) {
      isOpen = open;
      // the drawer carries an inline display:flex, which outranks [hidden]
      drawer.style.display = open ? 'flex' : 'none';
      drawer.hidden = !open;
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (glyph) glyph.textContent = open ? '×' : '≡';
    };
    set(false);
    btn.addEventListener('click', function () { set(!isOpen); });
    drawer.addEventListener('click', function (e) { if (e.target.closest('a')) set(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && isOpen) { set(false); btn.focus(); } });
  }
  var els = [].slice.call(document.querySelectorAll('[data-reveal]'));
  if (!els.length) return;
  if (!('IntersectionObserver' in window)) { els.forEach(function (el) { el.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.15 });
  els.forEach(function (el) { io.observe(el); });
  setTimeout(function () {
    els.forEach(function (el) { if (!el.classList.contains('in') && el.getBoundingClientRect().top < innerHeight) el.classList.add('in'); });
  }, 1500);
})();
</script>`;

const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const SERVICE_ID = { 'Product Teardown': 'teardown', 'Interface Refresh Sprint': 'refresh', 'Web Experience': 'web', 'Embedded Designer': 'embedded' };

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
${p.evidences ? `        <div style="font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.04em;color:#6a6b73;text-transform:uppercase">Evidences: ${esc(p.evidences)}</div>
` : ''}        <div style="display:flex;justify-content:space-between;gap:24px;align-items:flex-end">
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
        // the four ladder steps, read out of the rendered panels so services.html cannot drift from the homepage
        services: [...document.querySelectorAll('#services [role="tabpanel"]')].map((p) => {
          const t = (el) => (el ? el.textContent.replace(/\s+/g, ' ').trim() : '');
          const [head, title, body, foot] = p.children;
          const specs = [...body.querySelectorAll('[data-m="spec"]')];
          return {
            badge: t(head.children[0]), time: t(head.children[1]),
            name: t(title.children[0]), price: t(title.children[1]),
            desc: t(body.querySelector('p')),
            priceNote: t(specs[0].children[1]), evidence: t(specs[1].children[1]), credit: t(specs[2].children[1]),
            deliverables: [...specs[3].querySelectorAll('li')].map((li) => t(li.children[1])),
            note: t(foot.children[0]), cta: t(foot.querySelector('a span')),
          };
        }),
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

  // ── sibling pages: studio/work.html and studio/about.html ─────────────
  for (const part of ['header', 'pill', 'contact', 'drawer']) {
    if (!chrome[part]) throw new Error(`could not lift the ${part} out of the rendered homepage — the sibling pages would be missing their chrome`);
  }
  if (!chrome.cards.length) throw new Error('the homepage carousel rendered no cards, so work.html has nothing to list');

  // the menu button is the only <button> in the lifted header; assert that,
  // rather than trusting that it stays the first one in the document
  if ((chrome.header.match(/<button /g) || []).length !== 1) {
    throw new Error('the studio header no longer has exactly one button — the sibling pages cannot tell which to wire');
  }
  chrome.header = chrome.header.replace('<button ', '<button id="studioMenuBtn" ');

  /** Fill the slots every sibling page shares, then the page's own. */
  const siblingPage = (name, src, own) => {
    let page = src
      .replace('<!--#studio-css-->', '<style>' + chrome.css + '</style>')
      .replace('<!--#header-->', rehomeAnchors(chrome.header))
      // the drawer is captured open; these pages start with it shut. Its inline
      // display:flex outranks [hidden], so that has to go too or the drawer sits
      // over the page for anyone without JavaScript.
      .replace('<!--#drawer-->', shutDrawer(rehomeAnchors(chrome.drawer)))
      .replace('<!--#contact-->', rehomeAnchors(chrome.contact))
      .replace('<!--#sibling-js-->', SIBLING_JS);
    for (const [slot, html] of Object.entries(own)) page = page.replace(`<!--#${slot}-->`, html);
    if (!page.includes('id="studioMenuBtn"')) throw new Error(`${name} could not tag the menu button — the studio header markup changed`);
    if (page.includes('{{')) throw new Error(`${name} still contains {{ — the chrome was lifted before the runtime resolved it`);
    if (page.includes('<!--#')) throw new Error(`${name} still has an unfilled slot: ` + /<!--#[a-z-]+-->/.exec(page)[0]);
    return page;
  };

  // the three homepage projects, read out of its own carousel
  const homeProjects = chrome.cards.map((c) => {
    const { desc, evidences } = splitEvidence(c.desc);
    return { slug: c.name.toLowerCase().replace(/[^a-z0-9]+/g, '-'), name: c.name, desc, evidences, img: c.img };
  });

  // ── studio/work.html ───────────────────────────────────────────────────
  const workSrc = await readFile(WORK_SRC, 'utf8');
  const extra = JSON.parse(
    (/<script type="application\/json" id="extra-projects">([\s\S]*?)<\/script>/.exec(workSrc) || [, '[]'])[1]);

  const projects = [...homeProjects, ...extra].map((p) => ({
    ...p,
    // no project detail pages exist yet, so EXPLORE PROJECT goes to the card
    href: `work.html#${p.slug}`,
    cta: 'Explore project',
  }));

  const cards = '  <div data-m="cards" style="position:relative;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px;margin:72px auto 0;max-width:1400px">\n'
    + projects.map(workCard).join('\n') + '\n  </div>';

  const work = siblingPage('work.html', workSrc, { cards });

  // ── studio/about.html ──────────────────────────────────────────────────
  // The evidence strip names the homepage's own three projects and the service
  // each one proves, straight out of the carousel, so it cannot drift either.
  const evidence = '<div data-reveal="1" data-m="head" style="margin-top:64px;display:grid;grid-template-columns:1fr auto;gap:32px;align-items:center;border-top:1px solid #dcdee3;padding-top:32px">\n'
    + '      <div style="display:flex;gap:16px 48px;flex-wrap:wrap">\n'
    + homeProjects.map((p) => `        <a href="work.html#${esc(p.slug)}" style="display:flex;flex-direction:column;gap:6px;color:#16161a"><span style="font-size:22px;font-weight:600;letter-spacing:-0.02em">${esc(p.name)}</span><span style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.04em;color:#6a6b73;text-transform:uppercase">${p.evidences ? 'Evidences: ' + esc(p.evidences) : 'Case study'}</span></a>`).join('\n')
    + '\n      </div>\n'
    + '      <a href="work.html" style="font-family:\'JetBrains Mono\',monospace;font-size:13px;display:flex;justify-content:space-between;gap:48px;border-bottom:2px solid #ff7a12;padding-bottom:10px;min-width:230px;color:#16161a"><span style="text-transform:uppercase">View all projects</span><span>→</span></a>\n'
    + '    </div>';

  const about = siblingPage('about.html', await readFile(ABOUT_SRC, 'utf8'), { evidence });

  // ── studio/services.html ───────────────────────────────────────────────
  if (chrome.services.length !== 4) throw new Error(`the homepage ladder rendered ${chrome.services.length} steps, not 4 — services.html would be wrong`);
  const services = chrome.services.map((s) => {
    const [num, kicker] = s.badge.split('—').map((x) => x.trim());
    const project = s.evidence.replace(/^Evidence\s*—\s*/i, '').trim();
    const id = SERVICE_ID[s.name] || slug(s.name);
    if (!num || !kicker || !project) throw new Error(`could not read the ladder step "${s.name}" off the homepage`);
    return { ...s, num, kicker, id, project, projectSlug: slug(project) };
  });
  const ladder = services.map((s) => `        <a class="svc-row" href="#${s.id}" style="display:grid;grid-template-columns:44px 1fr auto;gap:16px;align-items:center;padding:18px 0;border-bottom:1px solid rgba(22,22,26,.15);color:#16161a"><span style="font-family:'JetBrains Mono',monospace;font-size:13px;color:#ff1f7a">${esc(s.num)}</span><span style="font-size:clamp(18px,1.6vw,24px);letter-spacing:-0.03em;font-weight:600">${esc(s.name)}</span><span style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#6a6b73;white-space:nowrap;text-transform:uppercase">${esc(s.time)} · ${esc(s.price)}</span></a>`).join('\n');
  const spec = (label, value) => `            <div data-m="spec" style="display:grid;grid-template-columns:140px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #dcdee3;font-size:14px;line-height:1.35"><span style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#6a6b73;letter-spacing:0.04em;text-transform:uppercase">${label}</span>${value}</div>`;
  const stepCards = services.map((s, i) => `      <section id="${s.id}" class="svc-card" aria-labelledby="${s.id}-name" style="scroll-margin-top:120px;background:#f5f6f8;color:#16161a;display:grid;grid-template-rows:auto auto 1fr auto">
        <div style="display:flex;justify-content:space-between;align-items:center;padding:clamp(20px,2.5vw,32px) clamp(24px,3vw,40px) 0">
          <span style="background:#16161a;color:#f5f6f8;font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.06em;padding:10px 14px;text-transform:uppercase">${esc(s.num)} — ${esc(s.kicker)}</span>
          <span style="font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.04em;color:#6a6b73;text-transform:uppercase">${esc(s.time)}</span>
        </div>
        <div style="padding:28px clamp(24px,3vw,40px) 0;display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;align-items:flex-end">
          <h3 id="${s.id}-name" style="margin:0;font-size:clamp(30px,3vw,46px);line-height:1;letter-spacing:-0.04em;font-weight:600;min-width:0">${esc(s.name)}</h3>
          <div style="font-size:clamp(26px,2.4vw,38px);line-height:1;letter-spacing:-0.04em;font-weight:600;color:#ff1f7a;white-space:nowrap">${esc(s.price)}</div>
        </div>
        <div style="padding:24px clamp(24px,3vw,40px) 0">
          <p style="margin:0;font-size:17px;line-height:1.4;color:#3a3b41;max-width:620px">${esc(s.desc)}</p>
          <div style="margin-top:28px;border-top:1px solid #16161a">
${spec('Timeline', `<span style="font-weight:600;text-transform:uppercase">${esc(s.priceNote)}</span>`)}
${spec('Evidence', `<span style="font-weight:600;text-transform:uppercase"><a href="work.html#${esc(s.projectSlug)}" style="border-bottom:2px solid #ff7a12;padding-bottom:2px">${esc(s.project)}</a></span>`)}
${spec('Credit', `<span style="color:#3a3b41">${esc(s.credit)}</span>`)}
            <div data-m="spec" style="display:grid;grid-template-columns:140px 1fr;gap:16px;padding:14px 0;font-size:14px;line-height:1.35"><span style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#6a6b73;letter-spacing:0.04em;text-transform:uppercase">You get</span>
              <ol style="margin:0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px 24px">
${s.deliverables.map((d, j) => `                <li style="display:flex;gap:10px;align-items:baseline"><span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#ff7a12">0${j + 1}</span><span style="font-weight:500">${esc(d)}</span></li>`).join('\n')}
              </ol>
            </div>
          </div>
        </div>
        <div style="margin-top:32px;background:#16161a;color:#f5f6f8;padding:22px clamp(24px,3vw,40px);display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap">
          <span style="font-size:14px;color:#9a9ba3">${esc(s.note)}</span>
          <a href="contact.html#${s.id}" style="font-family:'JetBrains Mono',monospace;font-size:13px;display:flex;justify-content:space-between;gap:40px;border-bottom:2px solid #ff7a12;padding-bottom:8px;min-width:200px;color:#f5f6f8"><span style="text-transform:uppercase">${esc(s.cta)}</span><span>→</span></a>
        </div>
      </section>`).join('\n');
  const servicesPage = siblingPage('services.html', await readFile(SERVICES_SRC, 'utf8'), { ladder, services: stepCards });

  // ── studio/contact.html ────────────────────────────────────────────────
  const contact = siblingPage('contact.html', await readFile(CONTACT_SRC, 'utf8'), {});

  await writeFile(TPL_OUT,
    '/* Generated by tools/build-studio.mjs — do not edit.\n'
    + '   Source of truth: studio/src/index.html */\n'
    + 'window.__dcTemplate = ' + JSON.stringify(template) + ';\n', 'utf8');
  await writeFile(OUT, out, 'utf8');
  await writeFile(WORK_OUT, work, 'utf8');
  await writeFile(ABOUT_OUT, about, 'utf8');
  await writeFile(SERVICES_OUT, servicesPage, 'utf8');
  await writeFile(CONTACT_OUT, contact, 'utf8');
  console.log(`studio/index.html written — ${(out.length / 1024).toFixed(0)} KB, 0 unresolved bindings`);
  console.log(`studio/assets/dc-template.js written — ${(template.length / 1024).toFixed(0)} KB of template`);
  console.log(`studio/work.html written — ${(work.length / 1024).toFixed(0)} KB, ${projects.length} projects: ${projects.map((p) => p.name).join(', ')}`);
  console.log(`studio/about.html written — ${(about.length / 1024).toFixed(0)} KB, evidence: ${homeProjects.map((p) => p.name).join(', ')}`);
  console.log(`studio/services.html written — ${(servicesPage.length / 1024).toFixed(0)} KB, steps: ${services.map((s) => s.name + ' ' + s.price).join(', ')}`);
  console.log(`studio/contact.html written — ${(contact.length / 1024).toFixed(0)} KB`);
};

main().catch((e) => { console.error('build-studio failed:', e.message); process.exit(1); });
