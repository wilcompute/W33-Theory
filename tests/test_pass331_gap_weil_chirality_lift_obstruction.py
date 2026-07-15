"""Focused parser tests for the GAP-owned Pass 331 certificate."""

from __future__ import annotations

import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass331_weil_chirality_lift_obstruction.g"
CERTIFICATE = ROOT / "data" / "w33_pass331_weil_chirality_lift_obstruction.json"


@lru_cache(maxsize=1)
def _certificate() -> dict:
    """Run GAP once; Python only parses the GAP-produced certificate."""

    gap = shutil.which("gap")
    assert gap is not None, "GAP is required for the Pass 331 certificate"
    result = subprocess.run(
        [gap, "-q", str(SCRIPT)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    assert (
        "Pass 331 GAP Weil chirality lift obstruction: PASS (24/24 checks)"
        in result.stdout
    )
    return json.loads(CERTIFICATE.read_text(encoding="utf-8"))


def test_q3_central_weil_pair_and_outer_frobenius() -> None:
    cert = _certificate()
    central = cert["central_H8"]
    assert cert["status"] == "PASS"
    assert central["PSp_endomorphism_ring"] == "F4"
    assert central["PGSp_endomorphism_ring"] == "F2"
    assert central["endomorphism_unit_orders"] == [1, 3, 3]
    assert "mutually dual" in central["F4_structure"]
    assert central["transvection_values"] == "(-1 plus-or-minus 3*sqrt(-3))/2"
    assert central["outer_controller_action"] == (
        "omega maps to omega^2=omega+1 (F4 Frobenius)"
    )


def test_logical_h10_has_the_dual_number_obstruction() -> None:
    logical = _certificate()["logical_H10"]
    assert logical["PSp_image_order"] == 25_920
    assert logical["PGSp_image_order"] == 51_840
    assert logical["endomorphism_ranks"] == [0, 1, 10, 10]
    assert logical["unit_orders"] == [1, 2]
    assert "F2[epsilon]/(epsilon^2)" in logical["endomorphism_ring_inner"]
    assert logical["epsilon_geometry"] == (
        "image(epsilon)=unique 1-space socle; "
        "kernel(epsilon)=unique 9-space radical"
    )
    assert logical["F4_extension_verdict"].startswith("IMPOSSIBLE equivariantly")


def test_d5_branching_and_outer_halfspin_exchange() -> None:
    cert = _certificate()
    branching = cert["D5_Brauer_branching"]
    outer = cert["outer_D5"]
    assert branching["possible_fusions"] == [
        [1, 5, 5, 2, 3, 6, 9, 9],
        [1, 5, 5, 4, 3, 7, 10, 10],
    ]
    assert branching["selected_natural10"] == "2*1 + 4a + 4b"
    assert branching["each_halfspin16"] == "2*1 + 4a + 4b + 6"
    assert outer["group_order"] == 46_998_591_897_600
    assert outer["derived_O10_order"] == 23_499_295_948_800
    assert outer["restriction"] == (
        "irreducible 32 restricts to two nonisomorphic irreducible 16s"
    )
    assert len(cert["checks"]) == 24
    assert all(cert["checks"].values())
