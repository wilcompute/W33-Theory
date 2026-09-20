#!/usr/bin/env python3
"""Exact A5 -> W33/S6 duad gauge-sector intertwiner.

The existing W33 S6 duad carrier is the 15-dimensional permutation module on
the edges {i,j} of K6.  Syntheme incidence D has rank 10 and kills its unique
five-dimensional gauge sector.

Let Q(A5)={x in Z^6 : sum_i x_i=0}.  Define
    Phi(x)_{ij}=x_i+x_j.
Then for every syntheme (perfect matching) M,
    sum_{ij in M} Phi(x)_{ij}=sum_i x_i=0,
so im Phi lies in ker D.  Phi has rank five and dim ker D=5, hence equality.

The intertwiner is S6-equivariant and its metric is
    Phi^T Phi = 4 C_A5
on the standard simple-root basis e_i-e_{i+1}.

The six-cycle c=(0 1 2 3 4 5) is the A5 Coxeter element.  On the 15 duads it
has cycle type 6^2 3, while c^2 has 3^5 and c^3 has 2^6 1^3.  This supplies an
intrinsic W33/S6 C6 whose C3 and C2 powers are genuine quotient/subcycle data.
It is NOT identified with the earlier oriented-Pauli CZ*parity C6.
"""
from __future__ import annotations
import itertools,json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_a5_duad_gauge_intertwiner.json'
V=tuple(range(6))
DUADS=list(itertools.combinations(V,2))
DIDX={e:i for i,e in enumerate(DUADS)}

def perfect_matchings(vertices):
    vertices=tuple(vertices)
    if not vertices:return [()]
    a=vertices[0];out=[]
    for j in range(1,len(vertices)):
        b=vertices[j]
        rest=vertices[1:j]+vertices[j+1:]
        for M in perfect_matchings(rest):
            out.append(tuple(sorted(((min(a,b),max(a,b)),)+M)))
    return sorted(set(out))

SYNTHEMES=perfect_matchings(V)

def rank(M):
    A=[[F(x) for x in r] for r in M]
    if not A:return 0
    m,n=len(A),len(A[0]);rr=0
    for c in range(n):
        p=next((i for i in range(rr,m) if A[i][c]),None)
        if p is None:continue
        A[rr],A[p]=A[p],A[rr]
        z=A[rr][c];A[rr]=[x/z for x in A[rr]]
        for i in range(m):
            if i!=rr and A[i][c]:
                z=A[i][c];A[i]=[A[i][j]-z*A[rr][j] for j in range(n)]
        rr+=1
    return rr

def phi(x):
    assert sum(x)==0
    return tuple(x[i]+x[j] for i,j in DUADS)

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def perm_duads(p):
    return tuple(DIDX[tuple(sorted((p[i],p[j])))] for i,j in DUADS)

def act6(p,x):
    # left permutation action: (p.x)_{p(i)}=x_i
    y=[0]*6
    for i in V:y[p[i]]=x[i]
    return tuple(y)

def act15(P,y):
    z=[0]*15
    for i,j in enumerate(P):z[j]=y[i]
    return tuple(z)

def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def ppow(p,n):
    r=tuple(range(len(p)))
    for _ in range(n):r=compose(p,r)
    return r
def cycle_type(p):
    seen=set();C=[]
    for i in range(len(p)):
        if i in seen:continue
        j=i;n=0
        while j not in seen:
            seen.add(j);n+=1;j=p[j]
        C.append(n)
    from collections import Counter
    return {str(k):v for k,v in sorted(Counter(C).items())}

def main(write=True):
    D=[[0]*15 for _ in SYNTHEMES]
    for r,M in enumerate(SYNTHEMES):
        for e in M:D[r][DIDX[e]]=1
    assert len(SYNTHEMES)==15 and rank(D)==10

    simples=[]
    for i in range(5):
        x=[0]*6;x[i]=1;x[i+1]=-1;simples.append(tuple(x))
    Pcols=[phi(x) for x in simples]
    P=[[Pcols[j][i] for j in range(5)] for i in range(15)]
    assert rank(P)==5
    assert all(sum(D[r][k]*P[k][j] for k in range(15))==0
               for r in range(15) for j in range(5))
    assert 15-rank(D)==rank(P)==5

    gram=[[dot(Pcols[i],Pcols[j]) for j in range(5)] for i in range(5)]
    cartan=[[2 if i==j else -1 if abs(i-j)==1 else 0 for j in range(5)] for i in range(5)]
    assert gram==[[4*x for x in r] for r in cartan]

    # Exhaustive equivariance for all 720 permutations of six labels.
    for p in itertools.permutations(V):
        Q=perm_duads(p)
        for x in simples:
            assert phi(act6(p,x))==act15(Q,phi(x))

    c=tuple((i+1)%6 for i in V)
    C=perm_duads(c)
    assert ppow(c,6)==tuple(V) and ppow(c,3)!=tuple(V)
    ct=cycle_type(C);c2=cycle_type(ppow(C,2));c3=cycle_type(ppow(C,3))
    assert ct=={'3':1,'6':2}
    assert c2=={'3':5}
    assert c3=={'1':3,'2':6}

    parent=ROOT/'PART_MMCCCXCI_S6_DUAD_REPRESENTATION_DECOMPOSITION_results.json'
    if parent.exists():
        d=json.loads(parent.read_text())
        assert d['checks']['D_rank_10'] is True
        assert d['checks']['D_kills_P5_gauge'] is True

    out={
      'schema':'w33.a5_duad_gauge_intertwiner.v1','status':'PASS_A5_DUAD_INTERTWINER',
      'headline':'The A5 root lattice Q(A5) embeds S6-equivariantly into the 15-dimensional K6-duad carrier by Phi(x)_{ij}=x_i+x_j. Its image is exactly the five-dimensional kernel of syntheme incidence, i.e. the existing W33 P5 gauge sector, and Phi scales the A5 Cartan metric by four. The natural six-cycle is the A5 Coxeter element and acts on duads with cycle types c:6^2 3, c^2:3^5, c^3:2^6 1^3.',
      'intertwiner':{
        'domain':'Q(A5)={x in Z^6: sum x_i=0}','codomain':'Z^{15} on K6 duads',
        'formula':'Phi(x)_{ij}=x_i+x_j','domain_rank':5,'image_rank':5,
        'syntheme_incidence_rank':10,'kernel_dimension':5,'image_equals_kernel':True,
        'metric':'Phi^T Phi = 4*C_A5','S6_equivariant_checked_elements':720},
      'coxeter_C6':{
        'six_cycle':'(0 1 2 3 4 5)','order':6,
        'duad_cycle_type':ct,'square_order':3,'square_duad_cycle_type':c2,
        'cube_order':2,'cube_duad_cycle_type':c3},
      'bridge':'The same A5 whose discriminant Z6 carries flagship hypercharge has an intrinsic five-dimensional W33/S6 gauge-module realization. This is an actual module intertwiner, not a 6=3*2 numerology.',
      'firewall':'This A5 Coxeter C6 is not identified with the oriented-Pauli CZ*parity C6. The latter acts on a different carrier and physical theta^3 parity has its own inner-E8 lift.',
      'parents':['PART_MMCCCXCI_S6_DUAD_REPRESENTATION_DECOMPOSITION_results.json','Holotrade data/w33_flagship_a5_hypercharge_organizer.json'],
      'checks':{'synthemes15':True,'D_rank10':True,'Phi_rank5':True,'image_kernel':True,'metric_4A5':True,'S6_equivariance720':True,'C6_cycle_types':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out
if __name__=='__main__':main(True)
