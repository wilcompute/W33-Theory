"""
Tests for PART_CXCV: Monstrous Moonshine Bridge
"""

import pytest
from PART_CXCV_MONSTROUS_MOONSHINE_BRIDGE import (
    Q, LAM, V, K, PHI3, PHI4, PHI6, PHI12, J_INV, EDGES, EIG_MAX, MULT_K2,
    MONSTER_P_ADIC, BABY_MONSTER_P_ADIC, CO1_P_ADIC, TH_P_ADIC, M24_P_ADIC,
    N_SPORADICS, N_HAPPY_FAMILY, N_PARIAHS, N_MATHIEU,
    J_CONSTANT, J_COEFF_1, LEECH_KISSING, LEECH_DIM,
    GOLAY_PRIME, K_MINUS_1, MONSTER_PRIME_COUNT,
    MoonCheck,
    _make_atom_checks,
    _make_monster_valuation_checks,
    _make_sporadic_structure_checks,
    _make_baby_monster_checks,
    _make_m24_checks,
    _make_conway_checks,
    _make_moonshine_checks,
    _make_structural_checks,
    monstrous_moonshine_bridge_audit,
)


# ---------------------------------------------------------------------------
# Atom tests
# ---------------------------------------------------------------------------
class TestAtoms:
    def test_Q(self):
        assert Q == 3

    def test_LAM(self):
        assert LAM == 2

    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_PHI3(self):
        assert PHI3 == Q**2 + Q + 1 == 13

    def test_PHI4(self):
        assert PHI4 == Q**2 + 1 == 10

    def test_PHI6(self):
        assert PHI6 == Q**2 - Q + 1 == 7

    def test_PHI12(self):
        assert PHI12 == Q**4 - Q**2 + 1 == 73

    def test_J_INV(self):
        assert J_INV == 8

    def test_EDGES(self):
        assert EDGES == V * K // 2 == 240

    def test_EIG_MAX(self):
        assert EIG_MAX == 5


# ---------------------------------------------------------------------------
# Monster p-adic valuation data
# ---------------------------------------------------------------------------
class TestMonsterPAdicData:
    def test_v2_value(self):
        assert MONSTER_P_ADIC[2] == 46

    def test_v3_value(self):
        assert MONSTER_P_ADIC[3] == 20

    def test_v5_value(self):
        assert MONSTER_P_ADIC[5] == 9

    def test_v7_value(self):
        assert MONSTER_P_ADIC[7] == 6

    def test_v11_value(self):
        assert MONSTER_P_ADIC[11] == 2

    def test_v13_value(self):
        assert MONSTER_P_ADIC[13] == 3

    def test_prime_count(self):
        assert len(MONSTER_P_ADIC) == 15

    def test_prime_23_present(self):
        assert 23 in MONSTER_P_ADIC

    def test_prime_71_present(self):
        assert 71 in MONSTER_P_ADIC


# ---------------------------------------------------------------------------
# Sporadic group constants
# ---------------------------------------------------------------------------
class TestSporadicConstants:
    def test_total_sporadics(self):
        assert N_SPORADICS == 26

    def test_happy_family(self):
        assert N_HAPPY_FAMILY == 20

    def test_pariahs(self):
        assert N_PARIAHS == 6

    def test_partition(self):
        assert N_HAPPY_FAMILY + N_PARIAHS == N_SPORADICS

    def test_mathieu_count(self):
        assert N_MATHIEU == 5

    def test_golay_prime(self):
        assert GOLAY_PRIME == 23

    def test_k_minus_1(self):
        assert K_MINUS_1 == 11

    def test_monster_prime_count(self):
        assert MONSTER_PRIME_COUNT == 15


# ---------------------------------------------------------------------------
# MoonCheck dataclass
# ---------------------------------------------------------------------------
class TestMoonCheck:
    def test_exact_pass(self):
        c = MoonCheck("t", "d", 5, 5)
        assert c.passes

    def test_exact_fail(self):
        c = MoonCheck("t", "d", 5, 6)
        assert not c.passes

    def test_inexact_pass(self):
        c = MoonCheck("t", "d", 1.000000000001, 1.0, exact=False)
        assert c.passes

    def test_inexact_fail(self):
        c = MoonCheck("t", "d", 1.0001, 1.0, exact=False)
        assert not c.passes


