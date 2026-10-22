# -*- coding: utf-8 -*-
"""紧密裁剪文物图的黑色边框，使图片比例与文物本身一致。"""
import os, sys

sys.path.insert(0, r"D:\Doubao工作区\_pylibs")
try:
    from PIL import Image
except ImportError:
    print("NO_PIL")
    sys.exit(1)

proj = os.path.dirname(os.path.abspath(__file__))
names = ["art_1_mask.jpg", "art_2_side.jpg", "art_3_head.jpg", "art_4_liren.jpg"]
THRESH = 26
PAD = 8

for name in names:
    path = os.path.join(proj, name)
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    minx, miny, maxx, maxy = w, h, -1, -1
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            if r > THRESH or g > THRESH or b > THRESH:
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
    minx = max(0, minx - PAD); miny = max(0, miny - PAD)
    maxx = min(w - 1, maxx + PAD); maxy = min(h - 1, maxy + PAD)
    crop = im.crop((minx, miny, maxx + 1, maxy + 1))
    crop.save(path, quality=92)
    print(name, "->", crop.size, "ratio %.2f" % (crop.size[0] / crop.size[1]))
