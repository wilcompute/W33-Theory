import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12131_to_12135_kY_law_moduli_exotics.json"


def test_kY_law_moduli_exotics():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12131_to_12135_kY_law_moduli_exotics.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
