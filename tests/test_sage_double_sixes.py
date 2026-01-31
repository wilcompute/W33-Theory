import subprocess
from pathlib import Path

import pytest

SCRIPT = Path("tools") / "sage_double_sixes.py"


def test_sage_double_sixes_runs_if_sage_available():
    # Skip if 'sage' runtime not available
    import shutil

    if shutil.which("sage") is None:
        pytest.skip("sage not available")

    res = subprocess.run(["sage", str(SCRIPT)], capture_output=True, text=True)
    assert res.returncode == 0, res.stdout + "\n" + res.stderr
    p = Path("artifacts") / "sage_double_sixes.json"
    assert p.exists()
