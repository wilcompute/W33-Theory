import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass12426_to_12433_distance_dictionary_flux_newparents.json"


def test_distance_dictionary_flux_newparents():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass12426_to_12433_distance_dictionary_flux_newparents.py")],
                   check=True, cwd=ROOT, capture_output=True, timeout=600)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
