# GEMIS® — Software Development Studio

An animation-rich, single-page studio site inspired by modern award-winning
agency websites. Fully static and self-contained — no build step, no CDN
dependencies, no audio.

## Highlights

- **Preloader** — percentage counter, progress bar, masked wordmark reveal,
  full-screen curtain wipe into the hero.
- **WebGL hero** — real-time chrome torus knot (Three.js) lit by a procedural
  studio environment, with pointer parallax and scroll-linked rotation.
- **Smooth scrolling** — Lenis + GSAP ScrollTrigger orchestration.
- **Scroll choreography** — staggered character reveals, word-by-word
  manifesto scrub, line-mask section titles, parallax work cards,
  scroll-velocity-reactive marquees, animated stat counters.
- **Live work-card visuals** — four procedural canvas animations (liquid
  chrome, neural constellation, silk waves, emerald grid) that run only
  while on screen.
- **Section theme morphing** — the page background cross-fades between dark
  and bone as sections enter.
- **Custom cursor** — lerped dot + ring with contextual "View" label,
  magnetic buttons, full-screen overlay menu.
- **Accessibility** — `prefers-reduced-motion` disables heavy animation,
  semantic markup, keyboard-closable menu.

## Running locally

Any static file server works:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Structure

```
index.html              # single page, all sections
assets/css/style.css    # design tokens + all styling
assets/js/main.js       # GSAP/Lenis interaction & scroll choreography
assets/js/hero3d.js     # Three.js hero centerpiece (ES module)
assets/js/cards.js      # procedural canvas visuals for work cards
assets/js/*.min.js      # vendored gsap, ScrollTrigger, lenis, three
assets/fonts/           # vendored variable fonts (Archivo, Space Grotesk, JetBrains Mono)
```

Libraries: [GSAP](https://gsap.com) + ScrollTrigger, [Lenis](https://lenis.darkroom.engineering), [Three.js](https://threejs.org).
