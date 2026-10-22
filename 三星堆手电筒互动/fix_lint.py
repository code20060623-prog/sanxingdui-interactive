# -*- coding: utf-8 -*-
"""修复自检提示：viewport 禁用缩放、暗层 ENTER 误判为可点按钮。"""
import os

proj = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(proj, "三星堆手电筒.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

repls = [
    (
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    ),
    (
        "  .wl .enter { font-size:clamp(26px,4.4vw,56px); color:#7dff2e; letter-spacing:3px; background:none; border:none;\n"
        "        font-family:inherit; cursor:pointer; pointer-events:auto; }",
        "  .wl .enter { font-size:clamp(26px,4.4vw,56px); color:#7dff2e; letter-spacing:3px; background:none; border:none;\n"
        "        font-family:inherit; }\n"
        "  #wlLit .enter { cursor:pointer; pointer-events:auto; }"
    ),
]

for old, new in repls:
    if old not in html:
        print("NOT FOUND:", old[:60])
    else:
        html = html.replace(old, new, 1)
        print("OK:", new[:60].replace("\n", " "))

with open(html_path, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("done, size KB:", round(os.path.getsize(html_path) / 1024))
