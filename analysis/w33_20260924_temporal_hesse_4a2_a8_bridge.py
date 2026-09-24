#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from collections import Counter, deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20260924_temporal_hesse_4a2_a8_bridge.json"

F3=range(3)
CELLS=list(itertools.product(F3,repeat=2))
CID={p:i for i,p in enumerate(CELLS)}

def det2(A):
    return (int(A[0,0])*int(A[1,1])-int(A[0,1])*int(A[1,0]))%3

def gl2():
    out=[]
    for z in itertools.product(F3,repeat=4):
        A=np.array(z,dtype=int).reshape(2,2)
        if det2(A):
            out.append(A)
    assert len(out)==48
    return out

def affine_perm(A,t):
    return tuple(
        CID[tuple(int(x) for x in ((A@np.array(p,dtype=int)+t)%3))]
        for p in CELLS
    )
def collinear(tri):
    pts=[np.array(CELLS[i],dtype=int) for i in tri]
    u=(pts[1]-pts[0])%3
    v=(pts[2]-pts[0])%3
    return (int(u[0])*int(v[1])-int(u[1])*int(v[0]))%3==0

def orbit(seed,perms):
    seed=frozenset(seed)
    return {
        frozenset(p[i] for i in seed)
        for p in perms
    }

def scaled_exterior_root(tri):
    # 3*w_S: +2 on S, -1 on the complement. Norm^2=18.
    r=-np.ones(9,dtype=int)
    for i in tri:
        r[i]=2
    assert int(r.sum())==0 and int(r@r)==18
    return tuple(map(int,r))

def scaled_a8_root(i,j):
    r=np.zeros(9,dtype=int)
    r[i]=3
    r[j]=-3
    assert int(r.sum())==0 and int(r@r)==18
    return tuple(map(int,r))
