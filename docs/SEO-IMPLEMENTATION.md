# SEO implementation — GEMIS corporate site and GEMIS Studio

24 November 2026. Implemented locally and left for review: **nothing has been
deployed.** The branch's pull request is open, not merged.

Everything below is generated or written from one place, `scripts/seo.py`, and
applied statically by `scripts/apply-seo.py` (the last step of the rebuild,
with a `--check` mode). No metadata is set by JavaScript in the browser.

## A. Pages audited

**Corporate site (29 public pages + 404):** `/` · `solutions/` and the nine
discipline pages (`custom-software`, `microsoft-cloud`, `enterprise-saas`,
`mobile-apps`, `business-intelligence`, `system-integration`, `ux-design`,
`modernisation`, `support`) · `work/` and six case studies (`sbs-waterproofing`,
`homeassist`, `wastemart`, `trans-hex`, `sonke`, `tores-foundation`) ·
`products/` · `products/managem/` · `insights/` and three articles
(`popia-business-systems-checklist`, `load-shedding-operations-resilience`,
`spreadsheets-to-a-system`) · `our-story/` · `contact.html` · `industries.html` ·
`privacy.html` · `terms.html` · `404.html`.

**GEMIS Studio (14 public pages + 404):** `studio/` · `work.html` · `about.html`
· `services.html` · `contact.html` · `privacy.html` · `terms.html` and seven
case pages `work-<slug>.html`.

**Redirect stubs (already `noindex`, outside the sitemap — unchanged):**
`solutions.html`, `work.html`, `managem.html`, `brand-studio.html`,
`services.html`, `about.html`, `case-studies.html`, `wastemart.html`,
`insights.html`, `solutions/bespoke-software/`, `solutions/managem/`.

**Other HTML the host serves publicly:** the two offline bundles, eight old
exports and prototypes at the root, `tools/og-card.html`, and the email
signature pages under `brand/` (see E).

Not in this repository: the dedicated ManaGEM site
(`sphamandla-designer.github.io/ManaGEM/`) — see F.

## B. Pages updated

All 30 corporate pages (title, description, robots, canonical, Open Graph,
Twitter/X, JSON-LD; H1 on the 23 pages the brief specified), the studio
homepage (title, description, H1, JSON-LD) and all studio pages (`og:locale`,
Twitter/X title/description/image, robots). `noindex` added to 15 non-page
files (E).

## C. SEO metadata matrix (corporate site)

