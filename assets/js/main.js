/* GEMIS — interaction & scroll choreography (GSAP + Lenis) */
(function () {
  gsap.registerPlugin(ScrollTrigger);
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) document.body.classList.add('reduced-motion');

  /* ───────── text splitting helpers ───────── */
  function splitChars(el) {
    const text = el.textContent;
    el.textContent = '';
    const frag = document.createDocumentFragment();
    for (const ch of text) {
      const s = document.createElement('span');
      s.className = 'char';
      s.textContent = ch === ' ' ? ' ' : ch;
      frag.appendChild(s);
    }
    el.appendChild(frag);
    return el.querySelectorAll('.char');
  }
  function splitWords(el) {
    const words = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    words.forEach((w, i) => {
      const s = document.createElement('span');
      s.className = 'word';
      s.textContent = w;
      el.appendChild(s);
      if (i < words.length - 1) el.appendChild(document.createTextNode(' '));
    });
    return el.querySelectorAll('.word');
  }
  function wrapLines(el) {
    // simple line wrapper for headings: wraps content in a mask
    const inner = document.createElement('span');
    inner.className = 'line-inner';
    while (el.firstChild) inner.appendChild(el.firstChild);
    const mask = document.createElement('span');
    mask.className = 'line-mask';
    mask.appendChild(inner);
    el.appendChild(mask);
    return inner;
  }

  // Split hero/footer display words into chars (keep .hero__accent intact)
  document.querySelectorAll('[data-split]').forEach((el) => {
    const accent = el.querySelector('.hero__accent');
    if (accent) accent.remove();
    splitChars(el);
    if (accent) el.appendChild(accent);
  });
  document.querySelectorAll('[data-split-lines]').forEach(wrapLines);
  const manifestoWords = document.getElementById('manifestoText')
    ? splitWords(document.getElementById('manifestoText'))
    : [];

  /* ───────── Lenis smooth scroll ───────── */
  let lenis = null;
  if (!reduced && window.Lenis) {
    lenis = new Lenis({ lerp: 0.09, wheelMultiplier: 1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    lenis.stop(); // locked during preloader
  }

  /* ───────── custom cursor ───────── */
  const cursor = document.getElementById('cursor');
  const dot = document.getElementById('cursorDot');
  const ring = document.getElementById('cursorRing');
  const label = document.getElementById('cursorLabel');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (finePointer && !reduced && cursor) {
    const pos = { x: -100, y: -100 };
    const ringPos = { x: -100, y: -100 };
    let shown = false;
    window.addEventListener('pointermove', (e) => {
      pos.x = e.clientX; pos.y = e.clientY;
      if (!shown) { shown = true; gsap.to(cursor, { opacity: 1, duration: 0.3 }); }
    }, { passive: true });
    gsap.ticker.add(() => {
      ringPos.x += (pos.x - ringPos.x) * 0.16;
      ringPos.y += (pos.y - ringPos.y) * 0.16;
      dot.style.transform = `translate(${pos.x}px, ${pos.y}px) translate(-50%,-50%)`;
      ring.style.transform = `translate(${ringPos.x}px, ${ringPos.y}px) translate(-50%,-50%)`;
    });
    document.querySelectorAll('[data-cursor], a, button').forEach((el) => {
      el.addEventListener('mouseenter', () => {
        const text = el.dataset.cursor;
        if (text) { label.textContent = text; cursor.classList.add('is-hover'); }
        else gsap.to(ring, { scale: 1.6, duration: 0.3 });
      });
      el.addEventListener('mouseleave', () => {
        cursor.classList.remove('is-hover');
        gsap.to(ring, { scale: 1, duration: 0.3 });
      });
    });
  }

  /* ───────── magnetic elements ───────── */
  if (finePointer && !reduced) {
    document.querySelectorAll('[data-magnetic]').forEach((el) => {
      const strength = 0.35;
      el.addEventListener('mousemove', (e) => {
        const r = el.getBoundingClientRect();
        gsap.to(el, {
          x: (e.clientX - r.left - r.width / 2) * strength,
          y: (e.clientY - r.top - r.height / 2) * strength,
          duration: 0.4, ease: 'power3.out',
        });
      });
      el.addEventListener('mouseleave', () => {
        gsap.to(el, { x: 0, y: 0, duration: 0.7, ease: 'elastic.out(1, 0.4)' });
      });
    });
  }

  /* ───────── preloader ───────── */
  const preloader = document.getElementById('preloader');
  const countEl = document.getElementById('preloaderCount');
  const barEl = document.getElementById('preloaderBar');

  function heroIntro() {
    const tl = gsap.timeline();
    tl.to('.hero .char', {
      yPercent: 0, duration: 1.1, ease: 'power4.out', stagger: 0.022,
    }, 0.1)
      .to('.hero__eyebrow', { opacity: 1, duration: 0.8 }, 0.5)
      .to('.hero__meta', { opacity: 1, duration: 0.8 }, 0.75)
      .from('.hero__ticker', { yPercent: 100, opacity: 0, duration: 0.9, ease: 'power3.out' }, 0.6)
      .from('.header', { yPercent: -120, duration: 0.8, ease: 'power3.out' }, 0.7);
    return tl;
  }
  gsap.set('.hero .char', { yPercent: 110 });
  gsap.set('.footer .char', { yPercent: 110 });

  if (preloader && !reduced) {
    const progress = { v: 0 };
    const tl = gsap.timeline({
      onComplete: () => {
        preloader.style.display = 'none';
        if (lenis) lenis.start();
        ScrollTrigger.refresh();
      },
    });
    tl.to('.pl-char', { y: 0, duration: 0.9, ease: 'power4.out', stagger: 0.06 }, 0.15)
      .to(progress, {
        v: 100, duration: 2.1, ease: 'power2.inOut',
        onUpdate: () => {
          const n = Math.round(progress.v);
          countEl.textContent = String(n).padStart(2, '0');
          barEl.style.width = n + '%';
        },
      }, 0.3)
      .to('.pl-char', { y: '-110%', duration: 0.7, ease: 'power3.in', stagger: 0.04 }, '-=0.35')
      .to('.preloader__row, .preloader__bar', { opacity: 0, duration: 0.4 }, '<')
      .to('.preloader__curtain', { yPercent: -100, duration: 1.0, ease: 'power4.inOut' }, '-=0.15')
      .to('.preloader__inner', { yPercent: -40, opacity: 0, duration: 0.7, ease: 'power3.in' }, '<')
      .add(heroIntro(), '-=0.55');
  } else {
    if (preloader) preloader.style.display = 'none';
    gsap.set('.hero .char', { yPercent: 0 });
    gsap.set(['.hero__eyebrow', '.hero__meta'], { opacity: 1 });
    if (lenis) lenis.start();
  }

  /* ───────── theme morphing per section ───────── */
  document.querySelectorAll('[data-section-theme]').forEach((sec) => {
    ScrollTrigger.create({
      trigger: sec,
      start: 'top 55%',
      end: 'bottom 55%',
      onToggle: (self) => {
        if (self.isActive) document.body.dataset.theme = sec.dataset.sectionTheme;
      },
    });
  });

  /* ───────── hero scroll: parallax + 3D handoff ───────── */
  if (!reduced) {
    ScrollTrigger.create({
      trigger: '.hero',
      start: 'top top',
      end: 'bottom top',
      scrub: true,
      onUpdate: (self) => {
        window.__heroScroll = self.progress;
        gsap.set('.hero__content', { yPercent: self.progress * 18, opacity: 1 - self.progress * 0.9 });
      },
    });
  }

  /* ───────── manifesto word-by-word reveal ───────── */
  if (manifestoWords.length) {
    gsap.to(manifestoWords, {
      opacity: 1,
      stagger: 0.06,
      ease: 'none',
      scrollTrigger: {
        trigger: '#manifestoText',
        start: 'top 78%',
        end: 'bottom 45%',
        scrub: 0.4,
      },
    });
  }

  /* ───────── generic reveals ───────── */
  document.querySelectorAll('.reveal').forEach((el, i) => {
    gsap.to(el, {
      opacity: 1, y: 0, duration: 1, ease: 'power3.out', delay: (i % 3) * 0.12,
      scrollTrigger: { trigger: el, start: 'top 85%' },
    });
  });

  /* ───────── section titles line reveal ───────── */
  document.querySelectorAll('[data-split-lines] .line-inner').forEach((inner) => {
    gsap.to(inner, {
      y: 0, duration: 1.1, ease: 'power4.out',
      scrollTrigger: { trigger: inner, start: 'top 88%' },
    });
  });

  /* ───────── footer big chars reveal ───────── */
  ScrollTrigger.create({
    trigger: '.footer__title',
    start: 'top 82%',
    onEnter: () => gsap.to('.footer .char', {
      yPercent: 0, duration: 1, ease: 'power4.out', stagger: 0.02,
    }),
  });

  /* ───────── work cards entrance + parallax ───────── */
  document.querySelectorAll('.card').forEach((card) => {
    gsap.from(card, {
      y: 80, opacity: 0, duration: 1.1, ease: 'power3.out',
      scrollTrigger: { trigger: card, start: 'top 88%' },
    });
    if (!reduced) {
      gsap.fromTo(card.querySelector('.card__media'),
        { yPercent: 6 }, {
          yPercent: -6, ease: 'none',
          scrollTrigger: { trigger: card, start: 'top bottom', end: 'bottom top', scrub: true },
        });
    }
  });

  /* ───────── services accordion ───────── */
  document.querySelectorAll('.service').forEach((service) => {
    const body = service.querySelector('.service__body');
    let open = false;
    const toggle = () => {
      open = !open;
      gsap.to(body, { height: open ? 'auto' : 0, duration: 0.55, ease: 'power3.inOut' });
    };
    service.addEventListener('click', toggle);
    service.addEventListener('mouseenter', () => { if (!open) toggle(); });
    service.addEventListener('mouseleave', () => { if (open) toggle(); });
    gsap.from(service, {
      y: 50, opacity: 0, duration: 0.9, ease: 'power3.out',
      scrollTrigger: { trigger: service, start: 'top 90%' },
    });
  });

  /* ───────── stat counters ───────── */
  document.querySelectorAll('.stat__num').forEach((el) => {
    const end = parseFloat(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    const decimals = el.dataset.count.includes('.') ? 1 : 0;
    const obj = { v: 0 };
    ScrollTrigger.create({
      trigger: el,
      start: 'top 85%',
      once: true,
      onEnter: () => gsap.to(obj, {
        v: end, duration: 1.8, ease: 'power3.out',
        onUpdate: () => { el.textContent = obj.v.toFixed(decimals) + suffix; },
      }),
    });
  });

  /* ───────── marquees: velocity-reactive ───────── */
  document.querySelectorAll('[data-ticker]').forEach((ticker) => {
    const track = ticker.querySelector('.ticker__track');
    const speed = parseFloat(ticker.dataset.speed || '1');
    let x = 0;
    let vel = 0;
    const base = 0.6 * speed;
    if (reduced) return;
    gsap.ticker.add(() => {
      const half = track.scrollWidth / 2;
      if (!half) return;
      x -= (base + vel * Math.sign(base));
      // wrap seamlessly
      if (x <= -half) x += half;
      if (x > 0) x -= half;
      track.style.transform = `translate3d(${x}px,0,0)`;
      vel *= 0.92;
    });
    ScrollTrigger.create({
      trigger: ticker,
      start: 'top bottom',
      end: 'bottom top',
      onUpdate: (self) => { vel = gsap.utils.clamp(-14, 14, self.getVelocity() / 220); },
    });
  });

  /* ───────── footer wordmark + badge spin ───────── */
  gsap.to('.footer__wordmark span', {
    y: 0, yPercent: 0, ease: 'none',
    scrollTrigger: { trigger: '.footer__wordmark', start: 'top bottom', end: 'bottom bottom', scrub: 0.5 },
  });
  gsap.set('.footer__wordmark span', { yPercent: 35 });
  if (!reduced) {
    gsap.to('#badge svg', { rotation: 360, duration: 14, repeat: -1, ease: 'none' });
  }

  /* ───────── overlay menu ───────── */
  const burger = document.getElementById('burger');
  const menu = document.getElementById('menu');
  let menuOpen = false;
  const menuTl = gsap.timeline({ paused: true })
    .set(menu, { visibility: 'visible' })
    .to('.menu__bg', { clipPath: 'inset(0 0 0% 0)', duration: 0.8, ease: 'power4.inOut' })
    .to('.menu__word', { y: 0, duration: 0.8, ease: 'power4.out', stagger: 0.07 }, '-=0.3')
    .to('.menu__foot', { opacity: 1, duration: 0.5 }, '-=0.4');

  function toggleMenu(force) {
    menuOpen = force !== undefined ? force : !menuOpen;
    burger.classList.toggle('is-open', menuOpen);
    burger.setAttribute('aria-label', menuOpen ? 'Close menu' : 'Open menu');
    menu.setAttribute('aria-hidden', String(!menuOpen));
    if (menuOpen) {
      menuTl.timeScale(1).play();
      if (lenis) lenis.stop();
    } else {
      menuTl.timeScale(1.6).reverse();
      if (lenis) lenis.start();
    }
  }
  burger.addEventListener('click', () => toggleMenu());
  document.querySelectorAll('[data-menu-close]').forEach((link) => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const target = link.getAttribute('href');
      toggleMenu(false);
      setTimeout(() => {
        if (lenis) lenis.scrollTo(target, { offset: 0, duration: 1.4 });
        else document.querySelector(target)?.scrollIntoView({ behavior: 'smooth' });
      }, 450);
    });
  });
  window.addEventListener('keydown', (e) => { if (e.key === 'Escape' && menuOpen) toggleMenu(false); });

  /* ───────── anchor links (non-menu) ───────── */
  document.querySelectorAll('a[href^="#"]:not([data-menu-close])').forEach((a) => {
    a.addEventListener('click', (e) => {
      const target = document.querySelector(a.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      if (lenis) lenis.scrollTo(target, { duration: 1.4 });
      else target.scrollIntoView({ behavior: 'smooth' });
    });
  });
})();
