#!/usr/bin/env node
/**
 * Go-live gate.
 *
 * Scans every .html file for data-tbc markers — the unconfirmed facts listed in
 * OPEN_ITEMS.md — and prints each one with the file it sits in. Exits 1 while any
 * remain, so the branch cannot merge to main with placeholders on it.
 *
 * No dependencies. Run from the repository root: node scripts/check-tbc.mjs
 */
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';

const ROOT = process.cwd();
const SKIP = new Set(['node_modules', '.git', '_project', 'qa']);

/** Every .html file in the repo, minus generated bundles and vendored uploads. */
function htmlFiles(dir) {
  const out = [];
  for (const entry of readdirSync(dir)) {
    if (SKIP.has(entry)) continue;
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) { out.push(...htmlFiles(full)); continue; }
    if (!entry.endsWith('.html')) continue;
    // standalone bundles are generated from the pages already scanned
    if (entry.includes('standalone')) continue;
    out.push(full);
  }
  return out;
}

const found = new Map();   // id -> Set of files
for (const file of htmlFiles(ROOT)) {
  const html = readFileSync(file, 'utf8');
  for (const m of html.matchAll(/data-tbc="([^"]+)"/g)) {
    const id = m[1];
    if (!found.has(id)) found.set(id, new Set());
    found.get(id).add(relative(ROOT, file));
  }
}

if (found.size === 0) {
  console.log('check-tbc: no placeholders left. Safe to merge.');
  process.exit(0);
}

const ids = [...found.keys()].sort();
console.log(`check-tbc: ${ids.length} unconfirmed item${ids.length === 1 ? '' : 's'} still on the branch.\n`);
for (const id of ids) {
  const files = [...found.get(id)].sort();
  console.log(`  ${id}`);
  for (const f of files) console.log(`      ${f}`);
}
console.log('\nEach id is listed in OPEN_ITEMS.md with what is needed and who supplies it.');
console.log('This branch must not merge to main while this check fails.');
process.exit(1);
