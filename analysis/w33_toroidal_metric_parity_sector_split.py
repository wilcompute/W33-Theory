#!/usr/bin/env python3
"""Parity-sector split of the toroidal metric edge multiplicity packet.

The parity-Taylor layer gave the metric multiplicity histogram

    c_1,c_2,c_3,c_4,c_5,c_6 = 12,48,0,4,1,3.

This script splits that histogram into odd and even multiplicity sectors.
The exact result is surprisingly rigid:

    odd metric classes  = c1+c3+c5 = 13 = Phi_3,
    even metric classes = c2+c4+c6 = 55 = 5*11,
    even - odd          = 42 = one toroidal chart flag count.

For the Boolean lift sum c_m 2^m, the split is

    odd  Boolean lift = 56  = 7*8,
    even Boolean lift = 448 = 7*64,
    total             = 504 = 7*(8+64) = 7*72.

Thus the middle eigenvalue 72 decomposes per realization as

    72 = 8 + 64 = 8*(1+8),

where 8=1+Phi_6 is the tetrahedron/tomotope cell packet.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "w33_toroidal_metric_parity_sector_split.json"

Q = 3
PHI3 = Q * Q + Q + 1       # 13
PHI4 = Q * Q + 1           # 10
PHI6 = Q * Q - Q + 1       # 7
IHARA = 11
TOROIDAL_EDGE_COUNT = 21
CHART_FLAG_COUNT = 42
MIDDLE_EIGENVALUE = 72
TOMOTOPE_CELLS = 1 + PHI6  # 8
DZ = Q + 1                 # 4

# c_m: number of metric edge classes of multiplicity m.
C = {1: 12, 2: 48, 3: 0, 4: 4, 5: 1, 6: 3}


def sector_values(parity: int) -> dict[str, int]:
    ms = [m for m in C if m % 2 == parity]
    classes = sum(C[m] for m in ms)
    instances = sum(m * C[m] for m in ms)
    kernel = sum((m - 1) * C[m] for m in ms)
    boolean = sum((2 ** m) * C[m] for m in ms)
    raw2 = sum((m ** 2) * C[m] for m in ms)
    return {
        "multiplicities": ms,
        "metric_classes": classes,
        "edge_instances": instances,
        "kernel_excess": kernel,
        "boolean_lift": boolean,
        "raw_second_moment": raw2,
    }


def build_payload() -> dict[str, Any]:
    odd = sector_values(1)
    even = sector_values(0)
    total = {
        key: odd[key] + even[key]
        for key in ["metric_classes", "edge_instances", "kernel_excess", "boolean_lift", "raw_second_moment"]
    }

    identities = {
        "odd_classes_phi3": odd["metric_classes"] == PHI3 == 13,
        "even_classes_5_ihara": even["metric_classes"] == 5 * IHARA == 55,
        "even_minus_odd_flags": even["metric_classes"] - odd["metric_classes"] == CHART_FLAG_COUNT == 42,
        "total_classes": total["metric_classes"] == 68,
        "odd_instances_prime17": odd["edge_instances"] == 17,
        "even_instances_phi4_phi3": even["edge_instances"] == PHI4 * PHI3 == 130,
        "total_instances": total["edge_instances"] == PHI6 * TOROIDAL_EDGE_COUNT == 147,
        "odd_kernel_dz": odd["kernel_excess"] == DZ == 4,
        "even_kernel_75": even["kernel_excess"] == 75,
        "total_kernel_79": total["kernel_excess"] == 79,
        "odd_boolean_7_8": odd["boolean_lift"] == PHI6 * TOMOTOPE_CELLS == 56,
        "even_boolean_7_64": even["boolean_lift"] == PHI6 * TOMOTOPE_CELLS * TOMOTOPE_CELLS == 448,
        "total_boolean_7_72": total["boolean_lift"] == PHI6 * MIDDLE_EIGENVALUE == 504,
        "middle_eigenvalue_split": MIDDLE_EIGENVALUE == TOMOTOPE_CELLS + TOMOTOPE_CELLS * TOMOTOPE_CELLS,
        "raw_second_split": total["raw_second_moment"] == 401 and odd["raw_second_moment"] == 37 and even["raw_second_moment"] == 28 * PHI3 == 364,
    }

    theorem = (
        "Toroidal Metric Parity-Sector Theorem.  The parity-Taylor histogram "
        "c_m=(12,48,0,4,1,3) splits into odd and even metric sectors with "
        "odd class count 13=Phi_3 and even class count 55=5*11.  Their "
        "difference is 42, exactly one toroidal chart flag count.  The Boolean "
        "lift splits as 56+448=7*8+7*64=7*(8+64), so the middle eigenvalue "
        "72 decomposes per realization as 8+64.  Odd edge instances give 17, "
        "while even edge instances give 130=Phi_4*Phi_3.  The odd kernel "
        "excess is 4=d_Z, leaving 75 in the even sector for the full kernel 79."
    )

    return {
        "summary": {
            "odd_metric_classes": odd["metric_classes"],
            "even_metric_classes": even["metric_classes"],
            "even_minus_odd": even["metric_classes"] - odd["metric_classes"],
            "odd_boolean_lift": odd["boolean_lift"],
            "even_boolean_lift": even["boolean_lift"],
            "middle_eigenvalue_split_per_realization": "72 = 8 + 64",
            "all_identities_hold": all(identities.values()),
        },
        "histogram": {str(k): v for k, v in C.items()},
        "odd_sector": odd,
        "even_sector": even,
        "total": total,
        "closed_forms": {
            "odd_classes": "13 = Phi3",
            "even_classes": "55 = 5*11 = Csaszar_count * Ihara prime",
            "even_minus_odd": "42 = one toroidal chart flag count = v+e+f = 2e",
            "odd_instances": "17",
            "even_instances": "130 = Phi4*Phi3 = 10*13",
            "odd_kernel": "4 = d_Z = q+1",
            "even_kernel": "75 = 3*25",
            "odd_boolean": "56 = 7*8",
            "even_boolean": "448 = 7*64",
            "middle_eigenvalue": "72 = 8 + 64 = tomotope_cells + tomotope_cells^2",
            "raw_second": "401 = 37 + 364 = 37 + 28*Phi3",
        },
        "spectrum_bridge": {
            "target_middle_eigenvalue": MIDDLE_EIGENVALUE,
            "per_realization_split": {
                "odd": TOMOTOPE_CELLS,
                "even": TOMOTOPE_CELLS * TOMOTOPE_CELLS,
                "sum": MIDDLE_EIGENVALUE,
            },
            "target_spectrum": [
                "648^1",
                "(144 + 36*sqrt(6))^24",
                "72^30",
                "(144 - 36*sqrt(6))^24",
                "40^81",
            ],
        },
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": "This is an exact finite parity-sector identity for the toroidal metric edge packet. It does not by itself infer physical dynamics or empirical observables.",
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
