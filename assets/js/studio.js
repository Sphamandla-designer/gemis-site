/* ═══════════════════════════════════════════════════════════════════════
   GEMIS® Studio — homepage interactions
   GSAP 3 + ScrollTrigger + Lenis. Everything animates FROM a visible
   state: if this file never runs, the page is complete and readable.
   ═══════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(pointer: fine)').matches;
  var hasGsap = typeof gsap !== 'undefined';
  if (hasGsap && typeof ScrollTrigger !== 'undefined') gsap.registerPlugin(ScrollTrigger);

  /* ── Smooth scroll (Lenis synced to GSAP ticker) ─────────────────── */
  var lenis = null;
  if (!reduced && typeof Lenis !== 'undefined' && hasGsap) {
    lenis = new Lenis({ duration: 1.1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
  }
  function scrollToEl(el) {
    if (!el) return;
    if (lenis) lenis.scrollTo(el, { offset: -70 });
    else el.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' });
  }
  /* anchor links */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var el = document.querySelector(a.getAttribute('href'));
      if (el) { e.preventDefault(); scrollToEl(el); }
    });
  });

  /* ── Preloader ───────────────────────────────────────────────────── */
  var preOn = document.documentElement.classList.contains('preload-on') && hasGsap && !reduced;
  function runPreloader(done) {
    var pre = document.getElementById('preloader');
    if (!pre) return done();
    try { sessionStorage.setItem('gemisStudioPre', '1'); } catch (e) {}
    var count = document.getElementById('preCount');
    var words = pre.querySelectorAll('[data-preword]');
    var n = { v: 0 };
    var tl = gsap.timeline({
      onComplete: function () { pre.style.display = 'none'; }
    });
    tl.to(n, {
      v: 100, duration: 1.6, ease: 'power2.out',
      onUpdate: function () { count.textContent = String(Math.round(n.v)).padStart(2, '0'); }
    }, 0);
    words.forEach(function (w, i) {
      tl.set(words, { className: 'preloader__word' }, i * 0.5)
        .set(w, { className: 'preloader__word is-on' }, i * 0.5);
    });
    tl.to(pre, { clipPath: 'inset(0 0 100% 0)', duration: 0.9, ease: 'expo.inOut' }, 1.6);
    /* hero reveal starts 200ms before the wipe finishes */
    tl.add(done, 1.6 + 0.9 - 0.2);
  }

  /* ── 01 · Navigation ─────────────────────────────────────────────── */
  var nav = document.getElementById('nav');
  function onScrollNav() { nav.classList.toggle('is-solid', window.scrollY > 100); }
  window.addEventListener('scroll', onScrollNav, { passive: true });
  onScrollNav();

  var burger = document.getElementById('burger');
  var mmenu = document.getElementById('mobileMenu');
  function closeMenu() {
    burger.classList.remove('is-open'); mmenu.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false'); mmenu.setAttribute('aria-hidden', 'true');
  }
  burger.addEventListener('click', function () {
    var open = !mmenu.classList.contains('is-open');
    burger.classList.toggle('is-open', open); mmenu.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open)); mmenu.setAttribute('aria-hidden', String(!open));
  });
  mmenu.querySelectorAll('[data-mclose]').forEach(function (a) { a.addEventListener('click', closeMenu); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });

  /* ── 02 · Hero scrubber ──────────────────────────────────────────── */
  var scrub = document.getElementById('scrub');
  var handle = document.getElementById('scrubHandle');
  var pos = 50;
  function setPos(p, announce) {
    pos = Math.max(0, Math.min(100, p));
    scrub.style.setProperty('--pos', pos + '%');
    handle.setAttribute('aria-valuenow', String(Math.round(pos)));
    handle.setAttribute('aria-valuetext', Math.round(pos) + '% — ' +
      (pos < 40 ? 'mostly showing the before interface' :
       pos > 60 ? 'mostly showing the after interface' :
       'showing equal parts of the before and after interface'));
  }
  setPos(50);

  /* drag (pointer events; also serves touch) */
  var sweep = null;
  function killSweep() { if (sweep) { sweep.kill(); sweep = null; } }
  handle.addEventListener('pointerdown', function (e) {
    killSweep();
    scrub.classList.add('is-grabbing');
    handle.setPointerCapture(e.pointerId);
    var rect = scrub.getBoundingClientRect();
    function move(ev) { setPos(((ev.clientX - rect.left) / rect.width) * 100); }
    function up() {
      scrub.classList.remove('is-grabbing');
      handle.removeEventListener('pointermove', move);
      handle.removeEventListener('pointerup', up);
      handle.removeEventListener('pointercancel', up);
    }
    handle.addEventListener('pointermove', move);
    handle.addEventListener('pointerup', up);
    handle.addEventListener('pointercancel', up);
  });
  /* keyboard — works with or without JS-driven motion */
  handle.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { killSweep(); setPos(pos - 2); e.preventDefault(); }
    else if (e.key === 'ArrowRight') { killSweep(); setPos(pos + 2); e.preventDefault(); }
    else if (e.key === 'Home') { killSweep(); setPos(0); e.preventDefault(); }
    else if (e.key === 'End') { killSweep(); setPos(100); e.preventDefault(); }
  });

  function heroIntro() {
    if (!hasGsap || reduced) return;
    gsap.from('.hero__title .mask__inner', {
      yPercent: 110, duration: 0.9, ease: 'expo.out', stagger: 0.06, clearProps: 'transform'
    });
    gsap.from(['.hero__eyebrow', '.hero__sub', '.hero__ctas'], {
      y: 24, opacity: 0, duration: 0.8, ease: 'expo.out', stagger: 0.08, delay: 0.25, clearProps: 'all'
    });
  }

  if (preOn) runPreloader(heroIntro); else heroIntro();

  /* auto-sweep 20 → 80 → 50 teaches the interaction, once, when the demo scrolls into view */
  if (hasGsap && !reduced) {
    ScrollTrigger.create({
      trigger: '.demo .scrub', start: 'top 70%', once: true,
      onEnter: function () {
        var p = { v: 50 };
        sweep = gsap.timeline({ onUpdate: function () { setPos(p.v); } });
        sweep.to(p, { v: 20, duration: 0.7, ease: 'power2.inOut' })
             .to(p, { v: 80, duration: 1.0, ease: 'power2.inOut' })
             .to(p, { v: 50, duration: 0.7, ease: 'power2.inOut' });
      }
    });
    /* gentle drift as the demo passes through the viewport (mockup roots, so
       the clip edge stays glued to the divider) */
    gsap.fromTo(['.demo .mkb', '.demo .mka'],
      { yPercent: -3, scale: 1.05 },
      { yPercent: 3, scale: 1.05, ease: 'none',
        scrollTrigger: { trigger: '.demo .scrub', start: 'top bottom', end: 'bottom top', scrub: true } });
  }

  /* ── 04 · Problem mirror ─────────────────────────────────────────── */
  (function () {
    var stage = document.getElementById('problemStage');
    var wrap = stage.closest('.problem__stagewrap');
    var lines = Array.prototype.slice.call(stage.querySelectorAll('.problem__line'));
    var bar = document.getElementById('problemBar');
    var pauseBtn = document.getElementById('problemPause');
    lines.forEach(function (l) {
      l.addEventListener('click', function () { scrollToEl(document.getElementById(l.dataset.target)); });
    });
    if (!hasGsap || reduced || lines.length < 2) return;

    stage.classList.add('is-live'); wrap.classList.add('is-live');
    var idx = 0, paused = false, hover = false, timer = null;
    var HOLD = 3200;

    function show(i) {
      var prev = lines[idx]; idx = i % lines.length;
      var next = lines[idx];
      gsap.to(prev, { opacity: 0, y: -40, filter: 'blur(12px)', duration: 0.5, ease: 'expo.in',
        onComplete: function () { prev.classList.remove('is-on'); gsap.set(prev, { clearProps: 'all' }); } });
      next.classList.add('is-on');
      gsap.fromTo(next, { opacity: 0, y: 40, filter: 'blur(12px)' },
        { opacity: 1, y: 0, filter: 'blur(0px)', duration: 0.7, ease: 'expo.out' });
      runBar();
    }
    var barTween = null;
    function runBar() {
      if (barTween) barTween.kill();
      gsap.set(bar, { width: '0%' });
      barTween = gsap.to(bar, { width: '100%', duration: HOLD / 1000, ease: 'none', paused: paused || hover });
      clearTimeout(timer);
      timer = setTimeout(tick, HOLD);
    }
    function tick() { if (paused || hover) { timer = setTimeout(tick, 300); return; } show(idx + 1); }

    lines.forEach(function (l, i) { if (i !== 0) l.classList.remove('is-on'); });
    lines[0].classList.add('is-on');
    runBar();

    wrap.addEventListener('mouseenter', function () { hover = true; if (barTween) barTween.pause(); });
    wrap.addEventListener('mouseleave', function () { hover = false; if (!paused && barTween) barTween.play(); });
    wrap.addEventListener('focusin', function () { hover = true; if (barTween) barTween.pause(); });
    wrap.addEventListener('focusout', function () { hover = false; if (!paused && barTween) barTween.play(); });
    pauseBtn.addEventListener('click', function () {
      paused = !paused;
      pauseBtn.setAttribute('aria-pressed', String(paused));
      pauseBtn.setAttribute('aria-label', paused ? 'Resume rotation' : 'Pause rotation');
      pauseBtn.textContent = paused ? '▶' : '⏸';
      if (barTween) paused ? barTween.pause() : barTween.play();
    });
  })();

  /* ── Generic scroll reveals ──────────────────────────────────────── */
  if (hasGsap && !reduced) {
    var ST = { start: 'top 75%', once: true };

    /* section labels + headline blocks */
    gsap.utils.toArray('.slabel, .demo__line, .practice__lead, .lead2__head, .instr__lead, .spec__head, .outc__head, .diff__head, .pricing__head, .faq__head, .contact__sub, .svcs__title').forEach(function (el) {
      gsap.from(el, { y: 40, opacity: 0, duration: 0.8, ease: 'expo.out',
        scrollTrigger: Object.assign({ trigger: el }, ST) });
    });

    /* practice principles + rules */
    gsap.from('.practice__col', { y: 40, opacity: 0, duration: 0.8, ease: 'expo.out', stagger: 0.12,
      scrollTrigger: Object.assign({ trigger: '.practice__cols' }, ST) });
    gsap.from('.practice__rule', { scaleY: 0, duration: 0.8, ease: 'expo.out',
      scrollTrigger: Object.assign({ trigger: '.practice__cols' }, ST) });

    /* new brief blocks — quiet row/cell staggers */
    [['.lead2__specs', '.lead2__specs li'], ['.staff__rows', '.staff__row'],
     ['.instr__cols', '.instr__cols li'], ['.outc__row', '.outc__item']].forEach(function (pair) {
      if (!document.querySelector(pair[0])) return;
      gsap.from(pair[1], { y: 24, opacity: 0, duration: 0.6, ease: 'expo.out', stagger: 0.05,
        scrollTrigger: Object.assign({ trigger: pair[0] }, ST) });
    });

    /* index rows — work + services */
    [['.windex', '.windex__item'], ['.svcx', '.svcx__item']].forEach(function (pair) {
      if (!document.querySelector(pair[0])) return;
      gsap.from(pair[1], { y: 34, opacity: 0, duration: 0.7, ease: 'expo.out', stagger: 0.08,
        scrollTrigger: Object.assign({ trigger: pair[0] }, ST) });
    });

    /* contact heading line masks */
    gsap.from('.contact__head .mask__inner', { yPercent: 110, duration: 0.9, ease: 'expo.out', stagger: 0.06,
      scrollTrigger: Object.assign({ trigger: '.contact__head' }, ST) });
  }

  /* device pointer tilt */
  if (finePointer && !reduced && hasGsap) {
    document.querySelectorAll('[data-tilt]').forEach(function (dev) {
      var holder = dev.closest('.svc__visual');
      var rx = gsap.quickTo(dev, 'rotationX', { duration: 0.6, ease: 'power4.out' });
      var ry = gsap.quickTo(dev, 'rotationY', { duration: 0.6, ease: 'power4.out' });
      holder.addEventListener('pointermove', function (e) {
        var r = holder.getBoundingClientRect();
        ry(((e.clientX - r.left) / r.width - 0.5) * 20);
        rx(-((e.clientY - r.top) / r.height - 0.5) * 20);
      });
      holder.addEventListener('pointerleave', function () { rx(0); ry(0); });
    });
  }

  /* ── 08 · Pipeline draw ──────────────────────────────────────────── */
  if (hasGsap && !reduced) {
    var main = document.getElementById('pipeMain');
    var stop = document.getElementById('pipeStop');
    if (main) {
      var L = main.getTotalLength();
      var tl = gsap.timeline({ scrollTrigger: { trigger: '.diff__pipe', start: 'top 75%', once: true } });
      gsap.set(main, { strokeDasharray: L, strokeDashoffset: L });
      tl.to(main, { strokeDashoffset: 0, duration: 2, ease: 'power2.inOut' }, 0);
      document.querySelectorAll('.diff__node').forEach(function (node, i) {
        tl.from(node, { scale: 0, transformOrigin: '50% 66%', duration: 0.45, ease: 'back.out(2)' }, i * 0.55 + 0.15);
        tl.fromTo(node.querySelector('.diff__pulse'),
          { attr: { r: 9 }, opacity: 0.8 }, { attr: { r: 22 }, opacity: 0, duration: 0.8 }, i * 0.55 + 0.3);
      });
      /* the dimmed line appears after — it stops at node 2. That contrast is the argument. */
      var Ls = stop.getTotalLength();
      gsap.set(stop, { strokeDasharray: Ls, strokeDashoffset: Ls, opacity: 0.55 });
      tl.to(stop, { strokeDashoffset: 0, duration: 1, ease: 'power2.inOut' }, 2.2);
      tl.from('.diff__stoplabel', { opacity: 0, duration: 0.6 }, 2.4);
    }
  }

  /* ── 09 · How we work — sticky number ────────────────────────────── */
  if (hasGsap && !reduced) {
    var numEl = document.getElementById('howNum');
    document.querySelectorAll('.how__step').forEach(function (step) {
      ScrollTrigger.create({
        trigger: step, start: 'top 55%', end: 'bottom 55%',
        onToggle: function (self) {
          if (!self.isActive || numEl.textContent === step.dataset.step) return;
          numEl.classList.add('is-swapping');
          setTimeout(function () {
            numEl.textContent = step.dataset.step;
            numEl.classList.remove('is-swapping');
          }, 200);
        }
      });
    });
    gsap.to('#howRail', {
      height: '100%', ease: 'none',
      scrollTrigger: { trigger: '.how__steps', start: 'top 70%', end: 'bottom 40%', scrub: true }
    });
  }

  /* ── Header clock — Johannesburg time (SAST) ─────────────────────── */
  (function () {
    var el = document.getElementById('navClock');
    if (!el) return;
    function tick() {
      var t = new Date().toLocaleTimeString('en-GB', { timeZone: 'Africa/Johannesburg', hour12: false });
      el.textContent = 'JHB ' + t;
    }
    tick();
    setInterval(tick, 1000);
  })();

  /* ── Scramble-decode hover on index names ────────────────────────── */
  (function () {
    if (reduced) return;
    var CHARS = '#/[]<>—+*=x%';
    document.querySelectorAll('[data-scramble]').forEach(function (el) {
      var original = el.textContent;
      var frame = null;
      el.closest('a, button').addEventListener('mouseenter', function () {
        var i = 0, len = original.length, ticks = 0;
        cancelAnimationFrame(frame);
        (function step() {
          ticks++;
          if (ticks % 2 === 0) i++;
          if (i >= len) { el.textContent = original; return; }
          var out = original.slice(0, i);
          for (var k = i; k < len; k++) {
            out += original[k] === ' ' ? ' ' : CHARS[(Math.random() * CHARS.length) | 0];
          }
          el.textContent = out;
          frame = requestAnimationFrame(step);
        })();
      });
    });
  })();

  /* ── 06 · Services — expanding index (first open; FR-06 keeps price
        and duration visible in every collapsed row) ─────────────────── */
  (function () {
    var wrap = document.getElementById('svcx');
    if (!wrap) return;
    wrap.classList.add('svcx--js');
    var heads = wrap.querySelectorAll('.svcx__head');
    function openOnly(head) {
      heads.forEach(function (h) {
        var body = document.getElementById(h.getAttribute('aria-controls'));
        var on = h === head;
        h.setAttribute('aria-expanded', String(on));
        body.classList.toggle('is-open', on);
      });
    }
    heads.forEach(function (h) {
      h.addEventListener('click', function () {
        var open = h.getAttribute('aria-expanded') === 'true';
        openOnly(open ? null : h);
        if (!open && hasGsap && typeof ScrollTrigger !== 'undefined') {
          setTimeout(function () { ScrollTrigger.refresh(); }, 600);
        }
      });
    });
    openOnly(heads[0]);
    /* the initial collapse changes page height after ScrollTrigger has
       measured — recalc once the height transition settles */
    if (hasGsap && typeof ScrollTrigger !== 'undefined') {
      setTimeout(function () { ScrollTrigger.refresh(); }, 700);
    }
  })();

  /* ── 07 · Work index — preview follows the pointer ───────────────── */
  (function () {
    if (!window.matchMedia('(hover: hover) and (min-width: 1024px)').matches) return;
    var rows = document.querySelectorAll('.windex__row');
    if (!rows.length) return;
    var active = null;
    var qx = null, qy = null;
    rows.forEach(function (row) {
      var pv = document.getElementById(row.dataset.pv);
      if (!pv) return;
      row.addEventListener('mouseenter', function () {
        if (active) active.classList.remove('is-on');
        active = pv;
        pv.classList.add('is-on');
        if (hasGsap && !qx) {
          qx = gsap.quickTo(pv, 'x', { duration: 0.4, ease: 'power3.out' });
          qy = gsap.quickTo(pv, 'y', { duration: 0.4, ease: 'power3.out' });
        }
      });
      row.addEventListener('mouseleave', function () {
        pv.classList.remove('is-on');
        if (active === pv) active = null;
        qx = null; qy = null;
      });
    });
    window.addEventListener('pointermove', function (e) {
      if (!active) return;
      var w = active.offsetWidth, h = active.offsetHeight;
      var x = Math.min(e.clientX + 28, window.innerWidth - w - 20);
      var y = Math.min(Math.max(e.clientY - h / 2, 20), window.innerHeight - h - 20);
      if (qx) { qx(x); qy(y); }
      else { active.style.transform = 'translate(' + x + 'px,' + y + 'px)'; }
    }, { passive: true });
  })();

  /* ── Hero dot field — pointer-reactive particle grid (canvas 2D) ─── */
  (function () {
    var canvas = document.getElementById('heroDots');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    var dots = [], W = 0, H = 0, raf = null;
    var mx = -9999, my = -9999;
    var SP = 30, R = 130, DOT = 1.1;
    function build() {
      var rect = canvas.parentElement.getBoundingClientRect();
      W = canvas.width = Math.floor(rect.width * devicePixelRatio);
      H = canvas.height = Math.floor(rect.height * devicePixelRatio);
      canvas.style.width = rect.width + 'px';
      canvas.style.height = rect.height + 'px';
      dots = [];
      var sp = SP * devicePixelRatio;
      for (var y = sp / 2; y < H; y += sp) {
        for (var x = sp / 2; x < W; x += sp) {
          dots.push({ ox: x, oy: y, x: x, y: y });
        }
      }
    }
    function draw(t) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = 'rgba(210, 210, 205, 0.4)';
      var r = R * devicePixelRatio;
      for (var i = 0; i < dots.length; i++) {
        var d = dots[i];
        var wob = Math.sin(t / 1400 + d.ox / 220 + d.oy / 320) * 1.6 * devicePixelRatio;
        var tx = d.ox, ty = d.oy + wob;
        var dx = tx - mx, dy = ty - my;
        var dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < r && dist > 0.01) {
          var f = (1 - dist / r) * 26 * devicePixelRatio;
          tx += (dx / dist) * f; ty += (dy / dist) * f;
        }
        d.x += (tx - d.x) * 0.12; d.y += (ty - d.y) * 0.12;
        ctx.beginPath();
        ctx.arc(d.x, d.y, DOT * devicePixelRatio, 0, 6.2832);
        ctx.fill();
      }
    }
    function drawStatic() {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = 'rgba(210, 210, 205, 0.3)';
      dots.forEach(function (d) {
        ctx.beginPath();
        ctx.arc(d.ox, d.oy, DOT * devicePixelRatio, 0, 6.2832);
        ctx.fill();
      });
    }
    build();
    if (reduced || !window.matchMedia('(min-width: 768px)').matches) {
      drawStatic();
    } else {
      var hero = canvas.closest('.hero');
      hero.addEventListener('pointermove', function (e) {
        var rect = canvas.getBoundingClientRect();
        mx = (e.clientX - rect.left) * devicePixelRatio;
        my = (e.clientY - rect.top) * devicePixelRatio;
      }, { passive: true });
      hero.addEventListener('pointerleave', function () { mx = my = -9999; });
      var running = true;
      (function loop(t) { if (running) { draw(t || 0); raf = requestAnimationFrame(loop); } })(0);
      /* stop rendering when the hero leaves the viewport */
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
          var vis = entries[0].isIntersecting;
          if (vis && !running) { running = true; raf = requestAnimationFrame(function loop2(t) { if (running) { draw(t); raf = requestAnimationFrame(loop2); } }); }
          else if (!vis) { running = false; cancelAnimationFrame(raf); }
        }).observe(canvas);
      }
    }
    var rT2;
    window.addEventListener('resize', function () {
      clearTimeout(rT2);
      rT2 = setTimeout(function () { build(); if (reduced || !window.matchMedia('(min-width: 768px)').matches) drawStatic(); }, 250);
    });
  })();

  /* ── 09B · Own standards — live token specimen (FR-11) ───────────── */
  (function () {
    var tokensEl = document.getElementById('specTokens');
    if (!tokensEl) return;
    var css = getComputedStyle(document.documentElement);
    function toHex(v) {
      var m = v.trim().match(/rgba?\((\d+),?\s*(\d+),?\s*(\d+)/);
      if (!m && /^#/.test(v.trim())) return v.trim().toUpperCase();
      if (!m) return v.trim();
      return '#' + [m[1], m[2], m[3]].map(function (n) {
        return (+n).toString(16).padStart(2, '0');
      }).join('').toUpperCase();
    }
    function lum(hex) {
      var c = [1, 3, 5].map(function (i) {
        var v = parseInt(hex.slice(i, i + 2), 16) / 255;
        return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
      });
      return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
    }
    function ratio(a, b) {
      var l1 = lum(a), l2 = lum(b);
      return ((Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05));
    }
    var names = ['--ink', '--ink-2', '--ink-3', '--bone', '--bone-dim', '--gold'];
    var vals = {};
    names.forEach(function (n) {
      var raw = css.getPropertyValue(n).trim();
      var hex = toHex(raw);
      vals[n] = hex;
      var d = document.createElement('div');
      d.className = 'spec__swatch';
      d.innerHTML = '<i style="background:' + raw + '"></i><b>' + n + '</b><span>' + hex + '</span>';
      tokensEl.appendChild(d);
    });
    /* type scale — computed live from real elements on this page */
    var typeEl = document.getElementById('specType');
    [['t-display', 'Display', '.hero__title', 'Aa'], ['t-body', 'Body', '.hero__sub', 'Aa'], ['t-mono', 'Mono', '.slabel', '01']].forEach(function (t) {
      var src = document.querySelector(t[2]);
      var size = src ? Math.round(parseFloat(getComputedStyle(src).fontSize)) : 0;
      var row = document.createElement('div');
      row.className = 'spec__trow';
      row.innerHTML = '<em class="' + t[0] + '">' + t[3] + ' ' + t[1] + '</em><span>' + size + 'px · computed</span>';
      typeEl.appendChild(row);
    });
    /* contrast ratios — computed live from the tokens above */
    var conEl = document.getElementById('specContrast');
    [['--bone', '--ink', 'Text / base'], ['--bone-dim', '--ink', 'Secondary / base'], ['--gold', '--ink', 'Accent / base']].forEach(function (pair) {
      var r = ratio(vals[pair[0]], vals[pair[1]]);
      var row = document.createElement('div');
      row.className = 'spec__crow';
      row.innerHTML = '<b>' + pair[2] + '</b><span>' + r.toFixed(1) + ' : 1 — AA ' + (r >= 4.5 ? '✓' : '✗') + '</span>';
      conEl.appendChild(row);
    });
  })();

  /* ── 13 · FAQ accordion (single-open, fragment-linkable FR-13) ───── */
  (function () {
    var faq = document.querySelector('.faq');
    faq.classList.add('faq--js');
    var qs = faq.querySelectorAll('.faq__q');
    function openOnly(q) {
      qs.forEach(function (other) {
        other.setAttribute('aria-expanded', 'false');
        document.getElementById(other.getAttribute('aria-controls')).classList.remove('is-open');
      });
      if (q) {
        q.setAttribute('aria-expanded', 'true');
        document.getElementById(q.getAttribute('aria-controls')).classList.add('is-open');
      }
    }
    qs.forEach(function (q) {
      q.addEventListener('click', function () {
        var open = q.getAttribute('aria-expanded') === 'true';
        openOnly(open ? null : q);
        if (!open && history.replaceState) history.replaceState(null, '', '#' + q.id);
      });
    });
    /* deep link: #faq-qN opens that question */
    function openFromHash() {
      var m = (location.hash || '').match(/^#(faq-q\d+)$/);
      if (!m) return;
      var q = document.getElementById(m[1]);
      if (!q) return;
      openOnly(q);
      setTimeout(function () { scrollToEl(q.closest('.faq__item')); q.focus(); }, 150);
    }
    window.addEventListener('hashchange', openFromHash);
    openFromHash();
  })();

  /* ── Analytics conversion events (FR-23) — dataLayer pushes only,
        no cookies are set by this page ─────────────────────────────── */
  var track = function (event, detail) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: event }, detail || {}));
  };
  document.querySelectorAll('a[href^="mailto:"]').forEach(function (a) {
    a.addEventListener('click', function () {
      track(a.classList.contains('contact__call') ? 'booking_click' : 'email_click');
    });
  });
  document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
    a.addEventListener('click', function () { track('tel_click'); });
  });
  (function () {
    var pricing = document.getElementById('pricing');
    if (!pricing || !('IntersectionObserver' in window)) return;
    var seen = false;
    new IntersectionObserver(function (entries, obs) {
      if (!seen && entries[0].isIntersecting) { seen = true; track('pricing_view'); obs.disconnect(); }
    }, { threshold: 0.25 }).observe(pricing);
  })();

  /* ── 14 · Contact form ───────────────────────────────────────────── */
  (function () {
    var form = document.getElementById('cform');
    var status = document.getElementById('formStatus');
    var msg = document.getElementById('f-msg');
    var counter = document.getElementById('msgCount');

    msg.addEventListener('input', function () {
      var n = msg.value.trim().length;
      counter.textContent = n < 20 ? n + ' / 20 min' : n + ' characters';
    });

    function validateField(input) {
      var field = input.closest('.cform__field');
      var ok = true;
      if (input.type === 'checkbox') ok = input.checked;
      else {
        if (input.required && !input.value.trim()) ok = false;
        if (ok && input.type === 'email' && input.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value)) ok = false;
        if (ok && input.minLength > 0 && input.value.trim().length < input.minLength) ok = false;
      }
      field.classList.toggle('is-error', !ok);
      var err = field.querySelector('.cform__err');
      if (err) err.setAttribute('aria-hidden', String(ok));
      return ok;
    }
    /* validate on blur, never on keystroke */
    form.querySelectorAll('input, textarea').forEach(function (input) {
      input.addEventListener('blur', function () { if (input.value) validateField(input); });
    });
    /* analytics: form_start on first interaction (FR-23) */
    var started = false;
    form.addEventListener('focusin', function () {
      if (!started) { started = true; track('form_start'); }
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var allOk = true;
      form.querySelectorAll('input[required], textarea[required], input[type="email"]').forEach(function (input) {
        if (!validateField(input)) allOk = false;
      });
      if (!allOk) { status.textContent = 'Please fix the highlighted fields.'; return; }
      status.textContent = '';
      form.classList.add('is-sending');
      track('form_submit');
      var data = new FormData(form);
      var body = 'Name: ' + data.get('name') + '\nEmail: ' + data.get('email') +
        '\nCompany: ' + (data.get('company') || '—') + '\nNeed: ' + data.get('need') +
        '\nBudget: ' + data.get('budget') +
        '\nConsent: given per the published privacy notice, ' + new Date().toISOString().slice(0, 10) +
        '\n\n' + data.get('message');
      /* static site — hand the enquiry to the visitor's mail client */
      window.location.href = 'mailto:info@gemis.co.za?subject=' +
        encodeURIComponent('Studio enquiry — ' + data.get('need')) +
        '&body=' + encodeURIComponent(body);
      setTimeout(function () {
        form.classList.remove('is-sending');
        form.classList.add('is-done');
        status.textContent = "Thanks — we'll be in touch within one business day.";
      }, 900);
    });
  })();

  /* ── Housekeeping ────────────────────────────────────────────────── */
  if (hasGsap) {
    var rT;
    window.addEventListener('resize', function () {
      clearTimeout(rT);
      rT = setTimeout(function () { ScrollTrigger.refresh(); }, 200);
    });
  }
})();
