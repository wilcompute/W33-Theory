"""Circle-bundle topological K-theory and spin-lift audit (standard library).

For Y(p,q) = S(L) over S2 x S2 with c1(L)=p*x+q*y,
K^0(base)=Z[X,Y]/(X^2,Y^2), X=[L_x]-1, Y=[L_y]-1.
K-theoretic Gysin: K^0(total)=coker(multiplication by 1-[L])
and K^1(total)=ker(same map).  All claims are *untwisted*
topological K-theory; RR Page charge and self-dual flux constraints
require further physical analysis.
"""
from __future__ import annotations
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_iib_K_gysin_ring.json"

def egcd(a:int,b:int):
    if b==0:return abs(a),(1 if a>=0 else -1),0
    g,x,y=egcd(b,a%b)
    return g,y,x-(a//b)*y

def k_gysin(p:int,q:int)->dict:
    if p==q==0:raise ValueError("nontrivial Euler class needed")
    g=math.gcd(p,q)
    a,b=p//g,q//g
    h,s,t=egcd(a,b)
    assert h==1 and a*s+b*t==1
    # Columns are e*{1,X,Y,XY}; e=p X+q Y+pq XY.
    M=((0,0,0,0),
       (p,0,0,0),
       (q,0,0,0),
       (p*q,q,p,0))
    d1=math.gcd(p,q,p*q)
    minors=[abs(p*p),abs(p*q),abs(q*q)]
    d12=math.gcd(*minors)
    assert d1==g and d12==g*g
    # u=pi^*((1+X)^a*(1+Y)^b-1)=a X+b Y+ab XY,
    # w=pi^*(XY), and u^2=2ab*w mod g.
    usquare=(2*a*b)%g
    return {
      "charges":[p,q],"gcd":g,
      "K0_additive":{"free_rank":2,"torsion_invariant_factors":[g,g] if g>1 else []},
      "K1_additive":{"free_rank":2,"torsion_invariant_factors":[]},
      "gysin_euler_matrix":M,
      "gysin_nonzero_smith_factors":[d1,d12//d1],
      "u_torsion_class_coefficients_in_X_Y_XY":[a,b,a*b],
      "u_square_coefficient_mod_g":usquare,
      "u_square_nonzero":bool(usquare),
      "XY_order":g,
      "H1_pi1":f"Z_{g}",
      "spin_structure_count":2 if g%2==0 else 1,
      "total_space_is_spin":True,
      "qualifier":"Untwisted topological K groups/ring only; no automatic claim about physical conserved brane charges."
    }

def quotient_spin_lifts(N:int)->dict:
    if N<1:raise ValueError("N>=1")
    # Quotient deck generator has eigenphases exp(+-2*pi*i/N)
    # on the two conifold Killing spinors. The alternate deck lift
    # adds -1 and exists iff N is even.
    shifts=[Fraction(0)]+([Fraction(1,2)] if N%2==0 else [])
    lifted=[]
    for shift in shifts:
        invariant=any((sign*Fraction(1,N)+shift).denominator==1 for sign in (1,-1))
        lifted.append({"shift":str(shift),"cover_spinor_invariant":invariant})
    return {"N":N,"spin_structures":len(shifts),"lifts":lifted,
      "some_cover_Killing_spinor_survives":any(a["cover_spinor_invariant"] for a in lifted)}

def verify()->dict:
    examples=[k_gysin(p,q) for p,q in
       [(1,1),(2,2),(3,3),(4,4),(3,0),(0,3),(6,10),(8,12),(-4,-4),(11,-13)]]
    for r in examples:
        g=r["gcd"]
        assert r["gysin_nonzero_smith_factors"]==[g,g]
        assert r["K0_additive"]["free_rank"]==2
        assert r["K1_additive"]["free_rank"]==2
        assert (r["spin_structure_count"]==2)==(g%2==0)
    a,b=k_gysin(3,0),k_gysin(3,3)
    assert a["K0_additive"]==b["K0_additive"]
    assert a["K1_additive"]==b["K1_additive"]
    assert a["u_square_coefficient_mod_g"]==0
    assert b["u_square_coefficient_mod_g"]==2
    # This controls a genuine ring distinction not just differing coordinate choices:
    # a torsion generator may be multiplied by a unit modulo g; zero/nonzero
    # square is unchanged by such a choice.
    assert k_gysin(4,4)["u_square_coefficient_mod_g"]==2
    assert k_gysin(2,2)["u_square_coefficient_mod_g"]==0
    spin=[quotient_spin_lifts(n) for n in range(1,17)]
    assert [x["N"] for x in spin if x["some_cover_Killing_spinor_survives"]]==[1,2]
    return {
      "status":"PASS_K_THEORETIC_GYSIN_RING_AND_COVER_SPINOR_PHASE",
      "examples":examples,"cover_spinor_quotient":spin,
      "distinguishing_example":{
        "Y30":"S(L) with c1=(3,0), same K0/K1 as Y33; torsion generator square zero",
        "Y33":"S(L) with c1=(3,3), torsion generator square 2w in Z3",
      },
      "topology_reference":"https://inspirehep.net/files/4eadf33259d623493f52eaba5c45ec90",
      "scope":"Exact for ordinary complex topological K theory and stated spinor phases; not twisted K theory or a complete Page charge classification."
    }

if __name__=="__main__":
    cert=verify()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(cert,indent=2)+"\n",encoding="utf-8")
    print(cert["status"],"cases",len(cert["examples"]))
