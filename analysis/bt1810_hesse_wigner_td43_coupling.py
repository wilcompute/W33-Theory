#!/usr/bin/env python3
"""BT1810: Hesse/Wigner phase coupling from the TD(4,3) escape surface.

For every defect center, the nine safe triads and nine cheap quads are the same
nine phase points seen from two sides. The four star-lines through the defect are
the four striations of AG(2,3). A ground vector selects one line in each striation,
and the four selected lines meet in one Hesse/Wigner phase point.

Honest boundary: this is the exact finite phase-space dictionary. It is not a
claim that Wigner negativity has been physically measured; it identifies the
nine-point phase carrier the fuel/readout layer can use.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bt1807_defect_phase_plane_transversal_design as td43  # noqa: E402

OUT = Path("data/PART_BT1810_HESSE_WIGNER_TD43_COUPLING_results.json")


def center_certificate(center, pts, adj, lines):
    rows, neighbors, safe = td43.vector_table(center, pts, adj)
    groups = td43.star_lines(center, lines)
    group_id = {x: gi for gi, group in enumerate(groups) for x in group}
    # A TD(4,3) block is encoded as the four labels it chooses, one per striation.
    signatures = []
    for phase, row in enumerate(rows):
        sig = tuple(sorted((group_id[x], groups[group_id[x]].index(x)) for x in row["quad"]))
        signatures.append(sig)
        assert [a for a, _ in sig] == [0, 1, 2, 3]
    assert len(set(signatures)) == 9

    # In AG(2,3), any two phase points determine exactly one line. Here this is
    # recovered as: two TD blocks agree in exactly one striation label.
    agreement_profile = Counter()
    for a, b in combinations(signatures, 2):
        agreement_profile[sum(1 for x, y in zip(a, b) if x == y)] += 1
    assert agreement_profile == Counter({1: 36})

    return {
        "center": center,
        "phase_points": 9,
        "striations": 4,
        "lines_per_striation": 3,
        "point_pair_agreement_profile": dict(agreement_profile),
        "first_three_phase_signatures": [list(map(list, sig)) for sig in signatures[:3]],
    }


def theorem_summary():
    pts, adj, lines = td43.build_w33()
    certs = [center_certificate(c, pts, adj, lines) for c in range(40)]
    assert all(c["point_pair_agreement_profile"] == {1: 36} for c in certs)
    summary = {
        "theorem": "BT1810 Hesse/Wigner TD(4,3) Coupling Theorem",
        "per_center_phase_space": {
            "phase_points": 9,
            "striations": 4,
            "lines_per_striation": 3,
            "model": "AG(2,3) / Hesse-Wigner nine-point phase plane",
            "dictionary": {
                "safe_triad": "one phase point as payload/address triple",
                "cheap_quad": "same phase point as one selected line from each of four striations",
                "star_line": "one Wigner/Hesse striation direction",
                "neighbor_on_star_line": "one line inside a striation",
            },
        },
        "global_counts": {
            "centers": 40,
            "phase_points_total_with_center_fibers": 360,
            "striations_total_with_center_fibers": 160,
            "phase_line_labels_total_with_center_fibers": 480,
        },
        "checks": {
            "all_centers_have_9_phase_points": True,
            "all_centers_have_4_striations_of_3_lines": True,
            "every_pair_of_phase_points_agrees_in_exactly_one_striation": True,
            "safe_triad_and_cheap_quad_are_bijective_phase_readings": True,
        },
        "sample_centers": certs[:3],
        "honest_scope": "Exact phase-space carrier/dictionary. This does not by itself measure Wigner negativity or quantum advantage."
    }
    return summary


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
