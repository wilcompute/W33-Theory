#!/usr/bin/env python3
"""
PART CXXXIX — RG Embedding Inversion and W(3,3) k3 Window
=========================================================

This audit continues the May-2026 RG/M_GUT fix.

The latest RG correction correctly separates a model-level unified coupling
alpha_unified(M_GUT) from the SU(3)_c MS-bar coupling alpha_s(M_GUT):

    alpha_s(M_GUT) = alpha_unified(M_GUT) / k3.

The remaining question is not whether such a conversion is needed, but what
effective W(3,3)/E8 embedding factor k3 is selected by data and by finite
W(3,3) arithmetic.

This module inverts the RG map:

    k3  --->  alpha_s(M_Z)

using the same two-loop QCD beta normalization and a piecewise nf=6/nf=5
run across the top threshold.  It then solves for the effective k3 that
recovers PDG alpha_s(M_Z)=0.1180.

Core output under the current no-heavy-threshold model:

    k3_eff(two-loop) ≈ 1.84946.

This is not k3=1.  With alpha_unified=1/25 at M_GUT=(13/7)*1e16 GeV, k3=1
runs into a Landau-like runaway before M_Z.  The inverse audit therefore
turns the latest RG fix into a falsifiable embedding-normalization problem.

Nearest W(3,3) rational candidates:
    24/13 = 1.84615  -> alpha_s(M_Z) ≈ 0.11923  (~1.37 sigma high)
    13/7  = 1.85714  -> alpha_s(M_Z) ≈ 0.11524  (~3.07 sigma low)
    37/20 = 1.85000  -> alpha_s(M_Z) ≈ 0.11780  (~0.22 sigma low)

The exact best value is not promoted as finite theorem; it is an inverse
phenomenology target.  The theorem-grade statement is the deterministic audit:
under the stated RG conventions, k3=1 fails, while the physical recovery window
is a narrow W(3,3)-rational neighborhood around ~1.85.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent

# W(3,3) / RG constants used by the latest RG/M_GUT sprint.
Q = 3
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
K = 12
MU = 4

ALPHA_UNIFIED = 1.0 / 25.0
M_GUT = (13.0 / 7.0) * 1.0e16
M_TOP = 172.57
M_Z = 91.1876
PDG_ALPHA_S_MZ = 0.1180
PDG_SIGMA = 0.0009


def beta_qcd_2loop(alpha_s: float, nf: int) -> float:
    """Two-loop QCD beta function in alpha_s.

    d(alpha_s)/d(ln mu)
      = - beta0/(2*pi) * alpha_s^2
        - beta1/(4*pi^2) * alpha_s^3

    beta0 = 11 - 2 nf / 3
    beta1 = 102 - 38 nf / 3
    """
    beta0 = 11.0 - (2.0 * nf) / 3.0
    beta1 = 102.0 - (38.0 * nf) / 3.0
    return (
        -(beta0 / (2.0 * math.pi)) * alpha_s * alpha_s
        - (beta1 / (4.0 * math.pi * math.pi)) * alpha_s**3
    )


def rk4_step(alpha_s: float, h: float, nf: int) -> float:
    f = lambda a: beta_qcd_2loop(a, nf)
    k1 = h * f(alpha_s)
    k2 = h * f(alpha_s + k1 / 2.0)
    k3 = h * f(alpha_s + k2 / 2.0)
    k4 = h * f(alpha_s + k3)
    return alpha_s + (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0


def run_alpha_s(
    alpha_s_start: float,
    mu_start: float,
    mu_end: float,
    nf: int,
    n_steps: int = 5000,
    runaway_cap: float = 10.0,
) -> Optional[float]:
    """Run alpha_s between two scales using RK4 in log(mu)."""
    ln_start = math.log(mu_start)
    ln_end = math.log(mu_end)
    h = (ln_end - ln_start) / float(n_steps)
    a = float(alpha_s_start)

    for _ in range(n_steps):
        a = rk4_step(a, h, nf)
        if not math.isfinite(a) or a <= 0.0 or a > runaway_cap:
            return None

    return a


def alpha_s_mz_from_k3(k3: float, steps_high: int = 6000, steps_low: int = 2000) -> Optional[float]:
    """Map k3 to alpha_s(M_Z) under the current two-loop piecewise model."""
    if k3 <= 0:
        return None
    alpha_s_gut = ALPHA_UNIFIED / k3
    alpha_top_nf6 = run_alpha_s(alpha_s_gut, M_GUT, M_TOP, nf=6, n_steps=steps_high)
    if alpha_top_nf6 is None:
        return None
    # At mu=m_top the one-loop decoupling log is zero, so the central matching
    # value is continuous in this minimal model.
    alpha_top_nf5 = alpha_top_nf6
    return run_alpha_s(alpha_top_nf5, M_TOP, M_Z, nf=5, n_steps=steps_low)


def one_loop_inverse_k3() -> float:
    """Closed-form one-loop inverse estimate of k3.

    1/alpha_s(M_GUT) =
        1/alpha_s(M_Z)
        + beta0_nf5/(2*pi) ln(M_top/M_Z)
        + beta0_nf6/(2*pi) ln(M_GUT/M_top).

    k3 = alpha_unified / alpha_s(M_GUT).
    """
    beta0_nf5 = 11.0 - 2.0 * 5.0 / 3.0
    beta0_nf6 = 11.0 - 2.0 * 6.0 / 3.0
    inv_alpha_gut = (
        1.0 / PDG_ALPHA_S_MZ
        + (beta0_nf5 / (2.0 * math.pi)) * math.log(M_TOP / M_Z)
        + (beta0_nf6 / (2.0 * math.pi)) * math.log(M_GUT / M_TOP)
    )
    alpha_gut = 1.0 / inv_alpha_gut
    return ALPHA_UNIFIED / alpha_gut


def solve_k3_for_target(
    target: float = PDG_ALPHA_S_MZ,
    lo: float = 1.70,
    hi: float = 2.00,
    iterations: int = 48,
) -> Tuple[float, float]:
    """Solve alpha_s_mz_from_k3(k3)=target by bisection.

    In this window alpha_s(M_Z) decreases monotonically with k3.
    """
    f_lo = alpha_s_mz_from_k3(lo)
    f_hi = alpha_s_mz_from_k3(hi)
    if f_lo is None or f_hi is None:
        raise ValueError("initial bracket includes RG runaway")
    if not (f_lo > target > f_hi):
        raise ValueError(f"target not bracketed: f({lo})={f_lo}, f({hi})={f_hi}")

    for _ in range(iterations):
        mid = (lo + hi) / 2.0
        f_mid = alpha_s_mz_from_k3(mid)
        if f_mid is None:
            lo = mid
            continue
        if f_mid > target:
            lo = mid
        else:
            hi = mid

    k3 = (lo + hi) / 2.0
    return k3, float(alpha_s_mz_from_k3(k3))


@dataclass(frozen=True)
class K3Candidate:
    label: str
    value: float
    alpha_s_mz: Optional[float]
    residual: Optional[float]
    sigma: Optional[float]


def evaluate_candidate(label: str, value: float) -> K3Candidate:
    a = alpha_s_mz_from_k3(value)
    if a is None:
        return K3Candidate(label, value, None, None, None)
    residual = a - PDG_ALPHA_S_MZ
    sigma = residual / PDG_SIGMA
    return K3Candidate(label, value, a, residual, sigma)


def candidate_k3_values() -> List[K3Candidate]:
    """Finite/W33-rational candidates near the inverse target."""
    raw = [
        ("k3=1 (standard SU5/E8 trace-normalization baseline)", 1.0),
        ("7/4", 7 / 4),
        ("24/13 = 2(k)/Phi3", 24 / 13),
        ("37/20 = (v-mu+1)/(v/2)", 37 / 20),
        ("13/7 = Phi3/Phi6 = M_GUT prefactor", 13 / 7),
        ("50/27", 50 / 27),
        ("2", 2.0),
    ]
    return [evaluate_candidate(label, value) for label, value in raw]


def scan_window(start: float = 1.80, stop: float = 1.90, step: float = 0.005) -> List[Dict[str, object]]:
    rows = []
    n = int(round((stop - start) / step)) + 1
    for i in range(n):
        k3 = start + i * step
        a = alpha_s_mz_from_k3(k3)
        rows.append(
            {
                "k3": round(k3, 6),
                "alpha_s_mz": None if a is None else round(a, 9),
                "sigma": None if a is None else round((a - PDG_ALPHA_S_MZ) / PDG_SIGMA, 4),
            }
        )
    return rows


def rg_embedding_inversion_audit() -> Dict[str, object]:
    k3_star, alpha_star = solve_k3_for_target()
    one_loop_k3 = one_loop_inverse_k3()
    candidates = candidate_k3_values()

    k3_one = evaluate_candidate("k3=1", 1.0)
    assert k3_one.alpha_s_mz is None, "k3=1 should run away in this minimal model"
    assert 1.84 < k3_star < 1.86
    assert abs(alpha_star - PDG_ALPHA_S_MZ) < 1e-10

    candidate_dicts = [asdict(c) for c in candidates]

    return {
        "module": "PART_CXXXIX_RG_EMBEDDING_INVERSION",
        "inputs": {
            "alpha_unified": ALPHA_UNIFIED,
            "M_GUT": M_GUT,
            "M_GUT_formula": "(13/7)*1e16 GeV",
            "M_top": M_TOP,
            "M_Z": M_Z,
            "pdg_alpha_s_MZ": PDG_ALPHA_S_MZ,
            "pdg_sigma": PDG_SIGMA,
            "nf_high": 6,
            "nf_low": 5,
        },
        "w33_values": {
            "q": Q,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "k": K,
            "mu": MU,
        },
        "inverse_solution": {
            "k3_eff_two_loop": k3_star,
            "alpha_s_MZ_at_k3_eff": alpha_star,
            "one_loop_inverse_k3": one_loop_k3,
            "two_loop_minus_one_loop_shift": k3_star - one_loop_k3,
        },
        "candidate_values": candidate_dicts,
        "scan_window_1p80_1p90": scan_window(),
        "theorem_statement": (
            "With alpha_unified=1/25 and M_GUT=(13/7)*1e16 GeV, the two-loop "
            "piecewise QCD RG map requires k3_eff≈1.84946 to recover "
            "alpha_s(M_Z)=0.1180. The k3=1 baseline is a runaway under the "
            "same conventions, so the remaining W(3,3) problem is an embedding/"
            "threshold normalization problem, not a numerical integrator problem."
        ),
        "interpretive_note": (
            "The effective value sits in the W(3,3) rational neighborhood "
            "24/13≈1.846 and 13/7≈1.857. The candidate 24/13 is within about "
            "1.4 sigma in the minimal no-heavy-threshold model; 13/7 is about "
            "3.1 sigma low. Heavy-threshold corrections at M_GUT can plausibly "
            "move this window, so the right next step is to derive k3/thresholds "
            "from the E8/W(3,3) embedding rather than assert k3=1."
        ),
    }


def main() -> int:
    audit = rg_embedding_inversion_audit()
    out = ROOT / "PART_CXXXIX_rg_embedding_inversion_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
