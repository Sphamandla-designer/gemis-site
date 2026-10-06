/* ══════════════════════════════════════════════════════════════════════
   GEMIS — home page
   The gem's four states, the pinned fracture, the estimator, the
   reassembly, the services stage, the living product cards, the process
   loop and the form. Everything here is additive: with scripts off or
   motion reduced the page is complete and still.
   ══════════════════════════════════════════════════════════════════════ */
import { reduced, loadGsap, startLenis, revealOnce, magnetic, spine, transitions } from './motion.js';
import { $, $$, html, MOBILE, gemFor, near, headlines, navHide, living, processLoop } from './common.js';

/* ── 0 · first-visit loader: the mark draws itself, then the page ──── */
function loader() {
  if (reduced()) return;
  try { if (sessionStorage.getItem('gemis-seen')) return; sessionStorage.setItem('gemis-seen', '1'); } catch { return; }
  const t0 = performance.now();
  const el = document.createElement('div');
  el.className = 'loader'; el.setAttribute('aria-hidden', 'true');
  el.innerHTML = `<svg viewBox="0 0 72 72"><path class="mark-line" d="M36 6 L66 27 L54 64 L18 64 L6 27 Z M36 6 L36 64 M6 27 L66 27"/><path class="mark-fill" d="M36 20 L50 30 L45 46 L27 46 L22 30 Z"/><circle class="mark-dot" cx="36" cy="35" r="3"/></svg>`;
  document.body.prepend(el);
  const done = () => { el.classList.add('is-done'); setTimeout(() => el.remove(), 600); };
  const finish = () => setTimeout(done, Math.max(0, 1000 - (performance.now() - t0)));
  if (document.readyState === 'complete') finish(); else window.addEventListener('load', finish, { once: true });
  setTimeout(done, 1800); // never longer than this
}

/* ── 1 · hero gem ──────────────────────────────────────────────────── */
async function hero() {
  const canvas = $('#gemHero');
  return gemFor(canvas, { state: 'whole', size: 1, maxDpr: MOBILE() ? 1.25 : 2 });
}

/* ── 2 · the fracture: pinned, scrubbed, four problems ─────────────── */
async function fracture() {
  const sec = $('#fracture'); if (!sec) return;
  const cards = $$('.fcard', sec), scene = $('#fractureScene');
  const activate = (i) => cards.forEach((c, j) => c.classList.toggle('is-active', j === i));
  if (MOBILE() || reduced()) { cards.forEach((c) => c.classList.add('is-active')); scene?.classList.add('is-split'); return; }
  await near(sec);
  const gem = await gemFor($('#gemFracture', sec), { state: 'fractured', size: 1, pointer: false });
  const { ScrollTrigger } = await loadGsap();
  let problem = -1;
  ScrollTrigger.create({
    trigger: $('.fracture__track', sec), start: 'top top', end: 'bottom bottom',
    onUpdate: (self) => {
      const p = self.progress;
      const f = Math.min(1, p / .22);
      const i = p < .22 ? 0 : Math.min(3, Math.floor((p - .22) / .78 * 4));
      gem?.setFracture(f);
      if (i !== problem) { problem = i; gem?.setProblem(i); activate(i); }
      scene.classList.toggle('is-split', f > .6);
      scene.classList.toggle('is-p1', f > .6 && i === 1);
    },
  });
}

/* ── 3 · the estimator: your numbers, not ours ─────────────────────── */
function estimator() {
  const root = $('#estimator'); if (!root) return;
  const people = $('#est-people'), hours = $('#est-hours'), rate = $('#est-rate');
  const fmt = (n) => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');   // SA style: space groups, no commas
  let last = {};
  const run = () => {
    const P = +people.value, H = +hours.value, R = +rate.value;
    const yearHours = P * H * 48, cost = yearHours * R, weeks = yearHours / 40;
    $('#est-people-out').textContent = P;
    $('#est-hours-out').textContent = H.toFixed(1) + ' h';
    $('#est-rate-out').textContent = 'R ' + fmt(R);
    $('#est-total').textContent = 'R ' + fmt(cost);
    $('#est-sum').textContent = `That is ${fmt(yearHours)} hours a year, or ${fmt(weeks)} working weeks of your team's time spent moving data between systems.`;
    last = { P, H, R, cost, weeks };
  };
  [people, hours, rate].forEach((el) => el.addEventListener('input', run));
  run();
  $('#estCta')?.addEventListener('click', () => {
    const notes = $('#d-notes'); if (!notes || notes.value.trim()) return;
    notes.value = `From the estimator on your homepage: ${last.P} people × ${last.H} h/week × R ${fmt(last.R)}/h ≈ R ${fmt(last.cost)} a year (${fmt(last.weeks)} working weeks).`;
    notes.closest('.field')?.classList.add('is-filled');
  });
}

