import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_generate_conjugators_matches_committed(tmp_path: Path) -> None:
    committed_path = ROOT / "proofs" / "lean" / "conjugators_generated.lean"
    if not committed_path.exists():
        pytest.skip(f"Missing committed Lean conjugator fixture: {committed_path}")
    out = tmp_path / "conjugators_generated.lean"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate_conjugators_lean.py"),
            "--out",
            str(out),
        ],
        check=True,
        cwd=ROOT,
    )
    committed = committed_path.read_text(encoding="utf-8")
    generated = out.read_text(encoding="utf-8")
    assert generated == committed
