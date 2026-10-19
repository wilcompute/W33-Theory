import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12071_what_a_context_of_clocks_leaves_of_e8.json"


def test_what_a_context_of_clocks_leaves_of_e8():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12071_what_a_context_of_clocks_leaves_of_e8.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
