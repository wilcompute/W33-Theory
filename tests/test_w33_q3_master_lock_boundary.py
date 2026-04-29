from __future__ import annotations

from scripts.w33_q3_master_lock_boundary import (
    build_q3_full_physical_realization_boundary_record,
)


def test_q3_master_lock_boundary_record_is_lightweight_and_stable() -> None:
    record = build_q3_full_physical_realization_boundary_record()

    assert record["name"] == "q3_full_physical_realization_theorem"
    assert record["support_level"] == "boundary summary with promoted frontier response"
    assert "exact finite spine" in record["statement"]
    assert "not by a newly claimed exact phenomenology theorem" in record["statement"]
    assert record["evidence"]["frontier_boundary"].startswith("CKM/E6 promotion remains")
    assert record["evidence"]["tests_total"] == "27 + 12 + 11 = 50 tests across exact-spine records"