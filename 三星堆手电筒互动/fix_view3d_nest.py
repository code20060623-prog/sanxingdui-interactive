# -*- coding: utf-8 -*-
"""修复：补上闭合 viewDetail 的 </div>，让 view3d 成为 viewDetail 的兄弟节点。"""
import os
proj = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(proj, "三星堆手电筒.html")
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

old = (
"    </div>\n"
"  </div>\n"
"<!-- ===== 文物3D旋转展示 ===== -->\n"
"<div id=\"view3d\">\n"
)
new = (
"    </div>\n"
"  </div>\n"
"</div>\n"
"<!-- ===== 文物3D旋转展示 ===== -->\n"
"<div id=\"view3d\">\n"
)
assert old in html, "修复锚点未找到"
html = html.replace(old, new, 1)

with open(p, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("viewDetail 已闭合，KB:", round(os.path.getsize(p) / 1024))
