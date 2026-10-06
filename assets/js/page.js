/* ══════════════════════════════════════════════════════════════════════
   GEMIS — every page except the home page
   Shared behaviours plus each page's one signature moment, chosen by what
   is in the markup: the timeline, the services stage, the module tour,
   the privacy scrollspy, the 404's missing facet.
   ══════════════════════════════════════════════════════════════════════ */
import { reduced, startLenis, revealOnce, magnetic, transitions } from './motion.js';
import { $, $$, gemFor, near, headlines, navHide, living, processLoop } from './common.js';

/* about: the timeline draws its line once in view */
function timeline() { const tl = $('.tl'); if (tl) revealOnce([tl], { threshold: .4 }); }

/* services: the diagram stage follows the open accordion item */
function servicesStage() {
  const stage = $('#svcStage'), items = $$('.acc__item[data-diagram]'); if (!stage || !items.length) return;
  const sources = $$('[data-diagram-src]');
  const diagrams = sources.map((src) => { const d = $('.diagram', src).cloneNode(true); d.dataset.id = src.dataset.diagramSrc; stage.appendChild(d); return d; });
  const show = (id) => diagrams.forEach((d) => d.classList.toggle('is-on', d.dataset.id === id));
  show(items[0].dataset.diagram);
  const sync = () => { const open = items.find((i) => i.hasAttribute('data-open')); if (open) show(open.dataset.diagram); };
  new MutationObserver(sync).observe($('.acc'), { attributes: true, subtree: true, attributeFilter: ['data-open'] });
  // on small screens each panel carries its own diagram; it plays when the panel opens
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) $('.diagram', e.target)?.classList.add('is-on'); }), { threshold: .2 });
  $$('.acc__viz').forEach((v) => io.observe(v));
}

/* managem: the module tour — the device's sidebar and panel follow the module you are reading */
function moduleTour() {
  const tour = $('#tour'); if (!tour) return;
  const mods = $$('.mod', tour), nav = $$('.tour__nav li', tour), title = $('#tourTitle'), body = $('#tourBody'), tag = $('#tourTag');
  const set = (i) => {
    mods.forEach((m, j) => m.classList.toggle('is-on', j === i));
    nav.forEach((n, j) => n.classList.toggle('is-on', j === i));
    const m = mods[i]; if (!m) return;
    title.textContent = $('.mod__t', m).textContent; body.textContent = $('p', m).textContent; tag.textContent = $('.mod__n', m).textContent;
  };
  set(0);
  if (!('IntersectionObserver' in window) || matchMedia('(max-width: 900px)').matches) return;
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) set(mods.indexOf(e.target)); }), { rootMargin: '-40% 0px -50% 0px', threshold: 0 });
  mods.forEach((m) => io.observe(m));
  mods.forEach((m, i) => { m.addEventListener('mouseenter', () => set(i)); m.addEventListener('focusin', () => set(i)); });
}

/* privacy: the table of contents follows the reader, with a progress line */
function scrollspy() {
  const toc = $('.legal__toc'); if (!toc) return;
  const links = $$('a[href^="#"]', toc), secs = links.map((a) => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
  const bar = document.createElement('span'); bar.className = 'legal__progress'; toc.prepend(bar);
  const mark = () => {
    const y = window.scrollY + window.innerHeight * .3; let active = 0;
    secs.forEach((s, i) => { if (s.offsetTop <= y) active = i; });
    links.forEach((a, i) => { a.classList.toggle('is-active', i === active); a.toggleAttribute('aria-current', i === active); });
    const body = $('.legal__body'); if (body) { const r = body.getBoundingClientRect(); const p = Math.max(0, Math.min(1, (window.innerHeight * .3 - r.top) / r.height)); bar.style.transform = `scaleY(${p})`; }
  };
  window.addEventListener('scroll', mark, { passive: true }); window.addEventListener('resize', mark); mark();
}

/* 404: the gem with one facet missing */
async function missingFacet() {
  const canvas = $('#gem404'); if (!canvas) return;
  await near(canvas.parentElement);
  gemFor(canvas, { state: 'whole', size: 1, missing: 2, maxDpr: 1.5 });
}

/* the small gem that some pages carry beside their CTA */
async function smallGems() {
  for (const c of $$('canvas.gem[data-small]')) { await near(c.parentElement, '40%'); gemFor(c, { state: 'small', size: .78, pointer: false, maxDpr: 1.5, lite: true }); }
}

transitions();
headlines();
navHide();
living();
timeline();
servicesStage();
moduleTour();
scrollspy();
processLoop($('#processLoop'));
magnetic('.btn, .form__send, .cta__btn');
startLenis().then((l) => { window.__lenis = l; }).catch(() => {});
requestAnimationFrame(() => setTimeout(() => { missingFacet(); smallGems(); }, 0));
