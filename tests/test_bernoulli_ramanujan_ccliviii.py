"""
Part CCLVIII — Bernoulli, Ramanujan 691, W(3,3) small-prime tower
Regression tests for exploration/PART_CCLVIII_BERNOULLI_RAMANUJAN_BRIDGE.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCLVIII_BERNOULLI_RAMANUJAN_BRIDGE import (
    Q, V, K, LAM, MU, F, G, EDGES,
    PHI3, PHI4, PHI6,
    PRIME_FORMS, DEN_W33_FORMS,
    RAM_691_FORM_A, RAM_691_FORM_B, RAM_691_LARGER, RAM_691_SHIFT,
    den_bernoulli, checks, Verified,
)


# ------------------------------------------------------------------
# Master gates
# ------------------------------------------------------------------
def test_verified_true():
    assert Verified is True


def test_all_bridge_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == []


def test_check_count():
    assert len(checks) == 36


# ------------------------------------------------------------------
# Small-prime closed forms
# ------------------------------------------------------------------
def test_prime_2_lam():
    assert PRIME_FORMS[2] == LAM == 2


def test_prime_3_q():
    assert PRIME_FORMS[3] == Q == 3


def test_prime_5_mu_plus_1():
    assert PRIME_FORMS[5] == MU + 1 == 5


def test_prime_7_phi6():
    assert PRIME_FORMS[7] == PHI6 == 7


def test_prime_11_k_minus_1():
    assert PRIME_FORMS[11] == K - 1 == 11


def test_prime_13_phi3():
    assert PRIME_FORMS[13] == PHI3 == 13


def test_prime_17_phi3_plus_mu():
    assert PRIME_FORMS[17] == PHI3 + MU == 17


def test_prime_19_f_minus_mu_minus_1():
    assert PRIME_FORMS[19] == F - MU - 1 == 19


def test_prime_23_phi3_plus_phi4():
    assert PRIME_FORMS[23] == PHI3 + PHI4 == 23


def test_nine_primes_total():
    # # small W(3,3) primes <= 23 = q^2 = 9
    assert len(PRIME_FORMS) == Q ** 2


def test_sum_primes_phi4_squared():
    # 2+3+5+7+11+13+17+19+23 = 100 = Phi_4^2
    assert sum(PRIME_FORMS.keys()) == PHI4 ** 2


# ------------------------------------------------------------------
# Bernoulli denominators
# ------------------------------------------------------------------
def test_den_b2():
    assert den_bernoulli(2) == DEN_W33_FORMS[2] == LAM * Q == 6


def test_den_b4_eq_h_e8():
    # den(B_4) = 30 = h(E_8) Coxeter number !
    assert den_bernoulli(4) == DEN_W33_FORMS[4] == Q * PHI4 == 30


def test_den_b6():
    assert den_bernoulli(6) == DEN_W33_FORMS[6] == LAM * Q * PHI6 == 42


def test_den_b8():
    assert den_bernoulli(8) == DEN_W33_FORMS[8] == 30


def test_den_b10():
    assert den_bernoulli(10) == DEN_W33_FORMS[10] == LAM * Q * (K - 1) == 66


def test_den_b12():
    # The MAIN identity: den(B_12) = 2730 = lam*q*(mu+1)*Phi_6*Phi_3
    assert den_bernoulli(12) == DEN_W33_FORMS[12] == 2730
    assert DEN_W33_FORMS[12] == LAM * Q * (MU + 1) * PHI6 * PHI3


def test_den_b14():
    assert den_bernoulli(14) == 6


def test_den_b16():
    assert den_bernoulli(16) == DEN_W33_FORMS[16] == LAM * Q * (MU + 1) * (PHI3 + MU) == 510


def test_den_b18():
    assert den_bernoulli(18) == DEN_W33_FORMS[18] == LAM * Q * PHI6 * (F - MU - 1) == 798


def test_den_b20():
    assert den_bernoulli(20) == DEN_W33_FORMS[20] == LAM * Q * (MU + 1) * (K - 1) == 330


def test_den_b22():
    assert den_bernoulli(22) == DEN_W33_FORMS[22] == LAM * Q * (PHI3 + PHI4) == 138


def test_den_b24():
    assert den_bernoulli(24) == DEN_W33_FORMS[24] == 2730


# ------------------------------------------------------------------
# Ramanujan 691 prime
# ------------------------------------------------------------------
def test_ram_691_form_a():
    assert RAM_691_FORM_A == 691


def test_ram_691_form_b():
    assert RAM_691_FORM_B == 691


def test_ram_691_forms_agree():
    assert RAM_691_FORM_A == RAM_691_FORM_B == 691


def test_ram_691_decomposition():
    # 691 = 640 + 51
    assert RAM_691_LARGER + RAM_691_SHIFT == 691
    assert RAM_691_LARGER == 640
    assert RAM_691_SHIFT == 51


def test_ram_691_640_two_forms():
    # 640 = lam*v*lam^q = lam^Phi_6 * (mu+1) = 128 * 5 = 80 * 8 (=lam*v*lam^q...)
    assert LAM * V * LAM ** Q == 640
    assert LAM ** PHI6 * (MU + 1) == 640


def test_ram_691_51():
    # 51 = q * (Phi_3 + mu) = 3 * 17
    assert Q * (PHI3 + MU) == 51


def test_ram_691_prime():
    # 691 is prime
    for d in range(2, 27):
        assert 691 % d != 0


# ------------------------------------------------------------------
# Cross-link: weight 11 = k-1 in Eisenstein E_12
# ------------------------------------------------------------------
def test_weight_11_eq_k_minus_1():
    # Ramanujan: tau(n) ≡ sigma_11(n) mod 691
    # weight 11 = k - 1
    assert 11 == K - 1


# ------------------------------------------------------------------
# Cross-link: B_4 denom = 30 = h(E_8)
# ------------------------------------------------------------------
def test_h_e8_eq_den_b4():
    h_E8 = Q * PHI4
    assert h_E8 == 30 == den_bernoulli(4)


# ------------------------------------------------------------------
# JSON output
# ------------------------------------------------------------------
def test_json_exists():
    assert (ROOT / "PART_CCLVIII_bernoulli_ramanujan_results.json").exists()


def test_json_verified():
    data = json.loads((ROOT / "PART_CCLVIII_bernoulli_ramanujan_results.json").read_text(encoding="utf-8"))
    assert data["Verified"] is True
    assert data["checks_passed"] == data["checks_total"] == 36


def test_json_ramanujan_value():
    data = json.loads((ROOT / "PART_CCLVIII_bernoulli_ramanujan_results.json").read_text(encoding="utf-8"))
    assert data["ramanujan_691"]["value"] == 691


def test_json_b12_denom():
    data = json.loads((ROOT / "PART_CCLVIII_bernoulli_ramanujan_results.json").read_text(encoding="utf-8"))
    assert data["bernoulli_denominators"]["B_12"]["denom"] == 2730


def test_json_tower_count():
    data = json.loads((ROOT / "PART_CCLVIII_bernoulli_ramanujan_results.json").read_text(encoding="utf-8"))
    assert data["tower_summary"]["count"] == 9
    assert data["tower_summary"]["count_eq_q_squared"] is True
    assert data["tower_summary"]["sum"] == 100
    assert data["tower_summary"]["sum_eq_phi4_squared"] is True
