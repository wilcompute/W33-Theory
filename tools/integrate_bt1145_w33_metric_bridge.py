#!/usr/bin/env python3
"""Integrate BT1145 metric bridge theorem into w33_paper.tex."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "w33_paper.tex"
INSERT = ROOT / "analysis" / "BT1145_w33_metric_bridge_insert.tex"
MARKER = "\\begin{theorem}[The complete spectral action of $W(3,3)$]"
SENTINEL = "\\label{thm:k3-w33-metric-bridge}"
PREREQ = "\\label{rem:k3-a4-convention-table}"


def main() -> int:
    text = PAPER.read_text(encoding="utf-8")
    if SENTINEL in text:
        print("BT1145 already present")
        return 0
    if PREREQ not in text:
        raise RuntimeError("BT1142 convention table missing")
    if MARKER not in text:
        raise RuntimeError("complete spectral action marker missing")
    insert = INSERT.read_text(encoding="utf-8").strip() + "\n\n"
    PAPER.write_text(text.replace(MARKER, insert + MARKER, 1), encoding="utf-8")
    print("BT1145 integrated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
