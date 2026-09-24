#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20260924_history_bigcell_q43_compactification.json"
P=3

def canon(v):
    v=tuple(int(x)%P for x in v)
    for x in v:
        if x:
            s=1 if x==1 else 2
            return tuple((s*y)%P for y in v)
    raise ValueError("zero")

def symp(u,v):
    return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%P

def line_from_basis(u,v):
    return frozenset(canon(tuple((a*u[i]+b*v[i])%P for i in range(4)))
                     for a,b in itertools.product(range(3),repeat=2) if a or b)
def all_points():
    return sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})

def all_lagrangian_lines():
    pts=all_points(); lines=set()
    for i,u in enumerate(pts):
        for v in pts[i+1:]:
            if symp(u,v)==0:
                L=line_from_basis(u,v)
                if len(L)==4: lines.add(L)
    return sorted(lines,key=lambda L:sorted(L))

def history_line(s):
    a,b,c=s
    return line_from_basis((a,b,1,0),(b,c,0,1))

def detdiff(s,t):
    a=(s[0]-t[0])%3; b=(s[1]-t[1])%3; c=(s[2]-t[2])%3
    return (a*c-b*b)%3

def wedge5(L):
    u,v=sorted(L)[:2]
    p12=(u[0]*v[1]-u[1]*v[0])%3
    p14=(u[0]*v[3]-u[3]*v[0])%3
    p23=(u[1]*v[2]-u[2]*v[1])%3
    p24=(u[1]*v[3]-u[3]*v[1])%3
    p34=(u[2]*v[3]-u[3]*v[2])%3
    return canon((p34,p14,p24,-p23,p12))
def q43(x):
    return (x[0]*x[4]-x[1]*x[3]+x[2]*x[2])%3

def graph_adj(lines):
    n=len(lines); A=np.zeros((n,n),dtype=int)
    for i in range(n):
        for j in range(i+1,n):
            if lines[i]&lines[j]:
                A[i,j]=A[j,i]=1
    return A

def spectrum(A):
    vals=np.linalg.eigvalsh(A.astype(float))
    return dict(sorted(Counter(int(round(x)) for x in vals).items(),reverse=True))

def srg_check(A):
    n=len(A); deg=A.sum(axis=1)
    assert len(set(map(int,deg)))==1
    lam=set(); mu=set()
    for i in range(n):
        for j in range(i+1,n):
            cn=int(A[i]@A[j])
            (lam if A[i,j] else mu).add(cn)
    return int(deg[0]),sorted(lam),sorted(mu)

def mat2(A,s):
    S=np.array([[s[0],s[1]],[s[1],s[2]]],dtype=int)
    R=(A@S@A.T)%3
    return int(R[0,0]),int(R[0,1]),int(R[1,1])
def gl2_projective_reps():
    mats=[]
    for z in itertools.product(range(3),repeat=4):
        A=np.array(z,dtype=int).reshape(2,2)
        det=int(round(np.linalg.det(A)))%3
        if det: mats.append(A)
    reps={}
    for A in mats:
        a=tuple(map(int,A.reshape(-1)))
        b=tuple(map(int,((-A)%3).reshape(-1)))
        reps[min(a,b)]=np.array(min(a,b),dtype=int).reshape(2,2)
    assert len(reps)==24
    return list(reps.values())

def history_perm(A,T,eps=1):
    hs=list(itertools.product(range(3),repeat=3)); idx={s:i for i,s in enumerate(hs)}
    out=[]
    for s in hs:
        r=mat2(A,s)
        u=tuple((eps*r[i]+T[i])%3 for i in range(3))
        out.append(idx[u])
    return tuple(out)

