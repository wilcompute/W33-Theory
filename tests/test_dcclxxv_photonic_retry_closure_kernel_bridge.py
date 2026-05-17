from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxxv_photonic_retry_closure_kernel_bridge import (  # noqa: E402
    OUT_PATH,
    build_bridge,
    write_bridge,
)


def _weight(row: dict[str, object]) -> Fraction:
    cell = row["transfer_weight"]
    assert isinstance(cell, dict)
    return Fraction(int(cell["numerator"]), int(cell["denominator"]))


def test_summary_values() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["closure_depth_count"] == 6
    assert summary["fusion_denominator"] == 2
    assert summary["accepted_slots"] == 240
    assert summary["return_slots"] == 240
    assert summary["directed_attempt_slots"] == 480
    assert summary["klm_primitive_slots"] == 960
    assert summary["maximal_retry_denominator"] == 32
    assert summary["all_identities_hold"] is True


def test_retry_kernel_is_transfer_power_law() -> None:
    rows = build_bridge()["retry_kernel"]["depth_rows"]

    assert len(rows) == 6
    assert [_weight(row) for row in rows] == [
        Fraction(1, 1),
        Fraction(1, 2),
        Fraction(1, 4),
        Fraction(1, 8),
        Fraction(1, 16),
        Fraction(1, 32),
    ]


def test_photonic_ledger_and_qec_identity() -> None:
    payload = build_bridge()
    ledger = payload["photonic_ledger"]

    assert ledger["accepted_slots"] == 240
    assert ledger["return_slots"] == 240
    assert ledger["directed_attempt_slots"] == 480
    assert ledger["klm_primitive_slots"] == 960
    assert ledger["qec_identity"] == "39 + 120 + 81 = 240"


def test_all_identities_hold() -> None:
    payload = build_bridge()
    identities = payload["identities"]

    assert identities["fusion_denominator_matches_transfer_weight"] is True
    assert identities["closure_depth_count_matches_success_slots"] is True
    assert identities["closure_depth_count_matches_return_slots"] is True
    assert identities["directed_attempt_slots_are_vertex_lift_of_retry_alphabet"] is True
    assert identities["maximal_retry_tail_is_one_over_32"] is True
    assert identities["qec_absorption_preserves_h1"] is True
    assert all(identities.values())


def test_theorem_boundary_and_public_index_exposure() -> None:
    payload = build_bridge()
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "Photonic Retry Closure-Kernel" in payload["theorem"]
    assert "does not prove a physical fusion threshold" in payload["honesty_boundary"]
    assert "Photonic Retry Closure-Kernel" in index
    assert "<code>2<sup>-d</sup></code>" in index
    assert "<code>480</code> directed retry attempts" in index


def test_write_and_reload() -> None:
    out = write_bridge()
    assert out == OUT_PATH

    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert data["summary"]["maximal_retry_denominator"] == 32
