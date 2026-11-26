/**
 * The studio case study page body — one structure for every project:
 *
 *   1 header (client · industry and service · timeline · built by · headline result)
 *   2 the problem · 3 what we found · 4 what we changed (+ screens)
 *   5 build and handoff · 6 results · 7 client quote · 8 next step
 *
 * Data comes from studio/src/cases.json; tools/build-studio.mjs calls renderCase()
 * for each record and slots the result into studio/src/case.html. A field the
 * record cannot fill renders a [data-tbc] note (hidden live, shown under
 * ?review=1) rather than anything invented.
 */

const esc = (s) => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const tbc = (text) => `<p data-tbc="case">${esc(text)}</p>`;

const KICKER = 'font-size:13px;font-weight:600;letter-spacing:0.04em;color:#ff7a12;text-transform:uppercase';          // on #16161a: 5.9:1
const KICKER_L = 'font-size:13px;font-weight:600;letter-spacing:0.04em;color:#a84a00;text-transform:uppercase';        // on #eef0f3: 5.0:1
const H2_DARK = 'margin:20px 0 0;font-size:clamp(40px,4.5vw,76px);line-height:0.95;letter-spacing:-0.045em;font-weight:600;color:#f5f6f8';
const H2_LIGHT = 'margin:20px 0 0;font-size:clamp(40px,4.5vw,76px);line-height:0.95;letter-spacing:-0.045em;font-weight:600;color:#16161a';
const LEDE_DARK = 'margin:0;max-width:380px;font-size:17px;line-height:1.4;color:#c9cad1;justify-self:end';
const LEDE_LIGHT = 'margin:0;max-width:380px;font-size:17px;line-height:1.4;color:#3a3b41;justify-self:end';
const LINK_DARK = "font-family:'JetBrains Mono',monospace;font-size:13px;display:flex;justify-content:space-between;gap:48px;border-bottom:2px solid #ff7a12;padding-bottom:10px;min-width:230px;color:#f5f6f8";
const LINK_LIGHT = "font-family:'JetBrains Mono',monospace;font-size:13px;display:flex;justify-content:space-between;gap:48px;border-bottom:2px solid #ff7a12;padding-bottom:10px;min-width:230px;color:#16161a";

const section = (id, label, dark, inner, pad = '120px 32px') =>
  `<section id="${id}" data-screen-label="${esc(label)}" style="position:relative;overflow:hidden;background:${dark ? '#16161a' : '#eef0f3'};color:${dark ? '#f5f6f8' : '#16161a'};padding:${pad}">
  <div style="position:relative">
${inner}
  </div>
</section>`;

const head = (num, kicker, title, lede, dark) =>
  `    <div data-m="head" style="display:grid;grid-template-columns:1fr 1fr;gap:32px;align-items:end;margin-bottom:56px">
      <div>
        <div style="${dark ? KICKER : KICKER_L}">${esc(num)} · ${esc(kicker)}</div>
        <h2 data-reveal="1" style="${dark ? H2_DARK : H2_LIGHT}">${title}</h2>
      </div>
      ${lede ? `<p data-reveal="2" style="${dark ? LEDE_DARK : LEDE_LIGHT}">${esc(lede)}</p>` : '<div></div>'}
    </div>`;

/** The case-study film (2026-11-26): the same film the corporate site plays, from
    assets/video/case-studies/. Captions are burned in; the transcript is on the
    corporate page the note links. */
const film = (c) => !c.video ? '' : section('film', 'The film', true,
  `    <div class="sc-head" style="margin-bottom:40px">
      <div><div style="${KICKER}">Watch · ${esc(c.video.length)}</div><h2 data-reveal="1" style="${H2_DARK}">The story,<br><span style="color:#ff1f7a">in a minute.</span></h2></div>
      <p data-reveal="2" style="margin:0;max-width:44ch;font-size:17px;line-height:1.5;color:#c9cad1;justify-self:end">A short film of the project, narrated and captioned. <a href="${esc(c.video.page)}" style="color:#f5f6f8;border-bottom:2px solid #ff7a12">Read the transcript on the GEMIS case study</a>.</p>
    </div>
    <video controls playsinline preload="none" poster="../assets/video/case-studies/${esc(c.video.stem)}_thumb.jpg" aria-label="${esc(c.name)}: the case-study film" style="display:block;width:100%;aspect-ratio:16/9;background:#000;border-radius:6px">
      <source src="../assets/video/case-studies/${esc(c.video.stem)}_web.webm" type="video/webm">
      <source src="../assets/video/case-studies/${esc(c.video.stem)}_web.mp4" type="video/mp4">
    </video>`).replace('<section ', '<section class="sc-dark" ');

