#!/usr/bin/env python3
"""Rule out ovoid deficiency six in W(3,5).

The previous support theorem proves every nonzero defect d of an ovoid-size
set satisfies A_line d = 4d and deficiency delta >= 5.  Here delta=6 is
classified completely.

Let M=max |d_i|.  At a coordinate with value M, the distance-two shell sums
to -5M.  The entire negative mass is only delta=6, so 5M<=6 and M=1.
Thus every nonzero coordinate is +/-1 and the positive/negative supports P,N
both have size six.

For p in P the eigen-equation says deg_P(p)-deg_N(p)=4, and similarly on N.
Hence every vertex in either six-set has internal degree at least four.  Any
six-vertex graph of minimum degree four contains a triangle.  In a generalized
quadrangle three pairwise intersecting lines are concurrent; a line outside
that pencil meets at most one pencil line.  Such an outside line could then
meet at most 1+2=3 of the other five support lines, contradiction.  Therefore
P and N are full six-line pencils.  They cannot have collinear centers because
then the common hinge line would belong to both supports.  Conversely two full
pencils at noncollinear centers have the required internal K6s and six cross
intersections.

So every hypothetical deficiency-six set has, up to PSp(4,5), one target:
  occupancy 0 on the six lines through a,
  occupancy 2 on the six lines through noncollinear b,
  occupancy 1 on all other 144 lines.

This program constructs W(3,5), verifies transvection transitivity on all
156*125=19,500 ordered noncollinear point pairs, and exactly backtracks the
representative target.  It is infeasible.  Therefore def(W(3,5)) >= 7.
The existing explicit Holotrade witness still gives def(W(3,5)) <= 12.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260828_Q5_DEFICIENCY6_NOGO.json'
Q=5

def norm(v):
    i=next(k for k,x in enumerate(v) if x%Q); z=pow(v[i]%Q,-1,Q)
    return tuple((z*x)%Q for x in v)
def form(u,v):
    return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%Q

def geometry():
    pts=sorted({norm(v) for v in itertools.product(range(Q),repeat=4) if any(v)})
    idx={v:i for i,v in enumerate(pts)}; lines=set()
    for ia,ib in itertools.combinations(range(len(pts)),2):
        a,b=pts[ia],pts[ib]
        if form(a,b): continue
        S=set()
        for s,t in itertools.product(range(Q),repeat=2):
            if s==t==0: continue
            S.add(idx[norm(tuple((s*a[k]+t*b[k])%Q for k in range(4)))])
        if len(S)==Q+1: lines.add(tuple(sorted(S)))
    lines=sorted(lines)
    assert len(pts)==len(lines)==156 and all(len(L)==6 for L in lines)
    return pts,idx,lines

def solve_target(lines,pls,target,size=26):
    allowed={p for p in range(156) if all(target[l]>0 for l in pls[p])}
    cand=[[p for p in L if p in allowed] for L in lines]
    cnt=[0]*156; chosen=[]; inside=[False]*156; sols=[]; nodes=0
    def rec():
        nonlocal nodes
        nodes+=1
        if sols or len(chosen)>size:return
        rem=sum(target[l]-cnt[l] for l in range(156))
        if len(chosen)+(rem+5)//6>size:return
        unmet=[]
        for l,t in enumerate(target):
            if cnt[l]>t:return
            need=t-cnt[l]
            if need:
                F=[p for p in cand[l] if not inside[p] and
                   all(cnt[j]<target[j] for j in pls[p])]
                if len(F)<need:return
                unmet.append((len(F),-need,l,F))
        if not unmet:
            if len(chosen)==size:sols.append(tuple(sorted(chosen)))
            return
        _,ng,_,F=min(unmet); need=-ng
        for sub in itertools.combinations(F,need):
            d=Counter()
            for p in sub:
                for j in pls[p]:d[j]+=1
            if any(cnt[j]+z>target[j] for j,z in d.items()):continue
            for p in sub:chosen.append(p);inside[p]=True
            for j,z in d.items():cnt[j]+=z
            rec()
            for j,z in d.items():cnt[j]-=z
            for _ in sub:inside[chosen.pop()]=False
            if sols:return
    rec();return sols,nodes

def transvection_perm(pts,idx,v):
    out=[]
    for x in pts:
        c=form(x,v)
        y=norm(tuple((x[k]+c*v[k])%Q for k in range(4)))
        out.append(idx[y])
    return tuple(out)

def main():
    pts,idx,lines=geometry(); pls=[[] for _ in range(156)]
    for li,L in enumerate(lines):
        for p in L:pls[p].append(li)
    assert all(len(x)==6 for x in pls)
    # Point collinearity graph has degree q(q+1)=30, hence 125 noncollinear mates.
    col=[set() for _ in range(156)]
    for L in lines:
        for a,b in itertools.combinations(L,2):col[a].add(b);col[b].add(a)
    assert {len(x) for x in col}=={30}
    a=0; b=next(x for x in range(1,156) if x not in col[a])
    assert not (set(pls[a])&set(pls[b]))

    # Verify the symplectic transvections are transitive on ordered noncollinear pairs.
    gens=[transvection_perm(pts,idx,v) for v in pts]
    orb={(a,b)}; q=deque([(a,b)])
    while q:
        x,y=q.popleft()
        for g in gens:
            z=(g[x],g[y])
            if z not in orb:orb.add(z);q.append(z)
    assert len(orb)==156*125==19500
    assert all(y not in col[x] and x!=y for x,y in orb)

    target=[1]*156
    for l in pls[a]:target[l]=0
    for l in pls[b]:target[l]=2
    assert Counter(target)==Counter({1:144,0:6,2:6})
    assert sum(target)==156==(Q+1)*(Q*Q+1)
    sols,nodes=solve_target(lines,pls,target)
    assert not sols

    out={
      'schema':'w33.20260828.q5-deficiency6-nogo.v1','status':'PASS',
      'classification':{
        'max_abs_entry':1,
        'reason':'distance-two shell sum is -5M while total negative mass is 6, so 5M<=6',
        'positive_support':6,'negative_support':6,
        'support_geometry':'each sign support is a full six-line pencil; centers are noncollinear',
        'unique_orbit_target':'0 on one full pencil, 2 on a noncollinear full pencil, 1 elsewhere'},
      'orbit_check':{'ordered_noncollinear_pairs':len(orb),'expected':19500,'transitive':True},
      'representative':{'centers':[a,b],'profile':{'0':6,'1':144,'2':6},
                        'backtrack_nodes':nodes,'feasible':False},
      'q5_consequence':{'deficiency_6_possible':False,'proved_lower_bound':7,
                        'known_upper_bound':12,'certified_interval':[7,12]},
      'theorem':'Every deficiency-six defect in W(3,5) would be the difference of two full line pencils at noncollinear centers. PSp(4,5) is transitive on the 19,500 ordered noncollinear center pairs, and the representative occupancy target has no 26-point realization. Hence def(W(3,5))>=7.',
      'boundary':'The upper bound 12 is the existing explicit Holotrade feasible witness. This pass does not claim deficiency 7 is attainable.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','q5_interval':[7,12],'pair_orbit':len(orb),'nodes':nodes}))
if __name__=='__main__':main()
