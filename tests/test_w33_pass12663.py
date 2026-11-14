"""Pass 12663: parity theorem for Lagrangians on the F_q quadric; exact certificate F >= 11/250 for type B."""
import itertools
import json
import os
import sys
from fractions import Fraction as Fr

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_parity_theorem_samples():
    d = load("w33_lagrangian_quadric_parity.json")
    for q in (2, 4, 8, 16, 32):
        r = d[f"q{q}"]
        assert r["odd_fibres_found"] == 0 and r["all_covered_counts_odd"]
        assert r["moore_det_max_over_ker_trace_samples"] == 0 and r["moore_det_of_field_basis"] != 0
        assert r["control_nonisotropic_subspaces_with_an_odd_fibre"] > 50


def test_exact_certificate_summary():
    d = load("w33_typeB_exact_certificate.json")
    assert d["delta"] == "11/250" and d["n_groups"] == 2601 and d["n_equations"] == 41616
    assert d["equations_exact"] and d["hermitian_exact"] and d["positive_definite_exact"]
    assert d["K_row_sum_bound"] < 1e-6 and d["G_row_sum_bound"] < 1e-6


def test_exact_certificate_identity_end_to_end():
    """Independent of the coefficient bookkeeping: evaluate F(v)|v|^2 - (11/250)|v|^6 and the SOS expression built from the stored
    exact Gram matrices at random v, directly from the 80 basis vectors of the CZ model."""
    sys.path.insert(0, os.path.join(ROOT, "analysis"))
    src = open(os.path.join(ROOT, "analysis", "w33_typeB_degree6_sos.py"), encoding="utf-8").read()
    g = {"__name__": "x", "__file__": os.path.join(ROOT, "analysis", "w33_typeB_degree6_sos.py")}
    exec(src[: src.index("# rows: only same-sector")], g)
    z = np.load(os.path.join(ROOT, "data", "w33_typeB_exact_certificate_gram.npz"))
    tof = lambda A: np.array([[float(Fr(x)) for x in row] for row in A])
    K = tof(z["K_re"]) + 1j * tof(z["K_im"])
    G = tof(z["G_re"]) + 1j * tof(z["G_im"])
    assert K.shape == (51, 51) and G.shape == (136, 136)
    assert np.linalg.eigvalsh(K)[0] > 1e-3 and np.linalg.eigvalsh(G)[0] > 1e-3
    E = g["bases"]([0, 1, 2, 3])
    assert len(E) == 80
    s0K, s0G, shiftK, shiftG, d = g["s0K"], g["s0G"], g["shiftK"], g["shiftG"], 16
    rng = np.random.default_rng(0)
    for _ in range(3):
        v = rng.standard_normal(d) + 1j * rng.standard_normal(d)
        nv = np.vdot(v, v).real
        F = sum((abs(np.vdot(e, v)) ** 2 - nv / d) ** 2 for e in E)
        lhs = F * nv - 11 / 250 * nv ** 3
        rhs = 0.0
        for a in range(d):
            mk = np.array([np.prod([v[i] for i in shiftK(m, a)]) for m in s0K])
            rhs += np.vdot(mk, K @ mk).real
            qg = []
            for qq in s0G:
                (i, j), kk = shiftG(qq, a)
                qg.append(v[i] * v[j] * np.conj(v[kk]))
            qg = np.array(qg)
            rhs += np.vdot(qg, G @ qg).real
        assert abs(lhs - rhs) < 1e-9 * max(1.0, abs(lhs)), (lhs, rhs)
        assert rhs > 0


def test_q128_annealing_consistent_with_conjecture_and_parity():
    runs = [load(f"w33_regulus_stabiliser_q128_seed{s}.json") for s in (0, 1, 2)]
    assert [r["best"] for r in runs] == [47, 49, 51]
    assert all(r["all_counts_odd"] and r["best"] >= r["predicted"] == 43 and r["steps"] > 4 * 10 ** 6 for r in runs)
