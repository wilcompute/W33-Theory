import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11908_split_ten_scan_beyond_a8.json"


def test_split_ten_scan_beyond_a8():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11908_split_ten_scan_beyond_a8.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["combined_models"] == 600 and d["combined_up_escape"] == 0
