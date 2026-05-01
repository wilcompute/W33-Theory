"""
w33_rg_phi6_polar_pipeline.py

Selected W(3,3) Phi6-polar RG pipeline adapter.

This module wires the branch-selection result of Parts CXLII-CXLIII into the
existing RG integrator without replacing scripts/w33_rg_gut_conversion.py.

Selected QCD-local branch:

    k3_bare = 24/13
    tau_GUT = log sqrt(mu/Phi6) = log(2/sqrt(7))
    delta_GUT = alpha_unified/(2*pi) * tau_GUT

and therefore

    alpha_s(M_GUT) = alpha_unified/k3_bare * (1 + delta_GUT).

Using the live two-loop RK4 integrator, this gives alpha_s(M_Z) ~= 0.118005,
within 0.006 sigma of PDG alpha_s(M_Z)=0.1180 +/- 0.0009.
"""

from __future__ import annotations

import math
import os
import sys
from typing import Dict

# Allow running as `python scripts/...` from repo root or from scripts/.
THIS_DIR = os.path.dirname(__file__)
if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)

from w33_rg_gut_conversion import (  # noqa: E402
    run_alpha_s,
    threshold_match_top,
    w33_alpha_unified_gut,
    w33_m_gut,
)

Q = 3
MU = 4
PHI3 = Q * Q + Q + 1
PHI6 = Q * Q - Q + 1
M_TOP = 172.57
M_Z = 91.1876
PDG_ALPHA_S_MZ = 0.1180
PDG_ALPHA_S_SIGMA = 0.0009
MODEL_NAME = "W33-Phi6-polar"


def selected_k3_bare() -> float:
    """CXLIII-selected QCD-local bare SU(3) embedding."""
    return 24.0 / PHI3


def selected_tau_gut() -> float:
    """CXLII/CXLIII-selected Phi6-polar threshold log."""
    return 0.5 * math.log(MU / PHI6)


def selected_delta_gut(alpha_unified: float | None = None) -> float:
    """One-loop GUT threshold delta = alpha/(2*pi)*tau."""
    if alpha_unified is None:
        alpha_unified = w33_alpha_unified_gut()
    return (alpha_unified / (2.0 * math.pi)) * selected_tau_gut()


def selected_k3_effective(alpha_unified: float | None = None) -> float:
    """Effective k3 after applying the selected Phi6-polar threshold."""
    if alpha_unified is None:
        alpha_unified = w33_alpha_unified_gut()
    return selected_k3_bare() / (1.0 + selected_delta_gut(alpha_unified))


def selected_alpha_s_gut(alpha_unified: float | None = None) -> float:
    """SU(3)_c MS-bar coupling at M_GUT for the selected branch."""
    if alpha_unified is None:
        alpha_unified = w33_alpha_unified_gut()
    return (alpha_unified / selected_k3_bare()) * (1.0 + selected_delta_gut(alpha_unified))


def w33_phi6_polar_alpha_s_mz(verbose: bool = True) -> Dict[str, object]:
    """Run the selected Phi6-polar branch from M_GUT to M_Z."""
    alpha_unified = w33_alpha_unified_gut()
    m_gut = w33_m_gut()
    alpha_gut = selected_alpha_s_gut(alpha_unified)

    a_top_nf6 = run_alpha_s(alpha_gut, m_gut, M_TOP, nf=6, n_steps=5000)
    if a_top_nf6 is None:
        return {
            "status": "runaway_gut_to_mtop",
            "model": MODEL_NAME,
            "alpha_s_mz": None,
            "alpha_s_gut": alpha_gut,
        }

    a_top_nf5 = threshold_match_top(a_top_nf6, M_TOP, M_TOP)
    a_mz = run_alpha_s(a_top_nf5, M_TOP, M_Z, nf=5, n_steps=2000)
    if a_mz is None:
        return {
            "status": "runaway_mtop_to_mz",
            "model": MODEL_NAME,
            "alpha_s_mz": None,
            "alpha_s_gut": alpha_gut,
        }

    residual = a_mz - PDG_ALPHA_S_MZ
    sigma = abs(residual) / PDG_ALPHA_S_SIGMA
    result = {
        "status": "ok",
        "model": MODEL_NAME,
        "alpha_unified_gut": alpha_unified,
        "k3_bare": selected_k3_bare(),
        "tau_gut": selected_tau_gut(),
        "delta_gut": selected_delta_gut(alpha_unified),
        "k3_effective": selected_k3_effective(alpha_unified),
        "alpha_s_gut": alpha_gut,
        "alpha_s_mtop_nf6": a_top_nf6,
        "alpha_s_mtop_nf5": a_top_nf5,
        "alpha_s_mz": a_mz,
        "pdg_alpha_s_mz": PDG_ALPHA_S_MZ,
        "residual": residual,
        "sigma": sigma,
        "M_GUT": m_gut,
        "M_top": M_TOP,
        "M_Z": M_Z,
    }

    if verbose:
        print("=" * 65)
        print("W(3,3) Phi6-Polar RG Pipeline")
        print("=" * 65)
        print(f"  model                = {MODEL_NAME}")
        print(f"  alpha_unified(M_GUT) = {alpha_unified:.9f}")
        print(f"  k3_bare              = {selected_k3_bare():.9f}")
        print(f"  tau_GUT              = {selected_tau_gut():+.9f}")
        print(f"  delta_GUT            = {selected_delta_gut(alpha_unified):+.9f}")
        print(f"  k3_eff               = {selected_k3_effective(alpha_unified):.9f}")
        print(f"  alpha_s(M_GUT)       = {alpha_gut:.9f}")
        print(f"  alpha_s(M_top,nf=6)  = {a_top_nf6:.9f}")
        print(f"  alpha_s(M_top,nf=5)  = {a_top_nf5:.9f}")
        print(f"  alpha_s(M_Z)         = {a_mz:.9f}")
        print(f"  PDG alpha_s(M_Z)     = {PDG_ALPHA_S_MZ:.9f}")
        print(f"  residual             = {residual:+.9e}")
        print(f"  sigma                = {sigma:.4f}")
        print("=" * 65)

    return result


def selected_phi6_polar_report() -> Dict[str, object]:
    """Compact audit report for downstream JSON/docs."""
    result = w33_phi6_polar_alpha_s_mz(verbose=False)
    return {
        "module": "scripts/w33_rg_phi6_polar_pipeline.py",
        "selected_branch": {
            "model": MODEL_NAME,
            "selection_principle": "QCD-local Phi6 sector because beta0=Phi6(3)=7",
            "k3_bare": "24/13",
            "tau_gut": "log sqrt(mu/Phi6)",
            "alpha_s_gut_formula": "alpha_unified/(24/13) * (1 + alpha_unified/(2*pi)*log sqrt(mu/Phi6))",
        },
        "result": result,
    }


if __name__ == "__main__":
    w33_phi6_polar_alpha_s_mz(verbose=True)
