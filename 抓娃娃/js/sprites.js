/* ============================================================
   sprites.js — 三星堆青铜文物像素精灵（24x24 精细网格）
   参考：青铜大面具 / 纵目面具 / 高冠人头像 / 青铜神鸟 /
        青铜太阳轮 / 青铜大立人 / 金面罩
   青铜字符：W 高光  A 亮绿  B 中亮绿  C 铜绿  D 深绿  E 暗绿
             T 土褐  U 深褐  V 孔雀蓝锈  K 眼窝缝隙  M 最深
             G/H/I 金饰
   金面字符：w 金高光  G 亮金  H 金  I 暗金  J 深金
   行宽由 normalize 自动补齐 "."。
   ============================================================ */

const BRONZE = {
  "W": "#eafaf0",
  "A": "#bfeed8",
  "B": "#82dcb0",
  "C": "#4fb085",
  "D": "#2f7a5c",
  "E": "#1c4c39",
  "T": "#b39a6b",
  "U": "#8a7148",
  "V": "#3fc7b2",
  "K": "#0a1710",
  "M": "#050c08",
  "G": "#f0d88a",
  "H": "#d9b44a",
  "I": "#a9862f",
};

const GOLD = {
  "w": "#fff3c0",
  "G": "#f0d88a",
  "H": "#d9b44a",
  "I": "#a9862f",
  "J": "#6f571d",
  "K": "#1a1404",
  "M": "#0b0802",
};

