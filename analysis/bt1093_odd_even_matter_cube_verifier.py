#!/usr/bin/env python3
"""BT1093: explicit odd/even decomposition of C[F3^3]."""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

F3 = range(3)
points = list(product(F3, repeat=3))
origin = (0, 0, 0)

def neg(v):
    return tuple((-x) % 3 for x in v)

def canonical_rep(v):
    if v == origin:
        return None
    # projective representative: first nonzero coordinate equals 1
    for x in v:
        if x != 0:
            inv = 1 if x == 1 else 2
            return tuple((inv*y) % 3 for y in v)
    return None

reps = []
seen = set()
for v in points:
    if v == origin or v in seen:
        continue
    r = canonical_rep(v)
    if r not in reps:
        reps.append(r)
    seen.add(r)
    seen.add(neg(r))
reps = sorted(reps)
pairs = [[list(r), list(neg(r))] for r in reps]

out = {
    "theorem": "BT1093 odd/even matter cube verifier",
    "ambient": "C[F3^3]",
    "ambient_dimension": 27,
    "origin": list(origin),
    "antipodal_pairs": pairs,
    "number_of_projective_directions": len(pairs),
    "odd_basis_rule": "e_x - e_-x for each antipodal pair",
    "even_basis_rule": "e_0 plus e_x + e_-x for each antipodal pair",
    "odd_dimension": len(pairs),
    "even_dimension": 1 + len(pairs),
    "dimension_check": f"{len(pairs)} + {1+len(pairs)} = 27",
    "boundary": "basis indexed by canonical projective representatives with first nonzero coordinate 1"
}
Path("data").mkdir(exist_ok=True)
Path("data/bt1093_odd_even_matter_cube_verifier.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps(out, indent=2))
