from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass179_poisson_modular_pair.py"
DATA = ROOT / "data" / "w33_pass179_poisson_modular_pair.json"
NOTE = ROOT / "PASS179_SENTINEL_CONTEXT_POISSON_PAIR.md"


def payload() -> dict:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
        timeout=60,
    )
    assert '"status": "PASS"' in completed.stdout
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_pass179_exact_dual_and_poisson_normalization() -> None:
    result = payload()
    assert result["status"] == "PASS"
    assert result["checks"] and all(result["checks"].values())
    pair = result["pair"]
    assert pair["euclidean_dual"] == "A^vee = (1/2)B"
    assert pair["euclidean_indices"] == {"A": 2**25, "B": 2**15}
    assert pair["euclidean_covolumes"] == {
        "A": "2^25",
        "(1/2)B": "2^-25",
    }
    assert pair["half_form_determinants"] == {"A": "2^10", "B": "2^-10"}
    assert "2^-25 t^-20" in pair["identity"]
    assert "1/(4t)" in pair["identity"]


def test_pass179_complete_macwilliams_and_shells() -> None:
    result = json.loads(DATA.read_text(encoding="utf-8"))
    macwilliams = result["macwilliams"]
    enumerator = {
        int(weight): count
        for weight, count in macwilliams["context_weight_enumerator"].items()
    }
    assert macwilliams["all_41_divisions_exact"] is True
    assert macwilliams["transform_back_matches_all_41_coefficients"] is True
    assert sum(enumerator.values()) == 2**25
    assert [enumerator.get(weight, 0) for weight in range(7)] == [
        1,
        0,
        0,
        0,
        40,
        0,
        240,
    ]
    assert result["sentinel_shells_scaled_0_to_40"][:5] == [
        1,
        0,
        80,
        0,
        14640,
    ]
    assert result["context_shells_scaled_0_to_40"][:5] == [
        1,
        0,
        720,
        15360,
        1350960,
    ]


def test_pass179_finite_values_are_not_presented_as_a_proof() -> None:
    result = json.loads(DATA.read_text(encoding="utf-8"))
    assert "poisson_certificate" not in result
    assert set(result["finite_shell_numerical_corrob"]) == {"0.45", "0.5", "0.55"}
    assert "only corroborate" in result["reading"]
    source = SCRIPT.read_text(encoding="utf-8")
    note = NOTE.read_text(encoding="utf-8")
    assert "They are not a proof" in source
    assert "finite shell window cannot prove" in note