| Page | URL | SEO title | Meta description | Primary keyword | H1 |
|---|---|---|---|---|---|
| Home | `/` | Custom Software & Business Systems South Africa | GEMIS | GEMIS designs, develops and supports custom business software, enterprise systems and mobile apps in South Africa — a long-term technology partner since 2014. | custom software development South Africa | Custom business software built around how your business works. |
| solutions | `/solutions/` | Software Development & IT Solutions South Africa | GEMIS | Explore GEMIS software development services in South Africa: custom software, Microsoft Azure, enterprise SaaS, mobile apps, system integration and UX design. | software development services South Africa | Software development and digital solutions for growing businesses. |
| products | `/products/` | Business Software & Digital Products | GEMIS | Explore GEMIS products: ManaGEM business management software, UX/UI and product design from GEMIS Studio, and practical technical training. | business software products | Business software, product design and technology training. |
| work | `/work/` | Software Development Case Studies South Africa | GEMIS | GEMIS software development case studies from South African construction, insurance, waste management, mining, non-profit and education organisations. | software development case studies South Africa | Business systems built to solve real operational challenges. |
| our-story | `/our-story/` | About GEMIS | South African Software Development Partner | GEM Information Systems is a Cape Town software development company that has built and supported business systems for South African organisations since 2014. | South African software development company | Building business systems and long-term technology partnerships. |
| contact | `/contact.html` | Contact GEMIS | Custom Software Development South Africa | Looking for custom software or business systems in South Africa? Contact GEMIS to discuss your project and book a discovery session. | custom software development South Africa contact | Let's discuss your business systems project. |
| insights | `/insights/` | Business Systems & Technology Insights | GEMIS | Practical insights from GEMIS on business software, POPIA compliance, keeping operations running through load-shedding, and moving off spreadsheets. | business systems insights | Insights on business systems, software and technology. |
| industries | `/industries.html` | Industries We Build Business Systems For | GEMIS | The sectors GEMIS has built business systems for, with the evidence: NGOs and non-profits, waste and field operations, and multi-company business and finance. | business systems by industry | Sectors we have built for |
| privacy | `/privacy.html` | Privacy Notice | GEM Information Systems (GEMIS) | How GEM Information Systems handles what you send through this site, which cookies it uses (none unless you accept analytics) and your rights under POPIA. | GEMIS privacy notice | How we handle your information |
| terms | `/terms.html` | Terms of Use | GEM Information Systems (GEMIS) | The terms for using the GEM Information Systems website: what its information means, who owns its content, links, liability and governing law. | GEMIS terms of use | The ground rules for this site |
| 404 | `/404.html` | Page not found | GEM Information Systems (GEMIS) | The page you were looking for has moved or never shipped. | — | This screen doesn’t exist. |
| custom-software | `/solutions/custom-software/` | Custom Software Development South Africa | GEMIS | GEMIS develops custom business software in South Africa: workflow automation, business management systems, customer portals and enterprise applications. | custom software development South Africa | Custom software development built around your business. |
| microsoft-cloud | `/solutions/microsoft-cloud/` | Microsoft Azure Cloud Solutions South Africa | GEMIS | GEMIS designs, deploys, migrates and supports secure Microsoft Azure environments for South African businesses, built around the systems they run. | Microsoft Azure solutions South Africa | Microsoft Azure cloud solutions for modern businesses. |
| enterprise-saas | `/solutions/enterprise-saas/` | Enterprise SaaS Development South Africa | GEMIS | GEMIS designs and develops enterprise SaaS platforms: one multi-tenant system serving many organisations, each with its own data, users and integrations. | enterprise SaaS development South Africa | Enterprise SaaS platforms built for many organisations. |
| mobile-apps | `/solutions/mobile-apps/` | Mobile App Development South Africa | GEMIS | GEMIS develops mobile apps that connect field teams, customers and business operations, including apps that keep working offline in the field. | mobile app development South Africa | Mobile applications that connect your business operations. |
| business-intelligence | `/solutions/business-intelligence/` | Business Intelligence & Power BI Solutions | GEMIS | Turn business data into reporting you can trust with GEMIS business intelligence: Power BI dashboards, automated reports and connected data. | Power BI business intelligence | Business intelligence and reporting that drive better decisions. |
| system-integration | `/solutions/system-integration/` | Business System Integration Services South Africa | GEMIS | Connect accounting, ERP, CRM, payments and APIs with GEMIS system integration. Stop typing the same information twice and keep data flowing between systems. | system integration services South Africa | Connect your business systems and eliminate manual data transfers. |
| ux-design | `/solutions/ux-design/` | UX/UI Design & Business System Design | GEMIS | GEMIS designs business software around its users through research, workflow mapping, prototyping and interface design for enterprise applications. | UX/UI design for business software | UX and system design built around the people who use your software. |
| modernisation | `/solutions/modernisation/` | Legacy Software Modernisation South Africa | GEMIS | Modernise ageing business software with GEMIS. Improve existing systems, infrastructure and workflows in planned stages, without stopping the business. | legacy software modernisation South Africa | Modernise your existing business software without disrupting operations. |
| support | `/solutions/support/` | Software Support & Maintenance South Africa | GEMIS | Keep business software reliable with GEMIS support: monitoring, maintenance, updates, troubleshooting and continuous improvement long after go-live. | software support and maintenance South Africa | Ongoing software support that keeps your business running. |
| sbs-waterproofing | `/work/sbs-waterproofing/` | Custom Business Management System for Construction | GEMIS | How GEMIS built SBS Waterproofing a business management system connecting enquiries, quotes, deposits, project profitability and stock. | construction business management system | How GEMIS built a business management system for SBS Waterproofing. |
| homeassist | `/work/homeassist/` | Insurance Claims Management Software | GEMIS | How GEMIS built HomeAssist's national plumbing-claims system: claims reported, plumbers dispatched, job evidence captured and signed off, customers kept informed. | insurance claims management software | Building a digital claims management system for HomeAssist. |
| wastemart | `/work/wastemart/` | Waste Management Software & Operations System | GEMIS | How GEMIS built WasteMart an operations platform connecting quotes, online payments, scheduling, a driver app and collection tracking. | waste management software | Connecting waste management operations from quote to collection. |
| trans-hex | `/work/trans-hex/` | Mining Reporting & SAP Integration Solution | GEMIS | How GEMIS stabilised a diamond miner's information system, automated its SAP financial data feed and built an integrated management report. | mining reporting SAP integration | Modernising mining operations through system integration and reporting. |
| sonke | `/work/sonke/` | NGO Monitoring & Evaluation Software | GEMIS | How GEMIS built Sonke Gender Justice a monitoring and evaluation system with offline mobile capture, approvals and donor reporting from verified data. | NGO monitoring and evaluation software | Designing a mobile monitoring and evaluation system for Sonke Gender Justice. |
| tores-foundation | `/work/tores-foundation/` | School Debating Management Platform | GEMIS | How GEMIS built Tore's Foundation one platform for its schools debating programme: competitions, live standings and coaches' claims across 24 schools. | school debating management platform | Building a digital debating management platform for 24 schools. |
| managem | `/products/managem/` | ManaGEM Business Management Software | GEMIS | Meet ManaGEM, a business management platform connecting enquiries, quotes, jobs, stock, invoicing and everyday operations in one system. | business management software | ManaGEM: one connected system for managing your business. |
| popia-business-systems-checklist | `/insights/popia-business-systems-checklist/` | POPIA Compliance for Business Systems: A Checklist | GEMIS | A practical POPIA checklist for business systems: where customer data lives, who can access it, and what happens when someone asks for it back. | POPIA compliance business systems | POPIA compliance: a practical checklist for your business systems. |
| load-shedding-operations-resilience | `/insights/load-shedding-operations-resilience/` | Business IT Resilience During Load-Shedding | GEMIS | How cloud hosting, offline-capable apps and backups keep business systems running through load-shedding, when a generator alone is not enough. | business IT resilience load-shedding | How to keep business systems running during load-shedding. |
| spreadsheets-to-a-system | `/insights/spreadsheets-to-a-system/` | When to Replace Spreadsheets with Business Software | GEMIS | Is your business outgrowing its spreadsheets? When to move to dedicated business software, what the move involves and what it really costs. | replace spreadsheets with business software | When should your business move from spreadsheets to software? |

