#!/usr/bin/env python3
"""Exact 120 ten-point plane hyperovals fill the q=8 CSS classical dual gap.

PG(3,8): 585 points, 4745 projective lines; binary line span rank 401,
but noncollinearity dual has dimension 521. Deterministic seed 20261022
constructs 120 independent hyperovals in 128 invertible shear steps.
The full classical dual is spanned by weight-9 lines and weight-10
hyperovals. These checks are generally CSS logicals, NOT stabilizers.
The underlying hyperoval/even-type-set concepts are published prior art.
"""
from __future__ import annotations
import hashlib,itertools,json,random
from pathlib import Path
from analysis.w33_20261022_six_algebra_optics_frontiers import field
from analysis.w33_20261022_hamada_golden_hidden_checks import (
    projective_points,projective_lines,rank_binary_line_masks
)

def insert(mask,pivs):
    x=mask
    while x:
        pivot=x.bit_length()-1
        if pivot in pivs:x^=pivs[pivot]
        else:pivs[pivot]=x;return True
    return False

def symplectic(x,y,add,mul):
    z=0
    for i,j in ((0,2),(1,3),(2,0),(3,1)):
        z=add[z,mul[x[i],y[j]]]
    return z

def release():
    p,t=2,3
    q,add,mul,inv,neg=field(p,t,(1,1,0,1))
    assert q==8
    P=projective_points(q)
    assert len(P)==585
    idx={v:i for i,v in enumerate(P)}
    lines,n=projective_lines(q,add,mul)
    assert n==585 and len(lines)==4745
    pivs={}
    for ln in lines:
        assert len(ln)==9
        insert(sum(1<<i for i in ln),pivs)
    assert len(pivs)==401
    B=[]
    for x in P:
        mask=sum(1<<i for i,y in enumerate(P) if symplectic(x,y,add,mul)!=0)
        assert mask.bit_count()==512
        B.append(mask)
    assert rank_binary_line_masks([[i for i in range(n) if row>>i&1]
                                   for row in B])==64
    # Standard conic + nucleus in plane x3=0:
    # (1,a,a^2,0) for a∈F8, plus (0,0,1,0),(0,1,0,0).
    vectors=[(1,a,int(mul[a,a]),0) for a in range(q)]
    vectors +=[(0,0,1,0),(0,1,0,0)]
    assert len(set(vectors))==10
    rng=random.Random(20261022)
    witnesses=[];trials=0
    for trial in range(1000):
        i,j=rng.sample(range(4),2)
        coefficient=rng.randrange(1,q)
        vectors=[
            tuple(int(add[v[k],mul[coefficient,v[j]]]) if k==i else v[k]
                  for k in range(4))
            for v in vectors
        ]
        support=[]
        for v in vectors:
            first=next(a for a in v if a)
            unit=inv[first]
            pt=tuple(int(mul[unit,x]) for x in v)
            support.append(idx[pt])
        assert len(set(support))==10
        mask=sum(1<<k for k in support)
        # Every hyperoval meets any polar plane in an even number of points.
        assert all(((mask&row).bit_count()%2)==0 for row in B)
        if insert(mask,pivs):
            witnesses.append(sorted(support))
        trials=trial+1
        if len(pivs)==521:break
    assert trials==128 and len(witnesses)==120 and len(pivs)==521
    assert witnesses[0]==[0,72,160,232,304,376,400,472,512,576]
    assert witnesses[-1]==[81,84,163,164,282,283,441,446,490,494]
    digest=hashlib.sha256(json.dumps(witnesses,separators=(',',':')).encode()).hexdigest()
    assert digest=="a5a43a18acc15681c9976d1666f35a5687e7caf0293ec961c868966a0e946113"
    return {
        "status":"PASS_EXACT_Q8_HYPEROVAL_COMPLETION",
        "classical_RH_proved":False,
        "geometry":"PG(3,8)", "field":"F8", "parity_field":"F2",
        "vertices":585,"noncollinearity_rank":64,"classical_dual_dim":521,
        "projective_line_count":4745,"line_check_weight":9,
        "line_check_rank":401,"independent_hyperovals":120,
        "hyperoval_check_weight":10,"completed_dual_rank":521,
        "deterministic_random_seed":20261022,"shear_steps":trials,
        "ordered_witness_sha256":digest,"witness_coordinate_supports":witnesses,
        "proof":"Projective line indicators lie in ker B. Every GL4(F8) transform of a plane conic+nucleus hyperoval remains a ten-point plane hyperoval, whose indicator is orthogonal to each symplectic polar-plane complement. The seeded 120 witnesses each increase GF2 rank of the 4745 line vectors from 401 to 521; dim ker B=585-rank B=521, proving completeness.",
        "physical_boundary":"These sparse parity checks generate the *classical* dual; do not confuse them with the 64D CSS stabilizer row space. No decoder threshold, universal quantum gates, TOE or classical RH proof."
    }

if __name__=="__main__":
    r=release()
    out=Path(__file__).resolve().parents[1]/"data"/"w33_20261022_q8_hyperoval_dual_completion.json"
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print("q8 line rank",r["line_check_rank"],"hyperoval completed",r["completed_dual_rank"])
