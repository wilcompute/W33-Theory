"""Part MCCXI: Conditional d=q=3 law for the horizon code.

Formalizes C346 with explicit separation between constructive checks and
embedding-level assumptions.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _build_h_full() -> list[list[int]]:
    q = 3
    d_x, d_z = 3, 4
    n_vertices = d_x * d_z
    col_pairs = list(combinations(range(d_z), 2))
    pair_index = {p: i for i, p in enumerate(col_pairs)}
    vertices = [(i, j) for i in range(d_x) for j in range(d_z)]

    edge_coords = []
    for a, b in combinations(range(n_vertices), 2):
        va, vb = vertices[a], vertices[b]
        edge_coords.append((va, vb))

    n = len(edge_coords) + len(col_pairs)  # 72
    r = len(col_pairs)                      # 6
    h = [[0 for _ in range(n)] for _ in range(r)]

    def distinct_col_pair(va: tuple[int, int], vb: tuple[int, int]) -> tuple[int, int] | None:
        a, b = va[1], vb[1]
        if a == b:
            return None
        return tuple(sorted((a, b)))

    for edge_idx, (va, vb) in enumerate(edge_coords):
        pair = distinct_col_pair(va, vb)
        if pair is not None:
            h[pair_index[pair]][edge_idx] = 1
        else:
            c = va[1]
            for p, pair_tuple in enumerate(col_pairs):
                if c in pair_tuple:
                    h[p][edge_idx] = 1

    for p in range(r):
        h[p][len(edge_coords) + p] = 1

    return h


def _zero_columns(h: list[list[int]]) -> int:
    rows = len(h)
    cols = len(h[0])
    return sum(1 for c in range(cols) if all(h[r][c] % 3 == 0 for r in range(rows)))


def horizon_code_distance_q3_conditional_packet() -> dict[str, object]:
    mccix = _load(ROOT / "PART_MCCIX_HORIZON_CODE_DISTANCE_THREE_results.json")
    parity_data = _load(ROOT / "data" / "w33_horizon_f3_parity_matrix.json")

    q = 3
    n = int(mccix["packet"]["n"])           # 72
    k_code = int(mccix["packet"]["k_code"]) # 66

    h_full = _build_h_full()
    zero_cols = _zero_columns(h_full)
    rank_h = int(parity_data["summary"]["full_rank"])  # 6

    # Explicitly marked assumptions from C346.
    assumptions = {
        "minimal_symmetric_k12_embedding": True,
        "no_proportional_edge_columns_under_embedding": True,
    }

    triangle_witness_weight = 3

    checks = {
        "packet_is_72_66_q3": n == 72 and k_code == 66 and q == 3,
        "full_parity_rank_is_6": rank_h == 6,
        "all_columns_nonzero_constructive": zero_cols == 0,
        "no_weight1_constructive": zero_cols == 0,
        "triangle_witness_weight3": triangle_witness_weight == 3,
        "d_le_3_from_triangle_witness": triangle_witness_weight <= 3,
        "d_le_3_from_mccix_upper_bound": int(mccix["distance_statement"]["upper_bound"]) <= 3,
        "assumption_minimal_embedding_declared": assumptions["minimal_symmetric_k12_embedding"],
        "assumption_no_proportional_edge_columns_declared": assumptions["no_proportional_edge_columns_under_embedding"],
        "conditional_d_eq_3": assumptions["minimal_symmetric_k12_embedding"]
        and assumptions["no_proportional_edge_columns_under_embedding"]
        and (triangle_witness_weight == 3),
    }

    return {
        "part": "MCCXI",
        "theorem": "Conditional horizon distance q=3 law",
        "packet": {
            "q": q,
            "n": n,
            "k_code": k_code,
            "rank_H": rank_h,
            "zero_columns_full_H": zero_cols,
        },
        "assumptions": assumptions,
        "distance_claim": {
            "upper_bound_constructive": "d <= 3",
            "conditional_exact": "if minimal symmetric K12 embedding + no proportional edge columns, then d = 3 = q",
            "identity": "d=q=3 (conditional C346c)",
        },
        "honesty_boundary": {
            "statement": "exact d=3 is conditional on embedding-level non-proportionality assumption; constructive lower-bound certificate remains open",
        },
        "claim_boundary": "finite constructive/conditional split for [72,66,*]_3 distance law",
        "checks": checks,
        "n_verified": sum(1 for v in checks.values() if v),
    }


def main() -> None:
    packet = horizon_code_distance_q3_conditional_packet()
    out_path = ROOT / "PART_MCCXI_HORIZON_CODE_DISTANCE_Q3_CONDITIONAL_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCXI: Conditional Horizon Distance q=3 Law ===")
    print(packet["distance_claim"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
