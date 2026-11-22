#!/usr/bin/env python3
"""One tunable Witting phase + three fixed order-three mirrors generate U(4).

Exact Q(omega) projective ray permutations; modular Lie witness in six primes.
Uses minimal control certificate from toe_20261122_witting_minimal_lie_control.py.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import json
from sympy.combinatorics import Permutation, PermutationGroup
import toe_20261122_witting_minimal_lie_control as lie

Z=(F(0),F(0)); O=(F(1),F(0)); W=(F(0),F(1))
FIXED=(5,26,33)
TUNABLE=36
TARGET=(0,2,7,20)

def add(x,y):return (x[0]+y[0],x[1]+y[1])
def neg(x):return (-x[0],-x[1])
def sub(x,y):return add(x,neg(y))
def mul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]-x[1]*y[1])
def conj(x):return (x[0]-x[1],-x[1])
def scale(x,c):return (x[0]*c,x[1]*c)
WPOW=(O,W,mul(W,W))

def all_rays():
    rays=[]
    for j in range(4):
        v=[Z]*4;v[j]=O;rays.append(tuple(v))
    for mu in range(3):
        for nu in range(3):
            a,b=WPOW[mu],WPOW[nu]
            rays.extend([
                (Z,O,neg(a),b),
                (O,Z,neg(a),neg(b)),
                (O,neg(a),Z,b),
                (O,a,b,Z),
            ])
    assert len(rays)==40
    return rays

def reflect(v,x):
    dot=Z
    for a,b in zip(v,x):
        dot=add(dot,mul(conj(a),b))
    phase=mul(scale(sub(W,O),F(1,3)),dot)
    return tuple(add(y,mul(phase,z)) for y,z in zip(x,v))

def proportional(x,y):
    return all(mul(x[i],y[j])==mul(x[j],y[i])
               for i in range(4) for j in range(i+1,4))

def permutations():
    rays=all_rays();out={}
    for k in FIXED:
        perm=[]
        for x in rays:
            y=reflect(rays[k],x)
            hits=[i for i,r in enumerate(rays) if proportional(y,r)]
            assert len(hits)==1,(k,hits)
            perm.append(hits[0])
        assert set(perm)==set(range(40))
        assert all(perm[perm[perm[i]]]==i for i in range(40))
        out[k]=perm
    return out

def orbit_and_paths(perms):
    paths={TUNABLE:()}
    queue=[TUNABLE]
    for k in queue:
        for generator in FIXED:
            j=perms[generator][k]
            if j not in paths:
                paths[j]=paths[k]+(generator,)
                queue.append(j)
    return paths

def verify():
    perms=permutations()
    paths=orbit_and_paths(perms)
    group=PermutationGroup([Permutation(perms[k]) for k in FIXED])
    assert group.order()==648
    group_orbits=sorted([sorted(int(v) for v in o) for o in group.orbits()],
                        key=len,reverse=True)
    assert list(map(len,group_orbits))==[27,12,1]
    assert len(paths)==27
    assert all(k in paths for k in TARGET)
    _, mats, words, layers=lie.exact_certificate(7,selected=TARGET)
    assert len(mats)==16 and layers==[4,8,14,16]
    ranks=[]
    for p in lie.PRIMES:
        _, m, _, _=lie.exact_certificate(p,selected=TARGET,words=words)
        rank=lie.modular_rank(m,p)
        assert rank==16,(p,rank)
        ranks.append(dict(prime=p,Lie_rank=rank))
    return {
        'status':'PASS_EXACT_QOMEGA_ORBIT_AND_MODULAR_LIE_CERTIFICATE',
        'date':'2026-11-22',
        'fixed_order3_reflection_rays':list(FIXED),
        'one_continuous_phase_ray':TUNABLE,
        'fixed_mirror_actions_are_permutations_of_all_40_rays':True,
        'fixed_mirror_orders':[3,3,3],
        'fixed_subgroup_permutation_order':int(group.order()),
        'fixed_subgroup_orbit_sizes':[len(o) for o in group_orbits],
        'fixed_subgroup_G25_note':'Rank-three order-648 complex reflection subgroup matches Hessian Shephard-Todd G25; physical E6 interpretation is not established.',
        'orbit_size':len(paths),
        'orbit_indices':sorted(paths),
        'target_four_ray_subset':list(TARGET),
        'paths_to_targets':{str(k):list(paths[k]) for k in TARGET},
        'target_lie_rank_layers':layers,
        'target_modular_certificates':ranks,
        'orbit_lie_words':[list(w) for w in words],
        'minimality':'One tunable rank-one projector and at most two fixed rank-one mirrors leave a nonzero common orthogonal subspace in C4. Three fixed mirrors are necessary.',
        'theorem':'Fixed order-three Witting reflections on rays 5,26,33 with continuous exp(i theta P36) generate U(4) under the Lie rank condition.',
        'scope':'Single-photon four-mode coherent control, not a multiphoton entangling gate, experimental hardware, or a TOE.'
    }

def main():
    d=verify()
    path=Path(__file__).resolve().parents[1]/'data'/'toe_20261122_witting_one_phase_three_fixed.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('PASS',d['fixed_order3_reflection_rays'],d['orbit_size'],d['target_four_ray_subset'])

if __name__=='__main__':main()
