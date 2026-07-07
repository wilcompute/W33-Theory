import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1818_compiled_packet_kernel_controller as bt1818  # noqa: E402
import bt1820_aperture_magic_estimator as bt1820  # noqa: E402
import bt1821_cache_locality_score as bt1821  # noqa: E402
import w33_packet_vm_kernel as kernel  # noqa: E402


def test_bt1823_kernel_uses_compiled_controller_class():
    assert hasattr(kernel, "CompiledInterruptController")
    assert issubclass(kernel.CompiledInterruptController, kernel.ic.InterruptController)


def test_bt1823_selector_balances_edge_rows():
    selector = bt1818.CompiledRelocationSelector()
    edge = sorted(selector.table)[0]
    phases = [selector.choose_phase(*edge) for _ in range(6)]
    assert phases[:3] == phases[3:]
    assert len(set(phases[:3])) == 3


def test_bt1825_aperture_estimator_constants():
    summary = bt1820.theorem_summary()
    assert summary["aperture_skeleton"]["total_apertures"] == 1440
    assert summary["shot_table"]["contextual_fraction_target"] == 0.1


def test_bt1821_locality_decision_still_edge():
    summary = bt1821.theorem_summary()
    assert summary["edge_move"]["locality_score"] > summary["nonedge_move"]["locality_score"]
    assert summary["edge_move"]["churn_points"] == summary["nonedge_move"]["churn_points"] == 9
