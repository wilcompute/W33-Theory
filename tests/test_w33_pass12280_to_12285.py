import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12280_to_12285_scherk_schwarz_brothers_and_coprime_rule.json"


def test_scherk_schwarz_brothers_and_coprime_rule():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12280_to_12285_scherk_schwarz_brothers_and_coprime_rule.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
