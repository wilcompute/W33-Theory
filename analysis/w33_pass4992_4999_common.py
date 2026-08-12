#!/usr/bin/env python3
"""Shared exact reconstruction for Passes 4992-4999.

Builds the cubic-surface 27-line geometry, 36 double-sixes/H36, the 45
tritangents, the standard W(3,3) point/line model and its 36 spreads, the E6
switching sign, the 1080 sigma-even triangle checks, and the residual 810
chordless A4 checks. Group actions are built only on request.
"""
from __future__ import annotations
import itertools
from collections import defaultdict, deque
import numpy as np
import networkx as nx


def Q6(v):
    a,c,d,e,f,g=v
    return (a*c+d*e+f+f*g+g)&1

def add2(a,b): return tuple(x^y for x,y in zip(a,b))
def polar(a,b): return Q6(add2(a,b))^Q6(a)^Q6(b)
def comp(p,q): return tuple(p[q[i]] for i in range(len(q)))

def closure(gens,n):
    I=tuple(range(n));S={I};D=deque([I])
    while D:
        a=D.popleft()
        for g in gens:
            z=comp(g,a)
            if z not in S:S.add(z);D.append(z)
    return S

def paired_closure(A,B,n,m):
    I=(tuple(range(n)),tuple(range(m)));S={I};D=deque([I])
    while D:
        a,b=D.popleft()
        for ga,gb in zip(A,B):
            z=(comp(ga,a),comp(gb,b))
            if z not in S:S.add(z);D.append(z)
    return S

def canon(v):
    for x in v:
        if x%3:
            z=1 if x%3==1 else 2
            return tuple((z*y)%3 for y in v)
    raise ValueError(v)

def sp(a,b):
    return (a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2])%3

def gf2_rank_int(rows):
    piv={}
    for x0 in rows:
        x=int(x0)
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def gf2_rank_matrix(M):
    rows=[]
    for row in np.asarray(M,dtype=np.uint8):
        x=0
        for i,b in enumerate(row):
            if int(b)&1:x|=1<<i
        rows.append(x)
    return gf2_rank_int(rows)

def mask_from_edges(edges,ei):
    m=0
    for e in edges:m|=1<<ei[tuple(sorted(e))]
    return m

