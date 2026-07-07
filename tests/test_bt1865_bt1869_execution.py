import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1865_integral_representative_equivalence_classes as bt1865  # noqa: E402
import bt1866_phase_action_invariant as bt1866  # noqa: E402
import bt1867_canonical_lift_criterion as bt1867  # noqa: E402
import bt1854_quotient_status_dashboard as bt1854  # noqa: E402


def test_bt1865_OA2_vs_WA2():
    summary = bt1865.theorem_summary()
    assert summary["O_A2_order"] == 12
    assert summary["W_A2_order"] == 6
    assert summary["checks"]["negative_identity_not_in_plain_Weyl_group"]


def test_bt1866_phase_coset_bit():
    assert bt1866.phase_coset_bit([[1, 0], [0, 1]]) == 0
    assert bt1866.phase_coset_bit([[-1, 0], [0, -1]]) == 1
    summary = bt1866.theorem_summary()
    assert summary["checks"]["support_mask_blind_to_both"]


def test_bt1867_lift_criterion():
    summary = bt1867.theorem_summary()
    assert summary["nontrivial_class_representative"] == [[-1, 0], [0, -1]]
    assert summary["checks"]["chain_complex_lift_still_requires_E8_representative_model"]


def test_bt1868_dashboard_replacement():
    summary = bt1854.theorem_summary()
    assert summary["remaining_open_stage"] == "integral_A2_representative_chain_lift"
    assert summary["checks"]["nine_stages_recorded"]
