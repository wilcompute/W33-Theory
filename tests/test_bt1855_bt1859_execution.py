import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1855_code_glue_stabilizer_intersection as bt1855  # noqa: E402
import bt1856_transport_local_survivor_to_H as bt1856  # noqa: E402
import bt1857_selector_api_refactor_audit as bt1857  # noqa: E402
import bt1858_holonet_machine_patch_materialization_plan as bt1858  # noqa: E402
import bt1853_runtime_selector_api as selector_api  # noqa: E402


def test_bt1855_glue_stabilizer_order():
    summary = bt1855.theorem_summary()
    assert summary["signed_monomial_glue_stabilizer_order"] == 48
    assert summary["block_quotient_order"] == 24
    assert summary["sign_kernel_size"] == 2


def test_bt1856_transport_split():
    summary = bt1856.theorem_summary()
    assert summary["H_effective_transport"]["transported_order"] == 24
    assert summary["not_yet_transportable"]["part"] == "sign kernel / local A2 Weyl lift"


def test_bt1857_selector_api_refactor_audit():
    summary = bt1857.theorem_summary()
    assert summary["status_label"] == "transported_S4_closed_local_A2_open"
    assert summary["checks"]["canonical_basis_single_source"]


def test_bt1858_materialization_plan():
    summary = bt1858.theorem_summary()
    assert summary["canonical_selector"] == [[3, 68], [4, 42], [38, 65], [90, 144]]
    assert summary["required_checks"]["local_A2_boundary_present"]


def test_bt1853_selector_api_records_boundary():
    assert selector_api.selector_pair_for_striation(0) == (3, 68)
    assert selector_api.selector_pair_for_striation(3) == (90, 144)
    assert "local A2" in selector_api.BOUNDARY
