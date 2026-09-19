#!/usr/bin/env python3
"""Triality decomposition of the physical flagship E8 C6 grading.

Parent:
  data/w33_physical_holonomy_e8_chevalley_lift.json

The parent proves that the joint order-(3,2) holonomy pair fixes
  D4 + A3 + u1
inside E8 and gives nonzero joint-character dimensions 48,38,40,38,40.

This certificate decomposes every nonneutral root sector as a representation
of D4 x A3 by exact root-operator connectivity and weight restriction.

Using the same explicit A8 model of the 240 E8 roots, two roots in one joint
character sector are connected when their difference is a neutral root.  The
connected components are:
  (0,-): 48
  (1,+): 32 + 6
  (1,-): 32 + 8
  (2,+): 32 + 6
  (2,-): 32 + 8.

Restriction to a rank-4 basis of the D4 roots and a rank-3 basis of A3 proves:
  * the 48 component has 8 distinct D4 weights, each repeated 6, and
    6 distinct A3 weights, each repeated 8 => (8_A,6);
  * each 32 has 8 distinct D4 weights repeated 4 and 4 A3 weights repeated 8
    => (8_B,4) or (8_C,4);
  * each 6 is D4-trivial with the six A3 antisymmetric weights => (1,6);
  * each 8 is A3-trivial with one of the D4 eight-weight orbits => (8_A,1).

Exactly THREE distinct eight-weight D4 restriction sets occur.  D4 has three
eight-dimensional minuscule representations, permuted by triality.  Therefore
these three sets are the triality triple {8_v,8_s,8_c}; their assignment to
v,s,c is noncanonical until a D4 triality frame is chosen.  We denote them
8_A,8_B,8_C.

Choosing the A3 fundamental convention so that the weight set appearing in
(1,+) is 4 and its dual is bar4 gives the exact decomposition:
  (0,-) = (8_A,6)
  (1,+) = (8_B,4) + (1,6)
  (2,+) = (8_B,bar4) + (1,6)
  (1,-) = (8_C,bar4) + (8_A,1)
  (2,-) = (8_C,4) + (8_A,1)

The a=1 and a=2 sectors are dual exactly.

Scope:
This is representation theory of the physical E8 inner holonomy grading.
It does not assign Standard-Model particles to these components and does not
choose which of A,B,C is vector versus the two spinors.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_physical_e8_triality_decomposition.json'
JOINT=[((0,0),3),((0,1),2),((1,0),1),((1,1),1),((2,0),1),((2,1),1)]

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def rank(rows):
    A=[list(r) for r in rows if any(r)]
    if not A:return 0
    m,n=len(A),len(A[0]);r=0
    for c in range(n):
        p=next((i for i in range(r,m) if A[i][c]),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r];z=A[r][c];A[r]=[x/z for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                z=A[i][c];A[i]=[A[i][j]-z*A[r][j] for j in range(n)]
        r+=1
    return r
def independent(ids,roots,n):
    B=[]
    for i in ids:
        if rank([roots[j] for j in B]+[roots[i]])>len(B):B.append(i)
        if len(B)==n:return B
    raise AssertionError('basis')
def components(ids,roots,steps):
    rem=set(ids);out=[]
    while rem:
        i=rem.pop();C=[i];stack=[i]
        while stack:
            u=stack.pop()
            ns=[v for v in list(rem) if sub(roots[v],roots[u]) in steps or sub(roots[u],roots[v]) in steps]
            for v in ns:rem.remove(v);stack.append(v);C.append(v)
        out.append(C)
    return sorted(out,key=len,reverse=True)

def main(write=True):
    chars=[]
    for ch,n in JOINT:chars += [ch]*n
    roots=[];rch=[]
    for i in range(9):
      for j in range(9):
        if i==j:continue
        v=[F(0)]*9;v[i]=1;v[j]=-1
        roots.append(tuple(v));rch.append(((chars[i][0]-chars[j][0])%3,(chars[i][1]-chars[j][1])%2))
    for S in itertools.combinations(range(9),3):
        v=[F(-1,3)]*9
        for i in S:v[i]+=1
        ch=(sum(chars[i][0] for i in S)%3,sum(chars[i][1] for i in S)%2)
        roots.append(tuple(v));rch.append(ch)
        roots.append(tuple(-x for x in v));rch.append(((-ch[0])%3,(-ch[1])%2))
    assert len(roots)==240

    neutral=[i for i,ch in enumerate(rch) if ch==(0,0)]
    N={roots[i] for i in neutral}
    nc=components(neutral,roots,N)
    assert sorted((len(C),rank([roots[i] for i in C])) for C in nc)==[(12,3),(24,4)]
    D4=max(nc,key=len);A3=min(nc,key=len)
    db=independent(D4,roots,4);ab=independent(A3,roots,3)
    dsig=lambda i:tuple(dot(roots[i],roots[j]) for j in db)
    asig=lambda i:tuple(dot(roots[i],roots[j]) for j in ab)

    sec={}
    for ch in [(0,1),(1,0),(1,1),(2,0),(2,1)]:
        ids=[i for i,c in enumerate(rch) if c==ch]
        cc=components(ids,roots,N)
        rec=[]
        for C in cc:
            dc=Counter(dsig(i) for i in C);ac=Counter(asig(i) for i in C)
            rec.append({'dimension':len(C),'D4_distinct_weights':len(dc),
                        'D4_weight_multiplicities':dict(Counter(dc.values())),
                        'A3_distinct_weights':len(ac),
                        'A3_weight_multiplicities':dict(Counter(ac.values())),
                        '_Dset':frozenset(dc),'_Aset':frozenset(ac)})
        sec[ch]=rec
    assert [x['dimension'] for x in sec[(0,1)]]==[48]
    assert [x['dimension'] for x in sec[(1,0)]]==[32,6]
    assert [x['dimension'] for x in sec[(1,1)]]==[32,8]
    assert [x['dimension'] for x in sec[(2,0)]]==[32,6]
    assert [x['dimension'] for x in sec[(2,1)]]==[32,8]

    A=sec[(0,1)][0]['_Dset']
    B=sec[(1,0)][0]['_Dset']
    C=sec[(1,1)][0]['_Dset']
    assert len(A)==len(B)==len(C)==8 and len({A,B,C})==3
    assert sec[(1,1)][1]['_Dset']==A and sec[(2,1)][1]['_Dset']==A
    assert sec[(2,0)][0]['_Dset']==B and sec[(2,1)][0]['_Dset']==C

    four=sec[(1,0)][0]['_Aset'];bar4=sec[(1,1)][0]['_Aset'];six=sec[(0,1)][0]['_Aset']
    assert len(four)==len(bar4)==4 and four!=bar4 and len(six)==6
    assert sec[(2,1)][0]['_Aset']==four and sec[(2,0)][0]['_Aset']==bar4
    assert sec[(1,0)][1]['_Aset']==six and sec[(2,0)][1]['_Aset']==six

    decomposition={
      '0,1':'(8_A,6)',
      '1,0':'(8_B,4) + (1,6)',
      '2,0':'(8_B,bar4) + (1,6)',
      '1,1':'(8_C,bar4) + (8_A,1)',
      '2,1':'(8_C,4) + (8_A,1)'}
    parent=json.loads((ROOT/'data/w33_physical_holonomy_e8_chevalley_lift.json').read_text())
    assert parent['status']=='PASS_PHYSICAL_INNER_CHEVALLEY_LIFT'

    clean={}
    for ch,rr in sec.items():
        clean[f'{ch[0]},{ch[1]}']=[{k:v for k,v in x.items() if not k.startswith('_')} for x in rr]
    out={'schema':'w33.physical_e8_triality_decomposition.v1','status':'PASS_TRIALITY_MATTER_SKELETON',
      'headline':'Under the physical fixed algebra D4+A3+u1, the nonneutral E8 holonomy sectors decompose into (8_A,6), (8_B,4)+(1,6), its conjugate, (8_C,bar4)+(8_A,1), and its conjugate. Exactly three distinct D4 eight-weight sets occur, so {8_A,8_B,8_C} is the Spin(8) triality triple {8v,8s,8c} up to a noncanonical triality-frame permutation.',
      'neutral_algebra':'D4 + A3 + u1',
      'sector_components':clean,'decomposition':decomposition,
      'triality':{'distinct_D4_eight_weight_orbits':3,
                  'sets':'8_A, 8_B, 8_C',
                  'identification':'{8_A,8_B,8_C}={8v,8s,8c} up to S3 triality',
                  'A_occurs_in':'(0,1) 48-block and the isolated 8-blocks in (1,1),(2,1)',
                  'B_occurs_in':'32-blocks of (1,0),(2,0)',
                  'C_occurs_in':'32-blocks of (1,1),(2,1)'},
      'A3_duality':{'4_weight_set':'(1,0) and (2,1)','bar4_weight_set':'(1,1) and (2,0)','6_is_self_dual':True},
      'boundary':'Representation skeleton only. No Standard-Model particle assignment and no canonical choice of which triality orbit is vector/spinor.',
      'checks':{'component_dimensions':True,'three_distinct_triality_orbits':True,
                'A3_4_bar4_duality':True,'parent_loaded':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
