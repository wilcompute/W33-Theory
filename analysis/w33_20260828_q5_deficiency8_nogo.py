#!/usr/bin/env python3
"""Exact no-go for deficiency eight in W(3,5).

Input from the earlier defect theorem: for a 26-point candidate S, the line
occupancy defect d=N chi_S-1 satisfies A_line d=4d and has equal positive and
negative mass equal to the number of missed lines.

At mass eight, a maximum-coordinate estimate gives 4m <= 8-m, hence m=1.
Thus d is +/-1 valued with eight positive and eight negative lines.  For a
positive line P, 4 = deg_+(P)-deg_-(P), so each sign support has induced
minimum degree at least four.  The same equation shows that once the internal
degree is exactly four there can be no cross-sign intersections.

Classify an eight-line set T of minimum intersection degree four relative to a
line ell in T.  Let r<=3 be the number of other T-lines disjoint from ell and
partition the 7-r neighbours of ell by their intersection point on ell.
Different parts are mutually disjoint.

  r=0: a part would need size >=4, but sum 7 forces an overfull pencil.
  r=1: parts have size >=3; the only 3+3 case would require the one disjoint
       line to meet all three members of each part, impossible.
  r=2: parts have size >=2; a size-two part needs four cross incidences but the
       two disjoint lines provide only two total slots into that part.
  r=3: size-two parts are again impossible.  The 3+1 case gives two K4
       pencils joined by a perfect matching, i.e. K4 square K2.  The
       1+1+1+1 case would be K4,4 and requires at least four common
       transversals to three pairwise-disjoint lines.

In W(3,5) the last case does not occur: the exact census for triples of
pairwise-disjoint lines gives 0 or 2 common transversals, never four.  Hence
K4 square K2 is the only support type.

PSp(4,5) is transitive on ordered noncollinear point pairs.  Such a pair gives
six canonically matched line-pairs between the two pencils.  A K4 square K2
support is a choice of four of those six pairs, so testing all C(6,4)=15
choices covers every support orbit without assuming the pair stabilizer is
transitive on four-subsets.  For every choice the set of lines disjoint from
all eight support lines has a unique nonempty 4-core, itself an eight-line
K4 square K2.  This is the only possible opposite-sign support.  Exact binary
occupancy backtracking then rejects all fifteen targets.

Therefore deficiency eight is impossible and def(W(3,5)) >= 9.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260828_Q5_DEFICIENCY8_NOGO.json'
Q=5

def norm(v):
    i=next(k for k,x in enumerate(v) if x%Q); z=pow(v[i]%Q,-1,Q)
    return tuple((z*x)%Q for x in v)
def form(u,v):
    return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%Q

def geometry():
    pts=sorted({norm(v) for v in itertools.product(range(Q),repeat=4) if any(v)})
    idx={v:i for i,v in enumerate(pts)}; lines=set()
    for a,b in itertools.combinations(range(len(pts)),2):
        if form(pts[a],pts[b]): continue
        S=set()
        for s,t in itertools.product(range(Q),repeat=2):
            if s==t==0: continue
            S.add(idx[norm(tuple((s*pts[a][k]+t*pts[b][k])%Q for k in range(4)))])
        if len(S)==Q+1: lines.add(tuple(sorted(S)))
    return pts,sorted(lines)

def solve_target(lines,pls,target,size=26):
    n=len(pls); allowed={p for p in range(n) if all(target[l]>0 for l in pls[p])}
    cand=[[p for p in L if p in allowed] for L in lines]
    cnt=[0]*len(lines); chosen=[]; inside=[False]*n; nodes=0
    def rec():
        nonlocal nodes
        nodes+=1
        if len(chosen)>size:return False
        unmet=[]; rem=0
        for l,t in enumerate(target):
            if cnt[l]>t:return False
            need=t-cnt[l]; rem+=need
            if need:
                F=[p for p in cand[l] if not inside[p] and all(cnt[j]<target[j] for j in pls[p])]
                if len(F)<need:return False
                unmet.append((len(F),-need,l,F))
        if not unmet:return len(chosen)==size
        if len(chosen)+math.ceil(rem/(Q+1))>size:return False
        _,ng,_,F=min(unmet); need=-ng
        for sub in itertools.combinations(F,need):
            d=Counter()
            for p in sub:
                for j in pls[p]:d[j]+=1
            if any(cnt[j]+z>target[j] for j,z in d.items()):continue
            for p in sub:chosen.append(p);inside[p]=True
            for j,z in d.items():cnt[j]+=z
            ok=rec()
            for j,z in d.items():cnt[j]-=z
            for _ in sub:inside[chosen.pop()]=False
            if ok:return True
        return False
    return rec(),nodes,len(allowed)

def main():
    pts,lines=geometry(); n=len(pts)
    assert n==len(lines)==156
    pls=[[] for _ in range(n)]
    for li,L in enumerate(lines):
        for p in L:pls[p].append(li)
    ladj=[set() for _ in range(n)]
    for p in range(n):
        for a,b in itertools.combinations(pls[p],2):ladj[a].add(b);ladj[b].add(a)
    assert {len(x) for x in ladj}=={30}

    # K4,4 alternative dies: line transitivity lets us fix line 0.  Among
    # pairwise-disjoint triples containing 0, common transversal counts are
    # exactly 0 or 2, never the >=4 needed by a K4,4 eight-support.
    non0=[l for l in range(1,n) if l not in ladj[0]]
    tr=Counter()
    for a,b in itertools.combinations(non0,2):
        if b in ladj[a]:continue
        tr[len(ladj[0]&ladj[a]&ladj[b])]+=1
    assert tr==Counter({2:3750,0:2500})

    # Fixed representative ordered noncollinear point pair.
    padj=[set() for _ in range(n)]
    for L in lines:
        for a,b in itertools.combinations(L,2):padj[a].add(b);padj[b].add(a)
    x=0; y=next(p for p in range(1,n) if p not in padj[x])
    matching=[]
    for a in pls[x]:
        hit=[b for b in pls[y] if b in ladj[a]]
        assert len(hit)==1; matching.append((a,hit[0]))
    assert len(matching)==6

    rows=[]; maxnodes=0
    for choose in itertools.combinations(range(6),4):
        P=set()
        for i in choose:P.update(matching[i])
        assert len(P)==8 and all(sum(j in P for j in ladj[l])==4 for l in P)
        D={l for l in range(n) if l not in P and all(l not in ladj[p] for p in P)}
        assert len(D)==16
        core=set(D)
        while True:
            bad={l for l in core if sum(j in core for j in ladj[l])<4}
            if not bad:break
            core-=bad
        M=core
        assert len(M)==8 and all(sum(j in M for j in ladj[l])==4 for l in M)
        target=[1]*n
        for l in P:target[l]=0
        for l in M:target[l]=2
        feasible,nodes,allowed=solve_target(lines,pls,target)
        assert not feasible
        maxnodes=max(maxnodes,nodes)
        rows.append({'choice':list(choose),'positive':sorted(P),'negative':sorted(M),
                     'disjoint_pool':len(D),'allowed_points':allowed,
                     'backtracking_nodes':nodes,'feasible':False})
    assert len(rows)==15 and maxnodes<=223

    out={
      'schema':'w33.20260828.q5-deficiency8-nogo.v1','status':'PASS',
      'defect_mass':8,'forced_values':[-1,0,1],
      'support_classification':{
        'minimum_internal_degree':4,
        'possible_abstract_types':['K4 square K2','K4,4'],
        'common_transversal_census_for_disjoint_triples_with_fixed_line':dict(sorted(tr.items())),
        'K4,4_possible_in_W35':False,
        'only_W35_type':'K4 square K2'},
      'orbit_cover':{'ordered_noncollinear_pair_representative':[x,y],
                     'matched_pencil_pairs':matching,'four_of_six_cases':15,
                     'why_complete':'PSp(4,5) is transitive on ordered noncollinear point pairs; all C(6,4) subsets are tested.'},
      'exact_realization_tests':rows,'maximum_backtracking_nodes':maxnodes,
      'theorem':'No deficiency-eight 26-set exists in W(3,5). Hence def(W(3,5)) >= 9.',
      'certified_interval_using_existing_upper_bound':[9,12],
      'boundary':'The existing feasible upper bound 12 is imported from Holotrade. Deficiencies 9,10,11 remain open here.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','def5_lower':9,'cases':15,'max_nodes':maxnodes,'transversals':dict(tr)}))
if __name__=='__main__':main()
