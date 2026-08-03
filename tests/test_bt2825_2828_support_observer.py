from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "bt2825_2827_support_observer.py"
SPEC = importlib.util.spec_from_file_location("bt2825", MODULE_PATH)
assert SPEC and SPEC.loader
BT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BT)


def test_adaptive_observer_profile() -> None:
    result = BT.adaptive_observer()
    assert result["class_counts"] == [16, 40, 78, 81]
    assert result["unresolved_pair_counts"] == [272, 53, 3, 0]
    assert result["newly_resolved_pair_counts"] == [2968, 219, 50, 3]
    assert result["adaptive_observability_index"] == 3


def test_fixed_open_loop_observer() -> None:
    result = BT.all_open_loop_words()
    assert result["best_distinct_trajectories_by_word_length"] == [25, 40, 45, 68, 77, 81]
    assert result["fixed_word_observability_index"] == 6
    assert result["injective_length6_word_count"] == 8
    assert result["canonical_word"] == [
        "CX_p->f",
        "F_p",
        "Z_p",
        "F_p",
        "Z_p",
        "CX_p->f",
    ]


def test_minimal_telemetry_taps() -> None:
    word = (1, 0, 3, 0, 3, 1)
    result = BT.minimal_taps(word)
    assert result["minimal_tap_count"] == 8
    assert result["seven_tap_selector_count"] == 0
    assert result["minimal_eight_tap_selector_count"] == 48
    assert result["canonical_selector_columns"] == [0, 1, 2, 5, 13, 21, 25, 26]
    assert result["mandatory_columns"] == [1, 2, 21, 25, 26]
    assert result["z_f_taps_required"] is False
    assert len(result["lookup_table"]) == 81


def test_rtl_sequence_and_tap_contract() -> None:
    rtl = (ROOT / "rtl" / "w33_pass2828_support_observer.sv").read_text(encoding="utf-8")
    assert "3'd0: op_o = OP_CX_PF" in rtl
    assert "3'd1: op_o = OP_FP" in rtl
    assert "3'd2: op_o = OP_ZP" in rtl
    assert "3'd3: op_o = OP_FP" in rtl
    assert "3'd4: op_o = OP_ZP" in rtl
    assert "3'd5: op_o = OP_CX_PF" in rtl
    for bit in range(8):
        assert f"code_q[{bit}]" in rtl
    assert "support_i[0]" not in "\n".join(
        line for line in rtl.splitlines() if "code_q[" in line and "<=" in line
    )
