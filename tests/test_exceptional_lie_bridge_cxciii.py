"""Regression tests for PART_CXCIII_EXCEPTIONAL_LIE_BRIDGE."""
import pytest
from PART_CXCIII_EXCEPTIONAL_LIE_BRIDGE import (
    Q, LAM, V, K, PHI3, PHI4, PHI6, J_INV, EDGES, EIG_MAX,
    EXCEPTIONAL_LIE_DATA,
    LieCheck,
    _make_atom_checks,
    _make_rank_checks,
    _make_root_checks,
    _make_dim_checks,
    _make_coxeter_checks,
    _make_dual_coxeter_checks,
    _make_weyl_checks,
    _make_structural_checks,
    exceptional_lie_bridge_audit,
)


# ---------------------------------------------------------------------------
# Atoms
# ---------------------------------------------------------------------------

class TestAtoms:
    def test_Q(self):          assert Q == 3
    def test_K(self):          assert K == 12
    def test_V(self):          assert V == 40
    def test_J_INV(self):      assert J_INV == 8
    def test_EDGES(self):      assert EDGES == 240
    def test_PHI3(self):       assert PHI3 == 13
    def test_PHI4(self):       assert PHI4 == 10
    def test_PHI6(self):       assert PHI6 == 7
    def test_LAM(self):        assert LAM == 2
    def test_EIG_MAX(self):    assert EIG_MAX == 5


# ---------------------------------------------------------------------------
# Exceptional Lie data table
# ---------------------------------------------------------------------------

class TestExceptionalLieData:
    def test_G2(self):
        assert EXCEPTIONAL_LIE_DATA["G2"] == (2, 12, 14, 6, 4)

    def test_F4(self):
        assert EXCEPTIONAL_LIE_DATA["F4"] == (4, 48, 52, 12, 9)

    def test_E6(self):
        assert EXCEPTIONAL_LIE_DATA["E6"] == (6, 72, 78, 12, 12)

    def test_E7(self):
        assert EXCEPTIONAL_LIE_DATA["E7"] == (7, 126, 133, 18, 18)

    def test_E8(self):
        assert EXCEPTIONAL_LIE_DATA["E8"] == (8, 240, 248, 30, 30)

    def test_five_algebras(self):
        assert len(EXCEPTIONAL_LIE_DATA) == 5


# ---------------------------------------------------------------------------
# LieCheck dataclass
# ---------------------------------------------------------------------------

class TestLieCheck:
    def test_passes_exact_equal(self):
        c = LieCheck("t", "d", 12, 12)
        assert c.passes

    def test_passes_exact_unequal(self):
        c = LieCheck("t", "d", 12, 13)
        assert not c.passes

    def test_passes_inexact_close(self):
        c = LieCheck("t", "d", 1.000000000001, 1.0, exact=False)
        assert c.passes

    def test_passes_inexact_far(self):
        c = LieCheck("t", "d", 1.1, 1.0, exact=False)
        assert not c.passes


# ---------------------------------------------------------------------------
# Rank checks
# ---------------------------------------------------------------------------

class TestRankChecks:
    def test_G2_rank(self):      assert EXCEPTIONAL_LIE_DATA["G2"][0] == LAM
    def test_F4_rank(self):      assert EXCEPTIONAL_LIE_DATA["F4"][0] == J_INV // 2
    def test_E6_rank(self):      assert EXCEPTIONAL_LIE_DATA["E6"][0] == K // 2
    def test_E7_rank(self):      assert EXCEPTIONAL_LIE_DATA["E7"][0] == PHI6
    def test_E8_rank(self):      assert EXCEPTIONAL_LIE_DATA["E8"][0] == J_INV
    def test_all_pass(self):
        assert all(c.passes for c in _make_rank_checks())


# ---------------------------------------------------------------------------
# Root system checks
# ---------------------------------------------------------------------------

class TestRootChecks:
    def test_G2_roots(self):     assert EXCEPTIONAL_LIE_DATA["G2"][1] == K
    def test_F4_roots(self):     assert EXCEPTIONAL_LIE_DATA["F4"][1] == 4 * K
    def test_E6_roots(self):     assert EXCEPTIONAL_LIE_DATA["E6"][1] == V + 2 * K + J_INV
    def test_E7_roots(self):     assert EXCEPTIONAL_LIE_DATA["E7"][1] == 2 * Q * Q * PHI6
    def test_E8_roots(self):     assert EXCEPTIONAL_LIE_DATA["E8"][1] == EDGES
    def test_all_pass(self):
        assert all(c.passes for c in _make_root_checks())


# ---------------------------------------------------------------------------
# Dimension checks
# ---------------------------------------------------------------------------

class TestDimChecks:
    def test_G2_dim(self):     assert EXCEPTIONAL_LIE_DATA["G2"][2] == 2 * PHI6
    def test_F4_dim(self):     assert EXCEPTIONAL_LIE_DATA["F4"][2] == 4 * PHI3
    def test_E6_dim(self):     assert EXCEPTIONAL_LIE_DATA["E6"][2] == 2 * Q * PHI3
    def test_E7_dim(self):     assert EXCEPTIONAL_LIE_DATA["E7"][2] == EDGES // 2 + PHI3
    def test_E8_dim(self):     assert EXCEPTIONAL_LIE_DATA["E8"][2] == EDGES + J_INV
    def test_all_pass(self):
        assert all(c.passes for c in _make_dim_checks())


# ---------------------------------------------------------------------------
# Coxeter number checks
# ---------------------------------------------------------------------------

