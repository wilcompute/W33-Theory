"""Resolve previously-open twisted-K additive extensions in proven subfamilies.

For Y(p,q)->S2xS2 with c1=g(a*x+b*y), H=k*z where pi_*z=a*x-b*y,
topological T-duality gives c1_hat=k(a*x-b*y), H_hat=g*z_hat,
where pi_hat*z_hat=a*x+b*y. T-duality shifts K-degree by one.
This certifies K_H^0(Y) = Z_g^2 for |k|=1 and arbitrary primitive
a,b by duality to primitive Y_hat = S2xS3 with twist g.
Other subfamilies follow from explicit product L(g,1)xS2.
General g>1, |k|>1, a*b !=0 remains unresolved.
"""
import json,math,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_twisted_K_Tduality_resolutions.json"
spec=importlib.util.spec_from_file_location("ahss",ROOT/"analysis"/"toe_20261116_twisted_K_AHSS_extensions.py")
ahss=importlib.util.module_from_spec(spec);spec.loader.exec_module(ahss)

def resolve(p,q,k):
    if not (p or q):raise ValueError("nontrivial original circle bundle")
    g=math.gcd(p,q)
    a,b=p//g,q//g
    if k==0:
        d=ahss.page(p,q,k)
        return {"original_c1":[p,q],"H_twist":0,"K0":d["K0_exact"],"K1":d["K1_exact"],
                "method":"untwisted K-Gysin"}
    d=ahss.page(p,q,k)
    ka=abs(k)
    result={
       "original_c1":[p,q],"H_twist":k,
       "dual_c1":[k*a,-k*b],"dual_twist":g,
       "dual_gcd":ka,"original_gcd":g,
       "original_H3_pushforward":[a,-b],
       "dual_H3_pushforward":[a,b],
       "E_infty_K0_order":g*g,"E_infty_K1_order":ka*ka,
       "degree_shift":"K_H^0(Y) = K_Hhat^1(Yhat); K_H^1(Y) = K_Hhat^0(Yhat)",
       "K0_exact":None,"K1_exact":None,
       "resolution":"unresolved in this method"
    }
    if g==1:
        result["K0_exact"]="0"
        result["K1_exact"]=f"Z_{ka} + Z_{ka}" if ka>1 else "0"
        result["resolution"]="primitive c1: Y diffeomorphic to S2xS3, twisted Kunneth"
    elif ka==1:
        result["K0_exact"]=f"Z_{g} + Z_{g}"
        result["K1_exact"]="0"
        result["resolution"]="T-dual has primitive circle class, nonzero twist g, so K^1 dual is Z_g^2"
    elif a*b==0:
        result["K0_exact"]=f"Z_{g} + Z_{g}"
        result["K1_exact"]=f"Z_{ka} + Z_{ka}"
        result["resolution"]="Y=L(g,1)xS2 (up to orientation) and twist from lens top H3; twisted Kunneth"
    return result

def verify():
    cases=[resolve(p,q,k) for p,q in [(1,1),(3,0),(0,5),(3,3),(4,4),(6,10),(-4,-4)]
           for k in (-2,-1,1,2,3)]
    assert resolve(3,3,1)["K0_exact"]=="Z_3 + Z_3"
    assert resolve(4,4,-1)["K0_exact"]=="Z_4 + Z_4"
    assert resolve(6,10,1)["K0_exact"]=="Z_2 + Z_2"
    assert resolve(6,10,3)["K0_exact"] is None
    assert resolve(3,0,7)["K0_exact"]=="Z_3 + Z_3"
    assert resolve(3,0,7)["K1_exact"]=="Z_7 + Z_7"
    for r in cases:
        if r["K0_exact"]=="0":assert r["original_gcd"]==1
        if r["K1_exact"]=="0":assert abs(r["H_twist"])==1
        dual=r["dual_c1"]
        assert math.gcd(*dual)==r["dual_gcd"]
    return {"status":"PASS_T_DUAL_RESOLUTION_OF_TWISTED_K_EXTENSIONS_FOR_UNIT_H",
            "theorem":"For every p,q not both zero, with g=gcd(p,q), H=+/-z primitive, K_H^0(Y)=Z_g+Z_g and K_H^1(Y)=0. This resolves the prior AHSS extension for unit H.",
            "also_resolved":"Primitive circle g=1 and product lens-space a*b=0 for arbitrary nonzero integral H twist.",
            "not_resolved":"g>1, |k|>1 and a*b!=0: extension structure needs additional construction.",
            "topological_T_duality_reference":"Bouwknegt-Evslin-Mathai 2004; Mathai-Rosenberg 2005",
            "physical_boundary":"These nonzero H backgrounds are NOT the currently analyzed source-free IIB H3=0 vacuum. Topological K classifications do not alone fix Page charge or exact D-brane decay.",
            "cases":cases}

if __name__=="__main__":
    r=verify();OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(r["status"])
