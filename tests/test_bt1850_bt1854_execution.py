import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1850_local_a2_weyl_glue_refinement_audit as bt1850  # noqa: E402
import bt1851_holonet_machine_selector_merge_patch as bt1851  # noqa: E402
import bt1852_compressed_shot_artifact_manifest as bt1852  # noqa: E402
import bt1853_runtime_selector_api as bt1853  # noqa: E402
import bt1854_quotient_status_dashboard as bt1854  # noqa: E402


def test_bt1850_local_boundary():
    summary = bt1850.theorem_summary()
    assert summary["bt943_local_result"]["four_plane_local_order"] == 1296
    assert summary["checks"]["local_glue_refinement_not_overclaimed"]


def test_bt1851_patch_checks():
    summary = bt1851.theorem_summary(apply=False)
    assert summary["checks"]["insert_has_canonical_selector"]
    assert summary["checks"]["local_A2_boundary_present"]


def test_bt1852_manifest_counts():
    summary = bt1852.theorem_summary()
    assert summary["compressed_bundles"] == 360
    assert summary["nominal_shots_preserved"] == 144000


def test_bt1853_api_pairs():
    assert bt1853.selector_pair_for_striation(0) == (3, 68)
    assert bt1853.selector_pair_for_striation(3) == (90, 144)
    summary = bt1853.theorem_summary()
    assert summary["metric_winner"] == 2


def test_bt1854_dashboard_open_stage():
    summary = bt1854.theorem_summary()
    assert summary["remaining_open_stage"] == "local_A2_Weyl_glue_refinement"
    assert summary["open_stage_count"] == 1
