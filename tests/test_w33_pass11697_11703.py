"""Regression tests for Passes 11697-11702 (chirality vacuum, Coble covariant, central triality, clock breaking)."""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass11663_odd_weil_normal_map as C  # noqa: E402
import w33_pass11697_11698_chirality_vacuum as V  # noqa: E402
import w33_pass11699_coble_covariant_is_maschke_map as K  # noqa: E402
import w33_pass11701_11702_clock_symmetry_breaking as B  # noqa: E402

DATA = ROOT / "data"


def test_parity_identity_one_and_two_qutrits():
    rng = np.random.default_rng(0)
    for n in (1, 2):
        d = 3 ** n
        ops = [V.weyl(v) for v in V.nonzero(n)]
        P = V.parity(n)
        for _ in range(5):
            psi = rng.normal(size=d) + 1j * rng.normal(size=d)
            psi /= np.linalg.norm(psi)
            a = np.array([np.vdot(psi, O @ psi) for O in ops])
            assert abs((a.imag ** 2).sum() - d / 2 * (1 - np.vdot(psi, P @ psi).real ** 2)) < 1e-12


def test_line_stabiliser_state_attains_27_over_8_and_random_states_do_not_exceed():
    ops = [V.weyl(v) for v in V.nonzero(2)]

    def S4(p):
        return (np.array([np.vdot(p, O @ p) for O in ops]).imag ** 4).sum()
    A, Bm = V.weyl((0, 1, 0, 0)), V.weyl((0, 0, 0, 1))      # Z1, Z2: a Lagrangian line
    psi = np.zeros(9, complex)
    psi[3 * 1 + 2] = 1                                         # joint eigenstate with characters (1, 2)
    assert np.allclose(A @ psi, np.vdot(psi, A @ psi) * psi) and np.allclose(Bm @ psi, np.vdot(psi, Bm @ psi) * psi)
    assert abs(S4(psi) - 27 / 8) < 1e-12
    psi0 = np.zeros(9, complex)
    psi0[0] = 1                                                # trivial character
    assert abs(S4(psi0)) < 1e-12
    rng = np.random.default_rng(1)
    for _ in range(50):
        p = rng.normal(size=9) + 1j * rng.normal(size=9)
        assert S4(p / np.linalg.norm(p)) <= 27 / 8 + 1e-12


def test_coble_covariant_is_minus_two_maschke_quartic():
    rng = np.random.default_rng(2)
    H = K.E.cartan_trivectors()
    ys = rng.normal(size=(40, 9)) + 1j * rng.normal(size=(40, 9))
    CB = K.cubic_basis(ys)
    for _ in range(3):
        c = rng.normal(size=4) + 1j * rng.normal(size=4)
        P = K.coble_cubic(c @ H, ys)
        b = np.linalg.lstsq(CB, P, rcond=None)[0]
        assert np.linalg.norm(CB @ b - P) < 1e-9 * np.linalg.norm(P)
        assert np.linalg.norm(b + 2 * C.quartic(c)) < 1e-9 * np.linalg.norm(b)


def test_certificates():
    v = json.load(open(DATA / "w33_pass11697_11698_chirality_vacuum.json"))
    assert v["p11698"]["stabiliser_state_S4_census"] == {"0.0": 40, "3.375": 320}
    assert v["p11698"]["all_starts_reach_max"] and v["p11698"]["carriers_pairwise_collinear"]
    k = json.load(open(DATA / "w33_pass11699_coble_covariant_is_maschke_map.json"))
    assert k["equivariant_quartic_dimensions"] == {"even": 1, "dual_even": 0, "conjugate_even": 0}
    assert k["image_quartics"] == 1 and k["max_norm_on_40_witting_rays"] < 1e-9
    t = json.load(open(DATA / "w33_pass11700_triality_is_central.json"))
    assert not t["any_transposition"] and t["every_gate_has_one_identity_lift"]
    c = json.load(open(DATA / "w33_pass11701_11702_clock_symmetry_breaking.json"))
    assert c["kac"]["min_order_sm_shaped"] == 16 and c["kac"]["min_order_regular"] == 30
    assert c["third_level"]["sm_shaped"] == 0 and set(c["third_level"]["e8_orders"]) == {"1", "3", "9"}
    assert c["pairs"]["types"]["A1+A2"] == 5037660


def test_kac_bound_small_orders():
    kac = B.kac_census(16)
    assert not any(kac[m]["sm_shaped"] for m in range(1, 16)) and kac[16]["sm_shaped"]


def test_two_commuting_clocks_give_sm_shape():
    XY = B.XY
    z = [B.kept(l) for l in B.lifts(B.Z9 ** np.array([3 * x % 9 for x, y in XY]))]
    g1 = [m for m in z if B.typ(m) == ("A2", "E6")][0]
    g2 = B.kept(B.lifts(B.Z9 ** np.array([(y ** 3 + 3 * x * y) % 9 for x, y in XY]))[0])
    assert B.typ(g1 & g2) == ("A1", "A2")
    assert B.decompose(g1 & g2) == {1: 30, 2: 20, 3: 30, 6: 12}


def test_single_third_level_clock_never_sm_shaped_sample():
    rng = np.random.default_rng(3)
    for _ in range(200):
        c1, c2 = rng.integers(3, size=2)
        q = tuple(rng.integers(3, size=7))
        for lam in B.lifts(B.Z9 ** B.expo(c1, c2, q)):
            assert B.typ(B.kept(lam)) != ("A1", "A2")
            assert B.e8_order(lam) in (1, 3, 9)


def test_vacuum_and_clock_share_a_line_certificate():
    r = json.load(open(DATA / "w33_pass11703_vacuum_and_clock_share_a_line.json"))
    assert r["su3_of_line_points_union_is_line_centraliser"]
    assert r["sm_shaped_pairs_with_Z_x_I"] == 1944 and r["colour_or_weak_outside_line"] == 0
    assert sorted(v["count"] for v in r["ordered_colour_weak_pairs"].values()) == [216] * 9
    assert set(r["vacua_with_colour_and_weak_points_chiral"].values()) == {4}
