# Case-study-led redesign — Phase A audit and plan

Date: 2026-10-22 · Branch: `claude/awesome-albattani-a8q6hu` (from `main` at `2752432`)

This is the Phase Zero deliverable the redesign brief asks for: what controls
production, what the site is today, what evidence exists for every claim, how
each project is classified, and what the implementation will do. Everything
below was read from the repository; nothing was assumed from the brief alone.

---

## 1. Repository and production target

| Question | Answer |
|---|---|
| Remote | `origin` → `github.com/Sphamandla-designer/gemis-site` (the only remote) |
| Production | GitHub Pages serving `main`, at `https://sphamandla-designer.github.io/gemis-site/`. There is no `CNAME`, no custom-domain configuration and no deploy workflow in `.github/`; Pages builds `main` directly. |
| Canonical URLs | Every page carries `<link rel="canonical">` on that address; `sitemap.xml` (33 URLs) and `robots.txt` agree. `www.gemis.co.za` is the company address in the profile but is not configured anywhere in this repository. |
| Working tree | Clean at the start of this work. |
| Architecture | Static HTML, no bundler. Shared chrome applied by `scripts/apply-chrome.py`; most pages generated from Python data files (`scripts/stories.py`, `cases.py`, `services.py`) by five build scripts. One stylesheet (`assets/css/site.css`) with a "TIDY" layer at its tail where decisions now live. |
| Standalone export | `gemis-site-standalone.html` is a 17 MB review copy built by `tools/build-site-standalone.py`. It is a derivative, **not** the source. It stays in the repo as a review artefact only. |

There is no ambiguity about the deployment target.

**Shipping conflict, resolved in the brief's favour.** `CLAUDE.md` says every
piece of work ends merged and deployed. The brief says do not push, deploy or
merge without approval. This work is committed on the branch and pushed so it
survives the ephemeral session container and can be reviewed; **no pull request
is opened and nothing is merged** until the owner says so.

## 2. Page audit

