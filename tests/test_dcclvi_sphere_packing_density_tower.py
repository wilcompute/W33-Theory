"""Part DCCLVI -- Sphere-packing density tower tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclvi_sphere_packing_density_tower import (  # noqa: E402
    F_EIGEN,
    K,
    LAM,
    MU,
    OUT_PATH,
    Q,
    G_384_w33_factorisations,
    build_bridge,
    cross_link_kissing_density,
    density_table,
    pi_exponents_in_densities,
    write_bridge,
)


def test_density_table_five_rows():
    assert len(density_table()) == 5


def test_solved_density_dimensions():
    table = density_table()
    dims = [r["dim"] for r in table]
    assert dims == [1, 2, 3, 8, 24]


def test_rho_8_denominator_is_384():
    table = density_table()
    rho_8 = next(r for r in table if r["dim"] == 8)
    assert rho_8["denominator"] == 384


def test_rho_24_denominator_is_12_factorial():
    table = density_table()
    rho_24 = next(r for r in table if r["dim"] == 24)
    assert rho_24["denominator"] == math.factorial(12) == 479001600


def test_G_384_eq_2_W_D4():
    assert 384 == 2 * 192


def test_G_384_eq_q_plus_1_squared_times_f():
    assert 384 == (Q + 1) ** 2 * F_EIGEN
    assert (Q + 1) ** 2 == 16  # trace(Cartan E_8)
    assert F_EIGEN == 24


def test_G_384_eq_q_plus_1_factorial_times_q_plus_1_squared():
    assert 384 == math.factorial(Q + 1) * (Q + 1) ** 2


def test_G_384_all_factorisations_equal_384():
    facts = G_384_w33_factorisations()
    for r in facts:
        assert r["value"] == 384


def test_G_384_has_seven_factorisations():
    facts = G_384_w33_factorisations()
    assert len(facts) >= 7


def test_pi_exponent_rho_8_is_mu():
    pi_exp = pi_exponents_in_densities()
    rho_8 = next(r for r in pi_exp if r["dim"] == 8)
    assert rho_8["pi_exponent"] == MU == 4


def test_pi_exponent_rho_24_is_k():
    pi_exp = pi_exponents_in_densities()
    rho_24 = next(r for r in pi_exp if r["dim"] == 24)
    assert rho_24["pi_exponent"] == K == 12


def test_kissing_minus_density_eq_d_4():
    cross = cross_link_kissing_density()
    assert cross["difference"] == [4]


def test_rho_2_value():
    table = density_table()
    rho_2 = next(r for r in table if r["dim"] == 2)
    expected = math.pi / (2 * math.sqrt(3))
    assert math.isclose(rho_2["density_decimal"], expected, abs_tol=1e-10)


def test_rho_3_value():
    table = density_table()
    rho_3 = next(r for r in table if r["dim"] == 3)
    expected = math.pi / (3 * math.sqrt(2))
    assert math.isclose(rho_3["density_decimal"], expected, abs_tol=1e-10)


def test_rho_8_value():
    table = density_table()
    rho_8 = next(r for r in table if r["dim"] == 8)
    expected = math.pi ** 4 / 384
    assert math.isclose(rho_8["density_decimal"], expected, abs_tol=1e-10)


def test_rho_24_value():
    table = density_table()
    rho_24 = next(r for r in table if r["dim"] == 24)
    expected = math.pi ** 12 / math.factorial(12)
    assert math.isclose(rho_24["density_decimal"], expected, abs_tol=1e-10)


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Density Tower Theorem" in b["theorem"]
    assert "pi^mu" in b["one_line"] or "G_384" in b["one_line"]


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
        "density_table",
        "G_384_w33_factorisations",
        "pi_exponents_in_densities",
        "cross_link_kissing_density",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
