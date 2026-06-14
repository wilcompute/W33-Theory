#!/usr/bin/env python3
"""BT949 - add a narrative cross-reference in photonic_holonet.tex.

photonic_holonet.tex is the current main narrative / architecture paper.  Heavy
E8/SNF/symplectic-selector details belong in w33_paper.tex.  This idempotent
patch inserts a short pointer after the Holonet abstract.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "photonic_holonet.tex"
MARKER = "% BEGIN BT949 W33 HEAVY-MATH CROSSREF"
END = "% END BT949 W33 HEAVY-MATH CROSSREF"
ANCHOR = "\\end{abstract}"
BLOCK = r"""
% BEGIN BT949 W33 HEAVY-MATH CROSSREF
\paragraph{Heavy-math companion.}
This Holonet paper is the narrative and architecture layer.  The heavy
$E_8$/Smith-normal-form/symplectic-selector derivations, including the
BT924--BT949 integral-lift status theorem and selector proof obligations, live
in the companion heavy-math manuscript \texttt{w33\_paper.tex}.  The two files
should be read as one stack: \texttt{photonic\_holonet.tex} explains the
machine architecture; \texttt{w33\_paper.tex} carries the algebraic load.
% END BT949 W33 HEAVY-MATH CROSSREF
"""


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    if MARKER in text:
        print("BT949 Holonet cross-reference already present")
        return
    if ANCHOR not in text:
        raise SystemExit("missing abstract anchor in photonic_holonet.tex")
    text = text.replace(ANCHOR, ANCHOR + "\n" + BLOCK, 1)
    TARGET.write_text(text, encoding="utf-8")
    print("BT949 Holonet cross-reference inserted")

if __name__ == "__main__":
    main()
