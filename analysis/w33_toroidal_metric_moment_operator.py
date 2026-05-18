#!/usr/bin/env python3
"""Metric moment / binomial-lift operator for seven toroidal realizations.

This goes one level deeper than the VEF edge-phase kernel:

    edge instances - metric edge classes = 147 - 68 = 79 = phase-frame kernel.

Now treat every metric edge class of multiplicity m as an internal Boolean
collision packet.  Its binomial lift contributes C(m,k) at order k and
2^m over all orders.  Across the seven realizations the binomial moments are:

    B_k = sum_classes C(m,k), k=0..6
        = 68,147,127,86,54,19,3.

Key consequences:

    B_0 = metric edge classes = 68
    B_1 = actual edge instances = 147
    B_1 - B_0 = 79 = signed phase-frame kernel
    B_2 = 127 = 2^7 - 1  (full nonempty heptad subset count)
    sum_k B_k = 504 = 7*72 = 21*24

Therefore the average Boolean edge-class lift per realization is exactly 72,
the middle eigenvalue in the minimal-logical X-association spectrum:

    648^1, (144±36√6)^24, 72^30, 40^81.

Second raw moment also locks to the CSS/TQC counts:

    sum m^2 = 401 = 320 + 81 = |X_min vectors| + H1.
    Csaszar part = 321 = 320 + 1.
    Szilassi part = 80 = 81 - 1.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "w33_toroidal_metric_moment_operator.json"

Q = 3
PHI6 = Q * Q - Q + 1
H1 = Q ** (Q + 1)
X_UNIQUE_VECTORS = 320
MIDDLE_EIGENVALUE = 72
W33_F = 24
EDGE_INSTANCES_PER_CHART = 21

REALIZATIONS: list[dict[str, Any]] = [
    {"label": "C1", "family": "Csaszar", "edge_multiplicities": [2, 1, 2, 4, 2, 2, 2, 2, 2, 2]},
    {"label": "C2", "family": "Csaszar", "edge_multiplicities": [1, 4, 2, 1, 6, 2, 2, 2, 1]},
    {"label": "C3", "family": "Csaszar", "edge_multiplicities": [2, 1, 2, 2, 4, 2, 5, 2, 1]},
    {"label": "C4", "family": "Csaszar", "edge_multiplicities": [2, 1, 4, 2, 2, 2, 2, 6]},
    {"label": "C5", "family": "Csaszar", "edge_multiplicities": [2, 1, 2, 2, 2, 2, 2, 2, 6]},
    {"label": "S1", "family": "Szilassi", "edge_multiplicities": [2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 1]},
    {"label": "S2", "family": "Szilassi", "edge_multiplicities": [2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2]},
]


def binomial_moments(multiplicities: list[int]) -> dict[int, int]:
    max_m = max(multiplicities)
    return {k: sum(math.comb(m, k) for m in multiplicities) for k in range(max_m + 1)}


def raw_moments(multiplicities: list[int], max_power: int = 4) -> dict[int, int]:
    return {p: sum(m ** p for m in multiplicities) for p in range(max_power + 1)}


def enrich_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in REALIZATIONS:
        ms = list(row["edge_multiplicities"])
        enriched = dict(row)
        enriched.update(
            {
                "edge_type_count": len(ms),
                "edge_instance_count": sum(ms),
                "degeneracy_excess": sum(m - 1 for m in ms),
                "collision_pairs": sum(math.comb(m, 2) for m in ms),
                "boolean_lift_total": sum(2 ** m for m in ms),
                "raw_moment_2": sum(m * m for m in ms),
                "binomial_moments": binomial_moments(ms),
            }
        )
        rows.append(enriched)
    return rows


def select(rows: list[dict[str, Any]], family: str) -> list[int]:
    return [m for row in rows if row["family"] == family for m in row["edge_multiplicities"]]


def build_payload() -> dict[str, Any]:
    rows = enrich_rows()
    all_m = [m for row in rows for m in row["edge_multiplicities"]]
    cs_m = select(rows, "Csaszar")
    sz_m = select(rows, "Szilassi")

    hist = dict(sorted(Counter(all_m).items()))
    B = binomial_moments(all_m)
    B_cs = binomial_moments(cs_m)
    B_sz = binomial_moments(sz_m)
    R = raw_moments(all_m)
    R_cs = raw_moments(cs_m)
    R_sz = raw_moments(sz_m)

    boolean_total = sum(B.values())
    boolean_cs = sum(B_cs.values())
    boolean_sz = sum(B_sz.values())
    metric_classes = B[0]
    edge_instances = B[1]
    kernel = edge_instances - metric_classes

    identities = {
        "histogram": hist == {1: 12, 2: 48, 4: 4, 5: 1, 6: 3},
        "B_sequence": [B[k] for k in range(7)] == [68, 147, 127, 86, 54, 19, 3],
        "B0_classes": B[0] == 68,
        "B1_instances": B[1] == 147,
        "kernel_79": kernel == 79,
        "B2_mersenne_heptad": B[2] == 127 == 2 ** PHI6 - 1,
        "boolean_total_504": boolean_total == PHI6 * MIDDLE_EIGENVALUE == EDGE_INSTANCES_PER_CHART * W33_F == 504,
        "boolean_average_72": boolean_total // PHI6 == MIDDLE_EIGENVALUE,
        "boolean_cs_420": boolean_cs == 5 * 84 == 420,
        "boolean_sz_84": boolean_sz == 84,
        "raw_second_total": R[2] == X_UNIQUE_VECTORS + H1 == 401,
        "raw_second_cs": R_cs[2] == X_UNIQUE_VECTORS + 1 == 321,
        "raw_second_sz": R_sz[2] == H1 - 1 == 80,
        "cs_collision_pairs": B_cs[2] == 4 * (Q ** Q) == 108,
        "sz_collision_pairs": B_sz[2] == 19,
        "higher_collisions_cs_only": all(B_sz.get(k, 0) == 0 for k in range(3, 7)),
        "B5_19_B6_3": B[5] == 19 and B[6] == 3,
    }

    theorem = (
        "Toroidal Metric Moment Operator Theorem.  The seven-realization "
        "edge-class multiplicity operator has binomial moments "
        "B_k=sum C(m,k) = 68,147,127,86,54,19,3.  Its first difference "
        "B_1-B_0=79 is the signed phase-frame kernel.  Its second binomial "
        "moment B_2=127=2^7-1 is the full nonempty heptad subset count.  "
        "The total Boolean lift sum_k B_k is 504=7*72=21*24, so the average "
        "Boolean lift per toroidal realization is exactly the middle eigenvalue "
        "72 of the minimal-logical X-association spectrum.  The raw second "
        "moment is 401=320+81, splitting the minimal X-vector count from H1."
    )

    return {
        "summary": {
            "multiplicity_histogram": hist,
            "binomial_moments_B0_to_B6": [B[k] for k in range(7)],
            "metric_classes_B0": metric_classes,
            "edge_instances_B1": edge_instances,
            "kernel_B1_minus_B0": kernel,
            "collision_pairs_B2": B[2],
            "boolean_lift_total": boolean_total,
            "boolean_lift_average_per_realization": boolean_total // PHI6,
            "raw_second_moment": R[2],
            "all_identities_hold": all(identities.values()),
        },
        "per_realization_rows": rows,
        "binomial_moment_operator": {
            "B_all": {str(k): v for k, v in B.items()},
            "B_csaszar": {str(k): v for k, v in B_cs.items()},
            "B_szilassi": {str(k): v for k, v in B_sz.items()},
            "closed_forms": {
                "B0": "68 metric edge classes",
                "B1": "147 actual edge instances",
                "B1_minus_B0": "79 = phase-frame kernel dimension",
                "B2": "127 = 2^7 - 1 = nonempty subsets of the toroidal heptad",
                "sum_Bk": "504 = 7*72 = 21*24",
                "average_Boolean_lift": "72 = middle eigenvalue of U U^T spectrum",
                "Cs_Boolean_lift": "420 = 5*84",
                "Sz_Boolean_lift": "84",
            },
        },
        "raw_moment_operator": {
            "R_all": {str(k): v for k, v in R.items()},
            "R_csaszar": {str(k): v for k, v in R_cs.items()},
            "R_szilassi": {str(k): v for k, v in R_sz.items()},
            "closed_forms": {
                "R2_total": "401 = 320 + 81 = |X_min unique F3 vectors| + H1",
                "R2_csaszar": "321 = 320 + 1",
                "R2_szilassi": "80 = 81 - 1",
                "B2_csaszar": "108 = 4*27 = 4*q^q",
                "B2_szilassi": "19",
                "higher_collisions": "All k>=3 binomial collisions live in the Csaszar packet; Szilassi has only multiplicities 1 and 2.",
            },
        },
        "spectrum_bridge": {
            "target_spectrum": [
                "648^1",
                "(144 + 36*sqrt(6))^24",
                "72^30",
                "(144 - 36*sqrt(6))^24",
                "40^81",
            ],
            "middle_eigenvalue_bridge": "sum_k B_k / 7 = 72",
            "phase_kernel_bridge": "B1-B0 = 79 = zero multiplicity 0^79 in spec(A A^T)",
            "raw_second_moment_bridge": "R2 = 401 = 320 + 81",
        },
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": "This is an exact finite metric-moment identity. It gives an operator interpretation of the edge multiplicity spectrum, but does not by itself prove physical dynamics or empirical observables.",
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
