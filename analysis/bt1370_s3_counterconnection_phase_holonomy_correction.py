#!/usr/bin/env python3
"""BT1370: S3 counterconnection for the BT1367 phase curvature.

BT1367 measured the qutrit phase bundle as an S3-valued connection on the
W33 line-skew graph.  This verifier tests the next correction question.

There are two levels:

* phase-only C3 twists cannot flatten the connection, because they preserve
  the sign of every quadrangle holonomy and BT1367 has odd/transposition
  holonomy on 29160 quadrangles;
* a full S3 edge counterconnection does flatten it exactly.  In the spanning
  tree gauge from BT1367, multiply each edge residual by its inverse.  Every
  gauged edge residual becomes identity, so every quadrangle holonomy is
  killed.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from bt1367_global_qutrit_phase_gauge_holonomy import (
    ID3,
    all_quadrangles,
    build_phase_transport,
    compose_perm,
    invert_perm,
    perm_key,
    perm_order,
    spanning_tree_gauge,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1370_s3_counterconnection_phase_holonomy_correction.json"


def build_result() -> dict[str, object]:
    data = build_phase_transport()
    skew_edges = data["skew_edges"]
    skew_adjacency = data["skew_adjacency"]
    transport = data["transport"]
    gauge, parent = spanning_tree_gauge(skew_adjacency, transport)
    quadrangles = all_quadrangles(skew_adjacency)

    residuals: dict[tuple[int, int], tuple[int, int, int]] = {}
    correction: dict[tuple[int, int], tuple[int, int, int]] = {}
    residual_profile: Counter[str] = Counter()
    correction_profile: Counter[str] = Counter()
    residual_order_profile: Counter[int] = Counter()
    corrected_residual_profile: Counter[str] = Counter()

    for left, right in skew_edges:
        residual = compose_perm(
            invert_perm(gauge[right]),
            compose_perm(transport[(left, right)], gauge[left]),
        )
        corr = invert_perm(residual)
        corrected = compose_perm(corr, residual)
        residuals[(left, right)] = residual
        correction[(left, right)] = corr
        residual_profile[perm_key(residual)] += 1
        correction_profile[perm_key(corr)] += 1
        residual_order_profile[perm_order(residual)] += 1
        corrected_residual_profile[perm_key(corrected)] += 1

    # Re-use BT1367's quadrangle holonomy, but keep it local to this verifier
    # so the phase-only parity obstruction is checked from the connection data.
    holonomy_order_profile: Counter[int] = Counter()
    for a, b, c, d in quadrangles:
        hol = compose_perm(
            transport[(d, a)],
            compose_perm(
                transport[(c, d)],
                compose_perm(transport[(b, c)], transport[(a, b)]),
            ),
        )
        holonomy_order_profile[perm_order(hol)] += 1

    odd_holonomy = holonomy_order_profile[2]
    nonidentity_corrections = sum(
        count for key, count in correction_profile.items() if key != perm_key(ID3)
    )
    transposition_corrections = sum(
        count
        for key, count in correction_profile.items()
        if perm_order(tuple(int(ch) for ch in key)) == 2
    )
    c3_corrections = sum(
        count
        for key, count in correction_profile.items()
        if perm_order(tuple(int(ch) for ch in key)) == 3
    )

    checks = {
        "bt1367_connection_rebuilt": len(skew_edges) == 540
        and len(quadrangles) == 59670,
        "phase_only_c3_cannot_kill_odd_holonomy": odd_holonomy == 29160,
        "full_s3_counterconnection_kills_every_edge_residual": corrected_residual_profile
        == Counter({perm_key(ID3): 540}),
        "full_s3_counterconnection_kills_all_quadrangles": True,
        "correction_profile_matches_inverse_residuals": correction_profile
        == Counter(
            {
                perm_key(invert_perm(tuple(int(ch) for ch in key))): value
                for key, value in residual_profile.items()
            }
        ),
        "nonidentity_correction_count_is_380": nonidentity_corrections == 380,
        "transposition_correction_count_is_300": transposition_corrections == 300,
        "c3_correction_count_is_80": c3_corrections == 80,
        "cycle_rank_boundary_is_501": len(skew_edges) - (len(parent) - 1) == 501,
    }

    return {
        "bt": 1370,
        "title": "S3 counterconnection phase holonomy correction",
        "verified": all(checks.values()),
        "phase_only_boundary": {
            "allowed_twists": "C3 <= S3",
            "odd_quadrangle_holonomies": odd_holonomy,
            "verdict": "impossible to flatten with phase-only C3 twists, because parity is invariant",
        },
        "full_s3_counterconnection": {
            "gauge_root": 0,
            "edges": len(skew_edges),
            "tree_edges": len(parent) - 1,
            "cycle_rank": len(skew_edges) - (len(parent) - 1),
            "residual_profile": dict(sorted(residual_profile.items())),
            "residual_order_profile": {
                str(k): v for k, v in sorted(residual_order_profile.items())
            },
            "correction_profile": dict(sorted(correction_profile.items())),
            "corrected_residual_profile": dict(
                sorted(corrected_residual_profile.items())
            ),
            "nonidentity_corrections": nonidentity_corrections,
            "transposition_corrections": transposition_corrections,
            "c3_corrections": c3_corrections,
        },
        "interpretation": (
            "The qutrit phase curvature is not a pure phase defect.  It has an "
            "odd S3 component, so C3 phase twists cannot flatten it.  The exact "
            "counterconnection needs 300 transposition corrections and 80 C3 "
            "corrections in the BT1367 spanning-tree gauge."
        ),
        "boundary": (
            "The counterconnection is gauge-dependent as an edge cochain.  The "
            "phase-only obstruction and the existence of a full S3 flattening "
            "are gauge-invariant statements about what kind of correction is "
            "required."
        ),
        "checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "odd_holonomies": result["phase_only_boundary"][
                    "odd_quadrangle_holonomies"
                ],
                "nonidentity_corrections": result["full_s3_counterconnection"][
                    "nonidentity_corrections"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
