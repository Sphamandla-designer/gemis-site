# gemis-site

Two sites in one repository, served by GitHub Pages from `main` at
`https://sphamandla-designer.github.io/gemis-site/`:

- the **corporate site** — `index.html` and the other pages at the repository root
- **GEMIS Studio** — `/studio/`

## Shipping

**Every piece of work ends merged.** Do not stop at a pushed branch and wait to be
asked: commit, open the pull request, and merge it. Then confirm the Pages deploy
succeeded for the merge commit before reporting back.

```sh
gh run list --repo Sphamandla-designer/gemis-site --limit 1 \
  --json headSha,status,conclusion
```

A merged pull request cannot carry new work. If the branch's last PR is already
merged, restart the branch from the latest `main` under the same name; if it still
holds unmerged commits, rebase them onto `main` rather than discarding them.

`main` moves between sessions, sometimes mid-task. Fetch and rebase before opening
a PR, and re-run the checks on the rebased base — not just before the rebase.

## Generated files — never edit these directly

| Generated | Source | Rebuild with |
|---|---|---|
| `studio/index.html`, `studio/work.html`, `studio/about.html`, `studio/services.html`, `studio/contact.html`, `studio/assets/dc-template.js` | `studio/src/index.html`, `studio/src/work.html` | `node tools/build-studio.mjs` |
| `gemis-site-standalone.html` | the root pages, `site.css`, `site.js`, fonts, images | `python3 tools/build-site-standalone.py` |

Rebuild the standalone bundle after **any** change to a root page or to
`assets/css/site.css` or `assets/js/site.js`, or it silently goes stale.

Two traps in these builds:

- The studio build bakes a live SAST clock into every page it writes, so a rebuild
  always dirties five files with a one-line timestamp change. Restore that line in
  the files you did not otherwise touch, so the diff is only the real work.
- `build-site-standalone.py` asserts every page in its `PAGES` list links
  `site.css`. A redirect stub has inline styles instead, so adding one to `PAGES`
  fails the build. Stubs belong in the list that gets routed to the live site.

## Redirect stubs

`solutions.html`, `work.html`, `managem.html` and `brand-studio.html` are redirect
stubs, not pages —
they keep old bookmarks and search results working. They carry
`<meta name="robots" content="noindex">`, stay out of `sitemap.xml`, and stay out
of the standalone bundle's `PAGES`.

Auditing one in a sandbox reports `document-title` and `html-has-lang` falsely: the
meta-refresh fires before axe runs, so it measures the failed navigation. Re-run
against the file's own bytes with the refresh stripped.

## CSS is shared across pages — scope restyles

Several component classes are used by more than one page. Restyling one page's
instance without scoping silently changes the others:

- `.rows` / `.row` — `index.html` **and** `industries.html`
- `.chips` — `index.html`, `about.html`, `services.html`, `insights.html`
- `.strip` — six pages

The homepage service rows and the services accordion are scoped as `.rows--svc`
and `.acc` for exactly this reason. Before restyling a class, grep for which pages
carry it, then check the other pages match none of the new rules.

## Scroll reveal

`[data-reveal]` is `opacity: 0` until `site.js` adds `.is-in`; `--d` staggers it.
There is a `<noscript>` fallback that reveals everything. Anything that must be
readable without JavaScript has to work with the class never arriving — decorative
accents may stay undrawn, but content may not stay invisible.

The studio's sibling pages carry no React runtime, so `tools/build-studio.mjs`
injects the same observer as `SIBLING_JS`. A `data-reveal` added to a sibling page
without that is permanently invisible.

## Checks worth running before a PR

Chromium is at `/opt/node22/lib/node_modules/playwright`; `PLAYWRIGHT_BROWSERS_PATH`
is already set, so never run `playwright install`.

- axe across the changed pages, with reveals forced in and accordions forced open
- widths 360 / 620 / 900 / 1024 / 1440 / 1920: no horizontal overflow, no clipped
  text, no JS errors
- the internal link graph — currently 267 links, 0 broken
- JavaScript off, and reduced motion, on anything that animates

**Known pre-existing violation, not yours:** a `mailto:` link inside a paragraph on
`index.html`, `industries.html` and `insights.html` fails `link-in-text-block`
(navy on near-black, 1.23:1 against the surrounding text). Everything else is clean.

Measure contrast from rendered pixels when the mark is a stroke rather than a fill
— a `-webkit-text-stroke` numeral reads as a meaningless 1:1 from its `color`.

## Content

`CONTENT-TODO.md` lists what is provisional and what still needs a decision. The
open one that keeps mattering: the studio enquiry form at `/studio/#enquire` shows
a success state and **discards what the visitor typed**. Do not route new calls to
action into it until that is fixed.

Never invent a client, a testimonial, a statistic or a case study. Everything on
the site has to be traceable to something already in the repository.
