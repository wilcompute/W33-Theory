#!/usr/bin/env python3
"""Comprehensive test suite for W(3,3) Dirac Index Theorem Audit"""

import pytest
from scripts.w33_dirac_index_theorem_audit import w33_dirac_index_theorem_summary


class TestT1DiracIndexEulerCharacteristic:
    """T1: Dirac index equals Euler characteristic -80"""
    
    def test_theorem_flag_true(self):
        summary = w33_dirac_index_theorem_summary()
        assert summary["theorem"]["T1_dirac_index_equals_euler_characteristic"] is True
    
    def test_index_value_is_minus_80(self):
        summary = w33_dirac_index_theorem_summary()
        index = summary["spectrum_and_index"]["atiyah_singer_index"]["dirac_index"]
        assert index == -80
    
    def test_euler_characteristic_equals_index(self):
        summary = w33_dirac_index_theorem_summary()
        chi = summary["spectrum_and_index"]["atiyah_singer_index"]["euler_characteristic"]
        index = summary["spectrum_and_index"]["atiyah_singer_index"]["dirac_index"]
        assert chi == index


class TestT2ZeroEigenspace:
    """T2: Zero eigenspace is well-defined and computable"""
    
    def test_theorem_flag_true(self):
        summary = w33_dirac_index_theorem_summary()
        assert summary["theorem"]["T2_zero_eigenspace_dimension_is_computed"] is True
    
    def test_zero_modes_exist(self):
        summary = w33_dirac_index_theorem_summary()
        n_zero = summary["spectrum_and_index"]["spectrum_analysis"]["n_zero_modes_actual"]
        assert n_zero > 0
    
    def test_zero_modes_count_reasonable(self):
        summary = w33_dirac_index_theorem_summary()
        n_zero = summary["spectrum_and_index"]["spectrum_analysis"]["n_zero_modes_actual"]
        # Should be on the order of betti number / dimension
        assert n_zero < 300  # Sanity check


class TestT3SpectralGap:
    """T3: Spectral gap between zero and nonzero modes"""
    
    def test_theorem_flag_true(self):
        summary = w33_dirac_index_theorem_summary()
        assert summary["theorem"]["T3_spectral_gap_zero_from_nonzero"] is True
    
    def test_first_nonzero_eigvals_reasonable(self):
        summary = w33_dirac_index_theorem_audit()
        eigvals = summary["spectrum_and_index"]["spectrum_analysis"]["first_5_zero_eigvals"]
        # All should be small
        assert all(abs(e) < 1.0 for e in eigvals if e is not None)


class TestT4LaplacianRelation:
    """T4: Nonzero eigenvalues are sqrt of Laplacian eigenvalues"""
    
    def test_theorem_flag_true(self):
        summary = w33_dirac_index_theorem_summary()
        assert summary["theorem"]["T4_nonzero_eigenvalues_are_sqrt_laplacian_eigenvalues"] is True
    
    def test_sqrt_10_eigenvalue_present(self):
        summary = w33_dirac_index_theorem_summary()
        mult = summary["spectrum_and_index"]["spectrum_analysis"]["multiplicity_dict"]
        # sqrt(10) ≈ 3.162
        assert any("3.16" in str(k) for k in mult.keys())
    
    def test_eigenvalue_4_present(self):
        summary = w33_dirac_index_theorem_summary()
        mult = summary["spectrum_and_index"]["spectrum_analysis"]["multiplicity_dict"]
        # Eigenvalue 4.0 from L₁ (edge Laplacian)
        assert "4.0" in mult or any("4" in str(k) for k in mult.keys())


class TestT5SelfAdjointness:
    """T5: Dirac operator is self-adjoint"""
    
    def test_theorem_flag_true(self):
        summary = w33_dirac_index_theorem_summary()
        assert summary["theorem"]["T5_dirac_operator_is_self_adjoint"] is True


class TestT6BettiFormula:
    """T6: Euler characteristic from Betti numbers"""
    
    def test_theorem_flag_true(self):
        summary = w33_dirac_index_theorem_summary()
        assert summary["theorem"]["T6_euler_characteristic_from_betti_numbers"] is True
    
    def test_betti_values(self):
        summary = w33_dirac_index_theorem_summary()
        betti = summary["spectrum_and_index"]["atiyah_singer_index"]
        assert betti["betti_0"] == 1
        assert betti["betti_1"] == 81
        assert betti["betti_2"] == 0
        assert betti["betti_3"] == 0
    
    def test_betti_formula_correct(self):
        summary = w33_dirac_index_theorem_summary()
        betti = summary["spectrum_and_index"]["atiyah_singer_index"]
        chi = betti["betti_0"] - betti["betti_1"] + betti["betti_2"] - betti["betti_3"]
        assert chi == -80


