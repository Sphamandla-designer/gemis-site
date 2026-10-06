/* ══════════════════════════════════════════════════════════════════════
   GEMIS — the gem
   One cut stone, procedural, lit like glass. Its silhouette comes from the
   favicon: a pentagon table, a decagonal girdle, a pavilion to a point.
   Built as four wedges so the same object can fracture into the four
   modules (Sales, Stock, Payroll, Projects) and lock back together.

   import { mountGem } from './gem.js'
   const gem = await mountGem(canvas, { state: 'whole', size: 1 })
   gem.setFracture(t)        // 0 = whole … 1 = fully apart (scrubbed by scroll)
   gem.setMode(i)            // which problem the shards are showing (0–3)
   gem.setState('small')     // calm, slowly turning
   gem.pause() / gem.resume()
   ══════════════════════════════════════════════════════════════════════ */
import * as THREE from './three.module.min.js';

const MODULES = ['Sales', 'Stock', 'Payroll', 'Projects'];
const SECTORS = 20;              // 4 wedges × 5 sub-sectors; the table stays a pentagon (4 samples per side)
const R_TABLE = .62, R_GIRDLE = 1, Z_TABLE = .46, Z_GIRDLE = .08, Z_CULET = -.98;

/* a point on a regular n-gon's perimeter at parameter u∈[0,1), radius r (the n-gon's circumradius) */
function ngonPoint(n, r, u, z, phase = 0) {
  const side = Math.floor(u * n), f = u * n - side;
  const a0 = phase + (side / n) * Math.PI * 2, a1 = phase + ((side + 1) / n) * Math.PI * 2;
  const x = r * (Math.cos(a0) * (1 - f) + Math.cos(a1) * f), y = r * (Math.sin(a0) * (1 - f) + Math.sin(a1) * f);
  return new THREE.Vector3(x, z, y);
}

/* the whole stone as a list of triangles, each tagged with the wedge it belongs to */
function stoneTriangles() {
  const tris = [];
  const top = new THREE.Vector3(0, Z_TABLE, 0), culet = new THREE.Vector3(0, Z_CULET, 0);
  const phase = -Math.PI / 2;   // a point of the pentagon faces the viewer, like the favicon
  for (let i = 0; i < SECTORS; i++) {
    const u0 = i / SECTORS, u1 = (i + 1) / SECTORS;
    const t0 = ngonPoint(5, R_TABLE, u0, Z_TABLE, phase), t1 = ngonPoint(5, R_TABLE, u1, Z_TABLE, phase);
    const g0 = ngonPoint(10, R_GIRDLE, u0, Z_GIRDLE, phase), g1 = ngonPoint(10, R_GIRDLE, u1, Z_GIRDLE, phase);
    const wedge = Math.floor(i / (SECTORS / 4));
    tris.push({ w: wedge, p: [top, t0, t1] });                 // table
    tris.push({ w: wedge, p: [t0, g0, g1] }, { w: wedge, p: [t0, g1, t1] });   // crown
    tris.push({ w: wedge, p: [g0, culet, g1] });               // pavilion
  }
  return tris;
}

/* each wedge's two cut faces lie in vertical planes through the axis; cap them so the glass reads solid */
function wedgeCaps(wedge) {
  const phase = -Math.PI / 2, caps = [];
  for (const edge of [0, 1]) {
    const u = ((wedge + edge) * (SECTORS / 4)) / SECTORS;
    const t = ngonPoint(5, R_TABLE, u, Z_TABLE, phase), g = ngonPoint(10, R_GIRDLE, u, Z_GIRDLE, phase);
    const top = new THREE.Vector3(0, Z_TABLE, 0), culet = new THREE.Vector3(0, Z_CULET, 0);
    // winding so the cap faces outward from the wedge
    const quad = edge === 0 ? [top, culet, g, t] : [top, t, g, culet];
    caps.push([quad[0], quad[1], quad[2]], [quad[0], quad[2], quad[3]]);
  }
  return caps;
}

function geometryFor(wedge) {
  const tris = stoneTriangles().filter((t) => t.w === wedge).map((t) => t.p).concat(wedgeCaps(wedge));
  const pos = new Float32Array(tris.length * 9);
  tris.forEach((t, i) => t.forEach((v, j) => { pos[i * 9 + j * 3] = v.x; pos[i * 9 + j * 3 + 1] = v.y; pos[i * 9 + j * 3 + 2] = v.z; }));
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  g.computeVertexNormals();   // non-indexed, so every facet is flat
  return g;
}

