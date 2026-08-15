#!/usr/bin/env python3
"""Pass5305: full orbital rank of the 2340-word q5 K0 minimum shell.

Pass5298 showed the 2340 minimum K0 words form one transitive few-distance shell.
This pass computes the actual PSp4(5) orbital refinement.  Acting on labels
(p,{l1,l2}) (a W-point plus an unordered pair of its six incident W-lines), the
group has order 4,680,000 and is transitive on 2340 labels.  A point in this
action has stabilizer order 2000.  Its suborbits give 21 orbitals, so the six
nonzero Hamming distances are a coarse fusion of a rank-21 coherent configuration.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5305_K0_MINIMUM_SHELL_ORBITALS.json'

def main():
    G=build_W(5);pts=G['pts'];pi={p:i for i,p in enumerate(pts)};lines=[tuple(sorted(L)) for L in G['lines']];lk={L:i for i,L in enumerate(lines)}
    byp=[[] for _ in pts]
    for l,L in enumerate(lines):
        for p in L:byp[p].append(l)
    labels=[];idx={}
    for p in range(156):
        for a,b in itertools.combinations(sorted(byp[p]),2):idx[(p,a,b)]=len(labels);labels.append((p,a,b))
    assert len(labels)==2340
    def norm(v):
        for x in v:
            if x:
                s=pow(x,-1,5);return tuple(s*y%5 for y in v)
        raise ValueError
    def sp(u,v):return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%5
    vs=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,0,1))
    gens=[]
    for v in vs:
        pp=[]
        for x in pts:
            a=sp(x,v);pp.append(pi[norm(tuple((x[k]+a*v[k])%5 for k in range(4)))])
        lp=[lk[tuple(sorted(pp[p] for p in L))] for L in lines]
        arr=[]
        for p,a,b in labels:
            aa,bb=sorted((lp[a],lp[b]));arr.append(idx[(pp[p],aa,bb)])
        gens.append(Permutation(arr))
    GP=PermutationGroup(gens);assert GP.order()==4680000
    assert len(GP.orbit(0))==2340
    St=GP.stabilizer(0);assert St.order()==2000
    orbs=St.orbits();assert len(orbs)==21
    # Actual apartment words, for Hamming-distance fusion.
    stars=[0]*len(G['flags'])
    for a,es in enumerate(G['apt_edges']):
        bit=1<<a
        for e in es:stars[e]|=bit
    fi={f:i for i,f in enumerate(G['flags'])};words=[]
    for p,a,b in labels:words.append(stars[fi[(p,a)]]^stars[fi[(p,b)]])
    assert {w.bit_count() for w in words}=={1000}
    records=[]
    for O in orbs:
        rep=min(O);d=(words[0]^words[rep]).bit_count();records.append((len(O),d))
    subdegrees=Counter(n for n,d in records);fusion=Counter(records)
    assert subdegrees==Counter({50:9,1:3,4:3,125:3,500:3})
    want=Counter({(1,0):1,(1,1000):2,(4,1000):3,(50,1840):1,(50,1920):4,(50,1960):4,(125,1984):1,(125,1992):2,(500,1992):3})
    assert fusion==want
    out={'pass':5305,'status':'THEOREM_Q5_K0_MINIMUM_SHELL_HAS_RANK21_PSP4_ORBITAL_CONFIGURATION',
      'vertices':2340,'group_order':4680000,'point_stabilizer_order':2000,'orbital_rank':21,
      'subdegree_histogram':{str(k):v for k,v in sorted(subdegrees.items())},
      'distance_fusion':[{'subdegree':n,'distance':d,'number_of_orbitals':m} for (n,d),m in sorted(fusion.items())],
      'conclusion':'The six nonzero Hamming distances from Pass5298 fuse multiple PSp4(5) orbitals; the true transitive coherent configuration has rank21.',
      'boundary':'Orbital partition/rank theorem. Intersection tensors/eigenmatrices of the rank21 coherent configuration are not yet tabulated.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
