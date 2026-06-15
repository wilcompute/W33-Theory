#!/usr/bin/env python3
"""BT1085 paper integration helper.

Inserts the BT1083--BT1085 sections into the W33 preprint and photonic
holonet paper at stable section boundaries.  The script is intentionally
idempotent.
"""
from pathlib import Path

INSERT_W33 = r"""
% BT1085 matter bridge update
\input{sections/sec_bt1083_1085_matter_bridge}
""".strip() + "\n\n"

INSERT_HOLONET = r"""
% BT1085 holonet runtime bridge update
\input{paper/sections/sec_bt1083_1085_holonet_bridge}
""".strip() + "\n\n"


def insert_once(path: Path, marker: str, insert: str) -> None:
    text = path.read_text(encoding="utf-8")
    if insert.strip() in text:
        return
    if marker not in text:
        raise RuntimeError(f"marker not found in {path}: {marker}")
    text = text.replace(marker, insert + marker, 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    insert_once(
        Path("paper/w33_preprint.tex"),
        "\\section{The TOE Singularity Theorem}",
        INSERT_W33,
    )
    insert_once(
        Path("photonic_holonet.tex"),
        "\\subsection{The ethos}",
        INSERT_HOLONET,
    )


if __name__ == "__main__":
    main()
