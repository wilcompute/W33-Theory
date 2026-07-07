import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1840_bt930_matrix_recovery_audit as bt1840  # noqa: E402
import bt1841_generated_artifact_pack as bt1841  # noqa: E402
import bt1842_e8_labelled_compiled_trace_schema as bt1842  # noqa: E402
import bt1843_aperture_to_shot_protocol as bt1843  # noqa: E402


def test_bt1840_matrix_recovered_and_winner_two():
    summary = bt1840.theorem_summary()
    assert summary["matrix_status"] == "recovered and stored by BT956"
    assert summary["bt956_metric_result"]["metric_winner"] == 2
    assert summary["checks"]["full_group_quotient_not_overclaimed"]


def test_bt1841_pack_manifest_has_generators():
    summary = bt1841.theorem_summary()
    assert len(summary["generators"]) == 7
    assert len(summary["expected_artifacts"]) == 7


def test_bt1842_trace_schema_e8_labels():
    summary = bt1842.theorem_summary()
    assert summary["uploaded_rows"] == 1023
    assert summary["e8_metric_winner"] == 2
    assert "compiled_phase" in summary["compiled_fields"]
    assert "e8_selector_pair_a" in summary["e8_selector_fields"]


def test_bt1843_protocol_counts():
    summary = bt1843.theorem_summary()
    assert summary["rows"] == 1440
    assert summary["total_nominal_shots"] == 144000
    assert set(summary["detector_channel_counts"].values()) == {360}
