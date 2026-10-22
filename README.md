# 三星堆交互 · Sanxingdui Interactive

三个基于手势/摄像头互动的三星堆主题 Web 作品。

## 作品列表

| 作品 | 说明 | 在线预览 (Cloudflare Pages) |
| --- | --- | --- |
| 三星堆手电筒互动 | 用身体姿态点亮三星堆文物，探索神秘青铜世界（单文件，自包含） | https://sanxingdui-torch.pages.dev |
| 抓娃娃 | 手势控制的抓娃娃机，把三星堆萌物带回家（HTML + CSS + JS，使用 MediaPipe Hands） | https://sanxingdui-claw.pages.dev |
| 赛博三星堆跑酷 | 赛博朋克风格三星堆跑酷，手势控制跳跃/滑行/速度（单文件，自包含） | https://sanxingdui-runner.pages.dev |

## 总入口页

https://sanxingdui-home.pages.dev

## 目录结构

- `三星堆手电筒互动/` — 手电筒互动作品（含源码与开发脚本）
- `抓娃娃/` — 抓娃娃作品（index.html + css + js）
- `赛博三星堆跑酷/` — 跑酷作品（含源码与开发脚本）
- `_deploy/` — Cloudflare Pages 部署目录（torch / claw / runner / home，未纳入 Git 版本控制）

## 技术说明

- 三个作品均可在浏览器直接运行；手电筒与跑酷为单文件自包含（图片 base64 内嵌），抓娃娃依赖 `@mediapipe/hands` CDN 与本地 css/js。
- 摄像头权限：作品需要浏览器摄像头/手势识别权限，请允许 camera 权限后使用。
