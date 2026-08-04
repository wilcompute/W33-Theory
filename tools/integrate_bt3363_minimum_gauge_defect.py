#!/usr/bin/env python3
"""Idempotently integrate BT3363 into the three wrapper papers and public index."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX_INPUT = r"\input{analysis/BT3363_minimum_gauge_defect_generation_insert}%"
HTML_ID = 'id="bt3363-minimum-gauge-defect-generation"'
TARGETS = ("w33_paper.tex", "photonic_holonet.tex", "holonet_machine_blueprint.tex")


def integrate_tex(text: str) -> str:
    if TEX_INPUT in text:
        return text
    anchor = "  }%\n}\n\\input{"
    if anchor not in text:
        raise ValueError("missing lightweight-wrapper insertion anchor")
    pos = text.index(anchor)
    return text[:pos] + f"    {TEX_INPUT}\n" + text[pos:]


def integrate_html(text: str, insert: str) -> str:
    if HTML_ID in text:
        return text
    lower = text.lower()
    pos = lower.rfind("</main>")
    if pos < 0:
        pos = lower.rfind("</body>")
    if pos < 0:
        raise ValueError("missing HTML insertion point")
    return text[:pos] + insert.rstrip() + "\n" + text[pos:]


def main() -> None:
    for name in TARGETS:
        path = ROOT / name
        old = path.read_text(encoding="utf-8")
        path.write_text(integrate_tex(old), encoding="utf-8")
    insert = (ROOT / "analysis/BT3363_minimum_gauge_defect_generation_index_insert.html").read_text(encoding="utf-8")
    path = ROOT / "docs/index.html"
    old = path.read_text(encoding="utf-8")
    path.write_text(integrate_html(old, insert), encoding="utf-8")
    print("integrated BT3363 into all four public front doors")


if __name__ == "__main__":
    main()