const SPRITES = {
  /* 青铜大面具（翼耳、金眉、大眼、薄嘴） */
  mask: {
    palette: BRONZE,
    rows: [
      "........................",
      "..E..................E..",
      ".DEGGHHHHHHHHHHHHHHGGED.",
      "DEEEBBCCCCCKKCCCCCBBEEED",
      "DEEEBCCCCCCKKCCCCVCBEEED",
      "DEEEBCCCCCCCCCCCCCCBEEED",
      "DEEECBGGGCCCCCCGGGBCEEED",
      "DEKECBKKKKCDDCKKKKBCEKED",
      "DKEECBBKKKDDDDKKKBBCEEKD",
      "DKEECCCKKBDDDDBKKCTCEEKD",
      "DKEECDDCCCCDDCCCVDDCEEKD",
      "DKEECCCCCDBBBDDCCCCCEEKD",
      "DKEECCCCDDABBADDCCCCEEKD",
      "DEKECCCCCKDCCDKCCCCCEKED",
      "DEEECCCBKKKKKKKKBCCCEEED",
      ".DEECCCCBTCBBCCBCCCCEED.",
      "..DECCCVCCCCCCCCCCCCED..",
      "....BDDDDDDDDDDDDDDB....",
      "........................",
      "........................",
      "........................",
      "........................",
      "........................",
      "........................",
    ],
  },
  /* 青铜纵目面具（凸目圆柱、方孔额、大翼耳） */
  zongmu: {
    palette: BRONZE,
    rows: [
      "........................",
      "..E..................E..",
      ".DEG..GHHHHHHHHGB..EGED.",
      ".DEE..BCCCCKKCCCCB.EEED.",
      ".DEE..BCCCCKKCCCCB.EEED.",
      ".DEECBBCCCCCCCCCCBBCEED.",
      ".DEEDDDDDCCCCCCDDDDDEED.",
      ".DKWBCKDCCCDDCCCDKCBWKD.",
      ".DBBCCCBCCCDDCCCBCCCBBD.",
      ".DKWBCKDCCCDDCCCDKCBWKD.",
      ".DEECCCCCCVDDCCCCTCCEED.",
      ".DEECCCDCTBBBDCCDCCCEED.",
      ".DEECCCDDDBCCBDDDCCCEED.",
      ".DEECCCCCKDDDDKCCCCCEED.",
      ".DEECCCBKKKKKKKKBCCCEED.",
      "..DECCCCBCCBBCCBVCCCED..",
      "....CCCCVCCCCCCCCCCC....",
      "....BDDDDDDDDDDDDDDB....",
      "........................",
      "........................",
      "........................",
      "........................",
      "........................",
      "........................",
    ],
  },
  /* 高冠青铜人头像（喇叭形高冠、金饰带） */
  crown: {
    palette: BRONZE,
    rows: [
      "........................",
      "...BCCCCCCCCCCCCCCCCB...",
      "....DDDDDDDDDDDDDDDD....",
      "......BCCCCCCCCB........",
      ".......BCCCCCCCB........",
      ".......CVCCCCCCC........",
      "........BCCCCCCB........",
      "........DDDDDDDD........",
      ".......BGHHHHHHGB.......",
      ".......BCCCCCCCCB.......",
      "..EEBBCCCCCCCCCCCCBBEE..",
      ".DEECBGGGCCCCCCGGGBCEED.",
      "DEEECBKKKKCDDCKKKKBCEEED",
      "DEEECBBKKKDDDDKKKBBCEEED",
      "DEEECDDCCDBBBDDCVDDCEEED",
      "DEEECCCCDDABBADDCCCCEEED",
      ".DEECCCBKKKKKKKKBCCCEED.",
      "..DEBCCCCCTCCCCCCCCBED..",
      "......BCCCCCCCVB........",
      "........BCCCCCCB........",
      ".........BCCCB..........",
      "........................",
      "........................",
      "........................",
    ],
  },
  /* 青铜神鸟（花冠、钩喙、同心目、卷翅、长羽） */
  bird: {
    palette: BRONZE,
    rows: [
      "........................",
      ".....B.BB...............",
      ".....BCBCBCB............",
      "....BCCCCCCB............",
      "....BCCCCT.........BCCB.",
      "....CCCCCCC...BCCCCCCCB.",
      ".BBBBCKKKCC...BCCCCCCCB.",
      ".BKKCCKBKCC...BCCCCCCCB.",
      "..BBBCCKKKCC..BCCCCCCCB.",
      "....CDBCCCC...BCCCCCCCB.",
      ".....BCCKKKKCCBCBKKKKCB.",
      ".....CCCKBBKCCBKKBKKKCB.",
      ".....CCCKBBKCCBKKBBKKCB.",
      ".....BCCKKKKCDBKKKKCCTB.",
      ".....CCCCCCCDDBCCCCB....",
      ".......BCCCVCBCCCBCCBB..",
      ".......BCB.BCCCBCCBCCBCC",
      "........DB.BCCCBCCBCCBCC",
      "........KK.BBCCCCCBCCBCC",
      ".....BKKK...BCCBCVBCCBCC",
      "........BKK.BCCBCCBCCBCC",
      "..............BCCBCCBCCB",
      "........................",
      "........................",
    ],
  },
  /* 青铜太阳轮（圆环、五辐、金铆钉、金毂） */
  sun: {
    palette: BRONZE,
    rows: [
      "........................",
      "........................",
      "........BBBBGCCC........",
      "......BBBBBBCCCCCC......",
      ".....BBBB..CC..CCCC.....",
      "....BBB....CC....CCC....",
      "...BBB.....CC.....CCC...",
      "...BB......CC......CC...",
      "..BBBC.....CD.....DCCC..",
      "..BGCCCCC..CD..DDDDDGC..",
      "..BBCCCCCCwGGHDDDDDDCC..",
      "..BB..CCCCGKHIDDDD..CC..",
      "..CC......GHHI......DD..",
      "..CC.....CHIIID.....DD..",
      "..CC....CCCCDDDD....DD..",
      "..CCC...CCC..DDD...DDD..",
      "...CC..CCCC..DDDD..DD...",
      "...CCCCCCC....DDDDDDD...",
      "....CCCCC......DDDDD....",
      ".....CGCC......DDGD.....",
      "......CCCCCCDDDDDD......",
      "........CCCCDDDD........",
      "........................",
      "........................",
    ],
  },
  /* 青铜大立人（花冠、巨手环抱、长袍、底座） */
  figure: {
    palette: BRONZE,
    rows: [
      "........................",
      "........BCCBCCB.........",
      ".........CCCCCC.........",
      "........BCCCCCCB........",
      "......E.BCCCCCCB.E......",
      ".....DEEBCCCCCCBEED.....",
      ".....DEECBKKKKBCEED.....",
      ".....BBBCCKKKKCCCCB.....",
      "....BBBBBCCCCCCCCEED....",
      "....BBBKKBBBCCCCCEED....",
      "....BBBKKBCCCDCCCEED....",
      "....BBBCCCCCCCBBCCDD....",
      "....BCCCBCCCCBBBBBCC....",
      "....BCC.BCCCBBBCTBCC....",
      "......BBCCCCCCCCCCBB....",
      "......BDVCDCCDCCDB......",
      "......CDCCBCCBCCDC......",
      "......CDCCDCCDVCDC......",
      ".......CBKKCCKKBC.......",
      "........BTCBBCCB........",
      ".......BCCCCCCCCCB......",
      ".......BKKKKKKKKKB......",
      "......BDDDDDDDDDDB......",
      "........................",
    ],
  },
  /* 金面罩（金色大面具） */
  goldmask: {
    palette: GOLD,
    rows: [
      "........................",
      "..H..................H..",
      ".IHGGHHHHHHHHHHHHHHGGHI.",
      "IHHHGGHHHHHKKHHHHHGGHHHI",
      "IHHHGHHHHHHKKHHHHGHGHHHI",
      "IHHHGHHHHHHHHHHHHHHGHHHI",
      "IHHHHGGGGHHHHHHGGGGHHHHI",
      "IHKHHGKKKKHIIHKKKKGHHKHI",
      "IKHHHGGKKKIIIIKKKGGHHHKI",
      "IKHHHHHKKGIIIIGKKHHHHHKI",
      "IKHHHIIHHHHIIHHHGIIHHHKI",
      "IKHHHHHHHIGGGIIHHHHHHHKI",
      "IKHHHHHHIIwGGwIIHHHHHHKI",
      "IHKHHHHHHKIHHIKHHHHHHKHI",
      "IHHHHHHGKKKKKKKKGHHHHHHI",
      ".IHHHHHHGHHGGHHGHHHHHHI.",
      "..IHHHHGHHHHHHHHHHHHHI..",
      "....GIIIIIIIIIIIIIIG....",
      "........................",
      "........................",
      "........................",
      "........................",
      "........................",
      "........................",
    ],
  },
};

