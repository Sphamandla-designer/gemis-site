# Solutions section — implementation report

Brief: "GEMIS Solutions Architecture — Full Website Implementation Brief".
Status: implemented and tested on branch `claude/awesome-albattani-a8q6hu`, committed
locally. **Not pushed, merged or deployed**, as the brief requires.

## Pages changed

| Page | What changed |
|---|---|
| `solutions/` | Rebuilt: hero with a nine-into-one drawing, the numbered directory (what each discipline is for, and when to choose it), "How the disciplines work together" (an illustrative six-stage track), evidence from three projects with the disciplines each shows, "Start from the problem" (seven pathways), an approved quotation, a centred closing enquiry. |
| `solutions/<service>/` ×9 | Rebuilt on a shared framework with a per-page sequence: hero (breadcrumb, label + headline, copy, CTAs, a drawing for that service), the situation, deliverables, the engagement, evidence, related services, FAQs, a service-specific closing enquiry. Page-specific modules: comparison tables (SaaS, modernisation), kinds of system (integration), relationship timeline (support), quotation (custom software). |
| every page | Hero titles: a missing space where the two-line break is dropped under 620px ("Nine disciplines.One…") is fixed site-wide. The navigation's Solutions drop-down carries the revised one-liners. |
| `contact.html` (via `site.js`) | `contact.html?service=<slug>` pre-selects the closest enquiry topic and starts the notes with "About: <service>". Without the parameter nothing changes. |
| `index.html` (via `home.js`) | The "Discover the complete collection…" statement never fades below 60 % opacity, so it passes 3:1 at every scroll position (it measured 2.2:1). |

## Shared components (`scripts/build-solutions.py`)

`hero`, `problem`, `deliver`, `approach` (four styles: **track** — a numbered line that
draws on reveal; **columns** — the stage ledger, columns matched to the step count;
**frames** — cards of increasing fidelity; **loop** — a cycle with a return line),
`compare` (an accessible table that stacks on phones), `kinds`, `timeline`,
`evidence` (still, why it is relevant here, GEMIS's role, status, Read / Play),
`quote`, `related` (each with the reason it connects), `faq` (`<details>` with matching
`FAQPage` data), `cta`. Grounds are assigned in sequence so two washes never touch.

Content is data: `scripts/solutions.py` holds the directory, pathways and each page's
copy and section order; `scripts/services.py` keeps only slug, name and the navigation
line. The previous long copy, capability lists and FAQs were removed from it.

## Service-specific visual concepts (hero drawings)

| Service | Drawing |
|---|---|
| Directory | Nine labelled disciplines converging into one accountable team |
| Custom software | Spreadsheet, email, apps and paper converging into one system (enquiry → invoice) |
| Microsoft Cloud | Applications, data, identity and Azure as layers, with backup & recovery alongside |
| Enterprise SaaS | Three organisations, each with users, data and settings, on one shared core (labelled conceptual) |
| Mobile apps | Capture on a phone → held offline → synced to the business system |
| Business intelligence | Sources → agreed definitions → report → decision |
| System integration | Before (retyped by hand) and after (a monitored integration layer) |
| UX & system design | Observe → map → prototype → interface, increasing in fidelity |
| Modernisation | Four stages: the existing system gives way as the improved one grows |
| Support | Go-live entering a cycle of monitor, maintain, improve, support |

All drawings are conceptual, carry an accessible label, contain no data or screenshots,
draw in with CSS only (no script), and are complete under reduced motion. They are
hidden below 560px, where every word they carry is already in the page text.

Evidence imagery is real: stills from GEMIS's own case-study videos, captioned
"From the case study video", each opening its video in the existing overlay.

## Evidence and content issues resolved

Recorded in full in `docs/SOLUTIONS-EVIDENCE.md`. In short:

- Removed: "thousands of users", the six unverified SaaS sectors, "zero-disruption",
  rehearsed recovery plans, measured training/support reductions, ManaGEM's
  architecture, "both platforms from one codebase", and other unsourced guarantees.
- Qualified: data hosting (Azure has South African regions; chosen per system), code
  ownership (set out per agreement), real-time reporting (refresh agreed per source),
  downtime (identified and agreed, not promised away), managed-service and support terms.
- Corrected evidence: Trans Hex and Sonke are no longer shown as cloud projects (their
  records list no Azure), and neither is presented as Power BI work. Cloud evidence is
  SBS and HomeAssist, whose records list Azure. Each evidence module states why it is
  relevant on that page, and notes where the record is silent.

## Claims still requiring GEMIS approval

See "Still needing GEMIS approval" in `docs/SOLUTIONS-EVIDENCE.md`: the wording of
items marked **Approve**, chiefly the enterprise SaaS capability list, managed Azure
environments as an ongoing service, support for systems built by others, and the
"within two working days" reply already used site-wide.

## Tests performed

| Check | Result |
|---|---|
| Internal links, every page at any depth (`node tools/check-links.mjs`) | 2,059 checked, 0 broken |
| axe (WCAG 2.0–2.2 A/AA) on all 29 non-redirect pages, reveals forced in | 0 violations after the home statement fix |
| Width sweep, 10 Solutions pages × 320, 360, 390, 620, 768, 900, 1024, 1280, 1440, 1920 | No overflow, no clipped titles, no off-screen text, touch targets ≥ 24px, no JS errors |
| Site-wide layout sweep, 14 pages × 4 widths; reduced motion; no-JS | 0 problems |
| Functional sweep (filters, overlays, stage tabs, nav, tab order) | Pass |
| Metadata | 10 unique titles, 10 unique descriptions, canonicals correct, no noindex |
| Structured data | BreadcrumbList + Service + FAQPage on each service page; FAQPage matches visible questions and answers exactly on 10/10 |
| FAQ keyboard use; evidence video; contact pre-fill | Pass |
| Every evidence still loads; one h1 per page; no duplicate ids; no failed requests | Pass on all 10 |
| JavaScript off / reduced motion | All content visible; drawings complete; nothing hidden |
| `apply-chrome.py --check` | Clean |
| Standalone bundle rebuilt | 19.6 MB, 29 pages |

Note on earlier rounds: the axe script takes its page list as arguments and had been
run without any in recent rounds, so those runs tested nothing. This round ran it
across every page; it found and fixed the one failure above.

## Outstanding

- `check-tbc` still reports the two long-standing blocking items (`timeline-order`,
  `managem-trial-url`), unrelated to this work.
- The branch is committed locally only. The cloud container is temporary, so the work
  should be pushed (or merged) once reviewed, or it can be lost.
