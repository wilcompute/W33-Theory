"""Pass 12673: exact torus eigenvalue formula, certified code-space SOS6, torus-invariant code spaces, global SOS6."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_torus_eigen_formula_exact():
    d = load("w33_f8_torus_eigen_exact.json")
    assert d["all_exact"] and d["sigma_fixed_points"] == 0 and d["all_64_by_pauli_conjugacy"]
    assert d["n_lifts_exact"] >= 3


def test_codespace_sos6_certificates():
    for name, c in (("49_20", "49/20"), ("62_25", "62/25"), ("249_100", "249/100")):
        d = load(f"w33_f8_codespace_sos6_certificate_{name}.json")
        assert d["certified"] and d["C_cert"] == c
        for b in ("block3", "block1"):
            assert d[b]["psd_certified"] and d[b]["frob_E_sq_over_delta_sq"] < 1


def test_torus_invariant_codespaces_q8():
    d = load("w33_regulus_torus_invariant_codespaces_q8.json")
    c8 = (47 - 32 * __import__("math").cos(2 * __import__("math").pi / 9)) / 9
    assert d["order_S"] == 9 and abs(d["best"] - c8) < 1e-8


def test_global_sos6_with_controls():
    d = load("w33_f8_global_sos6.json")
    assert d["status"] == "solved" and 0.75 < d["bound"] < 0.77 and d["gamma_order"] == 378
    a = load("w33_f8_global_sos6_control_all.json")
    assert abs(a["bound"] - 63) < 1e-6
    q4 = load("w33_f8_global_sos6_q4.json")
    assert abs(q4["bound"] / 16 - 0.0452) < 1e-4      # Pass 12660's independent degree-6 value


def test_q32_torus_constructions_at_or_above_11():
    d = load("w33_regulus_torus_invariant_codespaces_q32.json")
    assert d["fixed_subspace_dim"] == 10 and d["uncovered_fixed_vectors"] == 1023 and abs(d["best"] - 11) < 1e-6
    u = load("w33_regulus_torus_clifford_q32_unequal.json")
    assert all(r["best"] > 11 for r in u["runs"])
