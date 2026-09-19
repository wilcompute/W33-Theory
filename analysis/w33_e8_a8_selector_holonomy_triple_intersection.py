#!/usr/bin/env python3
"""Close the physical E8 lift with the order-3 A8 selector.

Parent w33_physical_holonomy_e8_chevalley_lift proves the inner E8 lift of the
flagship Wilson/parity pair.  This pass adjoins the independent order-3 inner
automorphism rho whose fixed algebra is A8 and whose E8 grading is

    E8 = A8_0 + Lambda^3(9)_1 + Lambda^6(9)_2.

That is the exact Lie-algebra selector for the local SU(9) chart.  Intersecting
rho with the physical pair removes the off-A8 84+84bar root spaces.  The
remaining pair-neutral A8 roots split as A2+A1, while the full rank-8 Cartan
survives, hence the triple fixed algebra is

    A2 + A1 + u(1)^5,

dimension 8+3+5 = 16.  This is exactly the corrected local SU(9) joint
centralizer S(U3 x U2 x U1^4).

The result explains the hierarchy of fixed algebras:
  rho                     -> A8                              dim 80
  W3                      -> D7 + u1                        dim 92
  theta3                  -> D8                             dim 120
  W3 & theta3             -> D4 + A3 + u1                  dim 44
  rho & W3                -> A4 + A1 + A1 + u1^2           dim 32
  rho & theta3            -> A4 + A3 + u1                  dim 40
  rho & W3 & theta3       -> A2 + A1 + u1^5                dim 16

This is the missing categorical distinction: the 44-dimensional common
centralizer of the physical pair in all of E8 is not the local gauge algebra.
The local A8 selector projects away the 28 pair-neutral roots in Lambda^3 and
Lambda^6, leaving the 8 A8 roots of A2+A1 and the eight-dimensional Cartan.
"""
from __future__ import annotations
import itertools, json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_e8_a8_selector_holonomy_triple_intersection.json'
JOINT=[((0,0),3),((0,1),2),((1,0),1),((1,1),1),((2,0),1),((2,1),1)]

def dot(a,b): return sum(x*y for x,y in zip(a,b))

def rank(rows):
    A=[list(r) for r in rows if any(r)]
    if not A:return 0
    m,n=len(A),len(A[0]); rr=0
    for c in range(n):
        p=next((i for i in range(rr,m) if A[i][c]),None)
        if p is None: continue
        A[rr],A[p]=A[p],A[rr]
        z=A[rr][c];A[rr]=[x/z for x in A[rr]]
        for i in range(m):
            if i!=rr and A[i][c]:
                z=A[i][c];A[i]=[A[i][j]-z*A[rr][j] for j in range(n)]
        rr+=1
    return rr

def components(roots, ids):
    rem=set(ids); out=[]
    while rem:
        i=rem.pop(); C=[i]; stack=[i]
        while stack:
            u=stack.pop()
            ns=[v for v in list(rem) if dot(roots[u],roots[v])!=0]
            for v in ns:
                rem.remove(v);stack.append(v);C.append(v)
        out.append(C)
    return sorted((len(C),rank([roots[i] for i in C])) for C in out)

