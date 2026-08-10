import subprocess
from pathlib import Path
import json

def test_quantum_channel_symmetry(tmp_path):
    # create a simple transposition permutation file
    perm = [1, 0, 2, 3]
    perm_file = tmp_path / "perm.json"
    perm_file.write_text(json.dumps(perm, encoding="utf-8"))
    repo = Path(__file__).resolve().parents[1]
    res = subprocess.run([".venv\\Scripts\\python.exe", str(repo / "tools" / "quantum_channel_symmetry.py"),
                          "--perm_file", str(perm_file)], cwd=repo, capture_output=True, text=True)
    assert res.returncode == 0
    out = res.stdout
    assert "unitary? True" in out
