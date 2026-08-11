#!/usr/bin/env python3
"""Pass4942 — defining-characteristic degeneration of the Steiner 20+60 sectors.

Pass4874 gives the rational 4-class association scheme on 120 Steiner triangles.
This pass asks what its 40+80 fiber decomposition becomes over F3, the field
where the nonlinear Steiner->adjoint bridge lives.  Because each fiber has
size three, the fiber-sum operator becomes square-zero and the rational
20+60 transverse eigenvalues 9 and -3 both collapse to zero mod 3.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4942_TRANSVERSE_CHAR3_DEGENERATION.json'

def Q6(v):
    a,c,d,e,f,g=v;return (a*c+d*e+f+f*g+g)&1
def add2(a,b):return tuple(x^y for x,y in zip(a,b))
def polar(a,b):return Q6(add2(a,b))^Q6(a)^Q6(b)
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def closure(gens,n):
    I=tuple(range(n));S={I};D=deque([I])
    while D:
        a=D.popleft()
        for g in gens:
            z=comp(g,a)
            if z not in S:S.add(z);D.append(z)
    return S

def rankp(M,p=3):
    A=np.array(M,dtype=int)%p;r=0
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
        if r==A.shape[0]:break
    return r

def main()->int:
    vecs=[v for v in itertools.product((0,1),repeat=6) if any(v)]
    sing=[v for v in vecs if Q6(v)==0];nons=[v for v in vecs if Q6(v)==1];si={v:i for i,v in enumerate(sing)}
    trans=[]
    for v in nons:
        trans.append(tuple(si[add2(x,v) if polar(x,v) else x] for x in sing))
    gp=[];S={tuple(range(27))}
    for g in [comp(trans[0],t) for t in trans[1:]]:
        T=closure(gp+[g],27)
        if len(T)>len(S):gp.append(g);S=T
        if len(S)==25920:break
    assert len(S)==25920
    qp=[sum(bit<<i for i,bit in enumerate(v)) for v in sing]
    pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp]
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if set(lines[i])&set(lines[j]):G.add_edge(i,j)
    C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G)) if len(c)==6]
    DS=set()
    for A,B in itertools.combinations(C6,2):
        if A&B:continue
        H=G.subgraph(A|B)
        if H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):DS.add(frozenset(A|B))
    DS=sorted(DS,key=lambda x:tuple(sorted(x)));assert len(DS)==36
    H36=nx.Graph();H36.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H36.add_edge(i,j)
    tri=[t for t in itertools.combinations(range(36),3) if all(H36.has_edge(*e) for e in itertools.combinations(t,2))]
    st=sorted(t for t in tri if len(DS[t[0]]&DS[t[1]]&DS[t[2]])==0);assert len(st)==120
    di={S:i for i,S in enumerate(DS)};sti={t:i for i,t in enumerate(st)}
    SP=[]
    for g in gp:
        dp=[di[frozenset(g[x] for x in S)] for S in DS]
        SP.append(tuple(sti[tuple(sorted(dp[i] for i in t))] for t in st))
    seen=set();orbits=[]
    for p in itertools.combinations(range(120),2):
        if p in seen:continue
        O={p};seen.add(p);D=deque([p])
        while D:
            a=D.popleft()
            for op in SP:
                b=tuple(sorted((op[a[0]],op[a[1]])))
                if b not in O:O.add(b);seen.add(b);D.append(b)
        orbits.append(sorted(O))
    R1,R2,R3,R4=sorted(orbits,key=len);assert list(map(len,(R1,R2,R3,R4)))==[120,1620,2160,3240]
    mats=[]
    for O in (R1,R2,R3,R4):
        M=np.zeros((120,120),dtype=int)
        for i,j in O:M[i,j]=M[j,i]=1
        mats.append(M)
    A1,A2,A3,A4=mats;I=np.eye(120,dtype=int)
    N=(I+A1)%3
    assert rankp(N)==40 and rankp(N@N)==0
    ranks={
      'fiber_sum_N':[rankp(N),rankp(N@N)],
      'R2':[rankp(A2),rankp(A2@A2),rankp(A2@A2@A2)],
      'R3':[rankp(A3),rankp(A3@A3)],
      'R4':[rankp(A4),rankp(A4@A4),rankp(A4@A4@A4)]}
    assert ranks=={'fiber_sum_N':[40,0],'R2':[34,14,0],'R3':[39,0],'R4':[34,14,0]}
    # R2 has nilpotent Jordan type 3^14 2^6 1^66 from ranks 34,14,0.
    n3=ranks['R2'][1];n2=ranks['R2'][0]-2*n3;n1=120-3*n3-2*n2
    assert (n3,n2,n1)==(14,6,66)
    # The fiber-constant image C=im(N) lies inside ker(N), because 3=0.
    # A3 maps into C: rows are complete K3xK3 lifts of W33 adjacency.
    C=np.zeros((120,40),dtype=int)
    FG=nx.Graph();FG.add_nodes_from(range(120));FG.add_edges_from(R1)
    fibers=[sorted(c) for c in nx.connected_components(FG)];assert len(fibers)==40
    for j,F in enumerate(fibers):
        for x in F:C[x,j]=1
    assert rankp(C)==40 and rankp(np.c_[C,(A3%3)])==40
    # R2 restricted to C is W33 nonadjacency on the quotient and is square-zero rank14 mod3.
    M2=np.zeros((40,40),dtype=int)
    for j in range(40):
        y=(A2@C[:,j])%3
        for i,F in enumerate(fibers):
            vals={int(y[x]) for x in F};assert len(vals)==1;M2[i,j]=next(iter(vals))
    assert rankp(M2)==14 and rankp(M2@M2)==0
    out={
      'pass':4942,
      'characteristic_zero_input':{'fiber_constant_dimension':40,'transverse_dimension':80,
        'transverse_primitive_dimensions':[20,60],'R2_eigenvalues_on_transverse':[9,-3]},
      'characteristic_three':{
        'fiber_sum_operator':'N=I+R1 is block J3 on each classical Steiner triad',
        'N_rank':40,'N_square_zero':True,'image_dimension':40,'kernel_dimension':80,
        'image_contained_in_kernel':True,
        'R2_nilpotent_ranks':[34,14,0],'R2_Jordan_blocks':{'size3':14,'size2':6,'size1':66},
        'R3_nilpotent_rank':39,'R3_square_zero':True,
        'R2_on_fiber_constant_rank':14,'R2_on_fiber_constant_square_zero':True},
      'interpretation':'The rational 20+60 eigensplitting is not a direct-sum decomposition in defining characteristic. Because 9=-3=0 mod3 and every fiber has size3, the three-fiber layer becomes a nonsemisimple nilpotent filtration: im(N)_40 is contained in ker(N)_80, while R2 has Jordan type 3^14 2^6 1^66.',
      'theorem':'The 20+60 transverse sectors of the Steiner association scheme undergo an exact defining-characteristic collapse over F3. The fiber-sum operator N=I+R1 has rank40 and N^2=0, so the 40-dimensional fiber-constant module lies inside the 80-dimensional fiber-sum-zero module. The R2 operator, whose rational transverse eigenvalues are 9 and -3, becomes nilpotent of index three with ranks 34,14,0 and Jordan type 3^14 2^6 1^66. R3 is square-zero of rank39. Thus the characteristic-three nonlinear bridge lives on a nonsemisimple three-fiber extension, not on the rational 20 and 60 eigenspaces separately.',
      'boundary':'Exact finite association-module theorem. It identifies the characteristic-three degeneration; it does not assign particle multiplets or continuum fields to the 20- or 60-dimensional rational sectors.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
