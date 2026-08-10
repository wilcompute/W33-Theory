from pathlib import Path
import importlib.util
import json
import sys

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
sys.path.insert(0, str(ANALYSIS))


def load(name):
    path = ANALYSIS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def test_pass410_q9_complete_smith():
    payload = load("w33_pass410_prime_power_smith").build_payload()
    q9 = payload["instances"]["9"]
    assert payload["status"] == "PASS"
    assert q9["p_primary_elementary_divisors"] == {"3": 128, "9": 292, "27": 92, "81": 37, "729": 79}
    assert payload["q9_tree_order"]["prime_factorization"] == {"2": 1368, "3": 1610, "5": 288}


def test_pass411_magic_injection():
    payload, feedforward = load("w33_pass411_qutrit_magic_injection").build_payload()
    assert payload["status"] == "PASS"
    assert len(feedforward["entries"]) == 9
    assert payload["gate_teleportation"]["maximum_feedforward_word_length"] <= 3
    assert payload["magic_state"]["maximum_single_qutrit_stabilizer_fidelity"] < 1


def test_pass412_radius_three_is_sharp():
    payload = load("w33_pass412_multislip_sandpile_decoder").build_payload()
    assert payload["status"] == "PASS"
    assert payload["theorem"]["unique_net_error_radius"] == 3
    assert payload["theorem"]["sharp_failure_weight"] == 4
    assert payload["net_divisor_class_counts"]["cumulative_zero_through_weight_three"] == 9871057


def test_pass413_twirl_dimensions():
    payload, schedule = load("w33_pass413_automorphism_twirl").build_payload()
    assert payload["status"] == "PASS"
    assert payload["spatial_twirl"]["commutant_dimension"] == 4
    assert payload["spatial_twirl"]["spectral_sector_ranks"] == {"8": 1, "2": 12, "-1": 8, "-4": 6}
    assert len(schedule["epochs"]) == 64


def test_pass414_custody_and_schema():
    module = load("w33_pass414_independent_lab_packet")
    packet, fixture, template = module.build_payload()
    assert packet["status"] == "PASS"
    schema = json.loads((ROOT / "schemas/w33_pass414_independent_lab_handoff_v1.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(fixture, schema)
    jsonschema.validate(template, schema)
    assert fixture["claim_eligible"] is False
    assert fixture["physical_experiment_completed"] is False


def test_frozen_artifacts_are_all_pass():
    names = [
        "w33_pass410_prime_power_smith.json",
        "w33_pass411_qutrit_magic_injection.json",
        "w33_pass412_multislip_sandpile_decoder.json",
        "w33_pass413_automorphism_twirl.json",
        "w33_pass414_independent_lab_packet.json",
    ]
    for name in names:
        payload = json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))
        assert payload["status"] == "PASS"
        assert all(payload["checks"].values())
