from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxi_holonomy_weld_associator_support_bridge import build_bridge


def test_dccxi_summary_matches_support_closure() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["weld_projector_rank"] == 1
    assert summary["seam_projector_rank"] == 1
    assert summary["covariance_trace"] == 13122
    assert summary["associator_rank"] == 2
    assert summary["scaled_support_abs_entry"] == 6561


def test_dccxi_scaled_support_kernel_is_exact_off_diagonal_packet_pair() -> None:
    payload = build_bridge()
    support = payload["weld_associator"]["scaled_support_kernel"]

    assert support == [[6561, 0], [0, -6561]]


def test_dccxi_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
