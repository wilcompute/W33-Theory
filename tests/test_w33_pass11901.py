import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11901_kahler_loophole_closed.json"


def test_kahler_loophole_closed():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11901_kahler_loophole_closed.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["geo_patterns"] == {"[0, 1, 1]": 72}
