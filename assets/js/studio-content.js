/* ═══════════════════════════════════════════════════════════════════════
   GEMIS® Studio — single source of truth for all copy, numbers & flags.
   Static-site adaptation of /content/site.ts from the build brief.

   HONESTY RULES:
   - Every number, client name and metric that needs human confirmation is
     flagged UNVERIFIED. Confirm before publishing marketing claims.
   - No invented client results, percentages or testimonials. Where a real
     metric is not supplied (metric: null) the outcome line renders without
     a number.
   ═══════════════════════════════════════════════════════════════════════ */

window.STUDIO_CONTENT = {

  meta: {
    title: "UI/UX & Product Design Studio in Johannesburg | GEMIS® Studio",
    description:
      "Product, interface and web design for South African companies. " +
      "Fixed pricing from R6,500. Designed and built under one roof — Sandton, Johannesburg.",
  },

  nap: {
    /* Exact NAP — must match schema + Google Business Profile everywhere. */
    address: "66 Park Lane, Sandown, Sandton, 2196",
    phone: "+27 11 219 5008",
    email: "info@gemis.co.za",
  },

  numbers: {
    /* UNVERIFIED — all four figures need human confirmation. The current
       Brand Studio page and the designer's portfolio disagree on client
       count; one set of figures must be used everywhere. */
    established: { value: 2005, label: "EST.", suffix: "", status: "UNVERIFIED" },
    products:    { value: 16,   label: "products shipped", suffix: "+", status: "UNVERIFIED" },
    clients:     { value: 20,   label: "clients", suffix: "+", status: "UNVERIFIED" },
    services:    { value: 4,    label: "services", suffix: "", status: "UNVERIFIED" },
  },

  heroMeta: "EST. 2005 · 16+ PRODUCTS SHIPPED · 20+ CLIENTS", /* UNVERIFIED */

  problems: [
    /* Section 04 — the problem mirror. targets map to service card ids. */
    { text: "“Our website looks fine but nobody enquires.”",   target: "svc-03" },
    { text: "“Our staff hate the system they use all day.”",   target: "svc-01" },
    { text: "“It works, it just looks like 2011.”",            target: "svc-02" },
    { text: "“Every screen in our product looks different.”",  target: "svc-02" },
    { text: "“We're adding AI and nobody trusts it.”",         target: "svc-01" },
    { text: "“Users drop off and we don't know where.”",       target: "svc-01" },
  ],

  services: [
    { id: "svc-01", num: "01", name: "Product Teardown",         price: "R6,500",              duration: "5 days" },
    { id: "svc-02", num: "02", name: "Interface Refresh Sprint", price: "R18,000 – R25,000",   duration: "2 weeks" },
    { id: "svc-03", num: "03", name: "Web Experience",           price: "R55,000 – R85,000",   duration: "6 – 8 weeks" },
    { id: "svc-04", num: "04", name: "Embedded Designer",        price: "R20,000 – R35,000 / month", duration: "Ongoing" },
  ],

  work: [
    { id: "01", name: "ManaGem",   disciplines: "Product design · Dashboard UX · Design system",
      outcome: "", metric: null, hue: "gold",
      href: "managem.html",
      status: "UNVERIFIED — confirm publication rights & outcome" },
    { id: "02", name: "WasteMart", disciplines: "Operations UX · Driver app · Customer portal",
      outcome: "", metric: null, hue: "signal",
      href: "wastemart.html",
      status: "UNVERIFIED" },
    { id: "03", name: "FINOS",     disciplines: "Financial operating system · AI review workflow",
      outcome: "", metric: null, hue: "bone",
      href: "index.html#work",
      status: "UNVERIFIED" },
    { id: "04", name: "CMAXX",     disciplines: "Web experience · Identity · Launch",
      outcome: "", metric: null, hue: "alert",
      href: "index.html#work",
      status: "UNVERIFIED" },
  ],

  clients: [
    /* UNVERIFIED — confirm each name may be shown publicly as a client. */
    "MANAGEM", "WASTEMART", "FINOS", "CMAXX", "SMARTSTART", "SONKE",
  ],

  tools: ["FIGMA", "REACT", "NEXT.JS", "WORDPRESS", "AZURE", "GSAP", "THREE.JS", "WEBFLOW"],
};
