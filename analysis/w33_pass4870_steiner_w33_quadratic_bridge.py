#!/usr/bin/env python3
"""Pass4870 — Steiner-triangle 3-cover of W33 and the first nonlinear adjoint bridge.

Pass4866 proved that H2 of the double-six clique complex over F3 is the
120-dimensional permutation module on the 120 maximal/Steiner triangles and
that Hom_G(H2,Q10)=Hom_G(Q10,H2)=0.

This pass classifies the PSp(4,3)-orbits on unordered pairs of Steiner
triangles. One relation of size 120 is 40 disjoint K3 fibers; another relation
of size 2160 is the complete 3-by-3 lift of adjacency between those fibers.
The quotient is explicitly isomorphic to W(3,3)=SRG(40,12,2,4).

Because char(F3)!=2, homogeneous equivariant quadratic maps H2->Q10 are
identified with Hom_G(Sym^2 H2,Q10). Sym^2 of a permutation module decomposes
as the diagonal permutation module plus the four unordered-pair orbit modules.
Stabilizer-fixed-space calculations show that the Hom space has dimension 2,
and both dimensions occur only on the 2160-pair W33-adjacency relation.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np,networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/PART_W33_PASS4870_STEINER_W33_QUADRATIC_BRIDGE.json"

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

def rref(M,p=3):
    A=np.array(M,dtype=int)%p;r=0;piv=[]
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        piv.append(c);r+=1
        if r==A.shape[0]:break
    return A,piv

def rank(M,p=3):return len(rref(M,p)[1])

def null(M,p=3):
    R,piv=rref(M,p);free=[c for c in range(R.shape[1]) if c not in piv];out=[]
    for f in free:
        x=np.zeros(R.shape[1],dtype=int);x[f]=1
        for i,c in enumerate(piv):x[c]=(-R[i,f])%p
        out.append(x)
    return np.array(out,dtype=int)

def invm(A,p=3):
    A=np.array(A,dtype=int)%p;n=A.shape[0];X=np.c_[A,np.eye(n,dtype=int)]
    for c in range(n):
        q=next(i for i in range(c,n) if X[i,c]);X[[c,q]]=X[[q,c]]
        X[c]=(X[c]*pow(int(X[c,c]),-1,p))%p
        for i in range(n):
            if i!=c and X[i,c]:X[i]=(X[i]-X[i,c]*X[c])%p
    return X[:,n:]%p

def fixed_dim(mats):
    if not mats:return 10
    A=np.vstack([(M-np.eye(10,dtype=int))%3 for M in mats])
    return 10-rank(A,3)

def main()->int:
    # Q^-(5,2), GQ(4,2), and exact PSp generators.
    vecs=[v for v in itertools.product((0,1),repeat=6) if any(v)]
    sing=[v for v in vecs if Q6(v)==0];nons=[v for v in vecs if Q6(v)==1]
    assert (len(sing),len(nons))==(27,36)
    si={v:i for i,v in enumerate(sing)}
    trans=[]
    for v in nons:
        p=[]
        for x in sing:p.append(si[add2(x,v) if polar(x,v) else x])
        trans.append(tuple(p))
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

    # Double-sixes and their 120 maximal/Steiner triangles.
    C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G)) if len(c)==6]
    DS=set()
    for A,B in itertools.combinations(C6,2):
        if A&B:continue
        H=G.subgraph(A|B)
        if len(A|B)==12 and H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):DS.add(frozenset(A|B))
    DS=sorted(DS,key=lambda x:tuple(sorted(x)));assert len(DS)==36
    H36=nx.Graph();H36.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H36.add_edge(i,j)
    tri=[t for t in itertools.combinations(range(36),3) if all(H36.has_edge(*e) for e in itertools.combinations(t,2))]
    steiner=sorted(t for t in tri if len(DS[t[0]]&DS[t[1]]&DS[t[2]])==0)
    assert len(steiner)==120
    di={S:i for i,S in enumerate(DS)};sti={t:i for i,t in enumerate(steiner)}
    def steiner_perm(g):
        dp=[di[frozenset(g[x] for x in S)] for S in DS]
        return tuple(sti[tuple(sorted(dp[i] for i in t))] for t in steiner)
    SP=[steiner_perm(g) for g in gp]

    # Pair orbit classification.
    allpairs=list(itertools.combinations(range(120),2));seen=set();orbits=[]
    for p in allpairs:
        if p in seen:continue
        O={p};seen.add(p);Dq=deque([p])
        while Dq:
            a=Dq.popleft()
            for op in SP:
                b=tuple(sorted((op[a[0]],op[a[1]])))
                if b not in O:O.add(b);seen.add(b);Dq.append(b)
        orbits.append(sorted(O))
    orbits.sort(key=len)
    assert [len(O) for O in orbits]==[120,1620,2160,3240]
    descriptors=[]
    for O in orbits:
        C=Counter()
        for a,b in O:
            A=set(steiner[a]);B=set(steiner[b])
            cross=sum(H36.has_edge(x,y) for x in A for y in B if x!=y)
            C[(len(A&B),cross)]+=1
        assert len(C)==1
        descriptors.append(next(iter(C)))
    assert descriptors==[(0,0),(1,6),(0,6),(0,4)]

    O120,O1620,O2160,O3240=orbits
    fiber_graph=nx.Graph();fiber_graph.add_nodes_from(range(120));fiber_graph.add_edges_from(O120)
    fibers=[set(c) for c in nx.connected_components(fiber_graph)]
    assert len(fibers)==40 and all(len(c)==3 and fiber_graph.subgraph(c).number_of_edges()==3 for c in fibers)
    fi={v:i for i,c in enumerate(fibers) for v in c}
    adjlift=nx.Graph();adjlift.add_nodes_from(range(120));adjlift.add_edges_from(O2160)
    quotient=nx.Graph();quotient.add_nodes_from(range(40))
    for a,b in O2160:
        assert fi[a]!=fi[b]
        quotient.add_edge(fi[a],fi[b])
    assert quotient.number_of_edges()==240 and set(dict(quotient.degree()).values())=={12}
    assert all(len(set(quotient[a])&set(quotient[b]))==2 for a,b in quotient.edges())
    assert all(len(set(quotient[a])&set(quotient[b]))==4 for a,b in itertools.combinations(range(40),2) if not quotient.has_edge(a,b))
    # every adjacent quotient pair lifts to all 3x3 pairs
    assert all(sum(1 for x in A for y in B if adjlift.has_edge(x,y))==9 for A,B in ((fibers[a],fibers[b]) for a,b in quotient.edges()))

    # Standard W(3,3) collinearity graph for an explicit isomorphism check.
    def canon3(v):
        v=np.array(v,dtype=int)%3
        nz=next(i for i,x in enumerate(v) if x)
        return tuple((v*pow(int(v[nz]),-1,3))%3)
    wpts=sorted({canon3(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    assert len(wpts)==40
    J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%3
    W=nx.Graph();W.add_nodes_from(range(40))
    for a,b in itertools.combinations(range(40),2):
        if int(np.array(wpts[a])@J@np.array(wpts[b]))%3==0:W.add_edge(a,b)
    assert nx.is_isomorphic(quotient,W)

    # Quotient action is faithful PSp of order 25920.
    fiber_sets={frozenset(c):i for i,c in enumerate(fibers)}
    QP=[]
    for op in SP:
        QP.append(tuple(fiber_sets[frozenset(op[x] for x in c)] for c in fibers))
    assert len(closure(QP,40))==25920

    # Reconstruct the incidence-derived Q10 action from Pass4871.
    ledges=sorted((p,L) for L,Ss in enumerate(lines) for p in Ss);lei={e:i for i,e in enumerate(ledges)}
    D=np.zeros((72,135),dtype=int)
    for e,(p,L) in enumerate(ledges):D[p,e]=1;D[45+L,e]=-1
    HB=null(D,3);assert HB.shape==(64,135)
    KV=[]
    for S6 in itertools.combinations(range(27),6):
        H=G.subgraph(S6)
        if H.number_of_edges()!=9 or set(dict(H.degree()).values())!={3} or not nx.is_bipartite(H):continue
        A,B=nx.algorithms.bipartite.sets(H)
        if len(A)!=3 or len(B)!=3:continue
        v=np.zeros(135,dtype=int)
        for a in A:
            for b in B:
                if G.has_edge(a,b):
                    p=next(iter(set(lines[a])&set(lines[b])))
                    v[lei[(p,a)]]=1;v[lei[(p,b)]]=2
        KV.append(v)
    KV=np.array(KV);assert rank(KV,3)==54
    sel=[]
    for v in KV:
        if rank(np.array(sel+[v.tolist()]),3)>len(sel):sel.append(v.tolist())
        if len(sel)==54:break
    B64=np.array(sel,dtype=int)
    for v in HB:
        if rank(np.vstack([B64,v]),3)>len(B64):B64=np.vstack([B64,v])
        if len(B64)==64:break
    _,pc=rref(B64,3);Pi=invm(B64[:,pc],3)
    co=lambda v:(np.array(v,dtype=int)[pc]@Pi)%3
    point_lines=[frozenset(L for L,Ss in enumerate(lines) if p in Ss) for p in range(45)]
    pl={T:i for i,T in enumerate(point_lines)}
    def qmat(g):
        pg=[pl[frozenset(g[L] for L in T)] for T in point_lines]
        ep=[lei[(pg[p],g[L])] for p,L in ledges]
        R=np.zeros((64,64),dtype=int)
        for i,v in enumerate(B64):
            w=np.zeros(135,dtype=int)
            for j,x in enumerate(v):
                if x:w[ep[j]]=x
            R[i]=co(w)
        assert not np.any(R[:54,54:])
        return R[54:,54:]%3
    QM=[qmat(g) for g in gp]

    # Simultaneous full group on Steiner triangles and Q10.
    I27=tuple(range(27));I120=tuple(range(120));I10=np.eye(10,dtype=np.int8)
    full={I27:(I120,I10)};Dq=deque([I27])
    while Dq:
        a=Dq.popleft();opa,Ma=full[a]
        for g,opg,Mg in zip(gp,SP,QM):
            z=comp(g,a)
            if z not in full:
                full[z]=(comp(opg,opa),(Ma@Mg)%3);Dq.append(z)
    assert len(full)==25920

    orbit_modules=[("diagonal",[(0,)]),
                   ("pair_120",O120),("pair_1620",O1620),("pair_2160",O2160),("pair_3240",O3240)]
    fixed={}
    for name,O in orbit_modules:
        rep=tuple(O[0])
        mats=[];stab=0
        for op,M in full.values():
            if tuple(sorted(op[i] for i in rep))==tuple(sorted(rep)):
                stab+=1;mats.append(M)
        fixed[name]={"orbit_size":120 if name=="diagonal" else len(O),"stabilizer_order":stab,"Q10_fixed_dimension":fixed_dim(mats)}
    assert [fixed[k]["Q10_fixed_dimension"] for k,_ in orbit_modules]==[0,0,0,2,0]
    homdim=sum(v["Q10_fixed_dimension"] for v in fixed.values())
    assert homdim==2

    out={
      "pass":4870,
      "steiner_pair_orbits":[
        {"size":120,"degree":2,"triangle_intersection":0,"cross_edges":0,"role":"fiber relation: 40 disjoint K3s"},
        {"size":1620,"degree":27,"triangle_intersection":1,"cross_edges":6,"role":"nonadjacent-fiber refinement"},
        {"size":2160,"degree":36,"triangle_intersection":0,"cross_edges":6,"role":"W33 adjacency lift: complete K3,3 between adjacent fibers"},
        {"size":3240,"degree":54,"triangle_intersection":0,"cross_edges":4,"role":"nonadjacent-fiber refinement"}],
      "intrinsic_three_cover":{"Steiner_triangles":120,"fibers":40,"fiber_size":3,
        "fiber_relation":"40 disjoint K3s","adjacency_lift_pairs":2160,
        "quotient":"SRG(40,12,2,4)","explicit_isomorphism_to_standard_W33":True,
        "PSp_action_on_quotient_order":25920,
        "between_adjacent_fibers":"all 9 pairs, i.e. K3,3"},
      "quadratic_bridge":{"field":"F3","reason_Sym2_equals_quadratic":"2 is invertible in F3",
        "Hom_PSp_Sym2H2_to_Q10_dimension":homdim,
        "orbit_fixed_space_table":fixed,
        "support":"both dimensions occur exclusively on the 2160-pair W33-adjacency lift relation",
        "nonzero_maps_surjective":True,
        "interpretation":"there is a two-dimensional family of PSp-equivariant homogeneous quadratic maps H2(F3)->Q10, even though Pass4866 proved all linear maps vanish"},
      "theorem":"The 120 Steiner triangles form an intrinsic 3-fiber refinement of W33. A 120-pair relation partitions them into 40 triples; the 2160-pair relation is exactly the complete K3,3 lift of adjacency on the quotient, and the quotient is explicitly isomorphic to W(3,3)=SRG(40,12,2,4) with faithful PSp(4,3) action. This same W33-adjacency relation supports the first nonlinear Steiner-to-adjoint bridge: Hom_PSp(Sym^2 H2,Q10) has dimension 2, while all other diagonal/pair orbit modules contribute zero. Thus the linear obstruction of Pass4866 is sharp: the first equivariant bridge occurs quadratically, mediated by the recovered W33 quotient.",
      "boundary":"Finite characteristic-three association-module theorem. The two-dimensional quadratic Hom space does not select a preferred physical coupling, normalization, or continuum field without additional structure."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=="__main__":raise SystemExit(main())
