# -*- coding: utf-8 -*-
"""增大膨胀闭合颈部阴影，背面调暗。"""
import os
proj = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(proj, "三星堆手电筒.html")
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

old1 = "  const cDilate = threshold(blurred(cCand, 3), 0.5);"
new1 = "  const cDilate = threshold(blurred(cCand, 8), 0.4);"
assert old1 in html
html = html.replace(old1, new1, 1)

old2 = """  const backMat = new THREE.MeshStandardMaterial({
    color: 0x354a46, alphaMap: texEdge, transparent: true,
    side: THREE.FrontSide, metalness: 0.3, roughness: 0.7
  });"""
new2 = """  const backMat = new THREE.MeshStandardMaterial({
    color: 0x2e3f3d, alphaMap: texEdge, transparent: true,
    side: THREE.FrontSide, metalness: 0.25, roughness: 0.75
  });"""
assert old2 in html
html = html.replace(old2, new2, 1)

with open(p, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("颈部闭合/背面调暗完成, KB:", round(os.path.getsize(p) / 1024))
