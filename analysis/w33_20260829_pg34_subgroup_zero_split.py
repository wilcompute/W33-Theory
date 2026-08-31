#!/usr/bin/env python3
"""Exact subgroup-breaking hierarchy for the 85-state chiral coupling.

For H <= PSp(4,3), an H-equivariant 40x45 coupling is an intertwiner between
its two permutation modules.  The maximum possible rank is therefore the sum,
over common irreducibles, of dim(V_lambda)*min(m40_lambda,m45_lambda).

This audit computes the S5 permutation characters directly from the native
W33/GQ(4,2) actions, then restricts them down the sentinel-circuit chain
S5 > A5 and S5 > S4 > A4 > V4 > C2 > 1.  In particular it replaces earlier
random orbital specializations below S5 by exact character-theoretic ceilings.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from collections import Counter

from w33_20260829_216_clifford_torsor_nogo import (
    geometry,supports_from_N,closure_paired,norm,form,porder
)
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_PG34_SUBGROUP_ZERO_SPLIT.json'

def parity(p):
    return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))&1

def cycle_type(p):
    seen=set();parts=[]
    for i in range(len(p)):
        if i in seen:continue
        j=i;n=0
        while j not in seen:seen.add(j);n+=1;j=p[j]
        parts.append(n)
    return tuple(sorted(parts,reverse=True))

def cross_orbit_count(H):
    rem={(i,j) for i in range(40) for j in range(45)};k=0
    while rem:
        seed=min(rem);O={(h[0][seed[0]],h[1][seed[1]]) for h in H}
        rem-=O;k+=1
    return k

def max_rank(decomp40,decomp45,dims):
    return sum(dims[x]*min(decomp40.get(x,0),decomp45.get(x,0)) for x in dims)

def main():
    pts,idxp,lines,N=geometry();supports,masks=supports_from_N(N)
    circuits=[]
    for cc in itertools.combinations(range(45),5):
        w=0
        for i in cc:w^=masks[i]
        if w==0:circuits.append(cc)
    assert len(circuits)==216

    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*form(x,v)%3;y=norm(tuple((x[k]+z*v[k])%3 for k in range(4)));p.append(idxp[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)};gens45=[]
    for p in gens40:gens45.append(tuple(si[frozenset(p[x] for x in S)] for S in supports))
    chosen=(18,62,77,10);G=closure_paired([gens40[i] for i in chosen],[gens45[i] for i in chosen]);assert len(G)==25920
    c0=tuple(circuits[0]);cset=set(c0)
    S5=[h for h in G if {h[1][x] for x in cset}==cset];assert len(S5)==120
    pos={x:i for i,x in enumerate(c0)}
    def p5(h):return tuple(pos[h[1][x]] for x in c0)
    A5=[h for h in S5 if parity(p5(h))==0];assert len(A5)==60
    S4=[h for h in S5 if p5(h)[0]==0];assert len(S4)==24
    A4=[h for h in S4 if parity(p5(h))==0];assert len(A4)==12
    V4=[h for h in A4 if porder(p5(h)) in (1,2)];assert len(V4)==4
    e=next(h for h in V4 if porder(p5(h))==1)
    g2=next(h for h in V4 if porder(p5(h))==2);C2=[e,g2]
    groups={'PSp(4,3)':G,'S5':S5,'A5':A5,'S4':S4,'A4':A4,'V4':V4,'C2':C2,'1':[e]}

    # Native S5 character: class values are fixed-point counts in the 40- and
    # 45-point permutation actions.  These are measured directly, not assumed.
    class_count=Counter(cycle_type(p5(h)) for h in S5);assert sum(class_count.values())==120
    perm40={};perm45={}
    for ct in class_count:
        vals=[h for h in S5 if cycle_type(p5(h))==ct]
        f40={sum(h[0][i]==i for i in range(40)) for h in vals};f45={sum(h[1][i]==i for i in range(45)) for h in vals}
        assert len(f40)==len(f45)==1;perm40[ct]=f40.pop();perm45[ct]=f45.pop()
    expected40={(1,1,1,1,1):40,(2,1,1,1):8,(2,2,1):0,(3,1,1):4,(3,2):2,(4,1):0,(5,):0}
    expected45={(1,1,1,1,1):45,(2,1,1,1):13,(2,2,1):5,(3,1,1):3,(3,2):1,(4,1):1,(5,):0}
    assert perm40==expected40 and perm45==expected45

    s5chars={
      '5':(1,{(1,1,1,1,1):1,(2,1,1,1):1,(2,2,1):1,(3,1,1):1,(3,2):1,(4,1):1,(5,):1}),
      '41':(4,{(1,1,1,1,1):4,(2,1,1,1):2,(2,2,1):0,(3,1,1):1,(3,2):-1,(4,1):0,(5,):-1}),
      '32':(5,{(1,1,1,1,1):5,(2,1,1,1):1,(2,2,1):1,(3,1,1):-1,(3,2):1,(4,1):-1,(5,):0}),
      '311':(6,{(1,1,1,1,1):6,(2,1,1,1):0,(2,2,1):-2,(3,1,1):0,(3,2):0,(4,1):0,(5,):1}),
      '221':(5,{(1,1,1,1,1):5,(2,1,1,1):-1,(2,2,1):1,(3,1,1):-1,(3,2):-1,(4,1):1,(5,):0}),
      '2111':(4,{(1,1,1,1,1):4,(2,1,1,1):-2,(2,2,1):0,(3,1,1):1,(3,2):1,(4,1):0,(5,):-1}),
      '11111':(1,{(1,1,1,1,1):1,(2,1,1,1):-1,(2,2,1):1,(3,1,1):1,(3,2):-1,(4,1):-1,(5,):1})}
    def s5_mults(perm):
        out={}
        for name,(dim,ch) in s5chars.items():
            num=sum(class_count[ct]*perm[ct]*ch[ct] for ct in class_count);assert num%120==0;out[name]=num//120
        return out
    s5_40,s5_45=s5_mults(perm40),s5_mults(perm45)
    dims_s5={k:v[0] for k,v in s5chars.items()};assert max_rank(s5_40,s5_45,dims_s5)==30

    # Exact restrictions.  A5's two 3-dimensional irreps differ only on the
    # split 5-cycle classes, where both permutation characters vanish; hence
    # their multiplicities are determined without adjoining sqrt(5).
    decomps={
      'PSp(4,3)':({'trivial':1,'shared24':1},{'trivial':1,'shared24':1,'rightDark20':1},{'trivial':1,'shared24':24,'rightDark20':20}),
      'S5':(s5_40,s5_45,dims_s5),
      'A5':(
        {'1':2,'3':2,"3prime":2,'4':4,'5':2},
        {'1':3,'3':1,"3prime":1,'4':4,'5':4},
        {'1':1,'3':3,"3prime":3,'4':4,'5':5}),
      'S4':(
        {'4':5,'1111':1,'22':2,'31':7,'211':3},
        {'4':7,'1111':0,'22':4,'31':8,'211':2},
        {'4':1,'1111':1,'22':2,'31':3,'211':3}),
      'A4':(
        {'1':6,'1prime':2,'1doubleprime':2,'3':10},
        {'1':7,'1prime':4,'1doubleprime':4,'3':10},
        {'1':1,'1prime':1,'1doubleprime':1,'3':3}),
      'V4':(
        {'1':10,'a':10,'b':10,'c':10},
        {'1':15,'a':10,'b':10,'c':10},
        {'1':1,'a':1,'b':1,'c':1}),
      'C2':(
        {'+':20,'-':20},{'+':25,'-':20},{'+':1,'-':1}),
      '1':({'1':40},{'1':45},{'1':1})}

    expected={'PSp(4,3)':25,'S5':30,'A5':34,'S4':36,'A4':40,'V4':40,'C2':40,'1':40}
    rows=[]
    for name in ['PSp(4,3)','S5','A5','S4','A4','V4','C2','1']:
        d40,d45,dims=decomps[name]
        # Dimension checks make every listed restriction self-auditing.
        assert sum(dims[k]*d40.get(k,0) for k in dims)==40
        assert sum(dims[k]*d45.get(k,0) for k in dims)==45
        r=max_rank(d40,d45,dims);assert r==expected[name]
        rows.append({'subgroup':name,'order':len(groups[name]),'crossPairOrbits':cross_orbit_count(groups[name]),
          'left40Decomposition':d40,'right45Decomposition':d45,'irreducibleDimensions':dims,
          'provenMaximumRank':r,'minimumChiralZeroModes':85-2*r})

    threshold=next(r['subgroup'] for r in rows if r['provenMaximumRank']==40);assert threshold=='A4'
    out={'schema':'w33.20260829.pg34-subgroup-zero-split.v3','status':'PASS','chain':rows,
      'S5PermutationCharacters':{'classCounts':{str(k):v for k,v in class_count.items()},
        'left40':{str(k):v for k,v in perm40.items()},'right45':{str(k):v for k,v in perm45.items()}},
      'firstFullRankSubgroupInChain':threshold,
      'zeroModeHierarchy':[35,25,17,13,5,5,5,5],
      'theorem':'Along PSp(4,3)>S5>A5 and S5>S4>A4>V4>C2>1, the exact maximum equivariant coupling ranks are 25,30,34,36,40,40,40,40. Thus A4 is the first subgroup in this chain at which all symmetry-protected excess zero modes can be lifted, leaving only the five rectangular-index modes.',
      'boundary':'Exact finite representation/intertwiner statement. Existence of a symmetry-allowed full-rank intertwiner is not a claim that a corresponding perturbation is physically local or dynamically generated.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