def main():
    lines=all_lagrangian_lines()
    assert len(lines)==40
    B=line_from_basis((1,0,0,0),(0,1,0,0))
    hs=list(itertools.product(range(3),repeat=3))
    hlines=[history_line(s) for s in hs]
    assert len(set(hlines))==27 and all(not (L&B) for L in hlines)
    boundary=[L for L in lines if L not in set(hlines)]
    assert len(boundary)==13 and all(L&B for L in boundary)
    coords={L:wedge5(L) for L in lines}
    assert all(q43(x)==0 for x in coords.values())
    assert coords[B]==(0,0,0,0,1)
    for s,L in zip(hs,hlines):
        x=coords[L]
        assert x==(1,s[0],s[1],s[2],(s[0]*s[2]-s[1]*s[1])%3)

    dirs=Counter()
    for L in boundary:
        x=coords[L]
        assert x[0]==0
        if L!=B:
            d3=canon(x[1:4])
            assert (d3[0]*d3[2]-d3[1]*d3[1])%3==0
            dirs[d3]+=1
    assert sorted(dirs.values())==[3,3,3,3]

    A40=graph_adj(lines)
    k,lam,mu=srg_check(A40)
    assert (k,lam,mu)==(12,[2],[4])
    hidx=[lines.index(L) for L in hlines]
    A27=A40[np.ix_(hidx,hidx)]
    assert set(map(int,A27.sum(axis=1)))=={8}
    for i,s in enumerate(hs):
        for j,t in enumerate(hs):
            if i!=j:
                assert bool(A27[i,j])==(detdiff(s,t)==0)
    aspec=spectrum(A27)
    lspec=spectrum(8*np.eye(27,dtype=int)-A27)
    assert aspec=={8:1,2:12,-1:8,-4:6}
    assert lspec=={12:6,9:8,6:12,0:1}
    assert int(A27.sum()//2)==108

    reps=gl2_projective_reps()
    psp={history_perm(A,T,1) for A in reps for T in hs}
    full={history_perm(A,T,e) for A in reps for T in hs for e in (1,2)}
    assert len(psp)==648 and len(full)==1296
    assert all(np.array_equal(A27,A27[np.ix_(p,p)]) for p in full)

    bdeg=Counter()
    for L in boundary:
        i=lines.index(L); bdeg[int(A40[i,[lines.index(K) for K in boundary]].sum())]+=1
    assert bdeg==Counter({3:12,12:1})
    cross=int(A40[np.ix_(hidx,[lines.index(L) for L in boundary])].sum())
    assert cross==108
    out={
      "schema":"w33.20260924.history_bigcell_q43_compactification.v1",
      "status":"PASS_27_HISTORY_BIG_CELL_COMPACTS_TO_Q43_LINE_CARRIER",
      "lagrangian_grassmannian":{
        "total_lagrangian_lines":40,
        "bell_line":sorted(B),
        "big_cell_disjoint_from_bell":27,
        "boundary_meeting_bell":13,
        "plucker_coordinates":"[p34,p14,p24,-p23,p12]",
        "quadric_equation":"x0*x4-x1*x3+x2^2=0 over F3",
        "history_embedding":"S=(a,b;b,c) -> [1,a,b,c,ac-b^2]",
      },
      "boundary_cone":{
        "vertex_is_bell_line":True,
        "nonvertex_points":12,
        "rank_one_projective_directions":4,
        "points_per_generator_excluding_vertex":3,
        "induced_degree_histogram":dict(bdeg),
      },
      "null_history_graph":{
        "vertices":27,"edges":108,"degree":8,
        "adjacency":"det(S-T)=0 for S!=T",
        "adjacency_spectrum":aspec,
        "laplacian_spectrum":lspec,
        "cycle_rank":108-27+1,
        "induced_from_Q43_line_intersection_graph":True,
      },
      "full_line_graph":{
        "vertices":40,"edges":240,
        "srg_parameters":[40,12,2,4],
        "cross_edges_bigcell_boundary":cross,
      },
      "stabilizer_actions":{
        "PSp_bell_line_action_order":len(psp),
        "PGSp_bell_line_action_order":len(full),
        "affine_model":"Sym_2(F3) translations semidirect projective congruences; nonsquare scaling doubles 648 to 1296",
      },
      "theorem":(
        "The 27 symmetric-matrix histories are exactly the big cell of the finite "
        "Lagrangian Grassmannian of W(3,3). Their natural completion is the 40-point "
        "parabolic quadric Q(4,3), i.e. the W33 line-side carrier. The 13-point "
        "boundary is a quadratic cone with Bell line as vertex and four 3-point "
        "generators indexed by the four rank-one/null directions."
      ),
      "correction_to_naive_projective_completion":(
        "The natural Lagrangian/Plucker boundary is not merely a PG(2,3) plane. "
        "It is the 13-point tangent-cone section of Q(4,3): 1+4*3. Thus 27+13=40 "
        "promotes to geometry specifically on the W33 line side."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "A27":aspec,
      "L27":lspec,
      "boundary":out["boundary_cone"],
      "groups":out["stabilizer_actions"],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
