# -*- coding: utf-8 -*-
"""flood fill 抠出角色（深色背景），生成透明底 PNG，边缘羽化。"""
from PIL import Image, ImageFilter
import os, sys
sys.path.insert(0, r"D:\Doubao工作区\_pylibs")
import numpy as np
HAVE_NP = True

proj = os.path.dirname(os.path.abspath(__file__))
im = Image.open(os.path.join(proj, "assets", "hero_run.jpg")).convert("RGB")
w, h = im.size

if HAVE_NP:
    arr = np.asarray(im).astype(np.float32)
    lum = arr.sum(axis=2) / 3.0
    # 候选背景：很暗
    bg_cand = lum < 42
    # flood fill 从边缘
    from collections import deque
    outside = np.zeros((h, w), dtype=bool)
    dq = deque()
    for x in range(w):
        for y in (0, h-1):
            if bg_cand[y, x] and not outside[y, x]:
                outside[y, x] = True; dq.append((x, y))
    for y in range(h):
        for x in (0, w-1):
            if bg_cand[y, x] and not outside[y, x]:
                outside[y, x] = True; dq.append((x, y))
    while dq:
        x, y = dq.popleft()
        for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0 <= nx < w and 0 <= ny < h and bg_cand[ny,nx] and not outside[ny,nx]:
                outside[ny,nx] = True; dq.append((nx,ny))
    alpha = np.where(outside, 0, 255).astype(np.uint8)
    a_img = Image.fromarray(alpha, "L")
else:
    # 纯 PIL 回退：亮度阈值
    g = im.convert("L")
    a_img = g.point(lambda v: 0 if v < 42 else 255)

# 边缘羽化（轻微）
a_img = a_img.filter(ImageFilter.GaussianBlur(1.2))
rgba = im.convert("RGBA")
rgba.putalpha(a_img)
# 裁剪到角色包围盒
bbox = a_img.point(lambda v: 255 if v > 30 else 0).getbbox()
if bbox:
    rgba = rgba.crop(bbox)
out = os.path.join(proj, "assets", "hero.png")
rgba.save(out)
print("saved", out, rgba.size, "numpy:", HAVE_NP)
