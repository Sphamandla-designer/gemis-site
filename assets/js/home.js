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
