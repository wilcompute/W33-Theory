from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccviii_holonomy_selector_quadratic_invariant_bridge import build_bridge


def test_dccviii_summary_matches_quadratic_invariants() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["selector_value_count"] == 2
    assert summary["invariant_norm_squared"] == 13122
    assert summary["invariant_signed_product"] == -6561
    assert summary["orientation_magnitude"] == 162


def test_dccviii_flip_preserves_invariants_and_reverses_orientation() -> None:
    payload = build_bridge()
    checks = payload["flip_checks"]

    for value in ["1", "2"]:
        assert checks[value]["norm_preserved"] is True
        assert checks[value]["signed_product_preserved"] is True
        assert checks[value]["orientation_negated"] is True


def test_dccviii_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())