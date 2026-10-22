/* ============================================================
   handtracking.js — MediaPipe Hands 手势识别
   食指 X 坐标 -> 爪子左右移动；拇指+食指捏合 -> 下爪
   失败时抛出异常，由 main.js 回退到鼠标 / 触屏模式
   ============================================================ */

const HandTracker = (function () {
  const MP_VERSION = "0.4.1675469240";

  // 手部骨架连线（兜底，若全局 HAND_CONNECTIONS 未加载则使用）
  const FALLBACK_CONNECTIONS = [
    [0, 1], [1, 2], [2, 3], [3, 4],
    [0, 5], [5, 6], [6, 7], [7, 8],
    [5, 9], [9, 10], [10, 11], [11, 12],
    [9, 13], [13, 14], [14, 15], [15, 16],
    [13, 17], [17, 18], [18, 19], [19, 20],
    [0, 17],
  ];

  let video, octx, hands;
  let running = false;
  let stream = null;
  let smoothX = null;
  let ratioEMA = 1;
  let pinchOn = false;
  let lastFrame = 0;

  function dist(a, b) {
    return Math.hypot(a.x - b.x, a.y - b.y);
  }

  async function start(opts) {
    video = opts.video;
    const overlay = opts.overlay;
    octx = overlay.getContext("2d");
    overlay.width = 640;
    overlay.height = 480;
    const onData = opts.onData;
    const onStatus = opts.onStatus;

    if (typeof Hands === "undefined") {
      throw new Error("MediaPipe 脚本加载失败（可能未联网）");
    }
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error("当前浏览器不支持摄像头 API");
    }

    onStatus("requesting");
    stream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 640 },
        height: { ideal: 480 },
        facingMode: "user",
      },
      audio: false,
    });
    video.srcObject = stream;
    await video.play();

    hands = new Hands({
      locateFile: (f) =>
        `https://cdn.jsdelivr.net/npm/@mediapipe/hands@${MP_VERSION}/${f}`,
    });
    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 0,
      minDetectionConfidence: 0.6,
      minTrackingConfidence: 0.5,
      selfieMode: false,
    });
    hands.onResults((results) => onResults(results, onData));

    running = true;
    onStatus("running");
    loop();
  }

  async function loop() {
    if (!running) return;
    if (video.readyState >= 2) {
      try {
        await hands.send({ image: video });
      } catch (e) {
        /* 单帧识别失败可忽略 */
      }
    }
    requestAnimationFrame(loop);
  }

  function onResults(results, onData) {
    const lm =
      results.multiHandLandmarks && results.multiHandLandmarks[0];
    drawSkeleton(lm);

    if (!lm) {
      pinchOn = false;
      onData({ found: false });
      return;
    }

    const thumb = lm[4];
    const index = lm[8];
    const wrist = lm[0];
    const middleMcp = lm[9];

    // 镜像：食指 X
    let x = 1 - index.x;
    smoothX = smoothX === null ? x : smoothX * 0.6 + x * 0.4;

    // 捏合比例（拇指-食指距离 / 手掌尺寸），带迟滞防抖
    const handScale = dist(wrist, middleMcp) || 1;
    const ratio = dist(thumb, index) / handScale;
    ratioEMA = ratioEMA * 0.7 + ratio * 0.3;
    if (!pinchOn && ratioEMA < 0.32) pinchOn = true;
    else if (pinchOn && ratioEMA > 0.45) pinchOn = false;

    onData({
      found: true,
      x: smoothX,
      pinch: pinchOn,
      landmarks: lm,
    });
  }

  /* 在预览上画骨架（镜像） */
  function drawSkeleton(lm) {
    const W = 640;
    const H = 480;
    octx.clearRect(0, 0, W, H);
    if (!lm) return;

    const px = (p) => (1 - p.x) * W;
    const py = (p) => p.y * H;

    const conns =
      typeof HAND_CONNECTIONS !== "undefined"
        ? HAND_CONNECTIONS
        : FALLBACK_CONNECTIONS;

    octx.lineWidth = 3;
    octx.strokeStyle = "rgba(47,224,154,0.85)";
    octx.beginPath();
    for (const [a, b] of conns) {
      if (!lm[a] || !lm[b]) continue;
      octx.moveTo(px(lm[a]), py(lm[a]));
      octx.lineTo(px(lm[b]), py(lm[b]));
    }
    octx.stroke();

    // 关键点
    for (let i = 0; i < lm.length; i++) {
      const tip = i === 4 || i === 8;
      octx.beginPath();
      octx.arc(px(lm[i]), py(lm[i]), tip ? 6 : 3, 0, Math.PI * 2);
      octx.fillStyle = tip ? "#e6c15a" : "#2fe09a";
      octx.fill();
    }

    // 捏合时在拇指/食指间画绿色圈
    if (pinchOn) {
      const cx = (px(lm[4]) + px(lm[8])) / 2;
      const cy = (py(lm[4]) + py(lm[8])) / 2;
      octx.beginPath();
      octx.arc(cx, cy, 14, 0, Math.PI * 2);
      octx.strokeStyle = "#6bffb0";
      octx.lineWidth = 4;
      octx.stroke();
    }
  }

  function stop() {
    running = false;
    if (stream) {
      stream.getTracks().forEach((t) => t.stop());
      stream = null;
    }
  }

  return { start, stop };
})();
