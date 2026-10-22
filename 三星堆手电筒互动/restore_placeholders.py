# -*- coding: utf-8 -*-
"""把 HTML 中内嵌的壁画 base64 还原为占位符，便于结构化编辑。"""
import os, re

proj = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(proj, "三星堆手电筒.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

html, n = re.subn(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', '__IMG_WALL__', html)

with open(html_path, "w", encoding="utf-8", newline="") as f:
    f.write(html)

print("replaced:", n)
print("size KB:", round(os.path.getsize(html_path) / 1024))
