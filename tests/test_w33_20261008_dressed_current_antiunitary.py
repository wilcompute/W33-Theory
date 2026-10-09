"""Regression: all 160 actual edge currents admit dressed antiunitary."""
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("w33_dressed_t",ROOT/"analysis/w33_20261008_dressed_current_antiunitary.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_all_current_factors_swap_exactly():
    data=module.certificate()
    assert data["status"]=="PASS"
    assert data["currents_checked"]==160
    assert data["canonical_cross_product_max_abs"]==0
    assert "T J_e T^-1" in data["quantum_current_invariance"]
    assert data["hamiltonian_invariance"]=="T H T^-1=H for H=sum_e J_e^2"

def test_balanced_bipartite_generality_and_unbalanced_control():
    """Exact U.V=1/m-1/n for every bipartite point/line projection."""
    from fractions import Fraction
    for n in range(2,8):
        for m in range(2,8):
            # One point endpoint 0 and one line endpoint 0; all other
            # choices are equivalent under coordinate permutations.
            up=[int(i==0)-Fraction(1,n) for i in range(n)]
            ul=[int(i==0)-Fraction(1,m) for i in range(m)]
            u=up+ul
            v=up+[-x for x in ul]
            d=[1]*n+[-1]*m
            assert [di*ui for di,ui in zip(d,u)]==v
            assert [di*vi for di,vi in zip(d,v)]==u
            overlap=sum(x*y for x,y in zip(u,v))
            assert overlap==Fraction(1,m)-Fraction(1,n)
            assert (overlap==0)==(n==m)
