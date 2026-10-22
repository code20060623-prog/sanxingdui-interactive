# -*- coding: utf-8 -*-
"""正面材质贴合原图（不膨胀），背面实心且调暗；几何用 solid 保持对齐。"""
import os
proj = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(proj, "三星堆手电筒.html")
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

si = html.find("/* 从文物图构建带轻微厚度的青铜器物")
ei = html.find("function initThree()")
assert si != -1 and ei != -1

new_func = r"""/* 从文物图构建带轻微厚度的青铜器物：正面贴图贴合原图，背面实心纯色后脑勺 */
function buildRelicGroup(img) {
  const base = 0.03, reliefAmt = 0.05;
  const iw = img.naturalWidth, ih = img.naturalHeight;
  const cColor = document.createElement('canvas');
  cColor.width = iw; cColor.height = ih;
  const xColor = cColor.getContext('2d');
  xColor.drawImage(img, 0, 0);
  const id = xColor.getImageData(0, 0, iw, ih).data;
  const cand = new Uint8Array(iw * ih);
  for (let q = 0; q < iw * ih; q++) {
    const ci = q * 4;
    const lum = (id[ci]*0.299 + id[ci+1]*0.587 + id[ci+2]*0.114) / 255;
    cand[q] = lum > 0.05 ? 1 : 0;
  }
  function toCanvas(bin) {
    const c = document.createElement('canvas');
    c.width = iw; c.height = ih;
    const x = c.getContext('2d');
    const im = x.createImageData(iw, ih);
    for (let q = 0; q < iw * ih; q++) {
      const ci = q * 4, v = bin[q] * 255;
      im.data[ci] = im.data[ci+1] = im.data[ci+2] = v; im.data[ci+3] = 255;
    }
    x.putImageData(im, 0, 0);
    return c;
  }
  function blurred(src, px) {
    const c = document.createElement('canvas');
    c.width = iw; c.height = ih;
    const x = c.getContext('2d');
    x.filter = 'blur(' + px + 'px)';
    x.drawImage(src, 0, 0);
    return c;
  }
  function threshold(src, t) {
    const c = document.createElement('canvas');
    c.width = iw; c.height = ih;
    const x = c.getContext('2d');
    const sd = src.getContext('2d').getImageData(0,0,iw,ih).data;
    const im = x.createImageData(iw, ih);
    for (let q = 0; q < iw * ih; q++) {
      const ci = q * 4, v = sd[ci] >= t * 255 ? 255 : 0;
      im.data[ci] = im.data[ci+1] = im.data[ci+2] = v; im.data[ci+3] = 255;
    }
    x.putImageData(im, 0, 0);
    return c;
  }
  const cCand = toCanvas(cand);
  // 正面软掩膜：贴合原图（不膨胀）
  const cCandSoft = blurred(cCand, 1.5);
  // 背面实心掩膜：强模糊填充眼窝/颈部阴影
  const cSolid = threshold(blurred(cCand, 20), 0.2);
  const cEdge = blurred(cSolid, 1.5);
  // 浮雕掩膜（亮度，4px）
  const relBin = new Uint8Array(iw * ih);
  for (let q = 0; q < iw * ih; q++) {
    const ci = q * 4;
    const lum = (id[ci]*0.299 + id[ci+1]*0.587 + id[ci+2]*0.114) / 255;
    relBin[q] = clamp((lum - 0.1) / 0.5, 0, 1) * cand[q];
  }
  const cRelB = blurred(toCanvas(relBin), 4);
  const solidD = cEdge.getContext('2d').getImageData(0,0,iw,ih).data;
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
    const sm = solidD[ci] / 255;
    const rm = relD[ci] / 255;
    pF.setZ(i, sm * base + rm * reliefAmt);
    pB.setZ(i, sm * base);
  }
  gF.computeVertexNormals();
  gB.computeVertexNormals();
  const texColor = new THREE.CanvasTexture(cColor);
  texColor.encoding = THREE.sRGBEncoding;
  texColor.anisotropy = 4;
  const frontMat = new THREE.MeshStandardMaterial({
    map: texColor, alphaMap: new THREE.CanvasTexture(cCandSoft),
    transparent: true, side: THREE.FrontSide,
    metalness: 0.5, roughness: 0.45
  });
  const backMat = new THREE.MeshStandardMaterial({
    color: 0x22302e, alphaMap: new THREE.CanvasTexture(cEdge),
    transparent: true, side: THREE.FrontSide,
    metalness: 0.15, roughness: 0.8
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
print("正面贴合/背面调暗完成, KB:", round(os.path.getsize(p) / 1024))
