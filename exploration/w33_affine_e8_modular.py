"""
Numeric modular-invariance checks for the affine E8 character.

This verifies that the character ch(τ) = q^{-1/3} * Σ a_n q^n computed from
`w33_affine_e8.affine_e8_series` is invariant under the modular S-transform
τ -> -1/τ (weight 0 modular function), to numerical precision.
"""
from __future__ import annotations

from fractions import Fraction
from typing import List, Dict, Any

try:
    import mpmath as mp
except Exception:  # pragma: no cover - tests will skip without mpmath
    mp = None

from w33_affine_e8 import affine_e8_series


def _evaluate_series_at_tau(series: List[int], shift: Fraction, tau: complex, prec: int = 80):
    if mp is None:
        raise RuntimeError("mpmath required for numeric modular checks")
    old = mp.mp.dps
    mp.mp.dps = int(prec)
    try:
        tau_c = mp.mpc(tau.real, tau.imag)
        q = mp.e ** (2 * mp.pi * mp.j * tau_c)
        total = mp.mpc(0)
        for n, a in enumerate(series):
            if a == 0:
                continue
            total += mp.mpf(a) * mp.power(q, n)
        # apply shift q^{shift}
        shift_val = mp.mpf(shift.numerator) / mp.mpf(shift.denominator)
        total = mp.power(q, shift_val) * total
        return total
    finally:
        mp.mp.dps = old


def verify_affine_e8_modular(q_order: int = 30, tau_im: float = 0.5, prec: int = 80) -> Dict[str, Any]:
    """Check ch(τ) ≈ ch(-1/τ) numerically for given truncation and precision.

    Returns dict with `match` boolean and numeric values as strings.
    """
    if mp is None:
        return {"match": False, "reason": "mpmath not available"}

    s = affine_e8_series(q_order=q_order)
    series = s["series"]
    shift = s["shift"]

    tau = complex(0.0, float(tau_im))
    val1 = _evaluate_series_at_tau(series, shift, tau, prec=prec)
    tau2 = -1.0 / tau
    val2 = _evaluate_series_at_tau(series, shift, tau2, prec=prec)

    # difference
    diff = mp.fabs(val1 - val2)
    match = diff < mp.mpf("1e-8")
    return {
        "tau": str(tau),
        "tau_S": str(tau2),
        "val_tau": mp.nstr(val1, 20),
        "val_tau_S": mp.nstr(val2, 20),
        "diff": mp.nstr(diff, 8),
        "match": bool(match),
    }


def derive_all_affine_e8_modular(q_order: int = 30, tau_im: float = 0.5, prec: int = 80) -> Dict[str, Any]:
    r = verify_affine_e8_modular(q_order=q_order, tau_im=tau_im, prec=prec)
    return {"modular_check": r, "summary_chain": {"S_invariance": r.get("match", False)}}


if __name__ == "__main__":
    print(derive_all_affine_e8_modular(q_order=30, tau_im=0.5, prec=100))
