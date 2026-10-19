import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12088_the_ckm_phase_is_not_a_clock_phase.json"


def test_the_ckm_phase_is_not_a_clock_phase():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12088_the_ckm_phase_is_not_a_clock_phase.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
