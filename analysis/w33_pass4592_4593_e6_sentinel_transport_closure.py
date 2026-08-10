#!/usr/bin/env python3
"""Passes 4592-4593 -- close the 45-carrier and rank-15 transport frontiers.

4592 constructs an explicit PSp(4,3)-equivariant bijection between the 45
Pass4585 singular-support lines and the older 45 center-quad quotient points.
Under that bijection the Pass4586 SRG(45,32,22,24) is exactly the old
center-quad transport/complement graph.

4593 then identifies the *matrix*, not only its row graph.  After the same row
bijection, the 45x40 Pass4586 polar-transport matrix is exactly the old
center-quad 8-point support-incidence matrix.  Modulo two its row span is the
sentinel C=ker(N^T)=[40,15,8], and its 45 rows are all 45 minimum-weight words.
"""
from __future__ import annotations
import itertools, json
from collections import defaultdict, deque, Counter
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import (
    build_geometry, build_line_perm, transvection_matrix, norm3
)

ROOT=Path(__file__).resolve().parents[1]
OUT92=ROOT/'data/PART_W33_PASS4592_EXPLICIT_45_E6_INTERTWINER.json'
OUT93=ROOT/'data/PART_W33_PASS4593_SENTINEL_MINIMUM_SHELL_TRANSPORT.json'

def rank2(M):
    A=np.asarray(M,dtype=np.uint8).copy();r=0
    for c in range(A.shape[1]):
        z=np.flatnonzero(A[r:,c])
        if not len(z):continue
        k=r+int(z[0]);A[[r,k]]=A[[k,r]]
        for i in np.flatnonzero(A[:,c]):
            if i!=r:A[i]^=A[r]
        r+=1
        if r==A.shape[0]:break
    return r

def rbasis(xs):
    piv={}
    for x in map(int,xs):
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return list(piv.values())
def span(B):
    S=[0]
    for b in B:S += [x^b for x in list(S)]
    return S

def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def pair_group(gens):
    ip=tuple(range(40)); il=tuple(range(40)); seen={(ip,il)};Q=deque([(ip,il)])
    while Q:
        a,b=Q.popleft()
        for gp,gl in gens:
            z=(compose(gp,a),compose(gl,b))
            if z not in seen:seen.add(z);Q.append(z)
    return seen

def point_perm(M,pts,pidx):
    out=[]
    for p in pts:
        y=(np.asarray(M,dtype=int)@np.asarray(p,dtype=int))%3
        out.append(pidx[norm3(tuple(map(int,y)))])
    return tuple(out)

def mask_image(S,p):return frozenset(p[i] for i in S)

def center_quad_45(Apoint):
    nb=[set(np.flatnonzero(Apoint[i]).tolist()) for i in range(40)]
    quads=set()
    for a,b,c in itertools.combinations(range(40),3):
        if Apoint[a,b] or Apoint[a,c] or Apoint[b,c]:continue
        X=frozenset(nb[a]&nb[b]&nb[c])
        if len(X)==4:quads.add(X)
    quads=sorted(quads,key=lambda x:tuple(sorted(x)));assert len(quads)==90
    qidx={q:i for i,q in enumerate(quads)};pair={}
    for i,q in enumerate(quads):
        X=frozenset(set.intersection(*(nb[v] for v in q)));assert len(X)==4
        pair[i]=qidx[X]
    seen=set();supports=[]
    for i in range(90):
        P=tuple(sorted((i,pair[i])))
        if P in seen:continue
        seen.add(P); U=frozenset(quads[P[0]]|quads[P[1]]);assert len(U)==8;supports.append(U)
    supports=sorted(supports,key=lambda x:tuple(sorted(x)));assert len(supports)==45
    # dual GQ(4,2) lines are five disjoint 8-supports partitioning all 40 points.
    lines=[]
    for C in itertools.combinations(range(45),5):
        U=set();ok=True
        for i in C:
            if U & supports[i]:ok=False;break
            U |= set(supports[i])
        if ok and len(U)==40:lines.append(C)
    assert len(lines)==27
    A=np.zeros((45,45),dtype=np.uint8)
    for L in lines:
        for i,j in itertools.combinations(L,2):A[i,j]=A[j,i]=1
    return supports,A,np.ones((45,45),dtype=np.uint8)^np.eye(45,dtype=np.uint8)^A

