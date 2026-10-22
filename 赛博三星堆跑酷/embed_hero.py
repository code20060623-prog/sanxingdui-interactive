# -*- coding: utf-8 -*-
"""把角色图内嵌为 base64 data URI，替换 JS 中的相对路径。"""
import base64, os

proj = r"D:\Doubao工作区\赛博三星堆跑酷"
html_path = os.path.join(proj, "赛博三星堆跑酷.html")
img_path = os.path.join(proj, "assets", "hero_run.jpg")

with open(img_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")
data_uri = "data:image/jpeg;base64," + b64

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

old = "heroImg.src = 'assets/hero_run.jpg';"
assert old in html, "未找到角色路径锚点"
html = html.replace(old, "heroImg.src = '" + data_uri + "';")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
print("embedded, html size KB:", round(os.path.getsize(html_path)/1024,1))
