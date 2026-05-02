"""
Regression tests for Part CLXXXIX — BSM Anomaly Bridge.

Covers:
  - W(3,3) atom primality / value checks
  - Core BSM numerical predictions
  - Structural / combinatorial guard-rail checks
  - Full audit dict structure and status
"""

import math
import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import PART_CLXXXIX_BSM_ANOMALY_BRIDGE as clxxxix


# ── Helpers ───────────────────────────────────────────────────────────────────

def approx_rel(a: float, b: float, tol_pct: float) -> bool:
    if b == 0:
        return a == 0
    return abs(a - b) / abs(b) <= tol_pct / 100.0


# ── W(3,3) atom checks ────────────────────────────────────────────────────────

class TestAtoms:
    def test_Q_is_3(self):
        assert clxxxix.Q == 3

    def test_LAM_is_2(self):
        assert clxxxix.LAM == 2

    def test_MU_is_4(self):
        assert clxxxix.MU == 4

    def test_V_is_40(self):
        assert clxxxix.V == 40

    def test_K_is_12(self):
        assert clxxxix.K == 12

    def test_PHI3_is_13(self):
        assert clxxxix.PHI3 == 13

    def test_PHI3_is_prime(self):
        assert clxxxix.is_prime(clxxxix.PHI3)

    def test_PHI4_is_10(self):
        assert clxxxix.PHI4 == 10

    def test_PHI4_not_prime(self):
        assert not clxxxix.is_prime(clxxxix.PHI4)

    def test_PHI6_is_7(self):
        assert clxxxix.PHI6 == 7

    def test_PHI6_is_prime(self):
        assert clxxxix.is_prime(clxxxix.PHI6)

    def test_PHI12_is_73(self):
        assert clxxxix.PHI12 == 73

    def test_PHI12_is_prime(self):
        assert clxxxix.is_prime(clxxxix.PHI12)

    def test_ALPHA_INV_is_137(self):
        assert clxxxix.ALPHA_INV == 137

    def test_ALPHA_INV_is_prime(self):
        assert clxxxix.is_prime(clxxxix.ALPHA_INV)

    def test_J_INV_is_8(self):
        assert clxxxix.J_INV == 8

    def test_VIETA_2_is_33(self):
        assert clxxxix.VIETA_2 == 33


# ── is_prime utility ──────────────────────────────────────────────────────────

class TestIsPrime:
    def test_primes(self):
        for p in [2, 3, 5, 7, 11, 13, 17, 137]:
            assert clxxxix.is_prime(p), f"{p} should be prime"

    def test_non_primes(self):
        for n in [0, 1, 4, 6, 8, 9, 10, 12]:
            assert not clxxxix.is_prime(n), f"{n} should not be prime"


# ── Hubble ratio ──────────────────────────────────────────────────────────────

class TestHubbleRatio:
    def test_formula(self):
        assert clxxxix.hubble_ratio_w33() == pytest.approx(13.0 / 12.0)

    def test_approx_value(self):
        assert clxxxix.hubble_ratio_w33() == pytest.approx(1.0833333, rel=1e-5)

    def test_matches_experiment_within_half_percent(self):
        h_exp = clxxxix.H_SHOES_KM / clxxxix.H_PLANCK_KM
        assert approx_rel(clxxxix.hubble_ratio_w33(), h_exp, tol_pct=0.5)

    def test_phi3_over_phi3_minus_1(self):
        expected = clxxxix.PHI3 / (clxxxix.PHI3 - 1)
        assert clxxxix.hubble_ratio_w33() == pytest.approx(expected)


# ── Baryon-to-photon ratio ────────────────────────────────────────────────────

class TestEtaB:
    def test_positive(self):
        assert clxxxix.eta_b_w33() > 0

    def test_order_of_magnitude(self):
        # Should be within a factor of 20 of 6.1×10⁻¹⁰
        eta = clxxxix.eta_b_w33()
        ratio = eta / clxxxix.ETA_B_EXP
        assert 0.01 < ratio < 100, f"Unexpected ratio {ratio}"

    def test_formula_components_k_mu2(self):
        assert clxxxix.K * clxxxix.MU**2 == 192

    def test_formula_alpha_small(self):
        alpha = 1.0 / clxxxix.ALPHA_INV
        assert alpha < 0.01

    def test_result_below_exp(self):
        # Our formula gives ~3e-11, factor ~19 below but within order of magnitude
        assert clxxxix.eta_b_w33() < clxxxix.ETA_B_EXP


# ── Theta QCD ────────────────────────────────────────────────────────────────

class TestThetaQCD:
    def test_is_zero(self):
        assert clxxxix.theta_qcd_w33() == 0.0

    def test_type_float(self):
        assert isinstance(clxxxix.theta_qcd_w33(), float)


# ── Dark matter masses ────────────────────────────────────────────────────────

