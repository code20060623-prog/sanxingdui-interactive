# -*- coding: utf-8 -*-
"""完整重做掩膜：膨胀闭合 + flood fill 实心 + 软边缘；正背面对齐，背面调暗。"""
import os
proj = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(proj, "三星堆手电筒.html")
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

# 替换 solidMask 与 buildRelicGroup（从 solidMask 注释到 initThree）
si = html.find("/* flood fill：")
if si == -1:
    si = html.find("function solidMask")
ei = html.find("function initThree()")
assert si != -1 and ei != -1

new_func = r"""/* 在二值掩膜上 flood fill 外部（从边缘），返回实心掩膜 Uint8(1=器物) */
function floodFillSolid(bin, iw, ih) {
  const outside = new Uint8Array(iw * ih);
  const stack = [];
  function pushXY(x, y) {
    if (x < 0 || x >= iw || y < 0 || y >= ih) return;
    const q = y * iw + x;
    if (bin[q] === 0 && outside[q] === 0) { outside[q] = 1; stack.push(q); }
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
/* 从文物图构建带轻微厚度的青铜器物：实心掩膜 + 正面贴图浮雕 + 纯色后脑勺 */
function buildRelicGroup(img) {
  const base = 0.03, reliefAmt = 0.05;
  const iw = img.naturalWidth, ih = img.naturalHeight;
  const cColor = document.createElement('canvas');
  cColor.width = iw; cColor.height = ih;
  const xColor = cColor.getContext('2d');
  xColor.drawImage(img, 0, 0);
  const id = xColor.getImageData(0, 0, iw, ih).data;
  // 原始二值掩膜（亮度）
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
  // 膨胀（3px 模糊 + 阈值），闭合边缘缝隙
  const cCand = toCanvas(cand);
  const cDilate = threshold(blurred(cCand, 3), 0.5);
  const dilateBin = new Uint8Array(iw * ih);
  const dd = cDilate.getContext('2d').getImageData(0,0,iw,ih).data;
  for (let q = 0; q < iw * ih; q++) dilateBin[q] = dd[q*4] >= 128 ? 1 : 0;
  // flood fill 实心
  const solid = floodFillSolid(dilateBin, iw, ih);
  const cSolid = toCanvas(solid);
  // 软边缘（1.5px）
  const cEdge = blurred(cSolid, 1.5);
  // 浮雕掩膜（亮度，4px）
  const relBin = new Uint8Array(iw * ih);
  for (let q = 0; q < iw * ih; q++) {
    const ci = q * 4;
    const lum = (id[ci]*0.299 + id[ci+1]*0.587 + id[ci+2]*0.114) / 255;
    relBin[q] = clamp((lum - 0.1) / 0.5, 0, 1) * solid[q];
  }
  const cRelB = blurred(toCanvas(relBin), 4);
  const edgeD = cEdge.getContext('2d').getImageData(0,0,iw,ih).data;
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
    const m = edgeD[ci] / 255;
    const rm = relD[ci] / 255;
    pF.setZ(i, m * base + rm * reliefAmt);
    pB.setZ(i, m * base);
  }
  gF.computeVertexNormals();
  gB.computeVertexNormals();
  const texColor = new THREE.CanvasTexture(cColor);
  texColor.encoding = THREE.sRGBEncoding;
  texColor.anisotropy = 4;
  const texEdge = new THREE.CanvasTexture(cEdge);
  const frontMat = new THREE.MeshStandardMaterial({
    map: texColor, alphaMap: texEdge, transparent: true,
    side: THREE.FrontSide, metalness: 0.5, roughness: 0.45
  });
  const backMat = new THREE.MeshStandardMaterial({
    color: 0x354a46, alphaMap: texEdge, transparent: true,
    side: THREE.FrontSide, metalness: 0.3, roughness: 0.7
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
print("掩膜流水线重做完成, KB:", round(os.path.getsize(p) / 1024))
