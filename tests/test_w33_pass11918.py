import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11918_tilt_ckm_and_up_lemma.json"


def test_tilt_ckm_and_up_lemma():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11918_tilt_ckm_and_up_lemma.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
