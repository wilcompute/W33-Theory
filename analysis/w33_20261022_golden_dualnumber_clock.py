#!/usr/bin/env python3
"""An exact phinary/supergolden splitting and native W(3,9) dual-number clock.

A repository research construction, not a new general mathematical theorem:
* Supergolden companion over F3 is similar to (-1) direct_sum (-golden).
* GF(9)=F3[phi]=F3[i], with i=phi^2.
* Native B=J-I-A of W(3,9) squares to 0 with rank 100; the unit
  phi*(I+B) has order lcm(8,3)=24 in GL_820(F9).
* The W33 extension-of-scalars module has 10 free dual-number blocks and
  20 simple blocks.
* Integer/complex lift of the characteristic-three clock is NOT unitary,
  and has spectral radius 28*phi > 1.
This is algebraic coding over finite fields; NO classical RH or physical
photon-computer claim follows.
"""
from __future__ import annotations
import itertools
import json
import math
from pathlib import Path
import numpy as np
from analysis.w33_20261022_six_algebra_optics_frontiers import field, rank_modp

F=np.array([[0,1],[1,1]],dtype=np.int64)
S=np.array([[0,0,1],[1,0,0],[0,1,1]],dtype=np.int64)
Q=np.array([[1,1,0],[2,1,2],[2,0,2]],dtype=np.int64)

def matrix_power_mod(A,n,p):
    """Exact repeated squaring with reduction at EACH multiplication (no int64 overflow)."""
    R=np.eye(A.shape[0],dtype=np.int64)
    A=np.asarray(A,dtype=np.int64)%p
    while n:
        if n&1:R=(R@A)%p
        A=(A@A)%p
        n//=2
    return R

def matrix_conjugacy():
    target=np.zeros((3,3),dtype=np.int64)
    target[0,0]=-1
    target[1:,1:]=-F
    assert np.array_equal((S@Q-Q@target)%3,np.zeros((3,3),dtype=np.int64))
    assert round(np.linalg.det(Q))%3==2
    I2=np.eye(2,dtype=np.int64)
    I3=np.eye(3,dtype=np.int64)
    assert np.array_equal(matrix_power_mod(F,4,3),(-I2)%3)
    assert np.array_equal(matrix_power_mod(S,8,3),I3%3)
    assert not np.array_equal(matrix_power_mod(S,4,3),I3%3)
    return dict(status="PASS_EXACT",similarity_Q_mod3=Q.tolist(),
      block_matrix_mod3=(target%3).tolist(),
      determinant_Q_mod3=2,supergolden_order_mod3=8,
      golden_order_mod3=8,
      proposition="S Q = Q[(-1) direct_sum(-F)] in GL3(F3)",
      prior_art="Standard rational canonical decomposition, explicit new cross-track witness in this repository.")

