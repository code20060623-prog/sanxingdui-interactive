# -*- coding: utf-8 -*-
"""稳健抠图：屏障轻度闭合 + flood fill 外部 + 从中心连通域重建（保留角色，去除碎片）。"""
import sys, os
sys.path.insert(0, r"D:\Doubao工作区\_pylibs")
import numpy as np
from PIL import Image, ImageFilter
from collections import deque

proj = r"D:\Doubao工作区\赛博三星堆跑酷"
im = Image.open(os.path.join(proj, "assets", "hero_run.jpg")).convert("RGB")
w, h = im.size
arr = np.asarray(im).astype(np.float32)
mx = arr.max(2); mn = arr.min(2)
lum = arr.sum(2)/3.0
sat = np.where(mx>0, (mx-mn)/np.maximum(mx,1), 0)

# 屏障：亮部 或 高饱和霓虹
barrier = (lum > 48) | (sat > 0.42)
b_img = Image.fromarray((barrier*255).astype(np.uint8), "L")
b_img = b_img.filter(ImageFilter.MaxFilter(3))   # 仅膨胀1像素，轻度闭合
barrier = np.asarray(b_img) > 40

# flood fill 外部
passable = ~barrier
outside = np.zeros((h,w), bool)
dq = deque()
for x in range(w):
    for y in (0,h-1):
        if passable[y,x] and not outside[y,x]:
            outside[y,x]=1; dq.append((x,y))
for y in range(h):
    for x in (0,w-1):
        if passable[y,x] and not outside[y,x]:
            outside[y,x]=1; dq.append((x,y))
while dq:
    x,y = dq.popleft()
    for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        if 0<=nx<w and 0<=ny<h and passable[ny,nx] and not outside[ny,nx]:
            outside[ny,nx]=1; dq.append((nx,ny))

# 角色候选 = 非外部
candidate = ~outside
# 从中心连通域重建（只保留角色主体，去掉孤立碎片）
seed = np.zeros((h,w), bool)
seed[h//2, w//2] = True
prev=None; guard=0
while not np.array_equal(seed,prev) and guard<300:
    prev=seed; guard+=1
    si = Image.fromarray((seed*255).astype(np.uint8),"L").filter(ImageFilter.MaxFilter(15))
    seed = (np.asarray(si)>0) & candidate

alpha = np.where(seed, 255, 0).astype(np.uint8)
a = Image.fromarray(alpha,"L").filter(ImageFilter.GaussianBlur(1.0))
rgba = im.convert("RGBA"); rgba.putalpha(a)
bbox = a.point(lambda v:255 if v>30 else 0).getbbox()
if bbox:
    bbox=(max(0,bbox[0]-8),max(0,bbox[1]-8),min(w,bbox[2]+8),min(h,bbox[3]+8))
    rgba = rgba.crop(bbox)
out = os.path.join(proj,"assets","hero_cut.png")
rgba.save(out)
print("saved", rgba.size, "iters:", guard)
