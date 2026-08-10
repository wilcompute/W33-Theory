#!/usr/bin/env python3
"""Pass 4574 -- observed exact global prism action on Q(5,3)=dual H(3,9).

Pass4547 installed a pynauty/Schreier verifier for a 544,320-prism homogeneous
space but deliberately left its target values fail-closed because remote workflow
status was not surfaced. This pass closes the same statement independently from
existing repository arithmetic, with no pynauty dependency.

Use Pass4389's explicit Hermitian surface H(3,9) over GF(9). Its 112 totally
isotropic lines are the 112 points of the dual Q(5,3)=GQ(3,9). Four explicit
unitary transvections generate PSU(4,3) on H(3,9). Adjoining the unitary diagonal
D=diag(lambda,1,1,1), lambda=3 (norm one, order four in GF(9)^*), gives the full
projective unitary action of order 13,063,680 on the 112 dual points.

For one noncollinear Q(5,3) point pair:
  pointwise stabilizer order = 1440,
  setwise stabilizer order   = 2880,
  common-neighbor rungs      = 10,
  induced setwise rung image = 1440, kernel 2,
  ordered distinct triple orbit = 720,
  unordered 3-subset orbit      = 120.

Hence the group is transitive on 4536 noncollinear pairs and on the 120 three-rung
prisms over each pair. The global prism carrier is one orbit of size
4536*120=544,320 with stabilizer order 24.
"""
from __future__ import annotations

import itertools,json
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup

import w33_pass4389_hermitian_quadrangle_measured as p4389

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4574_Q53_GLOBAL_PRISM_ACTION_OBSERVED.json'
MUL,ADD,CONJ,INV=p4389.MUL,p4389.ADD,p4389.CONJ,p4389.INV
herm=p4389.herm
PSU=3265920;PGU=13063680
TV=[((0,0,1,4),3),((0,0,1,5),3),((0,1,0,4),3),((1,0,0,4),3)]


def normalise(v):
    for c in v:
        if c:return tuple(MUL[INV[c]][x] for x in v)
    raise ValueError('zero')


def transvection(v,a):
    def T(x):
        c=MUL[a][herm(x,v)]
        return tuple(ADD[xi][MUL[c][vi]] for xi,vi in zip(x,v))
    return T


def diag_outer(x):
    return (MUL[3][x[0]],x[1],x[2],x[3])


def orbit_tuple(seed,gens,unordered=False):
    key=lambda x:tuple(sorted(x)) if unordered else tuple(x)
    seen={key(seed)};stack=list(seen)
    while stack:
        x=stack.pop()
        for g in gens:
            y=key(tuple(g(i) for i in x))
            if y not in seen:seen.add(y);stack.append(y)
    return seen


def main()->int:
    p4389.check_field();pts,lines,pidx=p4389.build_h39();assert (len(pts),len(lines))==(280,112)
    lidx={frozenset(L):i for i,L in enumerate(lines)}
    def point_perm(T):return Permutation([pidx[normalise(T(p))] for p in pts])
    def line_perm(pp):return Permutation([lidx[frozenset(pp(i) for i in L)] for L in lines])

    pgens=[point_perm(transvection(v,a)) for v,a in TV]
    assert PermutationGroup(pgens).order()==PSU
    lgens=[line_perm(g) for g in pgens]
    outer=line_perm(point_perm(diag_outer))
    G=PermutationGroup(lgens+[outer]);assert G.order()==PGU

    # Dual Q(5,3): each H point gives a Q-line consisting of the four H-lines through it.
    thru=[[] for _ in pts]
    for li,L in enumerate(lines):
        for p in L:thru[p].append(li)
    assert set(map(len,thru))=={4}
    qlines=[frozenset(x) for x in thru];qadj=[set() for _ in range(112)]
    for L in qlines:
        for a,b in itertools.combinations(L,2):qadj[a].add(b);qadj[b].add(a)
    assert set(map(len,qadj))=={30}
    nonpairs=[(a,b) for a in range(112) for b in range(a+1,112) if b not in qadj[a]]
    assert len(nonpairs)==4536
    a,b=nonpairs[0];rungs=sorted(qadj[a]&qadj[b]);assert len(rungs)==10

    Ga=G.stabilizer(a);Gab=Ga.stabilizer(b);assert Gab.order()==1440
    # Build one element swapping the two points exactly: t maps a->b; h fixes b and maps t(b)->a.
    t=next(g for g in G.orbit_transversal(a) if g(a)==b);c=t(b)
    Gb=G.stabilizer(b);h=next(g for g in Gb.orbit_transversal(c) if g(c)==a)
    swap=t*h;assert (swap(a),swap(b))==(b,a)
    Gset=PermutationGroup(Gab.generators+[swap]);assert Gset.order()==2880
    assert PGU//Gset.order()==4536

    ridx={x:i for i,x in enumerate(rungs)};rg=[]
    for g in Gset.generators:
        arr=[ridx[g(x)] for x in rungs];rg.append(Permutation(arr))
    R=PermutationGroup(rg);assert R.order()==1440
    assert Gset.order()//R.order()==2
    ord3=len(orbit_tuple((0,1,2),R.generators,False));sub3=len(orbit_tuple((0,1,2),R.generators,True))
    assert (ord3,sub3)==(720,120)
    global_orbit=4536*sub3;assert global_orbit==544320 and PGU//global_orbit==24

    out={
      'pass':4574,'status':'OBSERVED_EXACT_REPRODUCTION',
      'construction':'dual action on the 112 totally isotropic lines of the explicit GF(9) H(3,9) construction',
      'generators':{'four_unitary_transvections':[{'v':list(v),'a':a} for v,a in TV],
                    'PSU_order':PSU,'outer_unitary_diagonal':'diag(3,1,1,1)','full_projective_order':PGU},
      'noncollinear_pair_action':{'orbit_size':4536,'pointwise_stabilizer_order':1440,'setwise_stabilizer_order':2880,
                                  'common_neighbor_rungs':10,'rung_image_order':1440,'rung_kernel_order':2,
                                  'ordered_distinct_triple_orbit_size':720,'unordered_3_subset_orbit_size':120,
                                  'three_transitive_on_rungs':True},
      'global_prism_action':{'transitive':True,'orbit_size':544320,'stabilizer_order':24},
      'boundary':'Exact finite permutation action on Q(5,3). The order-1440 rung image is not assigned an abstract group name from order alone.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