| Page | Purpose / audience | Keep | Problems found | Action |
|---|---|---|---|---|
| `index.html` | Entry point, conversion | Hero photograph ground, partner line, stats (confirmed figures), client logo marquee (owner-supplied logos), stories panel (video evidence of the founding relationships), How-we-work timeline | Narrative is "who we are → trust → stories → process → testimonials → form". No featured project, no explanation of the thinking, no capability-to-evidence mapping. The "Client stories" section is **six invented testimonials** (placeholders at the owner's earlier instruction). The hero leads with the brand tagline rather than the proposition. The homepage carries a full copy of the enquiry form that also lives on Contact. | Rebuild to the brief's nine-section narrative. Remove invented testimonials (the brief's rule 1 supersedes the earlier placeholder instruction). The form lives on Contact only; the homepage closes with the enquiry invitation. |
| `work/` | Portfolio index | Hero, stats, featured ManaGEM, cards with Read/Play, filter, approach timeline, conversion band | Cards show industry and headline but not GEMIS's role, status or capabilities. | Add role, status and capability labels to every card. |
| `work/<slug>/` ×6 | Individual case studies | Hero with status, overview, challenge, approach, outcomes split delivered / verified / intended, related, tailored CTA | No walkthrough visuals beyond the video; no key-decision explanations; no statement of the discovery basis or validation. | Extend the template with optional sections: discovery basis, solution structure diagram, walkthrough stills from the case study video, key decisions, validation, client proof (hidden until approved). |
| `products/managem/` | Product story | Origin at SBS, capabilities from the video, confirmed metric | Feature list only; no walkthrough. | Add the walkthrough stills and the pipeline diagram; link both ways with the SBS case study. |
| `products/` | Products | Three products | Fine. | CTA language. |
| `solutions/`, `solutions/<slug>/` ×9 | Capabilities | Deliverables, why-it-matters rows, FAQs with FAQPage schema | Only one case study linked per page (`proof`), several pages none. | Each service page lists every relevant case study ("Where this has run"). |
| `our-story/` | Company | Founding relationships, history, milestones timeline, numbers, team | Team titles and surnames are hidden pending confirmation (facts.md). | Connect the history to the projects; keep the hidden titles hidden (the 2025 company profile in the repo carries them — see register). |
| `insights/` ×3 + index | Articles | Three articles | No links to the case studies that demonstrate the article's point. | Each article links the relevant case study. |
| `contact.html` | Enquiry | Form with validation and aria-live note; email, address | The form hands off to a pre-filled `mailto:` — it never submits anywhere and the success note is only shown after the mail client opens. The phone number is hidden (unconfirmed). | Keep the mechanism (it is the intended production behaviour of a static site — see §6) and say so on the page honestly. |
| `privacy.html`, `404.html`, `industries.html` | Legal, error, sectors | — | `industries.html` is reachable but not in the nav; it still describes "multi-company" operations. | Left as is; linked from the footer only. |
| Redirect stubs (11) | Old bookmarks | `noindex`, meta refresh | — | Unchanged. |
| `GEMIS Work.html`, `GEMIS Work v3.html`, `GEMIS Studio.html`, `ManaGem.html`, `wastemart-driver.html`, `*-standalone.html` | Loose exports and old drafts at the root | — | Not linked from the site; some carry stale claims ("payroll"). | Not part of the site; left untouched (deleting the owner's files is not in scope). |

Mobile and accessibility: every page was axe-clean at serious/critical and
overflow-free at 375–1440 on `main` before this work; the checks are re-run on
the result (see `docs/REDESIGN-REPORT.md`).

## 3. Asset audit

What is actually in the repository, inspected visually, not by filename.

| Asset | What it is | Authentic product evidence? | Use |
|---|---|---|---|
| `assets/video/case-studies/*_web.mp4` (7) + `_thumb.jpg` | The seven case study explainer videos (≈66–90 s each) with narrated transcripts recorded in `scripts/stories.py` | **Yes** — produced for GEMIS about its own systems. The interfaces shown are stylised illustrations made for the videos, not screen recordings. | Primary visual evidence. Frames are extracted to `assets/img/cases/<slug>/` (36 stills) and captioned "illustrated in the case study video", never presented as production screenshots. |
| `assets/img/proto/managem-poster.jpg`, `wastemart-poster.jpg` | Login screens of ManaGEM and the WasteMart system | Yes (real screens) | Available; low information value, not used in the new sections. |
| `assets/img/logos/clients/*` (9 clients, colour + grey) | Client logos the owner uploaded | Yes | Logo marquee (kept). |
| `assets/img/home/hero-bg.jpg` | The owner's chosen hero photograph | n/a (ground, not evidence) | Every photographic band (owner instruction, PR #83). |
| `assets/img/shots/*`, `assets/img/work/*`, `assets/img/portfolio/*`, `assets/img/menu/*` | Device mock-ups from the design studio: FINOS, RentFlow, NuraCoach, Lungelo, a ManaGEM dashboard in a laptop frame, a SmartStart and a Sonke site in laptop frames | **No** — studio renders; whether the ManaGEM dashboard pictured is the production product is not recorded. | Not used as product evidence. The studio pages keep them. |
| Root `Screenshot 2026-09-16 *.png` (28), `2026-10-01/02`, `Mockup*.png`, `FINOS Mockup.png`, `Wastemart mockup.png`, `MacBook Air*.png` | Design references from other agencies' websites, studio device mock-ups, CMaxx WiFi logos and a privacy-page screenshot | No | Not used. |
| `qa/design-refs/*.png` (7) | The owner's layout references applied in PRs #74–#81 | n/a | Already applied. |
| `Gemis Company Profile (1).pdf` (2025) | The company's own profile: founding, approach, six-stage methodology, partner model, technology, team names and roles, a portfolio with product URLs | Company statement | Source for the company-credibility copy and the evidence register below. |
| `spha product design portfolio.pdf` | The designer's personal portfolio | No | Not used. |

## 4. Content evidence register

Status key: **V** verified and approved (`scripts/facts.md`, the owner's
confirmed-facts document) · **P** present in existing content, awaiting
confirmation · **U** unsupported or contradicted · **M** missing · **R**
restricted / permission needed.

| Claim | Where | Source | Status | Action |
|---|---|---|---|---|
| Founded 2014, Cape Town (9 Tapiola Way, Edgemead) | every page, schema | facts.md ("since 2014" accepted when applied), company profile 2025 | V | Published |
| "12+ years building business systems" | home, work, our-story | arithmetic from 2014 | V | Published |
| 50+ systems delivered | home, work, our-story | facts.md: confirmed | V | Published |
| 5+ sectors | home, work, our-story | facts.md: confirmed (10+ was corrected in PR #85) | V | Published |
| ManaGEM "Month-end close: nine days to two" | products/managem | facts.md: confirmed by client | V | Published, labelled verified |
| WasteMart "six hours a week back, per depot" | work/wastemart | facts.md: confirmed by client | V | Published, labelled verified |
| About a dozen companies run on ManaGEM | home, products | facts.md: confirmed; video | V | Published |
| ManaGEM feature set: enquiry→sale with SMS/email, online quotes, deposit invoices, project profit, stock alerts, products/prices/staff | products/managem | ManaGEM video | V (video) | Published; "payroll" and "multi-company accounting" removed in PR #85 because the video does not show them |
| ManaGEM launch 2013 / redesign 2026 | — | facts.md, but contradicts the SBS narration (system from 2015) | U | Not published (PR #85). Now described as developed from the 2015 SBS system |
| SBS client since 2014, system since 2015 | home, work | facts.md confirmed; video | V | Published |
| HomeAssist client since 2014 | home, work | facts.md confirmed; video ("more than ten years") | V | Published |
| WasteMart client since 2013 | — | facts.md gives the year but does not mark it confirmed; it predates the company | U | "Client for more than ten years" (the video's wording) |
| Trans Hex 2017; Sonke 2018; Tore's 2014 | work | facts.md (Trans Hex confirmed) | V / P | Years published as given; Tore's 2014 contradicts the brief's running order → `timeline-order` blocking item stays open |
| Every capability listed on the six case studies | work/<slug> | the video transcripts, verbatim | V (video) | Published as "delivered" |
| "SBS has grown many times over" | work/sbs | video narration | P | Published with "(as stated in the case study)" |
| "A report that took weeks became available on demand" (Trans Hex) | work/trans-hex | video narration | P | Published with "(as stated in the case study)" |
| 40 countries (Sonke), 24 schools / 430+ learners (Tore's) | work | video narration | P | Published as the video states them; not turned into outcome metrics |
| Client testimonials (six, homepage) | home | invented placeholders (owner's earlier instruction) | U | **Removed** — the brief's rule 1 supersedes; replaced by the stories panel and confirmed metrics |
| Endorsement lines from Ryan Smith, Keshan Patel, Nazier Mathinus | work/<slug> | names and companies in facts.md; **no approved line** | M | Cards stay hidden (`endorsement-*` hideable items) |
| Phone number `+27 11 219 5008` | contact, home | old site only; absent from facts.md | U | Hidden (`phone-number`) |
| Microsoft Partner designation | home hero | owner instruction to keep; no designation in facts.md | P | Shown; marked under `?review=1` (`microsoft-partner-badge`) |
| Team titles and surnames (Graeme Mehl CEO, Leon Small BDM, Byron Thompson senior developer, Sebastian Vries and Vanessa Davis development) | our-story | **The 2025 company profile in the repository states them**; facts.md does not | P | Still hidden, per the owner's PR #85 instruction ("tbc unless facts.md confirms"). One line in facts.md clears it. |
| Sphamandla Xaba — UI/UX designer, head of GEMIS Studio | our-story | owner, PR #85 | V | Published |
| Company technology: Azure, Azure SQL, C#, Power BI, Bootstrap, React / React Native, Android | solutions | company profile 2025 | P (company statement) | Published as the company's stated stack, not as per-project claims |
| Methodology (understand → design → build → evolve; six stages) | home, solutions | company profile (six-stage methodology), services.py | V | Published |
| Response within two working days | contact, CTAs | existing site copy only | P | Kept (an existing commitment, not a new one); flagged here for the owner to confirm |
| ManaGEM product site | nav | profile says `www.managem.co.za`; nav links the GitHub Pages ManaGEM site at the owner's instruction (PR #73) | P | Unchanged; `managem-trial-url` blocking item stays open |
| HomeAssist Portal, WasteMart system, Tore's portal, Sonke, SmartStart URLs; "R 83+ million", "10,000 users", "award-winning" | company profile | profile only | R / P | Not published |

## 5. Project classification

| Project | Classification | GEMIS involvement documented | Status on the site | Evidence | Decision |
|---|---|---|---|---|---|
| ManaGEM | Internal product, grown from the SBS system | Yes (video, facts.md) | Live; about a dozen companies | video, confirmed metric | Featured product and the homepage feature |
| SBS Waterproofing | Client engagement, founding | Yes | Live, in daily use since 2015 | video, facts.md | Case study |
| WasteMart | Client engagement, founding | Yes | Live, more than ten years | video, confirmed metric | Case study |
| HomeAssist | Client engagement, founding | Yes | Live, more than ten years | video, profile | Case study |
| Sonke Gender Justice | Client engagement | Yes | Delivered 2018; current use not recorded | video, profile | Case study; status stated as delivered |
| Trans Hex Group | Client engagement | Yes | Delivered 2017; version two followed | video, facts.md | Case study |
| Tore's Foundation (for USB) | Client engagement | Yes | Delivered; current use not recorded | video, profile | Case study |
| SmartStart | Named in the company profile as a Moodle LMS engagement; logo supplied | Profile only | Unconfirmed | profile, logo | Logo in the marquee (owner-supplied); **not** a case study until confirmed (`entry-smartstart-status`) |
| ECD Connect | Logo supplied | None | Unconfirmed | logo | Logo only |
| SwiftMLS | Named in the company profile | Profile only | Unconfirmed | profile | Not published |
| FINOS, RentFlow, NuraCoach, Lungelo | Studio mock-ups; absent from the company profile | None | Unconfirmed | mock-ups | Not published on the corporate site (`entry-*-status` hideable items); remain on the studio pages |
| HashTopic | Named in the brief | **Nothing in the repository** | Unknown | none | Not published; recorded here |

## 6. Technical findings

- **Enquiry form.** `assets/js/site.js` validates in the page and hands off to a
  pre-filled `mailto:info@gemis.co.za`. Nothing is posted anywhere. For a static
  GitHub Pages site with no backend this is the intended production behaviour
  (confirmed by the absence of any form endpoint, key or workflow in the repo).
  The page must not claim a message was sent; it says the email client will open.
- **Routes.** Folder URLs with `index.html`; old flat URLs are meta-refresh stubs.
  GitHub Pages serves `404.html`. Nothing needs server redirects.
- **Performance.** One variable font, one stylesheet, videos `preload="none"`,
  the stories panel and overlay load MP4 only on play. The new walkthrough stills
  are 30–68 KB each, `loading="lazy"`.
- **Brand tokens.** The brief's palette (`#0F2D5E`, `#1A56A0`…) and fonts
  (Cormorant Garamond, DM Sans) are not in the repository. The repository's
  system — colour from the hero photograph, Archivo Var — was decided by the
  owner in this project's history (`IMPLEMENTATION_NOTES.md` §1, PR #71, PR #83
  "use the hero photograph as every ground"). The brief allows "a more recent,
  explicitly approved brand system" to take precedence; that is the case here,
  so **no token changes**. The decision is recorded, not silent.
- **Nav labels.** The brief's "About" / "Start a Project" are adapted to the
  site's conventions: the page is called **Our Story** (owner decision, PR #85)
  and the enquiry page is **Contact**; "Insights" is added to the primary nav.

## 7. Implementation plan (Phases B–H)

1. **Foundations.** Nav gains Insights. CTA language site-wide: *Explore our
   work*, *Read the case study*, *Discuss a project*, *Explore the solution*.
   Every enquiry CTA leads to `contact.html`. New shared components in the tail
   of `site.css` and helpers in `scripts/build-stories.py`: editorial feature,
   selected-projects grid, workflow diagram (`flow()`), capability map, decision
   cards, walkthrough rows, credibility block.
2. **Homepage** in the brief's order: proposition hero (headline "Systems your
   operation can run on — not work around.", the tagline as its support line) →
   featured case study (ManaGEM, with its SBS origin) → three selected projects
   (WasteMart, HomeAssist, Sonke: three different kinds of problem) → the
   thinking (three workflow diagrams drawn from the videos) → capabilities
   demonstrated through projects → long-term partnership proof (confirmed
   figures, client logos, the stories panel with the founding tags) → how GEMIS
   works → company credibility → enquiry invitation.
3. **Case Studies index.** Cards carry role, status and capability labels.
4. **Case study template.** Optional sections added to `story_page()` and the
   data to `scripts/cases.py`: discovery basis, system structure (diagram),
   walkthrough (video stills with captions), key decisions, validation and
   delivery, with the existing outcomes split and hidden client-proof block.
5. **Supporting pages.** Service pages list every relevant case study; ManaGEM
   gets the walkthrough and diagram; Our Story links the history to the
   projects; each article links a case study; Contact states the mechanism.
6. **QA.** axe, widths 375/768/1024/1440 (+360/620/900/1920 overflow), links,
   no-JS, reduced motion, filters, video overlay, `check-tbc`, standalone rebuild.
7. **Report** in `docs/REDESIGN-REPORT.md`.
