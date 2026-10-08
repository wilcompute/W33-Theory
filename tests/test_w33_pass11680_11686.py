"""Regression for Passes 11680-11681 (Claude track): Pauli-invariant cubic tensors and E8 built from two qutrits."""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))


def load(name):
    return json.load(open(ROOT / "data" / name))


def test_11680_cubic_tensors():
    d = load("w33_pass11680_heisenberg_cubic_tensors.json")
    for n, (s, a) in {"n1": (2, 1), "n2": (5, 4), "n3": (14, 13)}.items():
        v = d[n]
        assert v["sym_dim"] == s and v["alt_dim"] == a and v["mixed_dim"] == 0
        assert v["all_T_u_invariant"] and v["three_cycles_fix_T_u"] and v["transposition_sends_T_u_to_T_minus_u"]
    for n in ("n1", "n2"):
        c = d[n]["clifford_spectra"]
        assert c["sym_conj_even"] == c["alt_conj_odd"] == c["words"]


def test_11681_e8_from_two_qutrits():
    d = load("w33_pass11681_e8_from_two_qutrits.json")
    assert abs(d["gamma_from_jacobi"][0] + 1) < 1e-12 and d["jacobi_max_residual_27_type_triples"] < 1e-10
    assert d["cartan_brackets_max"] == 0 and d["ad_h_zero_eigenvalues"] == 8 and d["roots"] == 240
    assert d["distinct_roots"] == 240 and d["witting_rays"] == 40 and d["ray_overlaps"] == [0.0, 0.333333]
    assert d["roots_per_pauli_degree"] == [3] and d["pauli_degrees_carrying_roots"] == 80
    assert d["each_ray_one_w33_point"] and d["distinct_w33_points"] == 40
    assert d["orthogonal_iff_paulis_commute"] == 1560
    assert d["clifford_image_order_on_trivector_cartan"] == 103680 and d["clifford_image_reflections"] == 0
    assert d["conjugation_is_antilinear_automorphism_max_residual"] < 1e-12


def test_11681_live_jacobi_and_cartan():
    import w33_pass11681_e8_from_two_qutrits as E
    rng = np.random.default_rng(7)
    a, b, c = E._rnd(rng, "x"), E._rnd(rng, "k"), E._rnd(rng, "A")
    j = E._add(E.bracket(E.bracket(a, b), c), E.bracket(E.bracket(b, c), a), E.bracket(E.bracket(c, a), b))
    assert np.abs(E._vec(j)).max() < 1e-10
    h = E.cartan_trivectors()
    Z9, Z84 = np.zeros((9, 9), complex), np.zeros(84, complex)
    for x in h:
        for y in h:
            e = E.bracket((Z9, x, Z84), (Z9, Z84, y))
            assert np.abs(E._vec(e)).max() < 1e-12