def reflection(r,s):
    r=np.array(r,dtype=int)
    s=np.array(s,dtype=int)
    num=2*int(s@r)
    den=int(r@r)
    assert num%den==0
    return tuple(map(int,s-(num//den)*r))

def rank_q(vectors):
    M=np.array(vectors,dtype=float)
    return int(np.linalg.matrix_rank(M,tol=1e-9))

def main():
    triples=[tuple(t) for t in itertools.combinations(range(9),3)]
    lines=[t for t in triples if collinear(t)]
    triangles=[t for t in triples if not collinear(t)]
    assert (len(triples),len(lines),len(triangles))==(84,12,72)

    perms={
        affine_perm(A,np.array(t,dtype=int))
        for A in gl2() for t in CELLS
    }
    assert len(perms)==432
    line_orbit=orbit(lines[0],perms)
    tri_orbit=orbit(triangles[0],perms)
    assert len(line_orbit)==12 and len(tri_orbit)==72
    assert line_orbit==set(map(frozenset,lines))
    assert tri_orbit==set(map(frozenset,triangles))
    # Parallel classes are the four Hesse directions.
    remaining=set(map(frozenset,lines))
    parallel=[]
    while remaining:
        L=min(remaining,key=lambda x:tuple(sorted(x)))
        cls={M for M in remaining if not (L&M)}
        cls.add(L)
        assert len(cls)==3
        assert set().union(*map(set,cls))==set(range(9))
        assert all(not(A&B) for A,B in itertools.combinations(cls,2))
        parallel.append(sorted((tuple(sorted(x)) for x in cls)))
        remaining-=cls
    parallel=sorted(parallel)
    assert len(parallel)==4

    ext={t:scaled_exterior_root(t) for t in triples}
    hesse_pos=[ext[t] for t in lines]
    hesse_full=set(hesse_pos)|{
        tuple(-x for x in r) for r in hesse_pos
    }
    assert len(hesse_full)==24

    # Each parallel class is one A2; distinct classes are orthogonal.
    class_checks=[]
    for cls in parallel:
        rs=[np.array(ext[t],dtype=int) for t in cls]
        gram=[[int(a@b) for b in rs] for a in rs]
        assert gram==[[18,-9,-9],[-9,18,-9],[-9,-9,18]]
        assert np.array_equal(sum(rs),np.zeros(9,dtype=int))
        class_checks.append({"lines":[list(x) for x in cls],"scaled_gram":gram})
    for a,b in itertools.combinations(range(4),2):
        for L in parallel[a]:
            for M in parallel[b]:
                assert len(set(L)&set(M))==1
                assert int(np.array(ext[L])@np.array(ext[M]))==0

    assert rank_q(list(hesse_full))==8
    for r in hesse_full:
        for s in hesse_full:
            assert reflection(r,s) in hesse_full

    # Standard A8 realization of all 240 E8 roots, uniformly scaled by 3.
    a8={
        scaled_a8_root(i,j)
        for i in range(9) for j in range(9) if i!=j
    }
    lam3=set(ext.values())
    lam6={tuple(-x for x in r) for r in lam3}
    roots=a8|lam3|lam6
    assert (len(a8),len(lam3),len(lam6),len(roots))==(72,84,84,240)
    assert all(sum(r)==0 and sum(x*x for x in r)==18 for r in roots)
    assert not (a8&lam3) and not(a8&lam6) and not(lam3&lam6)

    noncol_pos={ext[t] for t in triangles}
    noncol_full=noncol_pos|{tuple(-x for x in r) for r in noncol_pos}
    assert len(noncol_full)==144
    assert roots==a8|hesse_full|noncol_full
    # Four affine directions are canonically P1(F3).
    directions=[]
    for cls in parallel:
        L=cls[0]
        p,q=CELLS[L[0]],CELLS[L[1]]
        d=((q[0]-p[0])%3,(q[1]-p[1])%3)
        if d[0]:
            s=1 if d[0]==1 else 2
        else:
            s=1 if d[1]==1 else 2
        directions.append(tuple((s*x)%3 for x in d))
    assert set(directions)=={(1,0),(0,1),(1,1),(1,2)}

    out={
      "schema":"w33.20260924.temporal_hesse_4a2_a8_bridge.v1",
      "status":"PASS_HESSE_12_IS_4A2_INSIDE_TEMPORAL_A8_E8",
      "history_plane":{
        "cells":9,
        "unordered_triples":84,
        "affine_group_order":len(perms),
        "AGL_orbits":{"Hesse_lines":len(line_orbit),"noncollinear_triangles":len(tri_orbit)},
        "parallel_classes":parallel,
        "projective_directions":[list(x) for x in sorted(set(directions))],
      },
      "A8_E8_model":{
        "root_scaling":"all roots multiplied by 3, so squared norm is 18",
        "sl9_A8_roots":len(a8),
        "Lambda3_roots":len(lam3),
        "Lambda6_roots":len(lam6),
        "total_E8_roots":len(roots),
        "branching":"240 = 72 + 84 + 84",
      },
      "Hesse_4A2":{
        "positive_exterior_roots":12,
        "negative_exterior_roots":12,
        "root_count":len(hesse_full),
        "rank":rank_q(list(hesse_full)),
        "components":4,
        "roots_per_component":6,
        "parallel_class_checks":class_checks,
        "reflection_closed":True,
        "cross_components_orthogonal":True,
      },
      "root_partition":{
        "A8_transition_roots":len(a8),
        "Hesse_4A2_roots":len(hesse_full),
        "noncollinear_temporal_triangle_roots":len(noncol_full),
        "identity":"240 = 72 + 24 + 144",
        "Lie_dimension_identity":"248 = 8 Cartan + 72 + 24 + 144 = 80 + 84 + 84",
      },
      "theorem":(
        "In the standard A8 realization of E8, the 84 Lambda^3 roots are indexed "
        "by 3-subsets of a nine-cell basis. When the basis is identified with "
        "AG(2,3), AGL(2,3) splits those roots into the 12 affine Hesse lines and "
        "72 noncollinear triples. The 12 Hesse roots form four parallel classes "
        "of three roots. Within each class the roots have pairwise inner product "
        "-1 and sum to zero; different classes are orthogonal. Adding their "
        "negatives from Lambda^6 produces a reflection-closed rank-eight 4A2 "
        "root subsystem with 24 roots. Hence the temporal/Hesse split refines "
        "the E8 root shell exactly as 240=72_A8+24_4A2+144_triangle."
      ),
      "repo_boundary":(
        "The A8 branching E8=sl9+Lambda3+Lambda6 and the existence/census of "
        "E8 4A2 subsystems are prior repository/classical results. The new packet "
        "is the explicit identification of the AG(2,3) Hesse 12+12 exterior roots "
        "with one 4A2 subsystem in the temporal nine-cell basis."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "orbits":out["history_plane"]["AGL_orbits"],
      "Hesse4A2":out["Hesse_4A2"],
      "partition":out["root_partition"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
