#!/usr/bin/env python3
"""Metric/Pell/exceptional lift suggested by the parallel-agent commits.

Inputs from the current local pipeline:

    metric class parity vector: c=(55,13)
    Szilassi metric packet: 23
    Boolean per-chart vector: b=(64,8), sum=72
    signed phase image/kernel: 81/79

Inputs from the parallel-agent Pell/exceptional commits:

    Pell sums: 7,17,25,31
    nonautomatic sums: 7+17+31=55
    automatic sum: 25=f+1, automatic pair root Phi3=13
    exceptional dimensions:
        G2=14, F4=52, E6=78, E7=133, E8=248
    modular level/index:
        X0(36) index=72

New bridge:

    even metric classes = 55 = nonautomatic Pell-sum sector
    odd metric classes  = 13 = Phi3 = automatic Pell root
    G2 = 2*Phi6 = 14, and one toroidal chart flag count 42 = 3*G2
    F4 = dZ*Phi3 = 4*13 = odd_classes*dZ
    E6 = even_metric_classes + Szilassi_metric_packet = 55+23 = 78
    E7 = E6 + even_metric_classes = 78+55 = 133
    E8 = edge_carrier + tomotope_cells = 240+8 = 248

Spectrum bridge:

    648 = H1*8 = Hessian/qutrit local braid order
    72  = 64+8 = Boolean per-chart lift = X0(36) index = Pell product 8*9
    40  = v = multiplier ladder total

Thus the same metric parity vector c=(55,13) is the handoff object between
Pell ladders and the exceptional chain.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "w33_metric_pell_exceptional_lift.json"

q = 3
lam = 2
mu = 4
k = 12
f = 24
g = 15
v = 40
E = 240
phi3 = q * q + q + 1       # 13
phi4 = q * q + 1           # 10
phi6 = q * q - q + 1       # 7
H1 = q ** (q + 1)          # 81
dX, dZ = 3, 4
tomotope_cells = 1 + phi6 # 8
sz_metric_packet = 23
cs_metric_packet = 45
metric_even = 55
metric_odd = 13
metric_total = 68
chart_flags = 42
phase_kernel = 79
boolean_per_chart_even = 64
boolean_per_chart_odd = 8
middle_eigenvalue = 72
pell_sums = [7, 17, 25, 31]
pell_products = [12, 72, 156, 240]
nonautomatic_pell_sums = pell_sums[0] + pell_sums[1] + pell_sums[3]
automatic_pell_sum = pell_sums[2]

exceptional = {
    "G2": 14,
    "F4": 52,
    "E6": 78,
    "E7": 133,
    "E8": 248,
}


def build_payload() -> dict[str, Any]:
    spectrum = {
        "top": 648,
        "plus_branch": "144 + 36*sqrt(6)",
        "middle": 72,
        "minus_branch": "144 - 36*sqrt(6)",
        "protected": 40,
        "multiplicities": [1, 24, 30, 24, 81],
    }

    identities = {
        "even_metric_is_nonautomatic_pell_sum": metric_even == nonautomatic_pell_sums == 55,
        "odd_metric_is_phi3": metric_odd == phi3 == 13,
        "automatic_pell_sum": automatic_pell_sum == f + 1 == 25,
        "pell_sum_total": sum(pell_sums) == 2 * v == 80,
        "metric_plus_auto_sum": metric_even + automatic_pell_sum == 2 * v == 80,
        "metric_total": metric_even + metric_odd == metric_total == 68,
        "metric_difference_flags": metric_even - metric_odd == chart_flags == 42,
        "G2_flags": exceptional["G2"] == 2 * phi6 == 14 and chart_flags == q * exceptional["G2"],
        "F4_from_odd_metric": exceptional["F4"] == dZ * metric_odd == mu * phi3 == 52,
        "E6_from_metric_and_sz": exceptional["E6"] == metric_even + sz_metric_packet == 78,
        "E6_from_xscheme": exceptional["E6"] == f + 2 * g + f == 78,
        "E7_from_E6_even_metric": exceptional["E7"] == exceptional["E6"] + metric_even == 133,
        "E8_from_edge_tomotope": exceptional["E8"] == E + tomotope_cells == 248,
        "middle_is_boolean_index_pell": middle_eigenvalue == boolean_per_chart_even + boolean_per_chart_odd == pell_products[1] == 72,
        "top_is_hessian": spectrum["top"] == H1 * tomotope_cells == 648,
        "protected_is_v": spectrum["protected"] == v == 40,
        "kernel_plus_image": phase_kernel + H1 == mu * v == 160,
        "moonshine_gap": 4 * H1 == 324,
    }

    theorem = (
        "Metric-Pell Exceptional Lift Theorem.  The toroidal metric parity "
        "vector c=(55,13) is the handoff between the Pell ladder and the "
        "exceptional Lie chain.  Its even component 55 is the nonautomatic "
        "Pell-sum sector 7+17+31, while its odd component 13 is Phi3, the "
        "automatic Pell root.  From this vector, the exceptional dimensions "
        "lift as G2=2Phi6, F4=4*13, E6=55+23, E7=E6+55, and E8=240+8.  "
        "Simultaneously, the spectrum anchors are 648=81*8, 72=64+8="
        "index X0(36)=Pell product 8*9, and 40=v."
    )

    return {
        "summary": {
            "metric_parity_vector": [metric_even, metric_odd],
            "pell_sums": pell_sums,
            "nonautomatic_pell_sum": nonautomatic_pell_sums,
            "automatic_pell_sum": automatic_pell_sum,
            "exceptional_dimensions": exceptional,
            "all_identities_hold": all(identities.values()),
        },
        "metric_pell_handoff": {
            "metric_even": metric_even,
            "metric_odd": metric_odd,
            "closed_forms": {
                "metric_even": "55 = 7+17+31 = nonautomatic Pell sums",
                "metric_odd": "13 = Phi3 = automatic Pell root",
                "automatic_sum": "25 = f+1 = (12,13) Pell sum",
                "total_pell_sums": "7+17+25+31 = 80 = 2v",
                "metric_plus_auto": "55+25=80=2v",
                "metric_difference": "55-13=42 = one toroidal chart flag count",
            },
        },
        "exceptional_lift": {
            "G2": "14 = 2*Phi6; chart flags 42 = q*G2",
            "F4": "52 = dZ*Phi3 = 4*13 = odd_metric*dZ",
            "E6": "78 = even_metric + Szilassi_metric_packet = 55+23 = f+2g+f",
            "E7": "133 = E6 + even_metric = 78+55",
            "E8": "248 = edge_carrier + tomotope_cells = 240+8",
        },
        "spectrum_and_modular_bridge": {
            "target_spectrum": [
                "648^1",
                "(144 + 36*sqrt(6))^24",
                "72^30",
                "(144 - 36*sqrt(6))^24",
                "40^81",
            ],
            "top": "648 = H1*8 = Hessian/local qutrit braid order",
            "middle": "72 = 64+8 = Boolean per-chart lift = Pell product 8*9 = index X0(36)",
            "protected": "40 = v = multiplier ladder total",
            "image_kernel": "160 = 81 protected image + 79 metric kernel = mu*v",
            "moonshine": "324 = 4*H1 = dZ*H1",
        },
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": "This is an exact finite arithmetic bridge using repo-established Pell, metric, and exceptional ledgers. It is structural evidence, not by itself a derivation of empirical observables.",
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
