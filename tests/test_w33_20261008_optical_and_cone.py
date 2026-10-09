"""Independent small exact physics checks."""
from fractions import Fraction
from math import sqrt
def test_quartic_kurtosis():
    from analysis.w33_20261008_single_edge_photonic_kurtosis import certificate
    x=certificate()
    assert x["exact_kappa4_coefficient"]=="618440/6591"
    assert x["exact_variance_coefficient"]=="5207/3042"
def test_cone_polynomial_degree():
    from analysis.w33_20261008_two_hop_cone_minimality import certificate
    x=certificate()
    assert x["minimal_degree"]==2
    assert x["degree_one_nonzero_solutions"]==0