/* ── 4 · the reassembly: shards lock, the product rises ────────────── */
async function reassembly() {
  const sec = $('#reassembly'); if (!sec) return;
  const product = $('#reassemblyProduct'), copy = $('.reassembly__copy', sec), scene = $('#reassemblyScene');
  if (MOBILE() || reduced()) { revealOnce([copy, product]); return; }
  await near(sec);
  const gem = await gemFor($('#gemReassembly', sec), { state: 'fractured', size: 1, pointer: false });
  gem?.setFracture(1);
  const { ScrollTrigger } = await loadGsap();
  copy.style.opacity = 0; copy.style.transform = 'translateY(16px)';
  ScrollTrigger.create({
    trigger: $('.reassembly__track', sec), start: 'top top', end: 'bottom bottom',
    onUpdate: (self) => {
      const p = self.progress;
      const lock = Math.min(1, p / .45);                      // 0 → 1 as the shards come home
      gem?.setFracture(1 - lock);
      const c = Math.max(0, Math.min(1, (p - .3) / .2));       // the headline, once it is nearly whole
      copy.style.opacity = c; copy.style.transform = `translateY(${16 * (1 - c)}px)`;
      const r = Math.max(0, Math.min(1, (p - .55) / .35));     // then the product rises through the gem
      const e = 1 - Math.pow(1 - r, 3);
      scene.style.opacity = 1 - e * .92; scene.style.transform = `scale(${1 - e * .12})`;
      product.style.opacity = e; product.style.transform = `translate(-50%, ${-38 - 12 * e}%)`;
      copy.style.opacity = Math.min(c, 1 - e);
    },
  });
}

/* ── 5 · services: the stage changes with the row ──────────────────── */
function services() {
  const rows = $$('#svcRows .row'), stage = $('#svcStage'); if (!rows.length) return;
  const stageDiagrams = rows.map((row) => { const d = $('.diagram', row).cloneNode(true); stage.appendChild(d); return d; });
  const set = (i) => { rows.forEach((r, j) => r.classList.toggle('is-active', j === i)); stageDiagrams.forEach((d, j) => d.classList.toggle('is-on', j === i)); };
  set(0);
  if (!('IntersectionObserver' in window)) { stageDiagrams[0].classList.add('is-on'); rows.forEach((r) => $('.diagram', r).classList.add('is-on')); return; }
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) set(+e.target.dataset.svc); }), { rootMargin: '-45% 0px -45% 0px', threshold: 0 });
  rows.forEach((r) => io.observe(r));
  // small screens: each row carries its own diagram; it plays once it is in view
  const io2 = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { $('.diagram', e.target).classList.add('is-on'); io2.unobserve(e.target); } }), { threshold: .3 });
  rows.forEach((r) => io2.observe(r));
}

/* ── 9 · the form: floating labels, inline validation, two steps on a phone, a real finish ── */
function form() {
  const f = $('#discoveryForm'); if (!f) return;
  const done = $('#formDone'), label = $('#formStepLabel'), next = $('#formNext');
  const groups = $$('.form__group', f);
  const fill = (el) => el.closest('.field--float')?.classList.toggle('is-filled', !!el.value);
  $$('.field--float input, .field--float textarea', f).forEach((el) => { fill(el); el.addEventListener('input', () => fill(el)); });
  const mark = (el, bad) => { el.closest('.field')?.classList.toggle('is-invalid', bad); const err = $('#' + el.id + '-err'); if (err) err.hidden = !bad; el.setAttribute('aria-invalid', bad ? 'true' : 'false'); };
  $$('[required]', f).forEach((el) => {
    el.addEventListener('blur', () => { if (el.value || el.type === 'checkbox') mark(el, !el.checkValidity()); });
    el.addEventListener('input', () => { if (el.checkValidity()) mark(el, false); });
    el.addEventListener('change', () => mark(el, !el.checkValidity()));
  });
  const step = (n) => {
    f.dataset.step = n;
    groups.forEach((g) => g.classList.toggle('is-on', +g.dataset.group === n));
    if (label) label.textContent = n === 1 ? 'Step 1 of 2 · About you' : 'Step 2 of 2 · The work';
    $('.form__steps .mono', f).textContent = `${n} / 2`;
  };
  next?.addEventListener('click', () => {
    const bad = $$('[required]', groups[0]).filter((el) => { const b = !el.checkValidity(); mark(el, b); return b; });
    if (bad.length) { bad[0].focus(); return; }
    step(2); $('select, input, textarea', groups[1])?.focus();
  });
  f.addEventListener('submit', () => {
    if (!f.checkValidity()) {
      const first = $(':invalid', f); const g = first?.closest('.form__group');
      if (g && !g.classList.contains('is-on') && matchMedia('(max-width: 720px)').matches) { step(+g.dataset.group); first.focus(); }
      return;
    }
    setTimeout(() => { f.classList.add('is-sent'); done.classList.add('is-on'); done.focus(); }, 600);
  });
}

/* ── 10 · the small gem beside the form ────────────────────────────── */
async function small() {
  await near($('#discovery'), '40%');
  return gemFor($('#gemSmall'), { state: 'small', size: .78, pointer: false, maxDpr: 1.5, lite: true });
}

/* ── go ─────────────────────────────────────────────────────────────── */
loader();
transitions();
headlines();
navHide();
estimator();
services();
living();
processLoop($('#processLoop'));
form();
magnetic('.btn, .form__send');
spine($$('[data-spine]'));
startLenis().then((l) => { window.__lenis = l; }).catch(() => {});

// the gems mount after first paint so the headline is never waiting on them
const afterPaint = (fn) => requestAnimationFrame(() => setTimeout(fn, 0));
afterPaint(async () => {
  await hero();                       // the one scene that is always in view first
  fracture(); reassembly(); small();  // each of these waits until its section is near
});
