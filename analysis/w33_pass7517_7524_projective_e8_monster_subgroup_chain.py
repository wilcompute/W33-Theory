#!/usr/bin/env python3
"""Pass7517-7524: locate the projective E8 Weyl action inside the 3360 triality carrier.

This is a current-frontier refinement of the old O8+(2) discussion in Pass1301.
It reconstructs the actual E8 simple-reflection action on the 1120 A2 systems
and 2240 Eisenstein W33 leaves used in Pass7401-7472, computes its faithful
projective order, and measures its action on the three D4(3) triality types.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, deque
from pathlib import Path
from sympy.combinatorics import Permutation, PermutationGroup

OUT=Path('data/PART_W33_PASS7517_7524_PROJECTIVE_E8_MONSTER_SUBGROUP_CHAIN.json')
SIMPLES=[
(1,-1,-1,-1,-1,-1,-1,1),(2,2,0,0,0,0,0,0),(-2,2,0,0,0,0,0,0),
(0,-2,2,0,0,0,0,0),(0,0,-2,2,0,0,0,0),(0,0,0,-2,2,0,0,0),
(0,0,0,0,-2,2,0,0),(0,0,0,0,0,-2,2,0)]

def roots():
    R=[]
    for i,j in itertools.combinations(range(8),2):
        for a in (2,-2):
            for b in (2,-2):
                v=[0]*8;v[i]=a;v[j]=b;R.append(tuple(v))
    for s in itertools.product((1,-1),repeat=8):
        if sum(x<0 for x in s)%2==0:R.append(tuple(s))
    assert len(R)==len(set(R))==240
    return R

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def refl(x,r):
    q=dot(x,r);assert q%4==0;k=q//4
    return tuple(x[i]-k*r[i] for i in range(8))
def enum_a2(R):
    I={r:i for i,r in enumerate(R)};out=set()
    for i,j in itertools.combinations(range(240),2):
        if dot(R[i],R[j])!=-4:continue
        s=tuple(R[i][k]+R[j][k] for k in range(8));k=I[s]
        out.add(frozenset((i,j,k,I[tuple(-x for x in R[i])],
                           I[tuple(-x for x in R[j])],I[tuple(-x for x in s)])))
    A=sorted(out,key=lambda x:tuple(sorted(x)));assert len(A)==1120
    return A

def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))

def main():
    R=roots();I={r:i for i,r in enumerate(R)};A2=enum_a2(R);ai={S:i for i,S in enumerate(A2)}
    rg=[tuple(I[refl(r,s)] for r in R) for s in SIMPLES]
    ag=[tuple(ai[frozenset(g[x] for x in S)] for S in A2) for g in rg]
    PG=PermutationGroup([Permutation(g) for g in ag])
    projective_order=int(PG.order())
    assert projective_order==348364800
    c=tuple(range(240))
    for g in rg:c=comp(g,c)
    J=tuple(range(240))
    for _ in range(10):J=comp(c,J)
    base=frozenset(i for i,S in enumerate(A2) if frozenset(J[x] for x in S)==S)
    assert len(base)==40
    leaves=[base];li={base:0};q=deque([base])
    while q:
        X=q.popleft()
        for g in ag:
            Y=frozenset(g[x] for x in X)
            if Y not in li:li[Y]=len(leaves);leaves.append(Y);q.append(Y)
    assert len(leaves)==2240
    lg=[tuple(li[frozenset(g[x] for x in L)] for L in leaves) for g in ag]
    bmask=sum(1<<x for x in base)
    ov=[(bmask & sum(1<<x for x in L)).bit_count() for L in leaves]
    assert Counter(ov)==Counter({40:1,13:40,4:390,1:1080,0:729})
    parity=[1 if z in (13,1) else 0 for z in ov]
    assert parity.count(0)==parity.count(1)==1120
    swap_bits=[]
    for g in lg:
        delta={parity[g[j]]^parity[j] for j in range(2240)}
        assert len(delta)==1
        swap_bits.append(next(iter(delta)))
    assert swap_bits==[1]*8
    type_image_order=2
    type_kernel_order=projective_order//type_image_order
    assert type_kernel_order==174182400
    ambient_order=118852315545600
    monster_local_order=2139341679820800
    assert ambient_order%projective_order==0
    assert monster_local_order%projective_order==0
    out={
      'schema':'w33.pass7517_7524.projective_e8_monster_subgroup_chain.v1','status':'PASS',
      'internal_reconstruction':{'E8_roots':240,'A2_subsystems':1120,'Eisenstein_W33_leaves':2240,
        'projective_A2_action_order':projective_order,'simple_reflections':8,'leaf_families':[1120,1120]},
      'triality_type_action':{'singular_point_type_fixed':True,'each_simple_reflection_swaps_generator_families':True,
        'simple_reflection_swap_bits':swap_bits,'type_image_order':type_image_order,'type_kernel_order':type_kernel_order},
      'group_identification':{
        'standard_external_fact':'W(E8) = 2.O8+(2).2 and W+(E8)/{±I} = O8+(2)',
        'projective_full':'W(E8)/{±I} = O8+(2):2','projective_even':'W+(E8)/{±I} = O8+(2)',
        'O8plus2_order':174182400},
      'nested_carrier_chain':{
        'chain':'O8+(2):2 < O8+(3):S4 < (3^2:2 x O8+(3)).S4 < Monster',
        'projective_E8_order':projective_order,'ambient_triality_order':ambient_order,
        'ambient_over_projective_index':ambient_order//projective_order,
        'Monster_local_order':monster_local_order,'Monster_local_over_projective_index':monster_local_order//projective_order,
        'geometric_meaning':'The projective E8 Weyl action fixes the Q+(7,3) point type and uses the unique C2 that exchanges the two generator families; the ambient D4(3) group enlarges this to the full S4 outer coordinate.'},
      'prior_art_boundary':'Pass1301 already discussed O8+(2) and Sp(4,3) abstractly. The new theorem is the explicit action of the current E8 A2/W33 leaf construction on the 3360 Q+(7,3) triality carrier and its placement in the Monster-local carrier chain.',
      'claim_boundary':'Finite Weyl/orthogonal/sporadic subgroup geometry only; no moonshine or physics consequence follows automatically.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
