/* ============================================================
   춘천닭갈비 · 인간형 수탉 파이터 — 관절 리그 (base)
   관절 좌표(뼈대) → 근육 캡슐로 렌더. 정면 기본 포즈.
   캐릭터 좌표계: 폭 300(x 0..300), 키 ~280(y 0..280, 발이 아래).
   window.Dakgalbi.render(pose, scale) → 외곽선까지 합성된 canvas 반환.
   ============================================================ */
(function () {
  const CHAR_W = 300, CHAR_H = 288;

  const C = {
    skin:      "#D0824F",   // 근육 피부(따뜻한 적갈)
    skinDark:  "#A85E33",
    skinLite:  "#E29A68",
    cream:     "#F3E8D4",   // 머리
    creamDark: "#DBC8A8",
    comb:      "#E23B2B",   // 볏/와틀
    combDark:  "#B5261C",
    beak:      "#F4C24E",
    beakDark:  "#D89A2A",
    hackle:    "#DFA23C",
    hackleDk:  "#A8791F",
    feather:   "#C4302F",   // 치마 깃털
    featherDk: "#8E1E22",
    featherLt: "#E0553F",
    boot:      "#F4C24E",
    bootDark:  "#D89A2A",
    eye:       "#221009",
    white:     "#F8F3EA",
    outline:   "#241209",
  };

  // ---- 기본 포즈 (건장·넓은 스탠스, 양팔 위로) --------------------
  const BASE = {
    head: { x: 150, y: 54, r: 42 },
    neck: { x: 150, y: 96 },
    sho:  { L: { x: 100, y: 108 }, R: { x: 200, y: 108 } },
    elb:  { L: { x: 66,  y: 80  }, R: { x: 234, y: 80  } },
    wri:  { L: { x: 84,  y: 34  }, R: { x: 216, y: 34  } },
    hipC: { x: 150, y: 182 },
    hip:  { L: { x: 118, y: 184 }, R: { x: 182, y: 184 } },
    kne:  { L: { x: 106, y: 230 }, R: { x: 194, y: 230 } },
    ank:  { L: { x: 100, y: 276 }, R: { x: 200, y: 276 } },
    breath: 0,   // 숨쉬기용(나중 애니메이션)
  };

  // ---- 저수준 도형 ---------------------------------------------
  function capsule(g, ax, ay, bx, by, wa, wb) {
    const dx = bx - ax, dy = by - ay, len = Math.hypot(dx, dy) || 1;
    const nx = -dy / len, ny = dx / len;
    g.beginPath();
    g.moveTo(ax + nx * wa, ay + ny * wa);
    g.lineTo(bx + nx * wb, by + ny * wb);
    g.lineTo(bx - nx * wb, by - ny * wb);
    g.lineTo(ax - nx * wa, ay - ny * wa);
    g.closePath(); g.fill();
    g.beginPath(); g.arc(ax, ay, wa, 0, 7); g.fill();
    g.beginPath(); g.arc(bx, by, wb, 0, 7); g.fill();
  }
  function circle(g, x, y, r) { g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }
  function ellipse(g, x, y, rx, ry, rot) { g.beginPath(); g.ellipse(x, y, rx, ry, rot || 0, 0, 7); g.fill(); }

  // ---- 부위 ----------------------------------------------------
  function drawLeg(g, hip, kne, ank, front) {
    g.fillStyle = front ? C.skin : C.skinDark;
    capsule(g, hip.x, hip.y, kne.x, kne.y, 30, 22);   // 허벅지
    capsule(g, kne.x, kne.y, ank.x, ank.y, 21, 15);   // 종아리
    if (front) {                                       // 근육 음영
      g.fillStyle = C.skinDark;
      capsule(g, hip.x + 10, hip.y + 6, kne.x + 6, kne.y, 8, 6);
    }
  }

  function drawFoot(g, ank, dir) {
    // 닭발톱 부츠: 발목에서 바깥으로 3발가락 + 뒤꿈치 며느리발톱
    g.fillStyle = C.boot;
    const fx = ank.x + dir * 6, fy = ank.y + 6;
    // 발등
    ellipse(g, fx, fy - 2, 14, 10, 0);
    // 앞 3발가락
    for (let i = -1; i <= 1; i++) {
      const tx = fx + dir * (18 + i * 2) + i * 6, ty = fy + 12 + Math.abs(i) * 2;
      capsule(g, fx + dir * 4, fy, tx, ty, 6, 3);
      g.fillStyle = C.bootDark; circle(g, tx, ty, 3); g.fillStyle = C.boot; // 발톱끝
    }
    // 뒤 며느리발톱
    capsule(g, fx - dir * 4, fy, fx - dir * 14, fy + 8, 5, 2.5);
  }

  function drawFist(g, w) {
    g.fillStyle = C.skin;
    circle(g, w.x, w.y, 17);
    ellipse(g, w.x, w.y + 10, 15, 9, 0);     // 손목 근처
    // 주먹 마디
    g.strokeStyle = C.skinDark; g.lineWidth = 2.5; g.lineCap = "round";
    for (let i = -1; i <= 2; i++) {
      g.beginPath(); g.arc(w.x - 9 + i * 7, w.y - 8, 3.4, 0.15, 3.0); g.stroke();
    }
    g.fillStyle = C.skinLite; ellipse(g, w.x - 5, w.y - 3, 6, 4, -0.4);
  }

  function drawClaw(g, w, dir) {
    g.fillStyle = C.skin;
    circle(g, w.x, w.y + 4, 13);              // 손바닥
    g.fillStyle = C.beak;
    // 발톱 3개 위로 펼침
    const claws = [[-10, -30], [2, -36], [15, -28]];
    for (const [dx, dy] of claws) {
      const bx = w.x + dx * (dir < 0 ? -1 : 1), by = w.y + dy;
      capsule(g, w.x + dx * 0.4, w.y - 6, bx, by, 6, 2.4);
    }
    g.fillStyle = C.skinLite; ellipse(g, w.x - 3, w.y + 2, 6, 4, -0.4);
  }

  function drawTorso(g, p) {
    // 넓은 가슴 → 잘록한 허리
    const L = p.sho.L, R = p.sho.R, hL = p.hip.L, hR = p.hip.R;
    g.fillStyle = C.skin;
    g.beginPath();
    g.moveTo(L.x - 6, L.y);
    g.bezierCurveTo(L.x - 14, L.y + 34, hL.x - 18, hL.y - 34, hL.x - 8, hL.y);
    g.lineTo(hR.x + 8, hR.y);
    g.bezierCurveTo(hR.x + 18, hR.y - 34, R.x + 14, R.y + 34, R.x + 6, R.y);
    g.bezierCurveTo(R.x - 10, R.y - 12, L.x + 10, L.y - 12, L.x - 6, L.y);
    g.closePath(); g.fill();

    // 가슴근 (두 덩이)
    g.fillStyle = C.skinDark;
    g.strokeStyle = C.skinDark; g.lineWidth = 3; g.lineCap = "round";
    const cy = 128;
    for (const s of [-1, 1]) {
      g.beginPath();
      g.moveTo(150 + s * 4, cy + 22);
      g.bezierCurveTo(150 + s * 4, cy + 4, 150 + s * 34, cy - 4, 150 + s * 40, cy + 10);
      g.bezierCurveTo(150 + s * 42, cy + 22, 150 + s * 30, cy + 30, 150 + s * 12, cy + 26);
      g.stroke();
    }
    // 복근 중앙선 + 갈비
    g.beginPath(); g.moveTo(150, cy + 24); g.lineTo(150, 178); g.stroke();
    g.lineWidth = 2;
    for (let i = 0; i < 3; i++) {
      const yy = 150 + i * 12;
      g.beginPath(); g.moveTo(132, yy); g.lineTo(148, yy + 2); g.stroke();
      g.beginPath(); g.moveTo(168, yy); g.lineTo(152, yy + 2); g.stroke();
    }
  }

  function drawArm(g, sho, elb, wri, dir) {
    g.fillStyle = C.skin;
    capsule(g, sho.x, sho.y, elb.x, elb.y, 21, 16);   // 상완
    capsule(g, elb.x, elb.y, wri.x, wri.y, 16, 12);   // 전완
    // 삼각근
    g.fillStyle = C.skinLite; circle(g, sho.x, sho.y - 2, 20);
    g.fillStyle = C.skin;     circle(g, sho.x, sho.y - 2, 17);
    // 이두 하이라이트
    g.fillStyle = C.skinLite;
    const mx = (sho.x + elb.x) / 2, my = (sho.y + elb.y) / 2;
    ellipse(g, mx + dir * 2, my, 7, 12, Math.atan2(elb.y - sho.y, elb.x - sho.x));
  }

  function drawHackle(g, p) {
    // 목 아래 톱니 깃털 러프 (목 칼라 정도로 작게)
    g.fillStyle = C.hackle;
    const y = 99, cx = 150;
    g.beginPath();
    g.moveTo(cx - 40, y);
    const zig = [[-30, 24], [-19, 5], [-10, 22], [0, 4], [10, 22], [19, 5], [30, 24], [40, 0]];
    for (const [dx, dy] of zig) g.lineTo(cx + dx, y + dy);
    g.bezierCurveTo(cx + 30, y + 4, cx - 30, y + 4, cx - 40, y);
    g.closePath(); g.fill();
    g.strokeStyle = C.hackleDk; g.lineWidth = 2; g.lineCap = "round";
    for (const [dx, dy] of zig) { if (dy > 14) { g.beginPath(); g.moveTo(cx + dx, y + 4); g.lineTo(cx + dx, y + dy - 3); g.stroke(); } }
  }

  function drawSkirt(g, p) {
    const cx = 150, y = 178;
    // 벨트 밴드
    g.fillStyle = C.featherLt;
    g.beginPath();
    g.moveTo(cx - 44, y);
    g.bezierCurveTo(cx - 20, y + 14, cx + 20, y + 14, cx + 44, y);
    g.bezierCurveTo(cx + 48, y + 20, cx + 48, y + 30, cx + 44, y + 38);
    g.bezierCurveTo(cx + 20, y + 52, cx - 20, y + 52, cx - 44, y + 38);
    g.bezierCurveTo(cx - 48, y + 30, cx - 48, y + 20, cx - 44, y);
    g.closePath(); g.fill();
    // 톱니 단
    g.fillStyle = C.feather;
    g.beginPath();
    g.moveTo(cx - 46, y + 30);
    const zig = [[-32, 58], [-16, 20], [0, 62], [16, 20], [32, 58], [46, 30]];
    for (const [dx, dy] of zig) g.lineTo(cx + dx, y + dy);
    g.bezierCurveTo(cx + 20, y + 44, cx - 20, y + 44, cx - 46, y + 30);
    g.closePath(); g.fill();
    g.strokeStyle = C.featherDk; g.lineWidth = 2.5;
    g.beginPath();
    g.moveTo(cx - 16, y + 20); g.lineTo(cx - 24, y + 44);
    g.moveTo(cx + 16, y + 20); g.lineTo(cx + 24, y + 44);
    g.moveTo(cx, y + 62); g.lineTo(cx, y + 40);
    g.stroke();
  }

  function drawHead(g, p) {
    const h = p.head, x = h.x, y = h.y, r = h.r;
    // 볏 (크고 도톰한 수탉 볏 — 위로 솟은 5개 로브)
    g.fillStyle = C.comb;
    g.beginPath();
    g.moveTo(x - 30, y - 24);
    const peaks = [[-30, -26], [-25, -48], [-14, -30], [-6, -52], [5, -34],
                   [12, -50], [20, -32], [27, -44], [32, -20]];
    for (const [dx, dy] of peaks) g.lineTo(x + dx, y + dy);
    g.bezierCurveTo(x + 24, y - 16, x - 20, y - 14, x - 30, y - 24);
    g.closePath(); g.fill();
    // 볏 밑동 음영
    g.fillStyle = C.combDark;
    g.beginPath();
    g.moveTo(x - 28, y - 22);
    g.bezierCurveTo(x - 10, y - 12, x + 14, y - 12, x + 30, y - 20);
    g.lineTo(x + 28, y - 26);
    g.bezierCurveTo(x + 10, y - 18, x - 12, y - 18, x - 26, y - 26);
    g.closePath(); g.fill();

    // 머리 본체
    g.fillStyle = C.cream;
    g.beginPath();
    g.ellipse(x, y, r, r * 0.98, 0, 0, 7); g.fill();
    // 볼(부리쪽 볼록)
    ellipse(g, x - r * 0.55, y + 6, 16, 18, 0);
    // 얼굴 음영(오른쪽)
    g.fillStyle = C.creamDark;
    g.beginPath(); g.ellipse(x + r * 0.42, y + 2, r * 0.5, r * 0.8, 0, -0.6, 2.4); g.fill();

    // 부리 (성나게 살짝 벌림, 왼쪽 향함)
    g.fillStyle = C.beak;
    g.beginPath();
    g.moveTo(x - r * 0.5, y - 2);
    g.bezierCurveTo(x - r - 20, y - 6, x - r - 22, y + 8, x - r * 0.55, y + 8);
    g.closePath(); g.fill();
    g.fillStyle = C.beakDark;         // 아랫부리
    g.beginPath();
    g.moveTo(x - r * 0.55, y + 8);
    g.bezierCurveTo(x - r - 14, y + 10, x - r - 8, y + 22, x - r * 0.5, y + 18);
    g.closePath(); g.fill();
    g.fillStyle = C.eye; circle(g, x - r * 0.72, y - 1, 2.4);   // 콧구멍

    // 와틀(볏턱)
    g.fillStyle = C.comb;
    g.beginPath();
    g.moveTo(x - r * 0.5, y + 16);
    g.bezierCurveTo(x - r * 0.62, y + 34, x - r * 0.3, y + 40, x - r * 0.2, y + 24);
    g.closePath(); g.fill();

    // 성난 눈썹
    g.strokeStyle = C.outline; g.lineWidth = 6; g.lineCap = "round";
    g.beginPath(); g.moveTo(x - 20, y - 12); g.lineTo(x + 2, y - 4); g.stroke();
    g.beginPath(); g.moveTo(x + 10, y - 6); g.lineTo(x + 30, y - 14); g.stroke();
    // 눈 흰자
    g.fillStyle = C.white;
    ellipse(g, x - 6, y + 2, 9, 7, -0.2);
    ellipse(g, x + 20, y + 0, 8, 7, 0.2);
    // 눈동자(안쪽 노려봄)
    g.fillStyle = C.eye;
    circle(g, x - 2, y + 3, 4.2);
    circle(g, x + 16, y + 1, 4.2);
    g.fillStyle = C.white;
    circle(g, x - 1, y + 1.6, 1.4);
    circle(g, x + 17, y - 0.4, 1.4);
  }

  // ---- 컬러 캐릭터 1장 (투명 배경) -----------------------------
  function drawColor(g, p) {
    // 뒤(원경) 다리 = 오른쪽(R), 앞 다리 = 왼쪽(L) 로 겹침감
    drawLeg(g, p.hip.R, p.kne.R, p.ank.R, false);
    drawFoot(g, p.ank.R, +1);
    drawLeg(g, p.hip.L, p.kne.L, p.ank.L, true);
    drawFoot(g, p.ank.L, -1);

    drawSkirt(g, p);
    drawTorso(g, p);

    // 뒷팔(R, 원경) → 몸 → 앞팔(L)
    drawArm(g, p.sho.R, p.elb.R, p.wri.R, +1);
    drawClaw(g, p.wri.R, +1);
    drawArm(g, p.sho.L, p.elb.L, p.wri.L, -1);
    drawFist(g, p.wri.L);

    drawHackle(g, p);
    drawHead(g, p);
  }

  // ---- 외곽선 합성 렌더 ----------------------------------------
  function off(w, h) { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; }

  function render(pose, scale) {
    const p = pose || BASE;
    const W = Math.ceil(CHAR_W * scale), H = Math.ceil(CHAR_H * scale);
    // 컬러 레이어
    const col = off(W, H), cg = col.getContext("2d");
    cg.save(); cg.scale(scale, scale); drawColor(cg, p); cg.restore();
    // 다크 실루엣
    const dk = off(W, H), dg = dk.getContext("2d");
    dg.drawImage(col, 0, 0);
    dg.globalCompositeOperation = "source-in";
    dg.fillStyle = C.outline; dg.fillRect(0, 0, W, H);
    // 합성: 외곽선 스탬프 링 + 컬러
    const out = off(W, H), og = out.getContext("2d");
    const T = Math.max(2, scale * 3.2);
    for (let a = 0; a < 20; a++) {
      const ang = a / 20 * Math.PI * 2;
      og.drawImage(dk, Math.cos(ang) * T, Math.sin(ang) * T);
    }
    og.drawImage(col, 0, 0);
    return out;
  }

  window.Dakgalbi = { render, BASE, CHAR_W, CHAR_H, palette: C };
})();
