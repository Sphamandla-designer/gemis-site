/* GEMIS — About page: hero letters parallax, journey rail, dna cards */
(function () {
  if (!document.body.classList.contains('page-about')) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* floating outline letters — scroll + mouse parallax */
  const letters = gsap.utils.toArray('.aletter');
  if (letters.length && !reduced) {
    gsap.from(letters, {
      opacity: 0, y: 90, duration: 1.4, ease: 'power3.out', stagger: 0.09, delay: 0.4,
    });
    letters.forEach((el) => {
      const depth = parseFloat(el.dataset.depth || '1');
      gsap.to(el, {
        yPercent: -34 * depth,
        rotate: (depth - 1) * 9,
        ease: 'none',
        scrollTrigger: { trigger: '.ahero', start: 'top top', end: 'bottom top', scrub: true },
      });
    });
    const fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    if (fine) {
      const movers = letters.map((el) => ({
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

  /* dna cards — staggered rise */
  gsap.utils.toArray('.dna__card').forEach((card, i) => {
    if (reduced) return;
    gsap.from(card, {
      y: 70, opacity: 0, duration: 0.9, ease: 'power3.out', delay: (i % 4) * 0.09,
      scrollTrigger: { trigger: card, start: 'top 88%' },
    });
  });

  /* journey rail draws + steps light up */
  const line = document.getElementById('journeyLine');
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

  /* pledge headline reveal */
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
