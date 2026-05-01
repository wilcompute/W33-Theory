from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "lean4.yml"


def test_lean_workflow_has_path_filters() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in text
    if "paths:" in text:
        assert '- "proofs/lean/**"' in text
        assert '- ".github/workflows/lean4.yml"' in text


def test_lean_workflow_has_cache_and_mathlib_cache_get() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "actions/cache@v4" in text
    assert "lake exe cache get" in text
    assert "concurrency:" in text


def test_lean_workflow_has_source_sanity_and_direct_typecheck() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Sanity-check z22 Lean source" in text
    assert "theorem zMap_fixed_point_unique" in text
    assert "theorem zMap_involution" in text
    assert "theorem z22_contradiction_via_zMap" in text
    assert "theorem z22_contradiction_of_fixed_point_via_zMap" in text
    assert "theorem z22_no_fixed_point_stabilizer_via_zMap" in text
    assert "lake env lean z22_exclusion.lean" in text
