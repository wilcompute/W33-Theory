#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; P=3

def canon(v):
    v=tuple(int(x)%P for x in v)
    if v==(0,0,0,0): raise ValueError
    for x in v:
        if x: return tuple(((1 if x==1 else 2)*y)%P for y in v)

def sp(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P

def spectrum_scaled(A,scale=1):
    return Counter(int(round(x*scale)) for x in np.linalg.eigvalsh(A.astype(float)))

def build_w33():
    pts=[]; seen=set()
    for raw in product(range(P), repeat=4):
        if raw==(0,0,0,0): continue
        z=canon(raw)
        if z not in seen: seen.add(z); pts.append(z)
    A=np.zeros((40,40), dtype=int)
    for i,j in combinations(range(40),2):
        if sp(pts[i],pts[j])==0: A[i,j]=A[j,i]=1
    return A

def main():
    A=build_w33(); I=np.eye(40,dtype=int); J=np.ones((40,40),dtype=int)
    # P15 = E15 = (8I+J-4A)/24, but keep numerator integral for exact checks.
    P15_num=8*I+J-4*A
    P25_num=16*I+4*A-J

    centers={}
    for t in combinations(range(40),3):
        if all(A[a,b]==0 for a,b in combinations(t,2)):
            centers[t]=tuple(x for x in range(40) if all(A[x,a] for a in t))

    curved=[tuple(sorted((c[0],)+t)) for t,c in centers.items() if len(c)==1]
    M=np.zeros((40,len(curved)), dtype=int)
    for j,B in enumerate(curved):
        for p in B: M[p,j]=1

    G=M@M.T
    # Projected frame operator on the E15 sector.  Since P15=P15_num/24,
    # exact identity is P15 G P15 = 192 P15, equivalently
    # P15_num G P15_num = 192*24*P15_num.
    exact_frame_left=P15_num@G@P15_num
    exact_frame_right=192*24*P15_num

    # Each curved event has E15 norm 1: b^T P15 b = 1, equivalently b^T P15_num b = 24.
    e15_norms=Counter(int(M[:,j].T@P15_num@M[:,j]) for j in range(M.shape[1]))
    e25_norms=Counter(int(M[:,j].T@P25_num@M[:,j]) for j in range(M.shape[1]))

    # Ordinary point-space pairwise projected inner products in numerator scale.
    # b_i^T P15_num b_j = 24 * <proj_i,proj_j>.
    sample_inner=Counter()
    for i,j in combinations(range(min(300,M.shape[1])),2):
        sample_inner[int(M[:,i].T@P15_num@M[:,j])] += 1

    checks={
        "curved_event_count": len(curved)==2880,
        "projector_scaled_idempotents": np.array_equal(P15_num@P15_num,24*P15_num) and np.array_equal(P25_num@P25_num,24*P25_num),
        "projector_ranks": int(np.trace(P15_num)//24)==15 and int(np.trace(P25_num)//24)==25,
        "curved_gram_identity": np.array_equal(G,272*I+16*J+20*A),
        "unit_e15_norms": e15_norms==Counter({24:2880}),
        "constant_e25_norms": e25_norms==Counter({72:2880}),
        "tight_frame_e15_exact": np.array_equal(exact_frame_left, exact_frame_right),
        "frame_bound_trace": int(np.trace(G@P15_num)//24)==2880 and 15*192==2880,
    }

    payload={
        "theorem_name":"Curved Events E15 Tomotope-Redundancy Tight Frame Theorem",
        "summary":{
            "all_checks_passed":all(checks.values()),
            "curved_events":len(curved),
            "rank_E15":15,
            "tomotope_redundancy":192,
            "identity":"P15 M M^T P15 = 192 P15",
            "unit_E15_norm":"each curved event has projected E15 norm 1",
            "total_trace":"2880 = 15 * 192",
        },
        "checks":checks,
        "norms_scaled_by_24":{
            "E15_norm_numerator_distribution":dict(e15_norms),
            "E25_norm_numerator_distribution":dict(e25_norms),
        },
        "sample_projected_inner_products_scaled_by_24":dict(sample_inner),
        "identities":{
            "E15":"E15=(8I+J-4A)/24",
            "curved_gram":"M_curved M_curved^T=272I+16J+20A",
            "tight_frame":"E15 M_curved M_curved^T E15 = 192 E15",
            "unit_norm":"For every curved event b, b^T E15 b = 1",
            "redundancy":"2880 curved events / rank(E15)=192",
        },
        "interpretation":"The 2880 one-centered curved events are not merely 15 times 192 by trace. Their E15 projections are 2880 unit vectors forming a tight frame in the 15-dimensional curvature-active sector with frame bound 192. Thus the tomotope 192 appears as the redundancy/flag-carrier scale per E15 dimension.",
        "boundary":"This is a canonical tight-frame theorem, stronger than a count. It still does not choose a canonical partition of the 2880 events into 15 disjoint 192-event packets."
    }
    path=ROOT/'data'/'w33_curved_events_e15_tight_frame.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps(payload['summary'],indent=2,sort_keys=True)); return 0 if payload['summary']['all_checks_passed'] else 1
if __name__=='__main__': raise SystemExit(main())
