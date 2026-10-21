#!/usr/bin/env node
/**
 * Go-live gate.
 *
 * Scans every .html file for data-tbc markers and sorts them into two kinds,
 * using scripts/tbc-kinds.json (generated from scripts/stories.py):
 *
 *   blocking — publishing it would be WRONG, not merely incomplete. Exit 1.
 *   hideable — publishing without it is fine. It is absent from the live build
 *              and visible only under ?review=1. Reported as a warning.
 *
 * So the branch can merge while content is still outstanding, as long as
 * nothing on the live build would be incorrect.
 *
 * No dependencies. Run from the repository root: node scripts/check-tbc.mjs
 */
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = process.cwd();
const HERE = dirname(fileURLToPath(import.meta.url));
const SKIP = new Set(['node_modules', '.git', '_project', 'qa']);

const KINDS = JSON.parse(readFileSync(join(HERE, 'tbc-kinds.json'), 'utf8'));

function htmlFiles(dir) {
  const out = [];
  for (const entry of readdirSync(dir)) {
    if (SKIP.has(entry)) continue;
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) { out.push(...htmlFiles(full)); continue; }
    if (!entry.endsWith('.html') || entry.includes('standalone')) continue;
    out.push(full);
  }
  return out;
}

const found = new Map();
for (const file of htmlFiles(ROOT)) {
  const html = readFileSync(file, 'utf8');
  for (const m of html.matchAll(/data-tbc="([^"]+)"/g)) {
    if (!found.has(m[1])) found.set(m[1], new Set());
    found.get(m[1]).add(relative(ROOT, file));
  }
}

// ids that are open but have no markup (the Then/Now blocks, for instance,
// are omitted entirely rather than rendered as a placeholder)
for (const id of Object.keys(KINDS)) if (!found.has(id)) found.set(id, new Set());

const unknown = [...found.keys()].filter((id) => !(id in KINDS));
const blocking = [...found.keys()].filter((id) => KINDS[id] === 'blocking').sort();
const hideable = [...found.keys()].filter((id) => KINDS[id] === 'hideable').sort();

const list = (ids) => ids.map((id) => {
  const files = [...found.get(id)].sort();
  return `  ${id}\n` + (files.length ? files.map((f) => `      ${f}`).join('\n')
                                     : '      (no markup — omitted from the build entirely)');
}).join('\n');

if (hideable.length) {
  console.log(`check-tbc: ${hideable.length} hideable item${hideable.length === 1 ? '' : 's'} — absent from the live build, visible under ?review=1.\n`);
  console.log(list(hideable));
  console.log('');
}

if (unknown.length) {
  console.log(`check-tbc: ${unknown.length} marker(s) not classified in scripts/stories.py:\n`);
  console.log(list(unknown));
  console.log('\nClassify each as blocking or hideable before merging.');
  process.exit(1);
}

if (blocking.length) {
  console.log(`check-tbc: ${blocking.length} BLOCKING item${blocking.length === 1 ? '' : 's'} — these would be wrong, not just missing.\n`);
  console.log(list(blocking));
  console.log('\nEach is listed in OPEN_ITEMS.md. This branch must not merge while this fails.');
  process.exit(1);
}

console.log('check-tbc: nothing blocking. Safe to merge — the live build shows only confirmed content.');
process.exit(0);
