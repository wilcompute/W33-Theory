import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass178_even_q_closed_form.py"
DATA = ROOT / "data" / "w33_pass178_even_q_closed_form.json"
NOTE = ROOT / "PASS178_EVEN_Q_INCIDENCE_RANK_TRANSFER.md"


def test_pass178_theorem_backed_witness_runs():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    assert completed.returncode == 0, completed.stderr or completed.stdout


def test_pass178_integral_transfer_and_q32_falsifier():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())
    assert payload["theorem"]["integral_transfer_matrix"] == [[4, 2], [2, 5]]
    assert payload["ranks"] == {
        "2": 10,
        "4": 50,
        "8": 298,
        "16": 1890,
        "32": 12250,
        "64": 80018,
        "128": 524170,
        "256": 3437250,
    }
    assert payload["q32_correction"] == {
        "theorem_value": 12250,
        "rejected_interpolant_value": 12794,
        "difference": -544,
    }

    note = NOTE.read_text(encoding="utf-8")
    assert "Sastry" in note and "Peter Sin" in note
    assert "\\boxed{r_n=1+\\operatorname{tr}(B^n)}" in note
    assert "not claimed" in note
