# -*- coding: utf-8 -*-
"""手势库改为多节点动态加载回退，提高网络不稳定时的可用性。"""
import os

proj = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(proj, "三星堆手电筒.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

repls = []

# 1) 移除静态 script 标签
repls.append((
    '<script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.4.1675469240/hands.js" crossorigin="anonymous"></script>\n'
    '<script>',
    '<script>'
))

# 2) 注入多节点加载器
repls.append((
    "function setLabel(btn, text) { btn.lastChild.textContent = text; }",
    "function setLabel(btn, text) { btn.lastChild.textContent = text; }\n\n"
    "/* ---------- MediaPipe 库：多节点自动回退加载 ---------- */\n"
    "const MP_BASES = [\n"
    "  'https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.4.1675469240',\n"
    "  'https://fastly.jsdelivr.net/npm/@mediapipe/hands@0.4.1675469240',\n"
    "  'https://gcore.jsdelivr.net/npm/@mediapipe/hands@0.4.1675469240'\n"
    "];\n"
    "let mpBase = MP_BASES[0], mpLoading = null;\n"
    "function loadMpScript(src) {\n"
    "  return new Promise((resolve, reject) => {\n"
    "    const s = document.createElement('script');\n"
    "    s.src = src; s.crossOrigin = 'anonymous';\n"
    "    s.onload = resolve;\n"
    "    s.onerror = () => reject(new Error('load fail'));\n"
    "    document.head.appendChild(s);\n"
    "  });\n"
    "}\n"
    "async function ensureHandsLib() {\n"
    "  if (typeof Hands !== 'undefined') return true;\n"
    "  if (mpLoading) return mpLoading;\n"
    "  mpLoading = (async () => {\n"
    "    for (const base of MP_BASES) {\n"
    "      try { await loadMpScript(base + '/hands.js'); mpBase = base; return true; }\n"
    "      catch (e) {}\n"
    "    }\n"
    "    mpLoading = null;\n"
    "    return false;\n"
    "  })();\n"
    "  return mpLoading;\n"
    "}"
))

# 3) startGesture 开头改为动态加载
repls.append((
    "async function startGesture() {\n"
    "  if (typeof Hands === 'undefined') {\n"
    "    toast('手势库未加载成功，请确认网络后刷新；鼠标/触摸仍可用');\n"
    "    return;\n"
    "  }\n"
    "  try {",
    "async function startGesture() {\n"
    "  const libOk = await ensureHandsLib();\n"
    "  if (!libOk) {\n"
    "    toast('手势库加载失败，请检查网络；鼠标/触摸仍可用');\n"
    "    return;\n"
    "  }\n"
    "  try {"
))

# 4) locateFile 用成功节点
repls.append((
    "locateFile: f => `https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.4.1675469240/${f}`",
    "locateFile: f => `${mpBase}/${f}`"
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
