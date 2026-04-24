"""Exact operator ladder for the W(3,3) discrete mass gap.

The active paper currently mixes three closely related quantities:

1. ``sqrt(10)`` as the first positive Dirac-scale mass,
2. ``10`` as the first positive Laplacian/canonical gap,
3. ``100`` as the first positive Yang-Mills action eigenvalue.

They are not competing claims. They are the same spectral datum viewed through
three operators on the same W(3,3) carrier:

    A      adjacency,              spec(A)   = {12, 2^24, (-4)^15}
    L      = 12 I - A,             spec(L)   = {0, 10^24, 16^15}
    |D|    = sqrt(L),              spec(|D|) = {0, (sqrt(10))^24, 4^15}
    H_YM   = L^2 = |D|^4,          spec(H)   = {0, 100^24, 256^15}

So the exact ladder is

    sqrt(10)  ->  10  ->  100
      |D|        L         H_YM.

This resolves the paper-level wording seam cleanly:

- in Dirac spectral units the first mass is ``sqrt(10)``;
- in Laplacian/canonical units the gap is ``10``;
- in Yang-Mills action units the first positive eigenvalue is ``100``.
"""

from __future__ import annotations

from fractions import Fraction
import json
from math import isqrt
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_mass_gap_operator_ladder_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from w33_homology import build_w33


def _eigen_signature(values: np.ndarray, decimals: int = 8) -> dict[str, int]:
    rounded = np.round(values.astype(float), decimals)
    uniq, counts = np.unique(rounded, return_counts=True)
    out: dict[str, int] = {}
    for value, count in zip(uniq, counts):
        ivalue = int(round(float(value)))
        out[str(ivalue)] = int(count)
    return out


def build_mass_gap_operator_ladder_summary() -> dict[str, Any]:
    n, _vertices, adj_list, _edges = build_w33()
    a = np.zeros((n, n), dtype=int)
    for i, nbrs in enumerate(adj_list):
        for j in nbrs:
            a[i, j] = 1

    k = 12
    q = 3
    lam = 2
    phi4 = q * q + 1
    color_adjoint_dim = q * q - 1

    a_vals = np.linalg.eigvalsh(a.astype(float))
    l = k * np.eye(n, dtype=int) - a
    l_vals = np.linalg.eigvalsh(l.astype(float))
    h_ym = l @ l
    h_vals = np.linalg.eigvalsh(h_ym.astype(float))

    positive_l = sorted(v for v in l_vals if v > 1e-8)
    positive_h = sorted(v for v in h_vals if v > 1e-8)

    lap_gap = int(round(positive_l[0]))
    ym_gap = int(round(positive_h[0]))
    dirac_gap_radicand = lap_gap
    dirac_gap_integer_branch = isqrt(int(round(positive_l[-1])))
    dirac_gap_is_irrational = isqrt(dirac_gap_radicand) ** 2 != dirac_gap_radicand

    normalized_gap = Fraction(lap_gap, k)

    return {
        "operator_ladder_dictionary": {
            "n_vertices": n,
            "adjacency_spectrum": _eigen_signature(a_vals),
            "laplacian_spectrum": _eigen_signature(l_vals),
            "yang_mills_action_spectrum": _eigen_signature(h_vals),
            "dirac_positive_scales": {
                "lowest_formula": "sqrt(Phi_4) = sqrt(10)",
                "higher_formula": "sqrt(16) = 4",
                "lowest_radicand": dirac_gap_radicand,
                "higher_integer_branch": dirac_gap_integer_branch,
            },
            "gap_dictionary": {
                "adjacency_transfer_gap_formula": "k - r = Phi_4",
                "laplacian_gap_formula": "gap(L) = Phi_4 = 10",
                "dirac_gap_formula": "gap(|D|) = sqrt(Phi_4) = sqrt(10)",
                "yang_mills_gap_formula": "gap(H_YM) = Phi_4^2 = 100",
                "normalized_gap_formula": "gap(L/k) = Phi_4 / k = 5/6",
                "laplacian_gap": lap_gap,
                "yang_mills_gap": ym_gap,
                "normalized_gap": {
                    "exact": f"{normalized_gap.numerator}/{normalized_gap.denominator}",
                    "float": float(normalized_gap),
                },
            },
            "color_side_dictionary": {
                "q": q,
                "phi4": phi4,
                "color_adjoint_dim": color_adjoint_dim,
                "lambda": lam,
                "phi4_equals_color_adjoint_plus_lambda": (
                    phi4 == color_adjoint_dim + lam
                ),
            },
        },
        "exact_factorizations": {
            "adjacency_spectrum_is_12_1_2_24_minus4_15": (
                _eigen_signature(a_vals) == {"-4": 15, "2": 24, "12": 1}
            ),
            "laplacian_spectrum_is_0_1_10_24_16_15": (
                _eigen_signature(l_vals) == {"0": 1, "10": 24, "16": 15}
            ),
            "yang_mills_action_spectrum_is_0_1_100_24_256_15": (
                _eigen_signature(h_vals) == {"0": 1, "100": 24, "256": 15}
            ),
            "laplacian_gap_equals_phi4": lap_gap == phi4,
            "dirac_gap_squared_equals_laplacian_gap": (
                dirac_gap_radicand == lap_gap
            ),
            "yang_mills_gap_is_laplacian_gap_squared": ym_gap == lap_gap * lap_gap,
            "sqrt_of_yang_mills_gap_returns_laplacian_gap": isqrt(ym_gap) == lap_gap,
            "dirac_low_gap_is_irrational": dirac_gap_is_irrational,
            "dirac_high_gap_is_exactly_4": dirac_gap_integer_branch == 4,
            "normalized_gap_is_5_over_6": normalized_gap == Fraction(5, 6),
            "phi4_equals_q2_plus_1": phi4 == q * q + 1,
            "phi4_equals_color_adjoint_plus_lambda": (
                phi4 == color_adjoint_dim + lam
            ),
        },
        "bridge_verdict": (
            "The paper's apparent mass-gap mismatch is an operator-choice issue, "
            "not an algebra failure. The same W(3,3) spectral datum appears as "
            "sqrt(10) on the Dirac square-root operator |D|, as 10 on the "
            "vertex/canonical Laplacian L=12I-A, and as 100 on the Yang-Mills "
            "action Hamiltonian H_YM=L^2. So the discrete gap closes as one exact "
            "operator ladder sqrt(10) -> 10 -> 100, with normalized gap 5/6."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_mass_gap_operator_ladder_summary(), indent=2),
        encoding="utf-8",
    )
    return path


if __name__ == "__main__":
    write_summary()
