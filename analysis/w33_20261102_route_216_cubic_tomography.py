#!/usr/bin/env python3
"""Exact cubic tomography of the 216 W33 minimum route supports.

Self-contained integer witness. The canonical seed uses lexicographically
ordered projective F3^4 points and isotropic lines. Pass 173/12483 establish
independently that the 216-element orbit is the complete minimum shell.
No continuum or physical substrate assertion is made here.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import json
import numpy as np

SEED = (10, 11, 25, 27, 28, 30, 31, 32, 37, 38)

def geometry():
    def norm(x):
        first = next((t for t in x if t % 3), None)
        if first is None:
            return None
        return tuple(t * pow(first, -1, 3) % 3 for t in x)
    pts = sorted({norm(x) for x in product(range(3), repeat=4)} - {None})
    ix = {p: i for i, p in enumerate(pts)}
    def omega(u, v):
        return (u[0]*v[2] + u[1]*v[3] - u[2]*v[0] - u[3]*v[1]) % 3
    lines = sorted({tuple(sorted({ix[norm(tuple((u[j]+t*v[j]) % 3
                    for j in range(4)))] for t in range(3)} | {ix[v]}))
                    for u in pts for v in pts if u != v and omega(u,v) == 0})
    N = np.zeros((40,40), dtype=np.int64)
    for j, line in enumerate(lines):
        assert len(line) == 4
        N[list(line),j] = 1
    assert len(pts) == len(lines) == 40
    assert np.all(N.sum(axis=0)==4) and np.all(N.sum(axis=1)==4)
    return pts,lines,N,ix,norm,omega

def compute():
    pts,lines,N,ix,norm,omega = geometry()
    lid = {frozenset(line):j for j,line in enumerate(lines)}
    seed = frozenset(SEED)
    assert len(seed)==10 and Counter(map(int,N[:,list(seed)].sum(axis=1)))=={0:20,2:20}
    gens=[]
    for a in pts:
        g=[ix[norm(tuple((x[j]+omega(x,a)*a[j]) % 3 for j in range(4)))]
           for x in pts]
        gens.append(tuple(lid[frozenset(g[x] for x in line)] for line in lines))
    orbit={seed}
    frontier=[seed]
    while frontier:
        follow=[]
        for s in frontier:
            for g in gens:
                t=frozenset(g[j] for j in s)
                if t not in orbit:
                    orbit.add(t);follow.append(t)
        frontier=follow
    assert len(orbit)==216
    supports=sorted(orbit,key=lambda s:tuple(sorted(s)))
    B=np.zeros((216,40),dtype=np.int64)
    for i,s in enumerate(supports):
        B[i,list(s)]=1
    Aline=N.T@N-4*np.eye(40,dtype=np.int64)
    Apoint=N@N.T-4*np.eye(40,dtype=np.int64)
    eye=np.eye(40,dtype=np.int64)
    ones=np.ones((40,40),dtype=np.int64)
    assert np.array_equal(B.T@B,44*eye+8*Aline+10*ones)
    cover=B@N.T
    assert set(np.unique(cover))=={0,2}
    H=cover//2
    assert np.all(H.sum(axis=0)==108) and np.all(H.sum(axis=1)==20)
    assert np.array_equal(H.T@H,60*eye+15*Apoint+48*ones)
    Z=2*H-1
    assert np.all(Z.sum(axis=0)==0) and np.all(Z.sum(axis=1)==0)
    projector_num=(Apoint+4*eye)@(12*eye-Apoint)
    assert np.array_equal(Z.T@Z,6*projector_num)
    assert np.array_equal((Z.T@Z)@(Z.T@Z),360*(Z.T@Z))
    assert np.linalg.matrix_rank(Z)==24
    Gram=H@H.T
    pair=Counter(int(Gram[i,j]) for i in range(216) for j in range(i+1,216))
    assert pair=={8:7020,9:6480,11:4320,12:3240,14:2160}
    cubic=defaultdict(Counter)
    for a,b,c in combinations(range(40),3):
        edges=int(Apoint[a,b]+Apoint[a,c]+Apoint[b,c])
        centers=int(np.sum(Apoint[:,a]*Apoint[:,b]*Apoint[:,c])) if edges==0 else 0
        m=int(np.dot(Z[:,a]*Z[:,b],Z[:,c]))
        cubic[(edges,centers)][m]+=1
        if m==108:
            assert edges==3 and int(np.sum(N[a]*N[b]*N[c]))==1
    expected={(0,1):{0:2880},(0,4):{-48:360},(1,0):{12:4320},
              (2,0):{-24:2160},(3,0):{108:160}}
    assert {k:dict(v) for k,v in cubic.items()}==expected
    assert np.array_equal(Apoint@Apoint,8*eye-2*Apoint+4*ones)
    return {
        "status":"PASS_INTEGER_ROUTE_216_CUBIC_TOMOGRAPHY",
        "seed":list(SEED),"point_count":40,"line_count":40,
        "minimum_support_orbit":216,"lines_per_support":10,"points_covered":20,
        "gram_line":"B.T B=44 I+8 A_line+10 J",
        "gram_point":"H.T H=60 I+15 A_point+48 J",
        "point_gram_eigenvalues":{"2160":1,"90":24,"0":15},
        "centered_sign_frame":"Z=2H-J; Z.T Z=360 E_2, rank 24",
        "spherical_tight_2_design":True,
        "pairwise_point_support_intersections":dict(sorted(pair.items())),
        "cubic_tensor":"T_abc=sum_s Z_sa Z_sb Z_sc",
        "cubic_types":[{"edge_pairs":a,"common_centers":c,
                        "moment":next(iter(m)),"triple_count":sum(m.values())}
                        for (a,c),m in sorted(cubic.items())],
        "scope":"Exact finite codeword tomography only; no physical TOE result."
    }

if __name__=="__main__":
    result=compute()
    target=Path(__file__).resolve().parents[1]/"data"/"w33_20261102_route_216_cubic_tomography.json"
    target.parent.mkdir(exist_ok=True,parents=True)
    target.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(result["status"], result["minimum_support_orbit"], result["cubic_types"])
