"""Focused regression for the GAP-owned Pass 383 C6/S3 control boundary."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 383")
def test_pass383_classifies_the_two_typed_branch_phase_lifts() -> None:
    result = subprocess.run(
        [GAP, "-q", str(ROOT / "analysis" / "w33_pass383_branch_phase_control_group.g")],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert "Pass383 status=PASS" in result.stdout
    assert "states=96 direct=C6 mirror=S3" in result.stdout.replace("\n", "")

    certificate = json.loads(
        (ROOT / "data" / "w33_pass383_branch_phase_control_group.json").read_text(
            encoding="utf-8"
        )
    )
    assert certificate["status"] == "PASS"
    assert certificate["check_count"] == 13 == len(certificate["checks"])
    assert all(certificate["checks"].values())
    assert certificate["state_space"] == {
        "branch_labels": 2,
        "bound_rows": 16,
        "phase_trits": 3,
        "states": 96,
    }
    assert certificate["orientation_preserving_lift"] == {
        "branch_action": "(b,row,p)->(b+1,row,p)",
        "phase_action": "(b,row,p)->(b,row,p+1)",
        "group": "C6",
        "order": 6,
    }
    assert certificate["phase_reflecting_lift"] == {
        "branch_action": "(b,row,p)->(b+1,row,-p)",
        "relation": "m^-1 r m = r^-1",
        "group": "S3",
        "order": 6,
    }
    assert certificate["search_signature"] == "96/16xC6/C6-vs-S3-control-boundary"


def test_pass383_does_not_confuse_a_control_interface_with_a_spectral_coupling() -> None:
    synthesis = (ROOT / "PASS383_BRANCH_PHASE_CONTROL_GROUP.md").read_text(
        encoding="utf-8"
    )
    assert "not a basis-level coupling" in synthesis
    assert "C6" in synthesis and "S3" in synthesis
    index = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8")
    assert "| `96/16xC6/C6-vs-S3-control-boundary` |" in index
