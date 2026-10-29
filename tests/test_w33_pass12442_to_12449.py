import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12442_to_12449_oddcase_sm2541_universality_priorart.json"


def test_oddcase_sm2541_universality_priorart():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12442_to_12449_oddcase_sm2541_universality_priorart.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=600)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
