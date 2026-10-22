# -*- coding: utf-8 -*-
"""几何平滑化：强模糊掩膜做厚度，轻微块面起伏，避免侧面锯齿与背面斑点。"""
import os
proj = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(proj, "三星堆手电筒.html")
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

si = html.find("/* 从文物图构建带厚度的青铜器物")
ei = html.find("function initThree()")
assert si != -1 and ei != -1

new_func = """/* 从文物图构建带厚度的青铜器物：平滑几何（不逐像素位移）+ 表面贴图 + 纯色后脑勺 */
function buildRelicGroup(img) {
  const thickness = 0.42, reliefAmt = 0.04;
  const iw = img.naturalWidth, ih = img.naturalHeight;
  const cColor = document.createElement('canvas');
  cColor.width = iw; cColor.height = ih;
  const xColor = cColor.getContext('2d');
  xColor.drawImage(img, 0, 0);
  const id = xColor.getImageData(0, 0, iw, ih).data;
  // 硬掩膜
  const cMask = document.createElement('canvas');
  cMask.width = iw; cMask.height = ih;
  const xMask = cMask.getContext('2d');
  const mi = xMask.createImageData(iw, ih);
  for (let q = 0; q < iw * ih; q++) {
    const ci = q * 4;
    const lum = (id[ci]*0.299 + id[ci+1]*0.587 + id[ci+2]*0.114) / 255;
    const m = clamp((lum - 0.045) / 0.04, 0, 1);
    mi.data[ci] = mi.data[ci+1] = mi.data[ci+2] = m * 255;
    mi.data[ci+3] = 255;
  }
  xMask.putImageData(mi, 0, 0);
  function blurred(px) {
    const c = document.createElement('canvas');
    c.width = iw; c.height = ih;
    const x = c.getContext('2d');
    x.filter = 'blur(' + px + 'px)';
    x.drawImage(cMask, 0, 0);
    return c;
  }
  // 软掩膜（alpha，1.5px）
  const cBlur = blurred(1.5);
  // 几何掩膜（厚度，8px，强平滑）
  const cGeo = blurred(8);
  // 浮雕掩膜（基于亮度，4px，轻微块面）
  const cRel = document.createElement('canvas');
  cRel.width = iw; cRel.height = ih;
  const xRel = cRel.getContext('2d');
  const ri = xRel.createImageData(iw, ih);
  for (let q = 0; q < iw * ih; q++) {
    const ci = q * 4;
    const lum = (id[ci]*0.299 + id[ci+1]*0.587 + id[ci+2]*0.114) / 255;
    const v = clamp((lum - 0.08) / 0.5, 0, 1) * 255;
    ri.data[ci] = ri.data[ci+1] = ri.data[ci+2] = v;
    ri.data[ci+3] = 255;
  }
  xRel.putImageData(ri, 0, 0);
  const cRelB = document.createElement('canvas');
  cRelB.width = iw; cRelB.height = ih;
  const xRelB = cRelB.getContext('2d');
  xRelB.filter = 'blur(4px)';
  xRelB.drawImage(cRel, 0, 0);

  const alphaD = cBlur.getContext('2d').getImageData(0,0,iw,ih).data;
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
    map: texColor, alphaMap: new THREE.CanvasTexture(cBlur),
    transparent: true, side: THREE.DoubleSide,
    metalness: 0.5, roughness: 0.45
  });
  const backMat = new THREE.MeshStandardMaterial({
    color: 0x58706c, alphaMap: new THREE.CanvasTexture(cMask),
    transparent: true, side: THREE.DoubleSide,
    metalness: 0.55, roughness: 0.5
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
print("几何已平滑, KB:", round(os.path.getsize(p) / 1024))
