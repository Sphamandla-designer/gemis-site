/* ══════════════════════════════════════════════════════════════════════
   GEMIS — motion utilities
   Every animation on the site shares these easings, durations and helpers,
   so timing feels like one hand. ES module; pages import what they need.
   ══════════════════════════════════════════════════════════════════════ */

export const EASE = {
  ui: 'cubic-bezier(.22,.61,.36,1)',
  scene: 'cubic-bezier(.7,0,.2,1)',
  // the same curves for GSAP
  gsapUi: 'power2.out',
  gsapScene: 'expo.inOut',
};
export const T = { micro: .18, ui: .36, scene: .76 };   // seconds

export const reduced = () =>
  typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;

export const isTouch = () =>
  typeof matchMedia === 'function' && matchMedia('(hover: none)').matches;

export const vw = () => Math.max(document.documentElement.clientWidth, window.innerWidth || 0);

/* GSAP + ScrollTrigger come from the self-hosted builds; register once. */
let _gsap = null;
export async function loadGsap() {
  if (_gsap) return _gsap;
  if (!window.gsap) await loadScript('assets/js/gsap.min.js');
  if (!window.ScrollTrigger) await loadScript('assets/js/ScrollTrigger.min.js');
  window.gsap.registerPlugin(window.ScrollTrigger);
  window.gsap.defaults({ ease: EASE.gsapUi, duration: T.ui });
  _gsap = { gsap: window.gsap, ScrollTrigger: window.ScrollTrigger };
  return _gsap;
}

/* Lenis smooth scroll, wired to ScrollTrigger. Off under reduced motion and on touch. */
export async function startLenis() {
  if (reduced() || isTouch()) return null;
  if (!window.Lenis) await loadScript('assets/js/lenis.min.js');
  const lenis = new window.Lenis({ lerp: .11, wheelMultiplier: 1, smoothWheel: true });
  const { gsap, ScrollTrigger } = await loadGsap();
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((t) => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
  // in-page anchors go through Lenis so the fixed header is accounted for
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a || a.getAttribute('href') === '#') return;
    const el = document.getElementById(a.getAttribute('href').slice(1));
    if (!el) return;
    e.preventDefault();
    lenis.scrollTo(el, { offset: -72, duration: 1.1, easing: (t) => 1 - Math.pow(1 - t, 3) });
    history.pushState(null, '', a.getAttribute('href'));
  });
  return lenis;
}

export function loadScript(src) {
  return new Promise((ok, fail) => {
    const s = document.createElement('script');
    s.src = src; s.async = false; s.onload = ok; s.onerror = () => fail(new Error('failed ' + src));
    document.head.appendChild(s);
  });
}

/* ── text: split a block into lines (not characters — corporate, not playful) ──
   Wraps each visual line in <span class="ln"><span class="ln__in">…</span></span>
   so the inner span can slide up and the headline can settle from condensed
   to normal width. Re-splits on resize. Keeps inline markup inside a line. */
export function splitLines(el) { return splitLinesAll([el])[0]; }
/* the same for many headlines at once: one write pass, one read pass, one write pass — a single layout, not one per headline */
export function splitLinesAll(els) {
  const todo = els.filter((el) => el.dataset.split !== '1');
  todo.forEach((el) => {
    const html = el.innerHTML; el.dataset.html = html;
    const words = html.split(/(\s+)/).filter(Boolean);
    el.innerHTML = words.map((w) => (/^\s+$/.test(w) ? ' ' : `<span class="w">${w}</span>`)).join('');
  });
  const measured = todo.map((el) => [...el.querySelectorAll('.w')].map((s) => [s.innerHTML, s.offsetTop]));
  todo.forEach((el, k) => {
    const lines = []; let top = null, cur = [];
    for (const [h, t] of measured[k]) {
      if (top === null || Math.abs(t - top) > 2) { if (cur.length) lines.push(cur); cur = []; top = t; }
      cur.push(h);
    }
    if (cur.length) lines.push(cur);
    el.innerHTML = lines.map((ws) => `<span class="ln"><span class="ln__in">${ws.join(' ')}</span></span>`).join(' ');
    el.dataset.split = '1';
  });
  return els.map((el) => [...el.querySelectorAll('.ln__in')]);
}
export function unsplit(el) { if (el.dataset.html) { el.innerHTML = el.dataset.html; delete el.dataset.split; } }

