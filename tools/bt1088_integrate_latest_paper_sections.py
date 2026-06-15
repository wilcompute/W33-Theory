#!/usr/bin/env python3
"""BT1088 cumulative paper integration helper.

Idempotently inserts the BT1083--BT1085 and BT1086--BT1088 paper sections
into the W33 preprint and photonic holonet source at stable boundaries.
"""
from pathlib import Path

W33_INSERTS = [
    "% BT1085 matter bridge update\n\\input{sections/sec_bt1083_1085_matter_bridge}\n\n",
    "% BT1088 core reservoir update\n\\input{sections/sec_bt1086_1088_core_reservoir}\n\n",
]

HOLONET_INSERTS = [
    "% BT1085 holonet runtime bridge update\n\\input{paper/sections/sec_bt1083_1085_holonet_bridge}\n\n",
    "% BT1088 holonet reservoir runtime update\n\\input{paper/sections/sec_bt1086_1088_holonet_reservoir_runtime}\n\n",
]


def insert_before(path: Path, marker: str, inserts: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    block = "".join(x for x in inserts if x.strip() not in text)
    if not block:
        return
    if marker not in text:
        raise RuntimeError(f"marker not found in {path}: {marker}")
    text = text.replace(marker, block + marker, 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    insert_before(Path("paper/w33_preprint.tex"), "\\section{The TOE Singularity Theorem}", W33_INSERTS)
    insert_before(Path("photonic_holonet.tex"), "\\subsection{The ethos}", HOLONET_INSERTS)


if __name__ == "__main__":
    main()
