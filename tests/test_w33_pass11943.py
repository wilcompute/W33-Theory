import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11943_pmns_no_go_and_lepton_band.json"


def test_pmns_no_go_and_lepton_band():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11943_pmns_no_go_and_lepton_band.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
