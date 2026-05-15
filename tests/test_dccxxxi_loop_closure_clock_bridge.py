from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxxi_loop_closure_clock_bridge import (
    build_bridge,
    closure_event_sequence,
    discrete_clock,
)


def test_event_sequence_binary() -> None:
    events = closure_event_sequence(7)
    assert len(events) == 7
    assert all(e in (0, 1) for e in events)


def test_discrete_clock_monotone() -> None:
    events = [1, 0, 1, 1, 0]
    tau = discrete_clock(events)
    assert tau == [1, 1, 2, 3, 3]
    assert all(tau[i] <= tau[i + 1] for i in range(len(tau) - 1))


def test_summary_and_identities() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["minimum_loop_vertices"] == 3
    assert s["closure_channel_dimension"] == 4
    assert s["quaternion_basis_dimension"] == 4
    assert s["clock_steps"] == 7
    assert s["final_clock_value"] == 5
    assert s["all_identities_hold"] is True


def test_bridge_claim_has_exact_and_conditional_layers() -> None:
    payload = build_bridge()
    claim = payload["bridge_claim"]
    assert "exact_layer" in claim
    assert "conditional_layer" in claim
    assert "requires" in claim["conditional_layer"] or "assumptions" in claim["conditional_layer"]
