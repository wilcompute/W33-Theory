#!/usr/bin/env python3
"""de Branges-adjacent kernel audit for the Casey reflection cocycle.

Two distinct positivity mechanisms must not be conflated.

1. The repaired Casey defect is exactly a Cauchy/Hardy reproducing-kernel
   distance between two Laplace kernels.  Its Gram determinant and difference
   norm are positive and vanish only when delta=0.

2. For every delta, including off-line delta != 0, the polynomial

       E_{delta,gamma}(z) = (z+i gamma)^2-delta^2

   is Hermite--Biehler when gamma>0: its zeros are in the lower half-plane and
   |E(z)|>|E#(z)| in the upper half-plane.  Therefore the mere existence of a
   de Branges space or an adaptable Hermite--Biehler function does NOT force
   the critical line.  A successful RH program must identify one fixed E tied
   to xi and prove its kernel positivity globally; it cannot choose a new E for
   each reflected quartet.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def hardy_kernel(c: float, d: float) -> float:
    """L2(0,infinity) Gram kernel for x -> exp(-c x)."""
    if c <= 0 or d <= 0:
        raise ValueError("kernel parameters must be positive")
    return 1 / (c + d)


def cocycle_gram(a: float, delta: float) -> tuple[tuple[float, float], ...]:
    if a <= abs(delta):
        raise ValueError("require a>|delta|")
    c_minus = a - delta
    c_plus = a + delta
    return (
        (hardy_kernel(c_minus, c_minus), hardy_kernel(c_minus, c_plus)),
        (hardy_kernel(c_plus, c_minus), hardy_kernel(c_plus, c_plus)),
    )


def determinant_2x2(matrix: tuple[tuple[float, float], ...]) -> float:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def kernel_defect_energy(a: float, delta: float) -> float:
    g = cocycle_gram(a, delta)
    return math.pi * (g[0][0] + g[1][1] - 2 * g[0][1])


def closed_defect_energy(a: float, delta: float) -> float:
    if a <= abs(delta):
        raise ValueError("require a>|delta|")
    return math.pi * delta**2 / (a * (a * a - delta * delta))


def hb_polynomial(z: complex, delta: float, gamma: float) -> complex:
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    return (z + 1j * gamma) ** 2 - delta**2


def hb_sharp(z: complex, delta: float, gamma: float) -> complex:
    """E#(z)=conj(E(conj(z)))."""
    return (z - 1j * gamma) ** 2 - delta**2


def hb_gap_closed(x: float, y: float, delta: float, gamma: float) -> float:
    """Exact |E|^2-|E#|^2 in the upper half-plane."""
    return 8 * gamma * y * (delta**2 + gamma**2 + x**2 + y**2)


def hb_real_parts(delta: float, gamma: float) -> dict[str, list[float]]:
    """Zeros of A and B for E=A+iB."""
    root = math.sqrt(gamma**2 + delta**2)
    return {"A_zeros": [-root, root], "B_zeros": [0.0]}


def interlace(data: dict[str, list[float]]) -> bool:
    a0, a1 = data["A_zeros"]
    b0 = data["B_zeros"][0]
    return a0 < b0 < a1


def build_certificate() -> dict[str, Any]:
    a = 0.5
    deltas = (0.0, 0.05, 0.2, -0.2)
    gamma = 14.0
    gram_cases = []
    hb_cases = []
    for delta in deltas:
        gram = cocycle_gram(a, delta)
        det = determinant_2x2(gram)
        kernel_energy = kernel_defect_energy(a, delta)
        closed_energy = closed_defect_energy(a, delta)
        gram_cases.append({"delta": delta, "gram": gram, "determinant": det, "kernel_energy": kernel_energy, "closed_energy": closed_energy})
        points = (0.2 + 0.1j, -1.3 + 0.7j, 2.0 + 3.0j)
        gaps = []
        gap_errors = []
        for z in points:
            direct = abs(hb_polynomial(z, delta, gamma)) ** 2 - abs(hb_sharp(z, delta, gamma)) ** 2
            closed = hb_gap_closed(z.real, z.imag, delta, gamma)
            gaps.append(direct)
            gap_errors.append(abs(direct - closed))
        parts = hb_real_parts(delta, gamma)
        hb_cases.append({
            "delta": delta,
            "zeros_E": [{"real": delta, "imag": -gamma}, {"real": -delta, "imag": -gamma}],
            "upper_half_plane_gaps": gaps,
            "max_gap_formula_error": max(gap_errors),
            "A_B_zeros": parts,
            "interlace": interlace(parts),
            "hermite_biehler": all(gap > 0 for gap in gaps),
        })
    checks = {
        "hardy_kernel_gram_psd": all(case["determinant"] >= -1e-14 for case in gram_cases),
        "kernel_defect_matches_casey_energy": all(abs(case["kernel_energy"] - case["closed_energy"]) < 1e-12 for case in gram_cases),
        "kernel_defect_zero_iff_delta_zero": all((abs(case["kernel_energy"]) < 1e-14) == (case["delta"] == 0.0) for case in gram_cases),
        "HB_gap_formula_exact": all(case["max_gap_formula_error"] < 1e-8 for case in hb_cases),
        "off_line_quartets_still_admit_HB_polynomials": all(case["hermite_biehler"] for case in hb_cases if case["delta"] != 0.0),
        "A_B_interlace_for_all_delta": all(case["interlace"] for case in hb_cases),
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "Hardy/de Branges kernel audit for the repaired Casey cocycle",
        "positive_kernel_result": {
            "kernel": "K(c,d)=1/(c+d)",
            "feature_vectors": "exp(-(a-delta)x), exp(-(a+delta)x)",
            "defect": "pi*(1,-1)G(1,-1)^T = pi*delta^2/[a(a^2-delta^2)]",
            "meaning": "Casey's repaired imbalance is an exact reproducing-kernel distance",
        },
        "hermite_biehler_audit": {
            "candidate": "E_delta,gamma(z)=(z+i gamma)^2-delta^2",
            "gap_identity": "|E(x+iy)|^2-|E#(x+iy)|^2=8 gamma y(delta^2+gamma^2+x^2+y^2)>0",
            "counterlesson": "E is Hermite--Biehler for every delta, so generic de Branges positivity alone does not detect RH",
        },
        "gram_cases": gram_cases,
        "HB_cases": hb_cases,
        "claim_boundary": {
            "proved": ["the cocycle defect is a Hardy-kernel norm", "off-line quartets still possess adaptable Hermite--Biehler polynomials"],
            "missing_for_classical_RH": "one fixed entire E canonically determined by xi, with global kernel positivity and no orbit-dependent retuning",
        },
        "checks": checks,
    }


def main() -> None:
    payload = build_certificate()
    output = ROOT / "data" / "w33_debranges_cocycle_kernel_certificate.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
