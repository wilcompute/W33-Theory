import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("number", [169, 171, 175])
def test_repaired_witness_runs(number):
    names = {
        169: "w33_pass169_canonical_cycles.py",
        171: "w33_pass171_even_q_rank_ladder.py",
        175: "w33_pass175_dual_shell_720.py",
    }
    completed = subprocess.run(
        [sys.executable, str(ROOT / "analysis" / names[number])],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=240,
    )
    assert completed.returncode == 0, completed.stderr or completed.stdout


def test_pass169_orbital_is_not_selected_by_intersections():
    payload = json.loads(
        (ROOT / "data" / "w33_pass169_canonical_cycles.json").read_text(encoding="utf-8")
    )
    assert payload["status"] == "PASS"
    assert payload["partner_rule"]["four_partner_signature"] == {
        "(0, 0, 0, 0)": 40
    }
    assert payload["partner_rule"]["other_zero_class_signatures"] == {
        "(0, 0, 0, 0)": 108
    }
    assert payload["checks"]["intersection_signature_cannot_select_orbital"]
    assert payload["checks"]["components_are_octahedra_exact"]


def test_pass171_headline_checks_are_executable():
    payload = json.loads(
        (ROOT / "data" / "w33_pass171_even_q_rank_ladder.json").read_text(encoding="utf-8")
    )
    assert payload["status"] == "PASS"
    assert payload["table"]["16"]["rank2_M"] == 1890
    assert not payload["table"]["16"]["even_cubic_holds"]
    for name in (
        "even_self_duality_verified",
        "even_AL_formula_survives",
        "even_M_odd_formula_not_universal",
        "even_AP_odd_formula_fails",
        "q16_rank_exact_1890",
        "even_cubic_refuted_at_q16",
    ):
        assert payload["checks"][name]
    assert "even_q_verdict_recorded" not in payload["checks"]


def test_pass175_shell_generates_the_full_dual_lattice():
    payload = json.loads(
        (ROOT / "data" / "w33_pass175_dual_shell_720.json").read_text(encoding="utf-8")
    )
    assert payload["status"] == "PASS"
    structure = payload["structure"]
    assert structure["generated_lattice"] == "L* exactly"
    assert structure["generated_lattice_index_in_Z40"] == 2**15
    assert structure["generated_lattice_half_form_determinant"] == "2^-10"
    assert "greedy_basis_abs_det" not in structure
    assert payload["checks"]["shell_generates_dual_lattice_exactly"]
