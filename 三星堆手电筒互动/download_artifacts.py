# -*- coding: utf-8 -*-
"""下载文物图片到项目目录。"""
import os, urllib.request

proj = os.path.dirname(os.path.abspath(__file__))
items = {
    "artifacts_liren.jpg": "https://aka.doubaocdn.com/s/JIK1uPOjQY",
    "artifacts_zongmu.jpg": "https://aka.doubaocdn.com/s/4aiqBzBHo2",
    "artifacts_shenshu.jpg": "https://aka.doubaocdn.com/s/1IWlNKScqY",
}
for name, url in items.items():
    path = os.path.join(proj, name)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    with open(path, "wb") as f:
        f.write(data)
    print(name, round(len(data) / 1024), "KB")
