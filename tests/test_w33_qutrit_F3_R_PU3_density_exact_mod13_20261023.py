"""Exact SU3 adjoint-irreducibility density certificate verification."""
import sys
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_qutrit_F3_R_PU3_density_exact_mod13_20261023 import (
    proof,gates_and_basis,modp,matrix_rank_mod_p)
def test_exact_pu3_density_certificate():
    r=proof()
    assert r['modular_rank']==63 and r['characteristic_zero_rank_exactly']==63
    assert r['real_commutant_dimension_exactly']==1
    assert r['single_qutrit_approximate_universality_proved']
    assert r['projective_closure']=='PU(3)'
def test_modular_embedding_and_rank_controls():
    assert 4*4%13==3
    assert modp(1/s.sqrt(3))==pow(4,-1,13)
    rank,piv=matrix_rank_mod_p([[1,0,1],[0,1,2],[1,1,3]])
    assert rank==2 and piv==[0,1]
def test_trace_determinant_and_orthogonality():
    F,D,G=gates_and_basis()
    assert s.simplify(s.trace(F*D)+1/s.sqrt(3))==0
    assert s.simplify(s.expand_complex((F*D).det())+s.I)==0
    assert s.simplify(F*F.H-s.eye(3))==s.zeros(3)
    assert all(s.simplify(s.trace(a*b)-2*(i==j))==0
               for i,a in enumerate(G) for j,b in enumerate(G))
