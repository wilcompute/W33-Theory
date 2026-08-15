#!/usr/bin/env python3
"""Pass5317: refine the Hoffman four-cell layer by the canonical W(D4) subgroup.

Pass5302 gives ten H-orbits on the 715 four-subsets of the 13 Hoffman cells,
where |H|=576.  Pass5308 gives the canonical normal N=W(D4) of order192 with
H/N=C3, and Pass5309 identifies N/Z on the 12 moving cells with the published
tomotope degree-12 action.

Therefore every H-orbit either remains one N-orbit or splits into three equal
N-orbits.  This pass constructs N on the original 13 cell labels from the
published tomotope generators plus the explicit Pass5309 conjugator, enumerates
all four-subset N-orbits, and freezes the exact split:

    10 H-orbits -> 22 W(D4)-orbits,
    4 unsplit + 6 triality triples.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/PART_W33_PASS5302_HOFFMAN_FOURCELL_ORBIT_REDUCTION.json'
OUT=ROOT/'data/PART_W33_PASS5317_HOFFMAN_FOURCELL_TRIALITY_REFINEMENT.json'
F=(0,3,9,5,6,10,1,4,11,2,8,7) # original moving-cell coord -> tomotope coord

def cp(cycles):
    a=list(range(12))
    for cyc in cycles:
        cyc=[x-1 for x in cyc]
        for x,y in zip(cyc,cyc[1:]+cyc[:1]):a[x]=y
    return Permutation(a)

def published_tomotope():
    return PermutationGroup([
      cp([(5,10),(6,9),(7,12),(8,11)]),
      cp([(1,6),(2,5),(3,8),(4,7)]),
      cp([(5,9),(6,10),(7,11),(8,12)]),
      cp([(5,8),(6,7),(9,12),(10,11)])])

def lift_to_13(g):
    fi=[0]*12
    for i,j in enumerate(F):fi[j]=i
    a=[0]*13;a[0]=0
    for c in range(1,13):
        y=F[c-1];y2=g(y);a[c]=1+fi[y2]
    return Permutation(a)

def orbit(G,S):
    S=tuple(sorted(S));return {tuple(sorted(g(i) for i in S)) for g in G.generate_schreier_sims()}

def main():
    T=published_tomotope();assert T.order()==96
    N13=PermutationGroup([lift_to_13(g) for g in T.generators]);assert N13.order()==96
    assert sorted(map(len,N13.orbits()))==[1,12] and N13.orbit(0)=={0}

    rem=set(itertools.combinations(range(13),4));Norbs=[]
    while rem:
        O=orbit(N13,next(iter(rem)));Norbs.append(O);rem-=O
    assert len(Norbs)==22 and sum(map(len,Norbs))==715
    size_hist=Counter(map(len,Norbs))
    assert size_hist==Counter({48:9,12:4,16:4,24:3,3:1,96:1})

    src=json.loads(SRC.read_text())
    rows=[]
    for rec in src['orbit_rank_data']:
        hs=int(rec['orbit_size']);rank=int(rec['rank']);rep=tuple(rec['representative'])
        ns=len(orbit(N13,rep));split=hs//ns
        assert hs%ns==0 and split in (1,3)
        rows.append({'H_orbit_size':hs,'rank':rank,'representative':list(rep),
                     'WD4_orbit_size':ns,'triality_split_factor':split})
    assert Counter(r['triality_split_factor'] for r in rows)==Counter({3:6,1:4})
    rank_orbits=Counter()
    for r in rows:rank_orbits[r['rank']]+=r['triality_split_factor']
    assert rank_orbits==Counter({40:9,35:4,38:4,39:3,33:2})

    out={'pass':5317,'status':'THEOREM_HOFFMAN_FOURCELL_10_ORBITS_REFINE_TO_22_WD4_ORBITS',
      'H_order':576,'WD4_order':192,'H_over_WD4':'C3','four_subsets':715,
      'H_orbits':10,'WD4_orbits':22,'unsplit_H_orbits':4,'triality_triple_H_orbits':6,
      'WD4_orbit_size_histogram':{str(k):v for k,v in sorted(size_hist.items())},
      'WD4_orbits_by_span_rank':{str(k):v for k,v in sorted(rank_orbits.items())},
      'orbit_refinement':rows,
      'conclusion':'Six Hoffman H-orbits are exactly fusions of three equal W(D4) orbits; the outer C3 triality permutes each triple. Four H-orbits are already W(D4)-transitive.',
      'boundary':'Orbit refinement only. Span rank is not minimum distance, and the shortened [312,52,d]_2 distance remains in {28,32,36,40}.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
