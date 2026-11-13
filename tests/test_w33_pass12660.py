"""Pass 12660: validated type B bound, stabiliser gap at q = 8, five-qubit 9-set census."""
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_typeB_margin_certificate():
    d = load("w33_typeB_degree6_margin.json")
    assert d["delta0"] == 0.044 and d["status"] == "optimal" and d["validated"]
    assert d["min_eig_K_after"] > 1e-3 and d["min_eig_G_after"] > 1e-3
    assert d["residual_after"] < 1e-12 and d["correction_frobenius"] < 1e-9 * d["t"] * 1e3
    s = np.load(os.path.join(ROOT, "data", "w33_typeB_degree6_margin_solution.npz"))
    assert s["K0"].shape == (51, 51) and s["G0"].shape == (136, 136)
    assert np.linalg.eigvalsh(s["K0"])[0] > 1e-3 and np.linalg.eigvalsh(s["G0"])[0] > 1e-3
    assert np.abs(s["K0"] - s["K0"].conj().T).max() < 1e-12


def test_stabiliser_minimum():
    d = load("w33_regulus_stabiliser_minimum.json")
    assert [d[f"q{q}"]["m_star_found"] for q in (2, 4, 8, 16)] == [1, 1, 3, 1]
    assert d["q8"]["steps"] > 10 ** 6


def test_f8_minimiser_structure():
    d = load("w33_f8_minimiser_structure.json")
    assert abs(d["c"] - 2.498508646688) < 1e-8 and abs(d["dF_from_paulis"] - d["c"]) < 1e-9
    assert d["stabiliser_size"] == 4 and d["stabiliser_all_uncovered_or_identity"] and d["n_covered"] == 567
    zero_cov = [c for v, c in d["covered_levels"] if abs(v) < 1e-9]
    assert zero_cov == [504]
    A = np.load(os.path.join(ROOT, "data", "w33_f8_minimiser.npy"))
    assert A.shape == (8, 8) and abs(np.linalg.norm(A) - 1) < 1e-12


def test_census():
    d = load("w33_five_qubit_nine_set_census.json")
    assert len(d) == 15
    weak = [r for r in d if not r["name"].startswith("quotient")]
    strong = [r for r in d if r["name"].startswith("quotient")]
    assert len(weak) == 13 and all(abs(r["c"] - 1) < 1e-7 and r["n_simple_eigs"] == 271 for r in weak)
    assert len(strong) == 2 and all(abs(r["c"] - 2.498508646688) < 1e-7 and r["n_simple_eigs"] == 1 for r in strong)
