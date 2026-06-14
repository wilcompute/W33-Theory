#!/usr/bin/env python3
"""BT959 - transported S4 orbit/stabilizer of the final selector.

Uses the recovered BT956 chain-to-tetracode matrix.  The explicit action that is
safe to transport today is the tetracode block-permutation quotient S4.  The
local A2/Weyl/glue stabilizer refinement remains a separate problem.

Result: the final selector has trivial S4 stabilizer and a 24-element S4 orbit.
That orbit intersects the six support-60 minimizers only at the selected
minimizer itself.
"""
from __future__ import annotations
from itertools import permutations
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt959_selected_minimizer_stabilizer_orbit.json"

M = np.array([
    [1,0,1,0,1,0,0,0],
    [0,0,0,1,0,1,0,1],
    [0,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,0,1,0,1,0,0],
    [0,0,1,0,0,0,0,0],
    [0,0,1,0,0,1,1,1],
    [0,1,0,0,1,0,0,1]
], dtype=np.uint8)

SELECTED = ((3,68),(4,42),(38,65),(90,144))
MINIMIZERS = [
    ((1,42),(12,65),(41,68),(90,144)),
    ((1,42),(12,65),(68,109),(90,144)),
    ((3,68),(4,42),(38,65),(90,144)),
    ((3,68),(12,65),(42,69),(90,144)),
    ((3,68),(12,65),(42,111),(90,144)),
    ((3,68),(12,89),(42,111),(90,144)),
]


def inv2(A):
    A = A.copy() % 2
    n = A.shape[0]
    aug = np.concatenate([A, np.eye(n, dtype=np.uint8)], axis=1)
    row = 0
    for col in range(n):
        piv = next(i for i in range(row, n) if aug[i, col])
        aug[[row, piv]] = aug[[piv, row]]
        for i in range(n):
            if i != row and aug[i, col]:
                aug[i] ^= aug[row]
        row += 1
    return aug[:, n:] % 2


def block_perm_matrix(perm):
    R = np.zeros((8,8), dtype=np.uint8)
    for target_block, source_block in enumerate(perm):
        for j in range(2):
            R[2*target_block+j, 2*source_block+j] = 1
    return R


def mask_to_vec(m):
    return np.array([(m >> i) & 1 for i in range(8)], dtype=np.uint8)


def vec_to_mask(v):
    out = 0
    for i, bit in enumerate(v.tolist()):
        if bit & 1:
            out |= 1 << i
    return out


def canon_dec(dec):
    return tuple(sorted(tuple(sorted(pair)) for pair in dec))


def act(T, dec):
    out = []
    for a,b in dec:
        aa = vec_to_mask((T @ mask_to_vec(a)) % 2)
        bb = vec_to_mask((T @ mask_to_vec(b)) % 2)
        out.append((aa,bb))
    return canon_dec(out)


def main():
    Minv = inv2(M)
    selected = canon_dec(SELECTED)
    support_set = {canon_dec(d) for d in MINIMIZERS}
    orbit = set()
    stabilizer = []
    for p in permutations(range(4)):
        R = block_perm_matrix(p)
        T = (Minv @ R @ M) % 2
        image = act(T, selected)
        orbit.add(image)
        if image == selected:
            stabilizer.append(p)
    orbit_support = sorted(orbit & support_set)
    result = {
        "theorem": "BT959 transported S4 orbit/stabilizer of final selector",
        "transported_group": "tetracode block-permutation quotient S4 via BT956 matrix",
        "selected_minimizer": [list(p) for p in selected],
        "group_order": 24,
        "orbit_size": len(orbit),
        "stabilizer_size": len(stabilizer),
        "stabilizer_permutations": [list(p) for p in stabilizer],
        "orbit_intersection_with_support60_minimizers_count": len(orbit_support),
        "orbit_intersection_with_support60_minimizers": [[list(p) for p in d] for d in orbit_support],
        "orbit_sample_first_5": [[list(p) for p in d] for d in sorted(orbit)[:5]],
        "reading": "Under the strongest explicit transported quotient currently available, the final selector is S4-rigid inside the six support-60 minimizers: its S4 orbit has size 24, but only the original selected minimizer remains support-minimal.",
        "boundary": "This is the transported block-permutation quotient. It does not yet include a fully transported local A2/Weyl glue stabilizer action.",
        "checks": {"T1_orbit_size_24": len(orbit) == 24, "T2_stabilizer_trivial": len(stabilizer) == 1, "T3_support60_intersection_singleton": len(orbit_support) == 1, "T4_selected_in_intersection": selected in orbit_support, "T5_full_local_A2_boundary_explicit": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT959 wrote", OUT)

if __name__ == "__main__":
    main()
