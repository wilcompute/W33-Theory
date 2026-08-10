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


def test_pass415_frobenius_packets_and_index():
    payload = load("w33_pass415_frobenius_smith_packets").build_payload()
    assert payload["status"] == "PASS"
    assert payload["instances"]["9"]["frobenius_orbit_length_counts"] == {"1": 2, "2": 1}
    assert payload["instances"]["27"]["frobenius_orbit_length_counts"] == {"1": 1, "3": 4}
    assert payload["instances"]["27"]["conductor_index_p_valuation"] == 3


def test_pass416_protocol_specific_no_go():
    payload = load("w33_pass416_qutrit_distillation_search").build_payload()
    assert payload["status"] == "PASS"
    assert payload["result"]["classification"].startswith("direct-distillation no-go")
    assert 0.918 < payload["result"]["pure_input_best_return_fidelity"] < 0.919
    assert payload["reference_validation"]["pure_fixed_point_fidelity"] > 0.999999999999


def test_pass417_optimal_telemetry_bits():
    payload = load("w33_pass417_divisor_cycle_hybrid_decoder").build_payload()
    assert payload["status"] == "PASS"
    assert payload["zero_divisor_fibre"]["unordered_total"] == 6202
    assert payload["zero_divisor_fibre"]["ordered_total"] == 35803
    assert payload["theorem"]["minimum_unordered_bits"] == 13
    assert payload["theorem"]["minimum_time_ordered_bits"] == 16


def test_pass418_complete_defect_coordinates():
    payload, atlas = load("w33_pass418_twirl_breaking_spectroscopy").build_payload()
    assert payload["status"] == "PASS"
    assert len(atlas["entries"]) == 378
    assert sum(row["kernel_rank"] for row in payload["orbit_families"]) == 374
    assert all(row["localized"] for row in payload["injected_defect_recovery"])


def test_pass419_hardened_chain_and_attacks():
    module = load("w33_pass419_adversarial_replication")
    payload, fixture, attack_matrix, raw = module.build_payload()
    assert payload["status"] == "PASS"
    schema = json.loads((ROOT / "schemas/w33_pass419_hardened_handoff_v2.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(fixture, schema)
    assert module.verify_manifest(fixture) == []
    assert len(attack_matrix["attacks"]) == 12
    assert attack_matrix["all_attacks_rejected"]
    assert attack_matrix["all_expected_reasons_observed"]
    assert len(raw.decode().splitlines()) == 128


def test_all_frozen_primary_certificates_pass():
    names = [
        "w33_pass415_frobenius_smith_packets.json",
        "w33_pass416_qutrit_distillation_search.json",
        "w33_pass417_divisor_cycle_hybrid_decoder.json",
        "w33_pass418_twirl_breaking_spectroscopy.json",
        "w33_pass419_adversarial_replication.json",
    ]
    for name in names:
        payload = json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))
        assert payload["status"] == "PASS"
        assert all(payload["checks"].values())
