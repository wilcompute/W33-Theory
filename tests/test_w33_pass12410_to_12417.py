import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12410_to_12417_closure_proof_alpha_ceiling_tprime.json"


def test_closure_proof_alpha_ceiling_tprime():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12410_to_12417_closure_proof_alpha_ceiling_tprime.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=600)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["12412"]["ceiling"]["rank_A_plus_I_mod3"] == 11
