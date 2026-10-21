import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12174_to_12179_real_forms_decide_the_string.json"


def test_real_forms_decide_the_string():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12174_to_12179_real_forms_decide_the_string.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
