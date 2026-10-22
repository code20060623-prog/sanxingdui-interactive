# -*- coding: utf-8 -*-
"""生成自动进入游戏的临时文件，用于截图验证游戏内画面。"""
import os, subprocess

proj = r"D:\Doubao工作区\赛博三星堆跑酷"
src = os.path.join(proj, "赛博三星堆跑酷.html")
test = os.path.join(proj, "_test_ingame.html")

s = open(src, encoding="utf-8").read()
anchor = "requestAnimationFrame(loop);"
inject = ("requestAnimationFrame(loop);\n"
          "startGame();\n"
          "for (let i=0;i<150;i++){ update(1/60); }")
s = s.replace(anchor, inject, 1)
open(test, "w", encoding="utf-8").write(s)

shot = r"C:\Users\Administrator\AppData\Local\Doubao\User Data\Profile 3\.doubao\agent_mode\workspace\.skills\html\scripts\shot.py"
r = subprocess.run(["python", shot, test, "--only", "desktop"],
                   capture_output=True, text=True, encoding="utf-8")
print("shot exit:", r.returncode)
# 找截图路径
import glob
for f in glob.glob(os.path.join(proj, "_shots", "*desktop*")):
    print(f)
