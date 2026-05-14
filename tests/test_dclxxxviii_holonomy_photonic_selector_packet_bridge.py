from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxxviii_holonomy_photonic_selector_packet_bridge import build_bridge


def test_dclxxxviii_summary_matches_common_packet_factorization() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["photonic_mode_count"] == 10
    assert summary["helicity_count"] == 2
    assert summary["deterministic_frame_size"] == 81
    assert summary["local_selector_order"] == 6
    assert summary["local_bulk_size"] == 27
    assert summary["common_packet_size"] == 162
    assert summary["global_selector_carrier"] == 1620


def test_dclxxxviii_common_packet_has_two_exact_readings() -> None:
    payload = build_bridge()
    factorizations = payload["factorizations"]

    assert factorizations["common_packet"]["selector_side"] == [6, 27]
    assert factorizations["common_packet"]["photonic_side"] == [2, 81]
    assert factorizations["common_packet"]["value"] == 162


def test_dclxxxviii_global_selector_carrier_has_both_mode_factorizations() -> None:
    payload = build_bridge()
    global_factorization = payload["factorizations"]["global_selector_carrier"]

    assert global_factorization["mode_packet_factorization"] == [10, 162]
    assert global_factorization["full_selector_factorization"] == [10, 6, 27]
    assert global_factorization["full_photonic_factorization"] == [10, 2, 81]
    assert global_factorization["value"] == 1620


def test_dclxxxviii_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())