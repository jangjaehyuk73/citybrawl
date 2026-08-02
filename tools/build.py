#!/usr/bin/env python3
"""src/body.html 을 배포용 index.html 로 감싼다.

왜 나눠 두는가
  - src/body.html : 실제로 손대는 소스. <title>·<style>·마크업·<script>만 들어 있다.
  - index.html    : PWA로 동작하려면 <!doctype>·<head>·매니페스트 링크가 필요하다.
  아티팩트로 미리 볼 때는 src/body.html 을 그대로 쓰고, 기기에 설치할 때는
  index.html 을 쓴다. 소스가 하나라 두 결과물이 어긋나지 않는다.

  python3 tools/build.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src", "game.html")
OUT = os.path.join(ROOT, "index.html")

DESC = "한국 지방도시의 상징물들이 벌이는 2D 대전 격투 게임"

HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">

<meta name="color-scheme" content="dark">


<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:locale" content="ko_KR">
</head>
<body>
"""

FOOT = """
</body>
</html>
"""


def main():
    if not os.path.exists(SRC):
        print("소스를 찾을 수 없습니다:", SRC, file=sys.stderr)
        return 1

    with open(SRC, encoding="utf-8") as f:
        body = f.read()

    m = re.search(r"<title>(.*?)</title>\s*", body, re.S)
    if not m:
        print("src/body.html 에 <title>이 없습니다.", file=sys.stderr)
        return 1
    title = m.group(1).strip()
    body = body[:m.start()] + body[m.end():]      # 본문에서 title 제거

    html = HEAD.format(title=title, desc=DESC) + body.strip() + FOOT

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)

    print("빌드 완료")
    print("  제목    %s" % title)
    print("  출력    %s  (%.1f KB)" % (os.path.relpath(OUT, ROOT), len(html) / 1024))
    print()
    print("로컬 확인 (서비스 워커는 localhost 또는 https 에서만 동작합니다):")
    print("  python3 -m http.server 8000 --directory %s" % ROOT)
    print("  → http://localhost:8000")
    return 0


if __name__ == "__main__":
    sys.exit(main())
