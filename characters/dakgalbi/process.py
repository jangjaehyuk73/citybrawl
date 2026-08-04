#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini 생성 이미지 → 게임용 투명 PNG.
테두리 flood-fill 로 균일한 회색 배경 + 바닥그림자 + 반짝이 워터마크 제거.
캐릭터 내부는 '연결성'으로 보호(경계 밖에서 도달 못하면 안 지움).
"""
from collections import deque
from PIL import Image, ImageFilter
import os

SRC = "characters/dakgalbi/Gemini_Generated_Image_cxq2ebcxq2ebcxq2.png"
OUT = "characters/dakgalbi/dakgalbi.png"

im = Image.open(SRC).convert("RGBA")
W, H = im.size
px = im.load()

def is_bg(p):
    r, g, b, a = p
    mx, mn = max(r, g, b), min(r, g, b)
    sat = mx - mn                 # 무채색도
    lum = 0.299*r + 0.587*g + 0.114*b
    return sat <= 26 and 105 <= lum <= 244

# 테두리에서 BFS
visited = bytearray(W*H)
q = deque()
def seed(x, y):
    i = y*W + x
    if not visited[i] and is_bg(px[x, y]):
        visited[i] = 1; q.append((x, y))
for x in range(W):
    seed(x, 0); seed(x, H-1)
for y in range(H):
    seed(0, y); seed(W-1, y)

while q:
    x, y = q.popleft()
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = x+dx, y+dy
        if 0 <= nx < W and 0 <= ny < H:
            i = ny*W + nx
            if not visited[i] and is_bg(px[nx, ny]):
                visited[i] = 1; q.append((nx, ny))

# 알파 적용
for y in range(H):
    base = y*W
    for x in range(W):
        if visited[base+x]:
            r, g, b, _ = px[x, y]
            px[x, y] = (r, g, b, 0)

# 알파 정리: 1px 침식으로 회색 프린지 제거 → 살짝 블러로 매끄럽게
a = im.getchannel("A")
a = a.filter(ImageFilter.MinFilter(3))       # erode
a = a.filter(ImageFilter.GaussianBlur(0.6))  # soften edge
im.putalpha(a)

# 내용물 타이트 크롭
bbox = im.getbbox()
im = im.crop(bbox)
im.save(OUT)
print("cropped size:", im.size, "bbox:", bbox)
