/* ============================================================
   main.js — 接线：启动游戏、手势/鼠标/触屏控制、面板状态
   ============================================================ */

(function () {
  const canvas = document.getElementById("game");
  const video = document.getElementById("cam");
  const handCanvas = document.getElementById("handCanvas");
  const overlay = document.getElementById("startOverlay");
  const camError = document.getElementById("camError");
  const camPlaceholder = document.getElementById("camPlaceholder");

  const statusDot = document.getElementById("statusDot");
  const statusText = document.getElementById("statusText");
  const chipMove = document.getElementById("chipMove");
  const chipPinch = document.getElementById("chipPinch");
  const startBtn = document.getElementById("startBtn");
  const mouseBtn = document.getElementById("mouseBtn");
  const shuffleBtn = document.getElementById("shuffleBtn");
  const resetBtn = document.getElementById("resetBtn");
  const muteBtn = document.getElementById("muteBtn");

  let mode = "none"; // hand | mouse | none
  let handFound = false;

  /* 初始化游戏 */
  Game.init(canvas);

  /* ---------------- 面板状态 ---------------- */
  function setStatus(on, text) {
    statusDot.classList.toggle("on", on);
    statusDot.classList.toggle("off", !on);
    statusText.classList.toggle("on", on);
    statusText.textContent = text;
  }

  function setChips(moveActive, pinchActive) {
    chipMove.classList.toggle("active", moveActive && !pinchActive);
    chipPinch.classList.toggle("pinch", pinchActive);
  }

  function onHandData(data) {
    handFound = data.found;
    if (data.found) {
      setStatus(true, "HAND TRACKING ACTIVE");
      Game.setMove(data.x);
      Game.setPinch(data.pinch);
      setChips(true, data.pinch);
    } else {
      setStatus(true, "SHOW YOUR HAND");
      Game.setPinch(false);
      setChips(false, false);
    }
  }

  /* ---------------- 启动手势 ---------------- */
  async function startHand() {
    SoundFX.unlock();
    startBtn.disabled = true;
    startBtn.textContent = "LOADING CAMERA...";
    try {
      await HandTracker.start({
        video,
        overlay: handCanvas,
        onData: onHandData,
        onStatus: (s) => {
          if (s === "requesting") setStatus(false, "REQUESTING CAMERA...");
          if (s === "running") setStatus(true, "HAND TRACKING ACTIVE");
        },
      });
      mode = "hand";
      camPlaceholder.classList.add("hide");
      overlay.classList.add("hidden");
      SoundFX.start();
    } catch (err) {
      console.warn("摄像头/手势启动失败：", err);
      startBtn.disabled = false;
      startBtn.textContent = "▶ ENABLE CAMERA & START";
      camError.textContent =
        "摄像头不可用（" + (err.message || "被拒绝") + "），已切换鼠标模式";
      enterMouseMode();
    }
  }

  function enterMouseMode() {
    SoundFX.unlock();
    mode = "mouse";
    setStatus(true, "MOUSE / TOUCH MODE");
    setChips(true, false);
    camPlaceholder.classList.remove("hide");
    camPlaceholder.querySelector("span").textContent = "MOUSE MODE";
    overlay.classList.add("hidden");
    SoundFX.start();
  }

  startBtn.addEventListener("click", startHand);
  mouseBtn.addEventListener("click", enterMouseMode);

  /* ---------------- 鼠标 / 触屏控制 ---------------- */
  function nxFromClient(clientX) {
    const rect = canvas.getBoundingClientRect();
    return (clientX - rect.left) / rect.width;
  }

  canvas.addEventListener("mousemove", (e) => {
    if (mode !== "mouse") return;
    Game.setMove(nxFromClient(e.clientX));
    setChips(true, e.buttons === 1);
  });
  canvas.addEventListener("mousedown", (e) => {
    if (mode !== "mouse") return;
    Game.setPinch(true);
    setChips(true, true);
  });
  window.addEventListener("mouseup", () => {
    if (mode !== "mouse") return;
    Game.setPinch(false);
    setChips(true, false);
  });

  canvas.addEventListener(
    "touchstart",
    (e) => {
      if (mode !== "mouse") return;
      e.preventDefault();
      const t = e.touches[0];
      Game.setMove(nxFromClient(t.clientX));
      Game.setPinch(true);
      setChips(true, true);
    },
    { passive: false }
  );
  canvas.addEventListener(
    "touchmove",
    (e) => {
      if (mode !== "mouse") return;
      e.preventDefault();
      const t = e.touches[0];
      Game.setMove(nxFromClient(t.clientX));
    },
    { passive: false }
  );
  const touchEnd = (e) => {
    if (mode !== "mouse") return;
    e.preventDefault();
    Game.setPinch(false);
    setChips(true, false);
  };
  canvas.addEventListener("touchend", touchEnd, { passive: false });
  canvas.addEventListener("touchcancel", touchEnd, { passive: false });

  /* ---------------- 键盘备用 ---------------- */
  let keyNx = 0.5;
  let keyHeld = false;
  window.addEventListener("keydown", (e) => {
    if (mode !== "mouse") return;
    if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") {
      keyNx = Math.max(0, keyNx - 0.06);
      Game.setMove(keyNx);
    } else if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") {
      keyNx = Math.min(1, keyNx + 0.06);
      Game.setMove(keyNx);
    } else if ((e.key === " " || e.key === "ArrowDown" || e.key === "s") && !keyHeld) {
      keyHeld = true;
      e.preventDefault();
      Game.setPinch(true);
      setChips(true, true);
    }
  });
  window.addEventListener("keyup", (e) => {
    if (mode !== "mouse") return;
    if (e.key === " " || e.key === "ArrowDown" || e.key === "s") {
      keyHeld = false;
      Game.setPinch(false);
      setChips(true, false);
    }
  });

  /* ---------------- 按钮 ---------------- */
  shuffleBtn.addEventListener("click", () => Game.shuffle());
  resetBtn.addEventListener("click", () => Game.reset());

  muteBtn.addEventListener("click", () => {
    const m = !SoundFX.isMuted();
    SoundFX.setMuted(m);
    muteBtn.textContent = m ? "🔇 SOUND OFF" : "🔊 SOUND ON";
  });

  /* 初始面板状态 */
  setStatus(false, "HAND TRACKING OFFLINE");
  setChips(false, false);
})();
