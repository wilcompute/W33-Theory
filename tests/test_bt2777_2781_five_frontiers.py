import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "data" / name).read_text())


def test_m36_no_go():
    data = load("PART_BT2777_M36_4_2_STABILIZER_CENSUS_summary.json")
    assert data["search_space"]["branches"] == 21420
    assert data["status"] == "EXACT_CANONICAL_DECODER_NO_GO"
    assert data["decoder_gauge"]["arbitrary_logical_clifford_exhausted"] is False
    assert all(row["m36_closed_branches"] > 0 for row in data["rows"])
    assert all(
        row["certified_nonimproving_branches"] == row["m36_closed_branches"]
        for row in data["rows"]
    )


def test_sensor():
    data = load("PART_BT2778_METAPLECTIC_INTERFEROMETER_summary.json")
    assert (data["class_count"], data["theta_pair_count"]) == (34, 33)
    assert data["shots_per_quadrature_hoeffding"] == 29579


def test_structured_compiler():
    data = load("PART_BT2779_STRUCTURED_CX_COMPILER_summary.json")
    assert data["checks"] == {
        "all_pairs_present": True,
        "all_rewrites_verified": True,
        "group_elements": 51840,
    }
    assert data["factorization"]["cosets"] == 480
    assert data["memory_bits"]["compression_ratio"] > 40


def test_repeater():
    data = load("PART_BT2781_REPEATER_REMOTE_SUM_summary.json")
    assert data["isotropic_recurrence"]["fixed_points"] == [1 / 9, 1 / 3, 1.0]
    result = data["scenario_summary"]["1280"]["best_distillable_rate"]
    assert result["segments"] == 8 and result["distillable"]


def test_release():
    data = load("PART_BT2784_BT2788_FIVE_FRONTIERS_results.json")
    assert data["canonical_pass_range"] == "2784-2788"
    assert data["check_count"] == 20 and all(data["checks"].values())
