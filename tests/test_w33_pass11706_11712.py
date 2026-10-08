"""Regression tests for Passes 11706-11711 (vacuum/clock compatibility, hypercharge, single tick, n-qutrit vacua)."""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass11697_11698_chirality_vacuum as V  # noqa: E402
import w33_pass11701_11702_clock_symmetry_breaking as B  # noqa: E402
import w33_pass11706_11709_vacuum_clock_hypercharge as H  # noqa: E402

DATA = ROOT / "data"
XY = B.XY


def _mask(f, k):
    return B.kept(B.lifts(B.Z9 ** np.array([f(x, y) % 9 for x, y in XY]))[k])


def test_minimal_clock_hamiltonian_reproduces_the_e8_element():
    lam = B.lifts(B.Z9 ** np.array([(y ** 3 + 3 * x * y) % 9 for x, y in XY]))[0]
    h = H.minimal_h(lam)
    assert abs(h.sum()) < 1e-9
    for kind, idx, v in B.T.ROOTS:
        val = lam[idx[0]] / lam[idx[1]] if kind == "A" else (lam[idx[0]] * lam[idx[1]] * lam[idx[2]]) ** (1 if kind == "L" else -1)
        assert abs(np.exp(2j * np.pi * (v @ h)) - val) < 1e-7


def test_operator_type_sm_and_free_vacua():
    m = _mask(lambda x, y: 3 * x * y * y, 1) & _mask(lambda x, y: x ** 3 + 3 * x * y + 3 * x * x * y, 1)
    assert B.typ(m) == ("A1", "A2")
    idx = np.nonzero(m)[0]
    assert all(H.KIND[j] == "A" for j in idx)
    support = {t for r in idx for t in B.T.ROOTS[r][1]}
    for s in range(1, 9):
        rho = -np.eye(9, dtype=complex) / 9
        rho[s, s] += 1
        assert all(H.commutes(rho, j) for j in idx) == (s not in support)
    comps = H.su5_completions(m)
    assert len(comps) == 6
    op = [Y for roots, Y in comps.items() if all(H.KIND[H.RKEY[r]] == "A" for r in roots)]
    assert len(op) == 1
    free = [t for t in range(1, 9) if t not in support]
    assert all(abs(op[0][t]) < 1e-9 for t in free)
    assert sorted(round(6 * float(op[0][t])) for t in range(9) if abs(op[0][t]) > 1e-9) in ([-3, -3, 2, 2, 2], [-2, -2, -2, 3, 3])
    for Y in comps.values():
        assert all(k in H.SM_ALLOWED for k in H.spectrum(m, Y))


def test_single_fourth_level_tick():
    z27 = np.exp(2j * np.pi / 27)
    lam = B.lifts(z27 ** np.array([(2 * x ** 3 + 26 * y ** 3) % 27 for x, y in XY]))[1]
    assert B.typ(B.kept(lam)) == ("A1", "A2") and B.e8_order(lam) == 27


def test_n_qutrit_quartic_bound():
    rng = np.random.default_rng(4)
    for n in (1, 2):
        d = 3 ** n
        ops = [V.weyl(v) for v in V.nonzero(n)]

        def S4(p):
            return (np.array([np.vdot(p, O @ p) for O in ops]).imag ** 4).sum()
        psi = np.zeros(d, complex)
        psi[-1] = 1
        assert abs(S4(psi) - 9 / 8 * 3 ** (n - 1)) < 1e-12
        for _ in range(30):
            p = rng.normal(size=d) + 1j * rng.normal(size=d)
            assert S4(p / np.linalg.norm(p)) <= 9 / 8 * 3 ** (n - 1) + 1e-12


def test_certificates():
    c = json.load(open(DATA / "w33_pass11706_11709_vacuum_clock_hypercharge.json"))
    assert all(x["dim"] == 64 and x["max_trivector_component"] < 1e-9 for x in c["p11706"]["pure_state_centraliser"])
    assert all(v["triples_are_eigenspaces_of_D_q"] for v in c["p11706"]["line_su3"].values())
    assert c["p11707"]["operator_type_sm_pattern_pairs"] == 83592
    assert list(c["p11707"]["census"]) == ["completions=6 all_operator=1 standard=True vacuum_disjoint=True"]
    assert list(c["p11708"]["vector_criterion"]) == ["1 hypercharge(s), all-operator=[True]"]
    s = json.load(open(DATA / "w33_pass11710_11711_single_tick_and_n_qutrit_vacua.json"))
    assert s["sm_shaped"] == 648 and s["e8_orders"] == {"27": 648}
    for n, v in s["quartic_vacua"].items():
        assert v["starts_at_bound"] == v["starts"] and abs(v["stabiliser_value"] - v["bound"]) < 1e-9
