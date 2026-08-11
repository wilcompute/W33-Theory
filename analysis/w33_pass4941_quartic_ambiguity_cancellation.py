#!/usr/bin/env python3
"""Pass4941 — wedge the two quadratic Steiner->Q10 channels through the intrinsic bracket.

Pass4870 gives a two-dimensional PSp-equivariant quadratic Hom space and
Pass4875 proves the PGSp outer involution acts as -I on that whole plane.
Pass4871 gives the unique intrinsic PGSp-equivariant Lie bracket on Q10.
Therefore [q1(x),q2(x)] is a basis-independent (up to determinant) quartic
candidate whose two outer minus signs cancel.  This producer reconstructs the
maps, proves the operation is nonzero with full Q10 image, and verifies that
both quadratic channels vanish on the 40-dimensional fiber-constant subspace.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4941_QUARTIC_AMBIGUITY_CANCELLATION.json'
SEL=ROOT/'data/PART_W33_PASS4875_PGSP_QUADRATIC_CHIRALITY.json'

def Q6(v):
    a,c,d,e,f,g=v;return (a*c+d*e+f+f*g+g)&1
def add2(a,b):return tuple(x^y for x,y in zip(a,b))
def polar(a,b):return Q6(add2(a,b))^Q6(a)^Q6(b)
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def closure(gens,n=27):
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
def wedge(R):
    P=list(itertools.combinations(range(10),2));W=np.zeros((45,45),dtype=int)
    for a,(i,j) in enumerate(P):
        for b,(k,l) in enumerate(P):W[a,b]=(R[i,k]*R[j,l]-R[i,l]*R[j,k])%3
    return W
def hom_null(As,Bs):
    m=As[0].shape[0];n=Bs[0].shape[0];rows=[]
    for A,B in zip(As,Bs):
        for i in range(m):
            nz=np.flatnonzero(A[i])
            for j in range(n):
                z=np.zeros(m*n,dtype=int)
                for k in nz:z[k*n+j]=(z[k*n+j]+A[i,k])%3
                for l in range(n):
                    if B[l,j]:z[i*n+l]=(z[i*n+l]-B[l,j])%3
                rows.append(z)
    return null(np.array(rows,dtype=int),3)

def main()->int:
    prior=json.loads(SEL.read_text());assert prior['PSp_quadratic_Hom_dimension']==2 and prior['PGSp_quadratic_Hom_dimension']==0
    assert prior['outer_action']['matrix_up_to_basis']=='-I_2'
    vecs=[v for v in itertools.product((0,1),repeat=6) if any(v)]
    sing=[v for v in vecs if Q6(v)==0];nons=[v for v in vecs if Q6(v)==1];si={v:i for i,v in enumerate(sing)}
    trans=[tuple(si[add2(x,v) if polar(x,v) else x] for x in sing) for v in nons]
    gp=[];S={tuple(range(27))}
    for g in [comp(trans[0],t) for t in trans[1:]]:
        T=closure(gp+[g])
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
    DS=sorted(DS,key=lambda x:tuple(sorted(x)));di={S:i for i,S in enumerate(DS)};assert len(DS)==36
    H36=nx.Graph();H36.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H36.add_edge(i,j)
    st=sorted(t for t in itertools.combinations(range(36),3)
              if all(H36.has_edge(*e) for e in itertools.combinations(t,2))
              and len(DS[t[0]]&DS[t[1]]&DS[t[2]])==0);sti={t:i for i,t in enumerate(st)};assert len(st)==120
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
    R1,R2,R3,R4=sorted(orbits,key=len);assert len(R3)==2160
    FG=nx.Graph();FG.add_nodes_from(range(120));FG.add_edges_from(R1);fibers=[sorted(c) for c in nx.connected_components(FG)];assert len(fibers)==40
    fi={x:i for i,F in enumerate(fibers) for x in F};Q=nx.Graph();Q.add_nodes_from(range(40))
    for a,b in R3:Q.add_edge(fi[a],fi[b])

    # Reconstruct the incidence-derived Q10 generator action exactly as Pass4870/4871.
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
                    p=next(iter(set(lines[a])&set(lines[b])));v[lei[(p,a)]]=1;v[lei[(p,b)]]=2
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
    _,pc=rref(B64,3);Pi=invm(B64[:,pc],3);co=lambda v:(np.array(v,dtype=int)[pc]@Pi)%3
    point_lines=[frozenset(L for L,Ss in enumerate(lines) if p in Ss) for p in range(45)];pl={T:i for i,T in enumerate(point_lines)}
    def qmat(g):
        pg=[pl[frozenset(g[L] for L in T)] for T in point_lines];ep=[lei[(pg[p],g[L])] for p,L in ledges];R=np.zeros((64,64),dtype=int)
        for i,v in enumerate(B64):
            w=np.zeros(135,dtype=int)
            for j,x in enumerate(v):
                if x:w[ep[j]]=x
            R[i]=co(w)
        assert not np.any(R[:54,54:]);return R[54:,54:]%3
    QM=[qmat(g) for g in gp]
    # Simultaneous group action so stabilizer-fixed vectors propagate to all 2160 pairs.
    full={tuple(range(27)):(tuple(range(120)),np.eye(10,dtype=int))};Dg=deque(full)
    while Dg:
        a=Dg.popleft();opa,Ma=full[a]
        for gg,opg,Mg in zip(gp,SP,QM):
            z=comp(gg,a)
            if z not in full:full[z]=(comp(opg,opa),(Ma@Mg)%3);Dg.append(z)
    assert len(full)==25920
    rep=tuple(R3[0]);stab=[M for op,M in full.values() if tuple(sorted((op[rep[0]],op[rep[1]])))==rep]
    fix=null(np.vstack([(M.T-np.eye(10,dtype=int))%3 for M in stab]),3);assert fix.shape==(2,10)
    pair_to_M={}
    for op,M in full.values():
        p=tuple(sorted((op[rep[0]],op[rep[1]])));pair_to_M.setdefault(p,M)
    assert len(pair_to_M)==2160
    maps=[{p:(q@M)%3 for p,M in pair_to_M.items()} for q in fix]
    for opg,Mg in zip(SP,QM):
        for p in pair_to_M:
            pgp=tuple(sorted((opg[p[0]],opg[p[1]])))
            assert np.array_equal(maps[0][pgp],(maps[0][p]@Mg)%3)
            assert np.array_equal(maps[1][pgp],(maps[1][p]@Mg)%3)
    # Intrinsic bracket from the same Q10 action.
    HX=hom_null([wedge(A) for A in QM],QM);assert HX.shape==(1,450);X=HX[0].reshape(45,10)%3;assert rank(X,3)==10
    pairs10=list(itertools.combinations(range(10),2));pi={p:i for i,p in enumerate(pairs10)}
    def bb(i,j):
        if i==j:return np.zeros(10,dtype=int)
        return X[pi[(i,j)]].copy() if i<j else (-X[pi[(j,i)]])%3
    def br(a,b):
        z=np.zeros(10,dtype=int)
        for i,ai in enumerate(a):
            if ai:
                for j,bj in enumerate(b):
                    if bj:z=(z+ai*bj*bb(i,j))%3
        return z
    def qeval(supp,k):
        z=np.zeros(10,dtype=int)
        for a,b in itertools.combinations(supp,2):
            p=tuple(sorted((a,b)))
            if p in maps[k]:z=(z+maps[k][p])%3
        return z
    # q_i vanish on every fiber-constant vector because every adjacent 3x3 block sums to zero.
    block_zero=True
    for a,b in Q.edges():
        ps=[tuple(sorted((x,y))) for x in fibers[a] for y in fibers[b]]
        for k in (0,1):
            if np.any(np.sum([maps[k][p] for p in ps],axis=0)%3):block_zero=False
    assert block_zero
    # Two-support inputs give zero quartic output, but three-support inputs already span Q10.
    assert all(not np.any(br(maps[0][p],maps[1][p])%3) for p in R3)
    vals=[];witness=[]
    for supp in itertools.combinations(range(120),3):
        v=br(qeval(supp,0),qeval(supp,1))%3
        if np.any(v):
            vals.append(v);witness.append(list(supp))
            if rank(np.array(vals),3)==10:break
    assert rank(np.array(vals),3)==10
    out={'pass':4941,
      'inputs':{'PSp_quadratic_Hom_dimension':2,'PGSp_quadratic_Hom_dimension':0,
        'outer_action_on_quadratic_plane':'-I_2','intrinsic_bracket_Hom_dimension':1},
      'quartic_operation':{'formula':'F(x)=[q1(x),q2(x)]','homogeneous_degree':4,
        'change_of_quadratic_basis':'F scales by det of the GL2 basis change','PGSp_outer_parity':'even: two outer minus signs cancel',
        'nonzero':True,'image_span_dimension':10,'three_support_full_rank_witnesses':witness[-10:]},
      'support_structure':{'two_support_inputs_zero':True,
        'fiber_constant_40_space_annihilated_by_each_quadratic_channel':True,
        'reason':'for every W33 adjacency edge, the sum of each Q10-valued map over its complete 3x3 lift is zero in F3'},
      'theorem':'Let q1,q2 be any basis of the two-dimensional PSp-equivariant quadratic Steiner-to-adjoint Hom plane. The intrinsic Lie bracket defines the quartic F(x)=[q1(x),q2(x)]. Under a GL2 basis change F scales only by the determinant, so it is a canonical projective quartic line. The PGSp outer involution multiplies both qi by -1 and therefore fixes F. Direct exact evaluation finds three-support inputs whose quartic outputs span all ten dimensions of Q10, while every two-support input and the entire 40-dimensional fiber-constant subspace vanish. Thus the quadratic ambiguity cancels at degree four without selecting an arbitrary quadratic channel.',
      'boundary':'Finite characteristic-three polynomial-module theorem. Projective uniqueness still leaves an overall nonzero scalar and supplies no continuum normalization or physical coupling.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
