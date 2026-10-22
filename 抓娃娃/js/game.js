/* ============================================================
   game.js — 像素抓娃娃机核心：状态机 + Canvas 渲染
   输入：setMove(0..1) / setPinch(bool)；动作：shuffle() / reset()
   ============================================================ */

const Game = (function () {
  const W = 900;
  const H = 640;

  // 布局常量
  const RAIL_Y = 40;
  const REST_Y = 86;
  const FLOOR_Y = 562;
  const CHUTE = { x: 8, w: 116, center: 64 };
  const MIN_X = 120;
  const MAX_X = 866;

  const DOWN_SPEED = 430;
  const UP_SPEED = 360;
  const MOVE_SPEED = 520; // 横向移动 px/s

  let canvas, ctx;
  let state = "idle";
  let stateT = 0;

  let clawX = 480;
  let clawY = REST_Y;
  let targetX = 480;
  let targetY = 530;
  let openAmt = 1; // 1=张开 0=闭合

  let monsters = [];
  let caught = null;
  let pending = null; // 下爪时锁定的目标
  let deposit = null; // 掉进 DROP 口的奖品动画
  let score = 0;
  let popups = [];
  let grabs = 0;
  let hint = true;
  let lastMoveSnd = 0;
  let respawnTimer = -1;
  let missStreak = 0; // 连续空抓次数
  let easyMode = false; // 连续三次空抓后进入降难度模式

  /* ---------------- 初始化怪物堆 ---------------- */
  // 玩偶自主游走范围
  const ROW_MIN = 128;
  const ROW_MAX = 870;
  const DODGE_RADIUS = 115; // 下爪时触发躲避的横向距离

  // 每个玩偶的游走 / 起伏 / 躲避参数
  function moveFields(row) {
    const front = row === 0;
    return {
      wanderRange: (front ? 42 : 34) + Math.random() * (front ? 46 : 34),
      wanderSpeed: (front ? 30 : 24) + Math.random() * 28,
      wanderTarget: 0,
      wanderWait: Math.random() * 1.4,
      bobPhase: Math.random() * Math.PI * 2,
      bobSpeed: 1.1 + Math.random() * 1.5,
      bobRange: (front ? 4 : 3) + Math.random() * (front ? 7 : 5),
      dodgeSpeed: (front ? 105 : 95) + Math.random() * 45,
      reactT: 0.08 + Math.random() * 0.28,
    };
  }

  function makeMonsters() {
    const names = SpriteLib.allNames();
    const arr = [];
    // 后排（小、靠后、略高）
    const backCount = 9;
    for (let i = 0; i < backCount; i++) {
      const x =
        132 + (i / (backCount - 1)) * 730 + (Math.random() * 44 - 22);
      const cx = Math.max(ROW_MIN, Math.min(ROW_MAX, x));
      const f = moveFields(1);
      f.wanderTarget = cx;
      arr.push({
        type: names[Math.floor(Math.random() * names.length)],
        x: cx,
        baseX: x,
        baseY: 550 + (Math.random() * 10 - 4),
        y: 550 + (Math.random() * 10 - 4),
        pixel: 2,
        row: 1,
        ...f,
      });
    }
    // 前排（大、靠前）
    const frontCount = 9;
    for (let i = 0; i < frontCount; i++) {
      const x =
        150 + (i / (frontCount - 1)) * 712 + (Math.random() * 40 - 20);
      const f = moveFields(0);
      f.wanderTarget = x;
      arr.push({
        type: names[Math.floor(Math.random() * names.length)],
        x,
        baseX: x,
        baseY: 572 + (Math.random() * 8 - 4),
        y: 572 + (Math.random() * 8 - 4),
        pixel: 3,
        row: 0,
        ...f,
      });
    }
    // 随机选 4 个玩偶做大幅度上下跳跃
    const idxs = arr.map((_, i) => i);
    for (let i = idxs.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [idxs[i], idxs[j]] = [idxs[j], idxs[i]];
    }
    for (let i = 0; i < 4; i++) {
      const m = arr[idxs[i]];
      m.hopper = true;
      m.hopT = Math.random() * 2;
      if (i < 2) {
        // 两个超级跳跃款：跃起高度超过画布总高（640）的一半
        m.hopPeriod = 2.4 + Math.random() * 1.0;
        m.hopHeight = 340 + Math.random() * 50; // 340–390
      } else {
        m.hopPeriod = 1.4 + Math.random() * 1.2;
        m.hopHeight = 32 + Math.random() * 30;
      }
    }
    return arr;
  }

  // 选取新的水平游走目标
  function pickWander(m) {
    const lo = Math.max(ROW_MIN, m.baseX - m.wanderRange);
    const hi = Math.min(ROW_MAX, m.baseX + m.wanderRange);
    m.wanderTarget = lo + Math.random() * Math.max(1, hi - lo);
    m.wanderWait = 0.4 + Math.random() * 1.4;
  }

  function remaining() {
    return monsters.filter((m) => !m.caught).length;
  }

  /* ---------------- 输入 ---------------- */
  function setMove(nx) {
    // 仅在 idle / return 时跟随手
    if (state === "idle" || state === "return") {
      targetX = MIN_X + Math.max(0, Math.min(1, nx)) * (MAX_X - MIN_X);
      // 移动滴答声
      const now = performance.now();
      if (state === "idle" && Math.abs(targetX - clawX) > 6 && now - lastMoveSnd > 260) {
        SoundFX.move();
        lastMoveSnd = now;
      }
    }
  }

  let pinchPrev = false;
  function setPinch(on) {
    if (on && !pinchPrev) startDrop();
    pinchPrev = on;
  }

  function startDrop() {
    if (state !== "idle" || remaining() === 0) return;
    hint = false;
    // 选最近的奖品决定下爪深度
    const target = nearestMonster(clawX, 52);
    if (target) {
      const s = SpriteLib.size(target.type, target.pixel);
      targetY = target.y - s.h + 26;
    } else {
      targetY = 540;
    }
    targetY = Math.max(470, Math.min(545, targetY));
    state = "down";
    stateT = 0;
    SoundFX.drop();
  }

  function nearestMonster(x, radius) {
    let best = null;
    let bestD = radius;
    for (const m of monsters) {
      if (m.caught) continue;
      const d = Math.abs(m.x - x);
      if (d < bestD) {
        bestD = d;
        best = m;
      }
    }
    return best;
  }

  /* ---------------- 按钮动作 ---------------- */
  function shuffle() {
    SoundFX.shuffle();
    const names = SpriteLib.allNames();
    const back = monsters.filter((m) => m.row === 1);
    const front = monsters.filter((m) => m.row === 0);
    back.forEach((m, i) => {
      m.type = names[Math.floor(Math.random() * names.length)];
      m.baseX =
        132 + (i / (back.length - 1)) * 730 + (Math.random() * 44 - 22);
      m.baseX = Math.max(ROW_MIN, Math.min(ROW_MAX, m.baseX));
    });
    front.forEach((m, i) => {
      m.type = names[Math.floor(Math.random() * names.length)];
      m.baseX =
        150 + (i / (front.length - 1)) * 712 + (Math.random() * 40 - 20);
    });
    // 快速归位动画
    monsters.forEach((m, i) => {
      m.tween = { from: m.x, to: m.baseX, t: 0, delay: i * 0.02 };
      m.wanderTarget = m.baseX;
      m.wanderWait = Math.random() * 1.2;
    });
  }

  function reset() {
    SoundFX.reset();
    score = 0;
    grabs = 0;
    popups = [];
    caught = null;
    pending = null;
    deposit = null;
    state = "idle";
    stateT = 0;
    clawY = REST_Y;
    clawX = 480;
    targetX = 480;
    openAmt = 1;
    monsters = makeMonsters();
    hint = true;
    respawnTimer = -1;
    missStreak = 0;
    easyMode = false;
  }

  /* ---------------- 状态机更新 ---------------- */
  function update(dt) {
    stateT += dt;

    // 玩偶：归位动画 / 自主游走 / 下爪躲避
    const clawActive = state === "down" || state === "close";
    for (const m of monsters) {
      if (m.tween) {
        if (stateT >= m.tween.delay) {
          m.tween.t += dt * 4;
          const t = Math.min(1, m.tween.t);
          m.x = m.tween.from + (m.tween.to - m.tween.from) * easeOut(t);
          if (t >= 1) {
            m.tween = null;
            m.wanderTarget = m.x;
            m.wanderWait = 0.2 + Math.random();
          }
        }
      } else if (!m.caught) {
        // 垂直运动：跳跃玩偶大起大落，其余小幅起伏（降难度时均减弱）
        if (m.hopper) {
          m.hopT += dt;
          if (m.hopT > m.hopPeriod) m.hopT -= m.hopPeriod;
          const p = m.hopT / m.hopPeriod;
          const h = easyMode ? m.hopHeight * 0.4 : m.hopHeight;
          if (p < 0.6) {
            const a = p / 0.6;
            m.y = m.baseY - Math.sin(a * Math.PI) * h;
          } else {
            m.y = m.baseY;
          }
        } else {
          m.bobPhase += dt * m.bobSpeed;
          const bobR = easyMode ? m.bobRange * 0.4 : m.bobRange;
          m.y = m.baseY - (0.5 + 0.5 * Math.sin(m.bobPhase)) * bobR;
        }

        let moved = false;
        // 下爪时附近玩偶横向逃离（降难度时不再躲避）
        if (!easyMode && clawActive && Math.abs(m.x - clawX) < DODGE_RADIUS) {
          if (m.reactT > 0) {
            m.reactT -= dt;
          } else {
            // 远离爪子方向逃；顶到边界则被夹住（可被抓）
            const dir = m.x < clawX ? -1 : 1;
            m.x = approach(m.x, m.x + dir * 1000, m.dodgeSpeed * dt);
            moved = true;
          }
        } else {
          m.reactT = 0.08 + Math.random() * 0.28;
        }

        // 水平游走（左右）
        if (!moved) {
          if (m.wanderWait > 0) {
            m.wanderWait -= dt;
          } else {
            const wSpeed = easyMode ? m.wanderSpeed * 0.4 : m.wanderSpeed;
            m.x = approach(m.x, m.wanderTarget, wSpeed * dt);
            if (Math.abs(m.x - m.wanderTarget) < 2) pickWander(m);
          }
        }
        m.x = Math.max(ROW_MIN, Math.min(ROW_MAX, m.x));
      }
    }

    // 掉入 DROP 口的奖品
    if (deposit) {
      deposit.t += dt;
      deposit.y += 360 * dt;
      deposit.rot += dt * 6;
      if (deposit.y > FLOOR_Y + 60) deposit = null;
    }

    // 横向移动（idle / return / toChute）
    if (state === "idle" || state === "return") {
      clawX = approach(clawX, targetX, MOVE_SPEED * dt);
      openAmt = approach(openAmt, 1, dt * 8);
    }

    switch (state) {
      case "down": {
        clawY = approach(clawY, targetY, DOWN_SPEED * dt);
        if (clawY >= targetY - 0.5) {
          pending = nearestMonster(clawX, 50);
          state = "close";
          stateT = 0;
        }
        break;
      }
      case "close": {
        openAmt = approach(openAmt, 0, dt * 12);
        if (!caught && pending && openAmt <= 0.05) {
          caught = pending;
          caught.caught = true;
          pending = null;
        }
        if (stateT > 0.28) {
          pending = null;
          state = "up";
          stateT = 0;
          SoundFX.clack();
          if (caught) {
            SoundFX.rise();
          } else {
            SoundFX.miss();
            if (!easyMode) {
              missStreak++;
              if (missStreak >= 3) {
                easyMode = true;
              }
            }
          }
        }
        break;
      }
      case "up": {
        openAmt = 0;
        clawY = approach(clawY, REST_Y, UP_SPEED * dt);
        if (clawY <= REST_Y + 0.5) {
          state = caught ? "toChute" : "return";
          stateT = 0;
        }
        break;
      }
      case "toChute": {
        clawX = approach(clawX, CHUTE.center, MOVE_SPEED * dt);
        if (Math.abs(clawX - CHUTE.center) < 2) {
          state = "deposit";
          stateT = 0;
        }
        break;
      }
      case "deposit": {
        openAmt = approach(openAmt, 1, dt * 6);
        if (caught && openAmt > 0.6 && !deposit) {
          deposit = {
            type: caught.type,
            pixel: caught.pixel,
            x: clawX,
            y: clawY + 26,
            rot: 0,
            t: 0,
          };
          caught = null;
          addScore();
        }
        if (stateT > 0.7) {
          state = "return";
          stateT = 0;
        }
        break;
      }
      case "return": {
        if (Math.abs(clawX - targetX) < 4) {
          state = "idle";
          stateT = 0;
        }
        break;
      }
    }

    // 全部抓完后自动补货
    if (remaining() === 0 && state === "idle") {
      if (respawnTimer < 0) respawnTimer = 1.4;
      respawnTimer -= dt;
      if (respawnTimer <= 0) {
        monsters = makeMonsters();
        respawnTimer = -1;
        popups.push({
          text: "NEW PRIZES!",
          x: W / 2,
          y: 300,
          life: 1.4,
          max: 1.4,
          color: "#37e0d0",
          size: 20,
        });
      }
    }

    // 弹窗
    popups.forEach((p) => (p.life -= dt));
    popups = popups.filter((p) => p.life > 0);
  }

  function addScore() {
    grabs++;
    score += 100;
    missStreak = 0;
    easyMode = false;
    SoundFX.gotcha();
    popups.push({
      text: "+100",
      x: 400,
      y: 360,
      life: 1.2,
      max: 1.2,
      color: "#e6c15a",
      size: 34,
      rise: 60,
    });
    popups.push({
      text: "GOTCHA!",
      x: 400,
      y: 280,
      life: 1.4,
      max: 1.4,
      color: "#6bffb0",
      size: 24,
      rise: 40,
    });
  }

  /* ---------------- 渲染 ---------------- */
  function draw() {
    // 背景
    ctx.fillStyle = "#070f0b";
    ctx.fillRect(0, 0, W, H);

    // 竖向舱板线（数码绿）
    ctx.strokeStyle = "rgba(47,224,154,0.05)";
    ctx.lineWidth = 2;
    for (let x = 46; x < W; x += 90) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, FLOOR_Y);
      ctx.stroke();
    }

    drawRail();
    drawChute();
    drawFloor();
    drawMonsters();
    drawDeposit();
    drawClaw();
    drawScorePanel();
    drawPopups();
    drawCenterHints();
  }

  function drawRail() {
    // 顶部轨道
    ctx.fillStyle = "#123023";
    ctx.fillRect(0, RAIL_Y - 12, W, 12);
    ctx.fillStyle = "#2fe09a";
    ctx.fillRect(0, RAIL_Y - 13, W, 3);
    ctx.fillStyle = "rgba(47,224,154,0.35)";
    ctx.fillRect(0, RAIL_Y, W, 2);

    // 金色倒三角标记
    ctx.fillStyle = "#e6c15a";
    ctx.beginPath();
    ctx.moveTo(clawX - 10, RAIL_Y - 30);
    ctx.lineTo(clawX + 10, RAIL_Y - 30);
    ctx.lineTo(clawX, RAIL_Y - 18);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = "#20180a";
    ctx.fillRect(clawX - 2, RAIL_Y - 28, 4, 4);
  }

  function drawFloor() {
    ctx.fillStyle = "#203428";
    ctx.fillRect(0, FLOOR_Y, W, H - FLOOR_Y);
    ctx.fillStyle = "#345242";
    ctx.fillRect(0, FLOOR_Y, W, 6);
    ctx.fillStyle = "#16261c";
    for (let x = 10; x < W; x += 26) {
      ctx.fillRect(x, FLOOR_Y + 14, 14, 4);
    }
  }

  function drawChute() {
    const x = CHUTE.x;
    const w = CHUTE.w;
    // 黑色投递口
    ctx.fillStyle = "#040a07";
    ctx.fillRect(x, FLOOR_Y - 120, w, 120 + (H - FLOOR_Y));
    ctx.strokeStyle = "#e6c15a";
    ctx.lineWidth = 3;
    ctx.strokeRect(x, FLOOR_Y - 120, w, 120 + (H - FLOOR_Y));
    // DROP 标签
    ctx.font = '16px "Press Start 2P", monospace';
    ctx.fillStyle = "#e6c15a";
    ctx.textAlign = "center";
    ctx.fillText("DROP", x + w / 2, FLOOR_Y + 44);
    ctx.textAlign = "left";
  }

  function drawMonsters() {
    // 阴影（跳跃时阴影留在地面并随高度缩小）
    ctx.fillStyle = "rgba(0,0,0,0.3)";
    for (const m of monsters) {
      if (m.caught) continue;
      const s = SpriteLib.size(m.type, m.pixel);
      const lift = Math.max(0, m.baseY - m.y);
      const rx = Math.max(6, s.w * 0.42 * (1 - lift / 220));
      ctx.beginPath();
      ctx.ellipse(m.x, m.baseY + 4, rx, 6, 0, 0, Math.PI * 2);
      ctx.fill();
    }
    // 后排
    for (const m of monsters) {
      if (m.row !== 1 || m.caught) continue;
      SpriteLib.draw(ctx, m.type, m.x, m.y, m.pixel);
    }
    // 前排
    for (const m of monsters) {
      if (m.row !== 0 || m.caught) continue;
      SpriteLib.draw(ctx, m.type, m.x, m.y, m.pixel);
    }
    // 被抓住的奖品挂在爪下
    if (caught) {
      SpriteLib.draw(ctx, caught.type, clawX, clawY + 30 + (openAmt * 8), caught.pixel);
    }
  }

  function drawDeposit() {
    if (!deposit) return;
    const { w, h } = SpriteLib.size(deposit.type, deposit.pixel);
    ctx.save();
    ctx.translate(deposit.x, deposit.y);
    ctx.rotate(Math.sin(deposit.rot) * 0.3);
    ctx.drawImage(
      SpriteLib.render(deposit.type, deposit.pixel),
      -w / 2,
      -h
    );
    ctx.restore();
  }

  function drawClaw() {
    const x = clawX;
    const y = clawY;

    // 钢缆
    ctx.strokeStyle = "#7fb6a0";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x, RAIL_Y);
    ctx.lineTo(x, y - 8);
    ctx.stroke();
    ctx.strokeStyle = "rgba(140,242,196,0.3)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x - 1, RAIL_Y);
    ctx.lineTo(x - 1, y - 8);
    ctx.stroke();

    // 爪头外壳（青铜数码绿）
    ctx.fillStyle = "#35c98f";
    ctx.fillRect(x - 15, y - 12, 30, 16);
    ctx.fillStyle = "#1b6e50";
    ctx.fillRect(x - 15, y + 2, 30, 4);
    ctx.fillStyle = "#9cf0c8";
    ctx.fillRect(x - 15, y - 12, 30, 3);
    ctx.fillStyle = "#072018";
    ctx.fillRect(x - 4, y - 6, 8, 8);

    // 三只爪（左、右、后）
    const spread = 6 + openAmt * 16;
    const len = 26;
    const baseY = y + 2;
    // 后爪（中间，略暗略短）
    drawProng(x, 0, 6, baseY, len - 4, 0, "#1f8a66");
    // 左、右前爪
    drawProng(x, -10, -spread, baseY, len, 1);
    drawProng(x, 10, spread, baseY, len, -1);
  }

  function drawProng(x, px, tipOffset, baseY, len, hookDir, color) {
    // 以中线为基准，px 为根部偏移，tipOffset 为尖端相对偏移
    const main = color || "#35c98f";
    ctx.lineCap = "butt";
    // 深色描边
    ctx.strokeStyle = "#0e3526";
    ctx.lineWidth = 8;
    ctx.beginPath();
    ctx.moveTo(x + px, baseY);
    ctx.lineTo(x + tipOffset, baseY + len);
    ctx.stroke();
    // 主色
    ctx.strokeStyle = main;
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(x + px, baseY);
    ctx.lineTo(x + tipOffset, baseY + len);
    ctx.stroke();
    // 末端内钩
    if (hookDir !== 0) {
      ctx.strokeStyle = main;
      ctx.lineWidth = 5;
      ctx.beginPath();
      ctx.moveTo(x + tipOffset, baseY + len);
      ctx.lineTo(x + tipOffset + hookDir * 7, baseY + len + 6);
      ctx.stroke();
    }
  }

  function drawScorePanel() {
    const x = 14;
    const y = 14;
    ctx.fillStyle = "#040a07";
    ctx.fillRect(x, y, 128, 56);
    ctx.strokeStyle = "#2fe09a";
    ctx.lineWidth = 3;
    ctx.strokeRect(x, y, 128, 56);
    ctx.font = '10px "Press Start 2P", monospace';
    ctx.fillStyle = "#8cf2c4";
    ctx.textAlign = "left";
    ctx.fillText("SCORE", x + 12, y + 20);
    ctx.font = '18px "Press Start 2P", monospace';
    ctx.fillStyle = "#ffffff";
    ctx.fillText(String(score).padStart(6, "0"), x + 12, y + 44);
  }

  function drawPopups() {
    for (const p of popups) {
      const t = p.life / p.max;
      const alpha = Math.min(1, t * 1.6);
      const rise = p.rise ? p.rise * (1 - t) : 0;
      ctx.globalAlpha = alpha;
      ctx.font = p.size + 'px "Press Start 2P", monospace';
      ctx.textAlign = "center";
      ctx.fillStyle = "#000";
      ctx.fillText(p.text, p.x + 3, p.y - rise + 3);
      ctx.fillStyle = p.color;
      ctx.fillText(p.text, p.x, p.y - rise);
      ctx.globalAlpha = 1;
      ctx.textAlign = "left";
    }
  }

  function drawCenterHints() {
    if (hint && state === "idle" && grabs === 0) {
      ctx.globalAlpha = 0.55 + Math.sin(performance.now() / 300) * 0.25;
      ctx.font = '14px "Press Start 2P", monospace';
      ctx.textAlign = "center";
      ctx.fillStyle = "#37e0d0";
      ctx.fillText("MOVE YOUR HAND · PINCH TO GRAB", W / 2, 240);
      ctx.globalAlpha = 1;
      ctx.textAlign = "left";
    }
    if (remaining() === 0 && state === "idle") {
      ctx.font = '20px "Press Start 2P", monospace';
      ctx.textAlign = "center";
      ctx.fillStyle = "#e6c15a";
      ctx.fillText("ALL PRIZES COLLECTED!", W / 2, 320);
      ctx.textAlign = "left";
    }
  }

  /* ---------------- 工具 ---------------- */
  function approach(a, b, step) {
    if (a < b) return Math.min(b, a + step);
    return Math.max(b, a - step);
  }
  function easeOut(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  /* ---------------- 主循环 ---------------- */
  let last = 0;
  function loop(ts) {
    const dt = Math.min(0.05, (ts - last) / 1000 || 0);
    last = ts;
    update(dt);
    draw();
    requestAnimationFrame(loop);
  }

  function init(cv) {
    canvas = cv;
    ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false;
    monsters = makeMonsters();
    requestAnimationFrame(loop);
  }

  return { init, setMove, setPinch, shuffle, reset };
})();
