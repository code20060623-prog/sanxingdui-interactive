# -*- coding: utf-8 -*-
"""首件标题在 Gold 后换行，复刻参考图；标题渲染改为 innerHTML。"""
import os

proj = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(proj, "三星堆手电筒.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

repls = [
    (
        "title: 'Bronze Head Mask with Gold Plating',",
        "title: 'Bronze Head Mask with Gold<br>Plating',"
    ),
    (
        "  dtitle.textContent = a.title;",
        "  dtitle.innerHTML = a.title;"
    ),
]

for old, new in repls:
    if old not in html:
        print("NOT FOUND:", old[:50])
    else:
        html = html.replace(old, new, 1)
        print("OK:", new[:50])

with open(html_path, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("done")