/** The <title>: short enough not to be cut off in search results (under ~60 characters). */
export function caseTitle(c) {
  if (c.seo && c.seo.title) return c.seo.title;
  return `${c.name} case study — GEMIS® Studio`;
}

/** The title a link preview shows: room for the headline result. */
export function caseShareTitle(c) {
  if (c.seo && c.seo.title) return c.seo.title;
  return c.result ? `${c.name} — ${c.result}` : `${c.name} — a GEMIS® Studio case study`;
}

/** The meta description: the result first, then as much context as fits in the
    ~160 characters a search result shows. */
export function caseDescription(c) {
  if (c.seo && c.seo.description) return c.seo.description;
  const parts = [c.result ? `${c.name}: ${c.result}${c.resultNote ? ' (' + c.resultNote.toLowerCase() + ')' : ''}.` : `${c.name}: a GEMIS® Studio case study.`,
    `${c.industry}.`, c.service ? `Evidences the ${c.service}.` : ''].filter(Boolean);
  let out = parts[0];
  for (const p of parts.slice(1)) if ((out + ' ' + p).length <= 160) out += ' ' + p;
  return out;
}

/** The one-line result for a Work card: the headline result, or the project's own line when none is confirmed. */
export function cardResult(c) {
  return c.result || c.problem[0].split('. ')[0] + '.';
}

