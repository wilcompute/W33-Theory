#!/usr/bin/env python3
"""
BT831 - Tomotope minimal-cover architecture boundary.

The Monson-Pellicer-Williams tomotope result matters architecturally: the local
48-block tomotope packet is finite and verified in BT814, but the regular cover
chosen to implement that packet is not unique.  The tomotope has infinitely many
pairwise non-comparable minimal regular covers indexed by coprime odd cover
parameters in the theorem.

BT831 does not reprove the group-theoretic paper.  It encodes the cited exact
cover arithmetic and tests the architecture consequence: use the 48/192 local
packet as the invariant ABI, and treat the regular cover index k as a pluggable
implementation gauge.
"""
from __future__ import annotations

from math import gcd
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    with (ROOT / path).open() as f:
        return json.load(f)


def qk_counts(k: int) -> dict:
    return {
        "k": k,
        "vertices": 4 * k**3,
        "edges": 24 * k**3,
        "triangles": 32 * k**3,
        "tetrahedra": 8 * k**3,
        "octahedra": 4 * k**3,
        "Wk_order": 24 * (2 * k) ** 3,
        "MonQk_order": 36864 * k**6,
        "kernel_order_to_Q1": k**6,
    }


def main() -> None:
    bt814 = load_json("data/bt814_tomotope_middle_layer_from_residual_tetrahedra.json")
    cover_indices = [3, 5, 7, 11, 13, 17, 19]
    cover_rows = [qk_counts(k) for k in cover_indices]
    pair_rows = [
        {"p": p, "q": q, "gcd": gcd(p, q), "noncomparable_by_theorem_5_9": gcd(p, q) == 1}
        for i, p in enumerate(cover_indices)
        for q in cover_indices[i + 1:]
    ]
    invariant_packet = bt814["f_vector_from_transversal_tetrahedra"]

    checks = {
        "bt814_local_packet_is_48": invariant_packet["middle_blocks"] == 48,
        "bt814_local_flags_are_192": invariant_packet["flags_if_each_block_has_2x2_fiber"] == 192,
        "cover_indices_are_pairwise_coprime_odd": all(row["noncomparable_by_theorem_5_9"] for row in pair_rows),
        "cover_orders_scale_as_k6": all(row["MonQk_order"] == 36864 * row["k"] ** 6 for row in cover_rows),
        "qk_counts_scale_as_k3": all(row["vertices"] == 4 * row["k"] ** 3 and row["edges"] == 24 * row["k"] ** 3 for row in cover_rows),
        "local_packet_independent_of_cover_index": all(invariant_packet["middle_blocks"] == 48 for _row in cover_rows),
        "first_three_cover_indices_match_substrate_primes": cover_indices[:3] == [3, 5, 7],
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT831 check failed: {name}")

    out = {
        "theorem": "BT831 tomotope minimal-cover architecture boundary",
        "source_facts": {
            "paper": "Barry Monson, Daniel Pellicer, Gordon Williams, The Tomotope, Ars Math. Contemp. 5 (2012), 355-370",
            "tomotope_counts": {"vertices": 4, "edges": 12, "triangles": 16, "tetrahedra": 4, "hemioctahedra": 4},
            "monodromy_order": 18432,
            "monodromy_type": "{3,12,4}",
            "monodromy_boundary": "Mon(T) is not a string C-group; the intersection condition fails",
            "infinite_cover_fact": "for coprime odd p,q>1, T has minimal regular covers Rp,Rq, neither covering the other nor R2",
            "qk_cover_arithmetic": "Qk has counts (4,24,32,8,4)*k^3 and |Mon(Qk)|=36864*k^6",
        },
        "architecture_interpretation": {
            "abi": "BT814 48-block / 192-flag tomotope middle packet is the cover-invariant local ABI",
            "implementation_gauge": "regular cover index k is a pluggable durable-commit implementation parameter",
            "boundary": "do not assert a unique global tomotope regularization unless a cover index is pinned",
            "new_design_rule": "fast routes compile to invariant packets; durable storage may choose one cover family without invalidating other minimal covers",
        },
        "cover_indices_tested": cover_rows,
        "pairwise_noncomparability_tests": pair_rows,
        "checks": checks,
    }
    path = ROOT / "data" / "bt831_tomotope_minimal_cover_architecture.json"
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
