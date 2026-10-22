# -*- coding: utf-8 -*-
"""清除所有接触图片边缘的连通区域（碎片），角色不接触边缘因此保留。"""
import sys, os
sys.path.insert(0, r"D:\Doubao工作区\_pylibs")
import numpy as np
from PIL import Image
from collections import deque

p = r"D:\Doubao工作区\赛博三星堆跑酷\assets\hero_cut.png"
im = Image.open(p).convert("RGBA")
w, h = im.size
alpha = np.asarray(im.split()[3])
mask = alpha > 30

edge = np.zeros((h,w), bool)
dq = deque()
for x in range(w):
    for y in (0,h-1):
        if mask[y,x] and not edge[y,x]:
            edge[y,x]=1; dq.append((x,y))
for y in range(h):
    for x in (0,w-1):
        if mask[y,x] and not edge[y,x]:
            edge[y,x]=1; dq.append((x,y))
while dq:
    x,y = dq.popleft()
    for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        if 0<=nx<w and 0<=ny<h and mask[ny,nx] and not edge[ny,nx]:
            edge[ny,nx]=1; dq.append((nx,ny))

new_alpha = np.where(edge, 0, alpha).astype(np.uint8)
im.putalpha(Image.fromarray(new_alpha,"L"))
# 重新裁剪
bbox = Image.fromarray(new_alpha,"L").point(lambda v:255 if v>30 else 0).getbbox()
if bbox:
    bbox=(max(0,bbox[0]-4),max(0,bbox[1]-4),min(w,bbox[2]+4),min(h,bbox[3]+4))
    im = im.crop(bbox)
im.save(p)
print("edge fragments removed", im.size)
