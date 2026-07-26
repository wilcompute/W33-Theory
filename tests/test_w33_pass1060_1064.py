"""Regression suite for Passes 1060--1064."""
from __future__ import annotations
import importlib
from pathlib import Path
import pytest

MODULES = [
    ("w33_pass1060_minimal_signed_cover", 7),
    ("w33_pass1061_springer_embedding_decision", 9),
    ("w33_pass1062_inner48_540_geometry", 8),
    ("w33_pass1064_dual_falsifier_preregistration", 13),
]

@pytest.mark.parametrize(("module_name", "expected_checks"), MODULES)
def test_pass(module_name: str, expected_checks: int) -> None:
    module = importlib.import_module(module_name)
    result = module.main()
    assert result["status"] == "PASS"
    assert result["check_count"] == expected_checks
    assert all(result["checks"].values())

def test_total_python_check_count() -> None:
    assert sum(count for _, count in MODULES) == 37

def test_formal_sources_are_wired() -> None:
    root = Path(__file__).resolve().parents[1]
    theorem = root / "formal" / "W33" / "Pass1063SignedLiftObstruction.lean"
    umbrella = root / "formal" / "W33.lean"
    assert theorem.exists()
    assert "import W33.Pass1063SignedLiftObstruction" in umbrella.read_text(encoding="utf-8")
