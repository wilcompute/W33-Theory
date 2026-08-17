"""Focused native-GAP regression for the Pass-4950 quarantine."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass4950_false_srg33_w33_quarantine.g"
FROZEN = ROOT / "data" / "PART_W33_PASS4950_FALSE_SRG33_QUARANTINE.json"
PASS_LINE = "Pass 4950 false SRG33 quarantine: 19/19 checks; status=PASS"


def _assert_exact_payload(payload: dict[str, object]) -> None:
    assert payload["schema"] == "w33.pass4950.false_srg33_quarantine.v1"
    assert payload["status"] == "PASS"
    assert payload["canonical_W33"] == {
        "object": "point-collinearity graph of W(3,3)",
        "parameters": [40, 12, 2, 4],
        "projective_action_order": 25920,
        "full_action_order": 51840,
    }
    contradictions = payload["fatal_contradictions"]
    assert set(contradictions) == {
        "SRG_feasibility",
        "spectrum",
        "group_action",
        "subgroup",
        "unitary_bridge",
    }
    assert "48" in contradictions["SRG_feasibility"]
    assert "40" in contradictions["SRG_feasibility"]
    assert "[1,32]" in contradictions["group_action"]
    checks = payload["checks"]
    assert len(checks) == 19
    assert set(checks.values()) == {True}
    assert "does not exist" in contradictions["SRG_feasibility"]
    assert "does not classify all strongly regular graphs" in payload["boundary"]


def test_native_gap_rebuild_matches_frozen_certificate(tmp_path: Path) -> None:
    gap = shutil.which("gap")
    assert gap is not None, "native GAP is required for Pass 4950"

    completed = subprocess.run(
        [gap, "-q", str(SOURCE)],
        cwd=tmp_path,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    assert completed.returncode == 0, completed.stdout[-6000:]
    assert PASS_LINE in completed.stdout.splitlines(), completed.stdout[-6000:]
    assert "Syntax warning" not in completed.stdout

    rebuilt = tmp_path / "data" / FROZEN.name
    rebuilt_bytes = rebuilt.read_bytes()
    assert rebuilt_bytes == FROZEN.read_bytes()
    _assert_exact_payload(json.loads(rebuilt_bytes))
