#!/usr/bin/env python3
"""BT781: generated action on the H15 frame."""
from __future__ import annotations

import json
from collections import Counter, deque
from pathlib import Path

import networkx as nx
import numpy as np

from bt766_intrinsic_k44_octet_quotient import build_w33

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT781_H15_FRAME_ACTION_summary.json"
MOD = 3
J = np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]], dtype=int) % MOD


def key(M):
    return tuple(int(x) % MOD for x in M.flatten())


def norm(v):
    v = tuple(int(x) % MOD for x in v)
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv*y) % MOD for y in v)
    raise ValueError("zero")


def apply(M, p):
    return norm(tuple((M @ np.array(p, dtype=int)) % MOD))


def tv(v):
    vv = np.array(v, dtype=int).reshape(4,1)
    return (np.eye(4, dtype=int) + vv @ ((J @ vv) % MOD).T) % MOD


def generate(pts):
    gens = []
    seen = set()
    for p in pts:
        T = tv(p)
        if key(T) not in seen:
            seen.add(key(T)); gens.append(T)
    I = np.eye(4, dtype=int) % MOD
    group = {key(I): I}
    q = deque([I])
    while q:
        A = q.popleft()
        for g in gens:
            B = (A @ g) % MOD
            k = key(B)
            if k not in group:
                group[k] = B; q.append(B)
    return gens, group


def main():
    pts, lines, idx, G, point_lines = build_w33()
    A = nx.to_numpy_array(G, nodelist=range(40), dtype=int)
    H = 8*np.eye(40, dtype=int) - 4*A + np.ones((40,40), dtype=int)
    gens, group = generate(pts)
    perms = set()
    ok_gram = True
    for M in group.values():
        perm = tuple(idx[apply(M, p)] for p in pts)
        perms.add(perm)
        for i in range(40):
            for j in range(40):
                if H[perm[i], perm[j]] != H[i, j]:
                    ok_gram = False
                    break
            if not ok_gram:
                break
        if not ok_gram:
            break
    eig = Counter(int(round(x)) for x in np.linalg.eigvalsh(H))
    checks = {
        "generators_40": len(gens) == 40,
        "matrix_order_51840": len(group) == 51840,
        "projective_order_25920": len(perms) == 25920,
        "central_kernel_2": len(group) // len(perms) == 2,
        "gram_preserved": ok_gram,
        "H15_spectrum": eig == Counter({24:15, 0:25}),
    }
    result = {
        "theorem": "BT781 H15 generated frame action",
        "summary": {
            "matrix_group_order": len(group),
            "projective_permutation_order": len(perms),
            "central_kernel_size": len(group)//len(perms),
            "frame_vectors": 40,
            "frame_dimension": 15,
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "This verifies the generated PSp(4,3) action preserves the H15 Gram frame. It does not independently enumerate every graph automorphism."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
