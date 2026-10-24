# Solutions — content and evidence register

Internal. Not published. Covers `/solutions/` and the nine service pages, built by
`scripts/build-solutions.py` from `scripts/solutions.py`.

## Sources

| Key | Source |
|---|---|
| CAT | The original GEMIS service catalogue: the nine service names, their one-line introductions and capability lists, carried in `scripts/services.py` since the first corporate build. GEMIS's own description of what it offers. |
| CASE | Case-study records: `scripts/stories.py` (summary, capabilities, tech, outcome) and `scripts/cases.py` (`DETAIL`: role, status, validation record / not recorded). Stills are frames of the case-study videos (`assets/img/cases/`). |
| FACTS | `scripts/facts.md` — dates, relationships, confirmed figures. |
| QUOTE | `scripts/endorsements.md` — quotations, verbatim. |
| PUB | A general, publicly verifiable fact about a third-party product. |
| METHOD | How GEMIS approaches the work. Written as approach, never as a guarantee; consistent with the site's existing approach copy (Understand · Design · Build · Evolve). |

Status: **Verified** (traceable to the source), **Approve** (GEMIS's own description or method — publishable, but GEMIS should confirm the wording), **Qualified** (rewritten to what the source supports), **Removed**.

## What changed from the previous Solutions copy

The previous service pages carried longer copy and FAQs written for an earlier build, not drawn from a source. Every one of these claims was removed or qualified:

| Previous claim | Page | Problem | Now |
|---|---|---|---|
| "Multi-tenant platforms built to serve thousands of users" | SaaS, navigation | No user count is recorded anywhere | **Removed.** "Platforms that serve many organisations from one product." |
| Six sectors listed as SaaS capabilities (property, healthcare, manufacturing, logistics, government & NGO, business operations) | SaaS | Not established as sectors GEMIS targets | **Removed.** No sector list. |
| "ManaGEM runs on exactly this foundation — a shared core with per-tenant configuration" | SaaS | ManaGEM's architecture is not documented | **Qualified.** ManaGEM shown only as GEMIS's own product used by about a dozen companies (FACTS); a note says its architecture is not described. |
| "Several of the systems in our case studies serve more than one organisation" | SaaS | Not recorded | **Removed.** |
| "For most clients [data is kept in South Africa]… we design environments in-country" | Cloud | Hosting regions of client systems not recorded | **Qualified.** Azure has South African regions (PUB); the region is chosen per system. |
| "We… monitor it and keep it patched as part of ongoing support. You see the cost and the status; we do the running." | Cloud | A service level, not recorded | **Qualified.** Who maintains the environment is agreed per engagement. |
| "a recovery plan that has actually been rehearsed"; "We migrate… so the business never has to stop" | Cloud, modernisation | Guarantees | **Qualified.** Disruption is assessed and agreed; no guarantee. |
| "Zero-disruption rollouts are the standard" / capability "Zero-disruption rollouts" | Modernisation | Guarantee | **Qualified.** "Staged rollouts… with a way back where possible"; downtime identified and agreed in advance. |
| "Who owns the system and the code? You do." | Custom software | Contractual claim | **Qualified.** Ownership, licensing and handover are set out in each agreement. |
| "Both [Android and iOS], from one codebase" | Mobile | Not recorded | **Qualified.** Decided per project during discovery. |
| "a lost phone can be cut off from the system without losing data" | Mobile | Not recorded | **Qualified.** Device protections designed per app. |
| "clear, real-time decision-making tools"; "A dashboard draws live from the systems" | BI | Real-time not substantiated | **Qualified.** Refresh schedule agreed per source; real-time not promised. Capability "Real-time monitoring" → "Monitoring". |
| Trans Hex shown as a cloud project (`SERVICE_STORIES`) | Cloud | Trans Hex's recorded tech is SAP integration · SQL · reporting — no Azure | **Removed** from Cloud. Cloud evidence is SBS and HomeAssist, whose records list Microsoft Azure. |
| Sonke shown as a cloud project | Cloud | No Azure recorded | **Removed** from Cloud. |
| Trans Hex / Sonke implied as Power BI work | BI | Tool not recorded | **Qualified.** Note on the page: neither is presented as a Power BI project. |
| "usually cuts training and support calls straight away"; "Interfaces that need less training, fewer support calls and no manual" | UX | Not measured | **Removed.** |
| "Every system we build comes with the people who built it… a partner who answers the phone" | Support | Service level | **Qualified.** Support is agreed per system; terms are in the agreement. |
| "Our founding clients have been with us since 2013 and 2014" | Support | Verified, kept | **Verified** (FACTS: WasteMart 2013, SBS 2014, HomeAssist 2014). |
| "Several of the systems we built in our first two years are still running today" | Custom software | Too broad | **Qualified** to the named, recorded relationships. |
| Directory "Six stages, no surprises… You see progress every sprint" and the six-stage timeline | Directory | Promise | **Removed.** Replaced by an illustrative "how the disciplines work together" sequence, labelled as illustrative. |

## The directory (`/solutions/`)

| Claim | Source | Status |
|---|---|---|
| Nine disciplines; their names | CAT | Verified |
| "Most engagements draw on several at once, and you deal with one team throughout" | CAT (existing directory copy) | Approve |
| Each discipline's "what it is" line | CAT intro lines, condensed | Approve |
| Each "Choose it when" line | Describes a visitor's situation, not a GEMIS claim | — |
| "How the disciplines work together" sequence | METHOD, labelled "an illustration, not a fixed sequence" | Approve |
| SBS: "connected to accounting, looked after since 2015, origin of ManaGEM" | CASE (summary, role_short, record) | Verified |
| Trans Hex: "stabilised first, automated SAP feed, report replaced weeks of compilation" | CASE | Verified |
| Sonke: "captured offline, checked and approved by role, progress and donor reporting" | CASE | Verified |
| Philippine Francke quotation | QUOTE | Verified (verbatim) |
| "We come back within two working days with a short written view" | Existing site-wide copy (Contact, home) | Approve |

## Per service page

### 01 Custom software development
| Claim | Source | Status |
|---|---|---|
| Six system types (internal management systems … enterprise applications) | CAT capability list, each explained | Verified / Approve explanations |
| Approach: map, find friction, design with users, build in stages, go live and stay | METHOD | Approve |
| SBS system from 2015: enquiries, pipeline, online quotes, deposits, profit per job, stock alerts; still runs on it | CASE | Verified |
| WasteMart quote-to-collection; "six hours a week back, per depot" | CASE + FACTS (client-confirmed) | Verified |
| HomeAssist: claims reported online or by insurers, nearest plumber, tracked to sign-off | CASE | Verified |
| SBS → accounting; HomeAssist → insurers and manufacturers | CASE capabilities | Verified |
| SBS, HomeAssist, WasteMart "more than ten years" | FACTS | Verified |
| Keshan Patel quotation | QUOTE | Verified (verbatim) |

### 02 Microsoft Cloud solutions
| Claim | Source | Status |
|---|---|---|
| Six capability areas (Azure, Azure SQL, hosting, identity, API integration, disaster recovery) | CAT | Verified / Approve explanations |
| "designs, deploys and manages… on Microsoft Azure" | CAT intro ("architect, deploy and manage") | Approve |
| Azure has South African regions | PUB | Verified |
| Cloud alone does not make a system secure or POPIA-compliant | General principle; no guarantee made | — |
| SBS, HomeAssist "built on Microsoft Azure, .NET and SQL" | CASE `tech` | Verified |
| Note: hosting arrangements are not described in the case studies | CASE (absence) | — |

### 03 Enterprise SaaS platforms
| Claim | Source | Status |
|---|---|---|
| Platform capabilities (multi-tenancy, tenant configuration, RBAC, release management, extensibility, usage insight) | Brief's capability list, framed as what GEMIS designs | **Approve** — GEMIS to confirm it offers each |
| Comparison table: custom system vs platform | Definitions, no claims about GEMIS | — |
| ManaGEM: own product, generalised from the SBS system, about a dozen companies | FACTS + CASE | Verified |
| Note: ManaGEM's architecture not described; not proof of every capability | — | — |

### 04 Mobile application development
| Claim | Source | Status |
|---|---|---|
| Six capabilities; "Real-time synchronisation" restated as "Synchronisation" | CAT | Verified / Qualified |
| Sonke: offline app, syncs with signal; officers approve records | CASE | Verified |
| HomeAssist: plumbers photograph each step in the app (SANS) | CASE | Verified |
| WasteMart: drivers confirm collection with a scan on the mobile app | CASE + video caption | Verified |
| Platform choice, device protection decided per app | METHOD | Approve |

### 05 Business intelligence & reporting
| Claim | Source | Status |
|---|---|---|
| Power BI dashboards | CAT intro | Approve |
| Power BI has mobile apps; can draw from several sources | PUB | Verified |
| Six reporting types; "Real-time monitoring" → "Monitoring" | CAT | Verified / Qualified |
| Trans Hex integrated management report; weeks → on demand; v2 forecasts and variances | CASE | Verified |
| Sonke progress against targets; donor reports from approved records | CASE | Verified |
| Note: neither case records the reporting tool | CASE (absence) | — |

### 06 System integration
| Claim | Source | Status |
|---|---|---|
| Kinds of system: accounting, ERP, CRM, payment gateways, authentication, APIs | CAT | Verified (as kinds, not named vendors) |
| Integration practices (mapping, one source per fact, supported interfaces, failure handling, monitoring, documentation) | METHOD; failure handling evidenced by Trans Hex | Approve |
| Trans Hex SAP feed: scheduled, de-duplicated, logged, failure emails | CASE | Verified |
| SBS deposit invoice into accounting | CASE | Verified |
| HomeAssist links to insurers and manufacturers | CASE | Verified |
| No compatibility guarantee; systems assessed case by case | — | — |

### 07 UX & system design
| Claim | Source | Status |
|---|---|---|
| Six capabilities (research … accessibility) | CAT | Verified / Approve explanations |
| Design and development in the same company; GEMIS Studio is GEMIS's design practice | Studio pages ("the product and interface design practice of GEM Information Systems") | Verified |
| Sonke role-specific views | CASE | Verified |
| HomeAssist designed for homeowners, plumbers and HomeAssist | CASE | Verified |
| Note: no usability-testing records, no measured results | CASE `not_recorded` | — |

### 08 Software modernisation
| Claim | Source | Status |
|---|---|---|
| Six kinds of improvement; "Zero-disruption rollouts" → "Staged rollouts" | CAT | Verified / Qualified |
| Comparison: replace vs improve in stages | General, no GEMIS claim | — |
| Trans Hex: stabilised first, SAP feed, reporting built in, v2 extended | CASE | Verified |
| SBS system extended over more than a decade, generalised into ManaGEM | CASE record | Verified |

### 09 Ongoing support & maintenance
| Claim | Source | Status |
|---|---|---|
| Six support elements | CAT | Verified / Approve explanations |
| Timeline: WasteMart 2013, SBS 2014 (system 2015), HomeAssist 2014, to today | FACTS | Verified |
| SBS, HomeAssist, WasteMart: GEMIS as long-term support partner, systems in use | CASE `role_short`, `status_short`, record | Verified |
| Support can be provided for systems others built, after review | METHOD | Approve |
| No SLA, response time, hours or contract terms stated | — | — |

## Still needing GEMIS approval

1. The wording of every **Approve** item above, in particular the enterprise SaaS capability list — confirm GEMIS offers each element.
2. That GEMIS manages Azure environments as an ongoing service (from the catalogue intro "architect, deploy and manage").
3. That GEMIS supports systems built by other providers.
4. The "within two working days" reply, already used site-wide.
5. The contact form maps each service to the closest existing enquiry topic; topics without a close match use "Not sure yet".