/* the direction a wedge drifts when the stone fractures: outward from its centre angle */
function wedgeDirection(wedge) {
  const a = -Math.PI / 2 + ((wedge + .5) / 4) * Math.PI * 2;
  return new THREE.Vector3(Math.cos(a), 0, Math.sin(a));
}

/* a soft studio: navy room, an ice panel and one warm rim — rendered once into an environment map */
function studioEnvironment(renderer) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#141a3a');
  const panel = (w, h, color, intensity, pos, lookAt) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color, side: THREE.DoubleSide }));
    m.material.color.multiplyScalar(intensity); m.position.copy(pos); m.lookAt(lookAt || new THREE.Vector3()); scene.add(m);
  };
  panel(6, 3, '#cfe0f0', 1.6, new THREE.Vector3(-4, 3, 2));      // ice key
  panel(2, 6, '#f3e9dc', 1.9, new THREE.Vector3(5, 1, -3));      // warm rim
  panel(8, 2, '#8ea9c6', .7, new THREE.Vector3(0, -4, 0));       // floor bounce
  panel(3, 3, '#ffffff', .9, new THREE.Vector3(1, 5, 4));        // top light
  const pmrem = new THREE.PMREMGenerator(renderer);
  const env = pmrem.fromScene(scene, .04).texture;
  pmrem.dispose();
  return env;
}

