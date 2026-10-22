# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, r"D:\Doubao工作区\_pylibs")
import yt_dlp

outdir = r"D:\Doubao工作区\三星堆手电筒互动\_ref"
os.makedirs(outdir, exist_ok=True)
url = "https://xhslink.cn/o/96v1Vn9dvKF"

opts = {
    "outtmpl": os.path.join(outdir, "xhs_ref.%(ext)s"),
    "format": "best",
    "quiet": False,
    "noprogress": True,
    "noplaylist": True,
    "ignoreerrors": False,
}
try:
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if info:
            print("TITLE:", info.get("title"))
            print("DURATION:", info.get("duration"))
            print("UPLOADER:", info.get("uploader"))
except Exception as e:
    print("ERROR:", type(e).__name__, str(e)[:500])

print("--- files ---")
for f in os.listdir(outdir):
    print(f, round(os.path.getsize(os.path.join(outdir, f)) / 1024), "KB")
