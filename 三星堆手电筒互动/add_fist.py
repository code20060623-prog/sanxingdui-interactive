# -*- coding: utf-8 -*-
"""新增握拳点击 ENTER：光圈移到 ENTER 上，握拳即跳转详情页。"""
import os

proj = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(proj, "三星堆手电筒.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1) ENTER 悬停高亮样式
old_css = "#wlLit .enter { text-shadow:0 0 26px rgba(127,255,46,.85), 0 0 60px rgba(127,255,46,.4); }"
new_css = (
    "#wlLit .enter { text-shadow:0 0 26px rgba(127,255,46,.85), 0 0 60px rgba(127,255,46,.4);"
    " transition:transform .15s ease, text-shadow .15s ease; }\n"
    "  #wlLit .enter.hand-hover { transform:scale(1.2);"
    " text-shadow:0 0 42px rgba(127,255,46,1), 0 0 96px rgba(127,255,46,.65); }"
)
assert old_css in html, "CSS anchor not found"
html = html.replace(old_css, new_css, 1)

# 2) onHand 增加握拳检测
old_onhand = (
    "function onHand(results) {\n"
    "  if (results.multiHandLandmarks && results.multiHandLandmarks.length) {\n"
    "    const p = results.multiHandLandmarks[0][8]; // 食指指尖\n"
    "    tx = (1 - p.x) * innerWidth;                // 镜像翻转\n"
    "    ty = p.y * innerHeight;\n"
    "  }\n"
    "}"
)
new_onhand = (
    "let prevFist = false, fistCooldown = 0, tipHistory = [];\n"
    "function mpDist(a, b) {\n"
    "  const dx = a.x - b.x, dy = a.y - b.y, dz = (a.z || 0) - (b.z || 0);\n"
    "  return Math.sqrt(dx * dx + dy * dy + dz * dz);\n"
    "}\n"
    "/* 四指（食/中/无名/小）中至少三指弯曲，判定为握拳 */\n"
    "function isFist(lm) {\n"
    "  const w = lm[0];\n"
    "  let bent = 0;\n"
    "  const pairs = [[8, 5], [12, 9], [16, 13], [20, 17]];\n"
    "  for (const [tip, mcp] of pairs) {\n"
    "    if (mpDist(lm[tip], w) < mpDist(lm[mcp], w) * 1.1) bent++;\n"
    "  }\n"
    "  return bent >= 3;\n"
    "}\n"
    "function expandedRect(el, pad) {\n"
    "  const b = el.getBoundingClientRect();\n"
    "  return { left: b.left - pad, right: b.right + pad, top: b.top - pad, bottom: b.bottom + pad };\n"
    "}\n"
    "function inRect(x, y, r) { return x >= r.left && x <= r.right && y >= r.top && y <= r.bottom; }\n"
    "function onHand(results) {\n"
    "  if (results.multiHandLandmarks && results.multiHandLandmarks.length) {\n"
    "    const lm = results.multiHandLandmarks[0];\n"
    "    const p = lm[8]; // 食指指尖\n"
    "    const px = (1 - p.x) * innerWidth;  // 镜像翻转\n"
    "    const py = p.y * innerHeight;\n"
    "    tx = px; ty = py;\n"
    "    if (viewDetail.classList.contains('show')) return;\n"
    "    const now = performance.now();\n"
    "    tipHistory.push({ x: px, y: py, t: now });\n"
    "    while (tipHistory.length && now - tipHistory[0].t > 350) tipHistory.shift();\n"
    "    const r = expandedRect(enterBtn, 70);\n"
    "    enterBtn.classList.toggle('hand-hover', inRect(px, py, r));\n"
    "    const fist = isFist(lm);\n"
    "    if (fist && !prevFist && now > fistCooldown) {\n"
    "      if (tipHistory.some(pt => inRect(pt.x, pt.y, r))) {\n"
    "        enterBtn.classList.remove('hand-hover');\n"
    "        enterBtn.click();\n"
    "        fistCooldown = now + 1500;\n"
    "      }\n"
    "    }\n"
    "    prevFist = fist;\n"
    "  } else {\n"
    "    prevFist = false;\n"
    "  }\n"
    "}"
)
assert old_onhand in html, "onHand anchor not found"
html = html.replace(old_onhand, new_onhand, 1)

# 3) 开启手势的提示文案
old_toast = "toast('把单手举到摄像头前，食指指向哪里，光照向哪里');"
new_toast = "toast('食指指向哪里光照向哪里；光圈移到 ENTER 上，握拳即可进入');"
assert old_toast in html, "toast anchor not found"
html = html.replace(old_toast, new_toast, 1)

with open(html_path, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("done, final KB:", round(os.path.getsize(html_path) / 1024))
