# -*- coding: utf-8 -*-
"""测试强模糊实心掩膜：对文物图亮度阈值->强模糊->低阈值，检查颈部/眼窝填充。"""
from PIL import Image, ImageFilter
import os
proj = os.path.dirname(os.path.abspath(__file__))

for name in ["art_1_mask.jpg", "art_2_side.jpg", "art_3_head.jpg", "art_4_liren.jpg"]:
    im = Image.open(os.path.join(proj, name)).convert("RGB")
    g = im.convert("L")
    # 二值
    bw = g.point(lambda v: 255 if v > 13 else 0)
    # 强模糊 + 低阈值（实心）
    blur = bw.filter(ImageFilter.GaussianBlur(20))
    solid = blur.point(lambda v: 255 if v > 51 else 0)
    # 再轻微模糊（软边缘）
    edge = solid.filter(ImageFilter.GaussianBlur(1.5))
    out = os.path.join(proj, "_ref", "testmask_" + name.replace(".jpg", ".png"))
    edge.save(out)
    print("saved", out)
