"""Regression tests for the GAP-owned Pass 541 all-m theorem."""

from __future__ import annotations

import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass541_q3_all_m_recurrence.g"
CERTIFICATE = ROOT / "data" / "w33_pass541_q3_all_m_recurrence.json"
GAP = shutil.which("gap")
pytestmark = pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 541")


@lru_cache(maxsize=1)
def _certificate() -> dict:
    """Run GAP once; Python checks only the emitted exact certificate."""

    assert GAP is not None
    before = CERTIFICATE.read_bytes()
    result = subprocess.run(
        [GAP, "-q", str(SCRIPT)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
    )
    assert "Pass 541: PASS (28/28)" in result.stdout
    assert CERTIFICATE.read_bytes() == before
    return json.loads(CERTIFICATE.read_text(encoding="utf-8"))


def test_exact_recurrence_certificates_cover_every_parity_class() -> None:
    cert = _certificate()
    assert cert["status"] == "PASS"
    assert cert["normalized_characteristic_parameters"] == [
        [0, 0],
        [1, 0],
        [2, 0],
        [3, 0],
        [3, 1],
        [4, 3],
    ]
    assert cert["section_multiplicities"] == [1, 8, 24, 8, 24, 16]
    assert cert["even_certificate"]["attainer"] == [1, 0]
    odd = cert["odd_certificate"]
    assert odd["A"]["mod9_word"] == [3, 0, 6]
    assert odd["A"]["attains_m_mod6"] == [3, 5]
    assert odd["B"]["mod9_tail_word"] == [8, 0, 5, 6, 2, 3]
    assert odd["B"]["attains_m_mod6"] == [1]
    assert odd["B"]["first_attainment"] == 7
    assert odd["coverage"]["odd_residue_classes_mod6"] == [1, 3, 5]


def test_finite_control_matches_closed_formula_without_owning_the_proof() -> None:
    cert = _certificate()
    control = cert["finite_control"]
    assert control["range"] == [2, 60]
    assert control["minimum_values"] == [2 * (m + (m % 2)) for m in range(2, 61)]
    assert "infinite in m" in cert["scope"]
    assert "specific to the six realized q=3" in cert["scope"]


def test_every_gap_check_passes() -> None:
    cert = _certificate()
    checks = cert["checks"]
    assert len(checks) == 28
    assert all(checks.values())
    assert "every m" in cert["corollaries"]["profile_completeness"]
    assert "exactly when" in cert["corollaries"]["factorial_agreement_locus"]
    assert "m=3^i+3^j" in cert["corollaries"]["factorial_agreement_locus"]
    assert checks["agreement_locus_has_explicit_ternary_classification"]
    assert checks["prime_power_branch_is_proper"]