def main(write=True):
    chars=[]
    for ch,n in JOINT: chars += [ch]*n
    roots=[]; labels=[]

    # A8 roots: rho-grade 0.
    for i in range(9):
        for j in range(9):
            if i==j: continue
            v=[F(0)]*9;v[i]=1;v[j]=-1
            roots.append(tuple(v))
            labels.append(((chars[i][0]-chars[j][0])%3,
                           (chars[i][1]-chars[j][1])%2,0,'A8'))

    # Lambda^3 and Lambda^6: rho-grades +1 and -1.
    for S in itertools.combinations(range(9),3):
        v=[F(-1,3)]*9
        for i in S:v[i]+=1
        a=sum(chars[i][0] for i in S)%3
        b=sum(chars[i][1] for i in S)%2
        roots.append(tuple(v));labels.append((a,b,1,'L3'))
        roots.append(tuple(-x for x in v));labels.append(((-a)%3,(-b)%2,2,'L6'))

    assert len(roots)==len(set(roots))==240
    assert all(dot(r,r)==2 for r in roots)

    def fixed(pred):
        return [i for i,x in enumerate(labels) if pred(*x)]

    rho=fixed(lambda a,b,c,s:c==0)
    w=fixed(lambda a,b,c,s:a==0)
    p=fixed(lambda a,b,c,s:b==0)
    wp=fixed(lambda a,b,c,s:a==0 and b==0)
    rw=fixed(lambda a,b,c,s:c==0 and a==0)
    rp=fixed(lambda a,b,c,s:c==0 and b==0)
    rwp=fixed(lambda a,b,c,s:c==0 and a==0 and b==0)

    sig={
      'rho_A8':components(roots,rho),
      'W3':components(roots,w),
      'theta3':components(roots,p),
      'W3_theta3':components(roots,wp),
      'rho_W3':components(roots,rw),
      'rho_theta3':components(roots,rp),
      'rho_W3_theta3':components(roots,rwp),
    }
    assert sig['rho_A8']==[(72,8)]
    assert sig['W3']==[(84,7)]
    assert sig['theta3']==[(112,8)]
    assert sig['W3_theta3']==[(12,3),(24,4)]
    assert sig['rho_W3']==[(2,1),(2,1),(20,4)]
    assert sig['rho_theta3']==[(12,3),(20,4)]
    assert sig['rho_W3_theta3']==[(2,1),(6,2)]

    counts={k:sum(n for n,r in v) for k,v in sig.items()}
    # rank(E8)=8 is retained by all torus centralizers.
    dims={k:8+counts[k] for k in counts}
    assert dims=={
      'rho_A8':80,'W3':92,'theta3':120,'W3_theta3':44,
      'rho_W3':32,'rho_theta3':40,'rho_W3_theta3':16}

    sectors=Counter(s for a,b,c,s in labels if a==0 and b==0)
    assert sectors==Counter({'L3':14,'L6':14,'A8':8})
    triple_sectors=Counter(s for a,b,c,s in labels if a==0 and b==0 and c==0)
    assert triple_sectors==Counter({'A8':8})

    parent=json.loads((ROOT/'data/w33_physical_holonomy_e8_chevalley_lift.json').read_text())
    assert parent['status']=='PASS_PHYSICAL_INNER_CHEVALLEY_LIFT'
    scope=json.loads((ROOT/'data/w33_holonomy_joint_centralizer_scope.json').read_text())
    assert scope['joint']['dimension']==16

    out={
      'schema':'w33.e8_a8_selector_holonomy_triple_intersection.v1',
      'status':'PASS_A8_SELECTOR_TRIPLE_CENTRALIZER',
      'headline':'Adjoining the order-3 A8 selector rho to the physical inner E8 Wilson/parity pair projects away the pair-neutral Lambda^3+Lambda^6 roots and reduces the full E8 pair centralizer D4+A3+u1 (dim44) to A2+A1+u1^5 (dim16), exactly the corrected local SU(9) joint centralizer. The three commuting inner automorphisms therefore give a single exact fixed-algebra chain rather than competing E8 and SU9 pictures.',
      'grading':'E8 = A8_0 + Lambda3(9)_1 + Lambda6(9)_2 under rho',
      'fixed_chain':{
        'rho':{'roots':72,'signature':sig['rho_A8'],'algebra':'A8','dimension':80},
        'W3':{'roots':84,'signature':sig['W3'],'algebra':'D7+u1','dimension':92},
        'theta3':{'roots':112,'signature':sig['theta3'],'algebra':'D8','dimension':120},
        'W3_and_theta3':{'roots':36,'signature':sig['W3_theta3'],'algebra':'D4+A3+u1','dimension':44},
        'rho_and_W3':{'roots':24,'signature':sig['rho_W3'],'algebra':'A4+A1+A1+u1^2','dimension':32},
        'rho_and_theta3':{'roots':32,'signature':sig['rho_theta3'],'algebra':'A4+A3+u1','dimension':40},
        'rho_W3_theta3':{'roots':8,'signature':sig['rho_W3_theta3'],'algebra':'A2+A1+u1^5','dimension':16}},
      'pair_neutral_sector_split_before_rho':dict(sectors),
      'triple_neutral_sector_split_after_rho':dict(triple_sectors),
      'removed_by_A8_selector':{'roots':28,'source':'14 Lambda3 + 14 Lambda6 pair-neutral roots'},
      'physics_reading':'The physical Wilson/parity pair has a larger 44-dimensional centralizer in all of E8; the local orbifold A8 selector is the missing projector that makes the local gauge algebra 16-dimensional. Hypercharge still selects one of the five surviving abelian Cartan directions; four further U(1)s require the usual heterotic mass/projection analysis.',
      'checks':{
        'E8_roots_240':True,'rho_fixes_A8_80':True,'physical_pair_fixes_44':True,
        'rho_removes_28_pair_neutral_off_A8_roots':True,
        'triple_fixed_A2_A1_u1_5_dim16':True,
        'matches_corrected_local_centralizer':True},
      'parents':['data/w33_physical_holonomy_e8_chevalley_lift.json','data/w33_holonomy_joint_centralizer_scope.json'],
      'boundary':'Exact E8 root/character arithmetic in the regular A8 model. Identifying rho with the recorded local orbifold selector uses the already-certified fact that the local fixed algebra is A8; this does not by itself determine the fate of the four extra U(1) gauge bosons.'
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out

if __name__=='__main__': main(True)
