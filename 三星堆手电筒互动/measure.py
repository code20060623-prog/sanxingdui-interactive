# -*- coding: utf-8 -*-
"""调试：测量详情页图片与容器的实际尺寸。"""
import os
from playwright.sync_api import sync_playwright

proj = os.path.dirname(os.path.abspath(__file__))

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("file:///" + os.path.join(proj, "_detail_preview.html").replace("\\", "/"))
    page.wait_for_timeout(1500)
    info = page.evaluate("""() => {
      const dimg = document.getElementById('dimg');
      const wrap = document.querySelector('.dimg-wrap');
      const grid = document.querySelector('.detail-grid');
      const cs = getComputedStyle(dimg);
      const r = dimg.getBoundingClientRect();
      const wr = wrap.getBoundingClientRect();
      const gr = grid.getBoundingClientRect();
      return {
        vw: window.innerWidth, vh: window.innerHeight,
        inlineMaxHeight: dimg.style.maxHeight,
        computedMaxHeight: cs.maxHeight,
        dimg: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
        wrap: {x: Math.round(wr.x), y: Math.round(wr.y), w: Math.round(wr.width), h: Math.round(wr.height)},
        grid: {x: Math.round(gr.x), y: Math.round(gr.y), w: Math.round(gr.width), h: Math.round(gr.height)}
      };
    }""")
    import json
    print(json.dumps(info, indent=2))
    browser.close()
