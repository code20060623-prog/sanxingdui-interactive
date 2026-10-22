# -*- coding: utf-8 -*-
"""把高清壁画以 base64 内嵌进 HTML，产出单文件自包含页面。"""
import base64, os

proj = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(proj, "三星堆手电筒.html")
img_path = os.path.join(proj, "sanxingdui.jpg")

with open(img_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")
data_uri = "data:image/jpeg;base64," + b64

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

count = html.count("__IMG_BASE64__")
html = html.replace("__IMG_BASE64__", data_uri)

with open(html_path, "w", encoding="utf-8", newline="") as f:
    f.write(html)

print("replaced placeholders:", count)
print("html size KB:", round(os.path.getsize(html_path) / 1024))
