"""Part DCCLXVI -- octahedral matrix-tree / density-denominator tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxvi_octahedral_matrix_tree_density_bridge import (  # noqa: E402
    F_EIGEN,
    G_384,
    MU,
    OUT_PATH,
    Q,
    W_D4_ORDER,
    bareiss_det,
    build_bridge,
    density_denominator_bridge,
    integer_octahedral_laplacian,
    matrix_tree_data,
    principal_minor,
    spectral_zeta_data,
    write_bridge,
)


def test_laplacian_spectrum_is_octahedral():
    data = matrix_tree_data()
    assert data["laplacian_spectrum"] == [0, 4, 4, 4, 6, 6]


def test_det_prime_laplacian_is_2304():
    data = matrix_tree_data()
    assert data["det_prime_laplacian"] == 4**3 * 6**2 == 2304


def test_matrix_tree_count_from_spectrum_is_384():
    data = matrix_tree_data()
    assert data["spanning_tree_count_from_spectrum"] == 384 == G_384


def test_all_principal_cofactors_are_384():
    data = matrix_tree_data()
    assert data["all_principal_cofactors_equal"] is True
    assert data["principal_cofactors"] == [384] * 6


def test_bareiss_minor_matches_matrix_tree_count():
    L = integer_octahedral_laplacian()
    minor = principal_minor(L, 0)
    assert bareiss_det(minor) == 384


def test_rho_8_denominator_equals_tree_count():
    tree = matrix_tree_data()
    density = density_denominator_bridge()
    assert density["rho_8_denominator"] == tree["matrix_tree_count"] == 384


def test_G_384_factorisations_remain_exact():
    density = density_denominator_bridge()
    assert all(row["value"] == 384 for row in density["G_384_factorisations"])
    assert 384 == 2 * W_D4_ORDER
    assert 384 == MU**2 * F_EIGEN
    assert 384 == math.factorial(Q) * MU**3


def test_additional_factorisations_include_tree_count():
    density = density_denominator_bridge()
    formulas = {row["formula"] for row in density["additional_factorisations"]}
    assert "tau(O)" in formulas
    assert "q! * (q+1)^3" in formulas


def test_spectral_zeta_rank_and_det():
    zeta = spectral_zeta_data()
    assert zeta["zeta_at_0"] == zeta["rank_laplacian"] == 5
    assert zeta["regularized_det"] == zeta["det_prime_laplacian"] == 2304


def test_spectral_zeta_logdet_identity():
    zeta = spectral_zeta_data()
    assert math.isclose(zeta["minus_zeta_prime_at_0"], math.log(2304), abs_tol=1e-12)


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Matrix-Tree" in b["theorem"]
    assert "384" in b["one_line"]


def test_honesty_boundary_mentions_viazovska():
    b = build_bridge()
    assert "Viazovska" in b["honesty_boundary"]


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert data["summary"]["spanning_tree_count"] == 384


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "matrix_tree_data",
        "spectral_zeta_data",
        "density_denominator_bridge",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
