# -*- coding: utf-8 -*-
"""背面改为纯色青铜（不透明，遮挡正面，模拟后脑勺），增大器物厚度。"""
import os
proj = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(proj, "三星堆手电筒.html")
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

start_mark = "/* 从文物图构建带厚度的青铜浮雕"
end_mark = "function initThree()"
si = html.find(start_mark)
ei = html.find(end_mark)
assert si != -1 and ei != -1

new_func = """/* 从文物图构建带厚度的青铜器物：正面贴图浮雕 + 背面纯色青铜（后脑勺），边缘闭合 */
function buildRelicGroup(img) {
  const thickness = 0.42, reliefAmt = 0.05;
  const iw = img.naturalWidth, ih = img.naturalHeight;
  const cColor = document.createElement('canvas');
  cColor.width = iw; cColor.height = ih;
  const xColor = cColor.getContext('2d');
  xColor.drawImage(img, 0, 0);
  const id = xColor.getImageData(0, 0, iw, ih).data;
  // 掩膜：黑底白物
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
  // 软掩膜（正面，平滑边缘）
  const cBlur = document.createElement('canvas');
  cBlur.width = iw; cBlur.height = ih;
  const xBlur = cBlur.getContext('2d');
  xBlur.filter = 'blur(1.5px)';
  xBlur.drawImage(cMask, 0, 0);
  const maskData = xBlur.getImageData(0, 0, iw, ih).data;
  const hardData = xMask.getImageData(0, 0, iw, ih).data;
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
    const m = maskData[ci] / 255;
    const mh = hardData[ci] / 255;
    const lum = (id[ci]*0.299 + id[ci+1]*0.587 + id[ci+2]*0.114) / 255;
    pF.setZ(i, m * (thickness / 2 + lum * reliefAmt));
    pB.setZ(i, mh * (thickness / 2));
  }
  gF.computeVertexNormals();
  gB.computeVertexNormals();
  const texColor = new THREE.CanvasTexture(cColor);
  texColor.encoding = THREE.sRGBEncoding;
  texColor.anisotropy = 4;
  const texSoft = new THREE.CanvasTexture(cBlur);
  const texHard = new THREE.CanvasTexture(cMask);
  // 正面：贴图，平滑边缘
  const frontMat = new THREE.MeshStandardMaterial({
    map: texColor, alphaMap: texSoft, transparent: true,
    side: THREE.DoubleSide, metalness: 0.5, roughness: 0.45
  });
  // 背面：纯色青铜（后脑勺），硬掩膜不透明遮挡
  const backMat = new THREE.MeshStandardMaterial({
    color: 0x6f8a82, alphaMap: texHard, transparent: true,
    side: THREE.DoubleSide, metalness: 0.55, roughness: 0.5
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
print("背面/厚度已改进, KB:", round(os.path.getsize(p) / 1024))