export function renderCase(c) {
  if (c.layout === 'showcase') return renderShowcase(c);
  const NDA = { full: 'Full — name, screens and metrics', anonymised: 'Anonymised — description in place of the name', 'results-only': 'Results only — no screens' }[c.nda] || c.nda;
  const client = c.nda === 'full' ? c.client : c.anonymised;
  const headline = c.result || c.name;

  // 1 · header ────────────────────────────────────────────────────────────
  const spec = [
    ['Client', client],
    ['Industry', c.industry],
    ['Service evidenced', c.service],
    ['Timeline', c.timeline],
    ['Built by', c.builtBy],
  ].filter(([, v]) => v).map(([k, v]) => `        <div><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join('\n');
  const headerTbc = [
    !c.service ? 'Service evidenced: not yet named.' : null,
    !c.timeline ? 'Timeline: not in the record.' : null,
    !c.builtBy ? 'Built by: not in the record (in-house team or GEMIS developers).' : null,
    !c.result ? 'Headline result: none confirmed for publication.' : null,
    `NDA level: ${NDA}${c.ndaAgreed ? ' — agreed in writing.' : ' — assumed; agree it with the client in writing before publishing.'}`,
  ].filter(Boolean).map(tbc).join('\n');
  const header = `<section id="case" data-screen-label="Case study" style="position:relative;overflow:hidden;background:#eef0f3;color:#16161a;padding:160px 32px 100px">
  <div style="position:absolute;inset:-6%;pointer-events:none;background:url(&quot;assets/heroBg.jpg&quot;) center/cover no-repeat;opacity:.12"></div>
  <div style="position:absolute;inset:0;pointer-events:none;background:linear-gradient(90deg,rgba(238,240,243,.96) 0%,rgba(238,240,243,.9) 50%,rgba(238,240,243,.3) 78%,rgba(238,240,243,0) 100%)"></div>
  <div style="position:relative">
    <nav aria-label="Breadcrumb" style="font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.04em;text-transform:uppercase;color:#6a6b73;display:flex;gap:12px;flex-wrap:wrap"><a href="work.html" style="color:#6a6b73">Work</a><span aria-hidden="true">/</span><span style="color:#16161a">${esc(c.name)}</span></nav>
    <div data-m="head" style="display:grid;grid-template-columns:1.1fr 1fr;gap:48px;align-items:end;margin-top:40px">
      <div>
        <div style="${KICKER_L}">Case study · ${esc(c.service || c.industry)}</div>
        <h1 data-reveal="1" style="margin:20px 0 0;font-size:clamp(40px,5vw,88px);line-height:0.95;letter-spacing:-0.045em;font-weight:600;color:#16161a">${esc(headline)}</h1>
        ${c.result && c.resultNote ? `<p data-reveal="2" style="margin:20px 0 0;font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.04em;text-transform:uppercase;color:#6a6b73">${esc(c.resultNote)}</p>` : ''}
      </div>
      <div data-reveal="3" style="background:rgba(255,255,255,.75);backdrop-filter:blur(8px);border:1px solid rgba(22,22,26,.25);padding:4px 28px 0">
        <dl class="cs-spec" style="margin:0;border-top:0">
${spec}
        </dl>
      </div>
    </div>
    <div style="margin-top:24px;display:grid;gap:8px">
${headerTbc}
    </div>
    <div data-reveal="1" style="margin-top:56px;aspect-ratio:16/8;overflow:hidden;border-radius:4px;background:#dcdee3"><img src="${esc(c.image)}" alt="${esc(c.imageAlt)}" decoding="async" style="width:100%;height:100%;object-fit:cover;display:block"></div>
  </div>
</section>`;

  // 2 · the problem ──────────────────────────────────────────────────────
  const problem = section('problem', 'The problem', true,
    head('02', 'The problem', 'What was going<br><span style="color:#ff1f7a">wrong.</span>', null, true)
    + `\n    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr));gap:20px clamp(32px,5vw,88px)">${c.problem.map((p) => `<p style="margin:0;font-size:clamp(18px,1.5vw,22px);line-height:1.4;letter-spacing:-0.01em;color:#f5f6f8;max-width:46ch">${esc(p)}</p>`).join('')}</div>`
    + (c.findings.length ? '' : '\n    ' + tbc('The problem in the client’s own words, and what it was costing them, is not yet in the record.')));

  // 3 · what we found ────────────────────────────────────────────────────
  const found = section('found', 'What we found', false,
    head('03', 'What we found', 'Evidence before<br><span style="color:#ff1f7a">opinion.</span>', c.findingsNote, false)
    + (c.findings.length
      ? `\n    <ol class="cs-list" style="border-bottom:1px solid #16161a">${c.findings.map((f, i) => `<li style="border-top-color:#16161a"><span>0${i + 1}</span><span>${esc(f)}</span></li>`).join('')}</ol>
    <p style="margin:24px 0 0;font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.04em;text-transform:uppercase;color:#6a6b73">Ranked by impact</p>`
      : `\n    <p style="margin:0;max-width:640px;font-size:17px;line-height:1.4;color:#3a3b41">The findings for this project are being written up with the client and will be published once approved.</p>
    ${tbc('What we found: 3–5 findings ranked by impact, from real observations, are not in the record.')}`));

  // 4 · what we changed ──────────────────────────────────────────────────
  const screens = c.screens.length ? `
    <div style="margin-top:64px">
      <div style="${KICKER};margin-bottom:24px">The screens</div>
      <div class="cs-screens">${c.screens.map((s) => `<figure><div class="frame"><span class="tag">${esc(s.label)}</span><img src="${esc(s.img)}" alt="${esc(s.caption)}" loading="lazy" decoding="async"></div><figcaption>${esc(s.caption)}</figcaption></figure>`).join('')}</div>
      ${c.screensNote ? `<p style="margin:20px 0 0;font-size:14px;line-height:1.45;color:#9a9ba3;max-width:70ch">${esc(c.screensNote)}</p>` : ''}
      ${tbc('Before screens, side by side with the after screens, are not in the record (then-now-screenshots).')}
    </div>` : '';
  const changed = section('changed', 'What we changed', true,
    head('04', 'What we changed', 'The decisions,<br><span style="color:#ff1f7a">and why.</span>', null, true)
    + (c.changes.length
      ? `\n    <div class="cs-dec">${c.changes.map((d, i) => `<div><span class="k">Decision 0${i + 1}</span><div class="d">${esc(d.decision)}</div><p class="w"><b>Why:</b> ${esc(d.why)}</p></div>`).join('')}</div>`
      : `\n    <p style="margin:0;max-width:640px;font-size:17px;line-height:1.4;color:#c9cad1">The design decisions for this project are being written up with the client and will be published once approved.</p>
    ${tbc('What we changed: 3–4 design decisions with the reason behind each are not in the record.')}`)
    + screens);

  // 5 · build and handoff ────────────────────────────────────────────────
  const build = section('build', 'Build and handoff', false,
    head('05', 'Build and handoff', 'How it reached<br><span style="color:#ff1f7a">production.</span>', null, false)
    + (c.build
      ? `\n    <p style="margin:0;max-width:760px;font-size:clamp(18px,1.5vw,22px);line-height:1.4;letter-spacing:-0.01em;color:#16161a">${esc(c.build)}</p>`
      : `\n    <p style="margin:0;max-width:640px;font-size:17px;line-height:1.4;color:#3a3b41">How the design reached production — the component spec, the handoff session and who built it — will be published once the client has approved the account.</p>
    ${tbc('Build and handoff: the component spec, the handoff session and who built it are not in the record.')}`));

  // 6 · results ──────────────────────────────────────────────────────────
  const numbers = c.resultsNumbers.length ? `\n    <div class="cs-num">${c.resultsNumbers.map((r) => `<div><div class="n">${esc(r.n)}</div><p class="l">${esc(r.l)}</p></div>`).join('')}</div>` : '';
  const qual = c.resultsQualitative.length ? `\n    <div style="margin-top:48px"><div style="${KICKER};margin-bottom:16px">What changed for the business</div><ul class="cs-plain">${c.resultsQualitative.map((q) => `<li>${esc(q)}</li>`).join('')}</ul></div>` : '';
  const designed = c.resultsDesignedFor.length ? `\n    <div style="margin-top:48px"><div style="${KICKER};margin-bottom:16px">Designed for — not yet measured</div><ul class="cs-plain">${c.resultsDesignedFor.map((q) => `<li>${esc(q)}</li>`).join('')}</ul></div>` : '';
  const notRecorded = c.resultsNotRecorded ? `\n    <p style="margin:40px 0 0;max-width:70ch;font-size:14px;line-height:1.45;color:#9a9ba3">${esc(c.resultsNotRecorded)}</p>` : '';
  const results = section('results', 'Results', true,
    head('06', 'Results', c.resultsNumbers.length ? 'Numbers first,<br><span style="color:#ff1f7a">then the rest.</span>' : 'Results are<br><span style="color:#ff1f7a">still coming in.</span>', null, true)
    + numbers + (qual || designed ? `\n    <div class="cs-two">${qual}${designed}\n    </div>` : '') + notRecorded
    + (c.resultsNumbers.length ? '' : '\n    ' + tbc('Results: numbers first, then qualitative outcomes; or what is being measured. Not in the record.')));

  // 7 · client quote ─────────────────────────────────────────────────────
  const quote = c.quote
    ? section('quote', 'In their words', false, `    <div style="${KICKER_L}">07 · In their words</div>
    <blockquote style="margin:28px 0 0"><p class="cs-quote">“${esc(c.quote.text)}”</p><footer style="margin-top:24px;font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.04em;text-transform:uppercase;color:#6a6b73">${esc(c.quote.person)}${c.quote.role ? ' · ' + esc(c.quote.role) : ''}</footer></blockquote>`, '100px 32px')
    : `<div data-tbc="quote" style="margin:0 32px">${esc('07 · Client quote: ' + (c.quoteTbc || 'none approved.'))}</div>`;

  // 8 · next step ────────────────────────────────────────────────────────
  const next = section('next', 'Next step', false,
    `    <div data-m="head" style="display:grid;grid-template-columns:1fr auto;gap:32px;align-items:center;border-top:1px solid #16161a;padding-top:32px">
      <div>
        <div style="${KICKER_L}">08 · Next step</div>
        <p style="margin:16px 0 0;font-size:clamp(22px,2vw,32px);line-height:1.2;letter-spacing:-0.03em;font-weight:600;max-width:24ch">${esc(c.cta.label)}.</p>
      </div>
      <div style="display:flex;gap:24px;flex-wrap:wrap">
        <a href="${esc(c.cta.href)}" style="${LINK_LIGHT}"><span style="text-transform:uppercase">${esc(c.service ? 'Book a teardown' : 'Book a teardown')}</span><span>→</span></a>
        <a href="work.html" style="${LINK_LIGHT.replace('#ff7a12', '#6a6b73')}"><span style="text-transform:uppercase">All projects</span><span>→</span></a>
      </div>
    </div>
    <div style="margin-top:32px;display:grid;gap:8px">${c.tbc.map(tbc).join('\n')}</div>`, '72px 32px 100px');

  return [header, film(c), problem, found, changed, build, results, quote, next].filter(Boolean).join('\n\n');
}

