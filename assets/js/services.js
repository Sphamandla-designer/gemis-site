/* GEMIS — Services page: glyph parallax, pain chips, service index, process rail */
(function () {
  if (!document.body.classList.contains('page-services')) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* floating outline glyphs — scroll + mouse parallax */
  const glyphs = gsap.utils.toArray('.aletter');
  if (glyphs.length && !reduced) {
    gsap.from(glyphs, {
      opacity: 0, y: 90, duration: 1.4, ease: 'power3.out', stagger: 0.09, delay: 0.4,
    });
    glyphs.forEach((el) => {
      const depth = parseFloat(el.dataset.depth || '1');
      gsap.to(el, {
        yPercent: -34 * depth,
        rotate: (depth - 1) * 9,
        ease: 'none',
        scrollTrigger: { trigger: '.ahero', start: 'top top', end: 'bottom top', scrub: true },
      });
    });
    if (finePointer) {
      const movers = glyphs.map((el) => ({
        x: gsap.quickTo(el, 'x', { duration: 1.1, ease: 'power2.out' }),
        y: gsap.quickTo(el, 'y', { duration: 1.1, ease: 'power2.out' }),
        depth: parseFloat(el.dataset.depth || '1'),
      }));
      window.addEventListener('pointermove', (e) => {
        const nx = (e.clientX / window.innerWidth - 0.5) * 2;
        const ny = (e.clientY / window.innerHeight - 0.5) * 2;
        movers.forEach((m) => { m.x(nx * 26 * m.depth); m.y(ny * 18 * m.depth); });
      }, { passive: true });
    }
  }

  /* pain chips — tap toggles the "solved" state (hover handles it on desktop) */
  document.querySelectorAll('.pain').forEach((pain, i) => {
    pain.addEventListener('click', () => pain.classList.toggle('is-fixed'));
    if (!reduced) {
      gsap.from(pain, {
        y: 34, opacity: 0, duration: 0.7, ease: 'power3.out', delay: i * 0.07,
        scrollTrigger: { trigger: '.pains', start: 'top 86%' },
      });
    }
  });

  /* service index — exclusive accordion */
  const items = gsap.utils.toArray('.xsv');
  let openItem = null;
  function setOpen(item, open) {
    const body = item.querySelector('.xsv__body');
    const row = item.querySelector('.xsv__row');
    item.classList.toggle('is-open', open);
    row.setAttribute('aria-expanded', String(open));
    gsap.to(body, { height: open ? 'auto' : 0, duration: 0.6, ease: 'power3.inOut' });
    gsap.to(item.querySelector('.xsv__arrow'), { rotation: open ? 45 : 0, duration: 0.45, ease: 'power3.out' });
  }
  items.forEach((item) => {
    const row = item.querySelector('.xsv__row');
    const toggle = () => {
      if (openItem === item) { setOpen(item, false); openItem = null; return; }
      if (openItem) setOpen(openItem, false);
      setOpen(item, true);
      openItem = item;
      setTimeout(() => ScrollTrigger.refresh(), 650);
    };
    row.addEventListener('click', toggle);
    row.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
    });
    if (!reduced) {
      gsap.from(item, {
        y: 46, opacity: 0, duration: 0.85, ease: 'power3.out',
        scrollTrigger: { trigger: item, start: 'top 92%' },
      });
    }
  });
  if (items.length) { setOpen(items[0], true); openItem = items[0]; }

  /* dna cards — staggered rise */
  gsap.utils.toArray('.dna__card').forEach((card, i) => {
    if (reduced) return;
    gsap.from(card, {
      y: 70, opacity: 0, duration: 0.9, ease: 'power3.out', delay: (i % 3) * 0.09,
      scrollTrigger: { trigger: card, start: 'top 88%' },
    });
  });

  /* process rail draws + steps light up */
  const line = document.getElementById('svcLine');
  if (line && !reduced) {
    gsap.fromTo(line, { scaleY: 0 }, {
      scaleY: 1, ease: 'none', transformOrigin: 'top center',
      scrollTrigger: {
        trigger: '.journey__wrap',
        start: 'top 70%',
        end: 'bottom 45%',
        scrub: 0.4,
      },
    });
    gsap.utils.toArray('.jstep').forEach((step) => {
      gsap.from(step, {
        x: -50, opacity: 0, duration: 0.8, ease: 'power3.out',
        scrollTrigger: { trigger: step, start: 'top 84%' },
      });
      ScrollTrigger.create({
        trigger: step,
        start: 'top 62%',
        end: 'bottom 38%',
        onToggle: (self) => step.classList.toggle('is-lit', self.isActive),
      });
    });
  }

  /* featured solutions — rows rise in */
  gsap.utils.toArray('.sol').forEach((sol, i) => {
    if (reduced) return;
    gsap.from(sol, {
      y: 44, opacity: 0, duration: 0.8, ease: 'power3.out', delay: (i % 2) * 0.08,
      scrollTrigger: { trigger: sol, start: 'top 92%' },
    });
  });

  /* adapt statement reveal */
  const pledgeInners = document.querySelectorAll('.pledge__title .line-inner');
  if (pledgeInners.length && !reduced) {
    gsap.set(pledgeInners, { y: 0, yPercent: 110 });
    gsap.timeline({ scrollTrigger: { trigger: '.pledge', start: 'top 72%' } })
      .to(pledgeInners, { yPercent: 0, duration: 1.1, ease: 'power4.out', stagger: 0.14 }, 0)
      .from('.pledge__text', { opacity: 0, y: 30, duration: 0.9, ease: 'power3.out' }, 0.4);
  } else if (pledgeInners.length) {
    gsap.set(pledgeInners, { y: 0, yPercent: 0 });
  }
})();
