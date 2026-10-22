# -*- coding: utf-8 -*-
"""用 Chrome headless --dump-dom 读取详情页元素的真实计算尺寸。"""
import os, subprocess, json, re

proj = os.path.dirname(os.path.abspath(__file__))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

with open(os.path.join(proj, "三星堆手电筒.html"), "r", encoding="utf-8") as f:
    html = f.read()

measure_js = """
<div id="measure-out" style="position:fixed;top:0;left:0;z-index:99999;color:#fff;font-size:12px;"></div>
<script>
window.addEventListener('load', function(){
  function collect(idx){
    renderDetail(idx);
    document.getElementById('viewDetail').classList.add('show');
    var dimg = document.getElementById('dimg');
    var wrap = document.querySelector('.dimg-wrap');
    var grid = document.querySelector('.detail-grid');
    var cs = getComputedStyle(dimg);
    var r = dimg.getBoundingClientRect();
    var wr = wrap.getBoundingClientRect();
    var gr = grid.getBoundingClientRect();
    var dc = document.querySelector('.dcontent');
    var dcr = dc.getBoundingClientRect();
    var wcs = getComputedStyle(wrap);
    var gcs = getComputedStyle(grid);
    return {
      idx: idx,
      vw: window.innerWidth, vh: window.innerHeight,
      inlineMaxH: dimg.style.maxHeight,
      computedMaxH: cs.maxHeight,
      gridClasses: grid.className,
      gridH: Math.round(gr.height),
      gridComputedH: gcs.height,
      gridTemplateRows: gcs.gridTemplateRows,
      gridTemplateCols: gcs.gridTemplateColumns,
      wrapAlignSelf: wcs.alignSelf,
      wrapComputedH: wcs.height,
      dimg: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
      wrap: {x: Math.round(wr.x), y: Math.round(wr.y), w: Math.round(wr.width), h: Math.round(wr.height)},
      dcontent: {x: Math.round(dcr.x), y: Math.round(dcr.y), w: Math.round(dcr.width), h: Math.round(dcr.height)}
    };
  }
  setTimeout(function(){
    var out = [];
    for (var i=0;i<4;i++){ out.push(collect(i)); }
    document.getElementById('measure-out').textContent = JSON.stringify(out);
  }, 300);
});
</script>
</body>"""

html2 = html.replace("</body>", measure_js, 1)
tmp = os.path.join(proj, "_measure.html")
with open(tmp, "w", encoding="utf-8", newline="") as f:
    f.write(html2)

res = subprocess.run(
    [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
     "--force-device-scale-factor=1", "--window-size=1440,900",
     "--virtual-time-budget=3000", "--dump-dom",
     "file:///" + tmp.replace("\\", "/")],
    capture_output=True, text=True, timeout=90, encoding="utf-8"
)

m = re.search(r'id="measure-out"[^>]*>(.*?)</div>', res.stdout, re.S)
if not m:
    print("未取到测量结果")
    print(res.stdout[-500:])
else:
    data = json.loads(m.group(1))
    for d in data:
        print("--- 文物", d["idx"], " 视口", d["vw"], "x", d["vh"])
        print("   内联maxH:", d["inlineMaxH"], " computed:", d["computedMaxH"])
        print("   dimg:", d["dimg"])
        print("   wrap:", d["wrap"])
