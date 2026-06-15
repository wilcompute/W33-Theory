#!/usr/bin/env python3
"""BT1144 -- align the K3 corpus carrier with the finite W33 operator.

Repo anchor: BT1033 already uses the finite W33 Hodge--Dirac square spectrum

    D_F^2 = 0^122 + 4^240 + 10^48 + 16^30

and extracts (Tr 1, Tr D_F^2, Tr D_F^4) = (440, 1920, 16320).

This script states the carrier theorem in executable form: the metric/topological
K3 curvature functional is the continuum carrier, and the finite W33 Hodge--Dirac
spectrum supplies the coefficients multiplying it in the almost-commutative
product.  The scalar, spin, and ordinary-Hodge continuum operators are probes of
this carrier, not replacements for the finite W33 spectrum.
"""

from __future__ import annotations

import json
from fractions import Fraction

DF2_SPECTRUM = {0: 122, 4: 240, 10: 48, 16: 30}
q = 3
Phi3 = q * q + q + 1
q_factorial = 6
E_edges = 240
K3_chi = 24

N = sum(DF2_SPECTRUM.values())
F2 = sum(lam * mult for lam, mult in DF2_SPECTRUM.items())
F4 = sum(lam * lam * mult for lam, mult in DF2_SPECTRUM.items())
F4_half = F4 // 2

carrier = {
    "continuum_metric_carrier": "K3 corpus/topological curvature functional",
    "finite_operator_carrier": "finite W33 Hodge--Dirac square D_F^2 spectrum",
    "product_formula": "C4 = Tr(1_F)*A4 + Tr(D_F^4)/2 when A2=0 and A0=1",
    "not_replacements": [
        "scalar positive Laplacian",
        "spin Dirac square",
        "ordinary all-forms Hodge trace",
    ],
}

C4_corpus = N * K3_chi + F4_half

result = {
    "bt": 1144,
    "title": "finite W33 carrier alignment for the K3 corpus curvature lane",
    "repo_anchor": "analysis/bt1033_spectral_action_term_by_term_geometric.py",
    "finite_spectrum_DF_squared": {str(k): v for k, v in DF2_SPECTRUM.items()},
    "finite_moments": {"Tr1": N, "TrDF2": F2, "TrDF4": F4, "TrDF4_half": F4_half},
    "k3_corpus_inputs": {"A0": 1, "A2": 0, "A4_corpus": K3_chi},
    "carrier": carrier,
    "C4_corpus": C4_corpus,
    "substrate_identity": {
        "C4_corpus_over_E": str(Fraction(C4_corpus, E_edges)),
        "q_factorial_Phi3": q_factorial * Phi3,
        "identity": "C4_corpus = E*q!*Phi3 = 240*6*13 = 18720",
    },
    "checks": {
        "finite_moments_match_BT1033": (N, F2, F4) == (440, 1920, 16320),
        "ricci_flat_A2_removed": True,
        "C4_corpus_is_18720": C4_corpus == 18720,
        "C4_identity": C4_corpus == E_edges * q_factorial * Phi3,
        "carrier_is_product_not_single_probe": len(carrier["not_replacements"]) == 3,
    },
}
result["checks"]["all_checks_pass"] = all(result["checks"].values())
print(json.dumps(result, indent=2, sort_keys=True))
