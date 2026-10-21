// Internal link graph: every href/src in every page, at any depth, must resolve
// to a file in the repository.   node tools/check-links.mjs
import fs from 'fs'; import path from 'path';
const SKIP = /studio\/src|node_modules|\/qa\/|standalone|^\.\/GEMIS |\/_project\//;
function walk(d, out = []) {
  for (const n of fs.readdirSync(d)) {
    const p = path.join(d, n);
    if (SKIP.test(p) || n === '.git') continue;
    if (fs.statSync(p).isDirectory()) walk(p, out);
    else if (n.endsWith('.html')) out.push(p);
  }
  return out;
}
let broken = 0, checked = 0;
for (const p of walk('.')) {
  const s = fs.readFileSync(p, 'utf8');
  for (const m of s.matchAll(/(?:href|src|poster)="([^"]+)"/g)) {
    const h = m[1];
    if (/^(#|mailto:|tel:|data:|https?:|\/\/)/.test(h)) continue;
    checked++;
    const file = h.split('#')[0].split('?')[0];
    if (!file) continue;
    let target = path.resolve(path.dirname(p), file);
    if (file.endsWith('/')) target = path.join(target, 'index.html');
    if (!fs.existsSync(target)) { console.log(`BROKEN  ${p} -> ${h}`); broken++; }
  }
}
console.log(`internal links checked: ${checked}, broken: ${broken}`);
process.exit(broken ? 1 : 0);
