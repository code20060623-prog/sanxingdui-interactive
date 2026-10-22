/* ============================================================
   audio.js — 用 WebAudio 合成的 8-bit 音效，无需任何音频文件
   ============================================================ */

const SoundFX = (function () {
  let ctx = null;
  let muted = false;

  function ensure() {
    if (!ctx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (AC) ctx = new AC();
    }
    if (ctx && ctx.state === "suspended") ctx.resume();
    return ctx;
  }

  /* 单个方波音符 */
  function tone(freq, start, dur, type, vol) {
    const ac = ctx;
    const osc = ac.createOscillator();
    const gain = ac.createGain();
    osc.type = type || "square";
    osc.frequency.setValueAtTime(freq, start);
    gain.gain.setValueAtTime(vol || 0.08, start);
    gain.gain.exponentialRampToValueAtTime(0.0001, start + dur);
    osc.connect(gain);
    gain.connect(ac.destination);
    osc.start(start);
    osc.stop(start + dur + 0.02);
  }

  /* 频率滑动 */
  function sweep(f1, f2, dur, type, vol) {
    const ac = ctx;
    const t = ac.currentTime;
    const osc = ac.createOscillator();
    const gain = ac.createGain();
    osc.type = type || "square";
    osc.frequency.setValueAtTime(f1, t);
    osc.frequency.exponentialRampToValueAtTime(f2, t + dur);
    gain.gain.setValueAtTime(vol || 0.06, t);
    gain.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    osc.connect(gain);
    gain.connect(ac.destination);
    osc.start(t);
    osc.stop(t + dur + 0.02);
  }

  /* 短促噪声（爪子咬合机械声） */
  function noise(dur, vol) {
    const ac = ctx;
    const bufferSize = Math.floor(ac.sampleRate * dur);
    const buffer = ac.createBuffer(1, bufferSize, ac.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = (Math.random() * 2 - 1) * (1 - i / bufferSize);
    }
    const src = ac.createBufferSource();
    src.buffer = buffer;
    const gain = ac.createGain();
    gain.gain.setValueAtTime(vol || 0.12, ac.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, ac.currentTime + dur);
    src.connect(gain);
    gain.connect(ac.destination);
    src.start();
  }

  const api = {
    unlock() {
      ensure();
    },
    setMuted(m) {
      muted = m;
    },
    isMuted() {
      return muted;
    },
    move() {
      if (muted) return;
      const ac = ensure();
      if (!ac) return;
      tone(220, ac.currentTime, 0.03, "square", 0.02);
    },
    drop() {
      if (muted) return;
      const ac = ensure();
      if (!ac) return;
      sweep(600, 180, 0.5, "sawtooth", 0.05);
    },
    clack() {
      if (muted) return;
      const ac = ensure();
      if (!ac) return;
      noise(0.09, 0.15);
      tone(140, ac.currentTime, 0.08, "square", 0.08);
    },
    rise() {
      if (muted) return;
      const ac = ensure();
      if (!ac) return;
      sweep(200, 520, 0.45, "square", 0.04);
    },
    gotcha() {
      if (muted) return;
      const ac = ensure();
      if (!ac) return;
      const t = ac.currentTime;
      const notes = [523.25, 659.25, 783.99, 1046.5]; // C5 E5 G5 C6
      notes.forEach((f, i) => tone(f, t + i * 0.09, 0.16, "square", 0.09));
    },
    miss() {
      if (muted) return;
      const ac = ensure();
      if (!ac) return;
      const t = ac.currentTime;
      tone(300, t, 0.12, "sawtooth", 0.05);
      tone(200, t + 0.12, 0.18, "sawtooth", 0.05);
    },
    shuffle() {
      if (muted) return;
      const ac = ensure();
      if (!ac) return;
      sweep(300, 900, 0.25, "square", 0.05);
      setTimeout(() => {
        if (!muted) sweep(900, 300, 0.25, "square", 0.05);
      }, 220);
    },
    reset() {
      if (muted) return;
      const ac = ensure();
      if (!ac) return;
      sweep(700, 200, 0.3, "triangle", 0.06);
    },
    start() {
      if (muted) return;
      const ac = ensure();
      if (!ac) return;
      const t = ac.currentTime;
      [440, 554, 659, 880].forEach((f, i) =>
        tone(f, t + i * 0.07, 0.12, "square", 0.07)
      );
    },
  };

  return api;
})();
