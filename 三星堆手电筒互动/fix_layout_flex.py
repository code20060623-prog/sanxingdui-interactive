# -*- coding: utf-8 -*-
"""将详情页从 Grid 改为 Flex 布局，修复图在右侧时容器高度塌陷。"""
import os

proj = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(proj, "三星堆手电筒.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 桌面 CSS
desk_old = (
"  .detail-grid { width:100%; height:100%; display:grid; grid-template-columns:44% 56%;\n"
"    align-items:center; }\n"
"  .detail-grid.img-right { grid-template-columns:56% 44%; }\n"
"  .detail-grid.img-right .dimg-wrap { grid-column:2; }\n"
"  .detail-grid.img-right .dcontent { grid-column:1; padding:0 2vw 0 6vw; }\n"
"  .dimg-wrap { height:100%; display:flex; align-items:center; justify-content:center; }\n"
"  #dimg { width:auto; height:auto; max-width:92%; max-height:78vh; object-fit:contain; }\n"
"  .dcontent { padding:0 6vw 0 2vw; max-width:640px; }\n"
)
desk_new = (
"  .detail-grid { width:100%; height:100%; display:flex; align-items:stretch; }\n"
"  .detail-grid.img-right { flex-direction:row-reverse; }\n"
"  .dimg-wrap { flex:0 0 44%; height:100%; display:flex; align-items:center; justify-content:center; }\n"
"  #dimg { width:auto; height:auto; max-width:92%; max-height:78vh; object-fit:contain; }\n"
"  .dcontent { flex:1 1 56%; align-self:center; padding:0 6vw 0 2vw; max-width:640px; }\n"
"  .detail-grid.img-right .dcontent { padding:0 2vw 0 6vw; }\n"
)
assert desk_old in html, "桌面 CSS 未找到"
html = html.replace(desk_old, desk_new, 1)

# 移动端 CSS
mob_old = (
"    .detail-grid { grid-template-columns:1fr; grid-template-rows:42% 58%; }\n"
"    .detail-grid.img-right { grid-template-columns:1fr; }\n"
"    .detail-grid.img-right .dimg-wrap { grid-column:1; }\n"
"    .detail-grid.img-right .dcontent { grid-column:2; padding:0 22px; }\n"
"    .dimg-wrap { height:100%; }\n"
"    #dimg { max-width:90%; max-height:38vh !important; }\n"
"    .dcontent { padding:0 22px; max-width:none; }\n"
)
mob_new = (
"    .detail-grid { flex-direction:column; }\n"
"    .detail-grid.img-right { flex-direction:column; }\n"
"    .dimg-wrap { flex:0 0 42%; height:auto; }\n"
"    #dimg { max-width:90%; max-height:38vh !important; }\n"
"    .dcontent { flex:1 1 58%; padding:0 22px; max-width:none; }\n"
)
assert mob_old in html, "移动端 CSS 未找到"
html = html.replace(mob_old, mob_new, 1)

with open(html_path, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("Flex 布局改造完成")
