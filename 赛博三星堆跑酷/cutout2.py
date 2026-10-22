# -*- coding: utf-8 -*-
"""改进抠图：霓虹/亮部作为屏障并膨胀闭合，flood fill 外部，保留角色内部暗部。"""
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
barrier = (lum > 50) | (sat > 0.45)
b_img = Image.fromarray((barrier*255).astype(np.uint8), "L")
# 膨胀闭合（让霓虹轮廓连续）
b_img = b_img.filter(ImageFilter.MaxFilter(7))
barrier = np.asarray(b_img) > 40

# 背景候选：非屏障
passable = ~barrier
# flood fill 从边缘
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

alpha = np.where(outside, 0, 255).astype(np.uint8)

# 只保留中心角色连通域（形态学重建，去掉边缘小碎片）
core = alpha > 30
seed = np.zeros((h,w), bool)
seed[h//2, w//2] = True
prev = None
guard = 0
while not np.array_equal(seed, prev) and guard < 400:
    prev = seed; guard += 1
    si = Image.fromarray((seed*255).astype(np.uint8),"L").filter(ImageFilter.MaxFilter(9))
    seed = (np.asarray(si) > 0) & core
alpha = np.where(seed, alpha, 0).astype(np.uint8)

# 开运算（先腐蚀后膨胀）去掉边缘小碎片
a = Image.fromarray(alpha, "L")
a = a.filter(ImageFilter.MinFilter(5))
a = a.filter(ImageFilter.MaxFilter(5))
a = a.filter(ImageFilter.GaussianBlur(1.0))
rgba = im.convert("RGBA"); rgba.putalpha(a)
bbox = a.point(lambda v: 255 if v>30 else 0).getbbox()
if bbox:
    bbox=(max(0,bbox[0]-4),max(0,bbox[1]-4),min(w,bbox[2]+4),min(h,bbox[3]+4))
    rgba = rgba.crop(bbox)
out = os.path.join(proj, "assets", "hero_cut.png")
rgba.save(out)
print("saved", out, rgba.size)
