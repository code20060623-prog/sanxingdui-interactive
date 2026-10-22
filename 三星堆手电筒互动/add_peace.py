# -*- coding: utf-8 -*-
"""添加剪刀手✌手势识别，检测到后跳转到青铜抓娃娃机小游戏。"""
import os

proj = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(proj, "三星堆手电筒.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1) 状态变量
old1 = "let prevFist = false, fistCooldown = 0, tipHistory = [];\n"
new1 = (old1 +
        "let prevPeace = false, peaceCooldown = 0;\n"
        "const GAME_URL = '../../ai-pixel-claw/index.html';\n")
assert old1 in html, "锚点1未找到"
html = html.replace(old1, new1, 1)

# 2) isPeace + launchGame
old2 = "  return bent >= 3;\n}\nfunction expandedRect(el, pad) {"
new2 = (
"  return bent >= 3;\n}\n"
"/* 剪刀手✌：食指、中指伸直并分开，无名指、小指弯曲 */\n"
"function isPeace(lm) {\n"
"  const w = lm[0];\n"
"  const ext = (tip, pip) => mpDist(lm[tip], w) > mpDist(lm[pip], w) * 1.12;\n"
"  const bend = (tip, pip) => mpDist(lm[tip], w) < mpDist(lm[pip], w) * 1.08;\n"
"  if (!(ext(8, 6) && ext(12, 10))) return false;\n"
"  if (!(bend(16, 14) && bend(20, 18))) return false;\n"
"  if (mpDist(lm[8], lm[12]) < mpDist(lm[6], lm[10]) * 1.25) return false;\n"
"  return true;\n}\n"
"function launchGame() {\n"
"  if (window.__gameLaunching) return;\n"
"  window.__gameLaunching = true;\n"
"  toast('检测到剪刀手，进入青铜抓娃娃机…');\n"
"  setTimeout(() => { window.location.href = GAME_URL; }, 600);\n"
"}\n"
"function expandedRect(el, pad) {"
)
assert old2 in html, "锚点2未找到"
html = html.replace(old2, new2, 1)

# 3) onHand 检测（提前 now，在详情页 return 之前也检测）
old3 = (
"    tx = px; ty = py;\n"
"    if (viewDetail.classList.contains('show')) return;\n"
"    const now = performance.now();\n"
"    tipHistory.push({ x: px, y: py, t: now });\n"
)
new3 = (
"    tx = px; ty = py;\n"
"    const now = performance.now();\n"
"    const peace = isPeace(lm);\n"
"    if (peace && !prevPeace && now > peaceCooldown) {\n"
"      peaceCooldown = now + 2000;\n"
"      launchGame();\n"
"    }\n"
"    prevPeace = peace;\n"
"    if (viewDetail.classList.contains('show')) return;\n"
"    tipHistory.push({ x: px, y: py, t: now });\n"
)
assert old3 in html, "锚点3未找到"
html = html.replace(old3, new3, 1)

# 4) else 分支
old4 = "  } else {\n    prevFist = false;\n  }\n}\nasync function detectLoop() {"
new4 = "  } else {\n    prevFist = false;\n    prevPeace = false;\n  }\n}\nasync function detectLoop() {"
assert old4 in html, "锚点4未找到"
html = html.replace(old4, new4, 1)

with open(html_path, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print("剪刀手检测已添加, KB:", round(os.path.getsize(html_path) / 1024))
