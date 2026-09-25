import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10944_five_front_computational_closure.py"
CERT = ROOT / "data/w33_pass10944_five_front_computational_closure.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays():
    subprocess.run([sys.executable, str(PRODUCER)], cwd=ROOT, check=True,
                   capture_output=True, text=True, timeout=40)


def test_intertwiner_no_go_and_constructive_complement():
    x = load()["front1_54D_intertwiner"]
    obstruction = x["H27_multiplicity_obstruction"]
    assert obstruction["maximum_H27_equivariant_rank"] == 36
    assert obstruction["invertible_H27_intertwiner_exists"] is False
    complement = x["constructive_symmetry_changing_isomorphism"]
    assert complement["counts"] == {"P": 36, "Q": 18}
    assert complement["combined_with_S1_rank"] == 81
    assert len(complement["quotient_basis_from_P"]) == 36
    assert len(complement["quotient_basis_from_Q"]) == 18


def test_cubic_tick_compiles_universal_control_primitive():
    x = load()["front2_reversible_cubic_clock"]
    assert x["opcode"]["reversible"] is True
    assert x["opcode"]["supported_triads"] == 45
    assert x["opcode"]["local_truth_table_roundtrip_checks"] == 162
    assert x["phase_kickback"]["Clifford_hierarchy_level"] == 3
    table = x["controlled_X_compiler"]["truth_table"]
    assert len(table) == 9
    assert all(row["output"] == (row["target"] + (row["control"] == 0)) % 3
               for row in table)
    assert x["universality"]["status"].startswith("APPROXIMATELY_UNIVERSAL")


def test_selector_covariance_is_full_s4():
    x = load()["front3_AGL_selector_covariance"]
    action = x["action_on_four_null_directions"]
    assert x["group_order"] == 432
    assert action["image_order"] == 24
    assert action["kernel_order"] == 18
    assert action["transitive"] is True
    gauge = x["canonical_three_plus_one_gauge"]
    assert gauge["label_stabilizer_order"] == 6
    assert gauge["full_preimage_order"] == 108
    assert set(x["explicit_linear_relabelings_moving_calibration_family"]) == {"0", "1", "2", "3"}


def test_golay_transversal_core_fault_curve():
    x = load()["front4_Golay_circuit_fault_model"]
    assert x["circuit"]["active_location_count"] == 66
    audit = x["exhaustive_support_audit"]
    assert audit["fault_subsets_of_size_at_most_two"] == 2212
    assert audit["all_correctable_by_distance_five"] is True
    curve = x["independent_stochastic_fault_curve"]
    assert curve["leading_coefficient"] == 45760
    assert len(curve["samples"]) == 3


def test_physical_interface_and_visible_surfaces():
    x = load()["front5_physical_interface"]
    interface = x["four_to_three_mode_interface"]
    assert interface["family_dark_modes"] == {"0": 0, "1": 1, "2": 2, "3": 3}
    assert interface["all_M36_rays_checked"] == 36
    assert interface["fidelity_budget"]["target_conditional_fidelity"] == 0.99
    assert interface["separate_dark_port_budget"]["dark_port_extinction_dB_at_least"] == 30.0
    assert x["dark_Strange_reservoir"]["resulting_steady_state_trace_distance_bound"] == 0.01
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(encoding="utf-8")
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    assert tail.count("PASS10944_FIVE_FRONT_COMPUTATIONAL_CLOSURE_INSERT") == 1
    assert docs.count('id="pass10944-five-front-computational-closure"') == 1
