"""Part DCCLIII -- Monster Moonshine W(3,3) bridge tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccliii_monster_moonshine_w33_bridge import (  # noqa: E402
    DIM_E8,
    E_VAL,
    F_EIGEN,
    G_EIGEN,
    K,
    LAM,
    MONSTER_PRIME_FACTORIZATION,
    MU,
    OUT_PATH,
    PHI_3,
    PHI_4,
    PHI_6,
    Q,
    THETA,
    V,
    build_bridge,
    fifteen_identifications,
    j_constant_196884_decomposition,
    j_constant_744_decompositions,
    leech_kissing_number,
    monster_prime_count,
    monster_w33_prime_table,
    moonshine_central_integers,
    ramanujan_tau,
    write_bridge,
)


def test_monster_has_15_primes():
    assert monster_prime_count() == 15 == G_EIGEN


def test_15_equals_M4_mersenne():
    assert 15 == (1 << 4) - 1


def test_15_equals_T5_triangular():
    assert 15 == 5 * 6 // 2


def test_15_equals_C_6_2():
    assert 15 == math.comb(6, 2)


def test_monster_prime_2_exponent_46_eq_v_plus_q_fact():
    assert MONSTER_PRIME_FACTORIZATION[2] == 46 == V + math.factorial(Q)


def test_monster_prime_3_exponent_20_eq_2_theta():
    assert MONSTER_PRIME_FACTORIZATION[3] == 20 == 2 * THETA


def test_monster_prime_5_exponent_9_eq_q_squared():
    assert MONSTER_PRIME_FACTORIZATION[5] == 9 == Q ** 2


def test_monster_prime_7_exponent_6_eq_q_factorial():
    assert MONSTER_PRIME_FACTORIZATION[7] == 6 == math.factorial(Q)


def test_monster_prime_11_exponent_2_eq_lambda():
    assert MONSTER_PRIME_FACTORIZATION[11] == 2 == LAM


def test_monster_prime_13_exponent_3_eq_q():
    assert MONSTER_PRIME_FACTORIZATION[13] == 3 == Q


def test_nine_supersingular_primes_exp_1():
    supersingular = {p: e for p, e in MONSTER_PRIME_FACTORIZATION.items()
                     if p >= 17}
    assert len(supersingular) == 9
    for e in supersingular.values():
        assert e == 1


def test_total_distinct_primes_6_plus_9_eq_15():
    multi = sum(1 for e in MONSTER_PRIME_FACTORIZATION.values() if e > 1)
    single = sum(1 for e in MONSTER_PRIME_FACTORIZATION.values() if e == 1)
    assert multi == 6
    assert single == 9
    assert multi + single == 15 == G_EIGEN


def test_j_constant_744_eq_q_times_dim_E8():
    j = j_constant_744_decompositions()
    assert j["decomposition_q_times_dim_E8"]["match"] is True
    assert j["decomposition_q_times_dim_E8"]["value"] == 744 == Q * DIM_E8


def test_j_constant_744_eq_31_times_24():
    j = j_constant_744_decompositions()
    assert j["decomposition_31_times_24"]["match"] is True
    assert (2 ** (Q + LAM) - 1) == 31


def test_j_constant_744_eq_q_times_E_plus_2q():
    j = j_constant_744_decompositions()
    assert j["decomposition_q_times_E_plus_lambda_q"]["match"] is True
    assert E_VAL + LAM ** Q == DIM_E8


def test_j_constant_196884_decomposition():
    j = j_constant_196884_decomposition()
    assert j["match"] is True
    assert j["leech_kissing_term"] == 196560
    assert j["mu_q4_correction"] == 324
    assert j["sum"] == 196884


def test_leech_kissing_eq_196560():
    leech = leech_kissing_number()
    assert leech["matches_196560"] is True
    assert leech["value"] == E_VAL * Q ** 2 * PHI_6 * PHI_3 == 196560


def test_tau_2_eq_minus_f():
    tau = ramanujan_tau()
    assert tau["tau_2"]["match"] is True
    assert tau["tau_2"]["value"] == -F_EIGEN == -24


def test_tau_3_eq_C_10_5():
    tau = ramanujan_tau()
    assert tau["tau_3"]["match"] is True
    assert tau["tau_3"]["value"] == 252 == math.comb(THETA, Q + LAM)


def test_central_moonshine_integers():
    central = moonshine_central_integers()
    assert len(central) == 5
    values = [c["integer"] for c in central]
    assert values == [12, 24, 27, 54, 248]
    assert 12 == K
    assert 24 == F_EIGEN
    assert 27 == Q ** Q
    assert 54 == 2 * Q ** Q
    assert 248 == DIM_E8


def test_fifteen_identifications_consistent():
    rows = fifteen_identifications()
    for r in rows:
        assert r["value"] == 15


def test_monster_table_15_rows():
    assert len(monster_w33_prime_table()) == 15


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Monster Moonshine" in b["theorem"]
    assert "15" in b["one_line"]


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "monster_w33_prime_table",
        "j_constant_744_decompositions",
        "j_constant_196884",
        "leech_kissing_number",
        "ramanujan_tau_values",
        "moonshine_central_integers",
        "fifteen_equals_g_identifications",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
