/* ──────────────────────────────────────────────────────────────────────
   Homepage motion: the stories slider and the testimonials slider.

   Both work on markup that already reads correctly without this file: the
   stories are a plain <ol> of cards, the testimonials a plain <ul>. This adds
   the stage, the auto-advance and the controls over the top. The logo marquee
   is CSS only. Under prefers-reduced-motion nothing advances on its own;
   every control still works, and changes are instant rather than animated.
   ────────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── stories: one card at a time, sliding vertically ─────────────────── */
  var frame = document.querySelector('[data-stories]');
  if (frame) {
    var slides = [].slice.call(frame.querySelectorAll('.sty'));
    var tabs = [].slice.call(frame.querySelectorAll('.stories__tab'));
    var ctl = frame.querySelector('.stories__ctl');
    var bar = frame.querySelector('.stories__bar');
    var cur = frame.querySelector('[data-cur]');
    var stage = frame.querySelector('.stories__stage');
    var n = slides.length, i = 0, timer = null, paused = false;
    var DWELL = 7000;

    frame.classList.add('stories--live');
    if (ctl) ctl.hidden = false;

    function fit() {
      // the stage is as tall as its tallest card, so the layout never jumps
      var h = 0;
      slides.forEach(function (s) { h = Math.max(h, s.offsetHeight); });
      stage.style.setProperty('--stage-h', h + 'px');
    }

    function show(k, dir) {
      k = (k + n) % n;
      slides.forEach(function (s, j) {
        s.classList.remove('is-active', 'is-above', 'is-below');
        if (j === k) s.classList.add('is-active');
        else s.classList.add(j < k ? 'is-above' : 'is-below');
        s.setAttribute('aria-hidden', j === k ? 'false' : 'true');
        [].forEach.call(s.querySelectorAll('a'), function (a) { a.tabIndex = j === k ? 0 : -1; });
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
      if (!reduced && !paused) bar.classList.add('is-running');
    }

    function schedule() {
      clearTimeout(timer);
      if (reduced || paused || document.documentElement.classList.contains('has-modal')) return;
      timer = setTimeout(function () { show(i + 1, 1); schedule(); }, DWELL);
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
    if (prev) prev.addEventListener('click', function () { show(i - 1, -1); schedule(); });
    if (next) next.addEventListener('click', function () { show(i + 1, 1); schedule(); });
    if (pause) pause.addEventListener('click', function () { setPaused(!paused); });

    // a pointer over the stage, or focus inside it, holds the current story
    var hold = false;
    function holdOn() { hold = true; clearTimeout(timer); if (bar) bar.classList.remove('is-running'); }
    function holdOff() { if (!hold) return; hold = false; restartBar(); schedule(); }
    stage.addEventListener('mouseenter', holdOn);
    stage.addEventListener('mouseleave', holdOff);
    stage.addEventListener('focusin', holdOn);
    stage.addEventListener('focusout', function (e) { if (!stage.contains(e.relatedTarget)) holdOff(); });

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
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
    show(0, 1);
    if (reduced) setPaused(true);
  }

  /* ── the video overlay: "Watch the story" expands the video on screen ── */
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
    function closeVideo() {
      mv.pause();
      if (modal.open) modal.close();
    }
    modal.addEventListener('close', function () {
      mv.pause();
      mv.removeAttribute('src');
      while (mv.firstChild) mv.removeChild(mv.firstChild);
      document.documentElement.classList.remove('has-modal');
      if (opener) opener.focus();
    });
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-watch]');
      if (btn) { e.preventDefault(); openVideo(btn); return; }
      if (e.target.closest('[data-close]')) { closeVideo(); return; }
      // a click on the backdrop (outside the video) closes it
      if (modal.open && e.target === modal) closeVideo();
    });
  }

  /* ── testimonials: a snapping track that advances on its own ─────────── */
  var track = document.querySelector('[data-testi]');
  if (track) {
    var cards = [].slice.call(track.children);
    var dots = document.querySelector('[data-testi-dots]');
    var t = 0, ttimer = null, thold = false;

    function cardWidth() { return cards[0].getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap || 0); }
    function perView() { return Math.max(1, Math.round(track.clientWidth / cardWidth())); }
    function pages() { return Math.max(1, Math.ceil(cards.length / perView())); }

    function paintDots() {
      if (!dots) return;
      dots.innerHTML = '';
      for (var k = 0; k < pages(); k++) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'testi__dot';
        b.setAttribute('aria-label', 'Show testimonials ' + (k * perView() + 1) + ' to ' + Math.min(cards.length, (k + 1) * perView()));
        b.setAttribute('aria-pressed', k === t ? 'true' : 'false');
        (function (k) { b.addEventListener('click', function () { go(k); tschedule(); }); })(k);
        dots.appendChild(b);
      }
    }

    function go(k) {
      t = (k + pages()) % pages();
      track.scrollTo({ left: t * perView() * cardWidth(), behavior: reduced ? 'auto' : 'smooth' });
      if (dots) [].forEach.call(dots.children, function (d, j) { d.setAttribute('aria-pressed', j === t ? 'true' : 'false'); });
    }

    function tschedule() {
      clearTimeout(ttimer);
      if (reduced || thold) return;
      ttimer = setTimeout(function () { go(t + 1); tschedule(); }, 6000);
    }

    track.addEventListener('mouseenter', function () { thold = true; clearTimeout(ttimer); });
    track.addEventListener('mouseleave', function () { thold = false; tschedule(); });
    track.addEventListener('focusin', function () { thold = true; clearTimeout(ttimer); });
    track.addEventListener('focusout', function (e) { if (!track.contains(e.relatedTarget)) { thold = false; tschedule(); } });
    // a manual scroll (touch) updates the dots and holds the timer briefly
    var sdeb = null;
    track.addEventListener('scroll', function () {
      clearTimeout(sdeb);
      sdeb = setTimeout(function () {
        var k = Math.round(track.scrollLeft / (perView() * cardWidth()));
        if (k !== t && dots) { t = k; [].forEach.call(dots.children, function (d, j) { d.setAttribute('aria-pressed', j === t ? 'true' : 'false'); }); }
      }, 120);
    }, { passive: true });
    window.addEventListener('resize', function () { paintDots(); go(Math.min(t, pages() - 1)); });

    var prevT = document.querySelector('[data-testi-prev]'), nextT = document.querySelector('[data-testi-next]');
    if (prevT) prevT.addEventListener('click', function () { go(t - 1); tschedule(); });
    if (nextT) nextT.addEventListener('click', function () { go(t + 1); tschedule(); });

    paintDots();
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) tschedule(); else clearTimeout(ttimer);
      }, { threshold: 0.25 }).observe(track);
    } else {
      tschedule();
    }
  }
})();
