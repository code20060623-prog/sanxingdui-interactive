# -*- coding: utf-8 -*-
"""背面材质改为不透明硬切（alphaTest），调暗颜色，遮挡正面消除重影。"""
import os
proj = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(proj, "三星堆手电筒.html")
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

old = """  const backMat = new THREE.MeshStandardMaterial({
    color: 0x58706c, alphaMap: new THREE.CanvasTexture(cMask),
    transparent: true, side: THREE.DoubleSide,
    metalness: 0.55, roughness: 0.5
  });"""
new = """  const backMat = new THREE.MeshStandardMaterial({
    color: 0x3f5652, alphaMap: new THREE.CanvasTexture(cMask),
    alphaTest: 0.4, side: THREE.DoubleSide,
    metalness: 0.6, roughness: 0.5
  });"""
assert old in html, "背面材质锚点未找到"
html = html.replace(old, new, 1)

with open(p, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("背面材质已修复, KB:", round(os.path.getsize(p) / 1024))
