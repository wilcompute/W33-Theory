from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PY_WITNESS = ROOT / "scripts" / "PART_CCCCCXCIX_e8_spectral_w33_bridge.py"
GAP_WITNESS = ROOT / "analysis" / "w33_e8_spectral_descent_scope_audit.g"
REPORT = ROOT / "analysis" / "PART_CCCCCXCIX_E8_SPECTRAL_SCOPE_AUDIT.md"


def run(command):
    return subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    ).stdout


def test_python_exact_spectral_descent_and_40_point_firewall():
    output = run([sys.executable, str(PY_WITNESS)])
    assert "EXACT SPECTRA PASS" in output
    assert "40 points; collinearity graph SRG(40,12,2,4)" in output
    assert "27+6=33 is not a W(3,3) vertex decomposition" in output


def test_gap_independent_w33_construction():
    output = run(["gap", "-q", str(GAP_WITNESS)])
    assert "Error" not in output
    assert "PASS w33_e8_spectral_descent_scope_audit" in output
    assert "spectrum=[12^1,2^24,-4^15]" in output


def test_false_bridge_language_cannot_return_to_executable_surface():
    source = PY_WITNESS.read_text(encoding="utf-8")
    for forbidden in (
        "W33 extra vertices",
        "W33 = 27",
        "8 doubled doily layers",
        "ALL THEOREMS PASS",
    ):
        assert forbidden not in source


def test_audit_names_prior_owners_and_real_matrix_bridge():
    report = REPORT.read_text(encoding="utf-8")
    for required in (
        "PASS7163_7170_e8_hexagonal_lift_insert.tex",
        "BT7171_BT7186_e8_d4_h27_q9.md",
        "PASS7017_7024_schlafli_w33_equivariant_no_go.md",
        "Passes 7317–7320",
        "T_0",
        "R_0",
        "N_0",
    ):
        assert required in report
