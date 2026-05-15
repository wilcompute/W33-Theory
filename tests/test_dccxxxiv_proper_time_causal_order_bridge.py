from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxxiv_proper_time_causal_order_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["spatial_symmetry_count"] == 48
    assert s["proper_time_level_count"] == 6
    assert s["initial_proper_time"] == 0
    assert s["final_proper_time"] == 5
    assert s["final_scale"] == 384


def test_causal_classes_and_differences() -> None:
    payload = build_bridge()
    classes = payload["causal_order"]["classes"]
    assert [c["proper_time"] for c in classes] == [0, 1, 2, 3, 4, 5]
    diffs = payload["causal_order"]["differences"]
    assert all(d["delta_tau"] == 1 for d in diffs)
    assert all(d["scale_ratio"] == 2 for d in diffs)


def test_spatial_symmetry_witness_preserves_tau() -> None:
    payload = build_bridge()
    witness = payload["spatial_symmetry"]["witness_samples"]
    tau = witness[0]["proper_time_history"]
    assert all(sample["proper_time_history"] == tau for sample in witness)


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
