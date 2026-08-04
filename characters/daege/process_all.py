#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
poses/*_raw.png (Gemini 원본, 회색 배경) → sprites/*.png (투명, 게임용)
- 테두리 flood-fill 로 회색 배경 + 바닥그림자 + 반짝이 워터마크 제거
- 캐릭터 내부는 연결성으로 보호
- 원본 768x1024 프레임을 그대로 유지(크롭 안 함) → 모든 포즈가 같은 좌표계라
  게임에서 균일 배율·동일 기준점으로 배치하면 크기·발위치가 일관됨
- manifest.json: 각 스프라이트의 프레임크기 + 캐릭터 content bbox 기록
"""
from collections import deque
from PIL import Image, ImageFilter
import os, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "poses")
OUT  = os.path.join(HERE, "sprites")
os.makedirs(OUT, exist_ok=True)

def is_bg(p, hi=255):
    r, g, b, a = p
    sat = max(r, g, b) - min(r, g, b)
    lum = 0.299*r + 0.587*g + 0.114*b
    # 테두리 flood(hi=255)엔 순백 워터반짝이 포함, 내부 갇힌영역 판정(hi=252)엔 흰 이빨·하이라이트 보호
    return sat <= 28 and 100 <= lum <= hi

def remove_bg(im):
    W, H = im.size
    px = im.load()
    seen = bytearray(W*H)
    q = deque()
    def seed(x, y):
        i = y*W + x
        if not seen[i] and is_bg(px[x, y]):
            seen[i] = 1; q.append((x, y))
    for x in range(W): seed(x, 0); seed(x, H-1)
    for y in range(H): seed(0, y); seed(W-1, y)
    while q:
        x, y = q.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < W and 0 <= ny < H:
                i = ny*W+nx
                if not seen[i] and is_bg(px[nx, ny]):
                    seen[i] = 1; q.append((nx, ny))
    for y in range(H):
        b = y*W
        for x in range(W):
            if seen[b+x]:
                r, g, bl, _ = px[x, y]; px[x, y] = (r, g, bl, 0)

    # 2차: 테두리에 안 닿는 '갇힌 배경 주머니' 제거
    # (예: 주먹 뻗을 때 팔-몸통 사이 회색 공간) — 큰 덩어리만, 작은 하이라이트는 보호
    seen2 = bytearray(W*H)
    for y in range(H):
        for x in range(W):
            i = y*W + x
            if seen2[i]:
                continue
            p = px[x, y]
            if p[3] == 0 or not is_bg(p, hi=252):   # 내부는 순백 제외(이빨·하이라이트 보호)
                seen2[i] = 1; continue
            comp = []; q2 = deque([(x, y)]); seen2[i] = 1
            while q2:
                cx, cy = q2.popleft(); comp.append((cx, cy))
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = cx+dx, cy+dy
                    if 0 <= nx < W and 0 <= ny < H:
                        j = ny*W+nx
                        if not seen2[j]:
                            q3 = px[nx, ny]
                            if q3[3] != 0 and is_bg(q3, hi=252):
                                seen2[j] = 1; q2.append((nx, ny))
                            else:
                                seen2[j] = 1
            if len(comp) > 150:          # 갇힌 배경 주머니 → 제거
                for cx, cy in comp:
                    r, g, bl, _ = px[cx, cy]; px[cx, cy] = (r, g, bl, 0)

    # 3차: 바닥 '회색 그림자' 제거 — 이미 투명한 바깥에서 회색으로만 번져 들어감.
    # 캐릭터(주황=고채도)와 검은 외곽선(어두움)은 벽이 되어 못 넘어가고,
    # 껍데기 안쪽 하이라이트/ko 소용돌이 눈(안쪽에 갇힘)은 바깥과 끊겨 보호됨.
    def is_shadow(p):
        r, g, b, a = p
        if a == 0:
            return False
        sat = max(r, g, b) - min(r, g, b)
        lum = 0.299*r + 0.587*g + 0.114*b
        return sat <= 40 and 78 <= lum <= 205     # 흐릿한 회색 그림자(흰 이빨 lum>205·검은 외곽선 lum<78 제외)
    seen3 = bytearray(W*H)
    q3 = deque()
    for y in range(H):
        b = y*W
        for x in range(W):
            if px[x, y][3] == 0:
                seen3[b+x] = 1; q3.append((x, y))
    while q3:
        x, y = q3.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < W and 0 <= ny < H:
                i = ny*W+nx
                if not seen3[i] and is_shadow(px[nx, ny]):
                    r, g, bl, _ = px[nx, ny]; px[nx, ny] = (r, g, bl, 0)
                    seen3[i] = 1; q3.append((nx, ny))

    # 알파 정리: 침식 → 소프트 블러 → 미세 잔여(≈투명) 컷
    a = im.getchannel("A").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
    a = a.point(lambda v: 0 if v < 14 else v)
    im.putalpha(a)
    return im

manifest = {"cell": None, "sprites": {}}
for f in sorted(glob.glob(os.path.join(SRC, "*_raw.png"))):
    name = os.path.basename(f).replace("_raw.png", "")
    im = Image.open(f).convert("RGBA")
    # 일부 다운로드에 가장자리 1~2px 검정/이질 선이 있어 테두리 4px 잘라냄
    w0, h0 = im.size
    im = im.crop((4, 4, w0 - 4, h0 - 4))
    W, H = im.size
    im = remove_bg(im)
    bbox = im.getbbox()            # 캐릭터가 프레임 안 어디 있는지
    im.save(os.path.join(OUT, name + ".png"))
    manifest["cell"] = [W, H]
    manifest["sprites"][name] = {
        "file": f"sprites/{name}.png",
        "frame": [W, H],
        "content": list(bbox) if bbox else None,   # [x0,y0,x1,y1]
    }
    print(f"{name:8s} frame={W}x{H} content={bbox}")

json.dump(manifest, open(os.path.join(HERE, "manifest.json"), "w"),
          ensure_ascii=False, indent=2)
print("\nmanifest.json written")

# manifest.js: file:// 게임이 fetch 없이 읽도록 (window.MANIFEST). process_all 돌 때마다 갱신
with open(os.path.join(HERE, "manifest.js"), "w") as fp:
    fp.write("window.MANIFEST = " +
             json.dumps(manifest, ensure_ascii=False, indent=2) + ";\n")
print("manifest.js written")
