import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1836_e8_selector_aperture_table as bt1836  # noqa: E402
import bt1837_tetracode_quotient_hunt as bt1837  # noqa: E402
import bt1838_compiled_log_annotator as bt1838  # noqa: E402


def test_bt1836_selector_table_constants():
    summary = bt1836.theorem_summary()
    assert summary["rows"] == 1440
    assert summary["metric_winner"] == 2
    assert set(summary["selector_pair_counts"].values()) == {360}


def test_bt1837_intrinsic_quotient_winner_singleton():
    summary = bt1837.theorem_summary()
    assert summary["metric_winner"] == 2
    assert summary["metric_winner_certificate_orbit"] == [2]
    assert summary["checks"]["bt930_matrix_required_to_finish"]


def test_bt1838_annotation_manifest_constants():
    summary = bt1838.theorem_summary()
    assert summary["uploaded_rows"] == 1023
    assert "compiled_phase" in summary["added_fields"]
    assert summary["required_checks"]["all_costs_are_three"]
