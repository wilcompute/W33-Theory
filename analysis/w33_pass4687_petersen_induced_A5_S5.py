#!/usr/bin/env python3
"""Pass 4687 — the Petersen shortcut module is literally induced from A5/S5.

Fix one of the 27 ten-line Schlaefli/Petersen components.  Its PSp stabilizer
has order 960 and acts on the ten vertices through A5 of order 60 with kernel
16.  The 15 Petersen edges form the A5/V4 degree-15 action; lifting back gives
edge stabilizer 64.  Under PGSp the component stabilizer doubles to 1920 and
the local image doubles to S5; the edge stabilizer becomes D8 downstairs and
128 upstairs.  Thus Q[405 hot edges] is exactly the induced local Petersen-edge
permutation module over the 27-object Schlaefli carrier.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,perm_group,transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
from w33_pass4595_concrete_d4_triality_w33_lifts import max_generators
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4687_PETERSEN_INDUCED_A5_S5_REGEN.json'

def pmask(m,p):
    y=0;x=int(m)
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y|=1<<p[i]
    return y

def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def pord(p):
    seen=[False]*len(p);z=1
    for i in range(len(p)):
        if not seen[i]:
            j=i;n=0
            while not seen[j]:seen[j]=True;n+=1;j=p[j]
            z=math.lcm(z,n)
    return z

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    j=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]]);V=set(span(B9));rep=lambda x:min(int(x),int(x)^j);q=lambda x:(rep(x).bit_count()//4)&1;polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    singular=sorted(x for x in {rep(v) for v in V} if x and q(x)==0);sidx={x:i for i,x in enumerate(singular)}
    def fib(ap):
        x=0
        for i in ap:x^=cols[int(i)]
        return rep(x)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(ap) for ap in apartments});selidx={L:i for i,L in enumerate(selected)}
    N=np.zeros((135,270),dtype=np.int64)
    for c,L in enumerate(selected):
        for x in L:N[sidx[x],c]=1
    Al=N.T@N-3*np.eye(270,dtype=np.int64)
    MG=max_generators(singular,rep,q,polar);selsets=[set(L) for L in selected];O27=[]
    for X in MG:
        I=frozenset(i for i,L in enumerate(selsets) if L.issubset(X))
        if len(I)==10:O27.append(I)
    assert len(O27)==27

    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts];gens=[];G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p])
        if len(trial)>len(G):gens.append(p);G=trial
        if len(G)==25920:break
    def actv(x,g):return rep(pmask(rep(x),g))
    def acts(i,g):return selidx[tuple(sorted(actv(x,g) for x in selected[i]))]
    C0=O27[0];vs=sorted(C0);vidx={v:i for i,v in enumerate(vs)}
    H=[g for g in G if frozenset(acts(v,g) for v in C0)==C0];assert len(H)==960
    image={tuple(vidx[acts(v,g)] for v in vs) for g in H};assert len(image)==60
    assert Counter(pord(p) for p in image)==Counter({5:24,3:20,2:15,1:1})
    kernel=len(H)//len(image);assert kernel==16
    local_edges=[frozenset((vidx[u],vidx[v])) for u,v in itertools.combinations(vs,2) if Al[u,v]];assert len(local_edges)==15
    e0=local_edges[0];estab=[p for p in image if frozenset(p[i] for i in e0)==e0]
    assert len(estab)==4 and Counter(pord(p) for p in estab)==Counter({2:3,1:1})
    assert len(H)//len(estab)==240 # kernel has not yet been divided here
    upstairs_edge_stab=kernel*len(estab);assert upstairs_edge_stab==64

    outer=build_line_perm(np.diag([1,2,1,2])%3,pts,pidx,lines,lidx);PG=set(G)|{comp(outer,g) for g in G};assert len(PG)==51840
    HP=[g for g in PG if frozenset(acts(v,g) for v in C0)==C0];assert len(HP)==1920
    imageP={tuple(vidx[acts(v,g)] for v in vs) for g in HP};assert len(imageP)==120
    assert Counter(pord(p) for p in imageP)==Counter({4:30,2:25,5:24,6:20,3:20,1:1})
    assert len(HP)//len(imageP)==16
    estabP=[p for p in imageP if frozenset(p[i] for i in e0)==e0]
    assert len(estabP)==8 and Counter(pord(p) for p in estabP)==Counter({2:5,4:2,1:1})
    assert 16*len(estabP)==128

    out={'pass':4687,
      'PSp_local':{'component_stabilizer_order':960,'kernel_on_10_vertices':16,'image_order':60,'image':'A5','image_element_orders':{'1':1,'2':15,'3':20,'5':24},'Petersen_edges':15,'edge_stabilizer_image':'V4','edge_stabilizer_upstairs_order':64},
      'PGSp_local':{'component_stabilizer_order':1920,'kernel_on_10_vertices':16,'image_order':120,'image':'S5','edge_stabilizer_image':'D8','edge_stabilizer_upstairs_order':128},
      'induction':{'PSp':'Q[405 hot] = Ind_{H960}^{PSp} Q[A5/V4] = Q[PSp/H64]','PGSp':'Q[405 hot] = Ind_{H1920}^{PGSp} Q[S5/D8] = Q[PGSp/H128]'},
      'theorem':'The 27xPetersen shortcut fabric is a literal induced local Petersen-edge module: the PSp component stabilizer acts through A5 and the PGSp extension through S5, with common kernel 16.',
      'boundary':'Exact finite permutation-module induction statement; no physical S5/A5 symmetry is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
