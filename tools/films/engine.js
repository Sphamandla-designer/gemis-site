// A deterministic timeline: every frame is a pure function of t, so Playwright
// can seek and screenshot frame by frame. No CSS animations, no timers.
const E = {
  out: (x) => 1 - Math.pow(1 - x, 3), inout: (x) => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
  back: (x) => { const c = 1.6; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); }, lin: (x) => x,
};
const TW = new Map(), SC = [], CAPS = [], HOOKS = [];
// tw('#el', start, duration, { x:[from,to], y, s, r, o, rx, ry, b (blur), w (width %) }, ease)
function tw(sel, t0, d, props, ease = 'out') {
  for (const el of document.querySelectorAll(sel)) { if (!TW.has(el)) TW.set(el, []); TW.get(el).push({ t0, d, props, ease }); }
}
function scene(id, t0, t1, fade = .35) { SC.push({ el: document.getElementById(id), t0, t1, fade }); }
function cap(t0, t1, text) { CAPS.push([t0, t1, text]); }
function hook(fn) { HOOKS.push(fn); }
const DEF = { x: 0, y: 0, s: 1, r: 0, o: 1, rx: 0, ry: 0, b: 0 };
function val(list, p, t) {
  let v, seen = false;
  for (const k of list) {
    if (!(p in k.props)) continue; const [a, b] = k.props[p];
    if (!seen) { v = a; seen = true; }
    if (t >= k.t0 + k.d) v = b; else if (t >= k.t0) { v = a + (b - a) * E[k.ease]((t - k.t0) / k.d); break; } else break;
  }
  return seen ? v : undefined;
}
window.seek = (t) => {
  for (const s of SC) {
    const a = Math.min(1, Math.max(0, (t - s.t0) / s.fade)), b = Math.min(1, Math.max(0, (s.t1 - t) / s.fade));
    const on = t >= s.t0 && t < s.t1; s.el.style.display = on ? 'block' : 'none'; s.el.style.opacity = Math.min(a, b);
  }
  for (const [el, list] of TW) {
    const g = (p) => { const v = val(list, p, t); return v === undefined ? DEF[p] : v; };
    el.style.transform = `translate(${g('x')}px,${g('y')}px) perspective(1600px) rotateX(${g('rx')}deg) rotateY(${g('ry')}deg) rotate(${g('r')}deg) scale(${g('s')})`;
    el.style.opacity = g('o'); const b = g('b'); el.style.filter = b ? `blur(${b}px)` : '';
    const w = val(list, 'w', t); if (w !== undefined) el.style.width = w + '%';
  }
  const c = CAPS.find(([a, b]) => t >= a && t < b), ce = document.getElementById('cap');
  if (ce) { ce.style.display = c ? 'block' : 'none'; if (c) ce.firstElementChild.textContent = c[2]; }
  for (const h of HOOKS) h(t);
};