/* ── reveal: once, then it stays ───────────────────────────────────── */
export function revealOnce(targets, { root = null, threshold = .18 } = {}) {
  const els = typeof targets === 'string' ? [...document.querySelectorAll(targets)] : [...targets];
  if (!els.length) return;
  if (reduced() || !('IntersectionObserver' in window)) { els.forEach((e) => e.classList.add('is-in')); return; }
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { root, threshold });
  els.forEach((e) => io.observe(e));
}

/* ── count-up for figures, once, tabular ───────────────────────────── */
export function countUp(el, { duration = 1.4 } = {}) {
  const end = parseFloat(el.dataset.count); const sup = el.dataset.sup || ''; const dec = (el.dataset.count.split('.')[1] || '').length;
  if (isNaN(end)) return;
  if (reduced()) { el.innerHTML = end.toLocaleString('en-ZA') + (sup ? `<sup>${sup}</sup>` : ''); return; }
  let t0 = null;
  const step = (t) => {
    if (t0 === null) t0 = t;
    const p = Math.min(1, (t - t0) / (duration * 1000)); const e = 1 - Math.pow(1 - p, 3);
    el.innerHTML = (end * e).toLocaleString('en-ZA', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + (sup ? `<sup>${sup}</sup>` : '');
    if (p < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

/* ── magnetic pull on primary buttons: max 6px, pointer devices only ── */
export function magnetic(selector, max = 6) {
  if (isTouch() || reduced()) return;
  document.querySelectorAll(selector).forEach((el) => {
    el.style.transition = `transform ${T.ui}s ${EASE.ui}`;
    el.addEventListener('pointermove', (e) => {
      const r = el.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width - .5) * 2 * max, y = ((e.clientY - r.top) / r.height - .5) * 2 * max;
      el.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px)`;
    });
    el.addEventListener('pointerleave', () => { el.style.transform = ''; });
  });
}

/* ── the progress spine: section indices along the left edge that fill as you scroll ── */
export function spine(sections) {
  const list = [...sections];
  if (list.length < 2 || vw() < 1180) return;
  const nav = document.createElement('nav');
  nav.className = 'spine'; nav.setAttribute('aria-label', 'Page sections');
  nav.innerHTML = list.map((s, i) => `<a class="spine__i" href="#${s.id}"><span class="spine__n mono">${String(i + 1).padStart(2, '0')}</span><span class="spine__t">${s.dataset.spine || ''}</span><span class="spine__tick" aria-hidden="true"></span></a>`).join('');
  document.body.appendChild(nav);
  const items = [...nav.children];
  const mark = () => {
    const y = window.scrollY + window.innerHeight * .42;
    let active = 0;
    list.forEach((s, i) => { if (s.offsetTop <= y) active = i; });
    items.forEach((it, i) => { it.classList.toggle('is-done', i < active); it.classList.toggle('is-active', i === active); });
    nav.classList.toggle('is-dark', !!document.elementFromPoint(24, window.innerHeight / 2)?.closest('.band-ink, .hero, .cta, .lead, .chero, .reassembly, .fracture'));
  };
  window.addEventListener('scroll', mark, { passive: true }); window.addEventListener('resize', mark); mark();
}

/* ── first-visit loader + facet page transitions ───────────────────── */
export function transitions() {
  const wipe = document.createElement('div');
  wipe.className = 'wipe'; wipe.setAttribute('aria-hidden', 'true');
  document.body.appendChild(wipe);
  if (reduced()) return;
  // leaving: a facet-shaped wipe in navy, then navigate
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href]');
    if (e.defaultPrevented || !a || a.target === '_blank' || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
    const href = a.getAttribute('href');
    if (!href || /^(#|mailto:|tel:|https?:)/.test(href) || a.hasAttribute('download')) return;
    if (document.startViewTransition) return; // the browser does the cross-fade; the wipe is the fallback
    e.preventDefault();
    wipe.classList.add('is-on');
    setTimeout(() => { location.href = href; }, 520);
  });
  window.addEventListener('pageshow', () => wipe.classList.remove('is-on'));
}