const SpriteLib = (function () {
  function normalize(sprite) {
    let width = 0;
    const rows = sprite.rows.map((r) => {
      width = Math.max(width, r.length);
      return r;
    });
    const grid = rows.map((r) => r.padEnd(width, "."));
    return { width, height: grid.length, grid, palette: sprite.palette };
  }

  const normalized = {};
  const cache = new Map();

  function get(name) {
    if (!normalized[name]) normalized[name] = normalize(SPRITES[name]);
    return normalized[name];
  }

  function render(name, pixel) {
    const key = name + "@" + pixel;
    if (cache.has(key)) return cache.get(key);

    const { width, height, grid, palette } = get(name);
    const cv = document.createElement("canvas");
    cv.width = width * pixel;
    cv.height = height * pixel;
    const ctx = cv.getContext("2d");
    ctx.imageSmoothingEnabled = false;

    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const ch = grid[y][x];
        if (ch === "." || ch === " ") continue;
        const color = palette[ch];
        if (!color) continue;
        ctx.fillStyle = color;
        ctx.fillRect(x * pixel, y * pixel, pixel, pixel);
      }
    }
    cache.set(key, cv);
    return cv;
  }

  function draw(ctx, name, cx, bottomY, pixel) {
    const cv = render(name, pixel);
    ctx.drawImage(cv, Math.round(cx - cv.width / 2), Math.round(bottomY - cv.height));
    return { w: cv.width, h: cv.height };
  }

  function size(name, pixel) {
    const n = get(name);
    return { w: n.width * pixel, h: n.height * pixel };
  }

  function allNames() {
    return Object.keys(SPRITES);
  }

  return { draw, render, size, allNames };
})();
