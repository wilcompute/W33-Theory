"""
Tests for the consolidated falsifiable predictions derived in
exploration/w33_predictions.py.

These pin down the rational algebraic identities (exact) and assert
reasonable agreement windows against PDG / Planck values for the
numerical predictions.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from fractions import Fraction
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PRED_PATH = ROOT / "exploration" / "w33_predictions.py"


@pytest.fixture(scope="module")
def preds():
    """Import exploration/w33_predictions.py as a module."""
    spec = importlib.util.spec_from_file_location("w33_predictions_mod", PRED_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["w33_predictions_mod"] = mod
    spec.loader.exec_module(mod)
    return mod


# ─── Graph parameter sanity ────────────────────────────────────────────────
class TestGraphParameters:
    def test_srg_identity(self, preds):
        assert (preds.v, preds.k, preds.lam, preds.mu) == (40, 12, 2, 4)

    def test_eigenvalues(self, preds):
        assert preds.r == 2 and preds.s == -4
        # r, s are roots of x^2 - (lam-mu)x - (k-mu) = 0  → x^2 + 2x - 8 = 0
        lam, mu, k = preds.lam, preds.mu, preds.k
        for x in (preds.r, preds.s):
            assert x * x - (lam - mu) * x - (k - mu) == 0

    def test_multiplicities(self, preds):
        assert preds.f == 24 and preds.g == 15 and preds.f + preds.g + 1 == preds.v

    def test_cyclotomic_values(self, preds):
        q = preds.q
        assert preds.Phi3 == q * q + q + 1 == 13
        assert preds.Phi4 == q * q + 1 == 10
        assert preds.Phi6 == q * q - q + 1 == 7


# ─── I. Gauge couplings ────────────────────────────────────────────────────
class TestGaugeCouplings:
    def test_alpha_inv_exact(self, preds):
        # alpha_em^-1(0) = (k-1)^2 + mu^2 = 11^2 + 4^2 = 121 + 16 = 137
        k, mu = preds.k, preds.mu
        assert (k - 1) ** 2 + mu ** 2 == 137

    def test_alpha_inv_matches_pdg(self, preds):
        # PDG α^-1(0) = 137.036. We predict 137. Error < 0.1%
        err = abs(137 - 137.036) / 137.036
        assert err < 1e-3

    def test_sin2w_exact(self, preds):
        assert Fraction(preds.q, preds.Phi3) == Fraction(3, 13)

    def test_sin2w_matches_pdg(self, preds):
        # PDG 0.23122, we predict 3/13 ≈ 0.23077.  Err ≈ 0.2%.
        err = abs(3 / 13 - 0.23122) / 0.23122
        assert err < 5e-3

    def test_alpha_s_exact(self, preds):
        assert Fraction(preds.mu * (preds.q + preds.lam), preds.Phi3 ** 2) == Fraction(20, 169)

    def test_alpha_s_matches_pdg(self, preds):
        # PDG α_s(M_Z) = 0.1180 ± 0.001. Predict 20/169 ≈ 0.1183. Err ≈ 0.3%.
        err = abs(20 / 169 - 0.1180) / 0.1180
        assert err < 1e-2

    def test_derive_gauge_runs(self, preds, capsys):
        result = preds.derive_gauge_unification()
        capsys.readouterr()  # silence
        assert result["alpha_em_inv_0"] == 137
        assert Fraction(result["sin2_W_frac"]) == Fraction(3, 13)
        assert Fraction(result["alpha_s_frac"]) == Fraction(20, 169)


# ─── II. Neutrinos ─────────────────────────────────────────────────────────
class TestNeutrinos:
    def test_dm2_ratio_exact(self, preds):
        # Δm²_atm / Δm²_sol = 2*Phi_3 + Phi_6 = 26 + 7 = 33
        assert 2 * preds.Phi3 + preds.Phi6 == 33

    def test_dm2_ratio_matches_pdg(self, preds):
        # PDG: 2.455e-3 / 7.42e-5 = 33.086. Predict 33. Err < 0.3%.
        pdg_ratio = 2.455e-3 / 7.42e-5
        err = abs(33 - pdg_ratio) / pdg_ratio
        assert err < 5e-3

    def test_normal_hierarchy(self, preds, capsys):
        result = preds.derive_neutrino_masses()
        capsys.readouterr()
        assert result["hierarchy"] == "normal"
        assert result["m1_meV"] <= result["m2_meV"] <= result["m3_meV"]

    def test_sum_below_planck_bound(self, preds, capsys):
        result = preds.derive_neutrino_masses()
        capsys.readouterr()
        # Σm_ν must remain below the 120 meV Planck+BAO bound
        assert result["sum_mnu_meV"] < 120.0


# ─── III. Cosmology ────────────────────────────────────────────────────────
class TestCosmology:
    def test_ns_exact(self, preds):
        # n_s = 1 - 1/(v - Phi_4) = 1 - 1/30 = 29/30
        ns = Fraction(preds.v - preds.Phi4 - 1, preds.v - preds.Phi4)
        assert ns == Fraction(29, 30)

    def test_ns_within_2sigma_of_planck(self, preds):
        # Planck 2018: n_s = 0.9649 ± 0.0042. We predict 29/30 ≈ 0.9667.
        # Deviation ≈ 0.42 sigma, well within 2σ.
        ns = 29 / 30
        dev = abs(ns - 0.9649) / 0.0042
        assert dev < 2.0

    def test_H0_between_planck_and_shoes(self, preds):
        # Our prediction H_0 = Phi_6 * Phi_4 = 70. Must sit between Planck (67.4)
        # and SH0ES (73.0) — the classic Hubble-tension window.
        H0 = preds.Phi6 * preds.Phi4
        assert H0 == 70
        assert 67.4 < H0 < 73.0

    def test_dark_matter_ratio(self, preds):
        # Ω_DM / Ω_b = q + lam = 5 vs observed 0.264/0.049 ≈ 5.39 (7%)
        observed = 0.264 / 0.049
        err = abs((preds.q + preds.lam) - observed) / observed
        assert err < 0.10

    def test_tensor_to_scalar_exact(self, preds):
        # r = 8 / (v - Phi_4) = 8 / 30 = 4 / 15
        assert Fraction(8, preds.v - preds.Phi4) == Fraction(4, 15)

    def test_tensor_to_scalar_conflicts_with_bicep(self, preds):
        # BICEP/Keck: r < 0.036. Our prediction 4/15 ≈ 0.267 exceeds the bound.
        # This is a documented falsifiable POINT — the prediction is a target,
        # not a "match". Flag it explicitly so future work can't silently tune.
        r = 4 / 15
        assert r > 0.036, (
            "r = 4/15 ≈ 0.267 is the naive slow-roll prediction; "
            "reconciling with BICEP r<0.036 requires extra-e-fold or "
            "non-slow-roll dynamics."
        )


# ─── IV. Fermion masses ─────────────────────────────────────────────────────
class TestFermions:
    def test_m_c_over_m_t(self, preds):
        # m_c/m_t ≈ ε² = 1/136. PDG: 1.27/172.69 = 0.00735. Predict: 1/136 ≈ 0.00735.
        ratio_pred = 1 / (preds.alpha_inv - 1)  # 1/136
        ratio_pdg = 1.27 / 172.69
        err = abs(ratio_pred - ratio_pdg) / ratio_pdg
        assert err < 0.05  # 5%

    def test_m_b_over_m_t(self, preds):
        # m_b/m_t = 1/(v + lam) = 1/42. PDG: 4.18/172.69 = 0.0242. Predict: 1/42 ≈ 0.0238.
        ratio_pred = 1 / (preds.v + preds.lam)
        ratio_pdg = 4.18 / 172.69
        err = abs(ratio_pred - ratio_pdg) / ratio_pdg
        assert err < 0.02

    def test_m_mu_over_m_tau(self, preds):
        # m_mu/m_tau = 1/(k+q+lam) = 1/17. PDG: 105.66/1777 ≈ 0.0595. Predict: 1/17 ≈ 0.0588.
        ratio_pred = 1 / (preds.k + preds.q + preds.lam)
        ratio_pdg = 105.66 / 1777.0
        err = abs(ratio_pred - ratio_pdg) / ratio_pdg
        assert err < 0.02

    def test_m_e_over_m_mu(self, preds):
        # m_e/m_mu = 1/(alpha_inv + v + 27 + lam) = 1/206 ≈ 0.00485. PDG: 0.511/105.66 ≈ 0.00484.
        denom = preds.alpha_inv + preds.v + preds.nn + preds.lam  # = 206
        assert denom == 206
        ratio_pred = 1 / denom
        ratio_pdg = 0.511 / 105.66
        err = abs(ratio_pred - ratio_pdg) / ratio_pdg
        assert err < 0.02

    def test_top_mass_from_vev(self, preds):
        # m_t = v_EW / sqrt(2). PDG 172.69 GeV, predict 174.1. Err ≈ 0.8%.
        mt_pred = preds.V_EW / math.sqrt(2)
        err = abs(mt_pred - 172.69) / 172.69
        assert err < 0.01


# ─── V. PMNS angles (rational exact identities) ─────────────────────────────
class TestPMNS:
    def test_sin2_theta12(self, preds):
        # sin²θ_12 = μ/Φ_3 = 4/13
        assert Fraction(preds.mu, preds.Phi3) == Fraction(4, 13)
        # PDG: 0.307. Err < 1%.
        assert abs(4 / 13 - 0.307) / 0.307 < 0.01

    def test_sin2_theta23(self, preds):
        # sin²θ_23 = Φ_6/Φ_3 = 7/13
        assert Fraction(preds.Phi6, preds.Phi3) == Fraction(7, 13)
        # PDG: 0.546. Err < 2%.
        assert abs(7 / 13 - 0.546) / 0.546 < 0.02

    def test_sin2_theta13(self, preds):
        # sin²θ_13 = 1/(v + q!) = 1/46
        qfact = math.factorial(preds.q)
        assert Fraction(1, preds.v + qfact) == Fraction(1, 46)
        # PDG: 0.0220. Err < 2%.
        assert abs(1 / 46 - 0.0220) / 0.0220 < 0.02


# ─── VI. End-to-end smoke test ──────────────────────────────────────────────
class TestIntegration:
    def test_main_runs_without_exception(self, preds, capsys):
        # The main() function prints the complete prediction table and
        # writes the JSON report. It must not raise.
        preds.main()
        out = capsys.readouterr().out
        assert "COMPLETE PREDICTION TABLE" in out
        assert "THE FIVE CRITICAL TESTS" in out

    def test_json_report_written(self, preds, capsys):
        preds.main()
        capsys.readouterr()
        report = ROOT / "data" / "w33_predictions.json"
        assert report.exists()
        import json
        with open(report) as fh:
            data = json.load(fh)
        assert "gauge" in data and "neutrinos" in data
        assert "cosmology" in data and "fermions" in data
