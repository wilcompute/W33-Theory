import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12298_to_12303_preregistered_torsion_levels_textures.json"


def test_preregistered_torsion_levels_textures():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12298_to_12303_preregistered_torsion_levels_textures.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=3000)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
