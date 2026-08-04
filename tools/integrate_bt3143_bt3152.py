#!/usr/bin/env python3
"""Idempotently integrate Passes 3143--3152 into all canonical front doors."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX_FILES = [ROOT / "w33_paper.tex", ROOT / "photonic_holonet.tex", ROOT / "holonet_machine_blueprint.tex"]
HTML = ROOT / "docs" / "index.html"
TEX_BEGIN = "% BEGIN BT3143-BT3152 FIVE FRONT CLOSURE"
TEX_END = "% END BT3143-BT3152 FIVE FRONT CLOSURE"
TEX_BLOCK = (
    f"\n{TEX_BEGIN}\n"
    "\\input{analysis/BT3143_BT3152_five_front_closure_insert}\n"
    f"{TEX_END}\n"
)
HTML_BEGIN = "<!-- BEGIN BT3143-BT3152 FIVE FRONT CLOSURE -->"
HTML_END = "<!-- END BT3143-BT3152 FIVE FRONT CLOSURE -->"
HTML_BODY = (ROOT / "analysis" / "BT3143_BT3152_five_front_closure_index_insert.html").read_text(encoding="utf-8").strip()
HTML_BLOCK = f"\n{HTML_BEGIN}\n{HTML_BODY}\n{HTML_END}\n"


def replace_or_insert(text, begin, end, block, anchor):
    if begin in text:
        start = text.index(begin)
        stop = text.index(end, start) + len(end)
        return text[:start] + block.strip("\n") + text[stop:]
    pos = text.rfind(anchor)
    if pos < 0:
        raise RuntimeError(f"anchor {anchor!r} not found")
    return text[:pos] + block + text[pos:]


def main():
    for path in TEX_FILES:
        source = path.read_text(encoding="utf-8")
        path.write_text(replace_or_insert(source, TEX_BEGIN, TEX_END, TEX_BLOCK, "\\end{document}"), encoding="utf-8")
    source = HTML.read_text(encoding="utf-8")
    HTML.write_text(replace_or_insert(source, HTML_BEGIN, HTML_END, HTML_BLOCK, "</body>"), encoding="utf-8")
    print("BT3143-BT3152 five-front closure integrated")


if __name__ == "__main__":
    main()
