// 验证 isPeace / isFist 手势判定
function mpDist(a, b) {
  const dx = a.x - b.x, dy = a.y - b.y, dz = (a.z || 0) - (b.z || 0);
  return Math.sqrt(dx * dx + dy * dy + dz * dz);
}
function isFist(lm) {
  const w = lm[0];
  let bent = 0;
  const pairs = [[8, 5], [12, 9], [16, 13], [20, 17]];
  for (const [tip, mcp] of pairs) {
    if (mpDist(lm[tip], w) < mpDist(lm[mcp], w) * 1.1) bent++;
  }
  return bent >= 3;
}
function isPeace(lm) {
  const w = lm[0];
  const ext = (tip, pip) => mpDist(lm[tip], w) > mpDist(lm[pip], w) * 1.12;
  const bend = (tip, pip) => mpDist(lm[tip], w) < mpDist(lm[pip], w) * 1.08;
  if (!(ext(8, 6) && ext(12, 10))) return false;
  if (!(bend(16, 14) && bend(20, 18))) return false;
  if (mpDist(lm[8], lm[12]) < mpDist(lm[6], lm[10]) * 1.25) return false;
  return true;
}

// ---- 基础手掌 ----
const base = {
  0: {x:0.5,y:0.85},
  1:{x:0.40,y:0.80}, 2:{x:0.36,y:0.76}, 3:{x:0.33,y:0.73}, 4:{x:0.33,y:0.70},
  5:{x:0.42,y:0.70}, 9:{x:0.50,y:0.68}, 13:{x:0.58,y:0.70}, 17:{x:0.66,y:0.74}
};
// 伸直手指
const straight = {
  i: {6:{x:0.40,y:0.56}, 7:{x:0.38,y:0.42}, 8:{x:0.36,y:0.28}},
  m: {10:{x:0.50,y:0.54}, 11:{x:0.50,y:0.40}, 12:{x:0.50,y:0.26}},
  a: {14:{x:0.58,y:0.56}, 15:{x:0.60,y:0.42}, 16:{x:0.62,y:0.28}},
  p: {18:{x:0.68,y:0.62}, 19:{x:0.70,y:0.50}, 20:{x:0.72,y:0.38}}
};
// 弯曲手指（指尖向掌心/手腕卷拢）
const bent = {
  i: {6:{x:0.42,y:0.74}, 7:{x:0.42,y:0.80}, 8:{x:0.44,y:0.82}},
  m: {10:{x:0.50,y:0.72}, 11:{x:0.50,y:0.78}, 12:{x:0.50,y:0.82}},
  a: {14:{x:0.58,y:0.74}, 15:{x:0.58,y:0.80}, 16:{x:0.56,y:0.82}},
  p: {18:{x:0.66,y:0.78}, 19:{x:0.66,y:0.82}, 20:{x:0.64,y:0.83}}
};
function build(i,m,a,p) {
  const lm = Object.assign({}, base);
  for (const k in i) lm[k]=i[k];
  for (const k in m) lm[k]=m[k];
  for (const k in a) lm[k]=a[k];
  for (const k in p) lm[k]=p[k];
  return lm;
}

// 并拢两指（食、中指朝同一方向）
const togetherI = {6:{x:0.44,y:0.56},7:{x:0.46,y:0.42},8:{x:0.48,y:0.28}};
const togetherM = {10:{x:0.50,y:0.54},11:{x:0.50,y:0.40},12:{x:0.50,y:0.26}};

const cases = [
  ['剪刀手✌',        build(straight.i,straight.m,bent.a,bent.p),  true],
  ['张开手掌',        build(straight.i,straight.m,straight.a,straight.p), false],
  ['握拳',           build(bent.i,bent.m,bent.a,bent.p), false],
  ['两指并拢(非V)',   build(togetherI,togetherM,bent.a,bent.p), false],
  ['只伸食指',        build(straight.i,bent.m,bent.a,bent.p), false],
  ['三指(食中无名)',  build(straight.i,straight.m,straight.a,bent.p), false],
];

let pass = 0;
for (const [name, lm, expect] of cases) {
  const got = isPeace(lm);
  const fist = isFist(lm);
  const ok = got === expect;
  if (ok) pass++;
  console.log((ok?'PASS':'FAIL'), name, '| isPeace:', got, '| isFist:', fist);
}
console.log('---\n通过 %d/%d', pass, cases.length);
