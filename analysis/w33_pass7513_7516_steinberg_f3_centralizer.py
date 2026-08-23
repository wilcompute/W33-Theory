#!/usr/bin/env python3
"""Pass7513-7516: defining-characteristic Schur test for the explicit Steinberg map."""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np,networkx as nx
from sympy.combinatorics import Permutation,PermutationGroup
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E
from analysis.w33_pass7509_7516_steinberg_global_intertwiner import build_T
OUT=ROOT/'data/PART_W33_PASS7513_7516_STEINBERG_F3_CENTRALIZER.json'

def inv_mod(A,p):
    A=np.asarray(A,dtype=np.int64)%p;n=A.shape[0];B=np.concatenate([A.copy(),np.eye(n,dtype=np.int64)],1);r=0
    for c in range(n):
        nz=np.flatnonzero(B[r:,c]);assert len(nz);z=r+int(nz[0]);B[[r,z]]=B[[z,r]]
        B[r]=(B[r]*pow(int(B[r,c]),-1,p))%p
        rows=np.flatnonzero(B[:,c]);rows=rows[rows!=r]
        if len(rows):B[rows]=(B[rows]-B[rows,c,None]*B[r])%p
        r+=1
    assert np.array_equal(B[:,:n],np.eye(n,dtype=np.int64)%p);return B[:,n:]%p

def basis_indices(A,p,target):
    A=np.asarray(A,dtype=np.int64).copy()%p;m,n=A.shape;r=0;orig=list(range(m));inds=[]
    for c in range(n):
        nz=np.flatnonzero(A[r:,c])
        if len(nz)==0:continue
        z=r+int(nz[0]);A[[r,z]]=A[[z,r]];orig[r],orig[z]=orig[z],orig[r]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        rows=np.flatnonzero(A[:,c]);rows=rows[rows!=r]
        if len(rows):A[rows]=(A[rows]-A[rows,c,None]*A[r])%p
        inds.append(orig[r]);r+=1
        if r==target:break
    return inds

def canon(v):
    for x in v:
        if x%3:
            c=1 if x%3==1 else 2;return tuple((c*y)%3 for y in v)
    raise ValueError

def std_w33_generators():
    pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)});pi={p:i for i,p in enumerate(pts)}
    def sp(x,y):return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3
    G=nx.Graph();G.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if sp(pts[i],pts[j])==0:G.add_edge(i,j)
    def trans(v):
        out=[]
        for x in pts:
            w=sp(x,v);out.append(pi[canon(tuple((x[k]+w*v[k])%3 for k in range(4)))])
        return tuple(out)
    chosen=[];grp=PermutationGroup([Permutation(list(range(40)))])
    for p in [trans(v) for v in pts]:
        H=PermutationGroup([Permutation(x) for x in chosen+[p]])
        if H.order()>grp.order():chosen.append(p);grp=H
        if grp.order()==25920:break
    assert grp.order()==25920 and len(chosen)==5
    return G,chosen

def main():
    R,A2,J,base,bl,AO,lab,edges,L,P,T,maps=build_T();p=3;Tm=T%p
    cols=basis_indices(Tm.T,p,81);B=Tm[:,cols];rows=basis_indices(B,p,81);Binv=inv_mod(B[rows,:],p)
    Gstd,stdgens=std_w33_generators();Gbase=nx.Graph();Gbase.add_nodes_from(range(40));Gbase.add_edges_from(edges)
    gm=next(nx.algorithms.isomorphism.GraphMatcher(Gbase,Gstd).isomorphisms_iter());invgm={v:k for k,v in gm.items()}
    basegens=[tuple(invgm[s[gm[i]]] for i in range(40)) for s in stdgens];eidx={e:i for i,e in enumerate(edges)};reps=[]
    for g in basegens:
        Q=np.zeros((240,240),dtype=np.int8)
        for j,(a,b) in enumerate(edges):
            ga,gb=g[a],g[b]
            if ga<gb:i=eidx[(ga,gb)];sgn=1
            else:i=eidx[(gb,ga)];sgn=-1
            Q[i,j]=sgn
        QB=(Q.astype(np.int64)@B)%p;Rg=(Binv@QB[rows,:])%p;assert np.array_equal((B@Rg)%p,QB);reps.append(Rg)
    n=81;v=np.zeros(n,dtype=np.int64);v[0]=1;Bcyc=np.zeros((n,0),dtype=np.int64);words=[];cand=[np.eye(n,dtype=np.int64)]
    while cand and Bcyc.shape[1]<n:
        W=cand.pop(0);x=(W@v)%p
        if E.rank_mod(np.column_stack([Bcyc,x]),p)>Bcyc.shape[1]:
            Bcyc=np.column_stack([Bcyc,x]);words.append(W)
            for S in reps:cand.append((S@W)%p)
    assert Bcyc.shape[1]==81;Bci=inv_mod(Bcyc,p);blocks=[]
    for S in reps:
        for k,W in enumerate(words):
            coeff=(Bci@(S@Bcyc[:,k]))%p;Q=(S@W)%p
            for l,c in enumerate(coeff):
                if c:Q=(Q-int(c)*words[l])%p
            blocks.append(Q)
    Cmat=np.vstack(blocks)%p;rank=E.rank_mod(Cmat,p);assert rank==80 and np.all((Cmat@v)%p==0)
    out={'schema':'w33.pass7513_7516.steinberg_f3_centralizer.v1','status':'PASS','passes':'7513-7516',
      'PSp4_3_generator_count':len(reps),'generator_orders':[int(Permutation(g).order()) for g in basegens],
      'Steinberg_dimension':81,'cyclic_orbit_basis_dimension':81,'commutant_constraint_shape':list(Cmat.shape),
      'constraint_rank_F3':rank,'centralizer_dimension_F3':1,
      'conclusion':'The explicit characteristic-3 Steinberg image has scalar commutant only. Together with irreducibility/BT861 this is the full defining-characteristic Schur channel; its generated endomorphism algebra is End_F3(V_81).',
      'operator_algebra_dimension':6561,'boundary':'Finite modular representation theorem only.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','centralizer_dim_F3':1,'operator_algebra_dim':6561}))
if __name__=='__main__':main()
