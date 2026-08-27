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

  /* Per project brief §9 (content governance): unverified counts are no
     longer displayed. The former numbers block is replaced by the
     Measured Outcomes block below. */
  heroMeta: "GEM INFORMATION SYSTEMS · SANDTON, JOHANNESBURG — 26.1076°S 28.0567°E",

  /* ── Block 05b · Design leadership — DRAFT copy, owner approval pending.
     OD-06 unresolved → role only, no personal name shown. ─────────────── */
  leadership: {
    headline: "SENIOR EYES ON EVERY SCREEN.",
    statement:
      "Every engagement is led by a senior product designer — the same person " +
      "who scopes the work reviews every screen that leaves the studio. No " +
      "handoffs to juniors, no account layer between you and the person " +
      "designing your product.",
    specialisms: [
      "Product strategy", "Interface design", "Design systems", "UX research",
      "Dashboard & data UX", "Service design", "Accessibility", "Developer handoff",
    ],
    pivot: "One lead, accountable end to end — backed by the team below.",
  },

  /* ── Block 05c · Staffing — DRAFT copy, owner approval pending. ──────── */
  staffing: {
    disciplines: [
      { name: "Product design",     line: "Flows, screens and states, specified to build." },
      { name: "Design systems",     line: "Tokens, components and rules your team can keep." },
      { name: "Research & content", line: "Interviews, audits and the words on the screen." },
      { name: "Engineering",        line: "The developers beside us who build what we design." },
    ],
    closing: "Sized to the work — never a bench you're paying for.",
  },

  /* ── Block 05d · Instruments — DRAFT copy, owner approval pending. ───── */
  instruments: {
    methods:  ["Heuristic evaluation", "Journey mapping", "Usability testing",
               "Analytics review", "Contrast auditing", "Content audits"],
    delivery: ["Figma", "Design tokens", "Annotated handoff",
               "Interaction specs", "Recorded walkthroughs", "30-day support channel"],
  },

  /* ── Block 10 · Measured outcomes — per brief §12 risk mitigation:
     no figures are published until verified with the client and
     publication rights are documented. Method statement only. ─────────── */
  outcomes: {
    status: "UNVERIFIED — all three metric values withheld pending client verification",
    metrics: [
      { name: "Enquiry conversion", direction: "up",   caption: "Measured on Web Experience engagements, before and after launch." },
      { name: "Task errors",        direction: "down", caption: "Measured on operations UX engagements, per release." },
      { name: "Time on task",       direction: "down", caption: "Measured in usability testing, before and after redesign." },
    ],
    footnote: "Figures appear here as client verification and publication rights are secured.",
  },

  vatNote: "All prices exclude VAT. GEM Information Systems (Pty) Ltd is a VAT-registered vendor.",
  /* UNVERIFIED — confirm VAT registration status before publishing (FR-12 / OD-05). */

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
