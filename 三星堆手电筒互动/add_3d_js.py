# -*- coding: utf-8 -*-
"""添加 Three.js 3D 旋转展示逻辑，并改造 Detail 按钮、onHand、键盘。"""
import os
proj = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(proj, "三星堆手电筒.html")
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

# ---------- 1) 新代码块 + 改造 detailBtn ----------
old_detail = (
"detailBtn.addEventListener('click', () => {\n"
"  const open = dpanel.classList.toggle('open');\n"
"  setLabel(detailBtn, open ? '收起' : 'Detail');\n"
"});\n"
)
new_block = """/* ============================================================
   文物3D旋转展示：Three.js 青铜浮雕 + 手势/鼠标/触摸控制
   ============================================================ */
const THREE_BASES = [
  'https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js',
  'https://fastly.jsdelivr.net/npm/three@0.128.0/build/three.min.js',
  'https://gcore.jsdelivr.net/npm/three@0.128.0/build/three.min.js'
];
let threeLoading = null;
function ensureThree() {
  if (typeof THREE !== 'undefined') return Promise.resolve(true);
  if (threeLoading) return threeLoading;
  threeLoading = (async () => {
    for (const src of THREE_BASES) {
      try { await loadMpScript(src); return true; } catch (e) {}
    }
    threeLoading = null;
    return false;
  })();
  return threeLoading;
}
const view3d = document.getElementById('view3d');
const threeWrap = document.getElementById('threeWrap');
const t3dTitle = document.getElementById('t3dTitle');
const t3dFacts = document.getElementById('t3dFacts');
const btn3dBack = document.getElementById('btn3dBack');
const t3d = { renderer:null, scene:null, camera:null, group:null,
  rotY:0, rotVel:0, handSpin:0, handPresent:false, active:false,
  dragging:false, lastX:0, raf:0, clock:null };
function clamp(v,a,b){ return Math.max(a, Math.min(b,v)); }
function disposeGroup(g) {
  g.traverse(o => {
    if (o.geometry) o.geometry.dispose();
    if (o.material) {
      const ms = Array.isArray(o.material) ? o.material : [o.material];
      for (const m of ms) { if (m.map) m.map.dispose(); m.dispose(); }
    }
  });
}
/* 从文物图构建带厚度的青铜浮雕：正面浮雕 + 背面平整，边缘闭合 */
function buildRelicGroup(img) {
  const thickness = 0.14, reliefAmt = 0.16;
  const iw = img.naturalWidth, ih = img.naturalHeight;
  const canvas = document.createElement('canvas');
  canvas.width = iw; canvas.height = ih;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0);
  const id = ctx.getImageData(0, 0, iw, ih).data;
  const aspect = iw / ih;
  let gw, gh;
  if (aspect >= 1) { gw = 2.2; gh = 2.2 / aspect; }
  else { gh = 2.7; gw = 2.7 * aspect; }
  const segY = 150, segX = Math.max(2, Math.round(segY * aspect));
  const gF = new THREE.PlaneGeometry(gw, gh, segX, segY);
  const gB = new THREE.PlaneGeometry(gw, gh, segX, segY);
  const pF = gF.attributes.position, pB = gB.attributes.position;
  for (let i = 0; i < pF.count; i++) {
    const nx = pF.getX(i) / gw, ny = pF.getY(i) / gh;
    const u = Math.round((nx + 0.5) * (iw - 1));
    const v = Math.round((0.5 - ny) * (ih - 1));
    const ci = (clamp(v,0,ih-1) * iw + clamp(u,0,iw-1)) * 4;
    const lum = (id[ci]*0.299 + id[ci+1]*0.587 + id[ci+2]*0.114) / 255;
    const m = clamp((lum - 0.05) / 0.05, 0, 1);
    pF.setZ(i, m * (thickness / 2 + lum * reliefAmt));
    pB.setZ(i, m * (thickness / 2));
  }
  gF.computeVertexNormals();
  gB.computeVertexNormals();
  const tex = new THREE.CanvasTexture(canvas);
  tex.encoding = THREE.sRGBEncoding;
  tex.anisotropy = 4;
  const mat = new THREE.MeshStandardMaterial({
    map: tex, transparent: true, alphaTest: 0.1,
    side: THREE.DoubleSide, metalness: 0.55, roughness: 0.4
  });
  const front = new THREE.Mesh(gF, mat);
  const back = new THREE.Mesh(gB, mat);
  back.rotation.y = Math.PI;
  const group = new THREE.Group();
  group.add(front);
  group.add(back);
  return group;
}
function initThree() {
  const w = innerWidth, h = innerHeight;
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(w, h);
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.outputEncoding = THREE.sRGBEncoding;
  threeWrap.appendChild(renderer.domElement);
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);
  const camera = new THREE.PerspectiveCamera(36, w / h, 0.1, 100);
  camera.position.set(0, 0, 4.6);
  scene.add(new THREE.AmbientLight(0x607060, 0.55));
  const key = new THREE.DirectionalLight(0xffe6bf, 1.15);
  key.position.set(2.2, 2.4, 3); scene.add(key);
  const fill = new THREE.DirectionalLight(0x8fb0ff, 0.45);
  fill.position.set(-2.4, -1, 2); scene.add(fill);
  const rim = new THREE.DirectionalLight(0x5fe0c0, 0.6);
  rim.position.set(0, 2.5, -3.2); scene.add(rim);
  t3d.renderer = renderer; t3d.scene = scene; t3d.camera = camera;
  t3d.clock = new THREE.Clock();
}
function animate3d() {
  t3d.raf = requestAnimationFrame(animate3d);
  if (!t3d.active || !t3d.group || !t3d.renderer) return;
  const dt = Math.min(0.05, t3d.clock.getDelta());
  if (t3d.handPresent) {
    t3d.rotVel += (t3d.handSpin - t3d.rotVel) * Math.min(1, dt * 8);
    t3d.rotY += t3d.rotVel * dt;
  } else if (!t3d.dragging) {
    t3d.rotY += 0.35 * dt;
  }
  t3d.group.rotation.y = t3d.rotY;
  t3d.renderer.render(t3d.scene, t3d.camera);
}
async function open3d(i) {
  const ok = await ensureThree();
  if (!ok) { toast('3D 库加载失败，请检查网络'); return; }
  if (!t3d.renderer) initThree();
  const a = ARTIFACTS[i];
  t3dTitle.textContent = a.title.replace(/<br\\s*\\/?>/g, ' ');
  t3dFacts.innerHTML = a.facts
    .map(f => `<div class="tf-row"><span class="k">${f[0]}</span><span class="v">${f[1]}</span></div>`)
    .join('');
  const img = new Image();
  img.onload = () => {
    if (t3d.group) { t3d.scene.remove(t3d.group); disposeGroup(t3d.group); }
    t3d.group = buildRelicGroup(img);
    t3d.scene.add(t3d.group);
    t3d.rotY = 0; t3d.rotVel = 0; t3d.handSpin = 0; t3d.handPresent = false;
    t3d.active = true;
    resize3d();
    view3d.classList.add('show');
    if (!t3d.raf) animate3d();
  };
  img.onerror = () => toast('文物图加载失败');
  img.src = a.src;
}
function close3d() {
  view3d.classList.remove('show');
  t3d.active = false;
  t3d.handPresent = false;
}
function resize3d() {
  if (!t3d.renderer) return;
  t3d.camera.aspect = innerWidth / innerHeight;
  t3d.camera.updateProjectionMatrix();
  t3d.renderer.setSize(innerWidth, innerHeight);
}
window.addEventListener('resize', resize3d);
btn3dBack.addEventListener('click', close3d);
threeWrap.addEventListener('mousedown', e => { t3d.dragging = true; t3d.lastX = e.clientX; });
window.addEventListener('mousemove', e => {
  if (!t3d.dragging) return;
  const dx = e.clientX - t3d.lastX; t3d.lastX = e.clientX;
  t3d.rotY += dx * 0.01;
});
window.addEventListener('mouseup', () => { t3d.dragging = false; });
threeWrap.addEventListener('touchstart', e => {
  t3d.dragging = true; t3d.lastX = e.touches[0].clientX;
}, { passive: true });
threeWrap.addEventListener('touchmove', e => {
  if (!t3d.dragging) return;
  const x = e.touches[0].clientX;
  t3d.rotY += (x - t3d.lastX) * 0.01; t3d.lastX = x;
}, { passive: true });
threeWrap.addEventListener('touchend', () => { t3d.dragging = false; });
detailBtn.addEventListener('click', () => { open3d(curIdx); });
"""
assert old_detail in html, "detail锚点未找到"
html = html.replace(old_detail, new_block, 1)

