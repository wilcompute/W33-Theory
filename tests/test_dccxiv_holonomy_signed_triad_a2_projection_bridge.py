from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxiv_holonomy_signed_triad_a2_projection_bridge import build_bridge


def test_dccxiv_summary_matches_signed_triad_projection() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["primitive_axis_count"] == 3
    assert summary["signed_channel_count"] == 6
    assert summary["a2_root_count"] == 6
    assert summary["packet_per_signed_axis"] == 2187
    assert summary["local_valency_split"].startswith("12 = 6 signed Clifford channels")


def test_dccxiv_a2_projection_is_root_hexagon() -> None:
    payload = build_bridge()
    projection = payload["a2_projection"]

    roots = {tuple(v) for v in projection["projected_signed_roots"].values()}
    assert len(roots) == 6
    assert projection["positive_root_sum"] == [0, 0, 0]
    assert projection["root_dot_values"] == [-2, -1, 1, 2]


def test_dccxiv_qec_ouroboros_turn_alphabet_is_six_plus_six() -> None:
    payload = build_bridge()
    qec = payload["qec_ouroboros"]

    assert qec["w33_directed_edge_carrier"] == 480
    assert qec["local_valency"] == 12
    assert qec["local_split"] == [6, 6]
    assert "H1=81" in qec["interpretation"]


def test_dccxiv_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