class TestCoxeterChecks:
    def test_G2_h(self):     assert EXCEPTIONAL_LIE_DATA["G2"][3] == K // 2
    def test_F4_h(self):     assert EXCEPTIONAL_LIE_DATA["F4"][3] == K
    def test_E6_h(self):     assert EXCEPTIONAL_LIE_DATA["E6"][3] == K
    def test_E7_h(self):     assert EXCEPTIONAL_LIE_DATA["E7"][3] == 2 * Q * Q
    def test_E8_h(self):     assert EXCEPTIONAL_LIE_DATA["E8"][3] == Q * PHI4
    def test_F4_E6_same_h(self):
        assert EXCEPTIONAL_LIE_DATA["F4"][3] == EXCEPTIONAL_LIE_DATA["E6"][3]
    def test_all_pass(self):
        assert all(c.passes for c in _make_coxeter_checks())


# ---------------------------------------------------------------------------
# Dual Coxeter number checks
# ---------------------------------------------------------------------------

class TestDualCoxeterChecks:
    def test_G2_hstar(self):   assert EXCEPTIONAL_LIE_DATA["G2"][4] == LAM * LAM
    def test_F4_hstar(self):   assert EXCEPTIONAL_LIE_DATA["F4"][4] == Q * Q
    def test_E6_hstar(self):   assert EXCEPTIONAL_LIE_DATA["E6"][4] == K
    def test_E7_hstar(self):   assert EXCEPTIONAL_LIE_DATA["E7"][4] == 2 * Q * Q
    def test_E8_hstar(self):   assert EXCEPTIONAL_LIE_DATA["E8"][4] == Q * PHI4
    def test_all_pass(self):
        assert all(c.passes for c in _make_dual_coxeter_checks())


# ---------------------------------------------------------------------------
# Weyl formula
# ---------------------------------------------------------------------------

class TestWeylChecks:
    @pytest.mark.parametrize("alg", ["G2", "F4", "E6", "E7", "E8"])
    def test_weyl_h_times_rank(self, alg):
        rank, n_roots, _dim, h, _hstar = EXCEPTIONAL_LIE_DATA[alg]
        assert h * rank == n_roots

    @pytest.mark.parametrize("alg", ["G2", "F4", "E6", "E7", "E8"])
    def test_dim_decomp(self, alg):
        rank, n_roots, dim, _h, _hstar = EXCEPTIONAL_LIE_DATA[alg]
        assert rank + n_roots == dim

    def test_all_pass(self):
        assert all(c.passes for c in _make_weyl_checks())


# ---------------------------------------------------------------------------
# Structural checks
# ---------------------------------------------------------------------------

class TestStructuralChecks:
    def test_E_series_simply_laced(self):
        for alg in ("E6", "E7", "E8"):
            h, hstar = EXCEPTIONAL_LIE_DATA[alg][3], EXCEPTIONAL_LIE_DATA[alg][4]
            assert h == hstar

    def test_G2_non_simply_laced(self):
        h, hstar = EXCEPTIONAL_LIE_DATA["G2"][3], EXCEPTIONAL_LIE_DATA["G2"][4]
        assert h - hstar == LAM

    def test_F4_non_simply_laced(self):
        h, hstar = EXCEPTIONAL_LIE_DATA["F4"][3], EXCEPTIONAL_LIE_DATA["F4"][4]
        assert h - hstar == Q

    def test_count_exceptional(self):
        assert len(EXCEPTIONAL_LIE_DATA) == EIG_MAX

    def test_E_series_rank_sum(self):
        total = sum(EXCEPTIONAL_LIE_DATA[a][0] for a in ("E6", "E7", "E8"))
        assert total == Q * PHI6

    def test_all_pass(self):
        assert all(c.passes for c in _make_structural_checks())


# ---------------------------------------------------------------------------
# Full audit
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def result():
    return exceptional_lie_bridge_audit()


class TestExceptionalLieBridgeAudit:
    def test_status_pass(self, result):
        assert result["status"] == "PASS"

    def test_all_checks_pass(self, result):
        assert result["all_checks_pass"] is True

    def test_no_failed_checks(self, result):
        assert result["failed_checks"] == []

    def test_total_check_count(self, result):
        assert result["check_count"] == 52

    def test_checks_passing_eq_total(self, result):
        assert result["checks_passing"] == result["check_count"]

    def test_atom_check_count(self, result):
        assert result["atom_check_count"] == 9

    def test_rank_check_count(self, result):
        assert result["rank_check_count"] == 5

    def test_root_check_count(self, result):
        assert result["root_check_count"] == 5

    def test_dim_check_count(self, result):
        assert result["dim_check_count"] == 5

    def test_coxeter_check_count(self, result):
        assert result["coxeter_check_count"] == 5

    def test_dual_coxeter_check_count(self, result):
        assert result["dual_coxeter_check_count"] == 5

    def test_weyl_check_count(self, result):
        assert result["weyl_check_count"] == 10

    def test_structural_check_count(self, result):
        assert result["structural_check_count"] == 8

    def test_E8_dim(self, result):
        assert result["exceptional_algebras"]["E8"]["dim"] == 248

    def test_E8_roots(self, result):
        assert result["exceptional_algebras"]["E8"]["n_roots"] == 240

    def test_E8_rank(self, result):
        assert result["exceptional_algebras"]["E8"]["rank"] == 8

    def test_G2_roots(self, result):
        assert result["exceptional_algebras"]["G2"]["n_roots"] == 12

    def test_theorem_present(self, result):
        assert "theorem_cxciii" in result
        assert "exceptional" in result["theorem_cxciii"].lower()

    def test_w33_atoms_present(self, result):
        atoms = result["w33_atoms"]
        assert atoms["Q"] == 3
        assert atoms["K"] == 12
        assert atoms["EDGES"] == 240
