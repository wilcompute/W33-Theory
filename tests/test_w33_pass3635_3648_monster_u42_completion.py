from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass3635_3648_monster_u42_completion.py"
FROZEN = ROOT / "data" / "PART_3635_3648_MONSTER_U42_COMPLETION_results.json"
EXPECTED_SHA = "cf276859798326def36c2bdc0e9fb75dbdadbbc44d69ba61cae24b5c82f40271"


def test_exact_monster_u42_completion(tmp_path: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert f"PASS_3635_3648 {EXPECTED_SHA}" in completed.stdout
    generated = json.loads(
        (tmp_path / "data" / "PART_3635_3648_MONSTER_U42_COMPLETION_results.json").read_text()
    )
    frozen = json.loads(FROZEN.read_text())
    assert generated == frozen
    assert generated["semantic_sha256"] == EXPECTED_SHA
    assert generated["u42_carrier"]["group_order"] == 25920
    assert generated["a5_a6_s6_geometry"]["components"] == 36
    assert generated["local_matrix_algebra"]["combined_rank"] == 576
    assert generated["leech_glue"]["scalar_unimodular_overlattice"] == "IMPOSSIBLE"
    assert generated["graded_modular_completion"]["character_j_plus_24"][2] == 196884


def test_evidence_boundary_is_fail_closed() -> None:
    frozen = json.loads(FROZEN.read_text())
    pending = set(frozen["evidence_boundary"]["not_proved_here"])
    assert "concrete mmgroup words for U4(2) inside M" in pending
    assert "unique Monster class fusion" in pending
    assert "Leech embedding of the W33 projector lattice" in pending
