# -*- coding: utf-8 -*-
"""生成默认显示详情页的临时副本，用于截图验证。用法: python make_detail_preview.py [序号]"""
import os, sys

proj = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(proj, "三星堆手电筒.html")
preview_path = os.path.join(proj, "_detail_preview.html")
idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0

with open(src_path, "r", encoding="utf-8") as f:
    html = f.read()

inject = (
    '<script>\n'
    'window.addEventListener("load", function(){\n'
    '  renderDetail(%d);\n'
    '  document.getElementById("viewDetail").classList.add("show");\n'
    '});\n'
    '</script>\n</body>' % idx
)
html = html.replace("</body>", inject, 1)

with open(preview_path, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("preview idx", idx, "KB:", round(os.path.getsize(preview_path) / 1024))
