"""Flux-incidence and triple intersection of S2 x S2 x T2, with 5D CS checks.

Unlike the IIB Y(p,q) topology, M6=S2xS2xT2 has H2=Z^3
and triple wedge intersection C_xyz=1, all repeated-index triples zero.
The 11D term C3 wedge G4 wedge G4 therefore has a candidate five-
dimensional A_x F_y F_z topological cubic and linear pairing with
magnetic flux. Exact integral lattice statements are established here.
The BF level requires full differential C-field treatment and is not
asserted to equal the unrefined wedge coefficient.
"""
from itertools import permutations, product
import json, math
from functools import reduce
from pathlib import Path
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_M5_STU_triple_intersection_flux_pairing.json"
LABELS=("sphere1","sphere2","torus")
H4=("sphere1_sphere2","sphere1_torus","sphere2_torus")

def c(i,j,k):
    if {i,j,k}=={0,1,2}:return 1
    return 0

def wedge_second_to_four(i,j):
    if i==j:return None
    return tuple(sorted((i,j)))

def flux_pairing(Nxy,Nxt,Nyt):
    """(Qx,Qy,Qt) = integral (x,y,t) wedge G4."""
    q=(Nyt,Nxt,Nxy)
    g=reduce(math.gcd,(abs(v) for v in q))
    mat=Matrix([list(q)])
    snf=smith_normal_form(mat,domain=ZZ)
    assert snf[0,0]==g or abs(int(snf[0,0]))==g
    # A formal rank-one compact BF interface has torsion Z_g.
    return {"G4_integral_periods":{"sphere1_sphere2":Nxy,
        "sphere1_torus":Nxt,"sphere2_torus":Nyt},
       "pairing_Q_A_to_G4":list(q),
       "Smith_invariant":g,
       "formal_rank_one_BF_finite_group":f"Z_{g}" if g>1 else "trivial",
       "physical_caveat":"The 5D topological BF level is not certified without a global differential C-field, precise 11D Chern-Simons normalization, flux-sourced Stückelberg constraints and dynamical spectrum."}

def intersection_certificate():
    tensor=[{"indices":list(t),"coefficient":c(*t)}
            for t in product(range(3),repeat=3)]
    assert sum(v["coefficient"] for v in tensor)==6
    assert all(c(*t)==1 for t in permutations(range(3)))
    for a,b,k in product(range(-2,3),repeat=3):
        # (a x + b y + k t)^3 = 6abk[x y t]
        coeff=sum(c(i,j,l)*[a,b,k][i]*[a,b,k][j]*[a,b,k][l]
                  for i,j,l in product(range(3),repeat=3))
        assert coeff==6*a*b*k
    return {"integral_H2_rank":3,"integral_H4_rank":3,"integral_H3_rank":4,
            "nonzero_triple_intersections":[list(t) for t in permutations(range(3))],
            "triple_intersection_value":1,
            "volume_cubic":"(1/6) integral J^3 = a*b*c",
            "11D_to_5D_CS_topological_tensor":"C_xyz=1, all permutations; repeat indices zero",
            "E6_diagonal_cubic_bridge":"Restricting E6 det A to diagonal A=diag(a,b,c) gives abc, the same abstract cubic polynomial. This alone is NOT a 5D E6 gauge sector or a TOE derivation.",
            "spin_and_G4_shift":"p1(S2xS2xT2)=0 by stable product tangent splitting and dim 2 of each factor, so the standard p1/4 shift has zero topological class on M6."}

def verify():
    top=intersection_certificate()
    rows=[flux_pairing(*v) for v in ((6,6,6),(6,6,5),(5,6,6),(1,1,1),(3,5,7),(0,0,0))]
    assert rows[0]["Smith_invariant"]==6
    assert rows[1]["Smith_invariant"]==1
    assert rows[-1]["Smith_invariant"]==0
    # IIB fiber pi1 depends gcd of MIXED fluxes p,q, not N0.
    # Example Nxy=5,Nxt=Nyt=6: IIB fiber has Z6; here Q has gcd1.
    compare={"IIB_mixed_Chern_periods":[6,6],"IIB_pi1":"Z_6",
      "M_fourform_periods":[5,6,6],"M_formal_BF_gcd":1,
      "conclusion":"The two discrete groups are not automatically identical. Identifying them requires a genuine T-duality/Page/winding operator dictionary."}
    return {"status":"PASS_M_TORUS_STU_INTERSECTION_AND_FLUX_SMITH_COMPARISON",
       "integral_topology":top,"flux_pairings":rows,
       "distinct_discrete_group_falsifier":compare,
       "scope":"Intersection and Smith forms exact; actual dynamical 5D CS/BF action and physical discrete symmetry require explicit global differential-field normalization."}
if __name__=="__main__":
    result=verify()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(result["status"],result["distinct_discrete_group_falsifier"])
