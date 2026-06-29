"""Pass 50: the machine audits itself.

The master audit re-derives the headline constant of every architectural layer from q = 3 in one
pass/fail ledger. These tests pin that the audit runs, covers every layer, and passes in full -- so CI
fails the moment any layer's recomputed constant drifts from the geometry.
"""

import os
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"
    ),
)

import w33_master_audit as audit  # noqa: E402


def test_audit_all_pass():
    checks, all_ok = audit.run_audit()
    failed = [name for name, ok in checks if not ok]
    assert all_ok, f"audit failures: {failed}"


def test_audit_covers_every_layer():
    checks, _ = audit.run_audit()
    names = " ".join(n for n, _ in checks)
    for layer in (
        "network",
        "processor",
        "contextuality",
        "magic",
        "fault-tol",
        "I/O",
        "minimal",
        "energy",
    ):
        assert layer in names, f"layer {layer!r} missing from audit ledger"


def test_audit_has_sixteen_checks():
    checks, _ = audit.run_audit()
    assert len(checks) == 16, f"expected 16 layer checks, got {len(checks)}"
