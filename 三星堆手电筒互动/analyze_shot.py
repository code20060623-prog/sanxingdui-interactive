# -*- coding: utf-8 -*-
"""分析截图中文物的实际边界（区分图片区与文字区）。"""
from PIL import Image

for i, zone in enumerate([("left", 0.45), ("right", 0.55), ("right", 0.55), ("left", 0.45)]):
    path = r"D:\Doubao工作区\三星堆手电筒互动\_shots\v%d.jpg" % i
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    side, cut = zone
    if side == "left":
        xrange = range(0, int(w * cut))
    else:
        xrange = range(int(w * cut), w)
    minx, miny, maxx, maxy = w, h, -1, -1
    for y in range(h):
        for x in xrange:
            r, g, b = px[x, y]
            if r > 30 or g > 30 or b > 30:
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
    print("v%d (%s) 文物边界 x:%d-%d y:%d-%d  高占比 %.1f%%  截图高 %d"
          % (i, side, minx, maxx, miny, maxy, 100.0 * (maxy - miny) / h, h))
