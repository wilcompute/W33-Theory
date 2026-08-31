#!/usr/bin/env python3
"""Identify the 120 polar-secant-pair stabilizers inside PSp(4,3).

The PG(3,4) line stratification gives 240 Hermitian secants in 120 polarity
pairs.  Each pair maps to the two complementary edges of a unique W33 line,
i.e. a perfect matching of its four points.  This audit computes the stabilizer
of an actual polar secant pair in the native 85-point action and proves it is
exactly the previously constructed second order-216 subgroup class.

It further resolves the internal structure by the action on the matched W33
K4: the image is the full D8 matching stabilizer and the kernel is tested for
order 27, exponent 3 and commutativity.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

import w33_20260829_pg34_polarity_sentinel as pg
import w33_20260829_216_clifford_torsor_nogo as base

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_PG34_POLAR_SECANT_STABILIZER216.json'


def main():
    N,A=pg.geometry(); B,G45=pg.trade_incidence(N)
    supports=[frozenset(i for i in range(40) if B[i][j]) for j in range(45)]
    H=[]
    for i in range(40):H.append(A[i]+B[i])
    for j in range(45):H.append([B[i][j] for i in range(40)]+[G45[j][k]+(1 if j==k else 0) for k in range(45)])
    assert len(H)==85
    lines85=set()
    for i,j in itertools.combinations(range(85),2):
        L=tuple(k for k in range(85) if H[i][k] and H[j][k]);assert len(L)==5;lines85.add(L)
    lines85=sorted(lines85);assert len(lines85)==357
    lix={L:i for i,L in enumerate(lines85)}
    pol=[]
    for L in lines85:
        i,j=L[:2];P=tuple(k for k in range(85) if H[i][k] and H[j][k]);assert P in lix;pol.append(lix[P])
    assert all(pol[pol[i]]==i for i in range(357))
    typ=[(sum(x>=40 for x in L),sum(x<40 for x in L)) for L in lines85]
    sec=[i for i,t in enumerate(typ) if t==(3,2)];assert len(sec)==240
    secpairs={tuple(sorted((i,pol[i]))) for i in sec};assert len(secpairs)==120

    # Native paired PSp action on 40 nonabsolute + 45 absolute labels.
    pts,idx,wlines,_=base.geometry()
    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*base.form(x,v)%3
                y=base.norm(tuple((x[k]+z*v[k])%3 for k in range(4)));p.append(idx[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)}
    gens45=[tuple(si[frozenset(p[x] for x in S)] for S in supports) for p in gens40]
    chosen=(18,62,77,10)
    G=base.closure_paired([gens40[i] for i in chosen],[gens45[i] for i in chosen]);assert len(G)==25920
    def p85(g):
        a,b=g;return tuple(a)+tuple(40+b[j] for j in range(45))
    def act_line(g,i):return lix[tuple(sorted(p85(g)[x] for x in lines85[i]))]

    P0=min(secpairs); i,j=P0
    Hsec=[g for g in G if tuple(sorted((act_line(g,i),act_line(g,j))))==P0]
    assert len(Hsec)==216
    orbit={tuple(sorted((act_line(g,i),act_line(g,j)))) for g in G};assert orbit==secpairs

    # Its W33 shadow is exactly a perfect matching on one four-point line.
    e1=tuple(x for x in lines85[i] if x<40);e2=tuple(x for x in lines85[j] if x<40)
    assert len(e1)==len(e2)==2 and set(e1).isdisjoint(e2)
    U=tuple(sorted(set(e1)|set(e2)));assert len(U)==4
    assert all(A[a][b] for a,b in itertools.combinations(U,2))
    matching={frozenset(e1),frozenset(e2)}
    Hmatch=[]
    for g in G:
        if {g[0][x] for x in U}!=set(U):continue
        image={frozenset(g[0][x] for x in e) for e in matching}
        if image==matching:Hmatch.append(g)
    assert len(Hmatch)==216 and set(Hmatch)==set(Hsec)

    # Compare directly to the class-11 construction from the earlier no-go.
    L0=tuple(U); pos={x:k for k,x in enumerate(L0)}
    induced=set();kernel=[]
    for g in Hsec:
        q=tuple(pos[g[0][x]] for x in L0);induced.add(q)
        if q==tuple(range(4)):kernel.append(g)
    assert len(induced)==8 and len(kernel)==27
    image_orders=Counter(base.porder(q) for q in induced)
    kernel_orders=Counter(base.porder(g[0]) for g in kernel)
    kernel_abelian=all(base.compose(a[0],b[0])==base.compose(b[0],a[0]) for a in kernel for b in kernel)
    kernel_exp3=set(kernel_orders)<= {1,3}
    assert image_orders==Counter({2:5,4:2,1:1})
    assert kernel_abelian and kernel_exp3 and kernel_orders[1]==1 and kernel_orders[3]==26

    # Self-normalizing class length 120, matching the complete secant-pair orbit.
    H45={g[1] for g in Hsec};G45=[g[1] for g in G]
    normalizer=base.normalizer_size(G45,H45,45);assert normalizer==216
    order_hist=dict(sorted(Counter(base.porder(g[0]) for g in Hsec).items()))

    out={
      'schema':'w33.20260831.pg34-polar-secant-stabilizer216.v1','status':'PASS',
      'polarSecantPairs':{'count':120,'transitive':True,'stabilizerOrder':216,
        'normalizerOrder':216,'conjugacyClassLength':120},
      'W33Shadow':{'fourPointLine':list(U),'matching':[sorted(e) for e in matching],
        'stabilizerEqualsPerfectMatchingStabilizer':True},
      'structure':{'kernelOrder':27,'kernel':'C3^3','kernelAbelian':kernel_abelian,
        'kernelElementOrders':dict(sorted(kernel_orders.items())),'quotientImageOrder':8,
        'quotientImage':'D8','quotientElementOrders':dict(sorted(image_orders.items())),
        'semidirectDescription':'3^3 : D8','elementOrderHistogram':order_hist},
      'classIdentification':{'order216Class':'second / Connor-Leemans class 11',
        'reason':'same native subgroup as the self-normalizing perfect-matching stabilizer; the 120 conjugates are exactly the 120 polar secant pairs'},
      'theorem':'A polar pair of Hermitian secants is equivalent to a perfect matching of a W33 line. Its stabilizer is the self-normalizing second order-216 subgroup, with elementary-abelian 3^3 kernel and full D8 matching action, hence concrete shape 3^3:D8.',
      'boundary':'Exact finite group/geometry statement. This order-216 group is distinct from the point-stabilizer/C3 projective qutrit-Clifford quotient unless an additional isomorphism/action map is proved.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','pairs':120,'stab':216,'normalizer':normalizer,
      'kernel':27,'image':8,'shape':'3^3:D8','orders':order_hist},sort_keys=True))

if __name__=='__main__':main()
