#!/usr/bin/env python3
"""Idempotently integrate Passes 3153-3162 into all canonical front doors."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = [
    ROOT / "w33_paper.tex",
    ROOT / "photonic_holonet.tex",
    ROOT / "holonet_machine_blueprint.tex",
]
HTML = ROOT / "docs" / "index.html"
TB = "% BEGIN BT3153-BT3162 ADAPTIVE EPOCH FACTOR ENGINE"
TE = "% END BT3153-BT3162 ADAPTIVE EPOCH FACTOR ENGINE"
HB = "<!-- BEGIN BT3153-BT3162 ADAPTIVE EPOCH FACTOR ENGINE -->"
HE = "<!-- END BT3153-BT3162 ADAPTIVE EPOCH FACTOR ENGINE -->"
TEX_BLOCK = (
    f"\n{TB}\n"
    "\\input{analysis/BT3153_BT3162_adaptive_epoch_factor_insert}\n"
    f"{TE}\n"
)
HTML_BODY = (
    ROOT / "analysis" / "BT3153_BT3162_adaptive_epoch_factor_index_insert.html"
).read_text(encoding="utf-8").strip()
HTML_BLOCK = f"\n{HB}\n{HTML_BODY}\n{HE}\n"


def splice_bytes(
    data: bytes, begin: bytes, end: bytes, block: bytes, anchor: bytes
) -> bytes:
    """Splice without decoding legacy TeX bytes outside the generated block."""
    if begin in data:
        start = data.index(begin)
        stop = data.index(end, start) + len(end)
        return data[:start] + block.strip(b"\n") + data[stop:]
    position = data.rfind(anchor)
    if position < 0:
        raise RuntimeError(f"missing byte anchor {anchor!r}")
    return data[:position] + block + data[position:]


def splice_text(text: str, begin: str, end: str, block: str, anchor: str) -> str:
    if begin in text:
        start = text.index(begin)
        stop = text.index(end, start) + len(end)
        return text[:start] + block.strip("\n") + text[stop:]
    position = text.rfind(anchor)
    if position < 0:
        raise RuntimeError(f"missing anchor {anchor!r}")
    return text[:position] + block + text[position:]


def main() -> None:
    begin = TB.encode("utf-8")
    end = TE.encode("utf-8")
    block = TEX_BLOCK.encode("utf-8")
    anchor = b"\\end{document}"
    for path in TEX:
        path.write_bytes(splice_bytes(path.read_bytes(), begin, end, block, anchor))

    html = HTML.read_text(encoding="utf-8")
    HTML.write_text(
        splice_text(html, HB, HE, HTML_BLOCK, "</body>"), encoding="utf-8"
    )
    print("BT3153-BT3162 adaptive epoch factor engine integrated")


if __name__ == "__main__":
    main()
