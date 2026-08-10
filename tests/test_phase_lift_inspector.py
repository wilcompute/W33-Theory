import json
import subprocess
import sys
from pathlib import Path

import numpy as np


def test_phase_lift_inspector_on_11a(tmp_path):
    # prepare JSON with 11A generators as full 12-point perms
    from scripts.derive_m12_p144_suborbits import perm_from_cycles

    b11 = perm_from_cycles(12, [[1, 4], [3, 10], [5, 11], [6, 12]])
    b21 = perm_from_cycles(12, [[1, 8, 9], [2, 3, 4], [5, 12, 11], [6, 10, 7]])
    data = {"11A": [list(b11), list(b21)]}
    file = tmp_path / "gens.json"
    file.write_text(json.dumps(data, encoding="utf-8"), encoding="utf-8")

    # run inspector as a subprocess to simulate CLI
    proc = subprocess.run(
        [sys.executable, "-m", "scripts.phase_lift_inspector", str(file)],
        cwd=str(Path(__file__).parent.parent),
        capture_output=True,
        text=True,
        timeout=10,
    )
    out = proc.stdout + proc.stderr
    # inspector should either find a lift (and print the group order) or
    # explicitly report that no sign lift exists for the supplied generators.
    assert (
        "monomial group order" in out
        or "no sign lift found" in out
    )
    assert proc.returncode == 0
