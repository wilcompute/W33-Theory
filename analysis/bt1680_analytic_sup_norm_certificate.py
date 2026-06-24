#!/usr/bin/env python3
"""BT1680 — analytic sup-norm certificate for the matter-24 Chebyshev candidate."""
from __future__ import annotations

import json
from pathlib import Path
from fractions import Fraction

# Exact even quartic in x for matter H=L/30 mapped to x=2H-1.
# p(x)= -625/256 x^4 + 225/128 x^2 + 175/256.
# It satisfies p(-1)=0, p(3/5)=1, p(1)=0, and has global max 1.
A = Fraction(-625, 256)
B = Fraction(225, 128)
C = Fraction(175, 256)


def p_at_fraction(x: Fraction) -> Fraction:
    return A * x**4 + B * x**2 + C


def main() -> None:
    values = {
        "p(-1)": str(p_at_fraction(Fraction(-1, 1))),
        "p(3/5)": str(p_at_fraction(Fraction(3, 5))),
        "p(1)": str(p_at_fraction(Fraction(1, 1))),
        "p(0)": str(p_at_fraction(Fraction(0, 1))),
    }
    result = {
        "theorem": "BT1680 Analytic Sup-Norm Certificate",
        "target": "P_matter_24 on x=2(L_m/30)-1 with spectral points {-1, 3/5, 1}",
        "certified_polynomial_power_basis": {
            "x4": str(A),
            "x2": str(B),
            "x0": str(C),
            "formula": "p(x)=-(625/256)x^4+(225/128)x^2+175/256",
        },
        "certified_polynomial_chebyshev_basis": {
            "T0": "1325/2048",
            "T2": "-175/512",
            "T4": "-625/2048",
            "chebyshev_l1": 2650 / 2048,
        },
        "interpolation_values": values,
        "derivative_certificate": {
            "p_prime_factorization": "p'(x)=x*(-625/64*x^2 + 225/64)",
            "critical_points_in_interval": ["-3/5", "0", "3/5"],
            "endpoint_values": {"p(-1)": 0, "p(1)": 0},
            "critical_values": {"p(-3/5)": 1, "p(0)": str(C), "p(3/5)": 1},
            "sup_norm_on_minus1_1": 1,
        },
        "qsvt_parity": {
            "parity": "even degree 4",
            "status": "parity-valid as a scalar polynomial candidate for matter-24",
        },
        "correction_to_BT1676": "The sampled degree-5 matter-24 candidate with sup norm 1.000004174608004 is replaced by an exact even quartic certificate with sup norm 1.",
        "boundary": "This certifies the scalar polynomial bound. It still does not synthesize the full QSVT phase sequence.",
    }
    assert p_at_fraction(Fraction(-1, 1)) == 0
    assert p_at_fraction(Fraction(3, 5)) == 1
    assert p_at_fraction(Fraction(1, 1)) == 0
    out = Path("data/PART_BT1680_ANALYTIC_SUP_NORM_CERTIFICATE_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
