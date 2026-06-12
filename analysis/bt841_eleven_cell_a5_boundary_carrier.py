#!/usr/bin/env python3
"""
BT841 - Local 660 carrier: eleven labels times the Clifford A5 torsor.

BT836/BT839 record the 11-cell flag count

    660 = |PSL(2,11)| = 11*A5 = k*N_eff.

This verifier builds an explicit 660-slot boundary carrier from the verified
Clifford L/R selector.  The 36 L/R cells form a 6 x 6 grid with 12 row/column
fibers.  At any chosen apex cell (r,c), the two incident fibers are the local
row/column frame; the remaining ten fibers plus the apex give

    11 = 1 + 5 + 5.

Crossing these eleven labels with the 60-element A5 degree-six selector gives
660 slots.  This is a carrier theorem, not a PSL(2,11) action theorem.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_clifford_antipodal_a5_selector_group import (  # noqa: E402
    clifford_antipodal_permutations,
    parity,
    permutation_order,
)


def boundary_labels_for_apex(row: int, col: int) -> list[dict[str, Any]]:
    labels: list[dict[str, Any]] = [{"kind": "apex_cell", "label": f"C{row}{col}", "address": [row, col]}]
    for other_row in range(6):
        if other_row != row:
            labels.append({"kind": "nonincident_L_fiber", "label": f"L{other_row}"})
    for other_col in range(6):
        if other_col != col:
            labels.append({"kind": "nonincident_R_fiber", "label": f"R{other_col}"})
    return labels


def main() -> None:
    k = 12
    n_eff = 55
    a5_map = clifford_antipodal_permutations()
    a5_perms = sorted(set(a5_map.values()))
    order_profile = Counter(permutation_order(perm) for perm in a5_perms)
    parity_profile = Counter(parity(perm) for perm in a5_perms)

    carriers = []
    label_kind_profiles = Counter()
    label_usage = Counter()
    for row in range(6):
        for col in range(6):
            labels = boundary_labels_for_apex(row, col)
            kind_profile = Counter(label["kind"] for label in labels)
            label_kind_profiles[tuple(sorted(kind_profile.items()))] += 1
            for label in labels:
                label_usage[label["label"]] += 1
            carriers.append(
                {
                    "apex": [row, col],
                    "label_count": len(labels),
                    "label_kind_profile": dict(sorted(kind_profile.items())),
                    "flag_count": len(labels) * len(a5_perms),
                    "sample_labels": labels[:6],
                }
            )

    fiber_usage = Counter(
        count for label, count in label_usage.items()
        if label.startswith(("L", "R"))
    )
    apex_usage = Counter(
        count for label, count in label_usage.items()
        if label.startswith("C")
    )

    checks = {
        "a5_selector_has_60_elements": len(a5_perms) == 60,
        "a5_order_profile": order_profile == {1: 1, 2: 15, 3: 20, 5: 24},
        "a5_all_even": parity_profile == {0: 60},
        "there_are_36_apex_carriers": len(carriers) == 36,
        "each_carrier_has_eleven_labels": Counter(row["label_count"] for row in carriers) == {11: 36},
        "eleven_decomposes_as_1_plus_5_plus_5": label_kind_profiles
        == {
            (
                ("apex_cell", 1),
                ("nonincident_L_fiber", 5),
                ("nonincident_R_fiber", 5),
            ): 36
        },
        "each_carrier_has_660_flags": Counter(row["flag_count"] for row in carriers) == {660: 36},
        "fiber_labels_each_appear_in_30_carriers": fiber_usage == {30: 12},
        "apex_cells_each_appear_once": apex_usage == {1: 36},
        "flag_count_is_11_times_A5": 11 * len(a5_perms) == 660,
        "flag_count_is_k_times_Neff": k * n_eff == 660,
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT841 check failed: {name}")

    out = {
        "theorem": "BT841 eleven-cell A5 boundary carrier",
        "a5_selector": {
            "source": "Clifford antipodal A5 degree-six selector",
            "element_count": len(a5_perms),
            "order_profile": dict(sorted(order_profile.items())),
            "parity_profile": dict(sorted(parity_profile.items())),
            "sample_permutations": [list(perm) for perm in a5_perms[:12]],
        },
        "eleven_label_carriers": {
            "carrier_count": len(carriers),
            "carrier_rule": "apex cell + five nonincident L fibers + five nonincident R fibers",
            "flag_count_per_carrier": 660,
            "factorizations": {
                "11_times_A5": 11 * len(a5_perms),
                "k_times_Neff": k * n_eff,
                "Neff": n_eff,
            },
            "sample_carriers": carriers[:6],
            "fiber_usage_profile": dict(sorted(fiber_usage.items())),
            "apex_usage_profile": dict(sorted(apex_usage.items())),
        },
        "claim_boundary": (
            "This is an explicit 660-slot carrier at the Clifford/schedule boundary; "
            "it does not claim a PSL(2,11) action or identify the full 11-cell automorphism group inside W33."
        ),
        "checks": checks,
    }
    path = ROOT / "data" / "bt841_eleven_cell_a5_boundary_carrier.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
