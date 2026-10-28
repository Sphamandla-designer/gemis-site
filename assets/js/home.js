/* ──────────────────────────────────────────────────────────────────────
   Homepage motion: the tabbed stage (In their words), the video overlay,
   the Solutions panel and the case-study carousel.

   Everything works on markup that already reads correctly without this
   file. Under prefers-reduced-motion nothing advances on its own; every
   control still works, and changes are instant rather than animated.

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
    var list = frame.querySelector('[data-list]');
    var slides = [].slice.call(frame.querySelectorAll('[data-slide]'));
    var tabs = [].slice.call(frame.querySelectorAll('[data-tab]'));
    var ctl = frame.querySelector('[data-ctl]');
    var prev = frame.querySelector('[data-prev]');
    var next = frame.querySelector('[data-next]');
    var pause = frame.querySelector('[data-pause]');
    var cur = frame.querySelector('[data-cur]');
    var bar = frame.querySelector('[data-bar]');
    var auto = frame.getAttribute('data-auto') !== '0' && !reduced;
    var DWELL = 6000;
    if (slides.length < 2) return;

    var i = 0, timer = null, paused = false, hold = false;
    frame.classList.add('is-staged');
    if (ctl) ctl.hidden = false;

    function fit() {
      var h = 0;
      slides.forEach(function (s) { h = Math.max(h, s.offsetHeight); });
      if (h) list.style.minHeight = h + 'px';
    }

    function show(k) {
      i = (k + slides.length) % slides.length;
      slides.forEach(function (s, j) {
        var on = j === i;
        s.classList.toggle('is-current', on);
        s.setAttribute('aria-hidden', on ? 'false' : 'true');
        [].forEach.call(s.querySelectorAll('a, button, video, summary'), function (el) { el.tabIndex = on ? 0 : -1; });
      });
      tabs.forEach(function (t, j) { t.setAttribute('aria-pressed', j === i ? 'true' : 'false'); });
      if (cur) cur.textContent = String(i + 1).replace(/^(\d)$/, '0$1');
      restartBar();
    }

    function restartBar() {
      if (!bar) return;
      bar.classList.remove('is-running');
      void bar.offsetWidth;
      if (auto && !paused && !hold) bar.classList.add('is-running');
    }

    function schedule() {
      clearTimeout(timer);
      if (!auto || paused || hold) return;
      timer = setTimeout(function () { show(i + 1); schedule(); }, DWELL);
    }

    function setPaused(p) {
      paused = p;
      if (pause) {
        pause.setAttribute('aria-pressed', p ? 'true' : 'false');
        pause.setAttribute('aria-label', p ? 'Resume' : 'Pause');
      }
      restartBar();
      schedule();
    }

    tabs.forEach(function (t) {
      t.addEventListener('click', function () { show(parseInt(t.getAttribute('data-go'), 10) || 0); schedule(); });
    });
    if (prev) prev.addEventListener('click', function () { show(i - 1); schedule(); });
    if (next) next.addEventListener('click', function () { show(i + 1); schedule(); });
    if (pause) pause.addEventListener('click', function () { setPaused(!paused); });

    function holdOn() { hold = true; clearTimeout(timer); if (bar) bar.classList.remove('is-running'); }
    function holdOff() { if (!hold) return; hold = false; restartBar(); schedule(); }
    list.addEventListener('mouseenter', holdOn);
    list.addEventListener('mouseleave', holdOff);
    list.addEventListener('focusin', holdOn);
    list.addEventListener('focusout', function (e) { if (!list.contains(e.relatedTarget)) holdOff(); });
    slides.forEach(function (s) {
      [].forEach.call(s.querySelectorAll('video'), function (v) {
        v.addEventListener('play', holdOn);
        v.addEventListener('pause', holdOff);
        v.addEventListener('ended', holdOff);
      });
    });

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) { fit(); schedule(); } else { clearTimeout(timer); }
      }, { threshold: 0.2 }).observe(frame);
    } else {
      schedule();
    }
    if ('ResizeObserver' in window) {
      var ro = new ResizeObserver(function () { fit(); });
      slides.forEach(function (s) { ro.observe(s); });
    }
    window.addEventListener('load', fit);
    fit();
    show(0);
  }
  [].forEach.call(document.querySelectorAll('[data-stage]'), stage);

  /* ── the video overlay: "Play story" expands the video on screen ──────── */
  var modal = document.getElementById('videoModal');
  if (modal && typeof modal.showModal === 'function') {
    var mv = modal.querySelector('video');
    var mt = modal.querySelector('[data-vtitle]');

    function openVideo(btn) {
      var mp4 = btn.getAttribute('data-mp4'), webm = btn.getAttribute('data-webm');
      mv.innerHTML = '';
      if (webm) { var s1 = document.createElement('source'); s1.src = webm; s1.type = 'video/webm'; mv.appendChild(s1); }
      if (mp4) { var s2 = document.createElement('source'); s2.src = mp4; s2.type = 'video/mp4'; mv.appendChild(s2); }
      mv.poster = btn.getAttribute('data-poster') || '';
      if (mt) mt.textContent = btn.getAttribute('data-title') || '';
      mv.load();
      modal.showModal();
      var p = mv.play();
      if (p && p.catch) p.catch(function () { /* autoplay blocked: the controls are there */ });
    }
    function closeVideo() { mv.pause(); if (modal.open) modal.close(); }
    modal.addEventListener('close', function () {
      mv.pause();
      mv.removeAttribute('src');
      mv.innerHTML = '';
      mv.load();
    });
    document.addEventListener('click', function (e) {
      var w = e.target.closest('[data-watch]');
      if (w) { e.preventDefault(); openVideo(w); return; }
      if (e.target.closest('[data-close]')) closeVideo();
      if (e.target === modal) closeVideo();
    });
  }

  /* ── Solutions: the line under the pointer is the one in the card ──────
        [data-svc] holds the card ([data-svc-name], [data-svc-pic],
        [data-svc-line], [data-svc-link]) and the "+" list of links, each
        carrying data-svc-item (the slug), data-svc-name and data-svc-line.
        Hover or focus brings a line into the card; the links still navigate. */
  var svc = document.querySelector('[data-svc]');
  if (svc) {
    var items = [].slice.call(svc.querySelectorAll('[data-svc-item]'));
    var sName = svc.querySelector('[data-svc-name]');
    var sPic = svc.querySelector('[data-svc-pic]');
    var sLine = svc.querySelector('[data-svc-line]');
    var sLink = svc.querySelector('[data-svc-link]');
    var sUse = sPic && sPic.querySelector('use');
    var sTimer = null;

    function pick(el) {
      if (el.classList.contains('is-on')) return;
      items.forEach(function (it) { it.classList.toggle('is-on', it === el); });
      if (sPic) sPic.classList.add('is-swapping');
      clearTimeout(sTimer);
      sTimer = setTimeout(function () {
        if (sName) sName.textContent = el.getAttribute('data-svc-name') || '';
        if (sLine) sLine.textContent = el.getAttribute('data-svc-line') || '';
        if (sLink) sLink.href = el.href;
        if (sUse) sUse.setAttribute('href', '#px-' + el.getAttribute('data-svc-item'));
        if (sPic) sPic.classList.remove('is-swapping');
      }, reduced ? 0 : 160);
    }
    items.forEach(function (it) {
      it.addEventListener('mouseenter', function () { pick(it); });
      it.addEventListener('focus', function () { pick(it); });
    });
  }

  /* ── Case studies: the carousel's counter and circle controls ──────────
        [data-rail] holds a scroll-snapping [data-rail-track] of
        [data-rail-item]s. The buttons scroll by one tile; the counter follows
        the scroll position. Keyboard and touch scrolling already work. */
  var rail = document.querySelector('[data-rail]');
  if (rail) {
    var track = rail.querySelector('[data-rail-track]');
    var tiles = [].slice.call(rail.querySelectorAll('[data-rail-item]'));
    var rCur = rail.querySelector('[data-rail-cur]');
    var rPrev = rail.querySelector('[data-rail-prev]');
    var rNext = rail.querySelector('[data-rail-next]');
    var rTick = false;

    function step() { return tiles.length > 1 ? tiles[1].offsetLeft - tiles[0].offsetLeft : track.clientWidth; }
    function index() { return Math.min(tiles.length, Math.round(track.scrollLeft / step()) + 1); }
    function paint() {
      rTick = false;
      var k = index();
      if (rCur) rCur.textContent = String(k);
      var max = track.scrollWidth - track.clientWidth - 2;
      if (rPrev) rPrev.disabled = track.scrollLeft <= 2;
      if (rNext) rNext.disabled = track.scrollLeft >= max;
    }
    function go(dir) {
      track.scrollBy({ left: dir * step(), behavior: reduced ? 'auto' : 'smooth' });
    }
    if (rPrev) rPrev.addEventListener('click', function () { go(-1); });
    if (rNext) rNext.addEventListener('click', function () { go(1); });
    track.addEventListener('scroll', function () { if (!rTick) { rTick = true; requestAnimationFrame(paint); } });
    window.addEventListener('resize', paint);
    window.addEventListener('load', paint);
    paint();
  }
})();
