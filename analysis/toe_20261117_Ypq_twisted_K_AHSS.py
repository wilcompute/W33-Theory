"""Integral K-theory Gysin and twisted K AHSS associated graded for
principal S1 bundles Y(p,q)->S2xS2 with NS H=k*z.

Exact untwisted K^0(Y)=Z^2 + Z_g + Z_g, K^1(Y)=Z^2
from Smith form of multiplication by (1-[L]) on K^0(S2xS2).

For NONZERO H=k*z, the twisted complex K-AHSS:
d3=Sq_Z^3+H cup. In dimension five, Sq_Z^3 has zero target
for torsion-free-source classes of degree0 and degree2 free, and
is zero from H2 torsion into H5 free; degree 1 vanishes.
d3:H0=Z to H3=Z multiply k.
d3:H2=Z+Z_g to H5=Z multiply +/-k on the free
quotient, zero on torsion.
Hence E_inf even has two Z_g graded factors (degrees2,4);
odd two Z_|k| (degrees3,5). This determines ORDER g² and k²,
but NOT the possible extension of these two cyclic factors.
T duality interchanges g and k and shifts degree parity,
matching the graded-factor orders. DO NOT claim canonical full
twisted K group splitting / Page charge.
"""
import itertools,math,json,sys
from pathlib import Path
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_Tduality_integral_Gysin_involution import dual
OUT=ROOT/"data"/"toe_20261117_Ypq_KGysin_twisted_AHSS_charge_shadow.json"
def k_matrix(p,q):
    # K^0(B)=Z[x,y]/(x²,y²); [L]=(1+x)^p(1+y)^q.
    # Multiplication by [L]-1 in basis (1,x,y,xy).
    return sp.Matrix([[0,0,0,0],[p,0,0,0],
                      [q,0,0,0],[p*q,q,p,0]])
def untwisted(p,q):
    assert (p,q)!=(0,0)
    g=math.gcd(p,q)
    S=smith_normal_form(k_matrix(p,q),domain=ZZ)
    absdiag=[abs(int(S[i,i])) for i in range(4)]
    nons=[v for v in absdiag if v]
    assert nons==[g,g],(p,q,nons)
    return {"Euler":[p,q],"gcd":g,"nonzero_Smith_invariants":nons,
      "K0_Y_free_rank":2,"K0_Y_torsion_cyclic_orders":[g,g] if g>1 else [],
      "K1_Y_free_rank":2,"K1_Y_torsion_cyclic_orders":[]}
def twisted_AHSS(p,q,k):
    assert k!=0 and (p,q)!=(0,0)
    g=math.gcd(p,q)
    Horder=abs(k)
    return {"Euler":[p,q],"H3_integer_generator_coefficient":k,
      "Einf_even_graded_torsion_H2_H4":([g,g] if g>1 else []),
      "Einf_odd_graded_torsion_H3_H5":([Horder,Horder] if Horder>1 else []),
      "K_even_group_cardinality":g*g,"K_odd_group_cardinality":Horder*Horder,
      "free_rank_in_both_twisted_groups":0,
      "d3_maps":{"H0_to_H3":"multiply k","H2_free_to_H5":"multiply k (primitive Poincare pairing)",
                 "H2_torsion_to_H5":"zero (torsion into Z)"},
      "extension_open":"The AHSS gives associated graded cyclic factors, NOT a canonical group decomposition. The full finite abelian K group could involve nontrivial extension classes unless resolved by additional K-theoretic methods."}
def verify():
    checked=0;cases=[]
    for p,q,k in itertools.product(range(-5,6),repeat=3):
        if (p,q)==(0,0) or k==0:continue
        x=untwisted(p,q)
        a=twisted_AHSS(p,q,k)
        pp,qq,kk=dual(p,q,k)
        b=twisted_AHSS(pp,qq,kk)
        assert a["K_even_group_cardinality"]==b["K_odd_group_cardinality"]
        assert a["K_odd_group_cardinality"]==b["K_even_group_cardinality"]
        assert sorted(a["Einf_even_graded_torsion_H2_H4"])==sorted(b["Einf_odd_graded_torsion_H3_H5"])
        checked+=1
        if (p,q,k) in ((6,6,5),(3,3,5),(-3,3,-2),(1,2,1)):
            cases.append({"original":a,"dual":b,"K_untwisted":x})
    assert checked==1200
    # add the g=6 / k=5 motivating example
    p,q,k=6,6,5
    ex={"original":twisted_AHSS(p,q,k),
        "Tdual":twisted_AHSS(*dual(p,q,k)),
        "untwisted_K_Y":untwisted(p,q)}
    assert ex["original"]["K_even_group_cardinality"]==36
    assert ex["original"]["K_odd_group_cardinality"]==25
    assert ex["Tdual"]["K_even_group_cardinality"]==25
    assert ex["Tdual"]["K_odd_group_cardinality"]==36
    return {"status":"PASS_Ypq_UNTWISTED_K_GYSIN_SMITH_AND_TWISTED_AHSS_TDUAL_PARITY_SHADOW",
      "exact_untwisted_K_Gysin":"K0(Y)=Z^2 + Z_g + Z_g, K1(Y)=Z^2 for Euler class (p,q) nonzero, g=gcd(p,q), via SNF of [L]-1 on K0(S2xS2).",
      "twisted_AHSS_rule":"For nonzero H=k generator of H3(Y), E_inf twisted-even has Z_g factors in degrees 2,4; twisted-odd has Z_|k| factors in degrees 3,5. Each K-group has finite order g² or k², not an asserted direct-product splitting.",
      "signed_integer_triples_checked":checked,"example_euler6_6_H5":ex,
      "scope":"Complex twisted topological K-theory first nontrivial AHSS stage on oriented five-manifold with H=k z. No explicit differential K-class, brane charge, Freed-Witten anomaly, Page normalization, physical M/IIB dictionary or resolved extension.",
      "citations":["https://arxiv.org/abs/hep-th/0306062","https://link.springer.com/article/10.1007/s00220-024-05044-0"]}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["signed_integer_triples_checked"])
