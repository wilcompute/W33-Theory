#!/usr/bin/env python3
"""W(3,5) deficiency-nine frontier.

At deficiency delta=9 the defect equation A_line d = 4d forces |d_i|<=1:
if t=max d_i>0 then 4t is the neighbour sum at that line, while the total
remaining positive mass is at most 9-t, so 4t<=9-t and t=1.  Thus a hypothetical
26-set has profile 0^9 1^138 2^9 and d is +/-1 on two nine-line supports P,N.
For l in P,N:
    deg_P(l)-deg_N(l)=4,   deg_N(l)-deg_P(l)=4,
and every zero line meets P and N equally often.

This pass freezes two inequivalent exact eigen-support strata and rejects one
point-incidence realization target from each.  It does NOT prove that the two
strata exhaust all nine-mass eigen-defects, so def(W(3,5)) remains in [9,12].
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260828_Q5_DEFICIENCY9_FRONTIER.json'
Q=5
TYPE_A=([32,33,34,39,42,90,108,121,149],[5,11,17,55,72,77,78,80,112])
TYPE_B=([0,36,41,43,44,45,59,103,122],[1,62,81,130,131,136,146,149,151])

def norm(v):
    i=next(k for k,x in enumerate(v) if x%Q);z=pow(v[i]%Q,-1,Q)
    return tuple((z*x)%Q for x in v)
def form(u,v):return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%Q
def geometry():
    pts=sorted({norm(v) for v in itertools.product(range(Q),repeat=4) if any(v)})
    idx={v:i for i,v in enumerate(pts)};lines=set()
    for a,b in itertools.combinations(range(len(pts)),2):
        if form(pts[a],pts[b]):continue
        S=set()
        for s,t in itertools.product(range(Q),repeat=2):
            if s==t==0:continue
            S.add(idx[norm(tuple((s*pts[a][k]+t*pts[b][k])%Q for k in range(4)))])
        if len(S)==6:lines.add(tuple(sorted(S)))
    return sorted(lines)
def solve_target(lines,pls,target):
    allowed={p for p in range(156) if all(target[l]>0 for l in pls[p])}
    cand=[[p for p in L if p in allowed] for L in lines];cnt=[0]*156;ch=[];inside=[False]*156;nodes=0;sol=[]
    def rec():
        nonlocal nodes
        nodes+=1
        if sol or len(ch)>26:return
        unmet=[]
        for l,t in enumerate(target):
            if cnt[l]>t:return
            need=t-cnt[l]
            if need:
                F=[p for p in cand[l] if not inside[p] and all(cnt[j]<target[j] for j in pls[p])]
                if len(F)<need:return
                unmet.append((len(F),-need,l,F))
        if not unmet:
            if len(ch)==26:sol.append(tuple(sorted(ch)))
            return
        _,ng,_,F=min(unmet);need=-ng
        for sub in itertools.combinations(F,need):
            d=Counter()
            for p in sub:
                for j in pls[p]:d[j]+=1
            if any(cnt[j]+z>target[j] for j,z in d.items()):continue
            for p in sub:ch.append(p);inside[p]=True
            for j,z in d.items():cnt[j]+=z
            rec()
            for j,z in d.items():cnt[j]-=z
            for _ in sub:inside[ch.pop()]=False
            if sol:return
    rec();return sol,nodes
def analyse(lines,P,N):
    LS=[set(L) for L in lines]
    def meet(i,j):return bool(LS[i]&LS[j])
    dp=[sum(meet(i,j) for j in P if j!=i) for i in P]
    dn=[sum(meet(i,j) for j in N if j!=i) for i in N]
    cross=[(i,j) for i in P for j in N if meet(i,j)]
    d=[0]*156
    for i in P:d[i]=1
    for i in N:d[i]=-1
    for i in range(156):
        s=sum(d[j] for j in range(156) if i!=j and meet(i,j))
        assert s==4*d[i]
    target=[1+x for x in d]
    return Counter(dp),Counter(dn),cross,target
def main():
    lines=geometry();assert len(lines)==156
    pls=[[] for _ in range(156)]
    for li,L in enumerate(lines):
        for p in L:pls[p].append(li)
    rows=[]
    for name,(P,N) in [('A',TYPE_A),('B',TYPE_B)]:
        dp,dn,cross,target=analyse(lines,P,N)
        sol,nodes=solve_target(lines,pls,target);assert not sol
        rows.append({'type':name,'P':P,'N':N,'P_degree_profile':dict(dp),'N_degree_profile':dict(dn),
                     'cross_edges':cross,'cross_count':len(cross),'realizable_26_set':False,'backtracking_nodes':nodes})
    assert rows[0]['P_degree_profile']=={4:9} and rows[0]['cross_count']==0 and rows[0]['backtracking_nodes']==118
    assert rows[1]['P_degree_profile']=={4:5,5:4} and rows[1]['cross_count']==4 and rows[1]['backtracking_nodes']==158
    out={'schema':'w33.20260828.q5-deficiency9-frontier.v1','status':'PASS',
         'forcedProfile':{'missed':9,'single':138,'double':9,'defectValues':'{-1,0,+1}'},
         'supportEquations':'A_line d=4d; on P, deg_P-deg_N=4; on N, deg_N-deg_P=4; outside support the two neighbour counts agree.',
         'strata':rows,
         'reading':'Nine-mass eigen-defects exist, so support theory alone no longer rules out the deficiency. Two inequivalent exact support strata have frozen infeasible incidence targets.',
         'certifiedInterval':[9,12],
         'boundary':'The two frozen support strata are not proved exhaustive. This pass does not prove def(W(3,5))>=10.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','strata':[(r['type'],r['cross_count'],r['backtracking_nodes']) for r in rows],'interval':[9,12]}))
if __name__=='__main__':main()
