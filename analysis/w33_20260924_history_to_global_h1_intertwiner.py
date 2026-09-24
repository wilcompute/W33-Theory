#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, sys
from collections import deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_history_to_global_h1_intertwiner.json"

from analysis.w33_20260924_history_bigcell_q43_compactification import (
    all_points, all_lagrangian_lines, history_line, graph_adj, symp,
    gl2_projective_reps, history_perm,
)
from analysis.w33_20260924_history_cycle81_character_bridge import point_perm


def rank_mod(A,p):
    A=np.array(A,dtype=np.int64)%p
    m,n=A.shape
    r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if A[i,c]%p),None)
        if piv is None:
            continue
        A[[r,piv]]=A[[piv,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and A[i,c]:
                A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
        if r==m:
            break
    return r


def signed_add(vec,eidx,u,v,coef=1):
    if u<v:
        vec[eidx[(u,v)]]+=coef
    else:
        vec[eidx[(v,u)]]-=coef


def fundamental_cycle_basis(n,edges):
    eidx={e:i for i,e in enumerate(edges)}
    adj=[[] for _ in range(n)]
    for k,(u,v) in enumerate(edges):
        adj[u].append((v,k))
        adj[v].append((u,k))
    parent=[-1]*n
    depth=[0]*n
    parent[0]=0
    tree=set()
    Q=deque([0])
    while Q:
        u=Q.popleft()
        for v,k in adj[u]:
            if parent[v]<0:
                parent[v]=u
                depth[v]=depth[u]+1
                tree.add(k)
                Q.append(v)
    chords=[k for k in range(len(edges)) if k not in tree]
    cols=[]
    for ck in chords:
        u,v=edges[ck]
        vec=np.zeros(len(edges),dtype=np.int64)
        signed_add(vec,eidx,u,v,1)
        a,b=v,u
        while depth[a]>depth[b]:
            pa=parent[a]
            signed_add(vec,eidx,a,pa,1)
            a=pa
        while depth[b]>depth[a]:
            pb=parent[b]
            signed_add(vec,eidx,pb,b,1)
            b=pb
        while a!=b:
            pa=parent[a]
            pb=parent[b]
            signed_add(vec,eidx,a,pa,1)
            signed_add(vec,eidx,pb,b,1)
            a,b=pa,pb
        cols.append(vec)
    return np.column_stack(cols)


def edge_action_matrix(perm,edges,eidx):
    M=np.zeros((len(edges),len(edges)),dtype=np.int64)
    for k,(u,v) in enumerate(edges):
        a,b=perm[u],perm[v]
        if a<b:
            M[eidx[(a,b)],k]=1
        else:
            M[eidx[(b,a)],k]=-1
    return M


def main():
    pts=all_points()
    pidx={p:i for i,p in enumerate(pts)}
    lines=all_lagrangian_lines()
    B=frozenset(p for p in pts if p[2]==0 and p[3]==0)
    hs=list(itertools.product(range(3),repeat=3))
    hlines=[history_line(s) for s in hs]
    A=graph_adj(hlines)
    hedges=[(i,j) for i in range(27) for j in range(i+1,27) if A[i,j]]
    heidx={e:i for i,e in enumerate(hedges)}
    assert len(hedges)==108

    gedges=[
        (i,j) for i,j in itertools.combinations(range(40),2)
        if symp(pts[i],pts[j])==0
    ]
    geidx={e:i for i,e in enumerate(gedges)}
    assert len(gedges)==240

    triangles=[]
    for L in lines:
        ids=sorted(pidx[x] for x in L)
        triangles.extend(itertools.combinations(ids,3))
    assert len(triangles)==160

    D2=np.zeros((240,160),dtype=np.int64)
    for k,(a,b,c) in enumerate(triangles):
        signed_add(D2[:,k],geidx,b,c,1)
        signed_add(D2[:,k],geidx,a,c,-1)
        signed_add(D2[:,k],geidx,a,b,1)

    M=np.zeros((240,108),dtype=np.int64)
    quad_count=[]
    edge_rows=[]
    for k,(i,j) in enumerate(hedges):
        L=hlines[i]
        R=hlines[j]
        meet=L&R
        assert len(meet)==1
        p=next(iter(meet))
        pi=pidx[p]
        used=0
        for b in sorted(B):
            bi=pidx[b]
            xs=[x for x in L if symp(b,x)==0]
            ys=[y for y in R if symp(b,y)==0]
            assert len(xs)==len(ys)==1
            x,y=xs[0],ys[0]
            if x==p:
                assert y==p
                continue
            xi,yi=pidx[x],pidx[y]
            signed_add(M[:,k],geidx,bi,xi,1)
            signed_add(M[:,k],geidx,xi,pi,1)
            signed_add(M[:,k],geidx,pi,yi,1)
            signed_add(M[:,k],geidx,yi,bi,1)
            used+=1
        assert used==3
        quad_count.append(used)
        edge_rows.append({
            "history_edge":[i,j],
            "intersection_point":list(p),
            "quadrilaterals":used,
        })

    D1=np.zeros((40,240),dtype=np.int64)
    for k,(u,v) in enumerate(gedges):
        D1[u,k]=-1
        D1[v,k]=1
    assert np.all(D1@M==0)

    C=fundamental_cycle_basis(27,hedges)
    assert C.shape==(108,82)
    Y=M@C

    htris=[t for t in itertools.combinations(range(27),3)
           if A[t[0],t[1]] and A[t[0],t[2]] and A[t[1],t[2]]]
    assert len(htris)==36
    HT=np.zeros((108,36),dtype=np.int64)
    for k,(a,b,c) in enumerate(htris):
        signed_add(HT[:,k],heidx,b,c,1)
        signed_add(HT[:,k],heidx,a,c,-1)
        signed_add(HT[:,k],heidx,a,b,1)

    ranks={}
    for prime in (5,7,11,101):
        rb=rank_mod(D2,prime)
        total=rank_mod(np.column_stack([D2,Y]),prime)
        ry=total-rb
        rt=rank_mod(HT,prime)
        tri_image_extra=rank_mod(np.column_stack([D2,M@HT]),prime)-rb
        ranks[str(prime)]={"boundary_rank":rb,"induced_history_rank":ry,
                           "history_triangle_rank":rt,
                           "triangle_image_extra_rank":tri_image_extra}
        assert (rb,ry,rt,tri_image_extra)==(120,46,36,0)

    reps=gl2_projective_reps()
    stabilizer={}
    for G in reps:
        for t in hs:
            hp=history_perm(G,t,1)
            pp=point_perm(G,t,pts)
            stabilizer[hp]=pp
    assert len(stabilizer)==648

    equivariant=True
    for hp,pp in stabilizer.items():
        H=edge_action_matrix(hp,hedges,heidx)
        Pm=edge_action_matrix(pp,gedges,geidx)
        if not np.array_equal(Pm@M,M@H):
            equivariant=False
            break
    assert equivariant

    out={
      "schema":"w33.20260924.history_to_global_h1_intertwiner.v1",
      "status":"PASS_EXPLICIT_TEMPORAL_CYCLES_TO_GLOBAL_W33_H1_INTERTWINER",
      "construction":{
        "domain":"oriented edges of the 27-history null graph",
        "codomain":"oriented cycles of the 40-point W33 graph",
        "edge_rule":(
          "for L->M meeting at p, sum over the three Bell points b not "
          "collinear with p of b->x_L(b)->p->x_M(b)->b"
        ),
        "quadrilaterals_per_history_edge":sorted(set(quad_count)),
        "orientation_reversal":"M->L negates the chain",
        "Bell_stabilizer_equivariant_all_648":equivariant,
      },
      "homology":{
        "history_cycle_dimension":82,
        "history_triangle_boundary_rank":36,
        "filled_history_H1_dimension":46,
        "global_triangle_boundary_rank":120,
        "global_H1_dimension":81,
        "induced_rank_mod_primes":ranks,
        "kernel_dimension_on_history_cycles":36,
        "kernel_is_exactly_history_triangle_boundary_space":True,
        "induced_filled_history_H1_map_rank":46,
      },
      "theorem":(
        "The Bell line turns every temporal edge into three W33 quadrilateral "
        "cycles. This integral chain map is equivariant under all 648 Bell-line "
        "stabilizer elements. Its homology rank is 46, and its kernel on the "
        "82-dimensional temporal cycle space is exactly the 36-dimensional "
        "span of the filled temporal triangles. It therefore gives an explicit "
        "injective map from filled temporal H1 (dimension 46) into global W33 H1."
      ),
      "boundary":(
        "Ranks are independently certified modulo 5,7,11,101. The map itself "
        "is integral. This proves the finite homology/module bridge, not a "
        "continuum proper-time interpretation."
      ),
      "sample_edges":edge_rows[:12],
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "equivariant":equivariant,
      "ranks":ranks,
      "kernel_dimension":36,
    },indent=2,sort_keys=True))


if __name__=="__main__":
    main()
