"""Pin the q!=2q master derivation chain in exploration/w33_master_derivation.py.

Every step of the algebraic closure from the master equation q! = 2q down to
the rational Standard Model + cosmology observables is frozen here.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from math import factorial
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_master_derivation import (  # noqa: E402
    alpha_em_inv,
    cyclotomic_values,
    derive_all_observables,
    minimal_polynomial_coefficients,
    prove_q_is_unique,
    spectrum,
    srg_parameters,
)


# ----------------------------------------------------------------------
# STEP 1. q! = 2q has the unique positive-integer solution q = 3.
# ----------------------------------------------------------------------
def test_q_factorial_equals_2q_unique_in_wide_range():
    solutions = [n for n in range(1, 2001) if factorial(n) == 2 * n]
    assert solutions == [3]


def test_prove_q_returns_three():
    assert prove_q_is_unique() == 3


# ----------------------------------------------------------------------
# STEP 2. SRG parameters as exact polynomial expressions in q.
# ----------------------------------------------------------------------
def test_srg_parameters_are_40_12_2_4():
    P = srg_parameters(3)
    assert (P["v"], P["k"], P["lam"], P["mu"]) == (40, 12, 2, 4)


def test_srg_edge_line_and_euler():
    P = srg_parameters(3)
    assert P["E"] == 240
    assert P["nn"] == 27
    assert P["chi"] == 22


def test_srg_polynomial_identities():
    q = 3
    assert q * (q + 1) == 12
    assert q - 1 == 2
    assert q + 1 == 4
    assert q ** 3 == 27
    assert (q + 1) * (q ** 2 + 1) == 40


# ----------------------------------------------------------------------
# STEP 3-4. Eigenvalues and multiplicities.
# ----------------------------------------------------------------------
def test_spectrum_eigenvalues_are_two_and_minus_four():
    S = spectrum(12, 2, 4, 40)
    assert S["r"] == 2 and S["s"] == -4


def test_spectrum_multiplicities_24_and_15():
    S = spectrum(12, 2, 4, 40)
    assert S["f"] == 24 and S["g"] == 15
    assert 1 + S["f"] + S["g"] == 40


def test_trace_condition_vanishes():
    S = spectrum(12, 2, 4, 40)
    assert 12 + S["r"] * S["f"] + S["s"] * S["g"] == 0


# ----------------------------------------------------------------------
# Minimal polynomial of the adjacency matrix.
# ----------------------------------------------------------------------
def test_minimal_polynomial_is_x3_minus_10x2_minus_32x_plus_96():
    assert minimal_polynomial_coefficients(12, 2, -4) == (-10, -32, 96)


# ----------------------------------------------------------------------
# STEP 5. Cyclotomic values at q=3.
# ----------------------------------------------------------------------
def test_cyclotomic_values_13_10_7():
    C = cyclotomic_values(3)
    assert (C["Phi3"], C["Phi4"], C["Phi6"]) == (13, 10, 7)


# ----------------------------------------------------------------------
# STEP 6. Electromagnetism identity.
# ----------------------------------------------------------------------
def test_alpha_em_inverse_is_137():
    assert alpha_em_inv(12, 4) == 137


# ----------------------------------------------------------------------
# STEP 7. Full closure surface — every Fraction is pinned.
# ----------------------------------------------------------------------
@pytest.fixture(scope="module")
def chain():
    return derive_all_observables()


EXPECTED_CLOSURES = {
    # --- Gauge ---
    "alpha_em_inv_0":        "137",
    "sin2_theta_W":          "3/13",
    "cos2_theta_W":          "10/13",
    "tan2_theta_W":          "3/10",
    "M_W2_over_M_Z2":        "10/13",
    "alpha_s_M_Z":           "20/169",
    "lambda_H":              "7/54",
    # --- Structural integers ---
    "N_colors":              "3",
    "N_generations":         "3",
    "N_SM_gauge_bosons":     "12",
    "N_Higgs_scalar_dof":    "4",
    # --- CKM ---
    "sin_theta_C":           "9/40",
    "V_cb":                  "1/25",
    # --- PMNS ---
    "sin2_theta12_PMNS":     "4/13",
    "sin2_theta23_PMNS":     "7/13",
    "sin2_theta13_PMNS":     "1/46",
    # --- Neutrino ---
    "dm2_atm_over_dm2_sol":  "33",
    # --- Charged-lepton / quark tower ---
    "m_c_over_m_t":          "1/136",
    "m_u_over_m_c":          "1/600",
    "m_b_over_m_t":           "1/42",
    "m_s_over_m_b":          "3/136",
    "m_d_over_m_s":           "1/20",
    "m_tau_over_m_t":         "1/98",
    "m_mu_over_m_tau":        "1/17",
    "m_e_over_m_mu":         "1/206",
    # --- Proton / electron ---
    "m_p_over_m_e":          "1836",
    # --- Cosmology ---
    "N_starobinsky":         "60",
    "n_s":                   "29/30",
    "r_tensor":              "1/300",
    "H0_km_s_Mpc":           "70",
    "Omega_DM":              "4/15",
    "Omega_b":               "1/20",
    "Omega_DM_over_Omega_b": "16/3",
    "Omega_Lambda":          "41/60",
    "T_CMB_K":               "11/4",
}


@pytest.mark.parametrize("name,expected", sorted(EXPECTED_CLOSURES.items()))
def test_closure_is_exact_fraction(chain, name, expected):
    assert chain["closures_as_fractions"][name] == expected


def test_all_expected_closures_present(chain):
    present = set(chain["closures_as_fractions"].keys())
    assert set(EXPECTED_CLOSURES).issubset(present)


def test_cosmology_density_budget_sums_to_unity(chain):
    sanity = chain["cosmology_sanity"]
    assert sanity["Omega_m_plus_Omega_Lambda"] == "1"
    assert sanity["is_unity"] is True


def test_weinberg_identity_sin2_plus_cos2_equals_one(chain):
    # sin^2(theta_W) + cos^2(theta_W) = q/Phi_3 + Phi_4/Phi_3
    #                                  = (q + q^2 + 1)/Phi_3 = Phi_3/Phi_3 = 1.
    wsanity = chain["weinberg_sanity"]
    assert wsanity["sin2_plus_cos2"] == "1"
    assert wsanity["is_unity"] is True


def test_M_W_over_M_Z_is_cos_theta_W(chain):
    fr = chain["closures_as_fractions"]
    assert fr["M_W2_over_M_Z2"] == fr["cos2_theta_W"]


def test_tan2_equals_sin2_over_cos2(chain):
    fr = chain["closures_as_fractions"]
    from fractions import Fraction as F
    assert F(fr["tan2_theta_W"]) == F(fr["sin2_theta_W"]) / F(fr["cos2_theta_W"])


def test_omega_m_fraction_is_19_over_60(chain):
    sanity = chain["cosmology_sanity"]
    assert sanity["Omega_m_fraction"] == str(Fraction(19, 60))


def test_master_equation_and_q_stamped(chain):
    assert chain["master_equation"] == "q! = 2 q"
    assert chain["q"] == 3


def test_minimal_polynomial_string(chain):
    assert chain["minimal_polynomial"] == "x^3 - 10 x^2 - 32 x + 96"


# ----------------------------------------------------------------------
# The closures must be algebraically consistent: decimals match fractions.
# ----------------------------------------------------------------------
def test_decimals_match_fractions(chain):
    fr = chain["closures_as_fractions"]
    dc = chain["closures_as_decimals"]
    assert set(fr) == set(dc)
    for name, frac_str in fr.items():
        assert float(Fraction(frac_str)) == pytest.approx(dc[name])


# ----------------------------------------------------------------------
# Spot-check two well-known identities: alpha^-1 = (k-1)^2 + mu^2 = 137
# and m_p/m_e = v^2 + E - mu.
# ----------------------------------------------------------------------
def test_alpha_from_spectral_identity():
    assert (12 - 1) ** 2 + 4 ** 2 == 137


def test_proton_electron_identity():
    v, E, mu = 40, 240, 4
    assert v ** 2 + E - mu == 1836
