#!/usr/bin/env python3
"""Pass7565-7572: one actual Eisenstein W33 leaf has a C3 phase extension of W(E6).

This is the current-object version of the older Pass1031/1037 controller theorem.
It rebuilds all 2240 E8/3E8 leaves, computes the stabilizer of one chosen leaf in
W(E8)/{+-I}, and computes its induced action on the leaf's 40 A2 points.

The abstract action of the quotient involution on the C3 kernel is imported only
from the already-certified full-E8 normalizer theorem (Pass1037), rather than
reclaimed here.
"""
from __future__ import annotations
import json
from collections import deque
from pathlib import Path
import sys
from sympy.combinatorics import Permutation, PermutationGroup

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E

OUT=ROOT/'data/PART_W33_PASS7565_7572_LEAF_PHASE_EXTENSION.json'

def comp(p,q): return tuple(p[q[i]] for i in range(len(q)))
def inv(p):
    z=[0]*len(p)
    for i,j in enumerate(p): z[j]=i
    return tuple(z)

def main():
    R,A2,ag,J,base,leaves,lgens,parity=E.build()
    assert len(leaves)==2240 and len(base)==40
    li={L:i for i,L in enumerate(leaves)}

    # Rebuild a Schreier transversal in the 1120-A2 action.  If t_x sends the
    # base leaf to x and g sends x to y, t_y^-1 g t_x stabilizes the base leaf.
    idp=tuple(range(1120)); trans=[None]*2240; trans[0]=idp; dq=deque([0])
    while dq:
        ix=dq.popleft(); tx=trans[ix]; X=leaves[ix]
        for g in ag:
            Y=frozenset(g[a] for a in X); iy=li[Y]
            if trans[iy] is None:
                trans[iy]=comp(g,tx); dq.append(iy)
    assert all(t is not None for t in trans)

    sch=[]; seen=set()
    for ix,X in enumerate(leaves):
        tx=trans[ix]
        for g in ag:
            Y=frozenset(g[a] for a in X); iy=li[Y]
            h=comp(inv(trans[iy]),comp(g,tx))
            if h!=idp and h not in seen: seen.add(h); sch.append(h)
    H=PermutationGroup([Permutation(list(h)) for h in sch])
    assert int(H.order())==155520

    bl=sorted(base); pos={a:i for i,a in enumerate(bl)}
    r40=[]
    for h in sch:
        assert all(h[a] in base for a in bl)
        r40.append(tuple(pos[h[a]] for a in bl))
    Q=PermutationGroup([Permutation(list(p)) for p in r40])
    qorder=int(Q.order()); derived=int(Q.derived_subgroup().order()); center=int(Q.center().order())
    assert (qorder,derived,center)==(51840,25920,1)
    kernel_order=int(H.order())//qorder
    assert kernel_order==3

    # Prior theorem dependencies: full E8 centralizer C = Z3 x Sp(4,3), and
    # N/Sp(4,3)=S3 with the external involution acting on C3 by inversion.
    p1031=json.loads((ROOT/'data/w33_pass1031_complex_determinant_phase_detector.json').read_text())
    p1037=json.loads((ROOT/'data/w33_pass1037_minimal_external_s3_controller_corollary.json').read_text())
    assert p1031['status']==p1037['status']=='PASS'
    assert p1031['abelian_invariants_of_C']==[3]
    assert p1037['orders']['Sp43_kernel']==51840
    assert p1037['orders']['centralizer']==155520
    assert p1037['orders']['normalizer']==311040
    assert p1037['checks']['controller_quotient_is_S3']
    assert p1037['checks']['external_involution_acts_by_inversion']

    out={
      'schema':'w33.pass7565_7572.leaf_phase_extension.v1','status':'PASS','passes':'7565-7572',
      'projective_E8_order':348364800,'Eisenstein_leaves':2240,
      'chosen_leaf_stabilizer_order':int(H.order()),'Schreier_generators':len(sch),
      'leaf_A2_points':40,'induced_leaf_group_order':qorder,
      'induced_leaf_group_identification':'W(E6) = U4(2):2 = PSp(4,3):2',
      'induced_leaf_group_derived_order':derived,'induced_leaf_group_center_order':center,
      'pointwise_kernel_order':kernel_order,'pointwise_kernel':'C3',
      'exact_sequence':'1 -> C3 -> Stab_projective_E8(L) -> W(E6) -> 1',
      'split_structure':'(C3 x U4(2)):2',
      'action':'the W(E6)/U4(2)=C2 quotient inverts C3; U4(2) centralizes C3',
      'dependency_weld':{
        'Pass1031':'full-E8 centralizer is Z3 x Sp(4,3), with Z3 detected by complex determinant',
        'Pass1037':'full normalizer quotient is S3 and its C2 acts on the phase C3 by inversion',
        'projectivization':'quotienting the common central {-I} inside Sp(4,3) sends Sp(4,3) to U4(2), leaving the phase C3 intact'
      },
      'theorem':'For an actual one of the 2240 E8/3E8 Eisenstein W33 leaves, the projective E8 stabilizer is a split C3 phase extension of the full W(E6) leaf controller. The C3 is pointwise invisible on all 40 A2 points, while the outer W(E6) involution inverts it.',
      'novelty_boundary':'Pass1031/1037 already owned the abstract full-E8 controller stack. This pass supplies the direct 2240-leaf/40-A2 projective action and welds that older theorem to the current global triality geometry.',
      'claim_boundary':'Exact finite group action only; no physical phase identification follows automatically.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','leaf_stabilizer':155520,'leaf_image':51840,'kernel':3,'structure':'(C3 x U4(2)):2'}))
if __name__=='__main__': main()
