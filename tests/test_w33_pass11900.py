import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11900_three_generations_over_a_w33_point.json"


def test_three_generations_over_a_w33_point():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11900_three_generations_over_a_w33_point.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["centraliser_projective"] == 648
    assert d["class_images"]["1"]["modular_projective"] == 216
