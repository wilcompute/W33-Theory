"""Scoped regression checks for five October-21 RH frontier followups."""
from analysis.w33_20261021_rh_next5_deep import (
  levi_conjugator, hecke_obstruction, apartment_holonomy,
  spectral_determinant, completed_weil_galerkin
)

def test_levi_complete_rational_conjugator():
    x=levi_conjugator()
    assert x["rank"]==156 and x["integer_TS_equals_SC"]
    assert x["symplectic_transvection_intertwiner_mod101"]

def test_hecke_invariant_obstruction():
    x=hecke_obstruction()
    assert x["Hom_G_of_trivial_E4_line_into_W33_nonconstant"]==0

def test_apartment_holonomy_classification():
    x=apartment_holonomy()
    assert x["cycle_space_GF2_rank"]==81 and x["octagons"]==1620
    assert sum(x["two_edge_flip_histogram"].values())==12720
    assert x["two_edge_flip_histogram"]=={108:480,144:1440,156:4320,160:6480}

def test_xi_normalized_determinant_falsifier():
    x=spectral_determinant()
    assert x["N"]==1200
    assert x["baseline_error"][-1]>.5
    assert x["inverse_moments"]["4"]["baseline"] < x["inverse_moments"]["4"]["actual_first60_lower_bound"]

def test_completed_prime_gamma_pole_weil_matrix():
    x=completed_weil_galerkin()
    assert x["max_difference"]<1.e-9
    assert min(x["eigenvalues"])>-1e-10
