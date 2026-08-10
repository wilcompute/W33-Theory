from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def read(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def test_pass400_minimal_control_certificate():
    p = read("w33_pass400_minimal_phase_control.json")
    assert p["status"] == "PASS"
    assert p["single_fibre_spectral_rank"] == 2
    assert p["global_control_rank"] == 18
    assert p["generated_lie_algebra"]["real_dimension"] == 2
    assert p["minimum_target_fidelity_exact"] == 1
    assert p["maximum_leakage_exact"] == 0


def test_pass401_critical_group_certificate():
    p = read("w33_pass401_critical_group_bockstein.json")
    assert p["status"] == "PASS"
    assert p["exact_full_smith_forms"]["3"]["216"] == 6
    assert p["exact_full_smith_forms"]["5"]["3000"] == 23
    assert p["q7_certified_primary_description"]["7_primary"] == "(Z/7)^176 + (Z/49)^35 + (Z/343)^47"
    assert p["bockstein_certificates"]["7"]["2"]["cumulative_divisibility_counts_p_p2_p3"] == [168, 126, 126]


def test_pass402_frontier_certificate():
    p = read("w33_pass402_quantum_classical_frontier.json")
    assert p["status"] == "PASS"
    q3a5 = next(c for c in p["cases"] if c["q"] == 3 and c["alpha"] == 5)
    q3a6 = next(c for c in p["cases"] if c["q"] == 3 and c["alpha"] == 6)
    assert q3a5["preserves_native_contraction_exactly"]
    assert not q3a6["preserves_native_contraction_exactly"]
    assert all(g["minimum_column_target_fidelity_exact"] == 1 and g["matrix_identity_verified"] for g in p["qutrit_gate_checks"])


def test_pass403_semilinear_certificate():
    p = read("w33_pass403_drackn_semilinear_classification.json")
    assert p["status"] == "PASS"
    orders = {c["q"]: c["permutation_group_order"] for c in p["cases"]}
    assert orders == {3: 1296, 5: 60000, 9: 8398080}
    assert all(c["all_generators_preserve_adjacency"] for c in p["cases"])


def test_pass404_compiler_certificate_and_schedule():
    p = read("w33_pass404_photonic_voltage_compiler.json")
    schedule = read("w33_pass404_photonic_voltage_schedule_q3.json")
    assert p["status"] == "PASS"
    assert p["native_hardware"]["layers"] == 9
    assert p["native_hardware"]["total_edges"] == 108
    assert p["control_hardware"]["couplers"] == 27
    assert len(schedule["native_layers"]) == 9
    assert all(len(layer["couplers"]) == 12 for layer in schedule["native_layers"])


def test_cross_pass_gate_alignment_and_claim_boundary():
    p400 = read("w33_pass400_minimal_phase_control.json")
    p404 = read("w33_pass404_photonic_voltage_compiler.json")
    assert p400["native_gate_time"] == p404["control_hardware"]["gate_time"]
    assert p404["blinded_choi_protocol"]["physical_experiment_completed"] is False
    assert p404["blinded_choi_protocol"]["study_type"] == "compiled_protocol_not_physical_data"
