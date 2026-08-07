#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dakgalbi/daege/soboro 의 manifest.json 을 합쳐 characters/roster.js 생성.
게임(game.html)이 <script src="roster.js"> 로 읽어 window.ROSTER 사용 (file:// CORS 회피).
각 캐릭터: 파일경로에 dir 접두, 라벨/필살기타입/홈스테이지/점프력 메타 추가.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

META = {
    "dakgalbi": {"label": "춘천닭갈비", "dir": "dakgalbi/", "proj": "fire",
                 "stage": "dakgalbi/stage/chuncheon_muted.png", "jumpV": 19, "koFlip": False},
    "daege":    {"label": "속초 대게",   "dir": "daege/",    "proj": "water",
                 "stage": "daege/stage/yeongdeok_muted.png",  "jumpV": 21, "koFlip": True},
    "soboro":   {"label": "대전소보로",  "dir": "soboro/",   "proj": "crumb",
                 "stage": "soboro/stage/daejeon_muted.png",   "jumpV": 17, "koFlip": True},
}

roster = {}
for key, meta in META.items():
    man = json.load(open(os.path.join(HERE, key, "manifest.json")))
    sprites = {}
    for pose, s in man["sprites"].items():
        sprites[pose] = {
            "file": meta["dir"] + s["file"],   # ex) soboro/sprites/idle.png
            "frame": s["frame"],
            "content": s["content"],
        }
    roster[key] = {
        "label": meta["label"], "proj": meta["proj"], "stage": meta["stage"],
        "jumpV": meta["jumpV"], "koFlip": meta["koFlip"], "sprites": sprites,
    }

out = os.path.join(HERE, "roster.js")
with open(out, "w") as fp:
    fp.write("window.ROSTER = " + json.dumps(roster, ensure_ascii=False, indent=1) + ";\n")
print("roster.js written:", list(roster.keys()))
