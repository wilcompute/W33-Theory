import pytest
from exploration.PART_CCLXII_BOSON_SAMPLING_BRIDGE import (
    checks,
    permanent_order_estimate,
    is_ramanujan,
    trace_a2,
    link_components,
    spectral_gap,
)

class TestCCLXIIBosonSampling:
    def test_all_checks_pass(self):
        failed = [name for name, ok in checks if not ok]
        assert failed == [], f"Failed checks: {failed}"

    def test_permanent_estimation(self):
        """k-regular graph has |E| = k*V/2 = 12*40/2 = 240 edges"""
        assert permanent_order_estimate > 0

    def test_ramanujan_property(self):
        """W(3,3) is Ramanujan: spectral gap ≥ 2√(k-1)"""
        assert is_ramanujan == True

    def test_eigenvalue_trace(self):
        """Trace of A² = 2|E| = 2*240"""
        assert trace_a2 == 480

    def test_knot_invariant(self):
        """Number of link components equals Q = 3"""
        assert link_components == 3

    def test_spectral_gap_bounds(self):
        """LAP_MID = 10 gives spectral gap satisfying Ramanujan bound"""
        assert spectral_gap == 10
