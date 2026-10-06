/* ══════════════════════════════════════════════════════════════════════
   GEMIS — behaviours every page shares
   Headlines that enter condensed and settle, a nav that tucks away on the
   way down, product loops that play only in view, and the gem mounted only
   when WebGL and motion are both allowed.
   ══════════════════════════════════════════════════════════════════════ */
import { reduced, isTouch, vw, splitLinesAll, revealOnce } from './motion.js';

export const $ = (s, r = document) => r.querySelector(s);
export const $$ = (s, r = document) => [...r.querySelectorAll(s)];
export const html = document.documentElement;
export const MOBILE = () => matchMedia('(max-width: 900px)').matches;

export function webgl() {
  try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch { return false; }
}
/* decided once, lazily: the WebGL probe costs a context, so it waits until a gem is actually about to mount */
let _live = null;
export function live() {
  if (_live === null) { _live = !reduced() && !window.__SINGLE_FILE && webgl(); if (!_live) html.classList.add('no-gem'); }
  return _live;
}
if (reduced() || window.__SINGLE_FILE) html.classList.add('no-gem');

let mountGem = null;
/* on a phone the still is the first paint; three.js only arrives once the visitor has moved */
export function firstTouch() {
  return new Promise((ok) => {
    const done = () => { ['scroll', 'pointerdown', 'touchstart', 'keydown'].forEach((t) => window.removeEventListener(t, done)); ok(); };
    ['scroll', 'pointerdown', 'touchstart', 'keydown'].forEach((t) => window.addEventListener(t, done, { passive: true, once: true }));
  });
}
export async function gemFor(canvas, opts) {
  if (!canvas || !canvas.clientWidth || reduced() || window.__SINGLE_FILE) return null;
  if (MOBILE()) await firstTouch();
  if (!live()) return null;
  try {
    if (!mountGem) ({ mountGem } = await import('./gem.js'));
    const gem = await mountGem(canvas, { lite: MOBILE(), ...opts });
    canvas.parentElement.classList.add('has-gem');
    return gem;
  } catch (e) { html.classList.add('no-gem'); return null; }
}

/* resolves when the element is within a screen of the viewport, so a scene costs nothing until it is needed */
export function near(el, margin = '60%') {
  return new Promise((ok) => {
    if (!el || !('IntersectionObserver' in window)) return ok();
    const io = new IntersectionObserver((es) => { if (es[0].isIntersecting) { io.disconnect(); ok(); } }, { rootMargin: `${margin} 0px ${margin} 0px` });
    io.observe(el);
  });
}

/* headlines: split into lines, enter condensed, settle; re-split when the width changes */
export function headlines() {
  const els = $$('[data-lines]');
  splitLinesAll(els);
  revealOnce(els, { threshold: .3 });
  let w = vw(), t;
  window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(() => { if (vw() === w) return; w = vw(); els.forEach((el) => { el.innerHTML = el.dataset.html; delete el.dataset.split; }); splitLinesAll(els); els.forEach((el) => el.classList.add('is-in')); }, 160); });
}

/* nav: tucks away on the way down, returns on the way up */
export function navHide() {
  const nav = $('#nav'); if (!nav) return;
  let last = window.scrollY, acc = 0;
  window.addEventListener('scroll', () => {
    const y = window.scrollY, d = y - last; last = y;
    if (nav.classList.contains('is-open') || nav.classList.contains('is-mega')) return;
    acc = Math.sign(d) === Math.sign(acc) ? acc + d : d;
    if (y < 160) nav.classList.remove('is-hidden');
    else if (acc > 48) nav.classList.add('is-hidden');
    else if (acc < -24) nav.classList.remove('is-hidden');
  }, { passive: true });
}

/* living product cards: loops play in view, tilt under the pointer */
export function living() {
  const loops = $$('.loop');
  if ('IntersectionObserver' in window && !reduced()) {
    const io = new IntersectionObserver((es) => es.forEach((e) => e.target.classList.toggle('is-playing', e.isIntersecting)), { threshold: .25 });
    loops.forEach((l) => io.observe(l));
  } else loops.forEach((l) => l.classList.add('is-playing'));
  if (isTouch() || reduced()) return;
  $$('.story__device, .tile__media--live, .cshot--live').forEach((wrap) => {
    const dev = $('.device, .pair-devices', wrap); if (!dev) return;
    wrap.addEventListener('pointermove', (e) => {
      const r = wrap.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      dev.style.transform = `rotateX(${(-y * 5).toFixed(2)}deg) rotateY(${(x * 6).toFixed(2)}deg)`;
    });
    wrap.addEventListener('pointerleave', () => { dev.style.transform = ''; });
  });
}

/* the process loop draws itself once it is in view */
export function processLoop(svg) {
  if (!svg) return;
  const draw = $('.path--draw', svg), nodes = $$('.n', svg);
  const on = (i) => { const n = nodes[i]; $('.node', n).classList.add('is-on'); $('.n-d', n)?.classList.add('is-on'); };
  const play = () => {
    if (reduced()) { draw.style.strokeDashoffset = 0; nodes.forEach((_, i) => on(i)); return; }
    draw.style.transition = 'stroke-dashoffset 2.4s cubic-bezier(.7,0,.2,1)'; draw.style.strokeDashoffset = 0;
    nodes.forEach((_, i) => setTimeout(() => on(i), 200 + i * 330));
  };
  if (!('IntersectionObserver' in window)) return play();
  const io = new IntersectionObserver((es) => { if (es[0].isIntersecting) { play(); io.disconnect(); } }, { threshold: .4 });
  io.observe(svg);
}
