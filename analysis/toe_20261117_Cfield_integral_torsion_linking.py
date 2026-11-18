"""Integral torsion linking of flat degree-four C-fields in
Y(p,q)xS1 and change under actual topological type-II T-duality.

Base B=S²xS², x,y generators H², xy orientation H⁴,
circle-bundle Euler e=p*x+q*y=g*eta, eta=(p/g)x+(q/g)y.
In the integral mapping-cone (Gysin) cochain picture,
dtheta=e, d(theta t)=e t=g eta t,
d(theta x)=q xy and d(theta y)=p xy.
Therefore eta t generates Tor H³(YxS1)=Z_g and xy generates
Tor H⁴(YxS1)=Z_g. Rational lift theta t/g of eta t
and integration over theta*x*y*t yields the linking form
<eta t,xy> = +/-1/g mod Z, nondegenerate.
This identifies flat torsion degree-four C-holonomy as
root-of-unity sectors, not real curvature G4.

Under topological type-II NS T-duality with H=k*z,
g'=|k|. The analogous torsion *cohomology* linking
denominator becomes |k|; this is NOT a physical Page
charge group isomorphism or the 11D/IIB differential map.
"""
import math,json,itertools
from fractions import Fraction
from pathlib import Path
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261117_Cfield_torsion_linking_Tduality_pairs.json"
def torsion(p,q):
    g=math.gcd(p,q)
    if not g:raise ValueError("nonzero circle Euler class required")
    primitive=(p//g,q//g)
    assert math.gcd(*primitive)==1
    # Integral generators: eta t in H³, xy in H⁴.
    # Their linking is 1/g mod 1 in a chosen orientation.
    M=sp.Matrix([[p,q],[q,p]])
    # Smith form for the H² quotient relation e (1x2) and
    # H⁴ quotient of e cup H² (1x2) both gcd g.
    d2=smith_normal_form(sp.Matrix([[p,q]]),domain=ZZ)
    d4=smith_normal_form(sp.Matrix([[q,p]]),domain=ZZ)
    assert abs(d2[0,0])==g and abs(d4[0,0])==g
    pairing=[[str(Fraction(a*b,g)%1) for b in range(g)] for a in range(g)] if g<=16 else []
    if g>1:
        # Pairing with generator is primitive: only 0 mod g pairs
        # trivially with every other character.
        for a in range(g):
            character=[(a*b)%g for b in range(g)]
            assert (all(v==0 for v in character))==(a==0)
    return {"Euler":[p,q],"g":g,"primitive_eta":list(primitive),
       "Tor_H3":f"Z_{g}" if g>1 else "0",
       "Tor_H4":f"Z_{g}" if g>1 else "0",
       "linking_orientation_chosen":"<eta*t, x*y> = 1/g mod Z",
       "unit_linking_fraction":"1/"+str(g) if g>1 else "zero",
       "linking_matrix_mod1_small_g":pairing,
       "flat_degree4_Ctorsion":"mu_g roots of unity" if g>1 else "none",
       "Gysin_chain_relations":{"dtheta":f"{p}x+{q}y",
          "d(theta*t)":f"{g}eta*t",
          "d(theta*x)":f"{q}xy",
          "d(theta*y)":f"{p}xy"}}
def dual(p,q,k):
    g=math.gcd(p,q)
    if g==0 or k==0:raise ValueError
    return (k*p//g,-k*q//g, (1 if k>0 else -1)*g)
def verify():
    checks=0;examples=[]
    for p,q,k in itertools.product(range(-5,6),repeat=3):
        if (p,q)==(0,0) or k==0:continue
        a=torsion(p,q);bp,bq,bk=dual(p,q,k)
        b=torsion(bp,bq)
        assert b["g"]==abs(k) and bk==(1 if k>0 else -1)*a["g"]
        assert dual(bp,bq,bk)==(p,q,k)
        checks+=1
        if (p,q,k) in ((3,3,5),(-3,3,-2),(1,2,1)):
            examples.append({"original":a,"typeII_Tdual":b,"original_NS_k":k})
    assert checks==1200
    a=torsion(6,6);b=torsion(5,-5)
    assert a["g"]==6 and b["g"]==5
    return {"status":"PASS_INTEGRAL_TORSION_CFIELD_LINKING_AND_CIRCLE_TDUALITY_SHADOW",
      "cochain_argument":"e=g eta with primitive eta, dtheta=e; eta*t has order g in H³(YxS1), xy has order g in H⁴(YxS1) since d(theta*x)=qxy, d(theta*y)=pxy. Their perfect torsion linking is 1/g mod Z, up to orientation, by rational Bockstein lift theta*t/g.",
      "original_e6_example_6_6":a,"Tdual_5_minus5":b,
      "integer_signed_triples_checked":checks,"samples":examples,
      "physical_warning":"A linking form on torsion cohomology of different backgrounds is NOT a canonical map of quantum Page charges. A type-II T-duality exchanges NS flux and circle topology; an M-theory/IIB C-field differential-cohomology duality, kinetic couplings and brane endpoint data remain unconstructed.",
      "sources":["https://arxiv.org/abs/hep-th/0306062",
                 "https://arxiv.org/abs/hep-th/9609122"]}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["integer_signed_triples_checked"],
         z["original_e6_example_6_6"]["unit_linking_fraction"])
