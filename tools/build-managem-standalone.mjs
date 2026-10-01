#!/usr/bin/env node
/**
 * Builds managem/managem-standalone.html: the landing page as one file.
 *   node tools/build-managem-standalone.mjs
 * Inlines managem.css and managem.js, embeds the font, the favicon and every
 * ../assets/img/managem/ screenshot as data URIs, and rewrites links to the
 * rest of the GEMIS site as absolute URLs so the file works from anywhere.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(fileURLToPath(new URL('..', import.meta.url)));
const BASE = 'https://sphamandla-designer.github.io/gemis-site/';
const b64 = (p, mime) => `data:${mime};base64,${readFileSync(join(ROOT, p)).toString('base64')}`;

let html = readFileSync(join(ROOT, 'managem/index.html'), 'utf8');
let css = readFileSync(join(ROOT, 'managem/managem.css'), 'utf8');
const js = readFileSync(join(ROOT, 'managem/managem.js'), 'utf8');

css = css.replace(/url\('\.\.\/assets\/fonts\/([^']+)'\)/g, (m, f) => `url('${b64('assets/fonts/' + f, 'font/woff2')}')`);
html = html.replace(/<link rel="icon"[^>]*>/, `<link rel="icon" type="image/svg+xml" href="${b64('assets/img/favicon.svg', 'image/svg+xml')}" />`);
html = html.replace(/  <link rel="preload" href="\.\.\/assets\/fonts\/[^\n]*\n/g, '');
html = html.replace(/<link rel="stylesheet" href="managem\.css[^"]*" \/>/, () => `<style>\n${css}\n  </style>`);
html = html.replace(/<script src="managem\.js[^"]*" defer><\/script>/, () => `<script>\n${js}\n  </script>`);
html = html.replace(/src="\.\.\/assets\/img\/managem\/([^"]+)"/g, (m, f) => `src="${b64('assets/img/managem/' + f, 'image/jpeg')}"`);
html = html.replace(/href="\.\.\/"/g, `href="${BASE}"`);
html = html.replace(/href="\.\.\/([a-z./#-]+)"/g, (m, p) => `href="${BASE}${p}"`);
html = html.replace('<!--\n    ManaGem landing page — v1 draft', '<!--\n    STANDALONE BUILD: styles, script, font, favicon and screenshots are inlined so\n    this one file can be opened or shared on its own. The editable sources are\n    managem/index.html, managem/managem.css and managem/managem.js.\n\n    ManaGem landing page — v1 draft');
if (html.includes('"../')) throw new Error('unresolved relative reference left in standalone build');

const out = join(ROOT, 'managem/managem-standalone.html');
writeFileSync(out, html);
console.log(`wrote ${out} (${Math.round(html.length / 1024)} KB)`);
