#!/usr/bin/env python3
"""Pass 4809 — complete the minimum nonlocal Levi-homology shell.

Pass4808 proved that C^perp/L has triangle-lift distance 6 and exhibited 360
projective K_{3,3} witnesses, without claiming completeness.  This producer
closes that boundary exactly.

A local line syndrome has minimum lift cost 0,1,2 with multiplicities 1,20,60.
For total cost six the only active-line patterns are
  (n1,n2)=(6,0),(4,1),(2,2),(0,3).
Before coefficient search, every nonzero local coordinate must occur at a GQ
point shared by another active line.  Exhaustion of all active line subsets and
all local minimum states leaves exactly 360 projective solutions, all in the
(6,0) pattern.  Their six active lines induce K3,3.  Thus the Pass4808 family
is the complete projective minimum shell.

The 27-line intersection graph has automorphism group 51840.  A deterministic
generator harvest from NetworkX followed by SymPy gives derived subgroup order
25920.  Both groups are transitive on the 360 supports, giving stabilizers 144
and 72 respectively.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
from sympy.combinatorics import Permutation, PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4809_COMPLETE_WEIGHT6_HOMOLOGY_SHELL.json'

def Qm(v):
    x1,x2,x3,x4,x5,x6=v
    return (x1*x2+x3*x4+x5+x5*x6+x6)&1

def bits(x):return tuple((x>>i)&1 for i in range(6))

def geometry():
    qp=[x for x in range(1,64) if Qm(bits(x))==0]
    ql=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    lines=[tuple(i for i,Q in enumerate(ql) if p in Q) for p in qp]
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if len(set(lines[i])&set(lines[j]))==1:G.add_edge(i,j)
    assert len(qp)==27 and len(ql)==45 and set(dict(G.degree()).values())=={10}
    return lines,G

def local_states():
    T=list(itertools.combinations(range(5),3));M=np.zeros((5,10),dtype=int)
    for j,t in enumerate(T):M[list(t),j]=1
    best={}
    for x in itertools.product(range(3),repeat=10):
        a=np.array(x,dtype=int);z=tuple(int(v) for v in (M@a)%3);w=int(np.count_nonzero(a))
        best[z]=min(best.get(z,99),w)
    by={w:[z for z,c in best.items() if c==w] for w in (0,1,2)}
    assert {w:len(v) for w,v in by.items()}=={0:1,1:20,2:60}
    return by

def possible_states_for_active(lines,active,states,cost):
    # A nonzero coordinate of a local state can only survive global point
    # conservation if that GQ point lies on another active line.
    A=set(active);out={}
    for ell in active:
        shared={p for p in lines[ell] if sum(p in lines[m] for m in A)>=2}
        pos={p:i for i,p in enumerate(lines[ell])}
        out[ell]=[z for z in states[cost[ell]] if all((not z[pos[p]]) or p in shared for p in lines[ell])]
    return out

def conserved(lines,active,zs):
    S=Counter()
    for ell,z in zip(active,zs):
        for k,p in enumerate(lines[ell]):S[p]=(S[p]+z[k])%3
    return all(v%3==0 for v in S.values())

def canonical_projective(zs):
    flat=tuple(v for z in zs for v in z)
    first=next(v for v in flat if v)
    if first==2:flat=tuple((2*v)%3 for v in flat)
    return flat

def complete_shell(lines,states):
    patterns=[(0,3),(2,2),(4,1),(6,0)]
    checked={};survivors={};supports=set()
    for n1,n2 in patterns:
        n=n1+n2;raw=0;sol=set()
        for active in itertools.combinations(range(27),n):
            for ones in itertools.combinations(active,n1):
                one=set(ones);cost={e:(1 if e in one else 2) for e in active}
                cand=possible_states_for_active(lines,active,states,cost)
                if any(not cand[e] for e in active):continue
                raw+=1
                for zs in itertools.product(*(cand[e] for e in active)):
                    if conserved(lines,active,zs):sol.add((active,canonical_projective(zs)))
        checked[f'{n1},{n2}']=raw;survivors[f'{n1},{n2}']=len(sol)
        if (n1,n2)==(6,0):supports={frozenset(a) for a,_ in sol}
        else:assert not sol
    assert len(supports)==360
    return checked,survivors,supports

def group_orbits(G,supports):
    GM=nx.algorithms.isomorphism.GraphMatcher(G,G)
    gens=[];H=PermutationGroup(Permutation(list(range(27))))
    aut_count=0
    for m in GM.isomorphisms_iter():
        aut_count+=1
        p=Permutation([m[i] for i in range(27)])
        if not H.contains(p):
            gens.append(p);H=PermutationGroup(gens)
            if H.order()==51840:break
    assert H.order()==51840
    D=H.derived_subgroup();assert D.order()==25920
    seed=next(iter(supports))
    def orb(group):
        seen={seed};q=[seed]
        while q:
            S=q.pop()
            for g in group.generators:
                T=frozenset(int(g(i)) for i in S)
                if T not in seen:seen.add(T);q.append(T)
        return seen
    oH=orb(H);oD=orb(D)
    assert oH==supports and oD==supports
    return {'full_order':51840,'PSp_order':25920,'full_orbit':len(oH),'PSp_orbit':len(oD),
            'full_stabilizer':51840//len(oH),'PSp_stabilizer':25920//len(oD)}

def main():
    lines,G=geometry();states=local_states();checked,surv,supports=complete_shell(lines,states)
    for S in supports:
        H=G.subgraph(S);assert H.number_of_edges()==9 and nx.is_bipartite(H) and set(dict(H.degree()).values())=={3}
    gr=group_orbits(G,supports)
    out={'pass':4809,'quotient':'C^perp/L ~= H_1(Levi(GQ(4,2));F3)','minimum_lift_weight':6,
      'projective_minimum_classes':360,'all_minimum_classes_are_induced_K33':True,
      'cost_patterns_surviving':surv,'active_subset_cases_after_support_filter':checked,
      'PSp_orbits':1,'PGSp_orbits':1,**gr,
      'theorem':'The 360 induced K3,3 witnesses of Pass4808 are the complete projective minimum-lift shell of C^perp/L. No mixed cost-1/cost-2 pattern survives. The shell is one orbit under PSp(4,3) and also one orbit under the full order-51840 outer action, with stabilizers 72 and 144.',
      'boundary':'This classifies quotient classes in the minimum triangle-lift metric. It does not identify the quotient with an unrelated 360-object merely from the count.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