class TestAllTheoremFlags:
    """Check that all six theorems are true"""
    
    def test_all_theorems_true(self):
        summary = w33_dirac_index_theorem_summary()
        theorem_dict = summary["theorem"]
        theorem_flags = [
            "T1_dirac_index_equals_euler_characteristic",
            "T2_zero_eigenspace_dimension_is_computed",
            "T3_spectral_gap_zero_from_nonzero",
            "T4_nonzero_eigenvalues_are_sqrt_laplacian_eigenvalues",
            "T5_dirac_operator_is_self_adjoint",
            "T6_euler_characteristic_from_betti_numbers",
        ]
        for flag in theorem_flags:
            assert theorem_dict[flag] is True, f"Flag {flag} is not True"
    
    def test_all_flags_present(self):
        summary = w33_dirac_index_theorem_summary()
        theorem_dict = summary["theorem"]
        expected_count = 6
        assert len(theorem_dict) == expected_count


class TestCarrierStructure:
    """Verify carrier graph structure"""
    
    def test_graph_is_w33(self):
        summary = w33_dirac_index_theorem_summary()
        carrier = summary["carrier"]
        assert carrier["graph"] == "W(3,3)"
    
    def test_vertex_count(self):
        summary = w33_dirac_index_theorem_summary()
        carrier = summary["carrier"]
        assert carrier["vertices"] == 40
    
    def test_edge_count(self):
        summary = w33_dirac_index_theorem_summary()
        carrier = summary["carrier"]
        assert carrier["edges"] == 240
    
    def test_type_is_srg(self):
        summary = w33_dirac_index_theorem_summary()
        carrier = summary["carrier"]
        assert "SRG(40,12,2,4)" in carrier["type"]


class TestHodgeDecomposition:
    """Verify Hodge decomposition Betti numbers"""
    
    def test_harmonic_0_forms(self):
        summary = w33_dirac_index_theorem_summary()
        hodge = summary["hodge_decomposition"]
        assert hodge["harmonic_0_forms"] == 1
    
    def test_harmonic_1_forms(self):
        summary = w33_dirac_index_theorem_summary()
        hodge = summary["hodge_decomposition"]
        assert hodge["harmonic_1_forms"] == 81
    
    def test_harmonic_2_forms(self):
        summary = w33_dirac_index_theorem_summary()
        hodge = summary["hodge_decomposition"]
        assert hodge["harmonic_2_forms"] == 0
    
    def test_total_harmonic(self):
        summary = w33_dirac_index_theorem_summary()
        hodge = summary["hodge_decomposition"]
        total = (hodge["harmonic_0_forms"] + hodge["harmonic_1_forms"] +
                 hodge["harmonic_2_forms"] + hodge["harmonic_3_forms"])
        assert total == 82


class TestDiracOperatorStructure:
    """Verify Dirac operator structure"""
    
    def test_is_self_adjoint(self):
        summary = w33_dirac_index_theorem_summary()
        dirac = summary["dirac_operator"]
        assert dirac["is_self_adjoint"] is True
    
    def test_block_structure_description(self):
        summary = w33_dirac_index_theorem_summary()
        dirac = summary["dirac_operator"]
        assert "0-forms" in dirac["block_structure"]
        assert "1-forms" in dirac["block_structure"]
    
    def test_dimension_is_280(self):
        summary = w33_dirac_index_theorem_summary()
        dirac = summary["dirac_operator"]
        assert dirac["dimension"] == 280  # 40 + 240


class TestBoundaryLanguage:
    """Verify boundary language and status"""
    
    def test_status_ok(self):
        summary = w33_dirac_index_theorem_summary()
        assert summary["status"] == "ok"
    
    def test_boundary_note_present(self):
        summary = w33_dirac_index_theorem_summary()
        note = summary["boundary_note"]
        assert "exact finite" in note.lower()
        assert "atiyah" in note.lower()
    
    def test_boundary_mentions_six_theorems(self):
        summary = w33_dirac_index_theorem_summary()
        note = summary["boundary_note"]
        assert "T1" in note or "six" in note.lower()


# Helper for tests that need to import the function
def w33_dirac_index_theorem_audit():
    return w33_dirac_index_theorem_summary()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
