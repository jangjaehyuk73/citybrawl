#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
~/Downloads/soboro_<pose>.png (Gemini 다운로드) → poses/<pose>_raw.png → 배경제거 → 게임반영

사용법:
  1) Gemini(소보로 대화 이어서)에서 포즈를 뽑아 soboro_<pose>.png 로 다운로드
     (pose ∈ idle,walk,punch,kick,jump,special,guard,crouch,hit,ko)
  2) python3 ingest.py            # 있는 것만 골라 들여오고 파이프라인 실행
     python3 ingest.py punch kick # 특정 포즈만

- idle_raw.png 와 바이트가 같으면 '중복(생성 실패)'로 보고 건너뜀 → 과거 walk/punch 사고 방지
- 들여온 뒤 process_all.py 자동 실행(배경제거 + manifest.json/.js 갱신)
"""
import os, sys, glob, shutil, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
POSES = os.path.join(HERE, "poses")
DL = os.path.expanduser("~/Downloads")
VALID = ["idle","walk","punch","kick","jump","special","guard","crouch","hit","ko"]

def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()

def main():
    want = [a for a in sys.argv[1:] if a in VALID]
    todo = want or VALID
    idle_raw = os.path.join(POSES, "idle_raw.png")
    idle_hash = md5(idle_raw) if os.path.exists(idle_raw) else None

    brought = []
    for pose in todo:
        src = os.path.join(DL, f"soboro_{pose}.png")
        if not os.path.exists(src):
            continue
        # idle 과 동일 = 생성이 안 나온 것(과거 사고). idle 자신은 예외.
        if idle_hash and pose != "idle" and md5(src) == idle_hash:
            print(f"  ⚠ {pose}: idle 과 동일한 파일 → 생성 실패로 보고 건너뜀")
            continue
        dst = os.path.join(POSES, f"{pose}_raw.png")
        shutil.copyfile(src, dst)
        brought.append(pose)
        print(f"  ✓ {pose:8s} ← {src}")

    if not brought:
        print("들여온 포즈 없음. ~/Downloads/soboro_<pose>.png 를 확인하세요.")
        print("남은 포즈:", [p for p in VALID
                          if not os.path.exists(os.path.join(POSES, f"{p}_raw.png"))])
        return

    print(f"\n{len(brought)}개 들여옴 → process_all.py 실행")
    subprocess.run([sys.executable, os.path.join(HERE, "process_all.py")], check=True)
    have = sorted(os.path.basename(f).replace("_raw.png","")
                  for f in glob.glob(os.path.join(POSES, "*_raw.png")))
    missing = [p for p in VALID if p not in have]
    print("\n보유 포즈:", have)
    if missing:
        print("남은 포즈:", missing)
    else:
        print("★ 전체 포즈 완성!")

if __name__ == "__main__":
    main()
