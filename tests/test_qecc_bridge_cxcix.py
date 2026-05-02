"""
Tests for PART_CXCIX: Quantum Error-Correcting Codes Bridge
============================================================
Regression tests for all atom, classical code, quantum code, stabilizer,
concatenation, and structural checks.
"""

import math
import pytest

from PART_CXCIX_QECC_BRIDGE import (
    Q, LAM, V, K, PHI3, PHI4, PHI6, J_INV, EDGES, EIG_MAX, MULT_K2,
    HAMMING_N, HAMMING_K, HAMMING_D, HAMMING_R, HAMMING_CHECK,
    HAMMING_SPHERE, HAMMING_SPHERE_CHECK, HAMMING_SPHERE_IS_J_INV,
    GOLAY_N, GOLAY_K, GOLAY_D, GOLAY_PERFECT_CHECK, GOLAY_T, GOLAY_T_IS_Q,
    GOLAY_SPHERE, GOLAY_SPHERE_FORMULA, GOLAY_SPHERE_PERFECT,
    Q5_N, Q5_K, Q5_D, Q5_SINGLETON, Q5_STAB_COUNT, Q5_STAB_IS_LAM_SQ, Q5_T,
    STEANE_N, STEANE_K, STEANE_D, STEANE_STABILIZER_ORDER, STEANE_SINGLETON, STEANE_T,
    RM_N, RM_K, RM_D,
    QHB_N_MIN, QHB_LHS, QHB_RHS, QHB_TIGHT,
    STABILIZER_MIN_WEIGHT, CONCAT_LEVELS, CONCAT_DISTANCE, CONCAT_ACHIEVES_GOLAY_D,
    WEIGHT4_COUNT_RM, HAMMING_CODE_SIZE, HAMMING_DUAL_SIZE,
    QECCCheck,
    _make_atom_checks, _make_classical_code_checks, _make_quantum_code_checks,
    _make_stabilizer_checks, _make_concatenation_checks, _make_structural_checks,
    qecc_bridge_audit,
)


class TestAtoms:
    def test_Q(self): assert Q == 3
    def test_LAM(self): assert LAM == 2
    def test_K(self): assert K == 12
    def test_PHI3(self): assert PHI3 == 13
    def test_PHI4(self): assert PHI4 == 10
    def test_PHI6(self): assert PHI6 == 7
    def test_J_INV(self): assert J_INV == 8
    def test_EDGES(self): assert EDGES == 240
    def test_EIG_MAX(self): assert EIG_MAX == 5


class TestClassicalCodes:
    def test_hamming_n_phi6(self): assert HAMMING_N == PHI6
    def test_hamming_n_value(self): assert HAMMING_N == 7
    def test_hamming_d_q(self): assert HAMMING_D == Q
    def test_hamming_d_value(self): assert HAMMING_D == 3
    def test_hamming_r_q(self): assert HAMMING_R == Q
    def test_hamming_perfect(self): assert HAMMING_CHECK is True
    def test_hamming_sphere_j_inv(self): assert HAMMING_SPHERE == J_INV
    def test_hamming_sphere_is_j_inv(self): assert HAMMING_SPHERE_IS_J_INV is True
    def test_golay_n_value(self): assert GOLAY_N == 23
    def test_golay_n_formula(self): assert GOLAY_N == K + PHI6 + LAM + LAM
    def test_golay_k_is_K(self): assert GOLAY_K == K
    def test_golay_k_value(self): assert GOLAY_K == 12
    def test_golay_d_phi6(self): assert GOLAY_D == PHI6
    def test_golay_d_value(self): assert GOLAY_D == 7
    def test_golay_perfect(self): assert GOLAY_PERFECT_CHECK is True
    def test_golay_t_is_q(self): assert GOLAY_T_IS_Q is True
    def test_golay_t_value(self): assert GOLAY_T == 3
    def test_golay_sphere_perfect(self): assert GOLAY_SPHERE_PERFECT is True
    def test_golay_sphere_2048(self): assert GOLAY_SPHERE == 2048
    def test_golay_sphere_formula(self): assert GOLAY_SPHERE == GOLAY_SPHERE_FORMULA


class TestQuantumCodes:
    def test_q5_n_eig_max(self): assert Q5_N == EIG_MAX
    def test_q5_n_value(self): assert Q5_N == 5
    def test_q5_d_q(self): assert Q5_D == Q
    def test_q5_d_value(self): assert Q5_D == 3
    def test_q5_singleton_mds(self): assert Q5_SINGLETON is True
    def test_steane_n_phi6(self): assert STEANE_N == PHI6
    def test_steane_n_value(self): assert STEANE_N == 7
    def test_steane_d_q(self): assert STEANE_D == Q
    def test_steane_singleton(self): assert STEANE_SINGLETON is True
    def test_rm_n_formula(self): assert RM_N == PHI4 + EIG_MAX
    def test_rm_n_value(self): assert RM_N == 15
    def test_rm_k_phi6(self): assert RM_K == PHI6
    def test_qhb_tight(self): assert QHB_TIGHT is True
    def test_qhb_lhs(self): assert QHB_LHS == 16
    def test_qhb_rhs(self): assert QHB_RHS == 16