/* ── the showcase case study ─────────────────────────────────────────────
   For a project whose real screens are in the repository (ManaGEM, WasteMart):
   every section pairs its copy with a mockup of those screens, made by
   tools/studio-case-mocks.mjs. Sections: a split (copy | mockup), chapters
   (alternating), a wide figure, results — then the shared next step. */
const fig = (m, eager) => m ? `<figure class="sc-fig" data-reveal="2"><div class="shot"><img src="${esc(m.img)}" alt="${esc(m.alt)}" width="2000" height="1250" ${eager ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async"></div>${m.caption ? `<figcaption>${esc(m.caption)}</figcaption>` : ''}</figure>` : '';
const paras = (ps, lead) => (ps || []).map((p, i) => `<p${lead && i === 0 ? ' class="lead"' : ''}>${esc(p)}</p>`).join('');
const plus = (xs) => xs && xs.length ? `<ul>${xs.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>` : '';
const h2 = (x, dark) => `<h2 data-reveal="1" style="${dark ? H2_DARK : H2_LIGHT};max-width:18ch">${esc(x.h2)}${x.h2accent ? `<br><span style="color:#ff1f7a">${esc(x.h2accent)}</span>` : ''}</h2>`;
const kick = (x, i, dark) => `<div style="${dark ? KICKER : KICKER_L}">${String(i + 2).padStart(2, '0')} · ${esc(x.kicker)}</div>`;

