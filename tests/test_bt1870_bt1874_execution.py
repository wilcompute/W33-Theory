import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1870_physical_e8_representative_model as bt1870  # noqa: E402
import bt1871_central_inversion_phase_transport_test as bt1871  # noqa: E402
import bt1872_central_inversion_wording_audit as bt1872  # noqa: E402
import bt1873_holonet_machine_bt1869_merge_patch as bt1873  # noqa: E402
import bt1874_final_selector_quotient_certificate as bt1874  # noqa: E402


def test_bt1870_model_fields():
    summary = bt1870.theorem_summary()
    assert "integral_E8_vector_a" in summary["required_model_fields"]
    assert "chain_boundary_compatibility" in summary["required_model_fields"]
    assert summary["checks"]["does_not_claim_model_exists_yet"]


def test_bt1871_phase_transport_support_fixed():
    summary = bt1871.theorem_summary()
    assert summary["phase_images_on_H_support"]["0"] == summary["canonical_selector"]
    assert summary["phase_images_on_H_support"]["1"] == summary["canonical_selector"]


def test_bt1872_wording_audit():
    summary = bt1872.theorem_summary()
    assert "bt1860_integral_a2_representative_lift.py" in " ".join(summary["patched_files"])
    assert summary["checks"]["active_BT1864_insert_patched"]


def test_bt1873_merge_patch():
    summary = bt1873.theorem_summary(apply=False)
    assert summary["checks"]["insert_has_selector"]
    assert summary["checks"]["insert_has_central_inversion_wording"]


def test_bt1874_final_certificate():
    summary = bt1874.theorem_summary()
    assert summary["checks"]["exactly_one_open_stage"]
    assert summary["checks"]["support_shadow_closed"]
    assert summary["phase_bit"]["ambient_quotient"] == "O(A2)/W(A2)"
