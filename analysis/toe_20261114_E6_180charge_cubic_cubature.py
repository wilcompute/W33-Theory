#!/usr/bin/env python3
"""Exact 180-point integral E6 cubic cubature and Schlaefli fourth moments.

Each of 45 signed tritangent supports has four sign patterns N=+1.
Their uniform 180-point orbit is a spherical 2-design whose signed
third moment reconstructs the canonical cubic exactly:
sum_{z in C} <z,x>^3 = 24 N(x).
The even fourth moment recovers the 135-edge incidence graph.
All checks use Python integers, not numerics.
"""
from pathlib import Path
from itertools import permutations,product
from collections import Counter
import sys,json,random
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
OUT=ROOT/"data/toe_20261114_E6_180charge_cubic_cubature.json"

def main():
    _,cubic,_,_,_=R.load()
    assert len(cubic)==45 and all(len(t)==3 and s in (-1,1) for t,s in cubic.items())
    incid=Counter(i for tri in cubic for i in tri)
    assert len(incid)==27 and set(incid.values())=={5}
    edge_counts=Counter(tuple(sorted((i,j)))
        for tri in cubic for i,j in ((tri[0],tri[1]),(tri[0],tri[2]),(tri[1],tri[2])))
    assert len(edge_counts)==135 and set(edge_counts.values())=={1}
    deg=Counter(i for u,v in edge_counts for i in (u,v))
    assert len(deg)==27 and set(deg.values())=={10}
    charges=[]
    for (i,j,k),s in cubic.items():
        for signs in product((-1,1),repeat=3):
            if signs[0]*signs[1]*signs[2]!=s:continue
            z=[0]*27
            z[i],z[j],z[k]=signs
            assert sum(v*v for v in z)==3
            assert sum(t*z[a]*z[b]*z[c] for (a,b,c),t in cubic.items())==1
            charges.append(tuple(z))
    assert len(charges)==180 and len(set(charges))==180
    first=Counter();second=Counter();third=Counter();fourth=Counter()
    for z in charges:
        supp=[(i,v) for i,v in enumerate(z) if v]
        assert len(supp)==3
        for i,zi in supp:
            first[i]+=zi
            for j,zj in supp:
                second[i,j]+=zi*zj
                for k,zk in supp:
                    third[i,j,k]+=zi*zj*zk
                    for l,zl in supp:
                        fourth[i,j,k,l]+=zi*zj*zk*zl
    assert all(first[i]==0 for i in range(27))
    assert {k:v for k,v in second.items() if v}=={(i,i):20 for i in range(27)}
    expected_third={}
    for tri,s in cubic.items():
        for p in permutations(tri):
            expected_third[p]=4*s
    assert {k:v for k,v in third.items() if v}==expected_third
    expected_fourth={(i,i,i,i):20 for i in range(27)}
    for i,j in edge_counts:
        for p in set(permutations((i,i,j,j))):
            expected_fourth[p]=4
    assert {k:v for k,v in fourth.items() if v}==expected_fourth
    rng=random.Random(20261114)
    trials=[]
    for t in range(40):
        x=[rng.randint(-3,3) for _ in range(27)]
        cubic_x=sum(s*x[i]*x[j]*x[k] for (i,j,k),s in cubic.items())
        quad_x=sum(v*v for v in x)
        pair_x=sum(x[i]*x[i]*x[j]*x[j] for i,j in edge_counts)
        moments=[sum((sum(z[i]*x[i] for i in range(27)))**p for z in charges) for p in range(1,5)]
        assert moments[0]==0
        assert moments[1]==20*quad_x
        assert moments[2]==24*cubic_x
        assert moments[3]==20*sum(a**4 for a in x)+24*pair_x
        if t<3:trials.append(dict(cubic=cubic_x,sums=moments))
    result=dict(
        status="PASS_EXACT_180CHARGE_SIGNED_E6_CUBIC_CUBATURE",
        source="Canonical signed E6 cubic with 45 triple monomials in native repo coordinate order",
        dimension=27,tritangents=45,coordinate_degree=5,
        Schlaefli_two_section_edges=135,Schlaefli_vertex_degree=10,
        charges_positive_unit_cubic=180,positive_sign_patterns_per_line=4,
        all_charges_integer_and_norm_squared_3=True,
        first_moment="sum_{z in C} z_i = 0",
        second_moment="sum_{z in C} z_i z_j = 20 delta_ij; mean covariance I27/9",
        third_moment="sum_{z in C} z_i z_j z_k = 4 s_ijk for any ordered distinct signed tritangent; 0 otherwise",
        cubic_cubature="sum_{z in C} (z dot x)^3 = 24 N(x); N(x)=sum_{45 lines} s_ijk x_i x_j x_k",
        fourth_moment="sum_{z in C} z_i^4=20; sum z_i^2 z_j^2=4 iff i,j collinear in 135-edge graph, else 0; all other index patterns vanish",
        quartic_cubature="sum_{z in C} (z dot x)^4 = 20 sum_i x_i^4 + 24 sum_{135 edges {i,j}} x_i^2 x_j^2",
        spherical_design_strength=2,
        is_spherical_3design=False,
        exact_random_integer_cubature_trials=40,
        sample_checks=trials,
        novelty_scope="A finite exact signed cubic/moment identity instantiated in the repo native coordinate basis, not an assertion of new exceptional algebra or physical spacetime. The 180 set was previously counted in Pass12668.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True),flush=True)
    return result

if __name__=="__main__":
    main()