# ---------- 2) onHand：view3d 分支 ----------
old_onhand = (
"    tx = px; ty = py;\n"
"    const now = performance.now();\n"
"    const peace = isPeace(lm);\n"
)
new_onhand = (
"    tx = px; ty = py;\n"
"    if (view3d.classList.contains('show')) {\n"
"      const dx = (px - innerWidth / 2) / (innerWidth / 2);\n"
"      t3d.handSpin = clamp(dx, -1, 1) * 2.2;\n"
"      t3d.handPresent = true;\n"
"      return;\n"
"    }\n"
"    const now = performance.now();\n"
"    const peace = isPeace(lm);\n"
)
assert old_onhand in html, "onHand锚点未找到"
html = html.replace(old_onhand, new_onhand, 1)

# ---------- 3) onHand else：handPresent 复位 ----------
old_else = (
"  } else {\n"
"    prevFist = false;\n"
"    prevPeace = false;\n"
"  }\n"
)
new_else = (
"  } else {\n"
"    prevFist = false;\n"
"    prevPeace = false;\n"
"    t3d.handPresent = false;\n"
"  }\n"
)
assert old_else in html, "else锚点未找到"
html = html.replace(old_else, new_else, 1)

# ---------- 4) 键盘：3D 视图 Escape ----------
old_key = (
"document.addEventListener('keydown', e => {\n"
"  if (!viewDetail.classList.contains('show')) return;\n"
"  if (e.key === 'ArrowLeft') prevBtn.click();\n"
"  if (e.key === 'ArrowRight') nextBtn.click();\n"
"  if (e.key === 'Escape') btnBack.click();\n"
"});\n"
)
new_key = (
"document.addEventListener('keydown', e => {\n"
"  if (view3d.classList.contains('show')) {\n"
"    if (e.key === 'Escape') close3d();\n"
"    return;\n"
"  }\n"
"  if (!viewDetail.classList.contains('show')) return;\n"
"  if (e.key === 'ArrowLeft') prevBtn.click();\n"
"  if (e.key === 'ArrowRight') nextBtn.click();\n"
"  if (e.key === 'Escape') btnBack.click();\n"
"});\n"
)
assert old_key in html, "key锚点未找到"
html = html.replace(old_key, new_key, 1)

with open(p, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("3D JS 已添加, KB:", round(os.path.getsize(p) / 1024))
