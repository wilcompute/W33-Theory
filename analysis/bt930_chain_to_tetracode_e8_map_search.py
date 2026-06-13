#!/usr/bin/env python3
"""BT930 - map the BT925 chain form into the tetracode E8 coordinates.

This is the independent companion to BT929.  Instead of using the vertex Cartan
witness, it imports the W33 tetracode E8 root-system packet, extracts its simple
root Gram matrix, and builds a mod-2 isometry from the BT925 chain form into
that tetracode metric basis.
"""
from __future__ import annotations
from fractions import Fraction
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_tetracode_e8_root_system_bridge import tetracode_e8_root_system_packet  # noqa: E402

OUT = ROOT / "data/bt930_chain_to_tetracode_e8_map_search.json"
B_CHAIN = np.array([[0,1,0,0,1,0,0,1],[1,0,0,0,1,1,1,1],[0,0,0,1,1,0,0,1],[0,0,1,0,1,1,1,1],[1,1,1,1,0,1,0,1],[0,1,0,1,1,0,1,1],[0,1,0,1,0,1,0,0],[1,1,1,1,1,1,0,0]], dtype=np.int64) % 2
S_CHAIN = np.array([[1,0,1,0,1,0,0,0],[0,1,0,1,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1],[0,0,0,0,1,0,1,0],[0,0,0,0,0,1,0,1],[0,0,1,1,1,0,0,1],[0,0,0,1,1,1,1,0]], dtype=np.int64) % 2


def parse_frac(s: str) -> Fraction:
    if "/" in s:
        a, b = s.split("/")
        return Fraction(int(a), int(b))
    return Fraction(int(s), 1)


def determinant_int(M):
    return int(round(np.linalg.det(np.array(M, dtype=float))))


def f2_rref(M):
    M = (np.array(M, dtype=np.int64) % 2).copy()
    rows, cols = M.shape
    pr = 0
    pivots = []
    for c in range(cols):
        piv = next((i for i in range(pr, rows) if M[i, c]), None)
        if piv is None:
            continue
        M[[pr, piv]] = M[[piv, pr]]
        for i in range(rows):
            if i != pr and M[i, c]:
                M[i] ^= M[pr]
        pivots.append(c)
        pr += 1
    return M[:pr], pivots


def f2_inv(M):
    M = (np.array(M, dtype=np.int64) % 2).copy()
    n = M.shape[0]
    aug = np.concatenate([M, np.eye(n, dtype=np.int64)], axis=1)
    row = 0
    for col in range(n):
        piv = next((i for i in range(row, n) if aug[i, col]), None)
        if piv is None:
            raise ValueError("singular over F2")
        aug[[row, piv]] = aug[[piv, row]]
        for i in range(n):
            if i != row and aug[i, col]:
                aug[i] ^= aug[row]
        row += 1
    return aug[:, n:] % 2


def symplectic_basis_from_gram(G):
    G = np.array(G, dtype=np.int64) % 2
    n = G.shape[0]
    basis = [np.eye(n, dtype=np.int64)[i] for i in range(n)]
    pairs = []
    while basis:
        e = basis.pop(0)
        j = next(i for i, f in enumerate(basis) if int(e @ G @ f) % 2 == 1)
        f = basis.pop(j)
        pairs.append((e.copy(), f.copy()))
        new = []
        for g in basis:
            be = int(g @ G @ e) % 2
            bf = int(g @ G @ f) % 2
            g2 = g.copy()
            if bf: g2 ^= e
            if be: g2 ^= f
            new.append(g2)
        if new:
            R, _ = f2_rref(np.array(new, dtype=np.int64))
            basis = [row.copy() % 2 for row in R]
        else:
            basis = []
    return np.column_stack([v for pair in pairs for v in pair]) % 2


def main():
    packet = tetracode_e8_root_system_packet()
    simple_gram_str = packet["simple_root_system"]["gram_matrix"]
    G = np.array([[int(parse_frac(x)) for x in row] for row in simple_gram_str], dtype=np.int64)
    G2 = G % 2
    S_tetra = symplectic_basis_from_gram(G2)
    M = (S_tetra @ f2_inv(S_CHAIN)) % 2
    assert np.array_equal((M.T @ G2 @ M) % 2, B_CHAIN)
    Mint = M.astype(np.int64)
    G_lift = Mint.T @ G @ Mint
    eig = np.linalg.eigvalsh(G_lift.astype(float))
    result = {
        "theorem": "BT930 chain-to-tetracode E8 map search",
        "tetracode_root_count": packet["root_system"]["count"],
        "tetracode_rank": packet["root_system"]["rank"],
        "tetracode_source_profile": packet["root_system"]["source_profile"],
        "tetracode_simple_gram_determinant": packet["simple_root_system"]["gram_determinant"],
        "mod2_isometry_matrix_M_chain_to_tetracode": Mint.astype(int).tolist(),
        "check_Mt_Gtetracode_M_equals_Bchain_mod2": True,
        "integer_lift_det_M": determinant_int(Mint),
        "lifted_gram_det": determinant_int(G_lift),
        "lifted_gram_positive_definite": bool(eig.min() > 1e-9),
        "lifted_gram_min_eigenvalue": float(eig.min()),
        "status": "explicit mod-2 chain-to-tetracode isometry; integral lift is an E8 basis in tetracode metric coordinates, but still basis-dependent",
        "checks": {
            "T1_tetracode_packet_imported": True,
            "T2_tetracode_is_240_root_E8": packet["checks"]["root_count_is_240"] and packet["checks"]["rank_is_8"],
            "T3_mod2_isometry_found": True,
            "T4_integral_lift_positive_definite": bool(eig.min() > 1e-9),
            "T5_canonicality_not_claimed": True,
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT930 wrote", OUT)


if __name__ == "__main__":
    main()
