import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12265_to_12270_strict_engine_and_mirage_census.json"


def test_strict_engine_and_mirage_census():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12265_to_12270_strict_engine_and_mirage_census.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
