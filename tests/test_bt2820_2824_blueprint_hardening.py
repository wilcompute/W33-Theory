from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "bt2820_2824_blueprint_hardening.py"
SPEC = importlib.util.spec_from_file_location("bt2820", MODULE_PATH)
assert SPEC and SPEC.loader
BT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BT)


def test_support_partition_profile() -> None:
    result = BT.compute_support_boundary()
    assert result["state_count"] == 81
    assert result["initial_support_classes"] == 16
    assert result["deterministic_refinement_class_counts"] == [16, 40, 78, 81]
    assert result["refinement_histograms"][-1] == {"1": 81}


def test_support_is_not_an_execution_congruence() -> None:
    witness = BT.compute_support_boundary()["non_lumpability_witness"]
    assert witness["support_mask"] == "0100"
    assert witness["states"] == [[0, 1, 0, 0], [0, 2, 0, 0]]
    assert witness["next_support_masks"] == ["0100", "0000"]


def gain(p: Fraction) -> Fraction:
    return p * (p - 1) * (3 * p - 2) / (4 * (p * p - 2 * p + 2))


def test_m36_gain_interval_and_boundary() -> None:
    assert gain(Fraction(1, 3)) > 0
    assert gain(Fraction(1, 2)) > 0
    assert gain(Fraction(2, 3)) == 0
    assert gain(Fraction(3, 4)) < 0


def test_selected_micro_isa_is_four_operations() -> None:
    operations = (BT.F_P, BT.CX_PF, BT.CX_FP, BT.z_p)
    assert len(operations) == 4


def test_frozen_sources_exist() -> None:
    assert (ROOT / "data" / "PART_BT2803_BT2807_FIVE_DEEP_FRONTIERS_results.json").exists()
    assert (ROOT / "data" / "PART_BT2808_PG32_TETRAHEDRAL_SUPPORT_LIFT_results.json").exists()
    assert (ROOT / "rtl" / "w33_pass2773_spread_mixer36_synth.sv").exists()
    assert not (ROOT / "rtl" / "w33_spread_mixer36.sv").exists()
