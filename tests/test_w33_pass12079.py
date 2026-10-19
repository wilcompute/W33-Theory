import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12079_a_context_of_clocks_is_a_hamming_code.json"


def test_a_context_of_clocks_is_a_hamming_code():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12079_a_context_of_clocks_is_a_hamming_code.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
