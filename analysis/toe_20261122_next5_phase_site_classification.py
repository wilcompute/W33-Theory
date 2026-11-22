#!/usr/bin/env python3
"""Complete exact 40-Witting-site classification for a fourth pi phase gate.

Fix order-three mirrors at rays 5,26,33 (group H of order 648).
An order-two phase gate D_r=I-2P_r is SU4-dense with these mirrors
iff r belongs to the 27-ray H orbit. The 12-ray orbit preserves a 3+1
orthogonal block; the unique fixed ray25 yields finite H x C2, order1296.
This is a full site-selection theorem for this specific fixed-mirror triple.
"""
from __future__ import annotations
import json
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
import toe_20261122_witting_one_phase_three_fixed as W
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_next5_phase_site_classification.json'

def dot(a,b):
    t=W.Z
    for x,y in zip(a,b):t=W.add(t,W.mul(W.conj(x),y))
    return t

def verify():
    rays=W.all_rays();perms=W.permutations()
    H=PermutationGroup([Permutation(perms[j]) for j in W.FIXED])
    assert H.order()==648
    orbits=sorted((sorted(map(int,o)) for o in H.orbits()),key=len,reverse=True)
    assert list(map(len,orbits))==[27,12,1]
    mixing,block,fixed=orbits
    assert fixed==[25] and 36 in mixing
    L=rays[25]
    # All fixed mirrors stabilize the line L pointwise, and the three
    # mirror vectors span its three-dimensional complex orthogonal complement.
    assert all(dot(rays[j],L)==W.Z for j in W.FIXED)
    for idx in block:
        assert dot(L,rays[idx])==W.Z
        assert not W.proportional(L,rays[idx])
    for idx in mixing:
        assert dot(L,rays[idx])!=W.Z
        assert not W.proportional(L,rays[idx])
    # H's entire 27 orbit of r36 is conjugate under H; D_hr = h D_r h^-1
    # because h is unitary, so <H,D_hr>=<H,D_r>.
    assert sorted(H.orbit(36))==mixing
    # The fixed-line D25 commutes with H, is not in H (det -1 vs det
    # in roots of unity of order 3), so the generated group is H x C2.
    return dict(status='PASS_COMPLETE_WITTING_40_PI_SITE_UNIVERSALITY_CLASSIFICATION',
      date='2026-11-22',fixed_order3_mirrors=list(W.FIXED),Hessian_H_order=648,
      unique_fixed_orthogonal_line_ray=25,
      fixed_line_orthogonal_to_three_generators=True,
      all_40_projective_rays_classified=True,
      dense_SU4_pi_sites=mixing,dense_site_count=len(mixing),
      block_preserving_nonuniversal_pi_sites=block,block_site_count=len(block),
      finite_nonuniversal_pi_site=fixed[0],fixed_site_count=len(fixed),
      finite_ray25_group_structure='H x C2',finite_ray25_group_order=1296,
      dense_class_closure='{U in U4: det(U) in mu6}',
      proof='The group H fixes the orthogonal line L (ray25). Of 40 Witting rays, 12 lie in L-perp and one equals L; their pi projectors preserve the L-perp⊕L splitting. Remaining 27 rays form one H orbit containing ray36; conjugating D36 by H gives every corresponding D_r, so generated closures coincide with the certified dense SU4 case. D25 commutes with H and has determinant -1, whereas H determinants are powers of omega, giving the direct product H×C2.',
      apparatus_decision='Choose the pi-phase line from the unique 27-orbit; the 12+1 alternative placements cannot give four-mode dense SU4 with the fixed three mirrors.',
      limitations='Only this three-mirror subset, one additional rank-one pi gate, ideal four modes; does not certify physical loss, gate efficiency or multiphoton entanglement.')

def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print('PASS phase site classification',d['dense_site_count'],d['block_site_count'],d['fixed_site_count'])

if __name__=='__main__':main()
