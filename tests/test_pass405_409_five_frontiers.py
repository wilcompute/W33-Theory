from __future__ import annotations
import base64
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def read(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def test_pass405_universal_critical_group():
    p = read("w33_pass405_universal_critical_group.json")
    assert p["status"] == "PASS"
    assert p["theorem_scope"].endswith("every odd prime q=p")
    p11 = p["instances"]["11"]
    assert p11["order_matches_decomposition"]
    assert p11["p_primary_elementary_counts"]["1331"] == 119
    assert p11["p_primary_elementary_counts"]["121"] == 165


def test_pass406_complete_qutrit_clifford_compiler():
    p = read("w33_pass406_nonabelian_clifford_compiler.json")
    s = read("w33_pass406_qutrit_clifford_schedule.json")
    assert p["status"] == "PASS"
    assert p["control_family"]["lie_dimension"] == 8
    assert p["clifford_compiler"]["projective_group_order"] == 216
    assert p["clifford_compiler"]["maximum_shortest_word_length"] == 7
    assert len(s["elements"]) == 216
    assert {e["word"] for e in s["elements"]} >= {"I", "X", "Z", "F", "P"}


def test_pass407_sandpile_decoder():
    p = read("w33_pass407_sandpile_calibration_memory.json")
    d = read("w33_pass407_single_slip_decoder_q3.json")
    assert p["status"] == "PASS"
    assert p["exact_decoder"]["oriented_single_slip_states"] == 702
    assert p["exact_decoder"]["minimum_pairwise_linf_ticks"] == 23
    assert d["shape"] == [702, 26]
    raw = zlib.decompress(base64.b64decode(d["syndrome_data"]))
    rows = [raw[i * 26:(i + 1) * 26] for i in range(702)]
    assert len(set(rows)) == 702


def test_pass408_full_automorphism_theorem():
    p = read("w33_pass408_full_automorphism_theorem.json")
    assert p["status"] == "PASS"
    assert p["instances"]["3"]["full_automorphism_order"] == 1296
    assert p["instances"]["5"]["full_automorphism_order"] == 60000
    assert p["instances"]["9"]["full_automorphism_order"] == 8398080
    assert p["instances"]["5"]["multiplier_index"] == 4


def test_pass409_hardware_falsifier_and_claim_boundary():
    p = read("w33_pass409_sealed_hardware_falsifier.json")
    bom = read("w33_pass409_vendor_neutral_bom.json")
    protocol = read("w33_pass409_preregistered_protocol.json")
    power = read("w33_pass409_nonclaim_power_study.json")
    raw = read("w33_pass409_nonclaim_raw_counts.json")
    assert p["status"] == "PASS"
    assert bom["compiled_counts"]["native_coupler_activations"] == 108
    assert protocol["physical_experiment_completed"] is False
    assert power["ideal_familywise_false_reject_log10_upper_bound"] < -1.3
    assert power["stuck_identity_false_pass_log10_upper_bound"] < -2
    assert raw["blinded"] is True and raw["gate_labels_present"] is False


def test_cross_pass_control_memory_and_falsifier_alignment():
    clifford = read("w33_pass406_nonabelian_clifford_compiler.json")
    memory = read("w33_pass407_sandpile_calibration_memory.json")
    protocol = read("w33_pass409_preregistered_protocol.json")
    assert clifford["clifford_compiler"]["projective_group_order"] == 216
    assert memory["exact_decoder"]["modulus_ticks"] == 216
    assert set(protocol["gates"]) == {"I", "X", "Z", "F3"}