# ---------------------------------------------------------------------------
# Monster valuation checks
# ---------------------------------------------------------------------------
class TestMonsterValuationChecks:
    def setup_method(self):
        self.checks = _make_monster_valuation_checks()

    def test_count(self):
        assert len(self.checks) == 6

    def test_all_pass(self):
        failed = [c for c in self.checks if not c.passes]
        assert not failed, [c.name for c in failed]

    def test_v2_formula(self):
        assert MONSTER_P_ADIC[2] == 2 * (K + PHI3 - 2)

    def test_v2_intermediate(self):
        assert K + PHI3 - 2 == 23  # = GOLAY_PRIME

    def test_v3_formula(self):
        assert MONSTER_P_ADIC[3] == V // 2

    def test_v5_formula(self):
        assert MONSTER_P_ADIC[5] == Q**2

    def test_v7_formula(self):
        assert MONSTER_P_ADIC[7] == K // 2

    def test_v11_formula(self):
        assert MONSTER_P_ADIC[11] == LAM

    def test_v13_formula(self):
        assert MONSTER_P_ADIC[13] == Q


# ---------------------------------------------------------------------------
# Sporadic structure checks
# ---------------------------------------------------------------------------
class TestSporadicStructureChecks:
    def setup_method(self):
        self.checks = _make_sporadic_structure_checks()

    def test_count(self):
        assert len(self.checks) == 6

    def test_all_pass(self):
        failed = [c for c in self.checks if not c.passes]
        assert not failed, [c.name for c in failed]

    def test_total_formula(self):
        assert N_SPORADICS == 2 * PHI3

    def test_happy_family_formula(self):
        assert N_HAPPY_FAMILY == V // 2

    def test_pariahs_formula(self):
        assert N_PARIAHS == K // 2

    def test_prime_count_formula(self):
        assert MONSTER_PRIME_COUNT == K + Q

    def test_golay_prime_formula(self):
        assert GOLAY_PRIME == K + PHI3 - 2

    def test_mathieu_count_formula(self):
        assert N_MATHIEU == EIG_MAX


# ---------------------------------------------------------------------------
# Baby Monster checks
# ---------------------------------------------------------------------------
class TestBabyMonsterChecks:
    def setup_method(self):
        self.checks = _make_baby_monster_checks()

    def test_count(self):
        assert len(self.checks) == 4

    def test_all_pass(self):
        failed = [c for c in self.checks if not c.passes]
        assert not failed, [c.name for c in failed]

    def test_baby_v2_formula(self):
        assert BABY_MONSTER_P_ADIC[2] == 3 * PHI3 + 2  # = 41

    def test_baby_v2_value(self):
        assert BABY_MONSTER_P_ADIC[2] == 41

    def test_baby_v3_formula(self):
        assert BABY_MONSTER_P_ADIC[3] == PHI3  # = 13

    def test_baby_v5_formula(self):
        assert BABY_MONSTER_P_ADIC[5] == K // 2  # = 6

    def test_baby_v7_formula(self):
        assert BABY_MONSTER_P_ADIC[7] == LAM  # = 2


# ---------------------------------------------------------------------------
# M24 checks
# ---------------------------------------------------------------------------
class TestM24Checks:
    def setup_method(self):
        self.checks = _make_m24_checks()

    def test_count(self):
        assert len(self.checks) == 4

    def test_all_pass(self):
        failed = [c for c in self.checks if not c.passes]
        assert not failed, [c.name for c in failed]

    def test_m24_v2_formula(self):
        assert M24_P_ADIC[2] == PHI4  # = 10

    def test_m24_v3_formula(self):
        assert M24_P_ADIC[3] == Q  # = 3

    def test_m24_prime_11(self):
        assert K - 1 == 11

    def test_m24_prime_23_divides(self):
        assert M24_P_ADIC.get(K + PHI3 - 2, 0) == 1


# ---------------------------------------------------------------------------
# Conway group checks
# ---------------------------------------------------------------------------
class TestConwayChecks:
    def setup_method(self):
        self.checks = _make_conway_checks()

    def test_count(self):
        assert len(self.checks) == 4

    def test_all_pass(self):
        failed = [c for c in self.checks if not c.passes]
        assert not failed, [c.name for c in failed]

    def test_co1_v2_formula(self):
        assert CO1_P_ADIC[2] == Q * PHI6  # = 21

    def test_co1_v2_value(self):
        assert CO1_P_ADIC[2] == 21

    def test_co1_v3_formula(self):
        assert CO1_P_ADIC[3] == Q**2  # = 9

    def test_co1_v5_formula(self):
        assert CO1_P_ADIC[5] == J_INV // 2  # = 4

    def test_co1_v7_formula(self):
        assert CO1_P_ADIC[7] == LAM  # = 2