**Studio homepage** `/studio/` — title *UX/UI & Product Design Studio South
Africa | GEMIS* · description *GEMIS Studio designs product and interface UX/UI,
websites and design systems for South African companies, with a developer-ready
handoff — or builds them too.* · keyword *UX/UI design studio South Africa* ·
H1 *UX/UI and product design for digital products that work.*

The other studio pages keep their existing titles (all unique), now with full
social metadata.

### Where the brief's wording was changed, and why

Every title, description and H1 was checked against the page's own record
(`scripts/cases.py`, `stories.py`, `solutions.py`, `services.py`,
`facts.md`). Where the record says something narrower, the wording follows the
record:

- **HomeAssist** — the record has plumber dispatch, job evidence and sign-off,
  not "contractor assignments and approvals".
- **Tore's Foundation** — competitions, live standings and coaches' claims;
  "reporting" is not in the record. "24 schools" **is** (kept).
- **Trans Hex** — "stabilised the information system, automated the SAP
  financial feed, integrated management report" (the record's words).
- **Microsoft Cloud** — "scalable" removed (the page never says it);
  "migration" kept (it does).
- **Enterprise SaaS** — "scalable architecture, workflows" replaced by what
  the page says: one multi-tenant system, many organisations, each kept
  separate. H1: *Enterprise SaaS platforms built for many organisations.*
