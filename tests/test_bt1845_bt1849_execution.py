import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1845_tetracode_stabilizer_action_audit as bt1845  # noqa: E402
import bt1846_winner2_canonical_basis_export as bt1846  # noqa: E402
import bt1847_shot_protocol_compression as bt1847  # noqa: E402
import bt1848_e8_labelled_trace_runner as bt1848  # noqa: E402


def test_bt1845_s4_rigidity():
    summary = bt1845.theorem_summary()
    assert summary["orbit_size"] == 24
    assert summary["stabilizer_size"] == 1
    assert summary["orbit_intersection_with_support60_minimizers_count"] == 1


def test_bt1846_canonical_basis():
    summary = bt1846.theorem_summary()
    assert summary["canonical_selector_pairs"] == [[3, 68], [4, 42], [38, 65], [90, 144]]
    assert summary["checks"]["s4_rigidity_recorded"]


def test_bt1847_compression():
    summary = bt1847.theorem_summary()
    assert summary["compressed_bundles"] == 360
    assert summary["compression_factor"] == 4
    assert summary["total_nominal_shots_preserved"] == 144000


def test_bt1848_trace_runner_schema():
    summary = bt1848.theorem_summary()
    assert summary["uploaded_trace_rows"] == 1023
    assert summary["e8_label"].startswith("canonical BT1846")
    assert "compiled_phase" in summary["row_fields"]
