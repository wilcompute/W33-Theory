import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12351_to_12356_tachyon_free_z6ii_standard_models.json"


def test_tachyon_free_z6ii_standard_models():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12351_to_12356_tachyon_free_z6ii_standard_models.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
