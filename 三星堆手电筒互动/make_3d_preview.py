# -*- coding: utf-8 -*-
"""生成默认显示3D旋转视图的临时副本。用法: python make_3d_preview.py [序号]"""
import os, sys
proj = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(proj, "三星堆手电筒.html")
idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
preview_path = os.path.join(proj, "_3d_preview.html")

with open(src_path, "r", encoding="utf-8") as f:
    html = f.read()

inject = (
    '<script>\n'
    'window.addEventListener("load", function(){\n'
    '  open3d(%d);\n'
    '});\n'
    '</script>\n</body>' % idx
)
html = html.replace("</body>", inject, 1)

with open(preview_path, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("3d preview idx", idx, "KB:", round(os.path.getsize(preview_path) / 1024))