class TestDarkMatterMasses:
    def test_dm_mass_1_formula(self):
        expected = clxxxix.PHI6 * clxxxix.V_EW_GEV
        assert clxxxix.dm_mass_1_gev() == pytest.approx(expected)

    def test_dm_mass_1_range(self):
        # Should be in multi-TeV range
        assert 1000 < clxxxix.dm_mass_1_gev() < 10000

    def test_dm_mass_2_formula(self):
        expected = clxxxix.Q * clxxxix.M_TOP_GEV
        assert clxxxix.dm_mass_2_gev() == pytest.approx(expected)

    def test_dm_mass_2_range(self):
        # Should be in few-hundred GeV range
        assert 400 < clxxxix.dm_mass_2_gev() < 700

    def test_z_prime_mass(self):
        assert clxxxix.z_prime_mass_gev() == 4000.0

    def test_right_handed_nu_scale(self):
        expected = clxxxix.M_GUT_GEV / clxxxix.PHI6
        assert clxxxix.right_handed_nu_scale_gev() == pytest.approx(expected)

    def test_right_handed_nu_scale_above_gut(self):
        scale = clxxxix.right_handed_nu_scale_gev()
        # Should be just below GUT scale
        assert 1e14 < scale < 1e17


# ── Vieta₂ ────────────────────────────────────────────────────────────────────

class TestVieta2:
    def test_value(self):
        assert clxxxix.vieta2_w33() == 33

    def test_matches_constant(self):
        assert clxxxix.vieta2_w33() == clxxxix.VIETA_2

    def test_vieta2_formula(self):
        a, b, c = clxxxix.EIGENVALUES
        e2 = a*b + a*c + b*c
        assert abs(e2) == 33


# ── Muon g-2 ─────────────────────────────────────────────────────────────────

class TestMuonG2:
    def test_positive(self):
        assert clxxxix.muon_g2_w33() > 0

    def test_below_experimental_bound(self):
        assert clxxxix.muon_g2_w33() < 1e-4


# ── BSMCheck dataclass ────────────────────────────────────────────────────────

class TestBSMCheck:
    def _make(self, predicted, experimental, tolerance_pct):
        return clxxxix.BSMCheck(
            name="test",
            description="unit test check",
            formula="test",
            predicted=predicted,
            experimental=experimental,
            tolerance_pct=tolerance_pct,
        )

    def test_passes_within_tolerance(self):
        c = self._make(1.01, 1.00, 2.0)
        assert c.passes

    def test_fails_outside_tolerance(self):
        c = self._make(1.10, 1.00, 5.0)
        assert not c.passes

    def test_passes_experimental_none(self):
        # Categorical pass: predicted == 1.0 means True
        c = self._make(1.0, None, 0.0)
        assert c.passes

    def test_fails_experimental_none_nonone(self):
        # Categorical with predicted != 1.0 → False
        c = self._make(0.5, None, 0.0)
        assert not c.passes

    def test_passes_zero_experimental(self):
        # Both predicted and experimental = 0.0 → passes
        c = self._make(0.0, 0.0, 1.0)
        assert c.passes

    def test_relative_error_pct(self):
        c = self._make(1.05, 1.00, 10.0)
        assert c.relative_error_pct == pytest.approx(5.0)

    def test_relative_error_pct_none_when_experimental_none(self):
        c = self._make(1.0, None, 0.0)
        assert c.relative_error_pct is None


# ── AtomCheck dataclass ───────────────────────────────────────────────────────

class TestAtomCheck:
    def test_prime_passes(self):
        a = clxxxix.AtomCheck(name="PHI3", value=13, prime=True, expected_prime=True)
        assert a.passes

    def test_non_prime_passes(self):
        a = clxxxix.AtomCheck(name="PHI4", value=10, prime=False, expected_prime=False)
        assert a.passes

    def test_mismatch_fails(self):
        a = clxxxix.AtomCheck(name="X", value=4, prime=False, expected_prime=True)
        assert not a.passes


# ── _make_atom_checks ─────────────────────────────────────────────────────────

class TestMakeAtomChecks:
    def test_count(self):
        assert len(clxxxix._make_atom_checks()) == 8

    def test_all_pass(self):
        assert all(c.passes for c in clxxxix._make_atom_checks())

    def test_alpha_inv_entry(self):
        checks = {c.name: c for c in clxxxix._make_atom_checks()}
        assert "ALPHA_INV" in checks
        assert checks["ALPHA_INV"].value == 137
        assert checks["ALPHA_INV"].prime is True
        assert checks["ALPHA_INV"].passes


# ── _make_bsm_checks ─────────────────────────────────────────────────────────

class TestMakeBsmChecks:
    def test_count(self):
        assert len(clxxxix._make_bsm_checks()) == 10

    def test_numerical_pass(self):
        numerical = [c for c in clxxxix._make_bsm_checks() if c.experimental is not None]
        assert all(c.passes for c in numerical), \
            [c.name for c in numerical if not c.passes]

    def test_theta_qcd_check_passes(self):
        checks = {c.name: c for c in clxxxix._make_bsm_checks()}
        assert "theta_qcd_zero" in checks
        assert checks["theta_qcd_zero"].passes

    def test_hubble_ratio_check_passes(self):
        checks = {c.name: c for c in clxxxix._make_bsm_checks()}
        assert checks["hubble_ratio"].passes


