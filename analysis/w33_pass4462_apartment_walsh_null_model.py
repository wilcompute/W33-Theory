#!/usr/bin/env python3
"""Pass 4462 -- exact null model for the W33 apartment-parity observable.

Pass 4461 identified the variable fourth spectral moment of a line-signed W33
collinearity graph with a quartic Walsh polynomial

    W4(sigma) = sum_{a in Apartments} prod_{line in a} sigma_line,

on the 40 independent line bits.  This pass removes the need for a Monte-Carlo
baseline by computing the low moments of W4 exactly.

For Walsh monomials chi_S, E chi_S chi_T is zero unless S=T.  More generally,
products survive expectation exactly when the symmetric difference of their
supports is empty.  Encoding each 4-line apartment as a 40-bit mask therefore
turns moments into XOR counts.

The exact ordered-pair XOR multiplicity spectrum is

      multiplicity c_x    number of XOR masks x
             1620                 1
               24               540
               12              2160
                8             14580
                6             10800
                4             64800
                2           1071630

and every apartment mask itself has c_x=8.  Consequently

    E[W4]   = 0,
    E[W4^2] = 1620,
    E[W4^3] = 12960,
    E[W4^4] = 9891720.

Thus the random-line-signing null is not exactly Gaussian: its standardized
skewness is about +0.1987616 and its excess kurtosis about +0.7691358.  For the
frustrated-apartment fraction f4=(1-W4/1620)/2 the skewness changes sign.

This is a baseline theorem, not evidence that any optimized signing is special.
It exists specifically to prevent a repetition of the search-without-baseline
failure quantified at Pass 4454.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np

from w33_pass4461_line_signing_apartment_trace import geometry, simple_four_cycles

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    _, _, A, _, edge_line = geometry()
    cycles = simple_four_cycles(A)
    supports = [frozenset(edge_line[e] for e in C) for C in cycles]
    assert len(supports) == 1620
    assert len(set(supports)) == 1620

    masks = []
    for support in supports:
        m = 0
        for li in support:
            m |= 1 << li
        masks.append(m)

    xor_counts = Counter()
    for a in masks:
        for b in masks:
            xor_counts[a ^ b] += 1

    pair_spectrum = Counter(xor_counts.values())
    expected_pair_spectrum = Counter(
        {
            1620: 1,
            24: 540,
            12: 2160,
            8: 14580,
            6: 10800,
            4: 64800,
            2: 1071630,
        }
    )
    assert pair_spectrum == expected_pair_spectrum
    assert sum(c * n for c, n in pair_spectrum.items()) == 1620**2
    assert set(xor_counts[m] for m in masks) == {8}

    m1 = 0
    m2 = 1620
    m3 = sum(xor_counts[m] for m in masks)
    m4 = sum(c * c for c in xor_counts.values())
    assert m3 == 12960
    assert m4 == 9891720

    skew = m3 / (m2 ** 1.5)
    excess = m4 / (m2**2) - 3.0

    # Pass 4461 trace relation T4=12000+8W4.
    trace4_mean = 12000
    trace4_var = 64 * m2
    trace4_sd = float(np.sqrt(trace4_var))

    result = {
        "pass": 4462,
        "theorem": "W33 apartment Walsh exact null model",
        "apartments": 1620,
        "walsh_moments": {
            "E_W4": m1,
            "E_W4_2": m2,
            "E_W4_3": m3,
            "E_W4_4": m4,
            "standardized_skewness": skew,
            "excess_kurtosis": excess,
        },
        "ordered_pair_xor_multiplicity_spectrum": {
            str(c): n for c, n in sorted(pair_spectrum.items(), reverse=True)
        },
        "apartment_mask_xor_multiplicity": 8,
        "frustrated_fraction": {
            "mean": 0.5,
            "sd": 1.0 / (2.0 * np.sqrt(1620.0)),
            "standardized_skewness": -skew,
            "excess_kurtosis": excess,
        },
        "trace_A4_null": {
            "mean": trace4_mean,
            "variance": trace4_var,
            "sd": trace4_sd,
        },
        "boundary": (
            "These are exact moments of the independent random line-signing baseline. "
            "They grade future optimized/sign-structured samples; they do not themselves "
            "make an optimized sample significant."
        ),
    }

    out = ROOT / "data" / "PART_W33_PASS4462_APARTMENT_WALSH_NULL_MODEL.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Pass 4462 -- exact apartment Walsh null model")
    print("  E W4^2 = 1620")
    print("  E W4^3 = 12960")
    print("  E W4^4 = 9891720")
    print(f"  skew(W4) = {skew:.12f}")
    print(f"  excess kurtosis(W4) = {excess:.12f}")
    print(f"  null SD(trace A_sigma^4) = {trace4_sd:.12f}")
    print(f"  wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
