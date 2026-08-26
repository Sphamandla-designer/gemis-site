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

  /* ── Custom cursor ───────────────────────────────────────────────── */
  if (finePointer && !reduced && hasGsap) {
    document.body.classList.add('has-cursor');
    var cursor = document.getElementById('cursor');
    var label = document.getElementById('cursorLabel');
    var cx = gsap.quickTo(cursor, 'x', { duration: 0.15, ease: 'power4.out' });
    var cy = gsap.quickTo(cursor, 'y', { duration: 0.15, ease: 'power4.out' });
    window.addEventListener('pointermove', function (e) { cx(e.clientX); cy(e.clientY); }, { passive: true });
    document.addEventListener('pointerover', function (e) {
      var special = e.target.closest('[data-cursor]');
      if (special) {
        var size = special.getAttribute('data-cursor-size');
        cursor.className = 'cursor ' + (size === 'drag' ? 'is-drag' : size === 'view' ? 'is-view' : 'is-link');
        label.textContent = special.getAttribute('data-cursor') || '';
        return;
      }
      if (e.target.closest('a, button, select, input, textarea, label')) {
        cursor.className = 'cursor is-link'; label.textContent = '';
      } else {
        cursor.className = 'cursor'; label.textContent = '';
      }
    });
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
    /* auto-sweep 20 → 80 → 50 teaches the interaction, once */
    var p = { v: 50 };
    sweep = gsap.timeline({ delay: 0.5, onUpdate: function () { setPos(p.v); } });
    sweep.to(p, { v: 20, duration: 0.7, ease: 'power2.inOut' })
         .to(p, { v: 80, duration: 1.0, ease: 'power2.inOut' })
         .to(p, { v: 50, duration: 0.7, ease: 'power2.inOut' });
  }

  if (preOn) runPreloader(heroIntro); else heroIntro();

  /* hero parallax on scroll away */
  if (hasGsap && !reduced) {
    gsap.to(scrub.children, {
      yPercent: 12, scale: 1.06, ease: 'none',
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
    });
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
    gsap.utils.toArray('.slabel, .practice__lead, .diff__head, .pricing__head, .faq__head, .contact__sub, .svcs__title').forEach(function (el) {
      gsap.from(el, { y: 40, opacity: 0, duration: 0.8, ease: 'expo.out',
        scrollTrigger: Object.assign({ trigger: el }, ST) });
    });

    /* practice principles + rules */
    gsap.from('.practice__col', { y: 40, opacity: 0, duration: 0.8, ease: 'expo.out', stagger: 0.12,
      scrollTrigger: Object.assign({ trigger: '.practice__cols' }, ST) });
    gsap.from('.practice__rule', { scaleY: 0, duration: 0.8, ease: 'expo.out',
      scrollTrigger: Object.assign({ trigger: '.practice__cols' }, ST) });

    /* RevealMedia — work scenes: clip-path opens upward, inner counter-scales */
    gsap.utils.toArray('[data-reveal-media]').forEach(function (el) {
      var tl = gsap.timeline({ scrollTrigger: Object.assign({ trigger: el }, ST) });
      tl.from(el, { clipPath: 'inset(0 0 100% 0)', duration: 1.1, ease: 'expo.inOut' }, 0)
        .from(el.children, { scale: 1.15, duration: 1.1, ease: 'expo.inOut' }, 0);
    });
    gsap.utils.toArray('.proj__info').forEach(function (el) {
      gsap.from(el.children, { y: 30, opacity: 0, duration: 0.7, ease: 'expo.out', stagger: 0.06,
        scrollTrigger: Object.assign({ trigger: el }, ST) });
    });

    /* contact heading line masks */
    gsap.from('.contact__head .mask__inner', { yPercent: 110, duration: 0.9, ease: 'expo.out', stagger: 0.06,
      scrollTrigger: Object.assign({ trigger: '.contact__head' }, ST) });
  }

  /* ── 06 · Services — horizontal pin ≥1280px ──────────────────────── */
  if (hasGsap) {
    var mm = gsap.matchMedia();
    mm.add('(min-width: 1280px) and (prefers-reduced-motion: no-preference)', function () {
      var sec = document.querySelector('.svcs');
      var track = document.getElementById('svcsTrack');
      var indexEl = document.getElementById('svcsIndex');
      sec.classList.add('is-pinned');
      var getDist = function () { return track.scrollWidth - document.querySelector('.svcs__viewport').clientWidth; };
      var tween = gsap.to(track, {
        x: function () { return -getDist(); },
        ease: 'none',
        scrollTrigger: {
          trigger: '.svcs__pin', pin: true, scrub: 0.6,
          end: function () { return '+=' + Math.max(getDist(), window.innerHeight * 3); },
          invalidateOnRefresh: true,
          onUpdate: function (self) {
            var i = Math.min(3, Math.floor(self.progress * 4));
            indexEl.textContent = '0' + (i + 1);
          }
        }
      });
      return function () { sec.classList.remove('is-pinned'); tween.scrollTrigger && tween.scrollTrigger.kill(); tween.kill(); };
    });
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

  /* ── 10 · Numbers — odometers ────────────────────────────────────── */
  if (hasGsap && !reduced) {
    document.querySelectorAll('.nums__val').forEach(function (el) {
      var target = parseInt(el.dataset.count, 10);
      var prefix = el.dataset.prefix || '';
      var suffix = el.dataset.suffix || '';
      var o = { v: 0 };
      gsap.to(o, {
        v: target, duration: 1.8, ease: 'power2.out', snap: { v: 1 },
        scrollTrigger: { trigger: el, start: 'top 75%', once: true },
        onUpdate: function () { el.textContent = prefix + o.v + suffix; }
      });
    });
  }

  /* ── 13 · FAQ accordion (single-open) ────────────────────────────── */
  (function () {
    var faq = document.querySelector('.faq');
    faq.classList.add('faq--js');
    var qs = faq.querySelectorAll('.faq__q');
    qs.forEach(function (q) {
      q.addEventListener('click', function () {
        var panel = document.getElementById(q.getAttribute('aria-controls'));
        var open = q.getAttribute('aria-expanded') === 'true';
        qs.forEach(function (other) {
          other.setAttribute('aria-expanded', 'false');
          document.getElementById(other.getAttribute('aria-controls')).classList.remove('is-open');
        });
        if (!open) { q.setAttribute('aria-expanded', 'true'); panel.classList.add('is-open'); }
      });
    });
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
      if (input.required && !input.value.trim()) ok = false;
      if (ok && input.type === 'email' && input.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value)) ok = false;
      if (ok && input.minLength > 0 && input.value.trim().length < input.minLength) ok = false;
      field.classList.toggle('is-error', !ok);
      var err = field.querySelector('.cform__err');
      if (err) err.setAttribute('aria-hidden', String(ok));
      return ok;
    }
    /* validate on blur, never on keystroke */
    form.querySelectorAll('input, textarea').forEach(function (input) {
      input.addEventListener('blur', function () { if (input.value) validateField(input); });
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
      var data = new FormData(form);
      var body = 'Name: ' + data.get('name') + '\nEmail: ' + data.get('email') +
        '\nCompany: ' + (data.get('company') || '—') + '\nNeed: ' + data.get('need') +
        '\nBudget: ' + data.get('budget') + '\n\n' + data.get('message');
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
