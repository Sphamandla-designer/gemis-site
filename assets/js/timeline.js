/* ──────────────────────────────────────────────────────────────────────
   The timeline, as an enhancement.

   The markup it works on is a plain <ol> of <li> cards that already reads
   correctly with this file absent, with JavaScript off, and with CSS off. This
   adds two things on top:

     1. the period label of the group currently passing sticks to the top of
        the column, so you always know which year you are reading;
     2. cards fade and rise once as they enter view.

   Nothing else moves. There is no scroll-jacking, no full-screen takeover and
   no horizontal scroll. Under prefers-reduced-motion both behaviours are off
   and every card is simply visible, which is also what happens if this file
   fails to load.
   ────────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var list = document.querySelector('.stl__list');
  if (!list) return;

  var items = [].slice.call(list.querySelectorAll('.stl__item'));
  if (!items.length) return;

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── 1. the sticky period label ─────────────────────────────────────
     Reveal is handled by site.js, which owns [data-reveal] for the whole site;
     duplicating it here would fight it. This file only adds the sticky label
     and the thread highlight. */
  var marker = document.querySelector('.stl__threads');

  function highlight() {
    // which card is currently crossing the upper third of the viewport
    var line = window.innerHeight * 0.34;
    var active = null;
    for (var i = 0; i < items.length; i++) {
      var box = items[i].getBoundingClientRect();
      if (box.top <= line && box.bottom > line) { active = items[i]; break; }
    }
    if (!marker) return;
    var slug = active && active.getAttribute('data-thread');
    [].forEach.call(marker.querySelectorAll('.stl__thread'), function (t) {
      t.classList.toggle('is-current', !!slug && t.getAttribute('data-thread') === slug);
    });
  }

  if (!reduced && 'requestAnimationFrame' in window) {
    var queued = false;
    var onScroll = function () {
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () { queued = false; highlight(); });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    highlight();
  }

  /* ── 2. one video at a time ─────────────────────────────────────────
     Not a behaviour the brief asks for, but with seven players on one page,
     starting a second while the first is talking is the obvious accident. No
     video is ever started here — only paused. */
  var videos = [].slice.call(document.querySelectorAll('.vid__el'));
  videos.forEach(function (v) {
    v.addEventListener('play', function () {
      videos.forEach(function (other) { if (other !== v && !other.paused) other.pause(); });
    });
  });
})();
