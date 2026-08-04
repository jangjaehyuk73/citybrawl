#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
춘천닭갈비 — 픽셀 스프라이트 시트 생성기 (시제품)
컨셉: 불의 붉은 수탉 파이터. 옆면(격투 게임 시점).

네이티브 저해상도(셀 72x72)로 그려 게임이 nearest-neighbor로 확대해 쓴다.
출력:
  dakgalbi_sheet.png      네이티브 1x 시트 (게임용)
  dakgalbi_preview.png    6x 확대 미리보기 (눈으로 확인용)
  dakgalbi.json           프레임 메타데이터
"""
import json, os
from PIL import Image, ImageDraw

CELL = 72
GROUND = 66          # 발이 닿는 y
SCALE = 6            # 미리보기 배율
OUT = os.path.dirname(os.path.abspath(__file__))

# ---- 팔레트 --------------------------------------------------------------
P = {
    "feather":  (216, 82, 58),    # 몸 깃털 (밝은 붉은)
    "feather2": (168, 51, 34),    # 깃털 그늘
    "feather3": (94, 26, 17),     # 깊은 그늘
    "cream":    (240, 228, 210),  # 얼굴/목
    "cream2":   (214, 194, 168),  # 얼굴 그늘
    "comb":     (226, 59, 43),     # 볏 (빨강)
    "comb2":    (176, 38, 30),
    "beak":     (242, 193, 78),    # 부리/다리 (노랑)
    "beak2":    (200, 150, 46),
    "eye":      (36, 24, 18),
    "white":    (255, 255, 255),
    "outline":  (40, 14, 8),       # 실루엣 외곽선
    "fl1":      (255, 210, 74),    # 불꽃 밝음
    "fl2":      (255, 138, 52),
    "fl3":      (229, 68, 42),
    "flash":    (255, 255, 255),
}

# ---- 저수준 도구 ---------------------------------------------------------
def new_cell():
    return Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))

def px(d, x, y, c):
    d.point((int(x), int(y)), fill=c)

def rect(d, x0, y0, x1, y1, c):
    d.rectangle([int(x0), int(y0), int(x1), int(y1)], fill=c)

def ell(d, x0, y0, x1, y1, c):
    d.ellipse([int(x0), int(y0), int(x1), int(y1)], fill=c)

def line(d, x0, y0, x1, y1, c, w=1):
    d.line([int(x0), int(y0), int(x1), int(y1)], fill=c, width=w)

def poly(d, pts, c):
    d.polygon([(int(a), int(b)) for a, b in pts], fill=c)

def add_outline(img, color):
    """비어있지 않은 실루엣 바깥에 1px 외곽선을 두른다."""
    px_ = img.load()
    w, h = img.size
    solid = [[px_[x, y][3] > 40 for y in range(h)] for x in range(w)]
    out = img.copy()
    o = out.load()
    for x in range(w):
        for y in range(h):
            if solid[x][y]:
                continue
            near = False
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                nx, ny = x+dx, y+dy
                if 0 <= nx < w and 0 <= ny < h and solid[nx][ny]:
                    near = True
                    break
            if near:
                o[x, y] = color + (255,)
    return out

# ---- 부위 그리기 ---------------------------------------------------------
def draw_leg(d, hipx, hipy, footx, footy, bend, flip_toes=False, c=None):
    """노란 다리 하나 — 허벅지→무릎→발, 3발가락."""
    c = c or P["beak"]
    kneex = (hipx + footx) / 2 + bend
    kneey = (hipy + footy) / 2
    line(d, hipx, hipy, kneex, kneey, c, 3)
    line(d, kneex, kneey, footx, footy, c, 3)
    # 발가락
    dirx = 1 if not flip_toes else -1
    for i in (-1, 0, 1):
        line(d, footx, footy, footx + dirx*4, footy + i*2, c, 1)
    # 뒤꿈치
    line(d, footx, footy, footx - dirx*2, footy, c, 1)

def draw_tail(d, bx, by, flare=0):
    """등 뒤로 솟은 수탉 꼬리 깃털 — 굵고 휘어진 겹깃."""
    # 각 깃: (끝점 dx,dy, 굵기, 색)  — 뒤(왼쪽) 위로 아치를 그리며 겹친다
    plumes = [
        (-19, -6,  4, P["feather3"]),
        (-21, -15, 5, P["feather2"]),
        (-16, -22, 5, P["feather"]),
        (-9,  -24, 4, P["comb"]),
    ]
    for tx, ty, wdt, col in plumes:
        tx -= flare
        ty -= flare // 2
        # 밑동→중간→끝 을 지나는 휜 깃대
        mx, my = bx + tx*0.55 - 3, by + ty*0.35
        line(d, bx, by, mx, my, col, wdt)
        line(d, mx, my, bx + tx, by + ty, col, max(2, wdt-1))
        # 깃 끝 뭉치
        ell(d, bx+tx-2, by+ty-2, bx+tx+3, by+ty+3, col)

def draw_body(d, cx, cy):
    ell(d, cx-15, cy-11, cx+13, cy+13, P["feather"])
    # 배 하이라이트
    ell(d, cx-4, cy-2, cx+12, cy+12, P["feather2"])
    ell(d, cx-2, cy+1, cx+11, cy+12, P["cream2"])
    # 등쪽 그늘
    ell(d, cx-15, cy-10, cx-2, cy+6, P["feather2"])

def draw_wing(d, sx, sy, ext, spread=0):
    """앞날개(팔) — ext: 앞으로 뻗는 정도(0~1). 펀치 때 주먹처럼 뻗는다."""
    tipx = sx + 6 + int(ext*22)
    tipy = sy - int(ext*3) + 2
    # 날개 몸체
    poly(d, [(sx-4, sy-6), (tipx, tipy-4), (tipx+2, tipy+3),
             (sx-2, sy+7)], P["feather2"])
    # 깃털 결
    line(d, sx-2, sy-2, tipx, tipy-1, P["feather3"], 1)
    if ext > 0.5:
        # 뻗은 끝 = 주먹 뭉치
        ell(d, tipx-3, tipy-4, tipx+5, tipy+4, P["feather"])
        px(d, tipx+1, tipy, P["fl1"])
    else:
        # 접힌 날개 끝 깃털
        for i in range(3):
            line(d, sx+2+i*2, sy+3, sx-2+i*2, sy+9, P["feather3"], 1)

def draw_head(d, hx, hy, look=0):
    # 목
    poly(d, [(hx-9, hy+9), (hx-4, hy+13), (hx-2, hy+4)], P["cream"])
    # 머리
    ell(d, hx-9, hy-9, hx+9, hy+9, P["cream"])
    ell(d, hx-8, hy-2, hx+6, hy+8, P["cream2"])
    # 볏 (빨강 톱니)
    for i, ox in enumerate((-6, -1, 4)):
        poly(d, [(hx+ox-3, hy-8), (hx+ox, hy-15+ (0 if i!=1 else -1)),
                 (hx+ox+3, hy-8)], P["comb"])
    px(d, hx-1, hy-12, P["comb2"])
    # 부리
    bx = hx + 8 + look
    poly(d, [(bx, hy-2), (bx+9, hy), (bx, hy+3)], P["beak"])
    line(d, bx, hy, bx+8, hy+1, P["beak2"], 1)
    # 볼우물(턱볏)
    ell(d, bx-3, hy+3, bx+2, hy+8, P["comb"])
    # 눈
    ell(d, hx+1, hy-4, hx+6, hy+2, P["eye"])
    px(d, hx+4, hy-3, P["white"])

def draw_flame(d, fx, fy, t):
    """불판 화염 — special 앞쪽 이펙트."""
    layers = [(P["fl3"], 11), (P["fl2"], 8), (P["fl1"], 5)]
    for col, r in layers:
        wob = ((t % 3) - 1)
        poly(d, [(fx-2, fy+r), (fx-r+wob, fy), (fx-2, fy-r+2),
                 (fx+2, fy-r-2), (fx+r, fy), (fx+2, fy+r)], col)

# ---- 한 프레임 = 포즈 ----------------------------------------------------
def draw_pose(pose):
    img = new_cell()
    d = ImageDraw.Draw(img)

    crouch = pose.get("crouch", 0)
    lean   = pose.get("lean", 0)          # 상체 앞뒤 기울기(px)
    bx, by = 30, 40 + crouch              # 몸 중심
    hx, hy = 39 + lean, 20 + crouch       # 머리 중심

    # KO — 뒤로 벌러덩 누운 자세 (머리 왼쪽 바닥, 다리 공중)
    if pose.get("ko"):
        gy = 58
        draw_tail(d, 42, gy-2, flare=8)               # 꼬리는 오른쪽 바닥으로
        ell(d, 22, gy-9, 45, gy+3, P["feather"])      # 가로로 누운 몸통
        ell(d, 30, gy-5, 45, gy+3, P["feather2"])
        ell(d, 28, gy-1, 42, gy+3, P["cream2"])       # 드러난 배
        draw_leg(d, 35, gy-6, 41, gy-17, 3)           # 공중에 든 다리
        draw_leg(d, 30, gy-6, 25, gy-15, -3)
        draw_head(d, 16, gy-2, look=-2)
        out = add_outline(img, P["outline"])
        od = ImageDraw.Draw(out)
        # 뇌진탕 X 눈
        line(od, 17, 53, 21, 57, P["outline"]); line(od, 21, 53, 17, 57, P["outline"])
        # 어질어질 별
        for sx, sy in ((12, 40), (20, 34), (28, 38)):
            line(od, sx-1, sy, sx+1, sy, P["fl1"]); line(od, sx, sy-1, sx, sy+1, P["fl1"])
        return out

    # 다리
    bl = pose.get("backleg",  (26, 51, 22, GROUND, 2))
    fl = pose.get("frontleg", (34, 51, 40, GROUND, -1))
    draw_leg(d, bl[0], bl[1]+crouch, bl[2], bl[3], bl[4], c=P["beak2"])  # 뒷다리 살짝 어둡게
    # 발차기?
    kick = pose.get("kick", 0)
    if kick > 0:
        kx = 40 + int(kick*22)
        ky = 44 - int(kick*6)
        draw_leg(d, 34, 48+crouch, kx, ky, -2)
        # 발끝 불꽃
        px(d, kx+2, ky, P["fl2"]); px(d, kx+3, ky-1, P["fl1"])
    else:
        draw_leg(d, fl[0], fl[1]+crouch, fl[2], fl[3], fl[4])

    # 꼬리 → 몸 → 뒷날개 힌트 → 머리 → 앞날개
    draw_tail(d, bx-10, by-6, flare=pose.get("tailflare", 0))
    draw_body(d, bx, by)
    draw_head(d, hx, hy, look=pose.get("look", 0))
    draw_wing(d, bx+9, by-2, pose.get("wing", 0.0))

    if pose.get("flame"):
        draw_flame(d, 58, 40, pose.get("t", 0))

    out = add_outline(img, P["outline"])

    if pose.get("hit"):
        # 피격 = 뒤로 젖힌 포즈(위 lean) + 앞쪽 충격 스파크. 흰 번쩍임은 런타임에서.
        od = ImageDraw.Draw(out)
        cx, cy = 52, 26
        for a in range(6):
            import math
            ang = a * math.pi / 3 + 0.3
            r1, r2 = 3, 8
            line(od, cx+math.cos(ang)*r1, cy+math.sin(ang)*r1,
                 cx+math.cos(ang)*r2, cy+math.sin(ang)*r2, P["fl1"])
        px(od, cx, cy, P["fl2"])
    return out

# ---- 액션(행) 정의 -------------------------------------------------------
def build_actions():
    A = {}

    # idle — 숨쉬기 4프레임
    A["idle"] = [dict(crouch=c) for c in (0, 1, 1, 0)]

    # walk — 다리 교차 4프레임
    A["walk"] = [
        dict(crouch=1, backleg=(24,51,20,GROUND,2),  frontleg=(36,51,42,GROUND-2,-2)),
        dict(crouch=0, backleg=(26,51,24,GROUND-3,1), frontleg=(34,51,40,GROUND,-1)),
        dict(crouch=1, backleg=(28,51,26,GROUND,-1), frontleg=(32,51,44,GROUND-2,-2)),
        dict(crouch=0, backleg=(26,51,22,GROUND,2),  frontleg=(34,51,38,GROUND-3,-1)),
    ]

    # punch — 날개 잽 3프레임 (준비→뻗음→회수)
    A["punch"] = [
        dict(wing=0.15, lean=1),
        dict(wing=1.0, lean=2, look=1),
        dict(wing=0.4, lean=1),
    ]

    # kick — 불발차기 3프레임
    A["kick"] = [
        dict(kick=0.2, lean=-1, crouch=1),
        dict(kick=1.0, lean=-2),
        dict(kick=0.4, lean=-1, crouch=1),
    ]

    # special — 불판 화염 3프레임
    A["special"] = [
        dict(crouch=1, lean=-1, tailflare=4),
        dict(flame=True, t=0, look=1, wing=0.3, lean=1),
        dict(flame=True, t=1, look=1, wing=0.5, lean=2),
    ]

    # hit — 피격 2프레임
    A["hit"] = [
        dict(hit=True, lean=-3, crouch=1, look=-2),
        dict(hit=True, lean=-2, crouch=0, look=-1),
    ]

    # ko — 넉다운 1프레임
    A["ko"] = [dict(ko=True)]

    return A

# ---- 시트 조립 -----------------------------------------------------------
def main():
    actions = build_actions()
    order = ["idle", "walk", "punch", "kick", "special", "hit", "ko"]
    cols = max(len(actions[a]) for a in order)
    rows = len(order)

    sheet = Image.new("RGBA", (cols*CELL, rows*CELL), (0, 0, 0, 0))
    meta = {"cell": CELL, "ground": GROUND, "actions": {}}

    for r, name in enumerate(order):
        frames = actions[name]
        meta["actions"][name] = {"row": r, "frames": len(frames)}
        for c, pose in enumerate(frames):
            cell = draw_pose(pose)
            sheet.paste(cell, (c*CELL, r*CELL), cell)

    sheet.save(os.path.join(OUT, "dakgalbi_sheet.png"))

    # 확대 미리보기 (배경 격자 포함)
    preview = Image.new("RGBA", sheet.size, (28, 24, 30, 255))
    # 체크무늬로 투명영역 구분
    for y in range(0, sheet.height, 8):
        for x in range(0, sheet.width, 8):
            if (x//8 + y//8) % 2 == 0:
                for yy in range(y, min(y+8, sheet.height)):
                    for xx in range(x, min(x+8, sheet.width)):
                        preview.putpixel((xx, yy), (38, 33, 40, 255))
    preview.alpha_composite(sheet)
    preview = preview.resize((sheet.width*SCALE, sheet.height*SCALE), Image.NEAREST)
    preview.save(os.path.join(OUT, "dakgalbi_preview.png"))

    with open(os.path.join(OUT, "dakgalbi.json"), "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print("sheet:", sheet.size, "| cols x rows:", cols, "x", rows)
    print("actions:", {k: v["frames"] for k, v in meta["actions"].items()})

if __name__ == "__main__":
    main()
