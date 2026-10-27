import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12322_to_12327_scherk_schwarz_consolidated.json"


def test_scherk_schwarz_consolidated():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12322_to_12327_scherk_schwarz_consolidated.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
