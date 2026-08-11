#!/usr/bin/env python3
"""Pass4875 — the quadratic Steiner->adjoint bridge is PGSp-odd.

Pass4870 proved
    dim Hom_PSp(Sym^2 H2,Q10)=2,
with both dimensions supported on the 2160-pair W33-adjacency lift.

Here the same orbit-stabilizer fixed-space calculation is repeated for the
full PGSp(4,3) action.  The 2160 relation remains one PGSp orbit, but its
stabilizer doubles from order 12 to 24 and fixes no nonzero vector of Q10.
Thus Hom_PGSp(Sym^2 H2,Q10)=0.

Since PGSp/PSp=C2 and char(F3)!=2, the induced outer involution on the
2-dimensional PSp-Hom space is semisimple with + eigenspace equal to the PGSp
Hom space.  Therefore it acts as -I on the entire quadratic-Hom space.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np,networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4875_PGSP_QUADRATIC_CHIRALITY.json'

def Q6(v):
    a,c,d,e,f,g=v; return (a*c+d*e+f+f*g+g)&1

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
        A[[r,q]]=A[[q,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        piv.append(c);r+=1
        if r==A.shape[0]:break
    return A,piv

def rank(M,p=3): return len(rref(M,p)[1])

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
    return 10-rank(np.vstack([(M-np.eye(10,dtype=int))%3 for M in mats]),3)

def pair_orbits(gens):
    seen=set();out=[]
    for p in itertools.combinations(range(120),2):
        if p in seen:continue
        O={p};seen.add(p);D=deque([p])
        while D:
            a=D.popleft()
            for op in gens:
                b=tuple(sorted((op[a[0]],op[a[1]])))
                if b not in O:O.add(b);seen.add(b);D.append(b)
        out.append(sorted(O))
    return sorted(out,key=len)

def main()->int:
    vecs=[v for v in itertools.product((0,1),repeat=6) if any(v)]
    sing=[v for v in vecs if Q6(v)==0];nons=[v for v in vecs if Q6(v)==1]
    assert (len(sing),len(nons))==(27,36)
    si={v:i for i,v in enumerate(sing)}
    trans=[]
    for v in nons:
        p=[]
        for x in sing:p.append(si[add2(x,v) if polar(x,v) else x])
        trans.append(tuple(p))

    gf=[];SFULL={tuple(range(27))}
    for g in trans:
        T=closure(gf+[g],27)
        if len(T)>len(SFULL):gf.append(g);SFULL=T
        if len(SFULL)==51840:break
    assert len(SFULL)==51840

    gp=[];SPART={tuple(range(27))}
    for g in [comp(trans[0],t) for t in trans[1:]]:
        T=closure(gp+[g],27)
        if len(T)>len(SPART):gp.append(g);SPART=T
        if len(SPART)==25920:break
    assert len(SPART)==25920

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
        if len(A|B)==12 and H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):DS.add(frozenset(A|B))
    DS=sorted(DS,key=lambda x:tuple(sorted(x)));assert len(DS)==36
    H36=nx.Graph();H36.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H36.add_edge(i,j)
    tri=[t for t in itertools.combinations(range(36),3) if all(H36.has_edge(*e) for e in itertools.combinations(t,2))]
    st=sorted(t for t in tri if len(DS[t[0]]&DS[t[1]]&DS[t[2]])==0);assert len(st)==120
    di={S:i for i,S in enumerate(DS)};sti={t:i for i,t in enumerate(st)}
    def steiner_perm(g):
        dp=[di[frozenset(g[x] for x in S)] for S in DS]
        return tuple(sti[tuple(sorted(dp[i] for i in t))] for t in st)
    PSp120=[steiner_perm(g) for g in gp]
    PGSp120=[steiner_perm(g) for g in gf]
    p_orbits=pair_orbits(PSp120);f_orbits=pair_orbits(PGSp120)
    assert [len(O) for O in p_orbits]==[120,1620,2160,3240]
    assert [len(O) for O in f_orbits]==[120,1620,2160,3240]

    # incidence-derived Q10 matrices, exactly as in Pass4870/4871
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
    QP=[qmat(g) for g in gp];QF=[qmat(g) for g in gf]

    # simultaneous PSp / PGSp action to read stabilizer fixed spaces
    def simultaneous(gens,perms,mats,target_order):
        I27=tuple(range(27));I120=tuple(range(120));I10=np.eye(10,dtype=np.int8)
        full={I27:(I120,I10)};Dq=deque([I27])
        while Dq:
            a=Dq.popleft();opa,Ma=full[a]
            for g,opg,Mg in zip(gens,perms,mats):
                z=comp(g,a)
                if z not in full:
                    full[z]=(comp(opg,opa),(Ma@Mg)%3);Dq.append(z)
        assert len(full)==target_order
        return full
    GP=simultaneous(gp,PSp120,QP,25920)
    GF=simultaneous(gf,PGSp120,QF,51840)

    def table(orbits,full):
        out=[]
        for O in orbits:
            rep=O[0];mats=[]
            for op,M in full.values():
                if tuple(sorted(op[i] for i in rep))==rep:mats.append(M)
            out.append({'orbit_size':len(O),'stabilizer_order':len(mats),'Q10_fixed_dimension':fixed_dim(mats)})
        return out
    tp=table(p_orbits,GP);tf=table(f_orbits,GF)
    assert [(x['orbit_size'],x['stabilizer_order'],x['Q10_fixed_dimension']) for x in tp]==[(120,216,0),(1620,16,0),(2160,12,2),(3240,8,0)]
    assert [(x['orbit_size'],x['stabilizer_order'],x['Q10_fixed_dimension']) for x in tf]==[(120,432,0),(1620,32,0),(2160,24,0),(3240,16,0)]

    # diagonal modules also contribute zero for both groups (point stabilizers)
    rep=0
    pdiag=[M for op,M in GP.values() if op[rep]==rep]
    fdiag=[M for op,M in GF.values() if op[rep]==rep]
    assert len(pdiag)==216 and fixed_dim(pdiag)==0
    assert len(fdiag)==432 and fixed_dim(fdiag)==0

    p_hom=2;f_hom=0
    # C2 quotient acts semisimply over F3; + eigenspace = PGSp Hom, hence +dim0,-dim2.
    out={
      'pass':4875,
      'PSp':{'order':25920,'quadratic_Hom_dimension':p_hom,'diagonal_fixed_dimension':0,'pair_orbits':tp},
      'PGSp':{'order':51840,'quadratic_Hom_dimension':f_hom,'diagonal_fixed_dimension':0,'pair_orbits':tf},
      'outer_C2_action_on_PSp_quadratic_Hom':{
        'dimension':2,'plus_eigenspace_dimension':0,'minus_eigenspace_dimension':2,
        'matrix_up_to_basis':'-I_2','reason':'PGSp/PSp=C2, char(F3)!=2, and the +1 eigenspace equals Hom_PGSp'},
      'selection_consequence':{
        'nonzero_PGSp_equivariant_quadratic_map_exists':False,
        'PSp_quadratic_maps_are_outer_odd':True,
        'projective_line_selected_by_outer_symmetry':False,
        'explanation':'multiplication by -1 fixes every 1D projective line setwise, so the outer involution imposes chirality/sign oddness but does not choose one of the projective quadratic channels'},
      'theorem':'The two-dimensional PSp-equivariant quadratic Steiner-to-adjoint Hom space is entirely odd under the outer PGSp/PSp involution. The full PGSp Hom space vanishes: the 2160-pair stabilizer doubles from order 12 to 24 and its Q10 fixed space drops from dimension 2 to 0, while all other orbit contributions remain zero. Since the quotient is C2 in characteristic three, the outer action on the PSp Hom space is exactly -I_2. Thus the quadratic bridge is chirality-odd; full PGSp symmetry forbids a nonzero invariant quadratic map, and the sign action still does not select a preferred projective channel.',
      'boundary':'Finite modular-representation selection rule. Chirality-odd means odd under the specific PGSp/PSp outer involution; it is not automatically the same as any spacetime parity or physical CP operation.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
