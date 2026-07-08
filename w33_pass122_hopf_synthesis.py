#!/usr/bin/env python3
"""Pass 103: finite projective/Hopf comparison with explicit claim boundaries."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "w33_pass122_hopf_synthesis.json"


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def main() -> int:
    p98 = load("w33_pass117_o8_e6_embedding.json")
    p101 = load("w33_pass120_srg120_anisotropic.json")
    projective_vectors = 3**4 - 1
    projective_points = projective_vectors // (3 - 1)
    checks = {
        "finite_projective_bundle_80_to_40": projective_vectors == 80
        and projective_points == 40,
        "projective_scalar_fiber_C2": projective_vectors // projective_points == 2,
        "selector_phase_count_40_times_3": 40 * 3 == 120,
        "signed_phase_count_40_times_3_times_2": 40 * 3 * 2 == 240,
        "e8_root_pairs_120": p101["parameters"][0] == 120,
        "e8_branching_object_level": p98["weyl_e6_orbits_on_anisotropic"]
        == [1, 1, 1, 27, 27, 27, 36],
    }
    payload = {
        "schema": "w33.pass103.hopf_synthesis.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "exact_finite_projectivization": {
            "total_nonzero_vectors": 80,
            "fiber": "F3^x ~= C2",
            "base": "PG(3,3), 40 points",
            "formula": "(3^4-1)/(3-1)=40",
        },
        "distinct_phase_bundle": {
            "selector_sheets": "40 W33 lines * 3 qutrit phases = 120",
            "signed_lift_count": "40 * 3 * 2 = 240",
            "warning": (
                "The C2 projective-scalar fiber and C3 qutrit-phase fiber are "
                "different structures. Equality with the E8-root set requires "
                "an equivariant bijection, not just the common count 240."
            ),
        },
        "proved_exceptional_branching": (
            "On E8 roots modulo sign, W(E6) orbits are " "3 fixed + 27+27+27 + 36."
        ),
        "paper_boundary": (
            "BU(1)=CPinfinity and the complex Hopf universal bundle are standard. "
            "They do not by themselves force Standard Model factors, torsion, "
            "3+1 Einstein equations, masses, or coupling constants."
        ),
        "checks": checks,
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
