# -*- coding: utf-8 -*-
"""用 flood fill 生成实心掩膜（器物内部深色区域也算器物），消除背面洞与重影。"""
import os
proj = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(proj, "三星堆手电筒.html")
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

si = html.find("/* 从文物图构建带厚度的青铜器物")
ei = html.find("function initThree()")
assert si != -1 and ei != -1

new_func = """/* flood fill：从边缘填充外部黑底，内部深色区域（眼窝等）保留为器物，得到实心掩膜 */
function solidMask(id, iw, ih) {
  const cand = new Uint8Array(iw * ih);
  for (let q = 0; q < iw * ih; q++) {
    const ci = q * 4;
    const lum = (id[ci]*0.299 + id[ci+1]*0.587 + id[ci+2]*0.114) / 255;
    cand[q] = lum > 0.05 ? 1 : 0;
  }
  const outside = new Uint8Array(iw * ih);
  const stack = [];
  function pushXY(x, y) {
    if (x < 0 || x >= iw || y < 0 || y >= ih) return;
    const q = y * iw + x;
    if (cand[q] === 0 && outside[q] === 0) { outside[q] = 1; stack.push(q); }
  }
  for (let x = 0; x < iw; x++) { pushXY(x, 0); pushXY(x, ih - 1); }
  for (let y = 0; y < ih; y++) { pushXY(0, y); pushXY(iw - 1, y); }
  while (stack.length) {
    const q = stack.pop();
    const x = q % iw, y = (q / iw) | 0;
    pushXY(x + 1, y); pushXY(x - 1, y); pushXY(x, y + 1); pushXY(x, y - 1);
  }
  const solid = new Uint8Array(iw * ih);
  for (let q = 0; q < iw * ih; q++) solid[q] = outside[q] ? 0 : 1;
  return solid;
}
/* 从文物图构建带厚度的青铜器物：实心掩膜 + 平滑几何 + 表面贴图 + 纯色后脑勺 */
function buildRelicGroup(img) {
  const thickness = 0.42, reliefAmt = 0.04;
  const iw = img.naturalWidth, ih = img.naturalHeight;
  const cColor = document.createElement('canvas');
  cColor.width = iw; cColor.height = ih;
  const xColor = cColor.getContext('2d');
  xColor.drawImage(img, 0, 0);
  const id = xColor.getImageData(0, 0, iw, ih).data;
  // 实心掩膜
  const solid = solidMask(id, iw, ih);
  const cSolid = document.createElement('canvas');
  cSolid.width = iw; cSolid.height = ih;
  const xSolid = cSolid.getContext('2d');
  const si2 = xSolid.createImageData(iw, ih);
  for (let q = 0; q < iw * ih; q++) {
    const ci = q * 4, v = solid[q] * 255;
    si2.data[ci] = si2.data[ci+1] = si2.data[ci+2] = v;
    si2.data[ci+3] = 255;
  }
  xSolid.putImageData(si2, 0, 0);
  function blurred(src, px) {
    const c = document.createElement('canvas');
    c.width = iw; c.height = ih;
    const x = c.getContext('2d');
    x.filter = 'blur(' + px + 'px)';
    x.drawImage(src, 0, 0);
    return c;
  }
  // 边缘平滑掩膜（alpha，1.5px）
  const cEdge = blurred(cSolid, 1.5);
  // 几何厚度掩膜（8px，强平滑）
  const cGeo = blurred(cSolid, 8);
  // 轻微浮雕掩膜（基于亮度，4px）
  const cRel = document.createElement('canvas');
  cRel.width = iw; cRel.height = ih;
  const xRel = cRel.getContext('2d');
  const ri2 = xRel.createImageData(iw, ih);
  for (let q = 0; q < iw * ih; q++) {
    const ci = q * 4;
    const lum = (id[ci]*0.299 + id[ci+1]*0.587 + id[ci+2]*0.114) / 255;
    const v = clamp((lum - 0.1) / 0.5, 0, 1) * 255 * solid[q];
    ri2.data[ci] = ri2.data[ci+1] = ri2.data[ci+2] = v;
    ri2.data[ci+3] = 255;
  }
  xRel.putImageData(ri2, 0, 0);
  const cRelB = blurred(cRel, 4);
  const geoD = cGeo.getContext('2d').getImageData(0,0,iw,ih).data;
  const relD = cRelB.getContext('2d').getImageData(0,0,iw,ih).data;
  const aspect = iw / ih;
  let gw, gh;
  if (aspect >= 1) { gw = 2.2; gh = 2.2 / aspect; }
  else { gh = 2.7; gw = 2.7 * aspect; }
  const segY = 160, segX = Math.max(2, Math.round(segY * aspect));
  const gF = new THREE.PlaneGeometry(gw, gh, segX, segY);
  const gB = new THREE.PlaneGeometry(gw, gh, segX, segY);
  const pF = gF.attributes.position, pB = gB.attributes.position;
  for (let i = 0; i < pF.count; i++) {
    const nx = pF.getX(i) / gw, ny = pF.getY(i) / gh;
    const u = Math.round((nx + 0.5) * (iw - 1));
    const v = Math.round((0.5 - ny) * (ih - 1));
    const ci = (clamp(v,0,ih-1) * iw + clamp(u,0,iw-1)) * 4;
    const gm = geoD[ci] / 255;
    const rm = relD[ci] / 255;
    pF.setZ(i, gm * thickness / 2 + rm * reliefAmt);
    pB.setZ(i, gm * thickness / 2);
  }
  gF.computeVertexNormals();
  gB.computeVertexNormals();
  const texColor = new THREE.CanvasTexture(cColor);
  texColor.encoding = THREE.sRGBEncoding;
  texColor.anisotropy = 4;
  const frontMat = new THREE.MeshStandardMaterial({
    map: texColor, alphaMap: new THREE.CanvasTexture(cEdge),
    transparent: true, side: THREE.DoubleSide,
    metalness: 0.5, roughness: 0.45
  });
  const backMat = new THREE.MeshStandardMaterial({
    color: 0x3f5652, alphaMap: new THREE.CanvasTexture(cSolid),
    alphaTest: 0.4, side: THREE.DoubleSide,
    metalness: 0.6, roughness: 0.5
  });
  const front = new THREE.Mesh(gF, frontMat);
  const back = new THREE.Mesh(gB, backMat);
  back.rotation.y = Math.PI;
  const group = new THREE.Group();
  group.add(front);
  group.add(back);
  return group;
}
"""

html = html[:si] + new_func + html[ei:]
with open(p, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("实心掩膜已应用, KB:", round(os.path.getsize(p) / 1024))
