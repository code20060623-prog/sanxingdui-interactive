# -*- coding: utf-8 -*-
"""标题字体改为 Chiller（内嵌），正文字体改为 Nanum Myeongjo（镜像）。"""
import base64, os

proj = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(proj, "三星堆手电筒.html")
font_path = os.path.join(proj, "_fonts", "chiller.ttf")

with open(font_path, "rb") as f:
    chiller_b64 = base64.b64encode(f.read()).decode("ascii")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

repls = []

# 1) 字体样式表链接加入 Nanum Myeongjo
repls.append((
    "https://miaoda.feishu.cn/fonts/css2?family=Permanent+Marker&family=Gochi+Hand&display=swap",
    "https://miaoda.feishu.cn/fonts/css2?family=Permanent+Marker&family=Gochi+Hand&family=Nanum+Myeongjo:wght@400;700;800&display=swap"
))

# 2) 内嵌 Chiller
repls.append((
    "<style>\n  * { margin:0; padding:0;",
    "<style>\n"
    "  @font-face {\n"
    "    font-family:'Chiller';\n"
    "    src:url('data:application/x-font-ttf;base64," + chiller_b64 + "') format('truetype');\n"
    "    font-display:swap;\n"
    "  }\n"
    "  * { margin:0; padding:0;"
))

# 3) 标题用 Chiller
repls.append((
    "  #dtitle { font-family:'Gochi Hand',cursive; font-weight:400; color:#e9c63c;",
    "  #dtitle { font-family:'Chiller','Gochi Hand',cursive; font-weight:400; color:#e9c63c;"
))

# 4) 正文用 Nanum Myeongjo
repls.append((
    "  #ddesc { font-family:Georgia,'Times New Roman',serif;",
    "  #ddesc { font-family:'Nanum Myeongjo',Georgia,'Times New Roman',serif;"
))

for i, (old, new) in enumerate(repls, 1):
    if old not in html:
        print("NOT FOUND #", i)
    else:
        html = html.replace(old, new, 1)
        print("OK #", i)

with open(html_path, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("final KB:", round(os.path.getsize(html_path) / 1024))
