from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxxvi_closure_action_weight_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["causal_class_count"] == 6
    assert s["elementary_action"] == 1
    assert s["maximal_action"] == 5
    assert s["maximal_weight_numerator"] == 1
    assert s["maximal_weight_denominator"] == 32


def test_elementary_edges_and_maximal_path() -> None:
    payload = build_bridge()
    edges = payload["elementary_edges"]
    assert len(edges) == 5
    assert all(edge["action"] == 1 for edge in edges)
    maximal = payload["path_table"][0][5]
    assert maximal["action"] == 5
    assert maximal["weight"] == {"numerator": 1, "denominator": 32}


def test_composition_witnesses() -> None:
    payload = build_bridge()
    for item in payload["composition_witness"]:
        assert item["action_ik"] == item["action_ij_plus_jk"]
        assert item["ratio_ik"] == item["ratio_ij_times_jk"]


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