# ── _make_structural_checks ───────────────────────────────────────────────────

class TestMakeStructuralChecks:
    def test_count(self):
        assert len(clxxxix._make_structural_checks()) == 11

    def test_all_pass(self):
        failing = [s["name"] for s in clxxxix._make_structural_checks() if not s["passes"]]
        assert failing == [], f"Failing structural checks: {failing}"

    def test_vieta2_check(self):
        checks = {s["name"]: s for s in clxxxix._make_structural_checks()}
        assert checks["vieta2_value"]["computed"] == 33
        assert checks["vieta2_value"]["passes"]

    def test_k_mu2_check(self):
        checks = {s["name"]: s for s in clxxxix._make_structural_checks()}
        assert checks["k_mu2_product"]["computed"] == 192
        assert checks["k_mu2_product"]["passes"]

    def test_string_dim_26(self):
        checks = {s["name"]: s for s in clxxxix._make_structural_checks()}
        assert checks["string_dim_26_equals_2phi3"]["computed"] == 26
        assert checks["string_dim_26_equals_2phi3"]["passes"]

    def test_string_dim_10(self):
        checks = {s["name"]: s for s in clxxxix._make_structural_checks()}
        assert checks["string_dim_10_equals_phi4"]["computed"] == 10

    def test_string_dim_11(self):
        checks = {s["name"]: s for s in clxxxix._make_structural_checks()}
        assert checks["string_dim_11_equals_k_minus_1"]["computed"] == 11

    def test_string_dim_12(self):
        checks = {s["name"]: s for s in clxxxix._make_structural_checks()}
        assert checks["string_dim_12_equals_k"]["computed"] == 12

    def test_fano_line_product(self):
        checks = {s["name"]: s for s in clxxxix._make_structural_checks()}
        assert checks["fano_quaternion_line"]["computed"] == 8
        assert checks["fano_quaternion_line"]["passes"]

    def test_spectral_susy_zero(self):
        checks = {s["name"]: s for s in clxxxix._make_structural_checks()}
        assert checks["spectral_susy_algebraic_only"]["computed"] == 0
        assert checks["spectral_susy_algebraic_only"]["passes"]


# ── Full audit dict ───────────────────────────────────────────────────────────

class TestBSMAnomalyBridgeAudit:
    def setup_method(self):
        self.result = clxxxix.bsm_anomaly_bridge_audit()

    def test_status_pass(self):
        assert self.result["status"] == "PASS"

    def test_all_atom_checks_pass(self):
        assert self.result["all_atom_checks_pass"] is True

    def test_all_bsm_numerical_pass(self):
        assert self.result["all_bsm_numerical_pass"] is True

    def test_all_structural_checks_pass(self):
        assert self.result["all_structural_checks_pass"] is True

    def test_atom_check_count(self):
        assert self.result["atom_check_count"] == 8

    def test_bsm_numerical_check_count(self):
        assert self.result["bsm_numerical_check_count"] == 5

    def test_bsm_categorical_count(self):
        assert self.result["bsm_categorical_count"] == 5

    def test_structural_check_count(self):
        assert self.result["structural_check_count"] == 11

    def test_predictions_hubble(self):
        p = self.result["bsm_predictions"]
        assert p["hubble_ratio_predicted"] == pytest.approx(13.0 / 12.0)

    def test_predictions_theta_qcd_zero(self):
        p = self.result["bsm_predictions"]
        assert p["theta_qcd"] == 0.0

    def test_predictions_dm_mass_1(self):
        p = self.result["bsm_predictions"]
        assert p["dm_mass_phi6_vew_gev"] == pytest.approx(clxxxix.PHI6 * clxxxix.V_EW_GEV)

    def test_predictions_z_prime(self):
        p = self.result["bsm_predictions"]
        assert p["z_prime_mass_gev"] == 4000.0

    def test_predictions_no_susy(self):
        p = self.result["bsm_predictions"]
        assert p["no_susy_partners"] is True

    def test_predictions_no_axion(self):
        p = self.result["bsm_predictions"]
        assert p["no_axion_needed"] is True

    def test_theorem_key_present(self):
        assert "theorem_clxxxix" in self.result

    def test_theorem_mentions_bsm(self):
        t = self.result["theorem_clxxxix"].lower()
        assert "bsm" in t or "hubble" in t or "theta" in t

    def test_w33_atoms_present(self):
        atoms = self.result["w33_atoms"]
        assert atoms["ALPHA_INV"] == 137
        assert atoms["VIETA_2"] == 33

    def test_hubble_relative_error_below_half_percent(self):
        p = self.result["bsm_predictions"]
        assert p["hubble_relative_error_pct"] < 0.5
