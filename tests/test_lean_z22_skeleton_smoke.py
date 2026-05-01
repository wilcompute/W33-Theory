from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LEAN_FILE = ROOT / "proofs" / "lean" / "z22_exclusion.lean"


def _lean_text() -> str:
    if not LEAN_FILE.exists():
        pytest.skip(f"Missing Lean z22 proof fixture: {LEAN_FILE}")
    return LEAN_FILE.read_text(encoding="utf-8")


def test_lean_z22_file_ascii_clean() -> None:
    text = _lean_text()
    assert all(ord(ch) < 128 for ch in text)
    assert "\u00c3\u00a2" not in text
    assert "\u00c3\u201a" not in text


def test_lean_z22_contains_key_lemmas() -> None:
    text = _lean_text()
    assert "theorem zMap_table" in text
    assert "theorem zMap_one" in text
    assert "theorem zMap_fixed_iff" in text
    assert "theorem zMap_fixed_point_unique" in text
    assert "theorem zMap_involution" in text
    assert "theorem z22_contradiction_via_zMap" in text
    assert "theorem z22_contradiction_of_fixed_point" in text
    assert "theorem z22_contradiction_of_fixed_point_via_zMap" in text
    assert "theorem z22_no_fixed_point_stabilizer" in text
    assert "theorem z22_no_fixed_point_stabilizer_via_zMap" in text
    # Candidate-based results
    assert (
        "theorem z22_no_fixed_point_stabilizer_for_candidate_line_through_origin"
        in text
    )
    assert "theorem candidate_preserves_line_through_origin" in text
    assert "theorem z22_no_fixed_point_for_any_candidate" in text
