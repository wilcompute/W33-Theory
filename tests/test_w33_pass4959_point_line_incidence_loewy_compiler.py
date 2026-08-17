"""Native-GAP regression for the Pass-4959 incidence Loewy compiler."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass4949_w33_levi_middle19_intertwiner.g"
FROZEN_4949 = ROOT / "data" / "PART_W33_PASS4949_W33_Q43_LEVI_MIDDLE_MODULES.json"
FROZEN_4959 = (
    ROOT / "data" / "PART_W33_PASS4959_POINT_LINE_INCIDENCE_LOEWY_COMPILER.json"
)
PASS_4949 = "Pass 4949 W33/Q43/Levi middle modules: 46/46 checks; status=PASS"
PASS_4959 = "Pass 4959 point-line incidence Loewy compiler: 9/9 checks; status=PASS"


def _assert_4959(payload: dict[str, object]) -> None:
    assert payload["schema"] == "w33.pass4959.point_line_incidence_loewy_compiler.v1"
    assert payload["status"] == "PASS"
    assert payload["incidence_factorization"] == {
        "rank_full": 25,
        "rank_augmentation": 24,
        "point_identity": "II^T=A_W+I",
        "line_identity": "I^TI=A_Q+I",
    }
    graded = payload["associated_graded_compiler"]
    assert "rank 14; kernel W5" in graded["point_to_line"]
    assert "rank 10; kernel the invariant 1-space" in graded["line_to_point"]
    assert "zero in both directions" in graded["homology_action"]

    bridge = payload["levi_bridge"]
    assert bridge["line_bottom14_to_Levi14_Hom_PSp_dimension"] == 1
    assert bridge["line_bottom14_to_Levi14_Hom_PGSp_dimension"] == 1
    assert bridge["intertwiner_rank"] == 14
    assert bridge["outer_sign_twisted_Hom_dimension"] == 0
    assert "point-line incidence" in bridge["factorization"]

    assert len(payload["checks"]) == 9
    assert set(payload["checks"].values()) == {True}
    assert "does not split LeviM19" in payload["boundary"]


def test_shared_gap_owner_rebuilds_both_frozen_certificates(tmp_path: Path) -> None:
    gap = shutil.which("gap")
    assert gap is not None, "native GAP is required for Pass 4959"

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
    lines = completed.stdout.splitlines()
    assert PASS_4949 in lines
    assert PASS_4959 in lines
    assert "Syntax warning" not in completed.stdout

    rebuilt_4949 = tmp_path / "data" / FROZEN_4949.name
    rebuilt_4959 = tmp_path / "data" / FROZEN_4959.name
    assert rebuilt_4949.read_bytes() == FROZEN_4949.read_bytes()
    assert rebuilt_4959.read_bytes() == FROZEN_4959.read_bytes()
    _assert_4959(json.loads(rebuilt_4959.read_bytes()))
