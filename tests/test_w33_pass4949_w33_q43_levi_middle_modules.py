"""Focused native-GAP regression for the Pass-4949 carrier correction."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass4949_w33_levi_middle19_intertwiner.g"
FROZEN = (
    ROOT / "data" / "PART_W33_PASS4949_W33_Q43_LEVI_MIDDLE_MODULES.json"
)
PASS_LINE = "Pass 4949 W33/Q43/Levi middle modules: 46/46 checks; status=PASS"


def _assert_exact_payload(payload: dict[str, object]) -> None:
    assert payload["schema"] == "w33.pass4949.w33_q43_levi_middle_modules.v1"
    assert payload["status"] == "PASS"

    dual = payload["dual_40s"]
    assert dual["Steiner_fiber_quotient"] == "Q(4,3) line-intersection graph"
    assert dual["recovered_K4_pencils"] == "W(3,3) point-collinearity graph"
    assert dual["common_parameters"] == "SRG(40,12,2,4)"
    assert dual["F3_rank_A_plus_I"] == {"W33_points": 11, "Q43_lines": 15}

    filtrations = payload["modular_filtrations"]
    assert filtrations["W33_point_augmentation"] == {
        "layers": [10, 19, 10],
        "middle_submodule_lattice": [0, 5, 14, 19],
        "middle_structure": "5 direct-sum 14",
    }
    assert filtrations["Q43_line_augmentation"] == {
        "layers": [14, 11, 14],
        "middle_submodule_lattice": [0, 1, 10, 11],
    }
    assert payload["Levi_M19"]["submodule_lattice"] == [0, 14, 19]
    assert payload["Levi_M19"]["structure"] == "nonsplit extension 14 by 5"

    complex_data = payload["exact_complex"]
    assert "rank 14" in complex_data["PSp_forward"]
    assert "rank 5" in complex_data["PSp_reverse"]
    assert complex_data["compositions"] == (
        "both zero; images equal subsequent kernels"
    )
    assert "vanishes untwisted" in complex_data["PGSp_reverse"]

    checks = payload["checks"]
    assert len(checks) == 46
    assert set(checks.values()) == {True}
    assert "Parameter equality and order 51840 do not identify it with W33" in (
        payload["correction"]
    )
    assert "does not identify the two 19-spaces" in payload["boundary"]


def test_native_gap_rebuild_matches_frozen_certificate(tmp_path: Path) -> None:
    gap = shutil.which("gap")
    assert gap is not None, "native GAP is required for Pass 4949"

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

    rebuilt = (
        tmp_path / "data" / "PART_W33_PASS4949_W33_Q43_LEVI_MIDDLE_MODULES.json"
    )
    rebuilt_bytes = rebuilt.read_bytes()
    assert rebuilt_bytes == FROZEN.read_bytes()
    _assert_exact_payload(json.loads(rebuilt_bytes))
