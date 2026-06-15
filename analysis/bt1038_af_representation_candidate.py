#!/usr/bin/env python3
"""BT1038: explicit A_F representation candidate on the 162 W33 fermion carrier.

Carrier model:
  H_ferm = C^2_chiral x C^3_generation x C^3_fiber x C^3_weakslot x C^3_color
         = 2*3*3*3*3 = 162.

The weakslot C^3 is decomposed as 1 singlet + 2 weak doublet.  The candidate
finite algebra A_F = C + H + M3(C) acts as:
  C        on the weak singlet/unimodular U(1) direction,
  H        on the weak doublet via the Pauli/quaternion representation,
  M3(C)    on the color slot.

This is a candidate representation, not yet the full Connes proof.  It locks the
matrix dimensions and the 1+3+8 Lie-algebra profile to be tested by BT1039.
"""
from __future__ import annotations

import json
from pathlib import Path

DIMS = {
    "chiral": 2,
    "generation": 3,
    "fiber": 3,
    "weakslot_singlet_plus_doublet": 3,
    "color": 3,
}

PROFILE = {
    "u1_singlet": 1,
    "su2_weak": 3,
    "su3_color": 8,
}


def main() -> None:
    dim = 1
    for value in DIMS.values():
        dim *= value
    out = {
        "theorem": "BT1038 A_F representation candidate on W33 fermion carrier",
        "algebra": "A_F = C + H + M3(C)",
        "carrier_factorization": DIMS,
        "carrier_dimension": dim,
        "target_carrier_dimension": 162,
        "dimension_hit": dim == 162,
        "weakslot_decomposition": "C^3 = C_singlet + C^2_weak_doublet",
        "representation_blocks": {
            "C": "acts on singlet / unimodular U(1) direction",
            "H": "acts on weak doublet through Pauli quaternion matrices",
            "M3C": "acts on color C^3"
        },
        "lie_algebra_profile": PROFILE,
        "lie_algebra_total": sum(PROFILE.values()),
        "expected_gauge_profile": [1, 3, 8],
        "status": "explicit block representation candidate; first-order and inner-one-form tests remain BT1039 targets"
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1038_af_representation_candidate.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
