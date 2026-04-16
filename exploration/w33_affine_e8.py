"""
Affine E8 character (level 1) exploration.

We compute a truncated q-expansion of the E8 lattice VOA character
using the identity

    ch_{E8, level=1}(tau) = Theta_{E8}(tau) / eta(tau)^8

where `Theta_{E8}` is provided by `w33_lattice_theta.e4_series` and
`eta` is the Dedekind eta function. We return the formal series and the
vacuum shift `-c/24 = -8/24 = -1/3`.
"""
from __future__ import annotations

from fractions import Fraction
from typing import List

from pathlib import Path
import json

from w33_lattice_theta import e4_series
from w33_euler_pentagonal import euler_pentagonal_series


def _series_mul(A: List[int], B: List[int], n_max: int) -> List[int]:
    out = [0] * (n_max + 1)
    for i, a in enumerate(A):
        if a == 0 or i > n_max:
            continue
        for j, b in enumerate(B):
            if i + j > n_max:
                break
            out[i + j] += a * b
    return out


def _series_pow(A: List[int], power: int, n_max: int) -> List[int]:
    out = [1] + [0] * n_max
    for _ in range(power):
        out = _series_mul(out, A, n_max)
    return out


def _series_inv(A: List[int], n_max: int) -> List[int]:
    """Formal power series inverse of A (A[0]==1) truncated to n_max."""
    assert A[0] == 1
    B = [0] * (n_max + 1)
    B[0] = 1
    for k in range(1, n_max + 1):
        s = 0
        for i in range(1, k + 1):
            ai = A[i] if i < len(A) else 0
            s += ai * B[k - i]
        B[k] = -s
    return B


def affine_e8_series(q_order: int = 10) -> dict:
    """Return {'shift': Fraction, 'series': [a0,a1,...]} where
    the character is q^{shift} * sum_{n>=0} series[n] q^n.
    """
    # prod(1 - q^n) coefficients
    euler = euler_pentagonal_series(q_order)
    # (prod (1 - q^n))^8
    prod8 = _series_pow(euler, 8, q_order)
    inv_prod8 = _series_inv(prod8, q_order)
    e4 = e4_series(q_order)
    # E4 * prod^{-8}
    series = _series_mul(e4, inv_prod8, q_order)
    # vacuum shift -c/24 for c=8
    shift = Fraction(-8, 24)
    return {"shift": shift, "series": series}


def derive_all_affine_e8(q_order: int = 10) -> dict:
    s = affine_e8_series(q_order=q_order)
    return {
        "shift": str(s["shift"]),
        "series_sample": s["series"][:10],
        "summary_chain": {
            "vacuum_shift_minus_one_third": s["shift"] == Fraction(-1, 3),
            "leading_coeff_1": s["series"][0] == 1,
        },
    }


def main() -> None:
    out = derive_all_affine_e8(q_order=10)
    p = Path(__file__).resolve().parent.parent / "data" / "w33_affine_e8.json"
    p.write_text(json.dumps(out, indent=2, default=str))
    print(f"Wrote {p}")


if __name__ == "__main__":
    main()
