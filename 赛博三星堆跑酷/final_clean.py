# -*- coding: utf-8 -*-
"""在最终 alpha 上从中心做连通域重建，只保留角色主体；边缘孤立碎片清零。"""
import sys, os
sys.path.insert(0, r"D:\Doubao工作区\_pylibs")
import numpy as np
from PIL import Image, ImageFilter

p = r"D:\Doubao工作区\赛博三星堆跑酷\assets\hero_cut.png"
im = Image.open(p).convert("RGBA")
w, h = im.size
alpha = np.asarray(im.split()[3])
core = alpha > 30

seed = np.zeros((h,w), bool)
seed[h//2, w//2] = True
prev = None
guard = 0
while not np.array_equal(seed, prev) and guard < 300:
    prev = seed; guard += 1
    si = Image.fromarray((seed*255).astype(np.uint8),"L").filter(ImageFilter.MaxFilter(15))
    seed = (np.asarray(si) > 0) & core

new_alpha = np.where(seed, alpha, 0).astype(np.uint8)
im.putalpha(Image.fromarray(new_alpha, "L"))
bbox = Image.fromarray(new_alpha,"L").point(lambda v:255 if v>30 else 0).getbbox()
if bbox:
    bbox=(max(0,bbox[0]-4),max(0,bbox[1]-4),min(w,bbox[2]+4),min(h,bbox[3]+4))
    im = im.crop(bbox)
im.save(p)
print("cleaned", im.size, "iterations:", guard)