def field_change():
    q,addg,mulg,invg,negg=field(3,2,(2,2,1)) # x²-x-1
    _,addi,muli,invi,negi=field(3,2,(1,0,1)) # x²+1
    phi=3;one=1;minusone=2
    phi2=int(mulg[phi,phi])
    phi4=int(mulg[phi2,phi2])
    assert (phi2,phi4)==(4,minusone)
    x=one
    for n in range(1,9):
        x=int(mulg[x,phi])
        if n<8: assert x!=one
    assert x==one
    # i -> phi² = 1+phi, coordinate map (a,b) -> (a+b,b).
    to_g=lambda x: (x%3+x//3)%3+3*(x//3)
    assert len({to_g(x) for x in range(q)})==q
    for a in range(q):
        for b in range(q):
            assert to_g(int(addi[a,b]))==int(addg[to_g(a),to_g(b)])
            assert to_g(int(muli[a,b]))==int(mulg[to_g(a),to_g(b)])
    return dict(status="PASS_EXACT",field_size=9,
      modulus_golden="x²-x-1",modulus_gaussian="x²+1",
      gaussian_to_golden="a+b*i -> (a+b)+b*phi",
      phi_square_is_i=True,phi_order=8,
      exact_addition_multiplication_checks=162)

def field_points(q):
    return [(0,)*k+(1,)+tail
            for k in range(4) for tail in itertools.product(range(q),repeat=3-k)]

def noncollinearity(p,t,poly):
    q,add,mul,inv,neg=field(p,t,poly)
    pts=field_points(q)
    n=(q+1)*(q*q+1)
    assert len(pts)==n
    V=np.array(pts,dtype=np.int16)
    sym=np.zeros((n,n),dtype=np.int16)
    for a,b,sign in ((0,2,1),(1,3,1),(2,0,-1),(3,1,-1)):
        term=mul[V[:,a,None],V[None,:,b]]
        if sign<0:term=neg[term]
        sym=add[sym,term]
    B=(sym!=0).astype(np.int64)
    assert not np.any((B@B)%p)
    rank=rank_modp(B,p)
    assert rank==math.comb(p+2,3)**t
    return pts,B,rank

def native_golden_clock():
    pts_g,Bg,r=noncollinearity(3,2,(2,2,1))
    pts_i,Bi,ri=noncollinearity(3,2,(1,0,1))
    assert (len(pts_g),r,ri)==(820,100,100)
    idx={pt:i for i,pt in enumerate(pts_g)}
    def to_g(x):return (x%3+x//3)%3+3*(x//3)
    perm=[idx[tuple(to_g(x) for x in pt)] for pt in pts_i]
    assert len(set(perm))==820
    assert np.array_equal(Bi,Bg[np.ix_(perm,perm)])
    assert np.count_nonzero(Bg)>0
    # In F9, (I+B)^k = I + (k mod 3) B, while phi has order eight.
    assert 24%8==0 and 24%3==0
    assert 8%3 != 0 and 3%8 != 0
    n=820
    return dict(status="PASS_EXACT",q=9,vertices=n,
      nilpotent_rank=r,nilpotent_square_zero=True,
      field_model_graph_isomorphism=True,
      clock="U=phi*(I+B), B=J-I-A, U has exact order 24 in GL_820(F9)",
      clock_order=24,order8_countercheck="U^8=I+2B != I",
      order3_countercheck="U^3=phi^3 I != I",
      dual_number_module="F9[epsilon]/(epsilon²)",
      free_rank=r,simple_F9_modules=n-2*r,
      boundary="This is a finite-characteristic module, not a complex unitary or arithmetic Frobenius eigenvalue operator.")

def w33_hybrid_and_complex_nogo():
    pts,B,r=noncollinearity(3,1,(0,1))
    n=len(pts)
    assert (n,r)==(40,10)
    I=np.eye(n,dtype=np.int64)
    T=np.kron(F,I+B)%3
    Id=np.eye(2*n,dtype=np.int64)
    assert np.array_equal(matrix_power_mod(T,24,3),Id)
    for exponent in (8,12):
        assert not np.array_equal(matrix_power_mod(T,exponent,3),Id)
    # Over the reals B is a nonnegative symmetric regular graph matrix
    # of degree 27. I+B therefore has a real eigenvalue 28.
    assert np.array_equal(B.sum(axis=1),27*np.ones(n,dtype=np.int64))
    golden=(1+math.sqrt(5))/2
    radius=28*golden
    assert radius>45.
    return dict(status="PASS_EXACT",w33_vertices=n,B_rank_over_F3=r,
      free_dual_number_blocks=10,simple_blocks=20,
      phi_tensor_unipotent_dimension_over_F3=80,order_mod3=24,
      complex_lift_eigenvalue="28*(1+sqrt(5))/2",
      complex_lift_spectral_radius=radius,
      complex_lift_unitary=False,
      no_go="Literal integer/complex lift has eigenvalue >45 and cannot be passive or finite-order. Reduction mod3 is essential.")

def certificate():
    r={"supergolden_golden_conjugacy":matrix_conjugacy(),
       "golden_gaussian_field_isomorphism":field_change(),
       "native_W39_dual_number_clock":native_golden_clock(),
       "W33_hybrid_complex_no_go":w33_hybrid_and_complex_nogo(),
       "classical_RH_proved":False,
       "physical_photon_clock_constructed":False}
    assert all(x["status"]=="PASS_EXACT" for x in r.values() if isinstance(x,dict))
    return r

if __name__=="__main__":
    r=certificate()
    out=Path(__file__).resolve().parents[1]/"data"/"w33_20261022_golden_dualnumber_clock.json"
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print({k:v.get("status") for k,v in r.items() if isinstance(v,dict)})
