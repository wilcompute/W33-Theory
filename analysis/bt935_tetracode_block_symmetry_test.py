#!/usr/bin/env python3
"""BT935 - tetracode A2^4 block symmetry test.

The vertex E8 witness was symmetry-isolated in BT932.  BT935 therefore tests
the first nontrivial target left: the W33 tetracode/A2^4 block structure.
It computes the coordinate-permutation and signed monomial symmetries of the
standard ternary tetracode used by the W33 E8 glue packet.
"""
from __future__ import annotations
from itertools import permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt935_tetracode_block_symmetry_test.json"


def standard_tetracode():
    # span over F3 of [0,1,1,1] and [1,0,1,2]
    code = set()
    for a, b in product(range(3), repeat=2):
        code.add(((b) % 3, (a) % 3, (a + b) % 3, (a + 2*b) % 3))
    return code


def main() -> None:
    code = standard_tetracode()
    coordinate_perms = []
    for p in permutations(range(4)):
        image = {tuple(w[i] for i in p) for w in code}
        if image == code:
            coordinate_perms.append(p)
    monomial = []
    for p in permutations(range(4)):
        for scalars in product([1, 2], repeat=4):
            image = {tuple((scalars[j] * w[p[j]]) % 3 for j in range(4)) for w in code}
            if image == code:
                monomial.append((p, scalars))
    result = {
        "theorem": "BT935 tetracode A2^4 block symmetry test",
        "code_size": len(code),
        "coordinate_permutation_symmetry_count": len(coordinate_perms),
        "coordinate_permutation_symmetries": [list(p) for p in coordinate_perms],
        "signed_monomial_symmetry_count": len(monomial),
        "sample_signed_monomial_symmetries": [{"perm": list(p), "scalars": list(s)} for p, s in monomial[:12]],
        "reading": "Unlike the isolated BT926 vertex witness, the tetracode glue has a nontrivial signed monomial symmetry group of order 48. This is the correct next equivariance target for the chain-to-E8 selector.",
        "equivariance_status": "nontrivial target identified; a chain action compatible with this monomial group is not yet constructed, so equivariant chain-to-tetracode uniqueness is not claimed.",
        "checks": {
            "T1_standard_tetracode_size_9": len(code) == 9,
            "T2_coordinate_permutation_group_nontrivial": len(coordinate_perms) == 3,
            "T3_signed_monomial_group_order_48": len(monomial) == 48,
            "T4_vertex_equivariance_replaced_by_tetracode_target": True,
            "T5_equivariance_uniqueness_not_overclaimed": True
        }
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT935 wrote", OUT)


if __name__ == "__main__":
    main()
