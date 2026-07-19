from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(n: int) -> dict:
    suffix = {
        463: "q5_central_sheet_exchange",
        464: "chain_ring_cyclotomic_conductors",
        465: "formal_cover_l2_l4_audit",
        466: "smith_bockstein_ramification",
        467: "hardware_blind_runner",
    }[n]
    return json.loads((ROOT / "data" / f"w33_pass{n}_{suffix}.json").read_text(encoding="utf-8"))


def test_pass463_central_sheet_exchange() -> None:
    p = load(463)
    assert p["status"] == "PASS"
    assert p["central_character_classes"] == {
        "square": [1, 4], "nonsquare": [2, 3], "exchange_multiplier": 2
    }
    assert p["faithful_quintic_factors"]["A_assignment"] != p["faithful_quintic_factors"]["B_assignment"]
    assert "x**10 - 120*x**8" in p["faithful_quintic_factors"]["norm_to_Q"]


def test_pass464_chain_ring_conductors() -> None:
    p = load(464)
    assert p["status"] == "PASS"
    assert [x["characters"] for x in p["z9_witness"]["conductor_strata"]] == [6, 2]
    assert [x["alternating_radical_size"] for x in p["z9_witness"]["conductor_strata"]] == [1, 9]
    assert p["z9_witness"]["cyclotomic_local_orders"][-1]["local_ramification_index"] == 6
    assert p["z25_witness"]["cyclotomic_local_orders"][-1]["local_ramification_index"] == 20


def test_pass465_complete_q3_cover_law_source() -> None:
    p = load(465)
    assert p["status"] == "PASS"
    assert p["q3_objectwise_counts"]["distance_shells"] == [1, 8, 16, 2]
    assert p["q3_objectwise_counts"]["intersection_array"] == [[8, 6, 1], [1, 3, 8]]
    src = (ROOT / "formal" / "W33" / "Pass465CoverLawL2L4Q3.lean").read_text(encoding="utf-8")
    assert "theorem q3_cover_law_L1_L4" in src
    assert "theorem cover_shell_total" in src
    assert src.count("native_decide") == 4
    assert "sorry" not in src.lower()


def test_pass466_bockstein_staircase() -> None:
    p = load(466)
    assert p["status"] == "PASS"
    assert list(p["z9_tail_dimensions"].values()) == [629, 475, 313, 233, 223, 18, 18, 7, 0]
    assert p["z9_exact_exponent_counts"]["6"] == 0
    assert p["z9_exact_exponent_counts"]["7"] == 11
    assert p["z9_exact_exponent_counts"]["8"] == 7
    assert p["ramification_localization"]["ramification_index"] == 6


def test_pass467_software_closed_hardware_open() -> None:
    p = load(467)
    assert p["status"] == "PASS"
    assert p["software_gate"] == "CLOSED"
    assert p["hardware_gate"] == "OPEN_NO_MEASURED_INPUT"
    assert p["synthetic_schema_rehearsal"]["score"]["balanced_accuracy"] == [1, 1]
    assert p["runner_contract"]["prediction"].endswith("margin 1/100")
    assert (ROOT / "hardware" / "pass467" / "calibration_matrix_template.csv").exists()
    assert (ROOT / "hardware" / "pass467" / "sealed_observations_template.csv").exists()
