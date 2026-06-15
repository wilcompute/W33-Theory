#!/usr/bin/env python3
"""BT1096: sparse matrix for K:T66 -> A12.

Domain ordering: three generation blocks.  Each block has F13 followed by D9:
  gen g starts at 22*g; F13 columns start+0..start+12; D9 start+13..start+21.
Target ordering is BT1095 A12 basis with 12 rows.
"""
from __future__ import annotations

import json
from pathlib import Path
from fractions import Fraction

entries = []
for row in range(12):
    for g in range(3):
        start = 22 * g
        entries.append({"row": row, "col": start + row, "value": "1/3"})
        entries.append({"row": row, "col": start + 12, "value": "-1/3"})

out = {
    "theorem": "BT1096 reservoir K matrix",
    "shape": "12 x 66",
    "domain_order": "for each generation: F13 columns 0..12 then D9 columns 13..21",
    "target_order": ["Y", "W0", "Wp", "Wm", "C12", "C21", "C13", "C31", "C23", "C32", "C0", "C8"],
    "nonzero_entries": entries,
    "rank": 12,
    "kernel_dimension": 54,
    "row_rule": "for target row i, put +1/3 on F13_i(g) and -1/3 on F13_12(g) for all three generations; all D9 columns vanish",
    "boundary": "sparse rational matrix for the generation-averaged trace-free quotient; target basis is the BT1095 complexified A12 basis"
}
Path("data").mkdir(exist_ok=True)
Path("data/bt1096_reservoir_K_matrix.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps(out, indent=2))