def build_base():
    # Cubic surface: 27 lines, 45 tritangents, 36 double-sixes.
    vec=[v for v in itertools.product((0,1),repeat=6) if any(v)]
    sing=[v for v in vec if Q6(v)==0];nons=[v for v in vec if Q6(v)==1]
    qp=[sum(bit<<i for i,bit in enumerate(v)) for v in sing]
    p27=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    l27=[tuple(i for i,P in enumerate(p27) if x in P) for x in qp]
    G27=nx.Graph();G27.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if set(l27[i])&set(l27[j]):G27.add_edge(i,j)
    tritangents=sorted(t for t in itertools.combinations(range(27),3)
                       if all(G27.has_edge(*e) for e in itertools.combinations(t,2)))
    C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G27)) if len(c)==6]
    DS=set()
    for X,Y in itertools.combinations(C6,2):
        if X&Y:continue
        H=G27.subgraph(X|Y)
        if H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):
            DS.add(frozenset(X|Y))
    DS=sorted(DS,key=lambda s:tuple(sorted(s)));di={D:i for i,D in enumerate(DS)}
    # p27 is the 45 triple presentation; l27 is the 27 cubic-line incidence presentation.
    assert (len(l27),len(p27),len(tritangents),len(DS))==(27,45,45,36)

    H36=nx.Graph();H36.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H36.add_edge(i,j)
    E=sorted(tuple(sorted(e)) for e in H36.edges());ei={e:i for i,e in enumerate(E)}
    assert H36.number_of_edges()==360 and set(dict(H36.degree()).values())=={20}
    M=np.array([[1 if len(set(t)&set(D))==2 else 0 for D in DS] for t in tritangents],dtype=int)
    assert set(map(int,M.sum(1)))=={24} and set(map(int,M.sum(0)))=={30}

    # Standard W(3,3) points/lines and 36 spreads. Q is the line-intersection graph Q(4,3).
    P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    W=nx.Graph();W.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if sp(P[i],P[j])==0:W.add_edge(i,j)
    L=sorted(tuple(sorted(c)) for c in nx.find_cliques(W) if len(c)==4)
    assert len(L)==40
    Q=nx.Graph();Q.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if set(L[i])&set(L[j]):Q.add_edge(i,j)
    spreads=sorted([frozenset(c) for c in nx.find_cliques(nx.complement(Q)) if len(c)==10],
                   key=lambda s:tuple(sorted(s)))
    assert len(spreads)==36
    Hw=nx.Graph();Hw.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(spreads[i]&spreads[j])==1:Hw.add_edge(i,j)
    iso_ds_sp=next(nx.algorithms.isomorphism.GraphMatcher(H36,Hw).isomorphisms_iter())
    C=np.zeros((36,40),dtype=int)
    for d in range(36):C[d,list(spreads[iso_ds_sp[d]])]=1

    # E6 root signing sigma on the 360 H36 edges.
    Cartan=np.eye(6,dtype=int)*2
    for a,b in ((0,1),(1,2),(2,3),(3,4),(2,5)):Cartan[a,b]=Cartan[b,a]=-1
    def ref(v,i):
        v=np.array(v,dtype=int);w=v.copy();w[i]-=int(v@Cartan[:,i]);return tuple(map(int,w))
    roots={(1,0,0,0,0,0)};Dq=deque(roots)
    while Dq:
        v=Dq.popleft()
        for i in range(6):
            w=ref(v,i)
            if w not in roots:roots.add(w);Dq.append(w)
    pos=sorted(v for v in roots if all(x>=0 for x in v));assert len(pos)==36
    ER=nx.Graph();ER.add_nodes_from(range(36));ip={}
    for i,j in itertools.combinations(range(36),2):
        z=int(np.array(pos[i])@Cartan@np.array(pos[j]));ip[(i,j)]=z
        if abs(z)==1:ER.add_edge(i,j)
    iso_sign=next(nx.algorithms.isomorphism.GraphMatcher(H36,ER).isomorphisms_iter())
    sigma=np.zeros(360,dtype=np.uint8)
    for k,(a,b) in enumerate(E):
        i,j=sorted((iso_sign[a],iso_sign[b]));sigma[k]=int(ip[(i,j)]<0)

    # All H36 triangles, the 1080 sigma-even dual checks, and 120 Steiner triangles.
    triangles=sorted(t for t in itertools.combinations(range(36),3)
                     if all(H36.has_edge(*e) for e in itertools.combinations(t,2)))
    steiner=set(t for t in triangles if len(DS[t[0]]&DS[t[1]]&DS[t[2]])==0)
    tri_masks=[];tri_by_mask={}
    for t in triangles:
        idx=[ei[tuple(sorted(e))] for e in itertools.combinations(t,2)]
        if sum(int(sigma[k]) for k in idx)&1:continue
        m=sum(1<<k for k in idx);tri_masks.append(m);tri_by_mask[m]=t
    assert (len(triangles),len(steiner),len(tri_masks))==(1200,120,1080)
    assert gf2_rank_int(tri_masks)==324

    # Residual 810 sigma-even chordless four-cycles.
    cycles={}
    for V in itertools.combinations(range(36),4):
        for cyc in ((V[0],V[1],V[2],V[3]),(V[0],V[1],V[3],V[2]),(V[0],V[2],V[1],V[3])):
            es=[tuple(sorted((cyc[i],cyc[(i+1)%4]))) for i in range(4)]
            if all(H36.has_edge(*e) for e in es):cycles[tuple(sorted(ei[e] for e in es))]=frozenset(V)
    residual=[]
    for idx,V in cycles.items():
        if sum(int(sigma[k]) for k in idx)&1:continue
        chords=sum(H36.has_edge(*e) for e in itertools.combinations(V,2))-4
        if chords==0:residual.append((sum(1<<k for k in idx),V))
    assert len(residual)==810

    # Pass4989 base map: three residual equators over each intersecting tritangent pair.
    pair_to_res=defaultdict(list)
    for m,V in residual:
        cnt=M[:,list(V)].sum(1);z=tuple(map(int,np.flatnonzero(cnt==0)))
        assert len(z)==2;pair_to_res[z].append((m,V))
    assert len(pair_to_res)==270 and {len(v) for v in pair_to_res.values()}=={3}

    return dict(vec=vec,sing=sing,nons=nons,p27=p27,l27=l27,G27=G27,tritangents=tritangents,
                DS=DS,di=di,H36=H36,E=E,ei=ei,M=M,P=P,W=W,L=L,Q=Q,spreads=spreads,Hw=Hw,
                iso_ds_sp=iso_ds_sp,C=C,sigma=sigma,triangles=triangles,steiner=steiner,
                tri_masks=tri_masks,tri_by_mask=tri_by_mask,residual=residual,pair_to_res=pair_to_res)


def build_group(base):
    sing=base['sing'];nons=base['nons'];DS=base['DS'];di=base['di'];spreads=base['spreads']
    iso=base['iso_ds_sp'];L=base['L']
    si={v:i for i,v in enumerate(sing)}
    trans=[tuple(si[add2(x,v) if polar(x,v) else x] for x in sing) for v in nons]
    gp=[];S0={tuple(range(27))}
    for g in [comp(trans[0],t) for t in trans[1:]]:
        T=closure(gp+[g],27)
        if len(T)>len(S0):gp.append(g);S0=T
        if len(S0)==25920:break
    assert len(S0)==25920 and len(closure(gp+[trans[0]],27))==51840
    def dperm(g):return tuple(di[frozenset(g[x] for x in D)] for D in DS)
    DPp=[dperm(g) for g in gp];DPf=DPp+[dperm(trans[0])]
    inv={w:d for d,w in iso.items()}
    def tr(p):return tuple(iso[p[inv[w]]] for w in range(36))
    SpP=[tr(p) for p in DPp];SpF=[tr(p) for p in DPf]
    sig={frozenset(i for i,S in enumerate(spreads) if q in S):q for q in range(40)}
    def lp(s):return tuple(sig[frozenset(s[i] for i,S in enumerate(spreads) if q in S)] for q in range(40))
    LpP=[lp(s) for s in SpP];LpF=[lp(s) for s in SpF]
    PF=paired_closure(LpF,SpF,40,36);PP=paired_closure(LpP,SpP,40,36)
    assert (len(PF),len(PP))==(51840,25920)
    return dict(trans=trans,gp=gp,DPp=DPp,DPf=DPf,SpP=SpP,SpF=SpF,LpP=LpP,LpF=LpF,PF=PF,PP=PP)
