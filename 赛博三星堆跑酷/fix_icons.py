# -*- coding: utf-8 -*-
"""替换指南卡片 emoji 为内联 SVG，并移除 user-scalable=no。"""
import os

p = r"D:\Doubao工作区\赛博三星堆跑酷\赛博三星堆跑酷.html"
with open(p, "r", encoding="utf-8") as f:
    html = f.read()

repls = [
    ('<div class="guide-icon">\U0001f590\ufe0f\u2b06\ufe0f</div>',
     '<div class="guide-icon"><svg viewBox="0 0 48 48" width="38" height="38" fill="none" stroke="#00f0ff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M24 38V12"/><path d="M12 23l12-12 12 12"/></svg></div>'),
    ('<div class="guide-icon">\U0001f590\ufe0f\u2b07\ufe0f</div>',
     '<div class="guide-icon"><svg viewBox="0 0 48 48" width="38" height="38" fill="none" stroke="#ff2bd6" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M24 10v26"/><path d="M12 25l12 12 12-12"/></svg></div>'),
    ('<div class="guide-icon">\U0001f4a8</div>',
     '<div class="guide-icon"><svg viewBox="0 0 48 48" width="38" height="38" fill="none" stroke="#ffe600" stroke-width="2.6" stroke-linecap="round"><path d="M10 16h14"/><path d="M10 24h24"/><path d="M10 32h32"/></svg></div>'),
]
for old, new in repls:
    if old in html:
        html = html.replace(old, new)
        print("replaced:", old[:30])
    else:
        print("NOT FOUND:", repr(old[:20]))

# 移除 user-scalable=no
html = html.replace(
    'width=device-width, initial-scale=1.0, user-scalable=no',
    'width=device-width, initial-scale=1.0')

with open(p, "w", encoding="utf-8") as f:
    f.write(html)
print("done, size KB:", round(os.path.getsize(p)/1024,1))
