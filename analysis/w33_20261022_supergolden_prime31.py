#!/usr/bin/env python3
"""Discriminant-controlled exceptional primes for phi and supergolden beta.

phi=x²-x-1: discriminant +5, repeated root at p5.
psi=x³-x²-1: discriminant -31, roots (x-10)(x-11)² mod31.
A six-dimensional faithful tensor module over F31 has exact order930.
Together with classical B rank theorem for W(3,31), this predicts the
full modular Jordan dimensions without constructing a 92,352x92,352 matrix.
No physical period or classical RH claim follows.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from sympy import symbols,discriminant
from analysis.w33_20261022_golden_dualnumber_clock import F,S,matrix_power_mod

def order_mod(a,p):
    x=1
    for n in range(1,p):
        x=x*a%p
        if x==1:return n
    raise AssertionError("no scalar order")

def certificate():
    x=symbols("x")
    d2=int(discriminant(x*x-x-1,x))
    d3=int(discriminant(x*x*x-x*x-1,x))
    assert (d2,d3)==(5,-31)
    p=31;I3=np.eye(3,dtype=np.int64)
    # x³-x²-1 = (x-10)(x-11)² mod31.
    for a in range(p):
        assert (a**3-a*a-1-(a-10)*(a-11)**2)%p==0
    assert not np.any((S-10*I3)@(S-11*I3)@(S-11*I3)%p)
    assert np.any((S-10*I3)@(S-11*I3)%p)
    scalar_orders={"root_10":order_mod(10,p),"root_11":order_mod(11,p)}
    assert scalar_orders=={"root_10":15,"root_11":30}
    # Faithful 6D test represents S ⊗ (I+B) with B a nonzero J2 nilpotent.
    B2=np.array([[0,1],[0,0]],dtype=np.int64)
    U=np.kron(S,np.eye(2,dtype=np.int64)+B2)%p
    E=np.eye(6,dtype=np.int64)
    for k in (930//z for z in (2,3,5,31)):
        assert not np.array_equal(matrix_power_mod(U,k,p),E)
    assert np.array_equal(matrix_power_mod(U,930,p),E)
    # The full graph dimensions below follow from the proved p-rank formula
    # rank_Fp(J-I-A)=binomial(p+2,3) for W(3,p), not a computed large matrix.
    n=(p+1)*(p*p+1)
    r=math.comb(p+2,3)
    assert (n,r)==(30784,5456)
    simple=n-2*r
    full={
        "root_11_repeated_Jordan":{"J3":r,"J2":simple,"J1":r},
        "root_10_simple_Jordan":{"J2":r,"J1":simple}}
    assert 3*r+2*simple+r + 2*r+simple==3*n
    return {"status":"PASS_EXACT_BLOCK_AND_SYMBOLIC_GRAPH","classical_RH_proved":False,
      "beta_discriminants":{"golden":d2,"supergolden":d3},
      "supergolden_mod31_factorization":"(x-10)*(x-11)^2",
      "scalar_orders":scalar_orders,
      "faithful_six_dimensional_tensor_order":930,
      "predicted_full_W3_31_dimension":3*n,
      "W3_31_vertices":n,"W3_31_B_rank_from_general_theorem":r,
      "predicted_full_Jordan_blocks":full,
      "proof":"Characteristic-31 supergolden module = eigenline 10 + J2(11). Tensor with the square-zero noncollinearity B; J2 tensor J2 has J3+J1 for p>2. Multiplicative scalar order lcm(15,30)=30 and nontrivial unipotent order31 yield order930.",
      "scope":"6D order directly verified; 92352D Jordan census algebraically derived, not numerically constructed. No global motive, optical implementation or RH proof."}

if __name__=="__main__":
    a=certificate()
    p=Path(__file__).resolve().parents[1]/"data"/"w33_20261022_supergolden_prime31.json"
    p.write_text(json.dumps(a,indent=2,sort_keys=True)+"\n")
    print({k:v for k,v in a.items() if k in ("status","faithful_six_dimensional_tensor_order","predicted_full_W3_31_dimension")})
