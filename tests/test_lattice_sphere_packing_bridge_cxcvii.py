"""
Tests for PART_CXCVII: Lattice Sphere Packing Bridge
=====================================================
98+ regression tests covering atom correctness, E₈, Leech, Barnes-Wall,
D₄ lattice constants, exceptional dimension characterisation, Coxeter
numbers, and the full audit function.
"""

import json
import os
import pytest

from PART_CXCVII_LATTICE_SPHERE_PACKING_BRIDGE import (
    Q, LAM, V, K, PHI3, PHI4, PHI6, PHI12, J_INV, EDGES, EIG_MAX, MULT_K2,
    E8_DIM, E8_KISSING, E8_POSITIVE_ROOTS, E8_RANK, E8_LIE_DIM,
    E8_COXETER_NUMBER, E8_MIN_NORM, E8_THETA_COEFF, E8_A2,
    LEECH_DIM, LEECH_KISSING, LEECH_MIN_NORM,
    LEECH_DENSITY_K, LEECH_DENSITY_DIM_HALF,
    BW_DIM, BW_KISSING,
    D4_DIM, D4_KISSING,
    OPTIMAL_PACKING_DIMS, N_OPTIMAL_KNOWN,
    E8_DENSITY_DENOM_FORMULA,
    HERMITE_4_NUM, HERMITE_8_NUM, HERMITE_24_NUM,
    E6_COXETER, E7_COXETER_NUMBER, E8_COXETER_NUMBER,
    PackCheck,
    _make_atom_checks, _make_e8_checks, _make_leech_checks,
    _make_barnes_wall_checks, _make_d4_checks,
    _make_exceptional_dims_checks, _make_coxeter_checks,
    _make_structural_checks,
    lattice_sphere_packing_bridge_audit,
)


# ---------------------------------------------------------------------------
# Atom tests
# ---------------------------------------------------------------------------
class TestAtoms:
    def test_Q(self): assert Q == 3
    def test_LAM(self): assert LAM == 2
    def test_V(self): assert V == 40
    def test_K(self): assert K == 12
    def test_PHI3(self): assert PHI3 == 13
    def test_PHI4(self): assert PHI4 == 10
    def test_PHI6(self): assert PHI6 == 7
    def test_PHI12(self): assert PHI12 == 73
    def test_J_INV(self): assert J_INV == 8
    def test_EDGES(self): assert EDGES == 240
    def test_EIG_MAX(self): assert EIG_MAX == 5
    def test_MULT_K2(self): assert MULT_K2 == K // 2


# ---------------------------------------------------------------------------
# E₈ lattice tests
# ---------------------------------------------------------------------------
class TestE8:
    def test_e8_dim_is_j_inv(self): assert E8_DIM == J_INV
    def test_e8_dim_value(self): assert E8_DIM == 8
    def test_e8_kissing_is_edges(self): assert E8_KISSING == EDGES
    def test_e8_kissing_value(self): assert E8_KISSING == 240
    def test_e8_positive_roots_is_half_edges(self): assert E8_POSITIVE_ROOTS == EDGES // 2
    def test_e8_positive_roots_value(self): assert E8_POSITIVE_ROOTS == 120
    def test_e8_rank_is_j_inv(self): assert E8_RANK == J_INV
    def test_e8_rank_value(self): assert E8_RANK == 8
    def test_e8_lie_dim_formula(self): assert E8_LIE_DIM == EDGES + J_INV
    def test_e8_lie_dim_value(self): assert E8_LIE_DIM == 248
    def test_e8_coxeter_formula(self): assert E8_COXETER_NUMBER == LEECH_DIM + MULT_K2
    def test_e8_coxeter_value(self): assert E8_COXETER_NUMBER == 30
    def test_e8_min_norm_is_lam(self): assert E8_MIN_NORM == LAM
    def test_e8_min_norm_value(self): assert E8_MIN_NORM == 2
    def test_e8_theta_coeff_is_edges(self): assert E8_THETA_COEFF == EDGES
    def test_e8_second_layer_formula(self): assert E8_A2 == Q**2 * EDGES
    def test_e8_second_layer_value(self): assert E8_A2 == 2160


