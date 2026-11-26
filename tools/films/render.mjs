// node render.mjs <film.html> <frames-dir> [fps] [only: t1,t2,…]  — one JPEG per frame via seek(t)
import { mkdirSync } from 'node:fs'; import { join, resolve } from 'node:path'; import { pathToFileURL } from 'node:url'; import { createRequire } from 'node:module';
const require = createRequire(import.meta.url); const { chromium } = require(process.env.PLAYWRIGHT_MODULE || '/opt/node22/lib/node_modules/playwright');
const [film, out, fpsArg, only] = process.argv.slice(2); const fps = +(fpsArg || 30);
mkdirSync(out, { recursive: true });
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
await p.goto(pathToFileURL(resolve(film)).href); await p.evaluate(() => document.fonts.ready);
await p.evaluate(() => Promise.all([...document.images].map((i) => i.decode().catch(() => {}))));
const dur = await p.evaluate(() => window.DURATION);
const times = only ? only.split(',').map(Number) : Array.from({ length: Math.round(dur * fps) }, (_, i) => i / fps);
let n = 0;
for (const t of times) { await p.evaluate((x) => window.seek(x), t); await p.screenshot({ path: join(out, only ? `t${String(t).replace('.', '_')}.jpg` : `f${String(n).padStart(5, '0')}.jpg`), type: 'jpeg', quality: only ? 80 : 93 }); n++; }
console.log('frames', n, 'duration', dur); await b.close();
