import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1818_compiled_packet_kernel_controller as bt1818  # noqa: E402
import bt1819_packet_trace_replay_compiled_vs_seeded as bt1819  # noqa: E402
import bt1820_aperture_magic_estimator as bt1820  # noqa: E402
import bt1821_cache_locality_score as bt1821  # noqa: E402


def test_bt1818_compiled_selector_counts():
    summary = bt1818.theorem_summary()
    assert summary["directed_edges"] == 480
    assert summary["phase_rows_per_edge"] == 3
    assert summary["compiled_rows"] == 1440


def test_bt1819_replay_contract():
    summary = bt1819.theorem_summary()
    assert summary["semantic_contract"]["program_inputs"] == 1600
    assert summary["semantic_contract"]["expected_output_mismatches"] == 0
    assert summary["compiled_trace_prediction"]["directed_edges_with_phase_rows"] == 480


def test_bt1820_aperture_estimator():
    summary = bt1820.theorem_summary()
    assert summary["aperture_skeleton"]["total_apertures"] == 1440
    assert summary["shot_table"]["contextual_fraction_target"] == 0.1


def test_bt1821_locality_score():
    summary = bt1821.theorem_summary()
    assert summary["edge_move"]["churn_points"] == 9
    assert summary["nonedge_move"]["churn_points"] == 9
    assert summary["locality_gap_edge_minus_nonedge"] > 0
