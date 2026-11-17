"""Full graded integer wedge-by-G4 incidence complex for M6=S2xS2xT2.

H^0 = Z; H^1 = Z^2; H^2 = Z^3; H^3=Z^4;
H^4 = Z^3; H^5 = Z^2; H^6=Z.
For G4=N_xy xy + N_xt xt + N_yt yt,
we compute the exact wedge maps H^0->H^4, H^1->H^5,
and H^2->H^6 and their Smith normal forms.

This is a purely topological integral cochain operation.
It is NOT by itself a twisted K/AHSS differential, Page charge
group or established physical BF gauge symmetry.
"""
from pathlib import Path
from math import gcd
from functools import reduce
from itertools import product
import json
import sympy as S
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_M5_graded_G4_wedge_complex.json"

# Basis of external 2-spheres, and 1-forms of T2.
# Encode cochains as oriented subsets of four formal generators:
# x (degree2), y (degree2), alpha,beta (degree1), with alpha beta=t.
# We never use x or y more than once; alpha,beta Grassmann.
BASIS={0:[()],1:[("a",),("b",)],2:[("x",),("y",),("a","b")],
       3:[("x","a"),("x","b"),("y","a"),("y","b")],
       4:[("x","y"),("x","a","b"),("y","a","b")],
       5:[("x","y","a"),("x","y","b")],
       6:[("x","y","a","b")]}
ORDER={"x":0,"y":1,"a":2,"b":3}
DEGREE={"x":2,"y":2,"a":1,"b":1}

def product_form(u,v):
    if set(u).intersection(v):return None
    inversions=sum(DEGREE[a]*DEGREE[b] for a in u for b in v if ORDER[a]>ORDER[b])
    return ((-1)**inversions,tuple(sorted(u+v,key=ORDER.get)))

def matrix(degree,Nxy,Nxt,Nyt):
    flux=[(Nxy,("x","y")),(Nxt,("x","a","b")),(Nyt,("y","a","b"))]
    src=BASIS[degree]
    dst=BASIS[degree+4]
    A=S.zeros(len(dst),len(src))
    for j,v in enumerate(src):
        for q,f in flux:
            p=product_form(v,f)
            if p is not None:
                sg,w=p
                A[dst.index(w),j]+=q*sg
    return A

def invariant(A):
    snf=smith_normal_form(A,domain=ZZ)
    return [abs(int(snf[i,i])) for i in range(min(A.rows,A.cols)) if snf[i,i]!=0]

def case(Nxy,Nxt,Nyt):
    d0=matrix(0,Nxy,Nxt,Nyt)
    d1=matrix(1,Nxy,Nxt,Nyt)
    d2=matrix(2,Nxy,Nxt,Nyt)
    assert d0==S.Matrix([[Nxy],[Nxt],[Nyt]])
    assert d1==S.diag(Nxy,Nxy)
    assert d2==S.Matrix([[Nyt,Nxt,Nxy]])
    g=reduce(gcd,map(abs,(Nxy,Nxt,Nyt)))
    g0=invariant(d0);g1=invariant(d1);g2=invariant(d2)
    assert g0==([g] if g else [])
    assert g2==([g] if g else [])
    assert g1==([abs(Nxy),abs(Nxy)] if Nxy else [])
    return {"flux_periods":[Nxy,Nxt,Nyt],
        "H0_to_H4":[list(map(int,d0.col(j))) for j in range(d0.cols)],
        "H1_to_H5":[list(map(int,d1.col(j))) for j in range(d1.cols)],
        "H2_to_H6":[list(map(int,d2.col(j))) for j in range(d2.cols)],
        "smith_invariants":{"H0_H4":g0,"H1_H5":g1,"H2_H6":g2},
        "torsion_coker_H0_H4":f"Z_{g}" if g>1 else "none",
        "torsion_coker_H1_H5":f"Z_{abs(Nxy)} x Z_{abs(Nxy)}" if abs(Nxy)>1 else "none",
        "torsion_coker_H2_H6":f"Z_{g}" if g>1 else "none"}

def verify():
    combos=[(6,6,6),(5,6,6),(6,6,5),(1,1,1),(0,6,6),(0,0,0),(100,101,100)]
    rows=[case(*args) for args in combos]
    assert rows[0]["smith_invariants"]=={"H0_H4":[6],"H1_H5":[6,6],"H2_H6":[6]}
    assert rows[1]["smith_invariants"]=={"H0_H4":[1],"H1_H5":[5,5],"H2_H6":[1]}
    assert rows[-1]["smith_invariants"]=={"H0_H4":[1],"H1_H5":[100,100],"H2_H6":[1]}
    # H3 free 4 generators unaltered by wedge G since H7=0
    # Note 4-differential squares to zero by dimension.
    for p,q,r in product(range(-2,3),repeat=3):
        z=case(p,q,r)
        g=reduce(gcd,(abs(p),abs(q),abs(r)))
        assert z["smith_invariants"]["H0_H4"]==([g] if g else [])
    return {"status":"PASS_M5_FULL_GRADED_G4_WEDGE_SMITH_CERTIFICATE",
        "cohomology_betti_numbers":{str(k):len(v) for k,v in BASIS.items()},
        "maps":["H0->H4","H1->H5","H2->H6"],
        "theorem":"For G4=Nxy xy+Nxt xt+Nyt yt, Smith H0->H4 and H2->H6 are gcd(Nxy,Nxt,Nyt), while H1->H5 has two invariants |Nxy| each, independent of Nxt,Nyt.",
        "new_crosssector_falsifier":"When (Nxy,Nxt,Nyt)=(N,N+1,N), the H0/H2 flux index is 1 but the H1 flux index is (N,N). The IIB Y(N+1,N) circle is simply connected; these graded wedge data cannot all be the same conserved charge group.",
        "physically_nonproven":"The graded integer wedge maps are not by themselves an M-theory differential cocycle action, quantum Page charge spectrum or source-free IIB winding classification.",
        "examples":rows}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["examples"][-1]["smith_invariants"])
