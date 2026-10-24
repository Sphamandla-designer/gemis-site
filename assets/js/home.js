/* ──────────────────────────────────────────────────────────────────────
   Homepage motion: the tabbed stages (the stories panel and the client
   stories) and the horizontal timeline.

   Every stage works on markup that already reads correctly without this
   file: a plain <ol> of cards. This adds the one-at-a-time stage, the tabs,
   the optional auto-advance and the controls over the top. The logo marquee
   is CSS only. Under prefers-reduced-motion nothing advances on its own;
   every control still works, and changes are instant rather than animated.

   A stage is any [data-stage] element holding:
     [data-list]   the <ol> of cards        [data-slide]  each card
     [data-tab]    a button per card, with data-go="<index>"
     [data-ctl]    optional controls: [data-prev] [data-next] [data-pause]
                   [data-cur] (the current number) [data-bar] (a progress bar)
     data-auto="0" turns the auto-advance off (the client stories)
   ────────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function stage(frame) {
    var slides = [].slice.call(frame.querySelectorAll('[data-slide]'));
    var tabs = [].slice.call(frame.querySelectorAll('[data-tab]'));
    var list = frame.querySelector('[data-list]');
    var ctl = frame.querySelector('[data-ctl]');
    var bar = frame.querySelector('[data-bar]');
    var cur = frame.querySelector('[data-cur]');
    var auto = frame.getAttribute('data-auto') !== '0';
    var n = slides.length, i = 0, timer = null, paused = !auto, hold = false;
    var DWELL = parseInt(frame.getAttribute('data-dwell'), 10) || 7000;
    if (!n || !list) return;

    frame.classList.add('is-live');
    if (ctl) ctl.hidden = false;

    function fit() {
      // the list is as tall as its tallest card, so the layout never jumps
      var h = 0;
      slides.forEach(function (s) { h = Math.max(h, s.offsetHeight); });
      list.style.setProperty('--stage-h', h + 'px');
    }

    function show(k) {
      k = (k + n) % n;
      slides.forEach(function (s, j) {
        var v = s.querySelector('video');
        if (v && !v.paused) v.pause();
        s.classList.remove('is-active', 'is-above', 'is-below');
        s.classList.add(j === k ? 'is-active' : (j < k ? 'is-above' : 'is-below'));
        s.setAttribute('aria-hidden', j === k ? 'false' : 'true');
        [].forEach.call(s.querySelectorAll('a, button, video, summary'), function (el) { el.tabIndex = j === k ? 0 : -1; });
      });
      tabs.forEach(function (t, j) { t.setAttribute('aria-pressed', j === k ? 'true' : 'false'); });
      if (cur) cur.textContent = String(k + 1);
      i = k;
      restartBar();
    }

    function restartBar() {
      if (!bar) return;
      bar.classList.remove('is-running');
      void bar.offsetWidth;   // restart the CSS animation
      if (!reduced && !paused && !hold) bar.classList.add('is-running');
    }

    function schedule() {
      clearTimeout(timer);
      if (reduced || paused || hold || !auto) return;
      timer = setTimeout(function () { show(i + 1); schedule(); }, DWELL);
    }

    function setPaused(p) {
      paused = p;
      var b = frame.querySelector('[data-pause]');
      if (b) {
        b.setAttribute('aria-pressed', p ? 'true' : 'false');
        b.setAttribute('aria-label', p ? 'Play' : 'Pause');
        b.classList.toggle('is-paused', p);
      }
      restartBar();
      schedule();
    }

    tabs.forEach(function (t) {
      t.addEventListener('click', function () { show(parseInt(t.getAttribute('data-go'), 10) || 0); schedule(); });
    });
    var prev = frame.querySelector('[data-prev]'), next = frame.querySelector('[data-next]'), pause = frame.querySelector('[data-pause]');
    if (prev) prev.addEventListener('click', function () { show(i - 1); schedule(); });
    if (next) next.addEventListener('click', function () { show(i + 1); schedule(); });
    if (pause) pause.addEventListener('click', function () { setPaused(!paused); });

    // a pointer over the cards, focus inside them, or a playing video holds the current one
    function holdOn() { hold = true; clearTimeout(timer); if (bar) bar.classList.remove('is-running'); }
    function holdOff() { if (!hold) return; hold = false; restartBar(); schedule(); }
    list.addEventListener('mouseenter', holdOn);
    list.addEventListener('mouseleave', holdOff);
    list.addEventListener('focusin', holdOn);
    list.addEventListener('focusout', function (e) { if (!list.contains(e.relatedTarget)) holdOff(); });
    slides.forEach(function (s) {
      var v = s.querySelector('video');
      if (!v) return;
      v.addEventListener('play', holdOn);
      v.addEventListener('pause', holdOff);
      v.addEventListener('ended', holdOff);
    });

    // only run while on screen
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) { if (!hold) { restartBar(); schedule(); } }
        else { clearTimeout(timer); if (bar) bar.classList.remove('is-running'); }
      }, { threshold: 0.25 }).observe(frame);
    } else {
      schedule();
    }

    fit();
    window.addEventListener('resize', fit);
    window.addEventListener('load', fit);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
    if ('ResizeObserver' in window) {
      var ro = new ResizeObserver(function () { fit(); });
      slides.forEach(function (s) { ro.observe(s); });
    }
    show(0);
    if (reduced && auto) setPaused(true);
  }

  [].forEach.call(document.querySelectorAll('[data-stage]'), stage);

  /* ── the video overlay: "Play story" expands the video on screen ──────── */
  var modal = document.getElementById('videoModal');
  if (modal && typeof modal.showModal === 'function') {
    var mv = modal.querySelector('.vmodal__video');
    var mt = modal.querySelector('[data-vtitle]');
    var opener = null;
    function openVideo(btn) {
      opener = btn;
      while (mv.firstChild) mv.removeChild(mv.firstChild);
      var webm = document.createElement('source'); webm.src = btn.getAttribute('data-webm'); webm.type = 'video/webm';
      var mp4 = document.createElement('source'); mp4.src = btn.getAttribute('data-mp4'); mp4.type = 'video/mp4';
      mv.appendChild(webm); mv.appendChild(mp4);
      mv.poster = btn.getAttribute('data-poster') || '';
      mv.setAttribute('aria-label', btn.getAttribute('data-title') || 'Case study video');
      if (mt) mt.textContent = btn.getAttribute('data-title') || '';
      mv.load();
      modal.showModal();
      document.documentElement.classList.add('has-modal');
      var p = mv.play();
      if (p && p.catch) p.catch(function () { /* autoplay blocked: the controls are there */ });
    }
    function closeVideo() { mv.pause(); if (modal.open) modal.close(); }
    modal.addEventListener('close', function () {
      mv.pause();
      while (mv.firstChild) mv.removeChild(mv.firstChild);
      document.documentElement.classList.remove('has-modal');
      if (opener) opener.focus();
    });
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-watch]');
      if (btn) { e.preventDefault(); openVideo(btn); return; }
      if (e.target.closest('[data-close]')) { closeVideo(); return; }
      if (modal.open && e.target === modal) closeVideo();
    });
  }

  /* ── selected work: the band pins and the cards travel across as the page scrolls ──
     Wide screens only, and never under reduced motion; otherwise the list stays
     vertical. Focus inside the track scrolls the page to bring the card on. */
  var hs = document.querySelector('[data-hscroll]');
  if (hs && !reduced && window.matchMedia('(min-width: 901px)').matches) {
    var track = hs.querySelector('[data-track]');
    var span = 0, total = 0;
    function hsSize() {
      hs.classList.add('is-pinned');
      span = Math.max(0, track.scrollWidth - window.innerWidth);
      total = span + Math.round(window.innerHeight * .25);   // one px of travel per px of scroll, then a short rest
      hs.style.height = (window.innerHeight + total) + 'px';
    }
    /* The travel follows the scroll with inertia: each frame the track closes a
       fraction of the distance to where the scroll says it should be, so a
       flick glides to rest instead of stopping dead, and a slow scroll feels
       weighted. The loop only runs while there is distance left to close. */
    var hsTarget = 0, hsNow = 0, hsTick = false, hsSnap = true;
    var cards = track.querySelectorAll('.selw__card');
    function hsPaint() {
      track.style.transform = 'translate3d(' + (-hsNow) + 'px,0,0)';
      // the cards lean into the direction of travel while moving, and settle upright
      var v = Math.max(-1, Math.min(1, (hsTarget - hsNow) / 400));
      hs.style.setProperty('--hs-v', v.toFixed(3));
      var vw = window.innerWidth;
      for (var i = 0; i < cards.length; i++) {
        var c = cards[i], cx = c.offsetLeft - hsNow + c.offsetWidth / 2;
        var d = Math.max(-1, Math.min(1, (cx - vw / 2) / vw));     // -1 left edge … 1 right edge
        c.style.setProperty('--hs-d', d.toFixed(3));
      }
    }
    function hsFrame() {
      var diff = hsTarget - hsNow;
      if (Math.abs(diff) < 0.3 || hsSnap) { hsNow = hsTarget; hsSnap = false; hsPaint(); hsTick = false; return; }
      hsNow += diff * 0.11;
      hsPaint();
      requestAnimationFrame(hsFrame);
    }
    function hsRun() {
      var top = hs.getBoundingClientRect().top;
      var p = total ? Math.min(1, Math.max(0, -top / span)) : 0;
      hsTarget = p * span;
      if (!hsTick) { hsTick = true; requestAnimationFrame(hsFrame); }
    }
    hsSize(); hsRun();
    window.addEventListener('scroll', hsRun, { passive: true });
    window.addEventListener('resize', function () { hsSize(); hsSnap = true; hsRun(); });
    window.addEventListener('load', function () { hsSize(); hsSnap = true; hsRun(); });
    track.addEventListener('focusin', function (e) {
      var item = e.target.closest('.selw__card'); if (!item || !span) return;
      var x = Math.min(span, Math.max(0, item.offsetLeft - 48));
      var y = hs.getBoundingClientRect().top + window.scrollY + (x / span) * total;
      hsSnap = true;                                              // keyboard focus lands at once
      window.scrollTo({ top: y, behavior: 'auto' });
    });
  }

  /* ── the transition statement: scales up as it is scrolled to the centre, holds, releases ──
     Scroll-linked, no library. The pin is a sticky block inside a tall wrapper;
     the statement's scale and opacity follow the wrapper's progress through
     the viewport: the first 60 % grows, the rest holds at full size, then the
     sticky block releases with the page. Under reduced motion the block is static. */
  var su = document.querySelector('[data-scaleup]');
  if (su && !reduced) {
    var stmt = su.querySelector('.selw__statement');
    var ease = function (t) { return 1 - Math.pow(1 - t, 3); };   // ease-out cubic
    var suPin = su.querySelector('.selw__out-pin');
    function suSize() { su.style.setProperty('--pinh', suPin.offsetHeight + 'px'); }
    var suTarget = 0, suNow = 0, suTick = false, suSnap = true;
    function suPaint() {
      var g = ease(Math.min(1, suNow / .6));                     // growth phase, then the hold
      su.style.setProperty('--s', (0.42 + 0.58 * g).toFixed(4));
      su.style.setProperty('--o', (0.6 + 0.4 * g).toFixed(4));   // never below 3:1 for large text
      su.style.setProperty('--l', (suNow > .5 ? Math.min(1, (suNow - .5) / .15) : 0).toFixed(3));
    }
    function suFrame() {
      var diff = suTarget - suNow;
      if (Math.abs(diff) < 0.001 || suSnap) { suNow = suTarget; suSnap = false; suPaint(); suTick = false; return; }
      suNow += diff * 0.14;
      suPaint();
      requestAnimationFrame(suFrame);
    }
    function suRun() {
      var r = su.getBoundingClientRect();
      // the pin holds the statement at the centre; the travel is the wrapper
      // beyond half a viewport, so the hold ends as the pin releases
      var total = su.offsetHeight - window.innerHeight * 0.5;
      if (total <= 0) return;
      suTarget = Math.min(1, Math.max(0, -r.top / total));
      if (!suTick) { suTick = true; requestAnimationFrame(suFrame); }
    }
    su.classList.add('is-scaling');
    suSize(); suRun();
    window.addEventListener('scroll', suRun, { passive: true });
    window.addEventListener('resize', function () { suSize(); suRun(); });
    window.addEventListener('load', function () { suSize(); suRun(); });
    if (stmt) stmt.addEventListener('transitionend', suRun);
  }

  /* ── operating principles: the row at the reading line is the live one ──
     The index numeral and the ticks on the sticky side follow the row whose
     box crosses a line 42 % down the viewport (the nearest row otherwise).
     Wide screens only; elsewhere, and without scripts, every row is full. */
  var prin = document.querySelector('[data-principles]');
  if (prin && window.matchMedia('(min-width: 1001px)').matches) {
    var pRows = [].slice.call(prin.querySelectorAll('[data-prin-row]'));
    var pNums = [].slice.call(prin.querySelectorAll('[data-prin-num]'));
    var pTicks = [].slice.call(prin.querySelectorAll('[data-prin-tick]'));
    var pCur = 0, pTick = false, pOn = false;
    function pSet(i) {
      if (i === pCur) return;
      pRows[pCur].classList.remove('is-active'); pNums[pCur].classList.remove('is-on'); pTicks[pCur].classList.remove('is-on');
      pCur = i;
      pRows[i].classList.add('is-active'); pNums[i].classList.add('is-on'); pTicks[i].classList.add('is-on');
    }
    function pFrame() {
      pTick = false;
      var line = window.innerHeight * 0.42, best = 0, bestD = Infinity;
      for (var i = 0; i < pRows.length; i++) {
        var r = pRows[i].getBoundingClientRect();
        if (r.top <= line && r.bottom > line) { best = i; bestD = 0; break; }
        var d = r.top > line ? r.top - line : line - r.bottom;
        if (d < bestD) { bestD = d; best = i; }
      }
      pSet(best);
    }
    function pScroll() { if (pOn && !pTick) { pTick = true; requestAnimationFrame(pFrame); } }
    prin.classList.add('is-live');
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { pOn = es[0].isIntersecting; if (pOn) pScroll(); }, { rootMargin: '20% 0px 20% 0px' }).observe(prin);
    } else { pOn = true; }
    window.addEventListener('scroll', pScroll, { passive: true });
    window.addEventListener('resize', pScroll);
    pFrame();
  }

  /* ── the horizontal timeline: draws its line and lands its steps in turn ── */
  var lines = [].slice.call(document.querySelectorAll('.tline'));
  if (lines.length) {
    var land = function (el) { el.classList.add('is-drawn'); };
    if (reduced || !('IntersectionObserver' in window)) {
      lines.forEach(land);
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { land(en.target); io.unobserve(en.target); } });
      }, { threshold: 0.3 });
      lines.forEach(function (el) { io.observe(el); });
    }
  }
})();
