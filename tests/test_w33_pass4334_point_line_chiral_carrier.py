"""Focused native-GAP regression for the Pass-4334 carrier split."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass4334_point_line_chiral_carrier.g"
FROZEN = ROOT / "data" / "PART_W33_PASS4334_POINT_LINE_CHIRAL_CARRIER.json"
PASS_LINE = "Pass 4334 point/line chiral carrier: 17/17 checks; status=PASS"

EXPECTED_CHECKS = {
    "carrier_sum_quadratic",
    "chambers_160",
    "chiral_image_contains_both_carriers",
    "chiral_image_is_point_line_direct_sum",
    "cross_maps_full_rank_24",
    "isoclinic_line_law",
    "isoclinic_point_law",
    "lifted_line_carrier_rank_24",
    "lifted_point_carrier_rank_24",
    "line_eigenprojector_rank_24",
    "lines_40",
    "panel_fixed_carriers",
    "point_eigenprojector_rank_24",
    "point_line_intersection_zero",
    "point_line_sum_rank_48",
    "points_40",
    "rational_span_projector_exact",
}


def _assert_exact_payload(payload: dict[str, object]) -> None:
    assert payload["schema"] == "w33.pass4334.point_line_chiral_carrier.v1"
    assert payload["status"] == "PASS"
    assert payload["objects"] == {
        "points": 40,
        "lines": 40,
        "chambers": 160,
        "point_carrier_rank": 24,
        "line_carrier_rank": 24,
        "chiral_rank": 48,
    }
    assert payload["object_level_split"] == {
        "identity": "im(Pi_48)=im(Q_p) direct_sum im(Q_l)",
        "dimensions": "48=24+24",
        "point_line_intersection_dimension": 0,
        "panel_actions": "P Q_p=3Q_p and L Q_l=3Q_l",
    }
    assert payload["uniform_isoclinicity"] == {
        "laws": "Q_p Q_l Q_p=(3/8)Q_p, Q_l Q_p Q_l=(3/8)Q_l",
        "squared_cosine": "3/8",
        "cosine": "sqrt(6)/4",
        "multiplicity": 24,
    }
    assert payload["rational_span_projector"] == {
        "Q": "Q_p+Q_l",
        "quadratic": "Q^2-2Q+(5/8)Pi_48=0",
        "formula": "Pi_48=(8/5)(2Q-Q^2)=-Omega^2/60",
    }
    assert "nonorthogonal but have zero intersection" in payload["boundary"]
    assert payload["checks"] == {name: True for name in EXPECTED_CHECKS}


def test_native_gap_rebuild_matches_frozen_certificate(tmp_path: Path) -> None:
    gap = shutil.which("gap")
    assert gap is not None, "native GAP is required for Pass 4334"

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

    rebuilt = tmp_path / "data" / "PART_W33_PASS4334_POINT_LINE_CHIRAL_CARRIER.json"
    rebuilt_bytes = rebuilt.read_bytes()
    assert rebuilt_bytes == FROZEN.read_bytes()
    _assert_exact_payload(json.loads(rebuilt_bytes))
