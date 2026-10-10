import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass11897_11898_kahler_moduli_two_qutrit_weil.json"


def test_kahler_moduli_two_qutrit_weil():
    subprocess.run([sys.executable, str(ROOT / "analysis" / "w33_pass11897_11898_kahler_moduli_two_qutrit_weil.py")],
                   check=True, cwd=ROOT, capture_output=True)
    d = json.loads(CERT.read_text())
    assert d["all_checks_pass"]
    assert d["part_11897"]["projective_order_full"] == 51840
    assert d["part_11897"]["projective_order_diagonal_moduli"] == 576
    assert d["part_11898"]["sp63_order"] == 9170703360