export async function mountGem(canvas, opts = {}) {
  const state = { mode: opts.state || 'whole', fracture: 0, problem: 0, missing: opts.missing ?? -1, t: 0, paused: false, pointer: { x: 0, y: 0 }, tilt: { x: 0, y: 0 } };
  const dpr = Math.min(window.devicePixelRatio || 1, opts.maxDpr ?? (window.innerWidth < 900 ? 1.5 : 2));
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(dpr);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, 1, .1, 50);
  camera.position.set(0, .35, 5.2); camera.lookAt(0, -.1, 0);
  // the lite build skips the pre-filtered environment (the expensive step on a phone) and lights the stone directly
  if (!opts.lite) scene.environment = studioEnvironment(renderer);
  else scene.add(new THREE.HemisphereLight('#f3e9dc', '#1a2c50', 1.4));

  const key = new THREE.DirectionalLight('#cfe0f0', 1.2); key.position.set(-3, 4, 3); scene.add(key);
  const rim = new THREE.DirectionalLight('#f3e9dc', 1.6); rim.position.set(4, 1.5, -2); scene.add(rim);
  scene.add(new THREE.AmbientLight('#8ea9c6', .25));

  // lite: no transmission pass (phones, the small gem) — the same stone, lit the same, without the refraction
  const material = opts.lite
    ? new THREE.MeshStandardMaterial({ color: '#c9dbec', metalness: .15, roughness: .32, transparent: true, opacity: .96, flatShading: true, side: THREE.FrontSide })
    : new THREE.MeshPhysicalMaterial({
    color: '#e6eff8', metalness: 0, roughness: .12, transmission: .88, ior: 2.0, thickness: 1.6,
    attenuationColor: new THREE.Color('#9fbfdc'), attenuationDistance: 2.2,
    specularIntensity: 1, envMapIntensity: 1.7, clearcoat: .4, clearcoatRoughness: .1, dispersion: .3,
    flatShading: true, side: THREE.FrontSide,
  });
  const dimMaterial = material.clone(); dimMaterial.color.set('#8a9099'); dimMaterial.roughness = .6; if (!opts.lite) { dimMaterial.transmission = .25; dimMaterial.attenuationColor.set('#5f6b7a'); }
  const outlineMaterial = new THREE.MeshBasicMaterial({ color: '#cfe0f0', wireframe: true, transparent: true, opacity: .55 });

  const stone = new THREE.Group();
  // whole: one seamless mesh of every facet; fractured: the four wedges, capped
  const whole = new THREE.Mesh(wholeGeometry(), material);
  stone.add(whole);
  const wedges = MODULES.map((name, i) => {
    const mesh = new THREE.Mesh(geometryFor(i), material);
    mesh.userData = { name, dir: wedgeDirection(i), home: new THREE.Vector3(), i };
    mesh.visible = false;
    stone.add(mesh); return mesh;
  });
  // fine facet lines over the whole stone, faint
  const edges = new THREE.LineSegments(new THREE.EdgesGeometry(whole.geometry, 8), new THREE.LineBasicMaterial({ color: '#eaf2fa', transparent: true, opacity: .22 }));
  stone.add(edges);
  scene.add(stone);

  const size = opts.size ?? 1;
  stone.scale.setScalar(size);

  function resize() {
    const w = canvas.clientWidth || 1, h = canvas.clientHeight || 1;
    renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
  }
  resize();
  const ro = new ResizeObserver(resize); ro.observe(canvas);

  if (opts.pointer !== false && matchMedia('(hover: hover)').matches) {
    window.addEventListener('pointermove', (e) => { state.pointer.x = (e.clientX / window.innerWidth - .5) * 2; state.pointer.y = (e.clientY / window.innerHeight - .5) * 2; }, { passive: true });
  }

  let visible = true;
  const io = new IntersectionObserver((es) => { visible = es[0].isIntersecting; }, { threshold: 0 });
  io.observe(canvas);
  document.addEventListener('visibilitychange', () => { state.paused = document.hidden; });

  let last = performance.now();
  function frame() {
    state.raf = requestAnimationFrame(frame);
    const now = performance.now(); const dt = Math.min((now - last) / 1000, .05); last = now;
    if (state.paused || !visible) return;
    state.t += dt;
    const turn = state.mode === 'small' ? .18 : .32;           // the small, steady gem turns slower
    const base = state.t * turn;
    state.tilt.x += ((state.pointer.y * .12) - state.tilt.x) * .06;
    state.tilt.y += ((state.pointer.x * .18) - state.tilt.y) * .06;
    stone.rotation.set(.18 + state.tilt.x, base + state.tilt.y, 0);
    // a slow breath so the caustic highlight walks across the facets
    rim.position.set(4 * Math.cos(state.t * .3), 1.5 + Math.sin(state.t * .2), -2 + 2 * Math.sin(state.t * .3));
    // fracture: the four wedges drift along their own directions; each problem has its own behaviour
    const f = state.fracture;
    whole.visible = f < .002 && state.missing < 0; edges.visible = whole.visible;
    wedges.forEach((m, i) => {
      m.visible = !whole.visible && i !== state.missing;   // the 404: one facet never arrived
      const d = m.userData.dir;
      const spread = .55 * f;
      m.position.set(d.x * spread, (i % 2 ? 1 : -1) * .08 * f, d.z * spread);
      m.rotation.set((i % 2 ? .22 : -.14) * f, 0, (i < 2 ? .18 : -.18) * f);
      let mat = material;
      if (f > .45 && state.problem === 2 && i === 2) mat = dimMaterial;          // legacy: one shard greys
      if (f > .45 && state.problem === 3 && i === 3) mat = outlineMaterial;      // blind spot: one you cannot see into
      if (m.material !== mat) m.material = mat;
    });
    renderer.render(scene, camera);
  }
  frame();

  return {
    scene, camera, renderer, stone, wedges, material,
    setFracture(t) { state.fracture = Math.max(0, Math.min(1, t)); },
    setProblem(i) { state.problem = i; },
    setMissing(i) { state.missing = i; },
    setState(mode) { state.mode = mode; if (mode === 'whole' || mode === 'small') state.fracture = 0; },
    pause() { state.paused = true; }, resume() { state.paused = false; },
    /* a still of the current state for the reduced-motion fallback */
    snapshot() { renderer.render(scene, camera); return canvas.toDataURL('image/png'); },
    /* for the fallback renderer: jump straight to a state and render once */
    renderState(mode, fracture = 0, problem = 0, rotation = .9) {
      state.mode = mode; state.fracture = fracture; state.problem = problem; state.t = rotation / .32;
      const p = state.paused, v = visible; state.paused = false; visible = true;
      cancelAnimationFrame(state.raf); last = performance.now(); frame();
      state.paused = p; visible = v;
    },
    dispose() { cancelAnimationFrame(state.raf); ro.disconnect(); io.disconnect(); renderer.dispose(); },
  };
}

function wholeGeometry() {
  const tris = stoneTriangles().map((t) => t.p);
  const pos = new Float32Array(tris.length * 9);
  tris.forEach((t, i) => t.forEach((v, j) => { pos[i * 9 + j * 3] = v.x; pos[i * 9 + j * 3 + 1] = v.y; pos[i * 9 + j * 3 + 2] = v.z; }));
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.computeVertexNormals(); return g;
}

function mergeWedges(wedges) {
  let total = 0; wedges.forEach((w) => { total += w.geometry.attributes.position.count; });
  const pos = new Float32Array(total * 3); let o = 0;
  wedges.forEach((w) => { pos.set(w.geometry.attributes.position.array, o); o += w.geometry.attributes.position.array.length; });
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); return g;
}

export { MODULES };
