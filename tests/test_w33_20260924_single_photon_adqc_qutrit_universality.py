import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_20260924_single_photon_adqc_qutrit_universality.py"
DATA = ROOT / "data/w33_20260924_single_photon_adqc_qutrit_universality.json"


def load_module():
    spec = importlib.util.spec_from_file_location("adqc10942", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_exact_certificate_rebuilds():
    mod = load_module()
    c = mod.build_certificate()
    assert c["status"] == "PASS_FIXED_INTERACTION_ADAPTIVE_MEASUREMENT_QUTRIT_UNIVERSALITY"
    assert max(c["checks"].values()) < 2e-12


def test_local_programming_is_deterministic_up_to_pauli_frame():
    c = load_module().build_certificate()
    rows = c["local_gate_theorem"]["phase_trials"]
    assert len(rows) == 17
    assert max(r["basis_unitarity_error"] for r in rows) < 2e-12
    assert max(r["max_gate_error"] for r in rows) < 2e-12
    assert max(r["max_probability_operator_error"] for r in rows) < 2e-12
    assert c["local_gate_theorem"]["branch_probability"] == "1/3 for every input state and every m"


def test_same_fixed_interaction_entangles_two_memories():
    c = load_module().build_certificate()["two_memory_entangler"]
    assert c["max_gate_error"] < 2e-12
    assert c["max_probability_operator_error"] < 2e-12
    assert c["recover_CZ_with_local_F_dagger_error"] < 2e-12


def test_nonclifford_power_is_in_analyzer_program():
    c = load_module().build_certificate()
    t = c["non_clifford_gate"]
    assert t["max_branch_error"] < 2e-12
    assert t["T_X_Tdag_nearest_pauli_projective_distance"] > 1.0
    assert t["analyzer_max_single_qutrit_stabilizer_fidelity"] < 0.8
    assert "measurement" in t["analyzer_resource_statement"]
    compiler = c["universal_gate_compiler"]
    assert "online magic-state" in compiler["resource_relocation"]
    assert "analyzer basis" in compiler["fault_tolerance_boundary"]


def test_single_particle_memory_scaling_is_explicitly_rejected():
    c = load_module().build_certificate()["single_particle_scaling_no_go"]
    table = {r["logical_qutrits"]: r["minimum_orthogonal_single_particle_modes"] for r in c["table"]}
    assert table[1] == 3
    assert table[6] == 729
    assert table[12] == 531441
    assert "mobile head/bus" in c["architectural_decision"]


def test_serialized_certificate_matches_core_claims():
    assert DATA.exists()
    c = json.loads(DATA.read_text(encoding="utf-8"))
    assert c["architecture"]["fixed_interaction"] == "E_AR=(F_A^dagger tensor F_R) CZ_AR"
    assert c["universal_gate_compiler"]["universality_type"].startswith("approximate universal")
    assert c["holonet_reinterpretation"]["boundary"].endswith("proved here.")
