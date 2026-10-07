"""Regression for Passes 11647-11651 (Claude track): union law closed by the semisimple-part lemma, label-blind time on
the equal-spectra locus, the maximal-arrow state, the no-reversal fraction, and the n-qutrit Hesse space."""

import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))


def load(name):
    return json.load(open(ROOT / "data" / name))


def test_11647_union_law_closed():
    d = load("w33_pass11647_union_law_closed.json")
    for n, nonsplit, lemB in (("n2", 1296, 7776), ("n3", 8046, 12600)):
        c = d[n]["counts"]
        assert c["k=0 non-split: Lemma A (A^N semisimple solution, split, dominated) holds"] == nonsplit
        assert c["k=0 non-split: Lemma A FAILS"] == 0
        assert c["k!=0, eigenvector cell: Lemma B (A^3 then semisimple part) holds"] == lemB
        assert c["k!=0, eigenvector cell: Lemma B FAILS"] == 0
        assert c.get("k!=0, other cell: NOT dominated", 0) == 0
    assert Fraction(d["n2"]["mass"]["union law PROVED (theorem + certificate)"]) == Fraction(8639, 8640)
    assert Fraction(d["n3"]["mass"]["union law PROVED (theorem + certificate)"]) == Fraction(28296133, 28304640)


def test_11647_lemma_A_live():
    """recompute Lemma A on the first Mz1 = z1 classes with a non-split reverser"""
    import w33_pass11350_linear_decider as L
    import w33_pass11330_orbit_census as O
    import w33_pass11647_union_law_closed as C
    D = L.Decider(2)
    seen = 0
    for M in np.array(O.all_symplectic(D.wl)[0]) % 3:
        if ((M @ D.z1 - D.z1) % 3).any():
            continue
        st = C.classify(D, M, 3 ** 8)
        if st and st.get("k=0 non-split: Lemma A (A^N semisimple solution, split, dominated) holds"):
            assert not st.get("k=0 non-split: Lemma A FAILS")
            seen += 1
            if seen == 3:
                break
    assert seen == 3


def test_11648_label_blind_sigma():
    d = load("w33_pass11648_label_blind_sigma.json")
    for k, v in d["sigma_restriction"].items():
        assert v["equal"], k
        if int(k) <= 15:
            assert v["certified"], k
    assert d["fits"]["excess_fit_all_degrees"] and d["fits"]["label_blind_fit_all_degrees"]
    assert d["fits"]["degrees"] == [9, 25]
    assert d["lattice_points_on_Sigma"]["all_time_symmetric"]
    assert d["lattice_points_on_Sigma"]["with_other_spectra_distinct"] == 1356


def test_11649_maximal_arrow():
    d = load("w33_pass11649_maximal_arrow_state.json")
    assert d["equals_minus_sqrt3_over_62208"] and d["orbit_size"] == 144 and d["orbit_positive"] == 72
    assert d["starts_reaching_max"] == d["end_points_in_orbit"] == 200
    assert d["three_mubs_share_a_spectrum"] and d["Pi_Z_at_star"] < 1e-15
    import w33_pass11649_maximal_arrow_state as P
    assert abs(abs(P.h6(P.STAR)) - np.sqrt(3) / 62208) < 1e-15
    lo, hi = 1 / 3 - np.sqrt(6) / 12, 1 / 3 + np.sqrt(6) / 12
    for spec in d["mub_spectra_at_star"][1:]:
        assert np.allclose(spec, [lo, 1 / 3, hi])


def test_11650_no_reversal():
    d = load("w33_pass11650_no_reversal_fraction.json")
    assert d["n2"]["affine_decides"] and d["n3"]["affine_decides"]
    assert Fraction(d["n2"]["fractions"]["no reversal"]) == Fraction(1, 40)
    assert Fraction(d["n3"]["fractions"]["no reversal"]) == Fraction(1, 28)
    assert Fraction(1, 52) + Fraction(3, 182) == Fraction(1, 28)
    for s in ("s4", "s5"):
        assert abs(d[s]["fraction"] - 0.037) < 0.004


def test_11651_hesse_space():
    d = load("w33_pass11651_n_qutrit_hesse_space.json")
    n1, n2 = d["n1"], d["n2"]
    assert n1["dimension"] == 2 and n2["dimension"] == 5
    assert n1["order_generated_by_reflections"] == 48 and n1["reflections_by_order"] == {"2": 6, "3": 8}
    assert n2["order_generated_by_reflections"] == 51840 and n2["reflections_by_order"] == {"2": 45}
    assert n2["spectra_match_conjugate_even_Weil"] == 60
    dims2 = {int(k): v for k, v in n2["invariant_dims_by_degree"].items()}
    assert [dims2[k] for k in range(1, 13)] == [0, 0, 0, 1, 0, 1, 0, 1, 0, 2, 0, 3]          # G33: 4, 6, 10, 12, 18
    g = n2["overlap_graphs"]["0.33333333"]
    assert g["degree"] == [12] and g["lam"] == [2] and g["mu"] == [4]
    # which SRG(40,12,2,4): the stabiliser rays are antiregular (Q(4,3), lines of W(3,3)); W(3,3) points are regular
    assert n2["regularity_stabiliser_rays"] == [[4, 2]] and n2["regularity_W33_point_graph"] == [[4, 4]]
    assert abs(n2["norm_affine_in_M3"]["a"] + 1 / 3) < 1e-9 and abs(n2["norm_affine_in_M3"]["b"] - 1 / 6) < 1e-9
    assert n2["triple_product_law"]["max_residual"] > 1e-3
    # live: the one-qutrit Hesse group is G6 (order 48)
    import w33_pass11651_n_qutrit_hesse_space as H
    _, _, _, B, wg = H.setup(1)
    G = H.closure([H.R_of(B, g) for g in wg.values()])
    assert len(G) == 48
