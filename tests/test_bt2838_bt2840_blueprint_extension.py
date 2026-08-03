from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
INTEGRATOR = ROOT / "tools" / "integrate_bt2838_bt2840_blueprint.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_integrator_is_idempotent_and_preserves_parallel_corrections():
    module = load_module(INTEGRATOR, "bt2840_integrator")
    text = (ROOT / "holonet_machine_blueprint.tex").read_text(encoding="utf-8")
    integrated = module.integrate(text)
    assert module.integrate(integrated) == integrated
    module.audit(integrated)
    assert integrated.count(module.INPUT) == 1
    assert "Clifford classes on the $36$ rays: $[4,8,12,12]$" in integrated
    assert "Minimal engine: $\\mathbf{43}$ LC, $\\mathbf{72.40}$" in integrated


def test_optimal_execution_codec_certificate():
    data = json.loads((ROOT / "data" / "PART_BT2838_OPTIMAL_EXECUTION_CODEC_results.json").read_text())
    assert data["status"] == "COMPLETE_EXACT"
    assert data["check_count"] == 7 and all(data["checks"].values())
    assert data["deterministic_refinement_counts"] == [16, 40, 78, 81]
    assert data["optimal_fixed_width_bits"] == 7
    assert data["transition_table_payload_bits"] == 2268


def test_repeated_branch_cost_certificate():
    data = json.loads((ROOT / "data" / "PART_BT2839_M36_REPEATED_BRANCH_COST_results.json").read_text())
    assert data["status"] == "EXACT_LOCAL_ASYMPTOTIC_AND_NUMERICAL_TRAJECTORIES"
    assert data["check_count"] == 6 and all(data["checks"].values())
    exponent = data["repeated_branch_overhead_exponent"]
    assert exponent["formula"] == "log(4)/log(3/2)"
    assert abs(exponent["value"] - 3.4190225827029095) < 1e-15
    assert "not an optimized protocol" in data["claim_boundary"]


def test_three_code_architecture_is_bound_to_parallel_observer_evidence():
    insert = (ROOT / "analysis" / "BT2838_BT2840_blueprint_extension_insert.tex").read_text()
    rom = (ROOT / "rtl" / "w33_pass2827_support_decoder_rom.sv").read_text()
    protected = json.loads((ROOT / "data" / "PART_BT2828_DOUBLE_WORD_DISTANCE4_summary.json").read_text())
    assert "Three codes have three different jobs" in insert
    assert rom.count("valid_o = 1'b1") == 81
    assert protected["ordered_pair_distance_profile"] == {"2": 40, "3": 16, "4": 8}
    assert protected["coding_consequence"] == {
        "trajectory_bits": 52,
        "minimum_distance": 4,
        "guaranteed_detection_bits": 3,
        "guaranteed_correction_bits": 1,
        "decoder": "nearest-neighbor over 81 exact codewords",
    }
    assert all(protected["checks"].values())


def test_four_class_magic_correction_is_not_regressed():
    magic = json.loads((ROOT / "data" / "PART_W33_PASS2797_2799_MAGIC_ORBITS_AND_MONOTONE.json").read_text())
    insert = (ROOT / "analysis" / "BT2838_BT2840_blueprint_extension_insert.tex").read_text()
    assert magic["pass_2797"]["class_sizes"] == [4, 8, 12, 12]
    assert "four representatives, not three" in insert
