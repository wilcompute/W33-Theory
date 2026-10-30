import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12458_to_12465_vacuum_thresholds_klines_mbqc.json"


def test_vacuum_thresholds_klines_mbqc():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12458_to_12465_vacuum_thresholds_klines_mbqc.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=600)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
