"""STU cubic as diagonal restriction of 27-dimensional exceptional Jordan norm.

For Herm_3(O), real dimension 3+3*8=27.
Its determinant is abc-a|x|^2-b|y|^2-c|z|^2+2Re((xy)z).
On the 3-dimensional diagonal subspace it is abc, the same
intersection cubic of H^2(S2 x S2 x T2;Z).
Our geometry has b2=3, so the harmonic C3-gauge-vector sector
contains precisely 3 U(1) candidates, NOT the 27 required for the
full exceptional magical supergravity cubic.
The missing 24 offdiagonal real parameters (3 octonions) would
need additional physical fields or a different compactification.
This is a structural dimension obstruction, not a proof no
other nonharmonic or nongeometric degrees can generate an E6 theory.
"""
import json,itertools
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_STU_J3Octonionic_24missing_modes.json"

def diagonal_and_real_check():
    a,b,c,x,y,z=sp.symbols("a b c x y z",real=True)
    matrix=sp.Matrix([[a,z,y],[z,b,x],[y,x,c]])
    det=sp.expand(matrix.det())
    jordan=sp.expand(a*b*c-a*x*x-b*y*y-c*z*z+2*x*y*z)
    assert sp.simplify(det-jordan)==0
    assert jordan.subs({x:0,y:0,z:0})==a*b*c
    # M6 basis x_sphere, y_sphere, t_torus:
    # 1/6 integral (a x+b y+c t)^3 = abc.
    cases=[]
    for vals in [(1,1,1,0,0,0),(2,3,5,0,0,0),(1,2,3,1,2,3),(-2,3,1,2,-1,1)]:
        M=matrix.subs(dict(zip((a,b,c,x,y,z),vals)))
        cases.append({"parameters":list(vals),"matrix_determinant":int(M.det()),
                      "exceptional_Jordan_real_slice":int(jordan.subs(dict(zip((a,b,c,x,y,z),vals))))})
        assert cases[-1]["matrix_determinant"]==cases[-1]["exceptional_Jordan_real_slice"]
    return {"real_symmetric_3x3_slice_det":str(jordan),
      "octonionic_J3_norm_formula":"abc - a|x|^2 - b|y|^2 - c|z|^2 +2 Re((xy)z)",
      "diagonal_restriction":"abc","real_dim_total":27,
      "real_dim_diagonal":3,"real_dim_missing_offdiagonal":24,
      "three_octonions_real_dimensions":[8,8,8],
      "small_exact_tests":cases}

def geometry_gap():
    b2=3
    # M6=S2xS2xT2. Betti via Kunneth:
    b1=2;b2=3;b3=4;b4=3;b5=2
    harmonic_C3_1form_count=b2
    return {
       "M6":"S2 x S2 x T2",
       "Betti_numbers":{"b1":b1,"b2":b2,"b3":b3,"b4":b4,"b5":b5},
       "harmonic_C3_5D_1form_fields":harmonic_C3_1form_count,
       "octonionic_magic_supergravity_cubic_variables":27,
       "missing_variables_for_full_J3O_harmonic_C3_sector":27-b2,
       "condition":"Need 24 extra independent vector/charge degrees to upgrade this particular 3-variable STU cubic to the 27-variable E6(-26) Jordan norm. A matching polynomial abc alone is not such an upgrade.",
       "nonclaim":"Other metric KK vectors, dual p-form fields, massive states or nongeometric sectors might contribute, but no complete 27-vector E6(-26) supergravity reduction is derived."}

def verify():
    r=diagonal_and_real_check();g=geometry_gap()
    assert r["real_dim_missing_offdiagonal"]==g["missing_variables_for_full_J3O_harmonic_C3_sector"]==24
    assert r["real_dim_total"]==27
    return {"status":"PASS_STU_TO_J3O_CUBIC_BRIDGE_WITH_24_MODE_DEFICIT",
      "exact_norm":r,"topological_vector_obstruction":g,
      "physics_contrast":"E6(-26) as U-duality of octonionic magical 5D supergravity is NOT automatically the same gauged complex/compact E6 GUT used in the 27-Higgs F-term sector.",
      "literature":"Gunaydin et al., magical supergravity from degree-3 Euclidean Jordan algebras, and subsequent octonionic magical supergravity reviews."}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["topological_vector_obstruction"]["missing_variables_for_full_J3O_harmonic_C3_sector"])
