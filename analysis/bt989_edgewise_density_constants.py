#!/usr/bin/env python3
"""
BT989 — Edgewise density constants replacing the barycentric 120/19 layer.

BT987/BT988 show the old barycentric constants cannot be reused for R3.  This
script computes the exact constants that *are* currently justified from explicit
CP2_9/K3_16 facets plus the k=2 edgewise top multiplier:

  - top-dimensional growth multiplier: 16, not 120;
  - mesh scale: h_r = 2^-r;
  - explicit seed top counts f4*16^r;
  - normalized top-count density ratio K3/CP2 = 8, invariant by level.

Boundary: the old `120/19` and `860/19` were full barycentric chain/trace
density constants. The full edgewise analogs require the local 4-simplex
edgewise incidence template. BT989 retires the old constants and installs the
exact top-channel constants that are justified now.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

SEEDS = {
    "CP2_9": {"f_vector": [9, 36, 84, 90, 36], "chi": 3},
    "K3_16": {"f_vector": [16, 120, 560, 720, 288], "chi": 24},
}


def frac(n: int, d: int = 1) -> dict:
    q = Fraction(n, d)
    return {"exact": str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}", "float": float(q)}


def main() -> None:
    levels = range(7)
    seed_packets = {}
    for name, data in SEEDS.items():
        f0, f1, f2, f3, f4 = data["f_vector"]
        seed_packets[name] = {
            "f_vector": data["f_vector"],
            "chi": data["chi"],
            "edgewise_multiplier": 16,
            "barycentric_multiplier": 120,
            "top_counts_edgewise": [f4 * (16 ** r) for r in levels],
            "top_counts_barycentric": [f4 * (120 ** r) for r in levels],
            "mesh_scales": [frac(1, 2 ** r) for r in levels],
            "edgewise_level1_vertex_count": f0 + f1,
        }
    out = {
        "theorem": "BT989 exact edgewise top-density constants for CP2_9/K3_16",
        "retired_barycentric_constants": ["120/19", "860/19"],
        "retirement_reason": "BT983: barycentric tower is not shape-regular, so its density constants are not valid for the CMS/DP/FEEC R3 route.",
        "edgewise_constants_currently_justified": {
            "dimension": 4,
            "k": 2,
            "top_simplex_multiplier": 16,
            "mesh_width_scale_per_step": "1/2",
            "K3_to_CP2_top_count_ratio": frac(SEEDS["K3_16"]["f_vector"][4], SEEDS["CP2_9"]["f_vector"][4]),
            "K3_to_CP2_chi_ratio": frac(SEEDS["K3_16"]["chi"], SEEDS["CP2_9"]["chi"]),
        },
        "seeds": seed_packets,
        "open_lower_incidence_constants": "Full edgewise chain/trace density constants require the local 4-simplex edgewise facet template; this file refuses to fake them.",
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt989_edgewise_density_constants.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
