#!/usr/bin/env python3
"""Pass 4482 -- optimal ten-line protected software readout.

Pass-4507 hardening correction: the previously frozen SELECTED list had drifted
from the current canonical W33 line ordering and no longer passed this script's
own Gram/P4+3K2 assertions.  The replacement below is recomputed directly in the
current geometry and again realizes the six-intersection optimum.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from w33_pass4461_line_signing_apartment_trace import geometry, simple_four_cycles
from w33_pass4463_apartment_parity_tomography import rank_mod2
from w33_pass4469_apartment_css_h10_intertwiner import nullspace_mod2, rref_rows

ROOT=Path(__file__).resolve().parents[1]
SELECTED=[0,1,4,10,17,18,22,24,26,31]
def inv2(M):
    M=np.asarray(M,dtype=np.uint8); n=len(M); A=np.hstack((M.copy(),np.eye(n,dtype=np.uint8)))
    for c in range(n):
        r=next(i for i in range(c,n) if A[i,c]); A[[c,r]]=A[[r,c]]
        for i in range(n):
            if i!=c and A[i,c]: A[i]^=A[c]
    return A[:,n:]
def compatible(e,f,A):
    if len(set(e+f))<4:return False
    return not any(A[u,v] for u in e for v in f)
def clique_target(edges,adj,target):
    def rec(cand,chosen):
        if len(chosen)==target:return chosen
        if len(cand)<target-len(chosen):return None
        while len(cand)>=target-len(chosen):
            v=cand[0]; rest=cand[1:]; hit=rec([u for u in rest if u in adj[v]],chosen+[v])
            if hit is not None:return hit
            cand=rest
        return None
    return rec(list(range(len(edges))),[])
def main():
    _,lines,A,N0,edge_line=geometry(); N=(N0%2).astype(np.uint8); Ast=(N.T@N)%2
    aps=[frozenset(edge_line[e] for e in c) for c in simple_four_cycles(A)]; H=np.zeros((40,len(aps)),dtype=np.uint8)
    for j,S in enumerate(aps):H[list(S),j]=1
    C=rref_rows(nullspace_mod2(N.T)); K=nullspace_mod2(Ast); radical=rref_rows(np.asarray([(H.T@k)%2 for k in K],dtype=np.uint8))
    G=Ast[np.ix_(SELECTED,SELECTED)]; X=N[:,SELECTED].T; B=H[SELECTED]
    deg=sorted(map(int,G.sum(1))); edges=int(G.sum()//2)
    unseen=set(range(10)); comps=[]
    while unseen:
        s=min(unseen); comp={s}; Q=[s]
        while Q:
            v=Q.pop()
            for w in np.flatnonzero(G[v]):
                w=int(w)
                if w not in comp:comp.add(w);Q.append(w)
        unseen-=comp; comps.append(len(comp))
    comps.sort()
    dual=[(i,j) for i in range(40) for j in range(i+1,40) if Ast[i,j]]; adj=[set() for _ in dual]
    for i in range(len(dual)):
        for j in range(i+1,len(dual)):
            if compatible(dual[i],dual[j],Ast):adj[i].add(j);adj[j].add(i)
    m5=clique_target(dual,adj,5); m4=clique_target(dual,adj,4); Gi=inv2(G)
    recovered=True
    for m in range(1<<10):
        c=np.array([(m>>i)&1 for i in range(10)],dtype=np.uint8); y=(c@B)%2; p=(y@B.T)%2
        if not np.array_equal((p@Gi)%2,c):recovered=False;break
    checks={'gram_rank10':rank_mod2(G)==10,'basis_P4_3K2':edges==6 and comps==[2,2,2,4] and deg==[1]*8+[2]*2,
      'logical_basis':rank_mod2(np.vstack((C,X)))==25,'apartment_basis':rank_mod2(np.vstack((radical,B)))==39,
      'weights':all(int(v.sum())==4 for v in X) and all(int(v.sum())==162 for v in B),'dual_edges240':len(dual)==240,
      'no_induced_matching5':m5 is None,'induced_matching4_exists':m4 is not None,'inverse':np.array_equal((G@Gi)%2,np.eye(10,dtype=np.uint8)),
      'radical_orthogonal':not np.any((radical@B.T)%2),'all1024_recovered':recovered}
    assert all(checks.values()),checks
    out={'pass':4482,'status':'REPAIRED_BY_PASS4507','theorem':'W33 optimal ten-line protected software readout theorem','selected_line_indices':SELECTED,
      'basis_graph':{'type':'P4 disjoint-union 3K2','edges':6,'maximum_induced_matching':4,'minimum_intersections':6},
      'readout':{'bits':10,'formula':'p_i=<y,g_i>; c=p G^{-1}','all_1024_classes_verified':True,'each_g_i_weight':162},
      'erratum':'The former frozen index list [1,5,14,15,19,23,24,33,35,39] had drifted and is superseded by the current canonical-basis list.',
      'boundary':'Ten bits are software parity post-processing of acquired apartment data, not ten physical apartment measurements or an optical-cost optimum.',
      'checks':{'passed':sum(checks.values()),'total':len(checks)}}
    p=ROOT/'data/PART_W33_PASS4482_TEN_LINE_PROTECTED_READOUT.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
