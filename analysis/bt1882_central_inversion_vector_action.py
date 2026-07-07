#!/usr/bin/env python3
"""BT1882: central-inversion vector action.

Applies the O(A2)/W(A2) central-inversion bookkeeping action to the BT1880
basis-level representatives. With the current BT982 vertex E8 basis, the phase-1
action is represented by simultaneous sign reversal of the two slot vectors. This
preserves all self/cross Gram contributions for the slot pair, while still
leaving explicit Z^40 chain-boundary compatibility open.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPED = ROOT / "data/PART_BT1880_BT982_TO_BT1875_MAPPED_TEMPLATE.json"
BT982 = ROOT / "data/bt982_explicit_integral_e8_basis.json"
OUT = ROOT / "data/PART_BT1882_CENTRAL_INVERSION_VECTOR_ACTION_results.json"


def dot_G(x, G, y):
    return sum(x[i] * G[i][j] * y[j] for i in range(len(x)) for j in range(len(y)))


def negate(v):
    return [-x for x in v]


def theorem_summary():
    rows = json.loads(MAPPED.read_text(encoding="utf-8"))["rows"]
    bt982 = json.loads(BT982.read_text(encoding="utf-8"))
    G = bt982["final_gram_Bt_G_vertex_B"]
    # Since BT982 final basis B has Gram E8 Cartan in its basis coordinates, use that
    # Gram for contribution checks on the mapped 8-coordinate representatives.
    row_results = []
    for r in rows:
        a = r["integral_E8_vector_a"]
        b = r["integral_E8_vector_b"]
        if r["phase_coset_bit"] == 0:
            aa, bb = a, b
        else:
            aa, bb = negate(a), negate(b)
        before = {
            "aa": dot_G(a, G, a),
            "bb": dot_G(b, G, b),
            "ab": dot_G(a, G, b),
        }
        after = {
            "aa": dot_G(aa, G, aa),
            "bb": dot_G(bb, G, bb),
            "ab": dot_G(aa, G, bb),
        }
        row_results.append({
            "selector_slot": r["selector_slot"],
            "support_pair": r["support_pair"],
            "phase_coset_bit": r["phase_coset_bit"],
            "action": "identity" if r["phase_coset_bit"] == 0 else "simultaneous_vector_negation",
            "gram_before": before,
            "gram_after": after,
            "gram_preserved": before == after,
        })
    checks = {
        "eight_rows_checked": len(row_results) == 8,
        "phase_zero_identity_rows_present": sum(1 for r in row_results if r["phase_coset_bit"] == 0) == 4,
        "phase_one_negation_rows_present": sum(1 for r in row_results if r["phase_coset_bit"] == 1) == 4,
        "all_slot_gram_contributions_preserved": all(r["gram_preserved"] for r in row_results),
        "chain_boundary_still_not_claimed": True,
    }
    return {
        "theorem": "BT1882 Central-Inversion Vector Action",
        "input": str(MAPPED.relative_to(ROOT)),
        "gram_source": "BT982 final_gram_Bt_G_vertex_B",
        "phase_one_action": "simultaneous sign reversal of both mapped slot vectors",
        "row_results": row_results,
        "closed_now": "basis-level Gram/metric contributions are preserved by the central-inversion bookkeeping action",
        "remaining_open": "explicit Z^40 chain-boundary compatibility for the phase action",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Vector-level Gram test in BT982 vertex E8 coordinates only; not a Z^40 chain-boundary proof."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
