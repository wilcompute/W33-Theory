"""Tests for PART CCCCXIX -- W33 Photonic Harmonic TQC Geometric Synthesis.

Tests verify all 27 bridge checks and the synthesis architecture identities
that unify the Lovász orthonormal labeling with the photonic harmonic TQC bus.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

from exploration.PART_CCCCXIX_PHOTONIC_HARMONIC_TQC_SYNTHESIS import (
    # geometry-qutrit alignment
    labeling_dimension,
    theta_equals_alpha_value,
    complement_theta_equals_mu,
    shannon_capacity_equals_V,
    gram_matrix_rank,
    labeling_sphere_dim,
    # denominator alignment
    klm_denominator,
    fusion_denominator,
    denominator_equals_complement_theta,
    denominator_equals_toric_gsd,
    fractional_chromatic_equals_V_over_theta,
    # harmonic shell geometry
    heawood_middle_shell,
    heawood_branch_size,
    heawood_two_branch_total,
    heawood_cycle_rank,
    heawood_vertex_count,
    csaszar_euler_char,
    # TQC protection stack
    logical_sector,
    base_css_code,
    q4_routing_code,
    active_protection_code,
    selector_trits,
    controller_bits,
    # grand synthesis
    synthesis_layers,
    sm_crosswalk,
    verify_all,
    build_ccccxix_summary,
    # constants
    Q, LAM, MU, K, V, E, H1, PHI6, ALPHA, CHI,
    TORIC_GSD, TORIC_LOGICAL_QUBITS, TORIC_GENUS,
)


# ─── Constants ────────────────────────────────────────────────────────────────
class TestConstants:
    """Verify that all fundamental W(3,3) constants are correct."""

    def test_q_is_3(self):
        assert Q == 3

    def test_lambda_is_2(self):
        assert LAM == 2

    def test_mu_is_4(self):
        assert MU == 4

    def test_K_is_12(self):
        assert K == 12

    def test_V_is_40(self):
        assert V == 40

    def test_E_is_240(self):
        assert E == 240

    def test_H1_is_81(self):
        assert H1 == 81

    def test_PHI6_is_7(self):
        assert PHI6 == 7

    def test_alpha_is_10(self):
        assert ALPHA == 10

    def test_chi_is_4(self):
        assert CHI == 4

    def test_toric_gsd_is_4(self):
        assert TORIC_GSD == 4

    def test_toric_logical_qubits_is_2(self):
        assert TORIC_LOGICAL_QUBITS == 2

    def test_toric_genus_is_1(self):
        assert TORIC_GENUS == 1


# ─── Geometry-qutrit alignment ────────────────────────────────────────────────
class TestGeometryQutritAlignment:
    """Test that the Lovász labeling geometric quantities match qutrit parameters."""

    def test_labeling_dimension_is_q(self):
        assert labeling_dimension() == Q

    def test_labeling_dimension_is_3(self):
        assert labeling_dimension() == 3

    def test_theta_equals_alpha(self):
        assert theta_equals_alpha_value() == ALPHA

    def test_theta_is_10(self):
        assert theta_equals_alpha_value() == 10

    def test_complement_theta_is_mu(self):
        assert complement_theta_equals_mu() == MU

    def test_complement_theta_is_4(self):
        assert complement_theta_equals_mu() == 4

    def test_shannon_capacity_is_V(self):
        assert shannon_capacity_equals_V() == V

    def test_shannon_capacity_is_40(self):
        assert shannon_capacity_equals_V() == 40

    def test_gram_matrix_rank_is_q(self):
        assert gram_matrix_rank() == Q

    def test_gram_matrix_rank_is_3(self):
        assert gram_matrix_rank() == 3

    def test_labeling_sphere_is_S2(self):
        assert labeling_sphere_dim() == 2

    def test_labeling_sphere_dim_is_q_minus_1(self):
        assert labeling_sphere_dim() == Q - 1

    def test_theta_times_complement_theta_is_V(self):
        assert theta_equals_alpha_value() * complement_theta_equals_mu() == V


# ─── Denominator alignment ────────────────────────────────────────────────────
class TestDenominatorAlignment:
    """Test that all TQC denominators match geometric theta values."""

    def test_klm_denominator_is_mu(self):
        assert klm_denominator() == MU

    def test_klm_denominator_is_4(self):
        assert klm_denominator() == 4

    def test_fusion_denominator_is_lambda(self):
        assert fusion_denominator() == LAM

    def test_fusion_denominator_is_2(self):
        assert fusion_denominator() == 2

    def test_klm_equals_complement_theta(self):
        assert denominator_equals_complement_theta()

    def test_klm_equals_toric_gsd(self):
        assert denominator_equals_toric_gsd()

    def test_fractional_chromatic_tight(self):
        assert fractional_chromatic_equals_V_over_theta()

    def test_klm_product_with_theta_G_equals_V(self):
        assert klm_denominator() * theta_equals_alpha_value() == V

    def test_fusion_times_klm_equals_chi_times_lambda(self):
        # fusion_denom * klm_denom = 2 * 4 = 8 = 2^q
        assert fusion_denominator() * klm_denominator() == 2**Q


# ─── Harmonic shell geometry ──────────────────────────────────────────────────
class TestHarmonicShellGeometry:
    """Test the Heawood oscillator and Csaszar torus geometry."""

    def test_heawood_middle_shell_is_K(self):
        assert heawood_middle_shell() == K

    def test_heawood_middle_shell_is_12(self):
        assert heawood_middle_shell() == 12

    def test_heawood_branch_size_is_q_factorial(self):
        assert heawood_branch_size() == math.factorial(Q)

    def test_heawood_branch_size_is_6(self):
        assert heawood_branch_size() == 6

    def test_heawood_two_branch_total_is_K(self):
        assert heawood_two_branch_total() == K

    def test_heawood_two_branch_total_is_12(self):
        assert heawood_two_branch_total() == 12

    def test_heawood_cycle_rank_is_2_pow_q(self):
        assert heawood_cycle_rank() == 2**Q

    def test_heawood_cycle_rank_is_8(self):
        assert heawood_cycle_rank() == 8

    def test_heawood_vertex_count_is_2_phi6(self):
        assert heawood_vertex_count() == 2 * PHI6

    def test_heawood_vertex_count_is_14(self):
        assert heawood_vertex_count() == 14

    def test_csaszar_euler_characteristic_is_zero(self):
        assert csaszar_euler_char() == 0

    def test_heawood_shell_is_3_times_mu(self):
        assert heawood_middle_shell() == 3 * MU


# ─── TQC protection stack ─────────────────────────────────────────────────────
class TestTQCProtectionStack:
    """Test the QEC CSS code parameters and classical selector."""

    def test_logical_sector_is_q4(self):
        assert logical_sector() == Q**4

    def test_logical_sector_is_81(self):
        assert logical_sector() == 81

    def test_base_css_code_format(self):
        code = base_css_code()
        assert code.startswith("[[")
        assert "240" in code
        assert "81" in code
        assert "3" in code

    def test_base_css_code_exact(self):
        assert base_css_code() == "[[240,81,3]]"

    def test_q4_routing_code(self):
        assert q4_routing_code() == "[[1296,81,4]]"

    def test_active_protection_code(self):
        assert active_protection_code() == "[[82320,81,>=81]]"

    def test_selector_trits_is_V(self):
        assert selector_trits() == V

    def test_selector_trits_is_40(self):
        assert selector_trits() == 40

    def test_controller_bits_is_64(self):
        assert controller_bits() == 64

    def test_3_pow_V_fits_in_64_bits(self):
        # 3^40 = 12157665459056928801
        val = 3**V
        assert 2**63 < val < 2**64


# ─── Grand synthesis architecture ────────────────────────────────────────────
class TestSynthesisLayers:
    """Test the five synthesis layers structure."""

    def test_five_layers(self):
        assert len(synthesis_layers()) == 5

    def test_layer_names(self):
        names = [layer["name"] for layer in synthesis_layers()]
        assert "geometric_carrier" in names
        assert "harmonic_oscillator" in names
        assert "toric_loop_memory" in names
        assert "protected_qec" in names
        assert "classical_selector" in names

    def test_layers_have_geometry_field(self):
        for layer in synthesis_layers():
            assert "geometry" in layer

    def test_layers_have_tqc_field(self):
        for layer in synthesis_layers():
            assert "tqc" in layer

    def test_layers_have_invariant_field(self):
        for layer in synthesis_layers():
            assert "invariant" in layer

    def test_geometric_carrier_invariant(self):
        layer = synthesis_layers()[0]
        assert str(Q) in layer["invariant"]

    def test_classical_selector_invariant(self):
        layer = synthesis_layers()[-1]
        assert str(V) in layer["invariant"]


# ─── SM crosswalk ─────────────────────────────────────────────────────────────
class TestSMCrosswalk:
    """Test the Standard Model crosswalk entries."""

    def test_seven_entries(self):
        assert len(sm_crosswalk()) == 7

    def test_lovasz_dim_entry(self):
        cw = sm_crosswalk()
        assert "lovasz_dim_equals_q" in cw
        assert "3" in cw["lovasz_dim_equals_q"]

    def test_theta_complement_entry(self):
        cw = sm_crosswalk()
        assert "theta_complement_equals_mu" in cw
        assert "4" in cw["theta_complement_equals_mu"]

    def test_shannon_capacity_entry(self):
        cw = sm_crosswalk()
        assert "shannon_capacity_V" in cw
        assert "40" in cw["shannon_capacity_V"]

    def test_chi_alpha_entry(self):
        cw = sm_crosswalk()
        assert "chi_alpha_product_V" in cw
        assert "40" in cw["chi_alpha_product_V"]

    def test_gram_matrix_entry(self):
        cw = sm_crosswalk()
        assert "gram_matrix_irreducible_3D" in cw

    def test_klm_toric_entry(self):
        cw = sm_crosswalk()
        assert "klm_toric_denominator_unification" in cw

    def test_heawood_entry(self):
        cw = sm_crosswalk()
        assert "heawood_shell_equals_degree" in cw


# ─── verify_all ───────────────────────────────────────────────────────────────
class TestVerifyAll:
    """Test that all 27 synthesis checks pass."""

    @pytest.fixture(scope="class")
    def results(self):
        checks, passed, total = verify_all()
        return checks, passed, total

    def test_total_checks_27(self, results):
        _, _, total = results
        assert total == 27

    def test_all_checks_pass(self, results):
        checks, passed, total = results
        failed = [name for name, ok in checks if not ok]
        assert failed == [], f"Failed checks: {failed}"

    def test_passed_equals_total(self, results):
        _, passed, total = results
        assert passed == total

    def test_check_names_unique(self, results):
        checks, _, _ = results
        names = [name for name, _ in checks]
        assert len(names) == len(set(names))

    def test_upstream_cccv_verified(self, results):
        checks, _, _ = results
        check_dict = dict(checks)
        assert check_dict.get("cccv_upstream_verified") is True

    def test_upstream_ccccxviii_verified(self, results):
        checks, _, _ = results
        check_dict = dict(checks)
        assert check_dict.get("ccccxviii_upstream_verified") is True


# ─── build_ccccxix_summary ────────────────────────────────────────────────────
class TestBuildSummary:
    """Test the JSON summary builder."""

    @pytest.fixture(scope="class")
    def summary(self):
        return build_ccccxix_summary()

    def test_status_pass(self, summary):
        assert summary["status"] == "PASS"

    def test_verified_true(self, summary):
        assert summary["verified"] is True

    def test_checks_pass_27(self, summary):
        assert summary["checks_passed"] == 27

    def test_checks_total_27(self, summary):
        assert summary["checks_total"] == 27

    def test_part_ccccxix(self, summary):
        assert summary["part"] == "CCCCXIX"

    def test_architecture_key(self, summary):
        arch = summary["architecture"]
        assert arch["labeling_dimension"] == Q
        assert arch["lovasz_theta"] == ALPHA
        assert arch["complement_theta"] == MU
        assert arch["shannon_capacity"] == V

    def test_ten_discoveries(self, summary):
        assert len(summary["discoveries"]) == 10

    def test_key_identity_theta_product(self, summary):
        ident = summary["key_identity"]["theta_times_complement_theta"]
        assert "40" in ident
        assert "V" in ident

    def test_json_written_to_disk(self, summary):
        json_path = ROOT / "PART_CCCCXIX_photonic_harmonic_tqc_synthesis_results.json"
        assert json_path.exists()

    def test_json_parseable(self, summary):
        json_path = ROOT / "PART_CCCCXIX_photonic_harmonic_tqc_synthesis_results.json"
        data = json.loads(json_path.read_text(encoding="utf-8"))
        assert data["status"] == "PASS"

    def test_failed_checks_empty(self, summary):
        assert summary["failed_checks"] == []
