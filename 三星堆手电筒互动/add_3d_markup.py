# -*- coding: utf-8 -*-
"""添加文物3D旋转展示的 HTML 结构与 CSS。"""
import os
proj = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(proj, "三星堆手电筒.html")
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

# ---------- CSS（在 </style> 前） ----------
css = """  /* ===== 文物3D旋转展示 ===== */
  #view3d { position:fixed; inset:0; background:#000; opacity:0; pointer-events:none;
    transition:opacity .6s ease; z-index:50; }
  #view3d.show { opacity:1; pointer-events:auto; }
  #threeWrap { position:absolute; inset:0; cursor:grab; }
  #threeWrap:active { cursor:grabbing; }
  #btn3dBack { position:absolute; top:20px; left:22px; z-index:5; font-family:'Gochi Hand',cursive;
    font-size:14px; color:#cfe8dc; background:rgba(20,28,24,.6);
    border:1px solid rgba(122,196,170,.25); border-radius:18px; padding:6px 14px;
    cursor:pointer; display:flex; align-items:center; gap:5px; }
  #btn3dBack svg { width:14px; height:14px; fill:none; stroke:#cfe8dc; stroke-width:2; }
  #btn3dBack:hover { background:rgba(34,46,40,.8); }
  #t3dHead { position:absolute; top:30px; left:50%; transform:translateX(-50%);
    text-align:center; z-index:4; width:90%; pointer-events:none; }
  #t3dTitle { font-family:'Chiller','Gochi Hand',cursive; font-weight:400; color:#e9c63c;
    font-size:clamp(22px,2.6vw,36px); line-height:1.2; }
  #t3dSub { font-family:'Nanum Myeongjo',Georgia,serif; font-size:11px; letter-spacing:3px;
    color:#8fa39a; margin-top:4px; }
  #t3dFacts { position:absolute; left:28px; bottom:34px; z-index:4; max-width:250px;
    font-family:'Nanum Myeongjo',Georgia,serif; }
  #t3dFacts .tf-row { display:flex; gap:10px; font-size:13px; padding:5px 0;
    border-bottom:1px solid rgba(170,150,80,.16); }
  #t3dFacts .tf-row .k { color:#c9a94e; min-width:52px; }
  #t3dFacts .tf-row .v { color:#d6d6d6; }
  #t3dHint { position:absolute; bottom:30px; left:50%; transform:translateX(-50%);
    display:flex; gap:26px; z-index:4; font-family:'Nanum Myeongjo',Georgia,serif;
    font-size:13px; color:#9fb5ac; }
  @media (max-width:600px) {
    #t3dHead { top:24px; }
    #t3dSub { font-size:9px; letter-spacing:2px; }
    #t3dFacts { display:none; }
    #t3dHint { flex-direction:column; gap:4px; bottom:18px; font-size:11px; text-align:center; }
    #btn3dBack { top:12px; left:12px; font-size:12px; padding:4px 10px; }
  }
</style>"""
assert "</style>" in html
html = html.replace("</style>", css, 1)

# ---------- HTML（在 viewDetail 结束、主 <script> 前） ----------
markup = """<!-- ===== 文物3D旋转展示 ===== -->
<div id="view3d">
  <button id="btn3dBack">
    <svg viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg>
    返回
  </button>
  <div id="t3dHead">
    <h2 id="t3dTitle">Bronze Head Mask</h2>
    <p id="t3dSub">SANXINGDUI · 3D RELIC ROTATION</p>
  </div>
  <div id="threeWrap"></div>
  <div id="t3dFacts"></div>
  <div id="t3dHint">
    <span>手势：手左右移动，控制旋转方向与速度</span>
    <span>鼠标 / 触摸：按住左右拖动</span>
  </div>
</div>

<script>
const stage = document.getElementById('stage');"""
anchor = "</div>\n\n<script>\nconst stage = document.getElementById('stage');"
assert anchor in html, "HTML锚点未找到"
html = html.replace(anchor, markup, 1)

with open(p, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("3D HTML/CSS 已添加, KB:", round(os.path.getsize(p) / 1024))