- **POPIA article** — "data storage" replaced by the article's own framing
  (where data lives, who can access it, requests).
- **Industries** — the description lists only the sectors the page covers.
- **Our Story** — "since 2014" and Cape Town are confirmed (`facts.md`, the
  published address).
- **ManaGEM "case study" (brief 6.07)** — the corporate site has no separate
  ManaGEM case-study route; `products/managem/` is the ManaGEM page and takes
  the product-overview specification (brief 7).
- **Johannesburg / Gauteng** — not targeted anywhere: nothing in the
  repository records an office, staff or service coverage there.

### Headings

- One H1 on every page (verified), no skipped levels (verified).
- The corporate hero titles now carry the specified H1s, in the existing
  style. The **homepage** keeps *Systems built to last. Partners built to
  stay.* as the label directly under the H1 (and in the footer).
- The **studio homepage** keeps its rotating *Designed to be built.* display
  line (an animation the brief says not to remove); the H1 is a new kicker line
  above it in the studio's existing kicker style, and the display line became a
  paragraph with identical styling.
- Two layout fixes the longer H1s made necessary: the homepage title may now
  wrap inside its white block (it was held to two unbreakable lines), and on
  phones the two halves of every hero title flow together instead of being
  force-broken. The homepage's white block now takes the full width on phones,
  as every other page's already did (an older rule had kept it at 64%).
- The brief's suggested homepage H2 set was **not** forced onto the page: the
  existing sections (proof, solutions, how we work, case studies, in their
  words, principles, insights, contact) are already H2s in order, and the
  brief says to adapt rather than force. Section copy was left as approved.

## D. Technical SEO changes

**Canonical URLs.** Absolute, one per page, self-referencing, on
`https://sphamandla-designer.github.io/gemis-site/` — the address that actually
serves these pages. `gemis.co.za` serves a different site today, so pointing
canonicals there would send search engines to pages that do not exist. When
the domain is moved (F), change `CANON` in `seo.py` (and `CANONICAL` in
`stories.py`) and rebuild.

**Robots.** `index, follow, max-image-preview:large` on every public page;
`noindex` on both 404s, the redirect stubs (existing) and the non-page files
(E). `robots.txt` allows everything and names the sitemap.

**Open Graph / Twitter/X.** Every page: `og:type` (article for articles and
case studies), `og:site_name`, `og:locale en_ZA`, title, description, url,
image with width, height and alt; `twitter:card summary_large_image`, title,
description, image and alt. Images: the share card
(`assets/img/og/gemis-share.jpg`, 1200×630) by default; each case study and
ManaGEM use a frame of their own video (1280×720). Every image exists.

**Structured data (JSON-LD).** One graph per corporate page:
- `Organization` (name, legal name, alternate name, logo, email, the Cape Town
  address, founding year, slogan, a sales `ContactPoint`, `sameAs` LinkedIn and
  gemis.co.za) and `WebSite` — the same `@id`s on every page, so they resolve
  to one entity.
- The page as `WebPage`, `CollectionPage`, `AboutPage` or `ContactPage`, with
  its `BreadcrumbList` (now starting at Home — the previous ones did not).
- `Service` on the nine disciplines (description from the page's own copy,
  provider, `areaServed` South Africa).
