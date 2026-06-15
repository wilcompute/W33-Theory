#!/usr/bin/env python3
"""
BT1133 -- finite W33 heat moment extractor.

Extracts N, F2, and F4 from the committed W33 Hodge--Dirac square spectrum

    D_F^2 : 0^122, 4^240, 10^48, 16^30

and plugs those moments into the BT1129/BT1130 product-heat formulas.

This is the numeric/exact execution of the second top next step after BT1129.
"""

from __future__ import annotations

import json
from fractions import Fraction

SPECTRUM_D2 = {
    0: 122,
    4: 240,
    10: 48,
    16: 30,
}


def moment(power: int) -> int:
    return sum((lam ** power) * mult for lam, mult in SPECTRUM_D2.items())


def main() -> None:
    # Theta_F(t)=Tr(exp(-t D_F^2))=N-F2*t+(F4/2)*t^2+...
    N = sum(SPECTRUM_D2.values())
    F2 = moment(1)
    F4 = moment(2)

    payload = {
        "bt": 1133,
        "title": "finite W33 heat moment extractor",
        "input_spectrum_DF_squared": {str(k): v for k, v in SPECTRUM_D2.items()},
        "moments": {
            "N": N,
            "F2": F2,
            "F4": F4,
            "F4_over_2": F4 // 2,
        },
        "raw_ratios": {
            "F2_over_N": str(Fraction(F2, N)),
            "F4_over_F2": str(Fraction(F4, F2)),
            "F4_over_N": str(Fraction(F4, N)),
        },
        "product_heat_coefficients": {
            "C0": "440*A0",
            "C2": "440*A2 - 1920*A0",
            "C4": "440*A4 - 1920*A2 + 8160*A0",
        },
        "ricci_flat_k3_specialization": {
            "condition": "A2=0",
            "C0": "440*A0",
            "C2": "-1920*A0",
            "C4": "440*A4 + 8160*A0",
        },
        "checks": {
            "dimension_is_440": N == 440,
            "Tr_DF2_is_1920": F2 == 1920,
            "Tr_DF4_is_16320": F4 == 16320,
            "F4_even_for_half_coefficient": F4 % 2 == 0,
            "all_checks_pass": (N, F2, F4, F4 % 2) == (440, 1920, 16320, 0),
        },
        "boundary": (
            "This extracts finite W33 moments from the committed D_F^2 spectrum. "
            "It does not compute a K3 metric, volume, or continuum spectral-action value."
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
