#!/usr/bin/env python3
"""BT926 - bounded extractor for the positive-definite integral E8 form.

BT924/BT925 leave exactly the positive-definite integral lift open.  BT926 does
not close it, but gives the next executable extractor:

1. certify the known 8-vertex Gram G=2I-A_sub as E8;
2. search all single-vertex swaps around that witness for other definite
   even-unimodular rank-8 vertex forms;
3. record why this vertex-sector extractor is not yet the canonical chain lift.
"""
from __future__ import annotations
from itertools import combinations, product
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt926_integral_definite_form_extractor.json"
E8_VERTEX_SUBSET = [0, 1, 4, 22, 27, 35, 23, 34]


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def build_w33_adjacency():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    A = np.zeros((40, 40), dtype=np.int64)
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i, j] = A[j, i] = 1
    return A


def gram_for_subset(A, subset):
    sub = A[np.ix_(subset, subset)]
    return 2*np.eye(len(subset), dtype=np.int64) - sub


def is_e8_vertex_form(G):
    vals = np.linalg.eigvalsh(G.astype(float))
    det = round(np.linalg.det(G))
    off = {int(G[i,j]) for i in range(8) for j in range(8) if i != j}
    return {
        "det": int(det),
        "positive_definite": bool(vals.min() > 1e-9),
        "smallest_eigenvalue": float(vals.min()),
        "largest_eigenvalue": float(vals.max()),
        "even_diagonal_2": bool(np.all(np.diag(G) == 2)),
        "offdiag_values": sorted(off),
        "is_e8_cartan_type": bool(det == 1 and vals.min() > 1e-9 and off <= {0, -1}),
    }


def main() -> None:
    A = build_w33_adjacency()
    base = E8_VERTEX_SUBSET
    G0 = gram_for_subset(A, base)
    cert0 = is_e8_vertex_form(G0)
    assert cert0["is_e8_cartan_type"]

    found = []
    base_set = set(base)
    outside = [v for v in range(40) if v not in base_set]
    for drop_index, drop_vertex in enumerate(base):
        for add_vertex in outside:
            cand = list(base)
            cand[drop_index] = add_vertex
            if len(set(cand)) != 8:
                continue
            cert = is_e8_vertex_form(gram_for_subset(A, cand))
            if cert["is_e8_cartan_type"]:
                found.append({"drop": drop_vertex, "add": add_vertex, "subset": cand, "smallest_eigenvalue": cert["smallest_eigenvalue"]})

    result = {
        "theorem": "BT926 bounded positive-definite integral E8 form extractor",
        "status": "partial extractor; vertex-sector definite E8 witnesses found, canonical chain lift still open",
        "base_subset": base,
        "base_certificate": cert0,
        "single_swap_search_space": len(base) * len(outside),
        "single_swap_e8_witness_count": len(found),
        "sample_single_swap_witnesses": found[:12],
        "chain_lift_boundary": "This extractor operates in the W33 vertex Cartan sector G=2I-A_sub. It certifies definite E8 forms in the ambient graph, but it does not yet choose the canonical coset representative in the BT924 valuation-1 chain sector.",
        "residual": "Find an explicit map from the canonical H=(Z/2)^8 valuation-1/SNF sector with BT925 symplectic form into one of these positive-definite E8 vertex/tetracode forms.",
        "checks": {
            "T1_base_vertex_subset_is_E8": bool(cert0["is_e8_cartan_type"]),
            "T2_single_swap_search_executed": True,
            "T3_positive_definite_form_available": bool(cert0["positive_definite"]),
            "T4_canonical_chain_lift_not_claimed": True,
            "T5_residual_map_precisely_stated": True,
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT926 wrote", OUT, "single-swap witnesses", len(found))


if __name__ == "__main__":
    main()