# ---------------------------------------------------------------------------
# Moonshine / j-invariant checks
# ---------------------------------------------------------------------------
class TestMoonshineChecks:
    def setup_method(self):
        self.checks = _make_moonshine_checks()

    def test_count(self):
        assert len(self.checks) == 5

    def test_all_pass(self):
        failed = [c for c in self.checks if not c.passes]
        assert not failed, [c.name for c in failed]

    def test_j_at_i(self):
        assert 1728 == K**3

    def test_j_constant_formula(self):
        assert J_CONSTANT == Q * EDGES + 2 * K  # = 744

    def test_j_constant_value(self):
        assert J_CONSTANT == 744

    def test_leech_kissing_formula(self):
        assert LEECH_KISSING == EDGES * PHI3 * PHI6 * Q**2

    def test_leech_kissing_value(self):
        assert LEECH_KISSING == 196560

    def test_leech_dim_formula(self):
        assert LEECH_DIM == 2 * K  # = 24

    def test_j_coeff_formula(self):
        computed = LEECH_KISSING + (J_INV // 2) * Q**4
        assert J_COEFF_1 == computed

    def test_j_coeff_value(self):
        assert J_COEFF_1 == 196884


# ---------------------------------------------------------------------------
# Structural checks
# ---------------------------------------------------------------------------
class TestStructuralChecks:
    def setup_method(self):
        self.checks = _make_structural_checks()

    def test_count(self):
        assert len(self.checks) == 6

    def test_all_pass(self):
        failed = [c for c in self.checks if not c.passes]
        assert not failed, [c.name for c in failed]

    def test_thompson_v3(self):
        assert TH_P_ADIC[3] == PHI4  # = 10

    def test_prime_71_formula(self):
        assert PHI12 - 2 == 71

    def test_prime_71_in_monster(self):
        assert 71 in MONSTER_P_ADIC

    def test_bosonic_string(self):
        assert N_SPORADICS == 2 * PHI3 == 26

    def test_k_minus_1_formula(self):
        assert K - 1 == 11


# ---------------------------------------------------------------------------
# Full audit
# ---------------------------------------------------------------------------
class TestMoonshineAudit:
    def setup_method(self):
        self.result = monstrous_moonshine_bridge_audit()

    def test_status_pass(self):
        assert self.result["status"] == "PASS"

    def test_all_checks_pass(self):
        assert self.result["all_checks_pass"] is True

    def test_check_count(self):
        assert self.result["check_count"] == 44

    def test_checks_passing(self):
        assert self.result["checks_passing"] == 44

    def test_no_failed_checks(self):
        assert self.result["failed_checks"] == []

    def test_category_atom_count(self):
        assert self.result["category_counts"]["atom_checks"] == 9

    def test_category_monster_valuation_count(self):
        assert self.result["category_counts"]["monster_valuation_checks"] == 6

    def test_category_sporadic_count(self):
        assert self.result["category_counts"]["sporadic_structure_checks"] == 6

    def test_category_baby_monster_count(self):
        assert self.result["category_counts"]["baby_monster_checks"] == 4

    def test_category_m24_count(self):
        assert self.result["category_counts"]["m24_checks"] == 4

    def test_category_conway_count(self):
        assert self.result["category_counts"]["conway_checks"] == 4

    def test_category_moonshine_count(self):
        assert self.result["category_counts"]["moonshine_checks"] == 5

    def test_category_structural_count(self):
        assert self.result["category_counts"]["structural_checks"] == 6

    def test_sporadic_census_in_result(self):
        census = self.result["sporadic_census"]
        assert census["total"] == 26
        assert census["happy_family"] == 20
        assert census["pariahs"] == 6
        assert census["mathieu_groups"] == 5

    def test_leech_kissing_in_result(self):
        assert self.result["leech_kissing"] == 196560

    def test_j_coeff_in_result(self):
        assert self.result["j_coeff_1"] == 196884

    def test_theorem_present(self):
        assert "theorem_cxcv" in self.result
        assert len(self.result["theorem_cxcv"]) > 50

    def test_w33_atoms_in_result(self):
        atoms = self.result["w33_atoms"]
        assert atoms["Q"] == 3
        assert atoms["K"] == 12
        assert atoms["EDGES"] == 240

    def test_category_counts_sum(self):
        total = sum(self.result["category_counts"].values())
        assert total == 44
