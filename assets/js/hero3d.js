/* GEMIS — hero WebGL centerpiece: liquid-chrome torus knot */
import * as THREE from 'three';

const canvas = document.getElementById('heroCanvas');
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (canvas && !reduced) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
  camera.position.set(0, 0, 7);

  // Procedural studio environment for chrome reflections
  const env = buildStudioEnv();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(env, 0.04).texture;
  env.clear();

  const geo = new THREE.TorusKnotGeometry(1.45, 0.42, 400, 64, 2, 3);
  const mat = new THREE.MeshStandardMaterial({
    color: 0xd8d8d8,
    metalness: 1,
    roughness: 0.08,
  });
  const knot = new THREE.Mesh(geo, mat);
  scene.add(knot);

  const key = new THREE.DirectionalLight(0xffffff, 1.4);
  key.position.set(4, 6, 6);
  scene.add(key);
  const rim = new THREE.DirectionalLight(0x17e685, 2.2);
  rim.position.set(-6, -3, -4);
  scene.add(rim);
  scene.add(new THREE.AmbientLight(0xffffff, 0.25));

  // pointer parallax (lerped)
  const target = { x: 0, y: 0 };
  const eased = { x: 0, y: 0 };
  window.addEventListener('pointermove', (e) => {
    target.x = (e.clientX / window.innerWidth - 0.5) * 2;
    target.y = (e.clientY / window.innerHeight - 0.5) * 2;
  }, { passive: true });

  // scroll influence — set by main.js via a shared global
  window.__heroScroll = 0;

  function layout() {
    const w = canvas.clientWidth || window.innerWidth;
    const h = canvas.clientHeight || window.innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    const compact = w < 820;
    knot.scale.setScalar(compact ? 0.62 : 1);
    knot.position.set(compact ? 0 : 1.55, compact ? 1.15 : 0.55, 0);
  }
  layout();
  window.addEventListener('resize', layout);

  const clock = new THREE.Clock();
  let inView = true;
  new IntersectionObserver(([entry]) => { inView = entry.isIntersecting; }, { threshold: 0 })
    .observe(canvas);

  renderer.setAnimationLoop(() => {
    if (!inView) return;
    const t = clock.getElapsedTime();
    eased.x += (target.x - eased.x) * 0.045;
    eased.y += (target.y - eased.y) * 0.045;
    const s = window.__heroScroll || 0;
    knot.rotation.x = t * 0.18 + eased.y * 0.35 + s * 2.2;
    knot.rotation.y = t * 0.24 + eased.x * 0.5 + s * 1.4;
    knot.rotation.z = s * 0.6;
    knot.position.y += Math.sin(t * 0.8) * 0.0016;
    renderer.render(scene, camera);
  });

  function buildStudioEnv() {
    const s = new THREE.Scene();
    s.background = new THREE.Color(0x050505);
    const panel = (color, intensity, w, h, pos, lookAt) => {
      const m = new THREE.Mesh(
        new THREE.PlaneGeometry(w, h),
        new THREE.MeshBasicMaterial({ color, side: THREE.DoubleSide })
      );
      m.material.color.multiplyScalar(intensity);
      m.position.copy(pos);
      m.lookAt(lookAt);
      s.add(m);
      return m;
    };
    const c = new THREE.Vector3(0, 0, 0);
    panel(0xffffff, 6, 6, 2, new THREE.Vector3(0, 5, 0), c);      // top softbox
    panel(0xffffff, 2.5, 2, 5, new THREE.Vector3(-6, 0, 2), c);   // left strip
    panel(0x17e685, 3.5, 2, 6, new THREE.Vector3(6, -1, -2), c);  // emerald strip
    panel(0x8888ff, 1.2, 4, 1, new THREE.Vector3(0, -5, 3), c);   // cool floor bounce
    return s;
  }
}
