# UX review and the pass that followed (2026-11-03)

The owner asked for the look to stay and the experience to improve: flow,
content, positioning, colour use, sections. The review ran against the
UI/UX Pro Max skill installed at `.claude/skills/ui-ux-pro-max/` (query it
with `python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<terms>"
--domain ux|landing|product`), its design-system recommendation for a B2B
systems consultancy, and its quick-reference checklist.

## What the skill recommended for GEMIS

- **Pattern:** Trust & Authority + Conversion — hero (mission, credibility)
  → proof (logos, stats) → solution overview → a clear path to one action.
- **Primary action:** one, in the hero and in the bar; secondary actions
  visually subordinate.
- **Colour:** navy and grey corporate, accent for the action only — the site
  already runs on midnight navy and white, so the accent is the white pill
  on navy and the navy pill on white.
- **Checks:** body 16px minimum, line length 60–75 characters, 44px targets,
  visible focus, inline validation on blur with a focusable error summary,
  current page marked in the navigation, breadcrumbs on pages three levels
  deep, pause controls on anything that advances on its own.

## Findings and what changed

| Finding | Where | Change |
|---|---|---|
| Body copy at 14px, ledes at 14px with opacity, labels at 11px | every page | 16px body, 17px ledes, 12px labels, 15px for card copy; measure held at 56–68 characters (SITE v5 in `site.css`) |
| The hero said what GEMIS believes, not what it does or for whom | home | The copy now names the service, the market and the proof: what is built, for whom, on what, and how long the team stays. The three confirmed figures sit under the actions. |
| A second section restated the hero | home | The statement section is gone; its one true line moved into the hero copy |
| Proof arrived after a long scroll | home | The client marks follow the hero directly |
| Nothing on the home said what happens after the first conversation | home | **How we work** — the four stages from `services.py` — sits between Solutions and the case studies, with the action beside it |
| Two navy tiles adjoined (hero, statement; solutions, words) | home | The order alternates: hero · proof (white) · solutions (navy) · how we work (white) · case studies (white, hairline) · in their words (navy) · principles (white) · insights (white, hairline) · contact (navy) |
| Four names for the same action — Discuss a project, Discuss a similar challenge, Discuss ManaGEM, Send an enquiry | everywhere | One: **Book a discovery session** (the sub-nav pill says *Book a session* for width) |
| No action in the bar | chrome | A pill at the end of the navigation on every page; in the phone drawer it is the last item |
| The current page was not marked | chrome | `site.js` sets `aria-current="page"` on the matching link and marks the Solutions or Products trigger on their pages |
| The enquiry validated on submit only, with no summary | contact, industries | Validation on leaving a field; after a failed send a summary at the top lists every problem, links each to its field and takes focus |
| Story pages three levels deep had no way back but the bar | case studies | A breadcrumb in the opener strip: Case studies / the client |
| The auto-advancing stages had previous and next but no pause | home, case studies index | A pause control on both |
| Breadcrumb links were 19px tall | service and story pages | 31px |

## Checks after the pass

axe clean at serious/critical on all 29 pages; no horizontal overflow at
320–1920; 2161 internal links, 0 broken; chrome check clean; JavaScript off
and reduced motion fine; the form, the pause controls and the current-page
mark verified in the browser; the standalone bundle rebuilt.

## Left as it was, on purpose

- The owner's headline, *Systems built to last. Partners built to stay.*
- The menus' content and order (the owner's instruction), apart from the
  pill at the end.
- The nine-discipline list on the home: it is the site's own, interactive
  index of the Solutions, and tested well across widths.
