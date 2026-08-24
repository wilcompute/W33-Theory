#!/usr/bin/env python3
"""Pass10329-10336: Gamma16 is the unique S4-invariant nontrivial C2 twist of the 4x4 rook fibres.

The Pass10169/10321 graph has four K4 fibres.  Between every pair of fibres the
matching is the same antipodal involution tau=(0 2)(1 3).  Regard the four
fibres as the vertices of a base K4 and encode each pairwise matching by a C2
edge voltage: 0=identity, 1=tau.

The ordinary 4x4 rook graph is voltage 0 on every base edge: its six matchings
assemble into four global columns.  Gamma16 is voltage 1 on every base edge.
Gauge relabelling a fibre by tau adds a graph coboundary.  Therefore the twist
lives in H^1(K4;F2), dimension E-V+1=3.

Exact enumeration of the eight cohomology classes shows that the S4 action on
base fibres fixes exactly two classes: zero and ONE nonzero class.  The constant
1 edge assignment represents that unique nonzero invariant class.  Every base
triangle has flux 1+1+1=1, so the twist cannot be gauged away and there is no
global column partition.

This also separates three tempting 16-vertex objects:
* rook graph R(4,4): degree 6, untwisted;
* Gamma16: degree 6, unique S4-symmetric frustrated twist;
* toroidal grid C4 square C4 = Q4: degree 4.

Finally, Aut(Gamma16)=S4 x D8 has order 192 but is NOT the orientation-preserving
tesseract group W(D4)=2^3:S4, also order 192.  Their element-order distributions
are different: Gamma16 has elements of order 12 and none of order 8; W(D4) has
48 elements of order 8 and none of order 12.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10329_10336_TWISTED_ROOK_COHOMOLOGY.json'

def pcomp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def porder(p):
    I=tuple(range(len(p)));x=I
    for k in range(1,100):
        x=pcomp(p,x)
        if x==I:return k
    raise RuntimeError

def spectrum(A):return {int(k):int(v) for k,v in sp.Matrix(A).eigenvals().items()}

def main():
    S4=list(itertools.permutations(range(4)))
    edges=list(itertools.combinations(range(4),2));eidx={e:i for i,e in enumerate(edges)}

    # Coboundaries from fibre gauge switches s_i in F2; global constant switch is kernel.
    cob=set()
    for s in itertools.product([0,1],repeat=4):cob.add(tuple(s[i]^s[j] for i,j in edges))
    assert len(cob)==8
    def xor(a,b):return tuple(x^y for x,y in zip(a,b))
    def rep(v):return min(xor(v,c) for c in cob)
    classes=sorted({rep(v) for v in itertools.product([0,1],repeat=6)})
    assert len(classes)==8
    def act(v,p):
        w=[0]*6
        for i,(a,b) in enumerate(edges):
            image=tuple(sorted((p[a],p[b])));w[eidx[image]]=v[i]
        return tuple(w)
    fixed=[c for c in classes if all(rep(act(c,p))==c for p in S4)]
    assert len(fixed)==2
    zero=rep((0,)*6);twist=rep((1,)*6)
    assert set(fixed)=={zero,twist} and twist!=zero

    # Constant-one twist has nontrivial holonomy around every K4 triangle.
    const=(1,)*6
    tri_flux={}
    for T in itertools.combinations(range(4),3):
        es=[eidx[tuple(sorted(e))] for e in itertools.combinations(T,2)]
        tri_flux[''.join(map(str,T))]=sum(const[i] for i in es)%2
    assert set(tri_flux.values())=={1}

    # Build rook, Gamma16, and torus=C4 square C4=Q4 on common C4xC4 cells.
    V=[(a,b) for a in range(4) for b in range(4)];idx={v:i for i,v in enumerate(V)}
    def graph(kind):
        A=[[0]*16 for _ in range(16)]
        for i,x in enumerate(V):
            for j,y in enumerate(V):
                if i>=j:continue
                da=(y[0]-x[0])%4;db=(y[1]-x[1])%4
                if kind=='rook': ok=(da==0 and db!=0) or (db==0 and da!=0)
                elif kind=='gamma': ok=(da==0 and db in (1,2,3)) or (da in (1,2,3) and db==2)
                elif kind=='torus': ok=(da in (1,3) and db==0) or (da==0 and db in (1,3))
                else:raise ValueError
                if ok:A[i][j]=A[j][i]=1
        return A
    Ar=graph('rook');Ag=graph('gamma');At=graph('torus')
    sr,sg,st=spectrum(Ar),spectrum(Ag),spectrum(At)
    assert sr=={6:1,2:6,-2:9}
    assert sg=={6:1,2:4,0:6,-2:3,-4:2}
    assert st=={4:1,2:4,0:6,-2:4,-4:1}

    # Product S4 x D8 element orders.
    tau=(2,3,0,1)
    D8=[p for p in S4 if pcomp(p,tau)==pcomp(tau,p)];assert len(D8)==8
    gd=Counter()
    for p in S4:
        for q in D8:gd[math.lcm(porder(p),porder(q))]+=1
    assert gd==Counter({4:68,2:59,6:40,12:16,3:8,1:1})

    # Orientation-preserving signed permutations of R4: W(D4), tesseract rotations.
    def parity(p):return -1 if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2 else 1
    WD=[]
    for p in S4:
        for s in itertools.product([1,-1],repeat=4):
            if math.prod(s)*parity(p)==1:WD.append((p,s))
    assert len(WD)==192
    ID=(tuple(range(4)),(1,1,1,1))
    def scomp(g,h):
        p,s=g;q,t=h
        return tuple(p[q[i]] for i in range(4)),tuple(t[i]*s[q[i]] for i in range(4))
    def sorder(g):
        x=ID
        for k in range(1,100):
            x=scomp(g,x)
            if x==ID:return k
        raise RuntimeError
    td=Counter(sorder(g) for g in WD)
    assert td==Counter({8:48,2:43,4:36,3:32,6:32,1:1})
    assert 12 in gd and 8 not in gd and 8 in td and 12 not in td

    out={
      'schema':'w33.pass10329_10336.twisted_rook_cohomology.v1','status':'PASS','passes':'10329-10336',
      'cohomology':{'base':'K4 on the four common-line/K4 fibres','coefficients':'C2 generated by tau=(0 2)(1 3)',
                    'H1_dimension':3,'H1_classes':8,'S4_fixed_classes':2,
                    'unique_nonzero_S4_fixed_class':'constant voltage 1 on all six base edges',
                    'triangle_flux':tri_flux,'interpretation':'all four base triangles are frustrated; the twist is not a coboundary'},
      'graphs':{'rook':{'meaning':'untwisted row/column geometry','degree':6,'spectrum':{str(k):v for k,v in sr.items()}},
                'Gamma16':{'meaning':'antipodally twisted rook fibres','degree':6,'spectrum':{str(k):v for k,v in sg.items()}},
                'C4_square_C4':{'meaning':'ordinary 4x4 toroidal grid = Q4','degree':4,'spectrum':{str(k):v for k,v in st.items()}}},
      'tesseract_guardrail':{'Gamma16_Aut':'S4 x D8','Gamma16_element_orders':{str(k):v for k,v in sorted(gd.items())},
                             'tesseract_rotation_group':'W(D4)=2^3:S4','tesseract_element_orders':{str(k):v for k,v in sorted(td.items())},
                             'isomorphic':False,'witness':'Gamma16 Aut has 16 elements of order 12 and no order 8; W(D4) has 48 elements of order 8 and no order 12'},
      'theorem':'Gamma16 is the unique nontrivial S4-invariant C2 voltage twist of the four-row K4 rook-fibre system. Its constant antipodal matching has nonzero holonomy on every base triangle, so no gauge relabelling can turn it into the ordinary 4x4 rook/Latin row-column geometry. The shared order 192 with the tesseract rotation group is not an isomorphism.',
      'interpretation':'The 4x4 bridge is cohomological: Gamma16 is a maximally symmetric frustrated version of the row/column board. This gives a concrete finite model of the repo\'s recurring orientation/frustration theme rather than another raw 192 count match.',
      'boundary':'Exact finite enumeration. The word Latin refers only to the standard row/column 4x4 cell geometry here; no bijection with all 576 Latin squares is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','H1':8,'S4_fixed':2,'triangle_flux':1,'GammaAut':'S4xD8','tesseract_same':False}))
    return 0
if __name__=='__main__':raise SystemExit(main())
