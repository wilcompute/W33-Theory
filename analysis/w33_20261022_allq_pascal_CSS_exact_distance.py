#!/usr/bin/env python3
"""Exact all-prime-power CSS distance theorem from symplectic noncollinearity.

Let q=p^t, V=PG(3,q), B_xy=1 if <x,y> != 0 else 0.
Over Fp, B^2=0, rank(B)=binom(p+2,3)^t.
The dual code of row(B) has minimum distance q+1:
  - every projective line provides weight q+1,
  - a hyperplane counting argument excludes <=q support.
The line vectors are NOT in row(B), yielding
  [[(q+1)(q²+1), (q+1)(q²+1)-2*binom(p+2,3)^t, q+1]]_p.
This is a projective incidence/CSS consequence of known rank theorems;
do not claim first discovery or a physical fault-tolerance threshold.
"""
from __future__ import annotations
import json, math, itertools
from pathlib import Path
import numpy as np
from analysis.w33_20261022_six_algebra_optics_frontiers import field,rank_modp

def projective_points(q):
    return [(0,)*i+(1,)+tail for i in range(4)
            for tail in itertools.product(range(q),repeat=3-i)]

def case(p,t,poly):
    q,add,mul,inv,neg=field(p,t,poly)
    pts=projective_points(q)
    n=len(pts)
    assert n==(q+1)*(q*q+1)
    P=np.asarray(pts,dtype=np.int16)
    sym=np.zeros((n,n),dtype=np.int16)
    for i,j,sign in ((0,2,1),(1,3,1),(2,0,-1),(3,1,-1)):
        term=mul[P[:,i,None],P[None,:,j]]
        if sign==-1:term=neg[term]
        sym=add[sym,term]
    B=(sym!=0).astype(np.int64)
    d=math.comb(p+2,3)**t
    rank=rank_modp(B,p)
    assert rank==d
    assert not np.any((B@B)%p)
    assert set(map(int,B.sum(1)))=={q**3}
    # Explicit projective line <e0,e1>, with points [1:a:0:0], [0:1:0:0]
    L={(1,a,0,0) for a in range(q)}
    L.add((0,1,0,0))
    assert len(L)==q+1
    ids=[j for j,pt in enumerate(pts) if pt in L]
    assert len(ids)==q+1
    witness=np.zeros(n,dtype=np.int64);witness[ids]=1
    assert not np.any((B@witness)%p)
    assert int(witness.sum())%p==1
    # Count all hyperplanes via polarity and verify the key covering bound.
    through_one=q*q+q+1
    through_two=q+1
    assert n-q*through_one==1
    assert through_one-(q-1)*through_two==q+2
    # Select one support set of size exactly q and construct for each point
    # an avoiding hyperplane and a hyperplane meeting the set just there.
    support=list(range(q))
    incidences=(sym==0)
    avoid=np.where(np.sum(incidences[:,support],axis=1)==0)[0]
    assert len(avoid)>=1
    isolating=[]
    for at in support:
        others=[j for j in support if j!=at]
        rows=np.where(incidences[:,at] & (np.sum(incidences[:,others],axis=1)==0))[0]
        assert len(rows)>=1
        isolating.append(int(rows[0]))
    # Optional brute-force independent binary distance sentinel for q=4:
    # any 4-column zero relation in F2 would give colliding pairwise XORs.
    binary_distance4_exhaustive=None
    if q==4:
        bitcols=[sum(int(B[i,j])<<i for i in range(n)) for j in range(n)]
        assert len(set(bitcols))==n and 0 not in bitcols
        sums={}
        for i,j in itertools.combinations(range(n),2):
            z=bitcols[i]^bitcols[j]
            if z in sums:
                a,b=sums[z]
                assert len({a,b,i,j})<4
            else:sums[z]=(i,j)
        assert all((bitcols[i]^bitcols[j]) not in set(bitcols)
                   for i,j in itertools.combinations(range(n),2))
        binary_distance4_exhaustive=True
    k=n-2*rank
    assert k>=0
    return {
        "p":p,"t":t,"q":q,"n":n,"rank_B":rank,
        "CSS":{"n":n,"k":k,"distance":q+1,"symbol_field":f"F_{p}"},
        "line_logical_word_weight":len(ids),
        "line_check_in_kernel_B":True,
        "line_not_in_stabilizer_row_B":True,
        "all_rows_weight":q**3,
        "projective_hyperplanes":n,
        "hyperplanes_through_one_point":through_one,
        "hyperplanes_through_two_points":through_two,
        "uncovered_hyperplane_union_bound":n-q*through_one,
        "isolating_hyperplane_lower_bound":through_one-(q-1)*through_two,
        "sample_support_q_avoiding_H_count":int(len(avoid)),
        "sample_support_q_isolating_H_indices":isolating,
        "q4_all_dual_weights_below5_excluded_by_xor":binary_distance4_exhaustive,
        "known_rank_boundary":"Known defining-characteristic projective hyperplane rank, not a new p-rank theorem."
    }

def release():
    cases=[case(*x) for x in [
        (2,1,(0,1)),(3,1,(0,1)),(2,2,(1,1,1)),
        (5,1,(0,1)),(2,3,(1,1,0,1)),(3,2,(1,0,1))
    ]]
    result={c["q"]:c["CSS"] for c in cases}
    expected={2:(15,7,3),3:(40,20,4),4:(85,53,5),
              5:(156,86,6),8:(585,457,9),9:(820,620,10)}
    assert {q:(v["n"],v["k"],v["distance"]) for q,v in result.items()}==expected
    return {
      "status":"PASS_EXACT_GEOMETRIC_CSS","classical_RH_proved":False,
      "theorem":"[[n, n-2 binomial(p+2,3)^t, q+1]]_p where n=(q+1)(q²+1), q=p^t",
      "distance_proof":"For <=q support S, some hyperplane H avoids S because v>q(q²+q+1). For each s in S another hyperplane meets S only at s because q²+q+1>(q-1)(q+1). As B is the complement-hyperplane incidence, Bc=0 forces sum(c)=0 and sum(c)-c_s=0, so c_s=0. Conversely an ambient PG(3,q) line has q+1 points, and each hyperplane intersects it in 1 or q+1 points. Every B row then intersects the line in q or 0 places, giving B*line=0 in Fp. Row(B) has coordinate sum 0 since every B row has q³ nonzeros, but the line has sum q+1=1 mod p, hence it is an unstabilized weight-(q+1) logical word.",
      "prior_art":"Projective hyperplane p-rank is classical, published e.g. 1969 Hamada; W33 [[40,20,4]]_3 already in Pass 5746. The all-q distance/CSS crosswalk is a new-to-repo packaging, not asserted publication novelty.",
      "cases":cases,
      "physics_boundary":"Code parameters do not prove hardware fault tolerance, local gate implementation, or classical RH."
    }

if __name__=="__main__":
    r=release()
    path=Path(__file__).resolve().parents[1]/"data"/"w33_20261022_allq_pascal_CSS_exact_distance.json"
    path.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print([(z["q"],z["CSS"]) for z in r["cases"]])
