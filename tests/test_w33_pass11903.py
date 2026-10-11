import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11903_local_ten_locks_charm_up.json"


def test_local_ten_locks_charm_up():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11903_local_ten_locks_charm_up.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["models"] == 491 and d["local_ten_models"] == 152 and d["up_escape_capable"] == []
