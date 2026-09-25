import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10943_protected_metaplectic_five_front.py"
CERT = ROOT / "data/w33_pass10943_protected_metaplectic_five_front.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays():
    subprocess.run([sys.executable, str(PRODUCER)], cwd=ROOT, check=True,
                   capture_output=True, text=True, timeout=50)


def test_protected_pipeline_and_dark_pump():
    x = load()
    assert x["status"] == "PASS_PROTECTED_METAPLECTIC_VM_FIVE_FRONT_CLOSURE"
    f1 = x["front1_protected_Strange_distillation"]
    comp = f1["repository_composition_with_Pass10942"]
    assert abs(comp["end_to_end_error_improvement_threshold"] - 0.2715245018525886) < 1e-14
    assert comp["small_error"] == "q_R=(220/27)*delta^3+O(delta^4)"
    assert comp["sample_delta_0_1"][1]["converted_R_error"] < 1e-6
    assert comp["sample_delta_0_1"][0]["pure_limit_raw_Strange_per_injected_R"] == 1_824_768
    f2 = x["front2_dark_Strange_dissipative_preparation"]
    assert f2["unique_steady_state"] is True
    assert f2["spectral_gap"] == "gamma/2"
    assert f2["unit_gamma_liouvillian_spectrum"] == {"0": 1, "-1/2": 4, "-1": 4}


def test_golay_logical_abi():
    f3 = load()["front3_fault_tolerant_R_injection"]
    assert f3["code_parameters"] == "[[11,1,5]]_3"
    assert (f3["classical_C_size"], f3["classical_C_perp_size"]) == (243, 729)
    assert (f3["minimum_weight_C"], f3["minimum_weight_C_perp_minus_C"]) == (6, 5)
    assert f3["correctable_physical_qutrit_errors"] == 2
    assert f3["weight_at_most_2_pauli_error_count"] == 3609
    assert f3["logical_injection"]["expected_distilled_Strange_blocks"] == 96


def test_m36_transducer_and_temporal_control_dictionary():
    f4 = load()["front4_M36_to_qutrit_transducer"]
    assert f4["classification"] == {"R_magic": 27, "stabilizer": 9}
    assert f4["distinct_qutrit_outputs"] == {"R_magic": 18, "stabilizer": 9}
    assert f4["R_magic_families"] == [0, 1, 2]
    assert f4["stabilizer_family"] == 3
    assert f4["maximum_Clifford_correction_length"] == 4
    assert f4["output_coordinate_permutation_checks"] == 216
    control = f4["temporal_control_dictionary"]
    assert control["family_resource_split"] == {"R_magic": 3, "stabilizer": 1}
    assert len(control["rows"]) == 4
    assert all(len(row["Hesse_striation"]) == 3 for row in control["rows"])
    assert all(row["oriented_E8_parabolic_clock_choices"] == 6 for row in control["rows"])
    assert all(row["E8_parabolic_Lie_dimensions"] == [2, 27, 54, 82, 54, 27, 2]
               for row in control["rows"])
    assert all(row["positive_clock_bracket_growth"] == [54, 81, 83]
               for row in control["rows"])
    assert "not an intrinsic preferred null direction" in control["symmetry_firewall"]
    assert f4["selected_factory_cost"]["expected_M36_states_per_R_injection"] == 3


def test_instruction_economy_and_visible_surfaces():
    x = load()["front5_R_T_instruction_economy"]
    assert x["exact_expressivity"]["known_T_count"] == 39
    assert x["exact_expressivity"]["strict_inclusion"] == "Clifford+R is a strict exact subset of Clifford+T"
    assert x["symbolic_break_even"]["c_T_threshold"] == "32/13"
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(encoding="utf-8")
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    report = (ROOT / "analysis/PASS10943_RESERVATION.md").read_text(encoding="utf-8")
    assert tail.count("PASS10943_PROTECTED_METAPLECTIC_FIVE_FRONT_INSERT") == 1
    assert docs.count('id="pass10943-protected-metaplectic-five-front"') == 1
    for stale in ("No Distillation Factory", "Here that cost vanishes", "P=1</strong> on this substrate"):
        assert stale not in docs
    assert "27 rays -> qutrit R-magic Clifford orbit" in report
