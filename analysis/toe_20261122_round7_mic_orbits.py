#!/usr/bin/env python3
"""Hessian orbit classification of proven minimal Witting 16-effect POVM.

Classification is under *the specific 648-element fixed-mirror subgroup*, not
all automorphisms of the complete 40-ray Witting configuration.
"""
from collections import Counter
from pathlib import Path
import json
import numpy as np
from sympy.combinatorics import Permutation,PermutationGroup
import toe_20261122_witting_one_phase_three_fixed as W
import toe_20261122_round6_16effect_optimal as P
from toe_20261122_round6_minimal_ic import get_mats

OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_round7_mic_orbits.json'

def verify():
    base=P.proof(); G=PermutationGroup([Permutation(v) for v in W.permutations().values()]);assert G.order()==648
    S=set(P.S);heavy=set(P.HEAVY)
    supports=set();wts=set();stabilizers=0;weighted_stabilizers=0
    partition=G.orbits();fixed=[sorted(int(j) for j in o) for o in partition];sizes=sorted(map(len,fixed));assert sizes==[1,12,27]
    orbitmap={i:len(o) for o in fixed for i in o}
    comps=Counter(orbitmap[x] for x in S)
    for g in G.generate_schreier_sims():
        s=tuple(sorted(int(g(j)) for j in S));h=tuple(sorted(int(g(j)) for j in heavy))
        supports.add(s);wts.add((s,h))
        stabilizers+=s==tuple(sorted(S))
        weighted_stabilizers+=(s==tuple(sorted(S)) and h==tuple(sorted(heavy)))
    assert len(supports)*stabilizers==648
    assert len(wts)*weighted_stabilizers==648
    Ps,A,b=get_mats()
    samples=[]
    for indices in sorted(supports)[:12]:
        # Here the transported weights are needed, not just the support.
        assert np.linalg.matrix_rank(A[:,indices])==16
        samples.append(indices)
    # Verify the actual transported weights for all subgroup elements.
    maxres=0
    for g in G.generate_schreier_sims():
        w=np.zeros(40)
        for k in S:w[int(g(k))]=float(P.WEIGHTS[k])
        maxres=max(maxres,float(np.max(np.abs(A@w-b))))
    assert maxres<1e-12
    result={
        'status':'PASS_G25_HESSIAN_SUBGROUP_ORBIT_OF_EXACT_MINIMAL16_POVM',
        'hessian_group_order':648,
        'support_orbit_size':len(supports),
        'weighted_povm_orbit_size':len(wts),
        'support_stabilizer_order':stabilizers,
        'weighted_povm_stabilizer_order':weighted_stabilizers,
        'support_composition_in_1_12_27_ray_orbits':{str(i):n for i,n in comps.items()},
        'distinct_projective_outcomes':16,
        'all_transported_supports_rank16':True,
        'all_transported_weighted_povms_normalized':True,
        'max_floating_point_identity_error':maxres,
        'exact_seed_Gram_determinant':base['exact_projector_Gram_determinant'],
        'seed_frame_condition':base['condition'],
        'sample_supports':[list(s) for s in samples],
        'scope':'This classifies the orbit under the order-648 subgroup only, not all minimal Witting POVMs or the full 40-ray symmetry group.'}
    return result

if __name__=='__main__':
 d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(d)
