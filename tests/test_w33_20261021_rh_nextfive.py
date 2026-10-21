"""Focused replay of the five follow-up research frontiers; each PASS is scoped."""
from analysis.w33_20261021_rh_nextfive import (
    hecke_obstruction,levi_conjugator,weil_completed_galerkin,
    apartment_classification,spectral_determinant_falsifier
)
def test_hecke_obstruction():
    r=hecke_obstruction()
    assert r["trivial_rep_to_24D_Hom_dimension"]==0
    assert r["trivial_rep_to_15D_Hom_dimension"]==0
def test_levi_rational_conjugator():
    r=levi_conjugator()
    assert r["rational_rank_witness_mod101"]==156
    assert r["transvection_mod101"]["order3"]
    assert r["transvection_mod101"]["nontrivial"]
def test_real_arithmetic_weil_formula():
    r=weil_completed_galerkin()
    assert r["min_eigenvalue"]>0
    assert max(abs(v["formula_minus_zero_sum"]) for v in r["cross_checks"].values())<5e-10
def test_apartment_holonomy_spanning():
    r=apartment_classification()
    assert r["apartments"]==1620 and r["cycle_space_rank"]==81
    assert r["undetected_non_gauge_signings"]==0
    assert r["canonical_chord_coordinates"]==81
    assert r["random_tempered"]==126 and r["random_untempered"]==2
    assert r["all_single_chord_signings_untempered"]
def test_infinite_spectral_determinant_negative_control():
    r=spectral_determinant_falsifier()
    assert not r["exact_Xi_determinant"]
    assert abs(r["normalized_determinants"]["10"]["relative_error"])>.5