def build_new(Astar,lines,aps):
    j=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    edges=[(i,k) for i in range(40) for k in range(i+1,40) if Astar[i,k]]
    V=set(span(rbasis([cols[i]^cols[k] for i,k in edges])));assert len(V)==512 and j in V
    rep=lambda x:min(int(x),int(x)^j); q=lambda x:(rep(x).bit_count()//4)&1
    polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    fibers=defaultdict(list)
    for ap in aps:
        x=0
        for i in ap:x^=cols[int(i)]
        fibers[rep(x)].append(tuple(map(int,ap)))
    st=defaultdict(list)
    for s,F in fibers.items():st[frozenset().union(*(set(ap) for ap in F))].append(s)
    new_supports=sorted(st,key=lambda U:tuple(sorted(U)));assert len(new_supports)==45
    singular_lines=[tuple(sorted(st[U])) for U in new_supports]
    anis=[]
    for p in range(40):
        L=sorted(i for i,L in enumerate(lines) if p in L);assert len(L)==4
        a,b,c,d=L; vals=[]
        for (u,v),(w,z) in [((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))]:
            x=rep(cols[u]^cols[v]);assert x==rep(cols[w]^cols[z]);vals.append(x)
        anis.append(tuple(sorted(vals)))
    T=np.zeros((45,40),dtype=np.uint8)
    for i,S in enumerate(singular_lines):
        for p,A in enumerate(anis):
            if all(polar(s,a)==0 for s in S for a in A):T[i,p]=1
    assert set(map(int,T.sum(1)))=={8} and set(map(int,T.sum(0)))=={9} and rank2(T)==15
    return new_supports,T

def main():
    pts,pidx,lines,lidx,Apoint,Astar,_,aps,_=build_geometry();Apoint=np.asarray(Apoint,dtype=np.uint8);Astar=np.asarray(Astar,dtype=np.uint8)
    old_supports,Aold,old_transport=center_quad_45(Apoint)
    new_supports,T=build_new(Astar,lines,aps)
    # paired point/line PSp action.
    gens=[];G={(tuple(range(40)),tuple(range(40)))}
    for v in pts:
        M=transvection_matrix(v); gp=point_perm(M,pts,pidx);gl=build_line_perm(M,pts,pidx,lines,lidx)
        trial=pair_group(gens+[(gp,gl)])
        if len(trial)>len(G):gens.append((gp,gl));G=trial
        if len(G)==25920:break
    assert len(G)==25920 and len(gens)==5
    nidx={U:i for i,U in enumerate(new_supports)};oidx={U:i for i,U in enumerate(old_supports)}
    U0=new_supports[0];H=[g for g in G if mask_image(U0,g[1])==U0];assert len(H)==576
    fixed_old=[Q for Q in old_supports if all(mask_image(Q,gp)==Q for gp,_ in H)];assert len(fixed_old)==1
    Q0=fixed_old[0]
    mapping={}
    for gp,gl in G:
        u=nidx[mask_image(U0,gl)];q=oidx[mask_image(Q0,gp)]
        if u in mapping:assert mapping[u]==q
        mapping[u]=q
    assert len(mapping)==45 and len(set(mapping.values()))==45
    # generator-equivariance, plus graph and matrix equality.
    for gp,gl in gens:
        for i,U in enumerate(new_supports):
            ni=nidx[mask_image(U,gl)]; oi=mapping[i]; no=oidx[mask_image(old_supports[oi],gp)];assert mapping[ni]==no
    P=np.zeros((45,45),dtype=np.uint8)
    for i,o in mapping.items():P[i,o]=1
    RR=T.astype(int)@T.astype(int).T;Anew=((RR==2)&(~np.eye(45,dtype=bool))).astype(np.uint8)
    assert np.array_equal(P.T@Anew@P,old_transport)
    # Stronger: T row supports are exactly center-quad quotient 8-point supports.
    for i,o in mapping.items():assert frozenset(np.flatnonzero(T[i]).tolist())==old_supports[o]

    # Point-line incidence and sentinel exact sequence.
    N=np.zeros((40,40),dtype=np.uint8)
    for li,L in enumerate(lines):N[list(L),li]=1
    assert rank2(N)==25 and rank2(T)==15 and not ((T@N)%2).any()
    # rank equality upgrades inclusions to equalities: ker(T)=im(N), row(T)=ker(N^T).
    # Confirm the historical complete enumerator independently from a row basis.
    B=[]
    for r in T:
        if rank2(np.asarray(B+[r],dtype=np.uint8))>len(B):B.append(r.copy())
    assert len(B)==15
    W=Counter()
    for m in range(1<<15):
        x=np.zeros(40,dtype=np.uint8)
        for i,b in enumerate(B):
            if (m>>i)&1:x^=b
        W[int(x.sum())]+=1
    expected=Counter({0:1,8:45,12:720,16:6930,20:17376,24:6930,28:720,32:45,40:1});assert W==expected
    assert all(int(r.sum())==8 for r in T) and len({tuple(r.tolist()) for r in T})==45

    o92={'pass':4592,'new_45':'Pass4585 singular 16-line supports','old_45':'center-quad antipodal-pair quotient / E6 tritangent carrier',
      'PSp_order':25920,'common_stabilizer_order':576,'old_points_fixed_by_new_stabilizer':1,'equivariant_bijection_size':45,
      'generator_equivariance_verified':True,'graph_identity':'new SRG(45,32,22,24) = old center-quad transport/complement graph under explicit bijection',
      'matrix_preview':'Pass4593 strengthens the same bijection to exact 45x40 support-incidence equality.',
      'theorem':'The Pass4585 45-carrier is explicitly PSp(4,3)-equivariantly identical to the existing center-quad/E6-tritangent 45-carrier.',
      'boundary':'This is an exact finite G-set intertwiner; it does not by itself identify a physical E6 degree of freedom.'}
    o93={'pass':4593,'matrix_identity':'After the Pass4592 row permutation, T[i,p]=1 iff W33 point p lies in the corresponding center-quad quotient 8-point support.',
      'T_shape':[45,40],'T_rank_F2':15,'point_line_incidence_rank_F2':25,'TN_zero':True,
      'exact_sequences':['ker(T)=im(N), dimensions 25=25','row(T)=ker(N^T), dimensions 15=15'],
      'sentinel':{'parameters':'[40,15,8]','minimum_words':45,'T_rows_are_all_minimum_words':True,'weight_enumerator':{str(k):v for k,v in sorted(expected.items())}},
      'theorem':'The rank-15 45x40 polar transport is exactly the center-quad support incidence and its rows are precisely the complete minimum shell of the W33 sentinel code ker(N^T).',
      'boundary':'The quotient F2^40/im(N) and sentinel ker(N^T) are dual 15D realizations. No unproved canonical identification between those two modules is asserted.'}
    OUT92.write_text(json.dumps(o92,indent=2,sort_keys=True)+'\n');OUT93.write_text(json.dumps(o93,indent=2,sort_keys=True)+'\n');print(json.dumps({'4592':o92,'4593':o93},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
