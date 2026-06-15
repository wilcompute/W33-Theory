#!/usr/bin/env python3
"""BT1097 cumulative paper integration helper.

Idempotently inserts BT1083--BT1096 paper sections into the W33 preprint and
photonic holonet source at stable boundaries.
"""
from pathlib import Path

W33_INSERTS = [
    "% BT1085 matter bridge update\n\\input{sections/sec_bt1083_1085_matter_bridge}\n\n",
    "% BT1088 core reservoir update\n\\input{sections/sec_bt1086_1088_core_reservoir}\n\n",
    "% BT1090 natural core/intertwiner update\n\\input{sections/sec_bt1089_1090_natural_core_intertwiner}\n\n",
    "% BT1093 explicit quotient/cube update\n\\input{sections/sec_bt1092_1093_explicit_quotient_cube}\n\n",
    "% BT1096 A12/K matrix update\n\\input{sections/sec_bt1095_1096_A12_K_matrix}\n\n",
]

HOLONET_INSERTS = [
    "% BT1085 holonet runtime bridge update\n\\input{paper/sections/sec_bt1083_1085_holonet_bridge}\n\n",
    "% BT1088 holonet reservoir runtime update\n\\input{paper/sections/sec_bt1086_1088_holonet_reservoir_runtime}\n\n",
    "% BT1090 holonet natural core/intertwiner update\n\\input{paper/sections/sec_bt1089_1090_holonet_core_intertwiner}\n\n",
    "% BT1093 holonet quotient/cube update\n\\input{paper/sections/sec_bt1092_1093_holonet_quotient_cube}\n\n",
    "% BT1096 holonet A12/K matrix update\n\\input{paper/sections/sec_bt1095_1096_holonet_A12_K_matrix}\n\n",
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
