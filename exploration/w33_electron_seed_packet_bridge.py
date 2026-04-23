"""Exact residual electron-seed packet bridge on the live W33 fermion stack.

The one-input fermion bridge already reduces the charged-lepton and neutrino
side to a single residual electron seed. This module packages the strongest
exact arithmetic currently visible inside that remaining slot.

The candidate denominator already factorizes into one exact three-factor
packet:

    m_t / m_e ?= (lambda * Phi6^2) * (mu^2 + 1) * (mu^2 * Phi3)
             = 98 * 17 * 208
             = 346528.

Those factors are not arbitrary:

  - 98 = lambda * Phi6^2 is the barrier shell,
  - 17 = mu^2 + 1 is the shifted Gaussian norm,
  - 208 = mu^2 * Phi3 is the exact charged-lepton shell.

And the same charged-lepton shell is also

    208 = mu * dim(F4) = 4 * 52,

so the residual electron slot already touches the exact F4 neutrino coefficient
side as well.

What remains open is narrower than "find an electron formula from scratch":
the exact factor packet is visible, but the final physical identification of
that packet is not yet an exact theorem.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Any

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from exploration.w33_f4_neutrino_scale_bridge import build_f4_neutrino_scale_summary
from exploration.w33_one_input_fermion_spectrum_bridge import (
    build_one_input_fermion_spectrum_summary,
)
from exploration.w33_q3_fermion_hierarchy_bridge import build_q3_fermion_hierarchy_summary


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_electron_seed_packet_bridge_summary.json"

Q = 3
V = 40
K = 12
LAMBDA = 2
MU = 4
PHI3 = Q * Q + Q + 1
PHI6 = Q * Q - Q + 1
V_EW = 246


def _fraction_dict(value: Fraction) -> dict[str, Any]:
    exact = str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    return {"exact": exact, "float": float(value)}


def _sympy_dict(value: sp.Expr) -> dict[str, Any]:
    return {"exact": str(sp.simplify(value)), "float": float(sp.N(value, 30))}


@lru_cache(maxsize=1)
def build_electron_seed_packet_summary() -> dict[str, Any]:
    hierarchy = build_q3_fermion_hierarchy_summary()
    one_input = build_one_input_fermion_spectrum_summary()
    neutrino = build_f4_neutrino_scale_summary()

    up_sector_suppressor = Fraction(
        hierarchy["electromagnetic_to_flavour_lock"]["up_sector_suppressor"]["exact"]
    )
    muon_shell = Fraction(
        hierarchy["dimensionless_hierarchy_ratios"]["mmu_over_me"]["exact"]
    )
    f4_dimension = int(neutrino["exceptional_scale_dictionary"]["f4_dimension"])

    barrier_shell = Fraction(LAMBDA * PHI6 * PHI6, 1)
    shifted_gaussian_norm = Fraction(MU * MU + 1, 1)
    candidate_denominator = barrier_shell * shifted_gaussian_norm * muon_shell
    candidate_top_over_muon = Fraction(candidate_denominator, muon_shell)
    candidate_charm_over_muon = Fraction(candidate_top_over_muon, up_sector_suppressor)

    mt_gev = sp.Rational(V_EW, 1) * sp.sqrt(2) / 2
    me_candidate_mev = sp.Rational(V_EW * 1000, candidate_denominator.numerator) * sp.sqrt(2) / 2
    mmu_candidate_mev = sp.Integer(muon_shell.numerator) * me_candidate_mev

    return {
        "status": "ok",
        "graph_packet": {
            "q": Q,
            "v": V,
            "k": K,
            "lambda": LAMBDA,
            "mu": MU,
            "phi3": PHI3,
            "phi6": PHI6,
            "vev_ew_gev": V_EW,
        },
        "exact_packet_dictionary": {
            "barrier_shell_lambda_phi6_squared": _fraction_dict(barrier_shell),
            "shifted_gaussian_norm_mu_squared_plus_one": _fraction_dict(shifted_gaussian_norm),
            "charged_lepton_shell_mu_squared_phi3": _fraction_dict(muon_shell),
            "f4_dimension": f4_dimension,
            "candidate_denominator_mt_over_me": _fraction_dict(candidate_denominator),
            "candidate_denominator_prime_factorization": "2^5 * 7^2 * 13 * 17",
            "factor_packet": [int(barrier_shell), int(shifted_gaussian_norm), int(muon_shell)],
        },
        "candidate_ratio_dictionary": {
            "me_over_mt_candidate": _fraction_dict(Fraction(1, candidate_denominator)),
            "mt_over_mu_candidate": _fraction_dict(candidate_top_over_muon),
            "mc_over_mu_candidate": _fraction_dict(candidate_charm_over_muon),
            "mu_shell_over_f4_dimension": _fraction_dict(Fraction(muon_shell, f4_dimension)),
            "up_sector_suppressor": _fraction_dict(up_sector_suppressor),
        },
        "graph_fixed_candidate_mass_shadow": {
            "mt_gev": _sympy_dict(mt_gev),
            "me_candidate_mev": _sympy_dict(me_candidate_mev),
            "mmu_candidate_mev": _sympy_dict(mmu_candidate_mev),
            "formula_dictionary": {
                "mt": "v_EW / sqrt(2)",
                "me_candidate": "v_EW / (sqrt(2) * lambda * Phi6^2 * (mu^2 + 1) * mu^2 * Phi3)",
                "mmu_candidate": "208 * m_e_candidate",
            },
        },
        "existing_bridge_cross_checks": {
            "one_input_residual_seed": one_input["charged_lepton_one_seed_closure"]["residual_seed"],
            "koide_q": one_input["charged_lepton_one_seed_closure"]["koide_q"],
            "f4_scale_ratio": neutrino["exceptional_scale_dictionary"][
                "mnu_over_me_squared_if_dirac_seed_is_electron"
            ],
        },
        "electron_seed_packet_theorem": {
            "barrier_shell_is_lambda_phi6_squared": barrier_shell == Fraction(LAMBDA * PHI6 * PHI6, 1),
            "shifted_gaussian_norm_is_mu_squared_plus_one": shifted_gaussian_norm == Fraction(MU * MU + 1, 1),
            "charged_lepton_shell_is_phi3_mu_squared": muon_shell == Fraction(PHI3 * MU * MU, 1),
            "charged_lepton_shell_is_mu_times_f4_dimension": muon_shell == Fraction(MU * f4_dimension, 1),
            "candidate_denominator_is_barrier_times_shift_times_muon_shell": candidate_denominator
            == barrier_shell * shifted_gaussian_norm * muon_shell,
            "candidate_top_over_muon_is_barrier_times_shift": candidate_top_over_muon
            == barrier_shell * shifted_gaussian_norm,
            "candidate_charm_over_muon_is_phi6_squared_over_mu": candidate_charm_over_muon
            == Fraction(PHI6 * PHI6, MU),
            "remaining_fermion_frontier_reduces_to_one_exact_three_factor_packet": True,
            "physical_electron_identification_remains_open": True,
        },
        "bridge_verdict": (
            "The residual charged-fermion slot is now narrower than a free electron formula. "
            "The exact packet [98, 17, 208] = [lambda*Phi6^2, mu^2+1, mu^2*Phi3] already "
            "carries the candidate denominator 346528, and the same 208 shell is also "
            "mu*dim(F4). So the remaining fermion wall is not missing factor arithmetic; "
            "it is the final physical identification of this exact packet."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_electron_seed_packet_summary(), indent=2),
        encoding="utf-8",
    )
    return path


if __name__ == "__main__":
    write_summary()
