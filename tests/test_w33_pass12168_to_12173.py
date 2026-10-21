import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12168_to_12173_level3_rediscovery_no10_z6i.json"


def test_level3_rediscovery_no10_z6i():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12168_to_12173_level3_rediscovery_no10_z6i.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
