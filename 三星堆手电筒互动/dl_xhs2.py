# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, r"D:\Doubao工作区\_pylibs")
import yt_dlp

outdir = r"D:\Doubao工作区\三星堆手电筒互动\_ref"
os.makedirs(outdir, exist_ok=True)
url = ("https://www.xiaohongshu.com/discovery/item/68d162db000000000b03f439"
       "?app_platform=ios&app_version=9.51&share_from_user_hidden=true"
       "&xsec_source=app_share&type=video"
       "&xsec_token=CBQxGO3pi93SwdCCL1E8zWw4ItvVvW8POk8vAdmwatfw8="
       "&author_share=1&xhsshare=CopyLink&track_code=96v1Vn9dvKF")

opts = {
    "outtmpl": os.path.join(outdir, "xhs_ref.%(ext)s"),
    "format": "best",
    "quiet": True,
    "noprogress": True,
    "noplaylist": True,
    "ignoreerrors": False,
    "extractor_args": {"xiaohongshu": []},
}
try:
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if info:
            print("TITLE:", info.get("title"))
            print("DURATION:", info.get("duration"))
except Exception as e:
    print("ERROR:", type(e).__name__, str(e)[:300])

print("--- files ---")
for f in os.listdir(outdir):
    print(f, round(os.path.getsize(os.path.join(outdir, f)) / 1024), "KB")
