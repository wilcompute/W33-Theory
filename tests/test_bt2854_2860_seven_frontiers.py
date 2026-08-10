from __future__ import annotations
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("release", ROOT / "analysis" / "bt2854_2860_seven_frontiers.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MOD)


def test_all_packets_and_count():
    result = MOD.build_all()
    assert result["total_exact_checks"] == 68
    assert result["status"].startswith("COMPLETE")


def test_polarization_groupoid():
    p = MOD.pass2854()
    assert p["groupoid"]["projective_arrows"] == 288
    assert p["fixed_polarization"]["permutation_projection_order"] == 8


def test_boolean_terwilliger():
    p = MOD.pass2855()
    assert p["support_S4_decomposition"] == {"[4]": 4, "[31]": 3, "[22]": 1}
    assert p["Q4_Terwilliger"]["generated_algebra_dimension"] == 35


def test_codec_and_fusion():
    assert all(MOD.decode_affine(MOD.encode_affine(v)) == v for v in MOD.product(range(3), repeat=4))
    assert MOD.pass2857()["valid_control_states"] == 96


def test_quantum_coarse_graining():
    p = MOD.pass2858()
    assert p["Weyl_noise_theorem"]["solution_space_dimension"] == 16
    assert p["deterministic_gate_theorem"]["support_descending_invertible_linear_maps"] == 384


def test_hadamard_and_green():
    assert MOD.pass2859()["global_spectrum"] == {"+q^2": 10, "-q^2": 6}
    p = MOD.pass2860()
    assert p["q3_atlas"]["minimum"] == "9/2"
    assert p["q3_atlas"]["maximum"] == "42"


def test_frozen_files():
    result = MOD.build_all()
    aggregate = json.loads((ROOT / "data" / "PART_BT2854_BT2860_SEVEN_FRONTIERS_results.json").read_text(encoding="utf-8"))
    assert aggregate == result
