import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11884_11886_one_loop_trinification.json"


def test_one_loop_trinification():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11884_11886_one_loop_trinification.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["11885_stability"]["tree_flat_nongauge"] == 55
