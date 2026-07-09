"""Regression tests for Pass 157's exact W33 +2-eigenlattice structure."""

from __future__ import annotations

import json
from pathlib import Path

from analysis import w33_pass157_eigenlattice_prime_collision as pass157


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "data" / "w33_pass157_eigenlattice_prime_collision.json"


def load_certificate() -> dict:
    return json.loads(CERTIFICATE.read_text(encoding="utf-8"))


def test_pass157_regenerates_exact_certificate() -> None:
    assert pass157.main() == 0
    data = load_certificate()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())


def test_pass157_closes_the_primary_decomposition() -> None:
    data = load_certificate()
    assert data["lattice"]["determinant"] == 2**16 * 3**10 * 5
    assert data["lattice"]["smith_profile"] == {
        "1": 8,
        "2": 6,
        "6": 9,
        "30": 1,
    }
    assert {
        prime: block["radical_dimension"]
        for prime, block in data["primary_radicals"].items()
    } == {"2": 16, "3": 10, "5": 1}
    assert data["primary_radicals"]["3"]["operator_identity"] == "(A+I)^2 = J mod 3"


def test_pass157_identifies_the_complete_minimal_shell() -> None:
    shell = load_certificate()["minimal_shell"]
    assert shell["minimal_norm"] == 6
    assert shell["minimal_vector_count"] == 480
    assert shell["ordered_local_line_pairs"] == 480
    assert shell["projective_minimal_rays"] == shell["axis_endpoints"] == 240
    assert shell["local_axes"] == 120
    assert shell["local_inner_product_profile"] == {
        "-6": 1,
        "-3": 4,
        "-2": 45,
        "-1": 108,
        "0": 164,
        "1": 108,
        "2": 45,
        "3": 4,
        "6": 1,
    }
