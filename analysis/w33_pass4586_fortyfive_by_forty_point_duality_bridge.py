#!/usr/bin/env python3
"""Pass 4586 (outside box) -- a 45x40 bridge crosses the W33 point/line boundary.

Pass 4585 constructs 45 totally singular projective lines in the protected
O+(8,2) quotient from common 16-line apartment supports.  Independently, each
of the 40 original W33 points determines a K4 pencil of four line-vertices; its
three opposite-edge pairs give three anisotropic protected classes and hence an
all-anisotropic projective line in V8.

Declare a singular 45-object S incident with a point-pencil anisotropic line P
when all 3x3 cross pairs are polar-orthogonal.  The resulting 45x40 matrix R has
row weight 8, column weight 9, and binary rank 15.  Its integer Gram matrices are

  R R^T = 8 I_45 + 2 A_45,
  R^T R = 8 I_40 + 2 A_point + J_40,

where A_45 is SRG(45,32,22,24) and A_point is exactly the POINT-side W33
collinearity graph.  A_point is explicitly checked different from the protected
LINE-side graph A_*; W(3,3) is not self-dual at q=3.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from w33_apartment_section_core import build_geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4586_FORTYFIVE_BY_FORTY_POINT_DUALITY_BRIDGE.json'

def rank2(M):
    A=np.asarray(M,dtype=np.uint8).copy();m,n=A.shape;r=0
    for c in range(n):
        rows=np.flatnonzero(A[r:,c])
        if not len(rows):continue
        rr=r+int(rows[0])
        if rr!=r:A[[r,rr]]=A[[rr,r]]
        for i in range(m):
            if i!=r and A[i,c]:A[i]^=A[r]
        r+=1
        if r==m:break
    return r

def rbasis(vecs):
    piv={}
    for x in map(int,vecs):
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

def srg_params(A):
    A=np.asarray(A,dtype=np.uint8);v=len(A);deg=A.sum(1)
    assert len(set(map(int,deg)))==1;k=int(deg[0]);lam=set();mu=set()
    for i,j in itertools.combinations(range(v),2):
        c=int(np.dot(A[i].astype(int),A[j].astype(int)))
        (lam if A[i,j] else mu).add(c)
    assert len(lam)==len(mu)==1
    return [v,k,next(iter(lam)),next(iter(mu))]

def main()->int:
    pts,pidx,lines,lidx,Apoint,Astar,_,aps,_=build_geometry()
    Apoint=np.asarray(Apoint,dtype=np.uint8);Astar=np.asarray(Astar,dtype=np.uint8)
    assert Apoint.shape==Astar.shape==(40,40) and not np.array_equal(Apoint,Astar)
    j=(1<<40)-1
    cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    ledges=[(i,k) for i in range(40) for k in range(i+1,40) if Astar[i,k]]
    B9=rbasis([cols[i]^cols[k] for i,k in ledges]);assert len(B9)==9
    V=set(span(B9));assert len(V)==512 and j in V
    rep=lambda x:min(int(x),int(x)^j)
    q=lambda x:(rep(x).bit_count()//4)&1
    polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))

    # 45 singular support-lines from apartment fibers.
    fibers=defaultdict(list)
    for ap in aps:
        x=0
        for i in ap:x^=cols[int(i)]
        fibers[rep(x)].append(tuple(map(int,ap)))
    assert len(fibers)==135
    support_to_s=defaultdict(list)
    for s,F in fibers.items():
        U=frozenset().union(*(set(ap) for ap in F));assert len(U)==16
        support_to_s[U].append(s)
    assert len(support_to_s)==45 and all(len(S)==3 for S in support_to_s.values())
    singular_lines=[]
    for U,S in sorted(support_to_s.items(),key=lambda kv:tuple(sorted(kv[0]))):
        T=tuple(sorted(S));assert all(q(x)==0 for x in T)
        assert rep(T[0]^T[1]^T[2])==0
        assert all(polar(a,b)==0 for a,b in itertools.combinations(T,2))
        singular_lines.append(T)

    # 40 anisotropic projective lines, one from each ORIGINAL W33 point pencil.
    anis_lines=[]
    for p in range(40):
        L=sorted(i for i,line in enumerate(lines) if p in line);assert len(L)==4
        assert all(Astar[a,b] for a,b in itertools.combinations(L,2))
        a,b,c,d=L
        matchings=[((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))]
        T=[]
        for (u,v),(w,z) in matchings:
            x=rep(cols[u]^cols[v]);y=rep(cols[w]^cols[z]);assert x==y
            T.append(x)
        T=tuple(sorted(T));assert len(set(T))==3 and all(q(x)==1 for x in T)
        assert rep(T[0]^T[1]^T[2])==0
        assert all(polar(x,y)==1 for x,y in itertools.combinations(T,2))
        anis_lines.append(T)
    assert len(set(anis_lines))==40

    # Complete 3x3 orthogonality is the cross-incidence relation.
    R=np.zeros((45,40),dtype=np.uint8);cross=Counter()
    for i,S in enumerate(singular_lines):
        for k,T in enumerate(anis_lines):
            c=sum(polar(s,a)==0 for s in S for a in T);cross[c]+=1
            assert c in (3,9)
            if c==9:R[i,k]=1
    assert cross==Counter({3:1440,9:360})
    assert set(map(int,R.sum(1)))=={8} and set(map(int,R.sum(0)))=={9}
    assert rank2(R)==15

    RR=R.astype(int)@R.astype(int).T;CC=R.astype(int).T@R.astype(int)
    A45=np.zeros((45,45),dtype=np.uint8);A40=np.zeros((40,40),dtype=np.uint8)
    rowints=Counter();colints=Counter()
    for i,k in itertools.combinations(range(45),2):
        z=int(RR[i,k]);rowints[z]+=1
        if z==2:A45[i,k]=A45[k,i]=1
        else:assert z==0
    for i,k in itertools.combinations(range(40),2):
        z=int(CC[i,k]);colints[z]+=1
        if z==3:A40[i,k]=A40[k,i]=1
        else:assert z==1
    assert rowints==Counter({2:720,0:270})
    assert colints==Counter({1:540,3:240})
    assert srg_params(A45)==[45,32,22,24]
    assert srg_params(A40)==[40,12,2,4]
    assert np.array_equal(A40,Apoint)
    assert not np.array_equal(A40,Astar)
    assert np.array_equal(RR,8*np.eye(45,dtype=int)+2*A45.astype(int))
    assert np.array_equal(CC,8*np.eye(40,dtype=int)+2*Apoint.astype(int)+np.ones((40,40),dtype=int))
    assert not ((R@R.T)%2).any()
    assert np.array_equal((R.T@R)%2,np.ones((40,40),dtype=np.uint8))

    out={'pass':4586,
      'objects':{'singular_support_lines':45,'point_pencil_anisotropic_lines':40,
        'singular_line_definition':'three singular V8 classes sharing one 16-line apartment support',
        'anisotropic_line_definition':'three opposite-edge V8 classes in the K4 pencil through one original W33 point'},
      'incidence':{'criterion':'all 3x3 cross pairs polar-orthogonal','shape':[45,40],'row_weight':8,'column_weight':9,'binary_rank':15,
        'cross_orthogonality_counts':{'3':1440,'9':360}},
      'row_gram':{'identity':'R R^T = 8 I45 + 2 A45','graph':'SRG(45,32,22,24)','pair_intersections':{'0':270,'2':720}},
      'column_gram':{'identity':'R^T R = 8 I40 + 2 A_point + J40','graph':'point-side W33 = SRG(40,12,2,4)','pair_intersections':{'1':540,'3':240},
        'exactly_point_graph':True,'different_from_protected_line_graph_Astar':True},
      'mod2':{'RRt':'0','RtR':'J40'},
      'theorem':'The protected line-side O+(8,2) shell canonically generates a rank-15 45x40 incidence transport whose column Gram reconstructs the non-self-dual point-side W33 graph and whose row Gram reconstructs SRG(45,32,22,24).',
      'rediscovery_boundary':'The repository already contains natural 45-object carriers and an SRG(45,32,22,24). This pass constructs the 45-set and transport independently but does not claim identity with a prior E6/center-quad carrier until an explicit action intertwiner is certified.',
      'boundary':'This is a finite incidence/duality bridge. It explicitly respects the fact that point-side and line-side W(3,3) are inequivalent G-sets at odd q.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
