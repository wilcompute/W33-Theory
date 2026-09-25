import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10948_clock_tetracode_negacyclic_hyperbolic_bridge.py"
CERT = ROOT / "data/w33_pass10948_clock_tetracode_negacyclic_hyperbolic_bridge.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays():
    subprocess.run(
        [sys.executable, str(PRODUCER)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=40,
    )

def test_phi8_negacyclic_orientation_gauges():
    x = load()
    assert x["status"] == "PASS_CLOCK_TETRACODE_NEGACYCLIC_HYPERBOLIC_BRIDGE"
    assert x["frozen_clock_code"]["negacyclic_in_frozen_orientation"] is False
    f = x["phi8_factorization_mod3"]
    assert f["identity"] == "x^4+1=(x^2+x-1)(x^2-x-1) over F3"
    assert f["factors_are_reciprocal"] is True
    g = x["orientation_gauges"]
    assert g["plus"]["coordinate_signs"] == [1, 2, 1, 1]
    assert g["minus"]["coordinate_signs"] == [1, 1, 1, 2]


def test_order8_and_hyperbolic_pair():
    x = load()
    n = x["negacyclic_clock"]
    assert n["operator_order"] == 8
    assert n["N4"] == "-I"
    assert n["N8"] == "I"
    h = x["hyperbolic_pair"]
    assert h["plus_is_totally_isotropic"] is True
    assert h["minus_is_totally_isotropic"] is True
    assert h["intersection_dimension"] == 0
    assert h["ambient_direct_sum_dimension"] == 4
    assert h["cross_pairing_matrix_in_polynomial_bases"] == [[1, 1], [2, 1]]
    assert h["cross_pairing_determinant_mod3"] == 2
    assert h["cross_pairing_nondegenerate"] is True
    assert h["cyclotomic_inversion_swaps_sectors"] is True


def test_signed_monomial_orbit_census():
    o = load()["monomial_orbit"]
    assert o["signed_permutation_group_order"] == 384
    assert o["distinct_tetracode_images"] == 8
    assert o["stabilizer_order"] == 48
    assert o["distinct_negacyclic_images"] == 2
    assert o["signed_permutation_gauges_yielding_negacyclicity"] == 96
    assert o["gauges_per_negacyclic_image"] == 48


def test_repo_welds_are_explicit_and_bounded():
    x = load()
    w = x["repo_welds"]
    assert "oriented P1(F3)" in w["pass10946"]
    assert "reciprocal Phi_8 factors" in w["pass9961_9984"]
    assert w["existing_E8_glue"] == "240 = 4*6 + 8*27"
    assert "not a physical arrow of time" in x["boundary"]