function renderShowcase(c) {
  const sc = c.showcase;
  const spec = sc.spec.map(([k, v]) => `        <div><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join('\n');
  const header = `<section id="case" data-screen-label="Case study" style="position:relative;overflow:hidden;background:#eef0f3;color:#16161a;padding:150px 32px 90px">
  <div style="position:relative">
    <nav aria-label="Breadcrumb" style="font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.04em;text-transform:uppercase;color:#6a6b73;display:flex;gap:12px;flex-wrap:wrap"><a href="index.html" style="color:#6a6b73">Studio</a><span aria-hidden="true">/</span><a href="work.html" style="color:#6a6b73">Work</a><span aria-hidden="true">/</span><span style="color:#16161a">${esc(c.name)}</span></nav>
    <div data-m="head" style="display:grid;grid-template-columns:1.15fr 1fr;gap:48px;align-items:end;margin-top:40px">
      <div>
        <div style="${KICKER_L}">Case study · ${esc(c.service)}</div>
        <h1 data-reveal="1" style="margin:20px 0 0;font-size:clamp(38px,4.6vw,80px);line-height:0.97;letter-spacing:-0.045em;font-weight:600;color:#16161a">${esc(sc.h1)}</h1>
        <p data-reveal="2" style="margin:28px 0 0;max-width:58ch;font-size:clamp(17px,1.4vw,20px);line-height:1.5;color:#3a3b41">${esc(sc.intro)}</p>
      </div>
      <div data-reveal="3" style="background:rgba(255,255,255,.75);border:1px solid rgba(22,22,26,.25);padding:4px 28px 0">
        <dl class="cs-spec" style="margin:0;border-top:0">
${spec}
        </dl>
      </div>
    </div>
    <div class="sc-wide">${fig(sc.hero, true)}</div>
    ${sc.note ? `<p style="margin:20px 0 0;font-size:13px;line-height:1.5;color:#6a6b73;max-width:80ch">${esc(sc.note)}</p>` : ''}
  </div>
</section>`;

  const body = sc.sections.map((x, i) => {
    const dark = !!x.dark;
    let inner;
    if (x.type === 'split') {
      inner = `    <div class="sc-split">
      <div class="sc-copy">${kick(x, i, dark)}${h2(x, dark)}<div style="margin-top:32px">${paras(x.paras, true)}${plus(x.list)}</div></div>
      ${fig(x.mock)}
    </div>`;
    } else if (x.type === 'chapters') {
      inner = `    <div class="sc-head" style="margin-bottom:clamp(56px,7vw,100px)"><div>${kick(x, i, dark)}${h2(x, dark)}</div>${x.lead ? `<div class="sc-copy">${paras([x.lead], true)}</div>` : ''}</div>
    <div class="sc-chapters">
${x.chapters.map((ch, j) => `      <article class="sc-ch">
        <div class="sc-copy"><div class="n">${String(j + 1).padStart(2, '0')} / ${String(x.chapters.length).padStart(2, '0')}</div><h3>${esc(ch.h3)}</h3>${paras(ch.paras)}${plus(ch.list)}</div>
        ${fig(ch.mock)}
      </article>`).join('\n')}
    </div>`;
    } else if (x.type === 'results') {
      inner = `    <div class="sc-split">
      <div class="sc-copy">${kick(x, i, dark)}${h2(x, dark)}
        <div class="cs-num" style="margin-top:40px">${x.numbers.map((r) => `<div><div class="n">${esc(r.n)}</div><p class="l">${esc(r.l)}</p></div>`).join('')}</div>
        <div style="margin-top:36px">${paras(x.paras)}${plus(x.list)}</div>
        ${x.note ? `<p class="sc-note">${esc(x.note)}</p>` : ''}
      </div>
      ${fig(x.mock)}
    </div>`;
    } else { // wide
      inner = `    <div class="sc-head"><div>${kick(x, i, dark)}${h2(x, dark)}</div><div class="sc-copy">${paras(x.paras, true)}${plus(x.list)}</div></div>
    <div class="sc-wide">${fig(x.mock)}</div>`;
    }
    return section(x.id, x.label || x.kicker, dark, inner).replace('<section ', `<section class="${dark ? 'sc-dark' : 'sc-light'}" `);
  }).join('\n\n');

  const quote = `<div data-tbc="quote" style="margin:0 32px">${esc('Client quote: ' + (c.quoteTbc || 'none approved.'))}</div>`;
  const next = section('next', 'Next step', false,
    `    <div data-m="head" style="display:grid;grid-template-columns:1fr auto;gap:32px;align-items:center;border-top:1px solid #16161a;padding-top:32px">
      <div>
        <div style="${KICKER_L}">Next step</div>
        <p style="margin:16px 0 0;font-size:clamp(22px,2vw,32px);line-height:1.2;letter-spacing:-0.03em;font-weight:600;max-width:24ch">${esc(c.cta.label)}.</p>
      </div>
      <div style="display:flex;gap:24px;flex-wrap:wrap">
        <a href="${esc(c.cta.href)}" style="${LINK_LIGHT}"><span style="text-transform:uppercase">Book a teardown</span><span>→</span></a>
        <a href="work.html" style="${LINK_LIGHT.replace('#ff7a12', '#6a6b73')}"><span style="text-transform:uppercase">All projects</span><span>→</span></a>
      </div>
    </div>
    <div style="margin-top:32px;display:grid;gap:8px">${c.tbc.map(tbc).join('\n')}</div>`, '72px 32px 100px');

  // structured data: the case study as an Article, its images the mockups shown
  const BASE = 'https://sphamandla-designer.github.io/gemis-site/';
  const url = `${BASE}studio/work-${c.slug}.html`;
  const ld = {
    '@context': 'https://schema.org', '@graph': [
      { '@type': 'Article', '@id': url + '#article', headline: sc.h1, description: c.seo.description, inLanguage: 'en-ZA',
        image: [sc.hero, ...sc.sections.flatMap((x) => [x.mock, ...(x.chapters || []).map((ch) => ch.mock)])].filter(Boolean).map((m) => `${BASE}studio/${m.img}`),
        about: { '@type': c.aboutType || 'Organization', name: c.name },
        author: { '@id': BASE + '#organization' }, publisher: { '@id': BASE + '#organization' },
        mainEntityOfPage: url, keywords: c.seo.keywords },
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'GEMIS Studio', item: BASE + 'studio/' },
        { '@type': 'ListItem', position: 2, name: 'Work', item: BASE + 'studio/work.html' },
        { '@type': 'ListItem', position: 3, name: c.name, item: url }] },
      { '@type': 'Organization', '@id': BASE + '#organization', name: 'GEM Information Systems', alternateName: 'GEMIS', url: BASE },
    ] };
  const jsonld = `<script type="application/ld+json">\n${JSON.stringify(ld, null, 2).replace(/</g, '\\u003c')}\n</script>`;

  return [header, film(c), body, quote, next, jsonld].filter(Boolean).join('\n\n');
}

/** Roughly how many words the live page carries (TBC notes excluded) — for the report. */
export function caseWords(html) {
  const live = html.replace(/<[^>]*data-tbc[^>]*>[\s\S]*?<\/(p|div)>/g, '').replace(/<style[\s\S]*?<\/style>/g, '').replace(/<[^>]+>/g, ' ');
  return live.split(/\s+/).filter(Boolean).length;
}
