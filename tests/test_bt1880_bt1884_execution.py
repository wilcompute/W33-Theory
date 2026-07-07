import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1880_bt982_to_bt1875_mapper as bt1880  # noqa: E402
import bt1881_chain_boundary_compatibility_tester as bt1881  # noqa: E402
import bt1882_central_inversion_vector_action as bt1882  # noqa: E402
import bt1874_final_selector_quotient_certificate as bt1874  # noqa: E402
import bt1884_paper_patch_apply_check_bundle as bt1884  # noqa: E402


def test_bt1880_mapper_contract():
    summary = bt1880.theorem_summary()
    assert summary["row_count"] == 8
    assert summary["checks"]["bt982_columns_cover_basis_once_per_phase_pair"]


def test_bt1881_boundary_pending():
    summary = bt1881.theorem_summary()
    assert summary["checks"]["all_integral_vector_shapes_ok"]
    assert summary["checks"]["boundary_not_falsely_passed"]


def test_bt1882_vector_action_gram():
    summary = bt1882.theorem_summary()
    assert summary["checks"]["all_slot_gram_contributions_preserved"]
    assert summary["checks"]["chain_boundary_still_not_claimed"]


def test_bt1883_certificate_upgrade():
    summary = bt1874.theorem_summary()
    assert summary["checks"]["BT982_basis_exists_recorded"]
    assert summary["checks"]["open_stage_is_Z40_chain_boundary"]


def test_bt1884_command_bundle():
    summary = bt1884.theorem_summary()
    assert summary["checks"]["apply_command_recorded"]
    assert summary["checks"]["pdf_build_not_claimed"]
