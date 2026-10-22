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
    function hsRun() {
      var top = hs.getBoundingClientRect().top;
      var p = total ? Math.min(1, Math.max(0, -top / span)) : 0;
      track.style.transform = 'translate3d(' + (-p * span) + 'px,0,0)';
    }
    hsSize(); hsRun();
    window.addEventListener('scroll', hsRun, { passive: true });
    window.addEventListener('resize', function () { hsSize(); hsRun(); });
    window.addEventListener('load', function () { hsSize(); hsRun(); });
    track.addEventListener('focusin', function (e) {
      var item = e.target.closest('.selw__card'); if (!item || !span) return;
      var x = Math.min(span, Math.max(0, item.offsetLeft - 48));
      var y = hs.getBoundingClientRect().top + window.scrollY + (x / span) * total;
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
    function suRun() {
      var r = su.getBoundingClientRect();
      var total = su.offsetHeight - window.innerHeight;
      if (total <= 0) return;
      var p = Math.min(1, Math.max(0, -r.top / total));
      var g = ease(Math.min(1, p / .6));                         // growth phase, then the hold
      su.style.setProperty('--s', (0.42 + 0.58 * g).toFixed(4));
      su.style.setProperty('--o', (0.35 + 0.65 * g).toFixed(4));
      su.style.setProperty('--l', (p > .5 ? Math.min(1, (p - .5) / .15) : 0).toFixed(3));
    }
    su.classList.add('is-scaling');
    suRun();
    window.addEventListener('scroll', suRun, { passive: true });
    window.addEventListener('resize', suRun);
    if (stmt) stmt.addEventListener('transitionend', suRun);
  }

  /* ── the operating logic: one line through the four principles, drawn on scroll ──
     The line's path is built from the real positions of the four index nodes
     (so it survives any width), drawn with a dash offset that follows the
     section's progress through the viewport. A principle becomes active when
     the line reaches its node, or on hover / focus; on touch screens scroll
     position alone decides. Under reduced motion the CSS shows everything
     resolved and this does nothing but build the path. */
  var op = document.querySelector('[data-oplogic]');
  if (op) {
    var opSvg = op.querySelector('[data-op-line]');
    var opBase = opSvg.querySelector('.op__line-base');
    var opDraw = opSvg.querySelector('.op__line-draw');
    var opItems = [].slice.call(op.querySelectorAll('[data-op]'));
    var opEnd = op.querySelector('.op__end-node');
    var opField = op.querySelector('.op__field');
    var fractions = [];          // where along the path each node sits, 0..1

    function opBuild() {
      var fr = opField.getBoundingClientRect();
      var pts = opItems.map(function (it) {
        var n = it.querySelector('[data-op-node]').getBoundingClientRect();
        return { x: n.left - fr.left + n.width / 2, y: n.top - fr.top + n.height / 2 };
      });
      var endR = opEnd.getBoundingClientRect();
      var end = { x: endR.left - fr.left + endR.width / 2, y: endR.top - fr.top - 4 };
      opSvg.setAttribute('viewBox', '0 0 ' + fr.width + ' ' + fr.height);
      opSvg.setAttribute('preserveAspectRatio', 'none');
      // an orthogonal route: 1 → 2 along the top, down the gutter and back to 3, across to 4, down to the end
      var segs = [], d = 'M' + pts[0].x + ' ' + pts[0].y, cur = pts[0], total = 0;
      function go(x, y) { total += Math.abs(x - cur.x) + Math.abs(y - cur.y); d += ' L' + x + ' ' + y; cur = { x: x, y: y }; }
      fractions = [0];
      if (window.matchMedia('(min-width: 901px)').matches) {
        go(pts[1].x, pts[0].y); go(pts[1].x, pts[1].y); fractions.push(total);
        var midY = (pts[1].y + pts[2].y) / 2 + Math.max(0, (pts[2].y - pts[1].y)) * 0.2;
        go(pts[1].x, midY); go(pts[2].x, midY); go(pts[2].x, pts[2].y); fractions.push(total);
        go(pts[3].x, pts[2].y); go(pts[3].x, pts[3].y); fractions.push(total);
        go(pts[3].x, end.y - 24); go(end.x, end.y - 24); go(end.x, end.y);
      } else {
        for (var i = 1; i < pts.length; i++) { go(pts[i].x, pts[i].y); fractions.push(total); }
        go(end.x, end.y);
      }
      fractions = fractions.map(function (f) { return total ? f / total : 0; });
      opBase.setAttribute('d', d); opDraw.setAttribute('d', d);
    }

    var opActive = -1, opHover = -1;
    function setActive(i) {
      opItems.forEach(function (it, j) { it.classList.toggle('is-active', j === i); });
    }
    function opRun() {
      var r = op.getBoundingClientRect(), vh = window.innerHeight;
      var fr = opField.getBoundingClientRect();
      // the line draws from when the field enters the lower third until its end passes the upper third
      var p = Math.min(1, Math.max(0, (vh * 0.72 - fr.top) / (fr.height + vh * 0.4)));
      op.style.setProperty('--p', p.toFixed(4));
      op.style.setProperty('--pe', Math.min(1, Math.max(0, (p - 0.86) / 0.14)).toFixed(3));
      // the principle whose node the line has reached most recently
      var k = -1;
      for (var i = 0; i < fractions.length; i++) if (p >= fractions[i] - 0.02) k = i;
      if (p <= 0 || r.bottom < 0 || r.top > vh) k = -1;
      opActive = k;
      if (opHover < 0) setActive(opActive);
    }
    opItems.forEach(function (it, i) {
      it.addEventListener('mouseenter', function () { opHover = i; setActive(i); });
      it.addEventListener('mouseleave', function () { opHover = -1; setActive(opActive); });
      it.addEventListener('focusin', function () { opHover = i; setActive(i); });
      it.addEventListener('focusout', function (e) { if (!it.contains(e.relatedTarget)) { opHover = -1; setActive(opActive); } });
    });
    opBuild();
    if (reduced) {
      op.style.setProperty('--p', '1'); op.style.setProperty('--pe', '1');
    } else {
      var opOn = false, opTick = false;
      function opFrame() { opTick = false; opRun(); }
      function opScroll() { if (opOn && !opTick) { opTick = true; requestAnimationFrame(opFrame); } }
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (en) { opOn = en[0].isIntersecting; if (opOn) opRun(); }, { rootMargin: '20% 0px 20% 0px' }).observe(op);
      } else { opOn = true; }
      window.addEventListener('scroll', opScroll, { passive: true });
      opRun();
    }
    window.addEventListener('resize', function () { opBuild(); if (!reduced) opRun(); });
    window.addEventListener('load', function () { opBuild(); if (!reduced) opRun(); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { opBuild(); if (!reduced) opRun(); });
    if ('ResizeObserver' in window) new ResizeObserver(function () { opBuild(); if (!reduced) opRun(); }).observe(opField);
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
