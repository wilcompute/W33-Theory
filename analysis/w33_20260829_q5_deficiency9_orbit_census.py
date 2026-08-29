#!/usr/bin/env python3
"""Exact PSp(4,5) orbit census for the two known mass-nine defect strata.

This advances the deficiency-nine frontier from isolated representatives to
full group orbits.  It intentionally does NOT claim the two orbits exhaust all
mass-nine eigen-defects.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_Q5_DEFICIENCY9_ORBIT_CENSUS.json'
Q=5
A0=((32,33,34,39,42,90,108,121,149),(5,11,17,55,72,77,78,80,112))
B0=((0,36,41,43,44,45,59,103,122),(1,62,81,130,131,136,146,149,151))

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
        if len(S)==Q+1:lines.add(tuple(sorted(S)))
    lines=sorted(lines);ladj=[set() for _ in lines]
    for i,j in itertools.combinations(range(len(lines)),2):
        if set(lines[i])&set(lines[j]):ladj[i].add(j);ladj[j].add(i)
    return pts,idx,lines,ladj

def main():
    pts,idx,lines,adj=geometry();assert len(pts)==len(lines)==156
    # Six projective transvections generate PSp(4,5).
    vecs=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,1,0)]
    gens=[]
    for vv in vecs:
        v=norm(vv);p=[]
        for x in pts:
            c=form(x,v)%Q;y=norm(tuple((x[k]+c*v[k])%Q for k in range(4)));p.append(idx[y])
        gens.append(tuple(p))
    G=PermutationGroup([Permutation(list(p)) for p in gens]);assert G.order()==4680000
    def verify(state):
        P,N=map(set,state);assert len(P)==len(N)==9 and not(P&N)
        d=[1 if i in P else -1 if i in N else 0 for i in range(156)]
        assert all(sum(d[j] for j in adj[i])==4*d[i] for i in range(156))
        return sum(1 for i in P for j in N if j in adj[i])
    def act(s,g):return (tuple(sorted(g[i] for i in s[0])),tuple(sorted(g[i] for i in s[1])))
    def orbit(seed):
        seen={seed};Qd=deque([seed])
        while Qd:
            s=Qd.popleft()
            for g in gens:
                t=act(s,g)
                if t not in seen:seen.add(t);Qd.append(t)
        return seen
    assert verify(A0)==0 and verify(B0)==4
    OA=orbit(A0);OB=orbit(B0);assert not(OA&OB)
    assert len(OA)==390000 and len(OB)==1170000
    out={'schema':'w33.20260829.q5-deficiency9-orbit-census.v1','status':'PASS','ambientGroup':'PSp(4,5)','ambientOrder':4680000,
      'orbits':[{'type':'A','description':'two cross-disjoint L2(3) grid supports','size':len(OA),'stabilizerOrder':12,'crossEdges':0},
                {'type':'B','description':'four cross edges forming a matching; degree profile 4^5 5^4','size':len(OB),'stabilizerOrder':4,'crossEdges':4}],
      'knownSignedDefects':len(OA)+len(OB),'orbitsDisjoint':True,
      'realizability':'The frozen representative occupancy target in each orbit is infeasible as a 26-point set; group transitivity therefore rejects every target in each certified orbit.',
      'certifiedDeficiencyInterval':[9,12],
      'boundary':'This is NOT an exhaustive orbit classification. A third PSp(4,5) orbit of mass-nine eigen-defects has not been ruled out.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','orbitA':len(OA),'orbitB':len(OB),'known':len(OA)+len(OB)}))
if __name__=='__main__':main()
