"""Integral topology of circle-bundle / H3-flux T-duality over S2xS2.

This is the Bouwknegt-Evslin-Mathai *topological* type-II circle
T-duality, NOT a completed M-theory/IIB Page-charge dictionary.

Let e=p*x+q*y, g=gcd(p,q)>0. Let H=k*z in H3(Y)=Z, where
Gysin pi_!(z)=(p/g)*x-(q/g)*y.
The dual Euler class is e'=k*(p/g*x-q/g*y), with gcd |k|.
The dual integral H' must satisfy pi'_!H'=e, and equals
sign(k)*g*z' in the dual generator convention.
This map is an involution on (p,q,k), including signed integers.

For k!=0, the dual pi1 torsion changes from Z_g to Z_|k|.
This is exactly how flux and topology exchange in topological
T-duality; do NOT claim the fundamental groups themselves are
preserved, or that torsion pi1 equals a Page-charge group.
"""
import math,json,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261117_integral_circle_Tduality_Gysin_involution.json"

def dual(p,q,k):
    if (p,q)==(0,0) or k==0:raise ValueError("Require nontrivial e and nonzero H generator coefficient")
    g=math.gcd(p,q)
    a,b=p//g,q//g
    newp,newq=k*a,-k*b
    g2=math.gcd(newp,newq)
    assert g2==abs(k)
    s=1 if k>0 else -1
    knew=s*g
    # The primitive dual pushforward is (p'/g2,-q'/g2);
    # H'=knew * dual_primitive yields (p,q).
    assert (knew*(newp//g2),-knew*(newq//g2))==(p,q)
    # e wedge e' = (p q' +q p') xy =0.
    assert p*newq+q*newp==0
    return (newp,newq,knew)

def cohomology_circle6(g):
    assert g>0
    tor=[] if g==1 else [g]
    # Y(p,q)xS1 via torsion-free Kunneth for S1, and
    # H*(Y)=Z,0,Z+Zg,Z,Zg,Z.
    return {
        "H0":{"free":1,"torsion":[]},
        "H1":{"free":1,"torsion":[]},
        "H2":{"free":1,"torsion":tor},
        "H3":{"free":2,"torsion":tor},
        "H4":{"free":1,"torsion":tor},
        "H5":{"free":1,"torsion":tor},
        "H6":{"free":1,"torsion":[]},
    }

def verify():
    samples=[]
    for p,q,k in ((6,6,5),(5,6,3),(12,18,-7),(-6,9,-4),(1,1,1),(0,6,4)):
        p2,q2,k2=dual(p,q,k)
        assert dual(p2,q2,k2)==(p,q,k)
        samples.append({"original":{"Euler":[p,q],"H3_coeff":k,
                "pi1_torsion_order":math.gcd(p,q)},
             "dual":{"Euler":[p2,q2],"H3_coeff":k2,
                     "pi1_torsion_order":math.gcd(p2,q2)},
             "involution_pass":True})
    count=0
    for p,q,k in itertools.product(range(-6,7),repeat=3):
        if (p,q)==(0,0) or k==0:continue
        assert dual(*dual(p,q,k))==(p,q,k)
        count+=1
    assert count==2016
    # Compare isolated M6 product with Y5xS1: cohomology and
    # degree-four flat differential characters differ for g>1.
    actual=cohomology_circle6(6)
    assert actual["H3"]=={"free":2,"torsion":[6]}
    assert actual["H4"]=={"free":1,"torsion":[6]}
    return {"status":"PASS_INTEGRAL_TOPOLOGICAL_CIRCLE_TDUALITY_FLUX_TORSION_INVOLUTION",
      "formula":{"original_Euler":"e=p*x+q*y",
        "primitive_Gysin_pushforward":"pi_!(z)=(p/g)*x-(q/g)*y, g=gcd(|p|,|q|)",
        "original_H3":"H=k*z, k nonzero integer",
        "dual_Euler":"e'=k*(p/g*x -q/g*y)",
        "dual_H3":"H'=sign(k)*g*z' with pi'_!(H')=e",
        "old_pi1_order":"g","dual_pi1_order":"|k|",
        "involution":"dual(dual(p,q,k))=(p,q,k) in the stated primitive generator convention"},
      "enumerated_nonzero_integer_cases":count,
      "examples":samples,
      "Y5_times_S1_cohomology_if_g6":actual,
      "M6_S2xS2xT2_cohomology":{
         "H1":{"free":2,"torsion":[]},"H2":{"free":3,"torsion":[]},
         "H3":{"free":4,"torsion":[]},"H4":{"free":3,"torsion":[]}},
      "flat_degree4_character_comparison":"Y5xS1: H^3(R/Z)=U(1)^2 x Z_g; M6=S2xS2xT2: U(1)^4 (no torsion), for g>1.",
      "not_same_as_M_IIB_duality":"This is standard topological type-II T-duality for a circle bundle WITH NS H3 flux. It does NOT construct an M-theory differential C-field, Page charges, or the actual E6/11D compactification duality.",
      "scientific_implication":"Topology can exchange with integer H flux, so comparing isolated pi1 or gcd values across candidate dual geometries without flux data is invalid.",
      "literature":"Bouwknegt-Evslin-Mathai, Topology and H-flux of T-dual manifolds, Phys Rev Lett 92 181601 (2004), doi:10.1103/PhysRevLett.92.181601"}
if __name__=="__main__":
    r=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(r["status"],r["enumerated_nonzero_integer_cases"])
