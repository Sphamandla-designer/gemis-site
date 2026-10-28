/* GEMIS corporate site — nav state, drop-downs, scroll reveals, stat counters, contact hand-off.
   No dependencies; every effect degrades to a fully readable static page. */
(function () {
  'use strict';
  document.documentElement.classList.add('has-js');
  // the home page runs edge to edge, so its bar does too
  if (document.querySelector('.hx-hero')) document.documentElement.classList.add('is-home');

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
  var links = document.getElementById('navDrawer');

  function closeMenu() {
    if (!nav) return;
    nav.classList.remove('is-open');
    if (burger) burger.setAttribute('aria-expanded', 'false');
    [].forEach.call(document.querySelectorAll('[data-mega]'), function (item) {
      var trigger = item.querySelector('.nav__trigger');
      var panel = item.querySelector('.mega');
      if (panel) panel.classList.remove('is-open');
      if (trigger) trigger.setAttribute('aria-expanded', 'false');
      item.removeAttribute('data-open');
    });
    nav.classList.remove('is-mega');
  }

  if (burger && nav && links) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeMenu();   // real navigation only
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
  }

  /* ── drop-down menus (Solutions, Products) ──────────────────────────
        Each [data-mega] item carries its own trigger and panel. Hover opens
        it on pointer devices (with a close delay so the cursor can travel
        diagonally into the panel); click and keyboard drive it everywhere,
        which is also the whole story on touch and inside the mobile burger
        panel. Opening one closes the other. */

  var megas = [].slice.call(document.querySelectorAll('[data-mega]')).map(function (item) {
    return { item: item, trigger: item.querySelector('.nav__trigger'), panel: item.querySelector('.mega'), open: false, timer: null };
  }).filter(function (m) { return m.trigger && m.panel; });

  if (megas.length && nav) {
    var anyOpen = function () { return megas.some(function (m) { return m.open; }); };
    var setMega = function (m, open) {
      m.open = open;
      m.panel.classList.toggle('is-open', open);
      m.item.toggleAttribute('data-open', open);
      m.trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
      // the panel is light, so the header has to leave its transparent state
      nav.classList.toggle('is-mega', anyOpen());
    };
    var closeAll = function () { megas.forEach(function (m) { clearTimeout(m.timer); if (m.open) setMega(m, false); }); };
    var openMega = function (m) {
      clearTimeout(m.timer);
      megas.forEach(function (o) { if (o !== m && o.open) setMega(o, false); });
      if (!m.open) setMega(m, true);
    };
    var closeMega = function (m) { clearTimeout(m.timer); m.byHover = false; if (m.open) setMega(m, false); };
    var suppressFocusOpen = false;

    megas.forEach(function (m) {
      // A click on a panel the hover already opened keeps it open (the visitor
      // is confirming, not dismissing); it only closes a panel the click opened.
      m.trigger.addEventListener('click', function (e) {
        e.preventDefault();
        if (m.open && m.byHover) { m.byHover = false; return; }
        m.open ? closeMega(m) : openMega(m);
      });

      // hover only where a real pointer exists; touch would fire it on every tap
      if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
        [m.item, m.panel].forEach(function (el) {
          el.addEventListener('mouseenter', function () { if (!m.open) m.byHover = true; openMega(m); });
          el.addEventListener('mouseleave', function () {
            clearTimeout(m.timer);
            m.timer = setTimeout(function () { closeMega(m); }, 220);
          });
        });
      }

      // Keyboard opens it on focus, but only for keyboard focus: a mouse or touch
      // press focuses the button first and would otherwise open the panel just in
      // time for the click handler to toggle it straight back shut.
      m.trigger.addEventListener('focus', function () {
        if (suppressFocusOpen) { suppressFocusOpen = false; return; }
        var keyboard = true;
        try { keyboard = m.trigger.matches(':focus-visible'); } catch (err) { /* older engines */ }
        if (keyboard) openMega(m);
      });
    });

    var inside = function (target) {
      return megas.some(function (m) { return m.open && (m.item.contains(target) || m.panel.contains(target)); });
    };
    document.addEventListener('focusin', function (e) { if (anyOpen() && !inside(e.target)) closeAll(); });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || !anyOpen()) return;
      var open = megas.filter(function (m) { return m.open; })[0];
      closeAll(); suppressFocusOpen = true; open.trigger.focus();
    });
    // a click anywhere else, or any scroll, dismisses it
    document.addEventListener('click', function (e) { if (anyOpen() && !inside(e.target)) closeAll(); });
    window.addEventListener('scroll', function () {
      if (anyOpen() && !nav.classList.contains('is-open')) closeAll();
    }, { passive: true });
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

  /* The real figure is in the markup, so it is what a reader without
     JavaScript — or with reduced motion — sees. Only when we are actually
     going to animate do we reset to zero, and that happens before first
     paint because this script is deferred and the stats sit below the fold. */
  if (!reduced) counters.forEach(function (el) { paint(el, 0); });

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

  /* ── services accordion ──────────────────────────────────────────────
        Rows are real <button>s inside the list, so keyboard and screen-reader
        behaviour comes for free; the panel animates on grid-template-rows,
        which works without measuring heights. */

  var accItems = [].slice.call(document.querySelectorAll('.acc__item'));

  accItems.forEach(function (item) {
    var btn = item.querySelector('.acc__btn');
    var panel = item.querySelector('.acc__panel');
    if (!btn || !panel) return;
    if ('inert' in panel && !item.hasAttribute('data-open')) panel.inert = true;

    btn.addEventListener('click', function () {
      var open = item.hasAttribute('data-open');
      if (open) {
        item.removeAttribute('data-open');
      } else {
        // one open at a time keeps the list scannable
        accItems.forEach(function (other) {
          if (other === item) return;
          other.removeAttribute('data-open');
          var b = other.querySelector('.acc__btn');
          var pnl = other.querySelector('.acc__panel');
          if (b) b.setAttribute('aria-expanded', 'false');
          if (pnl) { pnl.setAttribute('aria-hidden', 'true'); if ('inert' in pnl) pnl.inert = true; }
        });
        item.setAttribute('data-open', '');
      }
      btn.setAttribute('aria-expanded', open ? 'false' : 'true');
      panel.setAttribute('aria-hidden', open ? 'true' : 'false');
      // a closed panel may hold links; inert takes them out of the tab order
      // as well as out of the accessibility tree, which aria-hidden alone does not
      if ('inert' in panel) panel.inert = open;
    });
  });

  // a jump link into a collapsed service should open it on arrival
  function openFromHash() {
    if (!window.location.hash) return;
    var target = document.querySelector(window.location.hash);
    var item = target && target.closest ? target.closest('.acc__item') : null;
    if (!item) return;
    var btn = item.querySelector('.acc__btn');
    if (btn && !item.hasAttribute('data-open')) btn.click();
  }
  window.addEventListener('hashchange', openFromHash);
  openFromHash();

  /* ── work filters ────────────────────────────────────────────────────
        Filtering is attribute-driven: each tile lists its disciplines and a
        button matches against them. Tiles are hidden with the hidden
        attribute, so they leave the a11y tree as well as the layout. */

  var filterBar = document.querySelector('[data-filters]');

  if (filterBar) {
    var tiles = [].slice.call(document.querySelectorAll('[data-tags]'));
    var countEl = document.querySelector('[data-count-out]');
    var buttons = [].slice.call(filterBar.querySelectorAll('button'));

    var apply = function (want) {
      var shown = 0;
      tiles.forEach(function (tile) {
        var tags = (tile.getAttribute('data-tags') || '').split(/\s+/);
        var match = want === 'all' || tags.indexOf(want) !== -1;
        tile.hidden = !match;
        if (match) shown++;
      });
      buttons.forEach(function (b) {
        b.setAttribute('aria-pressed', b.getAttribute('data-filter') === want ? 'true' : 'false');
      });
      if (countEl) {
        countEl.textContent = shown + (shown === 1 ? ' project' : ' projects');
      }
    };

    filterBar.addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-filter]');
      if (btn) apply(btn.getAttribute('data-filter'));
    });

    apply('all');
  }

  /* ── discovery session form ──────────────────────────────────────────
        Same static-site constraint as the other forms: no endpoint, so this
        validates in the page and hands off to a pre-filled email. Errors are
        announced via aria-describedby, the outcome via the note's aria-live. */

  var discovery = document.getElementById('discoveryForm');

  if (discovery) {
    var dNote = document.getElementById('discoveryNote');

    /* Arriving from a service page (contact.html?service=<slug>): pre-select the
       closest topic and start the notes with the service, so the enquiry says
       what it is about. Unknown or missing values change nothing. */
    var SERVICE_TOPIC = {
      'custom-software': ['Custom software development', 'Build a new platform or app'],
      'microsoft-cloud': ['Microsoft Cloud solutions', 'Not sure yet'],
      'enterprise-saas': ['Enterprise SaaS platforms', 'Build a new platform or app'],
      'mobile-apps': ['Mobile application development', 'Build a new platform or app'],
      'business-intelligence': ['Business intelligence & reporting', 'Reporting and business intelligence'],
      'system-integration': ['System integration', 'Connect existing systems'],
      'ux-design': ['UX & system design', 'Not sure yet'],
      'modernisation': ['Software modernisation', 'Replace a legacy system'],
      'support': ['Ongoing support & maintenance', 'Not sure yet']
    };
    try {
      var svc = new URLSearchParams(window.location.search).get('service');
      var topic = svc && SERVICE_TOPIC[svc];
      if (topic) {
        var goal = document.getElementById('d-goal');
        var notes = document.getElementById('d-notes');
        if (goal) [].forEach.call(goal.options, function (o) { if (o.text === topic[1]) goal.value = o.value || o.text; });
        if (notes && !notes.value) notes.value = 'About: ' + topic[0] + '\n\n';
      }
    } catch (err) { /* no URLSearchParams: leave the form as it is */ }

    var showError = function (field, on) {
      var err = document.getElementById(field.id + '-err');
      if (err) err.hidden = !on;
      field.setAttribute('aria-invalid', on ? 'true' : 'false');
    };

    discovery.addEventListener('submit', function (e) {
      e.preventDefault();

      var required = [].slice.call(discovery.querySelectorAll('[required]'));
      var firstBad = null;
      required.forEach(function (field) {
        var ok = field.checkValidity();
        showError(field, !ok);
        if (!ok && !firstBad) firstBad = field;
      });
      if (firstBad) {
        firstBad.focus();
        if (dNote) dNote.textContent = 'Please complete the highlighted fields before sending.';
        return;
      }

      var val = function (id) {
        var el = document.getElementById(id);
        return el && el.value ? el.value.trim() : '';
      };

      var body = [
        'Name: ' + val('d-name'),
        'Work email: ' + val('d-email'),
        'Company: ' + val('d-company'),
        'Looking to do: ' + val('d-goal'),
        'Rough timeline: ' + (val('d-timeline') || '—'),
        '',
        'Anything we should know:',
        val('d-notes') || '—'
      ].join('\n');

      window.location.href = 'mailto:info@gemis.co.za'
        + '?subject=' + encodeURIComponent('Discovery Session request — ' + val('d-company'))
        + '&body=' + encodeURIComponent(body);

      if (dNote) {
        dNote.textContent = 'Opening your email client with your details pre-filled. '
          + 'If nothing happens, email info@gemis.co.za directly.';
      }
    });

    // clear an error as soon as the field becomes valid
    discovery.addEventListener('input', function (e) {
      var f = e.target;
      if (f.hasAttribute('required') && f.checkValidity()) showError(f, false);
    });
  }

  /* ── enquiry form → email hand-off ───────────────────────────────────
        Same constraint as the CTA field: the site is static, so there is no
        endpoint. Validate here, then open a pre-filled message. The consent
        box is required because the privacy notice promises consent is
        recorded with the enquiry. */

  var enquiry = document.getElementById('enquiry');

  if (enquiry) {
    enquiry.addEventListener('submit', function (e) {
      e.preventDefault();

      // novalidate is set so we can report the first problem ourselves
      var invalid = enquiry.querySelector(':invalid');
      if (invalid) {
        invalid.focus();
        if (invalid.reportValidity) invalid.reportValidity();
        return;
      }

      var val = function (id) {
        var el = document.getElementById(id);
        return el && el.value ? el.value.trim() : '';
      };

      var lines = [
        'Name: ' + val('f-name'),
        'Work email: ' + val('f-email'),
        'Company: ' + (val('f-company') || '—'),
        'Service: ' + (val('f-service') || '—'),
        'Indicative budget: ' + (val('f-budget') || 'Prefer not to say'),
        '',
        'What we are trying to solve:',
        val('f-message'),
        '',
        'I consent to GEMIS processing this information in order to respond to this enquiry.'
      ];

      window.location.href = 'mailto:info@gemis.co.za'
        + '?subject=' + encodeURIComponent('Enquiry from ' + (val('f-company') || val('f-name')))
        + '&body=' + encodeURIComponent(lines.join('\n'));

      var note = document.getElementById('enquiryNote');
      if (note) {
        note.textContent = 'Opening your email client with the enquiry pre-filled. '
          + 'If nothing happens, email info@gemis.co.za directly.';
      }
    });
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
