import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1860_integral_a2_representative_lift as bt1860  # noqa: E402
import bt1861_sign_kernel_action_on_winner2 as bt1861  # noqa: E402
import bt1862_quotient_dashboard_refinement as bt1862  # noqa: E402
import bt1863_trace_runner_selector_api_overlay as bt1863  # noqa: E402


def test_bt1860_candidate_long_element():
    summary = bt1860.theorem_summary()
    assert summary["one_plane_candidate_long_element"] == [[-1, 0], [0, -1]]
    assert summary["checks"]["candidate_reduces_to_identity_mod2"]
    assert summary["checks"]["chain_complex_lift_not_overclaimed"]


def test_bt1861_support_mask_fixed():
    summary = bt1861.theorem_summary()
    assert summary["support_mask_result"] == "winner-2 selector support is fixed at H level"
    assert summary["checks"]["integral_phase_action_remains_open"]


def test_bt1862_refined_dashboard():
    summary = bt1862.theorem_summary()
    assert summary["remaining_open_stage"] == "integral_A2_representative_chain_lift"
    assert summary["checks"]["glue_stabilizer_closed"]
    assert summary["checks"]["S4_transport_closed"]


def test_bt1863_overlay_uses_api():
    summary = bt1863.theorem_summary()
    assert summary["metric_winner"] == 2
    assert summary["status_label"] == "transported_S4_closed_local_A2_open"
