"""
Tests for Part CCXXXVI — Moonshine and the Monster Group
SRG(40,12,2,4) constants.

~70 tests across 10 classes.
"""

import json
from pathlib import Path
import pytest

from PART_CCXXXVI_MOONSHINE_MONSTER_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, EDGES, AUT_ORDER,
    dim_E8, kissing_Leech, dim_Leech, phi3_Q,
    j_at_i, j_constant, j_constant_div_Q,
    prime_4K_1, prime_5K_1, prime_6K_1,
    monster_irrep_1, j_coeff_196884, j_coeff_via_leech,
    monster_max_order,
    central_charge_Vsharp,
    j_vanishes_at_Q,
    dim_E8_check,
    checks, Verified,
)

ROOT = Path(__file__).resolve().parents[1]


class TestBridgeMetadata:
    def test_verified_true(self):
        assert Verified is True

    def test_all_checks_pass(self):
        failed = [lbl for lbl, v in checks if not v]
        assert failed == [], f"Failed checks: {failed}"

    def test_check_count_at_least_30(self):
        assert len(checks) >= 30

    def test_json_exists(self):
        assert (ROOT / "PART_CCXXXVI_moonshine_monster_results.json").exists()

    def test_json_verified(self):
        d = json.loads((ROOT / "PART_CCXXXVI_moonshine_monster_results.json").read_text(encoding="utf-8"))
        assert d["Verified"] is True

    def test_json_checks_equal(self):
        d = json.loads((ROOT / "PART_CCXXXVI_moonshine_monster_results.json").read_text(encoding="utf-8"))
        assert d["checks_passed"] == d["checks_total"]


class TestSRGParameters:
    def test_Q(self):
        assert Q == 3

    def test_K(self):
        assert K == 12

    def test_LAM(self):
        assert LAM == 2

    def test_MU(self):
        assert MU == 4

    def test_EDGES(self):
        assert EDGES == 240


class TestJFunctionAtI:
    """B1: j(i) = 1728 = K³."""

    def test_j_at_i_value(self):
        assert j_at_i == 1728

    def test_j_at_i_eq_K_cubed(self):
        assert j_at_i == K**3

    def test_K_cubed_value(self):
        assert K**3 == 1728

    def test_j_i_from_K(self):
        assert K**3 == 1728


class TestJConstant744:
    """B2: j-function constant offset 744 = Q·dim(E₈)."""

    def test_j_constant_value(self):
        assert j_constant == 744

    def test_j_constant_eq_Q_times_dim_E8(self):
        assert j_constant == Q * dim_E8

    def test_Q_times_EDGES_plus_2MU(self):
        assert Q * (EDGES + 2 * MU) == 744

    def test_dim_E8_value(self):
        assert dim_E8 == 248

    def test_dim_E8_eq_EDGES_plus_2MU(self):
        assert dim_E8 == EDGES + 2 * MU

    def test_j_constant_div_Q_eq_dim_E8(self):
        assert j_constant_div_Q == dim_E8

    def test_j_constant_is_Q_times_248(self):
        assert j_constant == Q * 248


class TestMonsterPrimeFactors:
    """B3: Three largest Monster prime factors = 4K-1, 5K-1, 6K-1."""

    def test_prime_47_eq_4K_minus_1(self):
        assert prime_4K_1 == 4 * K - 1

    def test_prime_47_value(self):
        assert prime_4K_1 == 47

    def test_prime_59_eq_5K_minus_1(self):
        assert prime_5K_1 == 5 * K - 1

    def test_prime_59_value(self):
        assert prime_5K_1 == 59

    def test_prime_71_eq_6K_minus_1(self):
        assert prime_6K_1 == 6 * K - 1

    def test_prime_71_value(self):
        assert prime_6K_1 == 71

    def test_three_primes_form_AP_in_K(self):
        # 4K-1, 5K-1, 6K-1 are arithmetic progression with common difference K
        assert prime_5K_1 - prime_4K_1 == K
        assert prime_6K_1 - prime_5K_1 == K


class TestMonsterSmallestIrrep:
    """B4: Smallest nontrivial Monster irrep = (4K-1)(5K-1)(6K-1) = 196883."""

    def test_monster_irrep_1_value(self):
        assert monster_irrep_1 == 196883

    def test_monster_irrep_1_factored(self):
        assert monster_irrep_1 == prime_4K_1 * prime_5K_1 * prime_6K_1

    def test_monster_irrep_1_K_formula(self):
        assert (4 * K - 1) * (5 * K - 1) * (6 * K - 1) == 196883

    def test_monster_irrep_eq_47_times_59_times_71(self):
        assert monster_irrep_1 == 47 * 59 * 71


class TestJCoefficient196884:
    """B5/B6: j-coefficient 196884 from two independent SRG formulas."""

    def test_j_coeff_McKay_value(self):
        assert j_coeff_196884 == 196884

    def test_j_coeff_McKay_eq_irrep_plus_1(self):
        assert j_coeff_196884 == monster_irrep_1 + 1

    def test_j_coeff_via_leech_value(self):
        assert j_coeff_via_leech == 196884

    def test_j_coeff_via_leech_formula(self):
        assert kissing_Leech + (K // 2 * Q)**2 == 196884

    def test_kissing_plus_324(self):
        assert kissing_Leech + 324 == 196884

    def test_K_half_Q_squared(self):
        assert (K // 2 * Q)**2 == 324

    def test_both_j_formulas_agree(self):
        assert j_coeff_196884 == j_coeff_via_leech


class TestMonsterMaxOrder:
    """B7: Monster maximum element order = EDGES/2 - 1 = 119."""

    def test_monster_max_order_value(self):
        assert monster_max_order == 119

    def test_monster_max_order_eq_EDGES_half_minus_1(self):
        assert monster_max_order == EDGES // 2 - 1

    def test_EDGES_half_minus_1(self):
        assert EDGES // 2 - 1 == 119


class TestMoonshineModule:
    """B8/B9: Central charge of V^♮ and j vanishing."""

    def test_central_charge_value(self):
        assert central_charge_Vsharp == 24

    def test_central_charge_eq_K_LAM(self):
        assert central_charge_Vsharp == K * LAM

    def test_central_charge_eq_dim_Leech(self):
        assert central_charge_Vsharp == dim_Leech

    def test_j_vanishes_at_Q_is_true(self):
        assert j_vanishes_at_Q is True

    def test_Q_is_3_cube_root_connection(self):
        # j(e^{2πi/Q}) = 0 only because Q=3; verify Q=3
        assert Q == 3


class TestCrossChecks:
    """Cross-verification identities across all moonshine bridges."""

    def test_j_constant_equals_Q_dim_E8(self):
        assert j_constant == Q * (EDGES + 2 * MU)

    def test_j_i_K_cubed(self):
        assert j_at_i == K**3

    def test_monster_prime_product_196883(self):
        assert prime_4K_1 * prime_5K_1 * prime_6K_1 == 196883

    def test_j_196884_both_formulas(self):
        assert j_coeff_196884 == j_coeff_via_leech

    def test_dim_E8_check(self):
        assert dim_E8_check == 248

    def test_j_constant_3_times_248(self):
        assert j_constant == 3 * 248