# ---------------------------------------------------------------------------
# Leech lattice tests
# ---------------------------------------------------------------------------
class TestLeech:
    def test_leech_dim_formula(self): assert LEECH_DIM == 2 * K
    def test_leech_dim_value(self): assert LEECH_DIM == 24
    def test_leech_kissing_formula(self):
        assert LEECH_KISSING == EDGES * PHI3 * PHI6 * Q**2
    def test_leech_kissing_value(self): assert LEECH_KISSING == 196560
    def test_leech_min_norm_formula(self): assert LEECH_MIN_NORM == J_INV // 2
    def test_leech_min_norm_value(self): assert LEECH_MIN_NORM == 4
    def test_leech_density_k(self): assert LEECH_DENSITY_K == K
    def test_leech_dim_half(self): assert LEECH_DENSITY_DIM_HALF == K
    def test_leech_e8_ratio(self):
        assert LEECH_KISSING // E8_KISSING == PHI3 * PHI6 * Q**2
    def test_leech_e8_ratio_value(self):
        assert LEECH_KISSING // E8_KISSING == 819


# ---------------------------------------------------------------------------
# Barnes-Wall lattice tests
# ---------------------------------------------------------------------------
class TestBarnesWall:
    def test_bw_dim_formula(self): assert BW_DIM == 2 * J_INV
    def test_bw_dim_value(self): assert BW_DIM == 16
    def test_bw_kissing_formula(self): assert BW_KISSING == 2 * Q**2 * EDGES
    def test_bw_kissing_value(self): assert BW_KISSING == 4320
    def test_bw_between_e8_and_leech(self): assert E8_DIM < BW_DIM < LEECH_DIM


# ---------------------------------------------------------------------------
# D₄ lattice tests
# ---------------------------------------------------------------------------
class TestD4:
    def test_d4_dim_formula(self): assert D4_DIM == J_INV // 2
    def test_d4_dim_value(self): assert D4_DIM == 4
    def test_d4_kissing_formula(self): assert D4_KISSING == 2 * K
    def test_d4_kissing_value(self): assert D4_KISSING == 24


