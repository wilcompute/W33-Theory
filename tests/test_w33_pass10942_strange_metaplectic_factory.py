import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10942_strange_metaplectic_factory.py"
CERT = ROOT / "data/w33_pass10942_strange_metaplectic_factory.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays():
    subprocess.run([sys.executable, str(PRODUCER)], cwd=ROOT, check=True,
                   capture_output=True, text=True, timeout=40)


def test_exact_factory_and_injection_certificate():
    x = load()
    assert x["status"] == "PASS_DARK_STRANGE_TO_SEVEN_QUTRIT_METAPLECTIC_UNIVERSAL_PORT"
    a = x["two_strange_to_norell"]
    b = x["two_norell_to_reflection_magic"]
    assert a["acceptance_probability"] == {"numerator": 1, "denominator": 2}
    assert b["acceptance_probability"] == {"numerator": 1, "denominator": 4}
    assert max(a["projective_output_error"], b["corrected_output_error"]) < 3e-12
    f = x["four_strange_factory"]
    assert f["pure_batch_success_probability"] == {"numerator": 1, "denominator": 16}
    assert f["buffered_expected_Strange_states_per_R"] == 32
    assert f["buffered_expected_Strange_states_per_injected_R_gate"] == 96
    inj = x["reflection_injection"]
    assert inj["R_is_Clifford"] is False
    assert inj["R_magic_maximum_stabilizer_fidelity"] == {"numerator": 7, "denominator": 9}
    assert inj["tracked_branch_group_projective_order"] == 4
    assert inj["repeat_until_success_expected_R_resources"] == 3
    assert all(row["maximum_error"] < 3e-12 for row in inj["branches"])


def test_noise_firewall_and_two_universal_lanes():
    x = load()
    n = x["noise_transfer"]
    assert n["strictly_amplifies_depolarizing_error_for_0_lt_p_lt_1"] is True
    assert n["small_p_output_error"] == "q(p)=8*p/3+O(p^2)"
    assert n["strict_amplification_sign_certificate"]["remaining_quadratic_discriminant"] == -156
    assert n["role"].endswith("not itself a distillation protocol")
    c = x["cyclotomic_firewall"]
    assert c["field_degree_K_over_Q"] == 4
    assert c["field_degree_Q_zeta9_over_Q"] == 6
    assert c["exact_Strange_to_T_by_finite_stabilizer_protocol"] is False
    vm = x["seven_qutrit_vm"]
    assert vm["applicable_modes"] == list(range(7))
    assert vm["logical_gate_set"] == "seven-qutrit Clifford+R"
    assert vm["ideal_algebraic_universality"] == "approximately universal"


def test_visible_surfaces_are_unique():
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(encoding="utf-8")
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    report = (ROOT / "analysis/PASS10942_RESERVATION.md").read_text(encoding="utf-8")
    assert tail.count("PASS10942_STRANGE_METAPLECTIC_FACTORY_INSERT") == 1
    assert docs.count('id="pass10942-strange-metaplectic-factory"') == 1
    assert "resource converter, not a distiller" in report
    assert "cyclotomic" in report.lower()
