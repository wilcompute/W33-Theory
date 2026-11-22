#!/usr/bin/env python3
"""Exact polar-pencil/H27 orbit decomposition on the canonical Witting 40-ray set.

At a fixed Witting ray, the normal H27 has orbits 1+3+3+3+3+27.
The four three-element fibers are the four isotropic/projective lines
through the fixed point in the W(3,3) graph; the 27 external points
form a regular Heisenberg torsor.
"""
from __future__ import annotations
import json
from itertools import combinations
from pathlib import Path
from collections import Counter
from sympy.combinatorics import Permutation,PermutationGroup
import toe_20261122_witting_one_phase_three_fixed as model

def inner(a,b):
    x=model.Z
    for u,v in zip(a,b):
        x=model.add(x,model.mul(model.conj(u),v))
    return x

def verify():
    rays=model.all_rays()
    perms=model.permutations()
    R={k:Permutation(perms[k]) for k in model.FIXED}
    G=PermutationGroup(list(R.values()))
    N=G.normal_closure([R[5]*R[33]**-1])
    assert (G.order(),N.order())==(648,27)
    pencil=sorted([sorted(int(i) for i in orbit) for orbit in N.orbits()],
                  key=lambda t:(len(t),t))
    counts=Counter(map(len,pencil))
    assert counts==Counter({1:1,3:4,27:1})
    fixed=next(orbit[0] for orbit in pencil if len(orbit)==1)
    triples=[orbit for orbit in pencil if len(orbit)==3]
    outer=next(orbit for orbit in pencil if len(orbit)==27)
    assert fixed==25
    assert sorted(outer)==sorted(model.orbit_and_paths(perms))
    assert all(inner(rays[fixed],rays[i])==model.Z
               for orbit in triples for i in orbit)
    assert all(inner(rays[fixed],rays[i])!=model.Z for i in outer)
    assert all(inner(rays[i],rays[j])==model.Z
               for orbit in triples for i,j in combinations(orbit,2))
    # Independent characteristic-zero SRG check without NetworkX or float.
    neighbors=[{j for j in range(40) if i!=j and inner(rays[i],rays[j])==model.Z}
               for i in range(40)]
    assert all(len(s)==12 for s in neighbors)
    profile=Counter()
    for i,j in combinations(range(40),2):
        common=len(neighbors[i]&neighbors[j])
        expected=2 if j in neighbors[i] else 4
        assert common==expected,(i,j,common)
        profile[(int(j in neighbors[i]),common)]+=1
    assert profile=={(1,2):240,(0,4):540}
    assert N.stabilizer(model.TUNABLE).order()==1
    return {
      'status':'PASS_EXACT_WITTING_H27_POLAR_PENCIL',
      'date':'2026-11-22',
      'fixed_witting_ray_zero_based':fixed,
      'heisenberg_order':int(N.order()),
      'fixed_mirror_group_order':int(G.order()),
      'H27_orbit_sizes':[len(o) for o in pencil],
      'four_three_ray_pencil_lines':triples,
      'regular_27_ray_orbit':outer,
      'line_through_fixed_ray_for_each_triplet':True,
      'four_pencil_lines_reconstruct_12_neighbors':True,
      'exterior_27_rays_all_nonorthogonal_to_fixed':True,
      'srg_parameters':[40,12,2,4],
      'pair_count_by_adjacency_and_common_neighbors':{
          'adjacent_common2':profile[(1,2)],
          'nonadjacent_common4':profile[(0,4)]},
      'regular_H27_orbit_point_stabilizer':int(N.stabilizer(model.TUNABLE).order()),
      'theorem':'Witting 40 rays split exactly into 1 fixed + 4 isotropic 3-fibers + 27 regular H27 outer points. The four lines through the fixed point explain its 12 orthogonal neighbors. This identifies the concrete polar neighborhood, not a spacetime or E6 matter coupling.',
      'scope':'Finite-projective, exact Q(omega) incidence and group action; no continuum or photonic device experiment.'
    }

def main():
    d=verify()
    output=Path(__file__).resolve().parents[1]/'data'/'toe_20261122_witting_h27_polar_pencil.json'
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('PASS H27 polar pencil: 1+3+3+3+3+27 with SRG(40,12,2,4)')

if __name__=='__main__':main()