- `Article` on the three insights (with `datePublished` 2026-10-21 from the
  articles' record) and the six case studies (about the client organisation).
- `SoftwareApplication` for ManaGEM — name, category, description, publisher.
  **No price, operating system or rating is stated because none is published;
  without a price it will not qualify for Google's software rich result.**
- Kept from the generators, unchanged: `FAQPage` (service pages), `ItemList`
  (solutions and case-study indexes), `VideoObject` (case studies).
- Studio homepage: Organization (same `@id`), WebPage, BreadcrumbList,
  Service.
- No `Review`, `AggregateRating` or `LocalBusiness` (not eligible on what is
  published).

**Sitemap.** Regenerated by `apply-seo.py`: 43 URLs (29 corporate, 14 studio),
canonical URLs only — no redirects, no 404s, no noindex pages — each with
`lastmod` from git.

**Image SEO.** Every image already had an `alt`; content images (walkthrough
stills, client logos) are descriptive, decorative ones (`aria-hidden` menu
duplicates, the repeated marquee track, posters inside labelled play controls)
are correctly empty. The 18 client logos now carry their true width as well
as height (read from each PNG), so the marquee reserves its space before they
load. Images were already compressed (largest 69 KB) and below-the-fold ones
lazy; filenames were left alone (renaming would break the case-study video
pipeline for no measurable gain).

**Internal linking.** Added only where the content supports it:
- Each case study's *Related work* section names the solution pages that cite
  it as evidence (`solutions.py`, inverted) — e.g. WasteMart → custom
  software, mobile apps, support; Trans Hex → business intelligence, system
  integration, modernisation. Tore's Foundation is cited by no solution page,
  so it gets none.
- Each article's *In practice* section names the disciplines the article
  discusses (POPIA → custom software, Microsoft Cloud; load-shedding →
  Microsoft Cloud, mobile apps; spreadsheets → custom software, business
  intelligence).
- Custom software → ManaGEM, with the fact from ManaGEM's own record: the
  system built for SBS Waterproofing was later generalised into ManaGEM.
- Already present: mobile apps → WasteMart and Sonke; UX design → Studio;
  system integration → Trans Hex; business intelligence → Trans Hex and Sonke;
  the homepage → solutions, products, case studies and contact in the page,
  and the Studio in the header menu and footer of every page.

**Performance.** Unchanged by this work and already within Google's "good"
thresholds on throttled mobile (LCP 0.7–2.0 s, measured in the launch
checklist); no third-party scripts load without consent; fonts are
self-hosted. No visual quality was traded away.

## E. Issues identified

- **Indexable duplicates (fixed).** Pages served the offline bundles, eight
  old exports and prototypes at the root (`GEMIS Studio.html`, `GEMIS
  Work.html`, `GEMIS Work v3.html`, `ManaGem.html`, `studio-standalone.html`,
  `studio-about-standalone.html`, `work-standalone.html`,
  `wastemart-driver.html`), `tools/og-card.html` and the per-person email
  signature pages, all indexable copies of real content. All are now
  `noindex` (the bundles and signatures at their generators). Consider
  deleting the eight old exports: they are not linked and not built.
- **Breadcrumb schema** on the solution pages started at "Solutions", not
  Home (fixed).
- **Duplicate/missing metadata:** none duplicated before or after; 22 titles
  over 60 characters were already fixed in the launch checklist and are now
  keyword-led; `og:locale`, Twitter title/description/image and robots tags
  were missing everywhere (fixed).
- **Broken links:** none (2,764 internal links checked).
- **`robots.txt` is ignored where it is.** Crawlers read robots.txt only at
  the host root (`sphamandla-designer.github.io/robots.txt`), which this
  repository does not control. Nothing is blocked, so nothing is lost, but the
  sitemap must be submitted in Search Console rather than discovered.
- **Domain.** `gemis.co.za` is not pointed at this site; no `CNAME` file
  exists. Until it is, `github.io` is the canonical host.
- **Pre-existing, fixed along the way:** `build-other.py` fails in a shallow
  clone (it reads old pages from git history) — documented in CLAUDE.md.

## F. Outstanding — needs access or a decision

1. **Production domain (DNS + repository settings).** To serve the site at
   `gemis.co.za`: add a `CNAME` file containing `gemis.co.za` (or
   `www.gemis.co.za`); in the registrar's DNS point the apex `A`/`AAAA` records
   at GitHub Pages' addresses (or a `www` CNAME at
   `sphamandla-designer.github.io`); set the custom domain and *Enforce HTTPS*
   in the repository's Pages settings; then change `CANON` in `seo.py` and
   `CANONICAL` in `stories.py`, rebuild, and redirect the old gemis.co.za pages
   to their new equivalents. Note the site lives under `/gemis-site/` today;
   on a custom domain it moves to the root, so every canonical changes.
