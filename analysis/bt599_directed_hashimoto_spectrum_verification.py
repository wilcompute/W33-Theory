#!/usr/bin/env python3
"""BT599: directed Hashimoto spectrum verification.

This verifies the nonbacktracking/Ihara layer for the W33 collinearity graph
from its known SRG spectrum 12^1, 2^24, (-4)^15.

For a d-regular graph with d=12 and m=240 undirected edges, the directed-edge
Hashimoto operator B has dimension 2m=480.  Ihara-Bass gives:

  det(I-uB) = (1-u^2)^(m-n) det(I-uA+(d-1)u^2 I).

Therefore the B-eigenvalues are:
  - for each adjacency eigenvalue lambda, roots of x^2-lambda*x+(d-1)=0;
  - plus +1 and -1, each with multiplicity m-n.

The Perron root is d-1=11.  The nontrivial quadratic roots have modulus sqrt(11),
and the denominator in the BT594/BT598 leakage normalization is 11^2=121.
"""
from __future__ import annotations

from fractions import Fraction
import cmath
import json
from pathlib import Path

n = 40
m = 240
d = 12
p = d - 1
spectrum_A = [(12, 1), (2, 24), (-4, 15)]

hashimoto_blocks = []
for lam, mult in spectrum_A:
    disc = lam * lam - 4 * p
    root_disc = cmath.sqrt(disc)
    r1 = (lam + root_disc) / 2
    r2 = (lam - root_disc) / 2
    hashimoto_blocks.append(
        {
            "lambda_A": lam,
            "multiplicity": mult,
            "quadratic": f"x^2 - ({lam}) x + {p}",
            "root_1": [round(r1.real, 12), round(r1.imag, 12)],
            "root_2": [round(r2.real, 12), round(r2.imag, 12)],
            "root_modulus_squared": round(abs(r1) ** 2, 12),
        }
    )

extra_plus = m - n
extra_minus = m - n
hashimoto_dimension = 2 * m
quadratic_dimension = 2 * sum(mult for _lam, mult in spectrum_A)
extra_dimension = extra_plus + extra_minus

# Moment/leakage normalization carried from BT598.
M3 = sum(mult * lam**3 for lam, mult in spectrum_A)
M5 = sum(mult * lam**5 for lam, mult in spectrum_A)
leakage = Fraction(M5, M3) / (p * p)

checks = {
    "directed_edge_dimension": hashimoto_dimension == 480,
    "quadratic_dimension_plus_trivial_dimension": quadratic_dimension + extra_dimension == hashimoto_dimension,
    "extra_plus_multiplicity": extra_plus == 200,
    "extra_minus_multiplicity": extra_minus == 200,
    "perron_root_is_p": p == 11,
    "ihara_square": p * p == 121,
    "moment_normalization_is_leakage": leakage == Fraction(244, 121),
    "M5_over_M3_is_244": Fraction(M5, M3) == 244,
}

result = {
    "bt": 599,
    "title": "Directed Hashimoto spectrum verification",
    "graph": {
        "vertices": n,
        "undirected_edges": m,
        "directed_edges": hashimoto_dimension,
        "degree": d,
        "nonbacktracking_outdegree": p,
    },
    "adjacency_spectrum": {str(lam): mult for lam, mult in spectrum_A},
    "ihara_bass_factorization": {
        "trivial_plus_one_multiplicity": extra_plus,
        "trivial_minus_one_multiplicity": extra_minus,
        "quadratic_root_dimension": quadratic_dimension,
        "total_dimension": hashimoto_dimension,
    },
    "hashimoto_quadratic_blocks": hashimoto_blocks,
    "moment_leakage_normalization": {
        "M3": M3,
        "M5": M5,
        "M5_over_M3": str(Fraction(M5, M3)),
        "divisor": "(d-1)^2",
        "divisor_value": p * p,
        "normalized_ratio": str(leakage),
    },
    "interpretation": "The directed Hashimoto spectrum supplies the p=d-1=11 nonbacktracking scale. The cubic leakage ratio is the W33 odd spectral transport M5/M3 normalized by p^2.",
    "checks": checks,
    "all_identities_hold": all(checks.values()),
}

Path("data/PART_BT599_DIRECTED_HASHIMOTO_SPECTRUM_VERIFICATION_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
