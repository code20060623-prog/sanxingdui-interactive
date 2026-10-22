# -*- coding: utf-8 -*-
"""按四张参考图重建详情页：左右交替布局、按比例图片、对应文本。"""
import os, re

proj = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(proj, "三星堆手电筒.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# ---------- 1) 桌面 CSS ----------
css_old = (
"  .detail-grid { width:100%; height:100%; display:grid; grid-template-columns:44% 56%;\n"
"    align-items:center; }\n"
"  .dimg-wrap { height:100%; display:flex; align-items:center; }\n"
"  #dimg { width:100%; height:100%; object-fit:contain; }\n"
"  .dcontent { padding:0 6vw 0 2vw; max-width:640px; }\n"
)
css_new = (
"  .detail-grid { width:100%; height:100%; display:grid; grid-template-columns:44% 56%;\n"
"    align-items:center; }\n"
"  .detail-grid.img-right { grid-template-columns:56% 44%; }\n"
"  .detail-grid.img-right .dimg-wrap { grid-column:2; }\n"
"  .detail-grid.img-right .dcontent { grid-column:1; padding:0 2vw 0 6vw; }\n"
"  .dimg-wrap { height:100%; display:flex; align-items:center; justify-content:center; }\n"
"  #dimg { width:auto; height:auto; max-width:92%; max-height:78vh; object-fit:contain; }\n"
"  .dcontent { padding:0 6vw 0 2vw; max-width:640px; }\n"
)
assert css_old in html, "桌面 CSS 未找到"
html = html.replace(css_old, css_new, 1)

# ---------- 2) 移动端 CSS ----------
mcss_old = (
"    .detail-grid { grid-template-columns:1fr; grid-template-rows:42% 58%; }\n"
"    .dimg-wrap { height:100%; }\n"
"    .dcontent { padding:0 22px; max-width:none; }\n"
)
mcss_new = (
"    .detail-grid { grid-template-columns:1fr; grid-template-rows:42% 58%; }\n"
"    .detail-grid.img-right { grid-template-columns:1fr; }\n"
"    .detail-grid.img-right .dimg-wrap { grid-column:1; }\n"
"    .detail-grid.img-right .dcontent { grid-column:2; padding:0 22px; }\n"
"    .dimg-wrap { height:100%; }\n"
"    #dimg { max-width:90%; max-height:38vh !important; }\n"
"    .dcontent { padding:0 22px; max-width:none; }\n"
)
assert mcss_old in html, "移动端 CSS 未找到"
html = html.replace(mcss_old, mcss_new, 1)

# ---------- 3) detailGrid 引用 ----------
ref_old = "const btnBack = document.getElementById('btnBack');\n"
ref_new = ref_old + "const detailGrid = document.querySelector('.detail-grid');\n"
assert ref_old in html, "btnBack 引用未找到"
html = html.replace(ref_old, ref_new, 1)

# ---------- 4) ARTIFACTS 数据 ----------
new_artifacts = """const ARTIFACTS = [
  {
    src: '__ART_1__', side: 'left', imgH: 78,
    title: 'Bronze Head Mask with Gold<br>Plating',
    desc: "An extremely thin sheet of gold foil is perfectly applied to the face of the bronze head, symbolizing supreme divine authority and status, and representing a masterpiece of Sanxingdui's gold-copper composite craftsmanship.",
    facts: [
      ['年代', '商代 · 约公元前1200年'],
      ['出土', '1986年 二号祭祀坑'],
      ['尺寸', '高约 42.5 cm'],
      ['馆藏', '三星堆博物馆']
    ]
  },
  {
    src: '__ART_2__', side: 'right', imgH: 74,
    title: 'Bronze Figure with Vertical<br>Streaming Hair',
    desc: "A powerfully built dignitary cast with remarkably realistic anatomy, its hair swept upright into an ornate crest. The arms are held before the chest in a ring gesture that once grasped a ritual object, portraying a member of a newly encountered lineage of the Shu kingdom.",
    facts: [
      ['年代', '商代晚期'],
      ['出土', '2022年 八号祭祀坑'],
      ['尺寸', '人像高约 80 cm，含台基约 1 m'],
      ['馆藏', '四川省文物考古研究院']
    ]
  },
  {
    src: '__ART_3__', side: 'right', imgH: 62,
    title: 'Bronze Human Head',
    desc: "One of dozens of bronze human heads cast with individual features, this figure wears a flat-topped crown with the hair swept back. The heads portray the diverse lineages and officials of the ancient Shu kingdom, distinguished by their hairstyles and rank.",
    facts: [
      ['年代', '商代 · 约公元前1200年'],
      ['出土', '1986年 二号祭祀坑'],
      ['尺寸', '高约 50 cm'],
      ['馆藏', '三星堆博物馆']
    ]
  },
  {
    src: '__ART_4__', side: 'left', imgH: 73,
    title: 'Bronze Standing Figure',
    desc: "Towering over the exhibition hall, this is the tallest surviving bronze human figure of the ancient world. Its oversized ring-shaped hands are believed to have once held an ivory tusk or a ritual object, portraying a supreme king or priest in communion with the divine.",
    facts: [
      ['年代', '商代 · 约公元前1200年'],
      ['出土', '1986年 二号祭祀坑'],
      ['尺寸', '通高约 260.8 cm（含底座）'],
      ['馆藏', '三星堆博物馆']
    ]
  }
];"""

html, n = re.subn(r"const ARTIFACTS = \[.*?\n\];", new_artifacts, html, count=1, flags=re.S)
assert n == 1, "ARTIFACTS 数组替换失败"

# ---------- 5) renderDetail ----------
rd_old = (
"function renderDetail(i) {\n"
"  const a = ARTIFACTS[i];\n"
"  dimg.src = a.src;\n"
"  dtitle.innerHTML = a.title;\n"
)
rd_new = (
"function renderDetail(i) {\n"
"  const a = ARTIFACTS[i];\n"
"  dimg.src = a.src;\n"
"  dimg.style.maxHeight = a.imgH + 'vh';\n"
"  detailGrid.classList.toggle('img-right', a.side === 'right');\n"
"  dtitle.innerHTML = a.title;\n"
)
assert rd_old in html, "renderDetail 未找到"
html = html.replace(rd_old, rd_new, 1)

# ---------- 6) 初始静态 dimg ----------
html = html.replace(
  '<div class="dimg-wrap"><img id="dimg" src="__IMG_WALL__" alt="文物"></div>',
  '<div class="dimg-wrap"><img id="dimg" src="__ART_1__" alt="文物"></div>',
  1
)

with open(html_path, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("HTML 改造完成, KB:", round(os.path.getsize(html_path) / 1024))