class TestStabilizer:
    def test_stab_min_weight_lam_sq(self): assert STABILIZER_MIN_WEIGHT == LAM**2
    def test_stab_min_weight_value(self): assert STABILIZER_MIN_WEIGHT == 4
    def test_q5_stab_count_lam_sq(self): assert Q5_STAB_COUNT == LAM**2
    def test_q5_stab_count_value(self): assert Q5_STAB_COUNT == 4
    def test_q5_stab_is_lam_sq(self): assert Q5_STAB_IS_LAM_SQ is True
    def test_steane_stab_order(self): assert STEANE_STABILIZER_ORDER == 64
    def test_q5_t_value(self): assert Q5_T == 1
    def test_steane_t_value(self): assert STEANE_T == 1


class TestConcatenation:
    def test_concat_levels(self): assert CONCAT_LEVELS == 2
    def test_concat_distance(self): assert CONCAT_DISTANCE == Q**2
    def test_concat_achieves_golay(self): assert CONCAT_ACHIEVES_GOLAY_D is True
    def test_weight4_count(self): assert WEIGHT4_COUNT_RM == EDGES


class TestStructural:
    def test_hamming_code_size(self): assert HAMMING_CODE_SIZE == 16
    def test_hamming_dual_size(self): assert HAMMING_DUAL_SIZE == J_INV
    def test_golay_k_is_K(self): assert GOLAY_K == K
    def test_golay_d_is_phi6(self): assert GOLAY_D == PHI6
    def test_rm_d_is_q(self): assert RM_D == Q
    def test_23_formula(self): assert K + PHI6 + LAM + LAM == 23


class TestQECCCheck:
    def test_exact_pass(self):
        c = QECCCheck("t", "d", 5, 5)
        assert c.passes

    def test_exact_fail(self):
        c = QECCCheck("t", "d", 5, 6)
        assert not c.passes

    def test_inexact_pass(self):
        c = QECCCheck("t", "d", 1.0 + 1e-12, 1.0, exact=False)
        assert c.passes

    def test_inexact_fail(self):
        c = QECCCheck("t", "d", 1.0 + 1e-9, 1.0, exact=False)
        assert not c.passes

    def test_frozen(self):
        c = QECCCheck("t", "d", 1, 1)
        with pytest.raises((AttributeError, TypeError)):
            c.name = "x"  # type: ignore[misc]


class TestCheckFactories:
    def test_atom_count(self): assert len(_make_atom_checks()) == 9
    def test_atom_all_pass(self): assert all(c.passes for c in _make_atom_checks())
    def test_classical_count(self): assert len(_make_classical_code_checks()) == 15
    def test_classical_all_pass(self): assert all(c.passes for c in _make_classical_code_checks())
    def test_quantum_count(self): assert len(_make_quantum_code_checks()) == 15
    def test_quantum_all_pass(self): assert all(c.passes for c in _make_quantum_code_checks())
    def test_stabilizer_count(self): assert len(_make_stabilizer_checks()) == 8
    def test_stabilizer_all_pass(self): assert all(c.passes for c in _make_stabilizer_checks())
    def test_concat_count(self): assert len(_make_concatenation_checks()) == 4
    def test_concat_all_pass(self): assert all(c.passes for c in _make_concatenation_checks())
    def test_structural_count(self): assert len(_make_structural_checks()) == 8
    def test_structural_all_pass(self): assert all(c.passes for c in _make_structural_checks())


class TestAudit:
    def setup_method(self):
        self.result = qecc_bridge_audit()

    def test_status_pass(self): assert self.result["status"] == "PASS"
    def test_all_checks_pass(self): assert self.result["all_checks_pass"] is True
    def test_no_failed(self): assert self.result["failed_checks"] == []
    def test_check_count(self): assert self.result["check_count"] == 59
    def test_checks_passing(self): assert self.result["checks_passing"] == 59

    def test_hamming_code_in_result(self):
        h = self.result["hamming_code"]
        assert h["n"] == 7 and h["k"] == 4 and h["d"] == 3

    def test_golay_code_in_result(self):
        g = self.result["golay_code"]
        assert g["n"] == 23 and g["k"] == 12 and g["d"] == 7

    def test_q5_code_in_result(self):
        q5 = self.result["q5_code"]
        assert q5["n"] == 5 and q5["k"] == 1 and q5["d"] == 3

    def test_steane_code_in_result(self):
        s = self.result["steane_code"]
        assert s["n"] == 7 and s["k"] == 1 and s["d"] == 3

    def test_w33_atoms_present(self):
        atoms = self.result["w33_atoms"]
        assert atoms["Q"] == 3 and atoms["EDGES"] == 240

    def test_theorem_key(self): assert "theorem_cxcix" in self.result

    def test_category_counts(self):
        cats = self.result["category_counts"]
        assert cats["atom_checks"] == 9
        assert cats["classical_code_checks"] == 15
        assert cats["quantum_code_checks"] == 15
        assert cats["stabilizer_checks"] == 8
        assert cats["concatenation_checks"] == 4
        assert cats["structural_checks"] == 8