# ---------------------------------------------------------------------------
# Exceptional dimension characterisation
# ---------------------------------------------------------------------------
class TestExceptionalDims:
    def test_optimal_dims_tuple(self): assert OPTIMAL_PACKING_DIMS == (4, 8, 24)
    def test_optimal_dim_d4(self): assert OPTIMAL_PACKING_DIMS[0] == D4_DIM
    def test_optimal_dim_e8(self): assert OPTIMAL_PACKING_DIMS[1] == E8_DIM
    def test_optimal_dim_leech(self): assert OPTIMAL_PACKING_DIMS[2] == LEECH_DIM
    def test_n_optimal_is_3(self): assert N_OPTIMAL_KNOWN == 3
    def test_n_optimal_formula(self): assert N_OPTIMAL_KNOWN == LAM + 1
    def test_optimal_set(self):
        assert set(OPTIMAL_PACKING_DIMS) == {J_INV // 2, J_INV, 2 * K}
    def test_e8_density_denom(self): assert E8_DENSITY_DENOM_FORMULA == 384
    def test_e8_density_denom_formula(self):
        assert E8_DENSITY_DENOM_FORMULA == BW_DIM * LEECH_DIM
    def test_dim_arithmetic(self): assert LEECH_DIM == E8_DIM + BW_DIM


# ---------------------------------------------------------------------------
# Coxeter number tests
# ---------------------------------------------------------------------------
class TestCoxeterNumbers:
    def test_e6_coxeter_formula(self): assert E6_COXETER == LEECH_DIM // 2
    def test_e6_coxeter_value(self): assert E6_COXETER == 12
    def test_e6_coxeter_equals_k(self): assert E6_COXETER == K
    def test_e7_coxeter_formula(self): assert E7_COXETER_NUMBER == 2 * Q**2
    def test_e7_coxeter_value(self): assert E7_COXETER_NUMBER == 18
    def test_e8_coxeter_value(self): assert E8_COXETER_NUMBER == 30
    def test_hermite_4(self): assert HERMITE_4_NUM == LAM
    def test_hermite_8(self): assert HERMITE_8_NUM == LAM
    def test_hermite_24(self): assert HERMITE_24_NUM == D4_DIM
    def test_hermite_24_value(self): assert HERMITE_24_NUM == 4


# ---------------------------------------------------------------------------
# PackCheck dataclass
# ---------------------------------------------------------------------------
class TestPackCheck:
    def test_exact_pass(self):
        c = PackCheck("t", "test", 42, 42, exact=True)
        assert c.passes

    def test_exact_fail(self):
        c = PackCheck("t", "test", 42, 43, exact=True)
        assert not c.passes

    def test_inexact_pass(self):
        c = PackCheck("t", "test", 1.0 + 1e-12, 1.0, exact=False)
        assert c.passes

    def test_inexact_fail(self):
        c = PackCheck("t", "test", 1.0 + 1e-9, 1.0, exact=False)
        assert not c.passes

    def test_frozen(self):
        c = PackCheck("t", "test", 1, 1)
        with pytest.raises((AttributeError, TypeError)):
            c.name = "x"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Check factory tests
# ---------------------------------------------------------------------------
class TestAtomChecks:
    def test_count(self): assert len(_make_atom_checks()) == 9
    def test_all_pass(self): assert all(c.passes for c in _make_atom_checks())


class TestE8Checks:
    def test_count(self): assert len(_make_e8_checks()) == 15
    def test_all_pass(self): assert all(c.passes for c in _make_e8_checks())


class TestLeechChecks:
    def test_count(self): assert len(_make_leech_checks()) == 7
    def test_all_pass(self): assert all(c.passes for c in _make_leech_checks())


class TestBWChecks:
    def test_count(self): assert len(_make_barnes_wall_checks()) == 4
    def test_all_pass(self): assert all(c.passes for c in _make_barnes_wall_checks())


class TestD4Checks:
    def test_count(self): assert len(_make_d4_checks()) == 4
    def test_all_pass(self): assert all(c.passes for c in _make_d4_checks())


class TestExceptionalDimsChecks:
    def test_count(self): assert len(_make_exceptional_dims_checks()) == 7
    def test_all_pass(self): assert all(c.passes for c in _make_exceptional_dims_checks())


class TestCoxeterChecks:
    def test_count(self): assert len(_make_coxeter_checks()) == 8
    def test_all_pass(self): assert all(c.passes for c in _make_coxeter_checks())


class TestStructuralChecks:
    def test_count(self): assert len(_make_structural_checks()) == 8
    def test_all_pass(self): assert all(c.passes for c in _make_structural_checks())


# ---------------------------------------------------------------------------
# Full audit function
# ---------------------------------------------------------------------------
class TestAudit:
    def setup_method(self):
        self.result = lattice_sphere_packing_bridge_audit()

    def test_status_pass(self): assert self.result["status"] == "PASS"
    def test_all_checks_pass(self): assert self.result["all_checks_pass"] is True
    def test_no_failed(self): assert self.result["failed_checks"] == []
    def test_check_count(self): assert self.result["check_count"] == 62
    def test_checks_passing(self): assert self.result["checks_passing"] == 62

    def test_e8_kissing_in_result(self): assert self.result["e8_kissing"] == 240
    def test_leech_kissing_in_result(self): assert self.result["leech_kissing"] == 196560
    def test_bw_kissing_in_result(self): assert self.result["bw_kissing"] == 4320
    def test_d4_kissing_in_result(self): assert self.result["d4_kissing"] == 24
    def test_e8_lie_dim_in_result(self): assert self.result["e8_lie_dim"] == 248

    def test_optimal_dims(self):
        assert self.result["optimal_packing_dims"] == [4, 8, 24]

    def test_w33_atoms_present(self):
        atoms = self.result["w33_atoms"]
        assert atoms["Q"] == 3
        assert atoms["EDGES"] == 240
        assert atoms["K"] == 12

    def test_theorem_key_present(self): assert "theorem_cxcvii" in self.result

    def test_category_counts(self):
        cats = self.result["category_counts"]
        assert cats["atom_checks"] == 9
        assert cats["e8_checks"] == 15
        assert cats["leech_checks"] == 7
        assert cats["barnes_wall_checks"] == 4
        assert cats["d4_checks"] == 4
        assert cats["exceptional_dims_checks"] == 7
        assert cats["coxeter_checks"] == 8
        assert cats["structural_checks"] == 8
