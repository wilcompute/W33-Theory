import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1875_integral_e8_representative_template as bt1875  # noqa: E402
import bt1876_representative_existence_search as bt1876  # noqa: E402
import bt1877_regenerate_corrected_summaries_audit as bt1877  # noqa: E402
import bt1878_apply_bt1873_patch_plan as bt1878  # noqa: E402


def test_bt1875_template_rows():
    summary = bt1875.theorem_summary()
    assert summary["row_count"] == 8
    assert summary["checks"]["bt982_candidate_basis_linked"]


def test_bt1876_finds_bt982():
    summary = bt1876.theorem_summary()
    assert summary["primary_candidate"] == "analysis/bt982_explicit_integral_e8_basis.py"
    assert summary["checks"]["bt982_has_final_basis_contract"]


def test_bt1877_corrected_summaries():
    summary = bt1877.theorem_summary()
    assert summary["correction"] == "central inversion in O(A2), outside plain W(A2)"
    assert summary["checks"]["bt1860_summary_corrected"]


def test_bt1878_apply_plan():
    summary = bt1878.theorem_summary()
    assert summary["checks"]["apply_command_recorded"]
    assert summary["checks"]["static_tex_check_recorded"]
