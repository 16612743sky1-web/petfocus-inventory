#!/usr/bin/env python3
"""HTML 파일을 '공유해도 한글 안 깨지는' 표준 문서로 만든다.

문제: 상세페이지·목업 HTML을 파일로 전달하면, <meta charset="utf-8"> 선언이 없을 때
브라우저(특히 iOS Safari)가 한글을 잘못 해석해 깨진 글자(모지바케)로 보인다.
영문·숫자는 멀쩡하고 한글만 깨지면 십중팔구 이 문제다.

해결: charset·viewport 메타를 넣고, 조각(fragment) HTML이면 표준 문서 구조
(doctype/html/head/body)로 감싼다. 파일은 UTF-8(BOM 없음)로 저장한다.

사용:
    python make_shareable_html.py <입력.html> [출력.html]
출력 경로를 안 주면 '<이름>_공유용.html'로 저장하고, 최종 경로를 stdout에 출력한다.
"""
import io
import os
import re
import sys

CHARSET = '<meta charset="utf-8">'
VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1">'


def make_shareable(src_path, dst_path=None):
    with io.open(src_path, encoding="utf-8") as f:
        html = f.read()

    low = html.lower()
    head_open = re.search(r"<head[^>]*>", html, flags=re.I)
    has_html = "<html" in low
    has_body = "<body" in low
    # charset가 문서 앞부분(첫 1KB)에 있어야 브라우저가 인코딩을 제때 잡는다.
    has_early_charset = "charset" in low[:1024]

    if head_open:
        # 이미 <head>가 있는 완전한 문서 → 부족한 메타만 보충
        insert = ""
        if not has_early_charset:
            insert += CHARSET + "\n"
        if "viewport" not in low:
            insert += VIEWPORT + "\n"
        if insert:
            i = head_open.end()
            html = html[:i] + "\n" + insert.rstrip() + html[i:]
    elif not has_html and not has_body:
        # 조각(title/style/div ...) → 표준 문서로 감싼다
        m = re.search(r"<(div|section|main|header|article|nav|table|img|p)\b", html, flags=re.I)
        cut = m.start() if m else 0
        head_part = html[:cut].strip()
        body_part = html[cut:]
        # 조각 안에 이미 메타가 있으면 중복으로 넣지 않는다
        head_low = head_part.lower()
        metas = ""
        if "charset" not in head_low:
            metas += CHARSET + "\n"
        if "viewport" not in head_low:
            metas += VIEWPORT + "\n"
        html = (
            '<!doctype html>\n<html lang="ko">\n<head>\n'
            + metas
            + head_part
            + "\n</head>\n<body>\n"
            + body_part
            + "\n</body>\n</html>\n"
        )
    else:
        # <html>/<body>는 있는데 <head>가 없는 드문 경우 → head 블록을 만들어 끼운다
        head_block = "<head>\n" + CHARSET + "\n" + VIEWPORT + "\n</head>\n"
        if has_html:
            html = re.sub(r"(<html[^>]*>)", r"\1\n" + head_block, html, count=1, flags=re.I)
        else:
            html = re.sub(r"(<body[^>]*>)", head_block + r"\1", html, count=1, flags=re.I)

    if dst_path is None:
        base, ext = os.path.splitext(src_path)
        dst_path = base + "_공유용" + (ext or ".html")

    # UTF-8, BOM 없이 저장 (BOM은 불필요하고 간혹 첫 글자를 깨뜨린다)
    with io.open(dst_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    return dst_path


def _verify(path):
    with io.open(path, encoding="utf-8") as f:
        head = f.read(1024).lower()
    return "charset" in head


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python make_shareable_html.py <입력.html> [출력.html]", file=sys.stderr)
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else None
    out = make_shareable(src, dst)
    ok = _verify(out)
    print(out)
    if not ok:
        print("경고: 저장된 파일 앞부분에서 charset을 확인하지 못했습니다.", file=sys.stderr)
        sys.exit(2)
