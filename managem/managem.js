/* ManaGem landing page — v1 draft behaviour. No dependencies. */
(function () {
  'use strict';
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── tracking: every CTA has a unique data-track id ─────────────────── */
  function track(id, extra) {
    if (!id) return;
    const ev = Object.assign({ event: 'cta_click', cta: id }, extra || {});
    (window.dataLayer = window.dataLayer || []).push(ev);
    if (window.gtag) window.gtag('event', 'cta_click', ev);
  }
  document.addEventListener('click', (e) => {
    const t = e.target.closest('[data-track]');
    if (t) track(t.dataset.track);
  });

  /* ── header: transparent over hero, solid after 80px ────────────────── */
  const hdr = $('#hdr');
  const onScroll = () => hdr.classList.toggle('is-stuck', window.scrollY > 80);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* active anchor in the desktop nav */
  const navLinks = $$('.hdr__nav a');
  const sections = navLinks.map((a) => $(a.getAttribute('href'))).filter(Boolean);
  if ('IntersectionObserver' in window && sections.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        navLinks.forEach((a) => a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id));
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    sections.forEach((s) => io.observe(s));
  }

  /* ── mobile menu ─────────────────────────────────────────────────────── */
  const burger = $('.burger');
  const mmenu = $('#mmenu');
  function setMenu(open) {
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    mmenu.hidden = !open;
    document.body.classList.toggle('is-locked', open);
    if (open) hdr.classList.add('is-stuck');
    else onScroll();
  }
  burger.addEventListener('click', () => setMenu(mmenu.hidden));
  $$('a', mmenu).forEach((a) => a.addEventListener('click', () => setMenu(false)));

  /* ── scroll reveal ───────────────────────────────────────────────────── */
  const reveals = $$('[data-reveal]');
  if (reduced || !('IntersectionObserver' in window)) {
    reveals.forEach((el) => el.classList.add('is-in'));
  } else {
    const ro = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('is-in'); ro.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    reveals.forEach((el) => ro.observe(el));
  }

  /* ── the flow: tabs + pulse along the line on scroll ─────────────────── */
  const flow = $('#flow');
  if (flow) {
    const tabs = $$('.stage__btn', flow);
    const panels = $$('.shot', flow);
    const stages = $$('.stage', flow);
    let hoverTimer = null;

    function select(n, focus) {
      tabs.forEach((t, i) => {
        const on = i === n;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        panels[i].hidden = !on;
        if (on && focus) t.focus();
      });
    }
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(i));
      t.addEventListener('focus', () => select(i));
      /* hover previews on pointer devices; tap selects on touch */
      t.addEventListener('mouseenter', () => { clearTimeout(hoverTimer); hoverTimer = setTimeout(() => select(i), 120); });
      t.addEventListener('mouseleave', () => clearTimeout(hoverTimer));
      t.addEventListener('keydown', (e) => {
        const k = e.key;
        if (k !== 'ArrowRight' && k !== 'ArrowLeft' && k !== 'ArrowDown' && k !== 'ArrowUp' && k !== 'Home' && k !== 'End') return;
        e.preventDefault();
        let n = i;
        if (k === 'ArrowRight' || k === 'ArrowDown') n = (i + 1) % tabs.length;
        if (k === 'ArrowLeft' || k === 'ArrowUp') n = (i - 1 + tabs.length) % tabs.length;
        if (k === 'Home') n = 0;
        if (k === 'End') n = tabs.length - 1;
        select(n, true);
      });
    });

  }

  /* ── who it's for: tabs ──────────────────────────────────────────────── */
  const whoTabs = $$('.chip[data-who]');
  const whoPanels = whoTabs.map((t) => $('#' + t.getAttribute('aria-controls')));
  function selectWho(n, focus) {
    whoTabs.forEach((t, i) => {
      const on = i === n;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      whoPanels[i].hidden = !on;
      if (on && focus) t.focus();
    });
  }
  whoTabs.forEach((t, i) => {
    t.addEventListener('click', () => selectWho(i));
    t.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      e.preventDefault();
      selectWho(e.key === 'ArrowRight' ? (i + 1) % whoTabs.length : (i - 1 + whoTabs.length) % whoTabs.length, true);
    });
  });
  $$('[data-who-link]').forEach((a) => a.addEventListener('click', () => selectWho(Number(a.dataset.whoLink) - 1)));

  /* ── pricing toggle (Monthly | Yearly segments) ───────────────────── */
  const segs = $$('.toggle__seg');
  if (segs.length) {
    const amts = $$('.plan__price .amt');
    const pers = $$('.plan__price .per');
    segs.forEach((seg) => seg.addEventListener('click', () => {
      const annual = seg.dataset.billing === 'annual';
      segs.forEach((s2) => { const on = s2 === seg; s2.classList.toggle('is-on', on); s2.setAttribute('aria-pressed', String(on)); });
      amts.forEach((a) => { a.textContent = annual ? a.dataset.annual : a.dataset.monthly; });
      pers.forEach((p) => { p.textContent = annual ? '/month, billed yearly' : '/month'; });
      track('pricing-toggle', { billing: annual ? 'annual' : 'monthly' });
    }));
  }

  /* ── modals (signup, demo, setup) ────────────────────────────────────── */
  let lastFocus = null;
  function openModal(id, opener) {
    const m = $('#m-' + id);
    if (!m) return;
    lastFocus = opener || document.activeElement;
    if (id === 'signup') {
      const plan = opener && opener.dataset.plan;
      $('#signupPlan').value = plan || '';
      const h = $('#m-signup-t');
      h.textContent = plan ? `Start your ${plan} trial.` : 'Your account in two minutes.';
    }
    m.hidden = false;
    document.body.classList.add('is-locked');
    const first = $('input, select, button:not(.modal__x)', m);
    if (first) setTimeout(() => first.focus(), 60);
    if (!mmenu.hidden) setMenu(false);
  }
  function closeModal() {
    const m = $('.modal:not([hidden])');
    if (!m) return;
    m.hidden = true;
    document.body.classList.remove('is-locked');
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  document.addEventListener('click', (e) => {
    const o = e.target.closest('[data-modal]');
    if (o) { e.preventDefault(); if (!$('.modal:not([hidden])')) openModal(o.dataset.modal, o); else { closeModal(); openModal(o.dataset.modal, o); } return; }
    if (e.target.closest('[data-close]')) closeModal();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { closeModal(); if (!mmenu.hidden) setMenu(false); }
    /* keep tab inside an open modal */
    const m = $('.modal:not([hidden])');
    if (e.key === 'Tab' && m) {
      const f = $$('a[href], button:not([disabled]), input, select, textarea', m).filter((el) => el.offsetParent !== null);
      if (!f.length) return;
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  /* deep links: #signup / #demo open the modal */
  if (location.hash === '#signup' || location.hash === '#demo') openModal(location.hash.slice(1));

  /* forms: client-side validation and a thank-you state.
     CONTENT-TODO: no backend yet — wire to the ManaGem signup / booking endpoints in v2. */
  $$('.form').forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let ok = true;
      $$('[required]', form).forEach((f) => {
        const bad = !f.value.trim() || (f.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value));
        f.classList.toggle('is-bad', bad);
        if (bad && ok) { f.focus(); ok = false; }
      });
      if (!ok) return;
      track(form.id === 'signupForm' ? 'submit-trial' : 'submit-demo', { plan: form.plan ? form.plan.value : undefined });
      form.hidden = true;
      const done = form.parentElement.querySelector('.form__done');
      done.hidden = false;
      $('button', done).focus();
    });
    $$('[required]', form).forEach((f) => f.addEventListener('input', () => f.classList.remove('is-bad')));
  });

  /* feature "See more" links: feature pages are v2; for now scroll to the flow stage */
  const featureStage = { 'sales-pipeline': 0, 'products-pricing': 1, 'quotes-invoicing': 2, 'projects': 5, 'factory': 4, 'stock-control': 4 };
  $$('[data-feature]').forEach((a) => a.addEventListener('click', (e) => {
    e.preventDefault();
    const n = featureStage[a.dataset.feature];
    const tab = $$('.stage__btn')[n];
    if (tab) { tab.click(); $('#how').scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' }); }
  }));

  /* ── draft toggle: outline every [A#] assumption ─────────────────────── */
  const draft = $('#draftToggle');
  if (draft) {
    draft.addEventListener('click', () => {
      const on = draft.getAttribute('aria-pressed') !== 'true';
      draft.setAttribute('aria-pressed', String(on));
      document.body.classList.toggle('show-assumptions', on);
      draft.textContent = on ? 'Draft v1 · hide assumptions' : 'Draft v1 · show assumptions';
    });
  }
})();
