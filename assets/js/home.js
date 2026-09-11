/* GEMIS home page — nav state, scroll reveals, stat counters, contact hand-off.
   No dependencies; every effect degrades to a fully readable static page. */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── header: transparent over the hero, solid once past it ───────────── */
  var nav = document.getElementById('nav');
  var hero = document.getElementById('hero');

  if (nav && hero) {
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        nav.classList.toggle('is-stuck', !entries[0].isIntersecting);
      }, { rootMargin: '-72px 0px 0px 0px', threshold: 0 })
        .observe(hero);
    } else {
      nav.classList.add('is-stuck');
    }
  }

  /* ── mobile menu ─────────────────────────────────────────────────────── */
  var burger = document.getElementById('navBurger');
  var links = document.getElementById('navLinks');

  function closeMenu() {
    if (!nav) return;
    nav.classList.remove('is-open');
    if (burger) burger.setAttribute('aria-expanded', 'false');
  }

  if (burger && nav && links) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeMenu();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
  }

  /* ── scroll reveals + stat counters ─────────────────────────────────
        One rAF-throttled sweep drives both. A scroll position check is
        deterministic where IntersectionObserver can drop entries during fast
        or programmatic scrolling — nothing is ever left stuck at opacity 0. */

  var revealables = [].slice.call(document.querySelectorAll('[data-reveal]'));
  var counters = [].slice.call(document.querySelectorAll('[data-count]'));

  function paint(el, value) {
    var sup = el.getAttribute('data-sup');
    el.textContent = String(value);
    if (sup) {
      var s = document.createElement('sup');
      s.textContent = sup;
      el.appendChild(s);
    }
  }

  function count(el) {
    var target = parseInt(el.getAttribute('data-count'), 10) || 0;
    if (reduced) { paint(el, target); return; }

    var duration = 1400;
    var start = null;

    function step(now) {
      if (start === null) start = now;
      var t = Math.min((now - start) / duration, 1);
      paint(el, Math.round(target * (1 - Math.pow(1 - t, 3))));
      if (t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function showAll() {
    revealables.forEach(function (el) { el.classList.add('is-in'); });
    counters.forEach(function (el) { paint(el, parseInt(el.getAttribute('data-count'), 10) || 0); });
    revealables = [];
    counters = [];
  }

  if (reduced) {
    showAll();
  } else {
    var queued = false;

    var sweep = function () {
      queued = false;
      var limit = window.innerHeight * 0.92;

      revealables = revealables.filter(function (el) {
        if (el.getBoundingClientRect().top > limit) return true;
        el.classList.add('is-in');
        return false;
      });

      counters = counters.filter(function (el) {
        if (el.getBoundingClientRect().top > window.innerHeight * 0.85) return true;
        count(el);
        return false;
      });
    };

    var schedule = function () {
      if (queued) return;
      queued = true;
      requestAnimationFrame(sweep);
    };

    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', schedule);
    window.addEventListener('load', schedule);
    sweep();
  }

  /* ── contact form → email hand-off (the site is static, so there is no
        endpoint to post to; we open a pre-addressed message instead) ────── */
  var form = document.getElementById('ctaForm');

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var field = document.getElementById('ctaEmail');
      var address = field && field.value ? field.value.trim() : '';
      if (field && !field.checkValidity()) { field.reportValidity(); return; }

      var body = 'Hi GEMIS team,\n\nI\'d like to talk about a project.\n\n'
               + 'You can reach me at: ' + address + '\n\n'
               + 'A little about what we need:\n';

      window.location.href = 'mailto:info@gemis.co.za'
        + '?subject=' + encodeURIComponent('Project enquiry via gemis.co.za')
        + '&body=' + encodeURIComponent(body);
    });
  }
})();
