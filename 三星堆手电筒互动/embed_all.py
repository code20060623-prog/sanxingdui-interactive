# -*- coding: utf-8 -*-
"""把壁画与4张文物图以 base64 内嵌进 HTML，产出单文件。"""
import base64, os

proj = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(proj, "三星堆手电筒.html")


def data_uri(path):
    with open(path, "rb") as f:
        head = f.read(4)
    mime = "image/png" if head.startswith(b"\x89PNG") else "image/jpeg"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return "data:%s;base64,%s" % (mime, b64)


mapping = {
    "__IMG_WALL__": os.path.join(proj, "sanxingdui.jpg"),
    "__ART_1__": os.path.join(proj, "art_1_mask.jpg"),
    "__ART_2__": os.path.join(proj, "art_2_side.jpg"),
    "__ART_3__": os.path.join(proj, "art_3_head.jpg"),
    "__ART_4__": os.path.join(proj, "art_4_liren.jpg"),
}

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

for placeholder, img_path in mapping.items():
    uri = data_uri(img_path)
    count = html.count(placeholder)
    html = html.replace(placeholder, uri)
    print(placeholder, "x", count, "imgKB:", round(os.path.getsize(img_path) / 1024))

with open(html_path, "w", encoding="utf-8", newline="") as f:
    f.write(html)

print("final html KB:", round(os.path.getsize(html_path) / 1024))
