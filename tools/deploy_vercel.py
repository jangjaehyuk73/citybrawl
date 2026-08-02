#!/usr/bin/env python3
"""Vercel REST API로 정적 사이트를 배포한다.

Vercel CLI는 Node.js가 필요하고 로그인이 대화형이라 이 환경에서 쓸 수 없습니다.
대신 REST API에 파일을 인라인으로 실어 보냅니다. 표준 라이브러리만 씁니다.

준비
  https://vercel.com/account/tokens 에서 토큰을 만들고
  ~/projects/citybrawl/.env 에 아래 한 줄을 넣습니다.
      VERCEL_TOKEN=발급받은토큰

사용
  python3 tools/deploy_vercel.py                 # 미리보기 배포
  python3 tools/deploy_vercel.py --prod          # 운영 배포
  python3 tools/deploy_vercel.py --name mygame   # 프로젝트 이름 지정
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.vercel.com"

# 배포에 포함할 파일 — 소스와 도구는 올리지 않는다
INCLUDE = ["index.html"]
INCLUDE_DIRS = []          # 필요하면 "assets" 같은 폴더를 넣는다
SKIP = {".DS_Store"}


def load_env():
    path = os.path.join(ROOT, ".env")
    env = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def token():
    t = os.environ.get("VERCEL_TOKEN") or load_env().get("VERCEL_TOKEN", "")
    if not t:
        sys.exit(
            "VERCEL_TOKEN 이 없습니다.\n"
            "  1) https://vercel.com/account/tokens 에서 토큰 생성\n"
            "  2) %s 에 아래 한 줄 추가\n"
            "     VERCEL_TOKEN=발급받은토큰" % os.path.join(ROOT, ".env"))
    return t


def call(path, tok, data=None, method="GET", timeout=120):
    req = urllib.request.Request(
        API + path,
        data=json.dumps(data).encode("utf-8") if data is not None else None,
        headers={"Authorization": "Bearer " + tok,
                 "Content-Type": "application/json"},
        method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            err = json.loads(raw).get("error", {})
            msg = err.get("message") or raw
        except Exception:
            msg = raw
        raise RuntimeError("Vercel 오류 %s: %s" % (e.code, msg[:500]))
    except urllib.error.URLError as e:
        raise RuntimeError("네트워크 오류: %s" % e.reason)


def gather():
    """올릴 파일을 모은다. 각 파일은 base64 로 인라인 전송."""
    files, total = [], 0
    def add(rel):
        nonlocal total
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p) or os.path.basename(p) in SKIP:
            return
        with open(p, "rb") as f:
            raw = f.read()
        total += len(raw)
        files.append({"file": rel.replace(os.sep, "/"),
                      "data": base64.b64encode(raw).decode("ascii"),
                      "encoding": "base64"})
    for rel in INCLUDE:
        add(rel)
    for d in INCLUDE_DIRS:
        base = os.path.join(ROOT, d)
        for cur, _, names in os.walk(base):
            for n in names:
                add(os.path.relpath(os.path.join(cur, n), ROOT))
    return files, total


def main():
    p = argparse.ArgumentParser(description="Vercel 배포")
    p.add_argument("--name", default="citybrawl", help="Vercel 프로젝트 이름")
    p.add_argument("--prod", action="store_true", help="운영 배포")
    p.add_argument("--dry", action="store_true", help="보낼 내용만 확인")
    a = p.parse_args()

    files, total = gather()
    if not files:
        sys.exit("올릴 파일이 없습니다. 먼저 python3 tools/build.py 를 실행하세요.")

    print("배포 준비")
    for f in files:
        print("  %-24s %6.1f KB" % (f["file"], len(f["data"]) * 3 / 4 / 1024))
    print("  합계 %.1f KB · 대상 %s" % (total / 1024, "운영" if a.prod else "미리보기"))

    if a.dry:
        print("\n--dry 이므로 실제 배포는 하지 않았습니다.")
        return 0

    tok = token()
    body = {
        "name": a.name,
        "files": files,
        "projectSettings": {"framework": None},   # 순수 정적 — 빌드 단계 없음
    }
    if a.prod:
        body["target"] = "production"

    try:
        print("\n업로드 중...", end="", flush=True)
        res = call("/v13/deployments?skipAutoDetectionConfirmation=1", tok, body, "POST")
        print(" 접수됨")

        dep_id = res.get("id")
        url = res.get("url")
        print("  배포 ID %s" % dep_id)

        # 빌드 완료까지 기다린다
        state = res.get("readyState") or res.get("status")
        waited = 0
        while state not in ("READY", "ERROR", "CANCELED") and waited < 300:
            time.sleep(4)
            waited += 4
            st = call("/v13/deployments/%s" % dep_id, tok)
            state = st.get("readyState") or st.get("status")
            url = st.get("url") or url
            print("  %s (%d초)" % (state, waited), end="\r", flush=True)

        print(" " * 40, end="\r")
        if state != "READY":
            raise RuntimeError("배포 상태가 %s 입니다." % state)

        print("\n배포 완료")
        print("  https://%s" % url)

        # 운영 배포면 프로젝트 고정 주소도 알려 준다
        try:
            proj = call("/v9/projects/%s" % a.name, tok)
            for al in (proj.get("alias") or [])[:3]:
                dom = al.get("domain") if isinstance(al, dict) else al
                if dom:
                    print("  https://%s" % dom)
        except RuntimeError:
            pass
        return 0

    except RuntimeError as e:
        print("\n[오류] %s" % e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