2. **Google Search Console.** Add a URL-prefix property for
   `https://sphamandla-designer.github.io/gemis-site/` (or a Domain property
   once gemis.co.za points here); choose HTML-tag verification and put the
   token in `GSC_VERIFICATION` in `seo.py` — apply-seo writes it on the
   homepage. Then submit `sitemap.xml`. Indexing, mobile usability and Core
   Web Vitals field data can only be read there; none is claimed here.
3. **Dedicated ManaGEM site** (`sphamandla-designer.github.io/ManaGEM/`) is a
   separate repository this session cannot reach. Its brief (title *Job
   Management Software South Africa | ManaGEM*, H1 *Manage every job from
   enquiry to invoice in one connected system*) is ready to apply there. It
   should keep its own self-referencing canonical — it is a different
   destination from `products/managem/`, as the brief says.
4. **Business verification:** the Information Officer, company registration
   number and directors (also outstanding on the privacy and terms pages), and
   whether a Google Business Profile exists for the Cape Town address — if it
   does, add its URL to `sameAs`.
5. **External validation:** schema.org and Google's Rich Results Test are not
   reachable from the build sandbox; run the live pages through
   <https://search.google.com/test/rich-results> and
   <https://validator.schema.org> after deployment.

## G. Final validation

| Check | Result |
|---|---|
| Full rebuild (`build-home` → `build-services` → `build-pages` → `build-other` → `apply-chrome` → `apply-seo`) | passes |
| `apply-seo --check` / `apply-chrome --check` | both pass |
| `seo.py` validation (unique titles ≤ 60, unique descriptions) | passes, 30 pages |
| Per-page audit: one title, description, canonical, robots; OG + Twitter complete; `en_ZA`; share images exist; one H1 equal to seo.py; no heading skips; no duplicate schema types; `@id`s on the canonical host | passes, 30 pages |
| JSON-LD: valid JSON; type-checked against the schema.org vocabulary (`schema-dts` 1.1.5 + `tsc --strict`) | 46 blocks, 0 errors (one real finding fixed: ImageObject width/height as bare numbers) |
| Internal links (`tools/check-links.mjs`) | 2,764 checked, 0 broken |
| Accessibility (axe, serious/critical) and overflow at 360 / 620 / 900 / 1024 / 1440 / 1920 px, JS errors logged | 14 corporate pages clean, no overflow, no errors; studio pages clean apart from the header wordmark's known `mix-blend-mode` false positive (pixel-verified legible) |
| Behaviour suites (forms, consent, 404, no-JS) — corporate and studio | both pass |
| Load speed, throttled mobile (Fast 4G, 4× CPU) | home LCP 0.81 s, Custom software 0.72 s, Sonke 2.02 s — unchanged |
| Standalone bundles rebuilt | both, now `noindex` |
| Studio homepage: one H1, rotator working, with and without JavaScript | passes |
| Sitemap well-formed; 43 canonical URLs | passes |

Not done here, by instruction: deployment, merging, and any claim about
indexing or rankings.
