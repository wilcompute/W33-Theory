import os
import subprocess
import sys
from pathlib import Path

import pytest

# simple regression: helper script should report a 24-dimensional eigenspace


def test_24_script():
    repo = Path(__file__).resolve().parents[1]
    if not (repo / "data" / "24_basis.npz").exists():
        pytest.skip(
            "24_basis.npz cache is absent; run scripts/dump_24_vectors.py "
            "--index 1410 --output data/24_basis.npz to enable the search shortcut"
        )
    script = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "scripts", "search_24_subspace.py"
        )
    )
    # limit to run quickly (known solution index is 1410)
    proc = subprocess.run(
        [sys.executable, script, "--limit", "2000"], capture_output=True, text=True
    )
    out = proc.stdout + proc.stderr
    assert "eigenspace size 24" in out, "script did not report a 24-dim eigenspace"
    assert "automorphism 1410" in out, "expected index 1410 in output"


def test_dump_basis():
    dump_script = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "scripts", "dump_24_vectors.py")
    )
    outpath = os.path.join(os.path.dirname(__file__), "..", "data", "test_basis.npz")
    if os.path.exists(outpath):
        os.remove(outpath)
    proc = subprocess.run(
        [sys.executable, dump_script, "--index", "1410", "--output", outpath],
        capture_output=True,
        text=True,
    )
    out = proc.stdout + proc.stderr
    assert os.path.exists(outpath), "basis file was not created"
    # load and check shape
    import numpy as np

    arr = np.load(outpath)["arr_0"]
    assert arr.shape == (81, 24), f"unexpected basis shape {arr.shape}"
