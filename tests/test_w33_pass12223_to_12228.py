import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12223_to_12228_twisted_tens_three_generations_and_radius.json"


def test_twisted_tens_three_generations_and_radius():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12223_to_12228_twisted_tens_three_generations_and_radius.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
