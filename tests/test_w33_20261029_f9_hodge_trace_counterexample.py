"""Exact GF9 characteristic-three closure counterexample regression."""
from analysis.w33_20261029_f9_hodge_trace_counterexample import verify,mul,add

def test_gf9_scalar_closure_trace_zero_nonmetric():
    r=verify()
    assert r["q"]==9 and r["q_mod4"]==1
    assert r["P_symmetric"] and r["kappa_squared_minus_I"]
    assert r["trace_kappa"]==[0,0]
    assert [r["plus_i_eigenspace_dimension"],r["minus_i_eigenspace_dimension"]]==[6,0]
    assert not r["trace_zero_sufficient_for_Hodge"]

def test_gf9_minimal_polynomial_and_both_eigenvalues():
    assert mul((0,1),(0,1))==(2,0)
    assert add((0,1),(0,2))==(0,0)
    assert (0,1)!=(0,2)
