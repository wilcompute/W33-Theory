#!/usr/bin/env python3
"""Exact scope correction for the heterotic CZ/parity holonomy pair.

The simultaneously diagonalized flagship pair has fundamental joint
multiplicities (3,2,1,1,1,1).  For a commuting semisimple family on C^n with
joint multiplicities m_i, its centralizer in SU(n) is S(prod_i U(m_i)) and has
Lie algebra dimension sum_i m_i^2 - 1.

Therefore the pair's full local SU(9) centralizer is
  S(U(3) x U(2) x U(1)^4),
with Lie algebra su(3)+su(2)+u(1)^5, dimension 16.  The observable SM algebra
su(3)+su(2)+u(1)_Y has dimension 12, so four local abelian directions remain
beyond hypercharge.  The exact positive mechanism is the SU(5)->3+2 split of
the nonabelian factor; the full centralizer is not literally the SM group.

This file preserves the useful mechanism while closing the scope overclaim.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_holonomy_joint_centralizer_scope.json'

def centralizer(blocks):
    return {
        'blocks':blocks,
        'dimension':sum(m*m for m in blocks)-1,
        'center_rank':len(blocks)-1,
        'semisimple_dimension':sum(m*m-1 for m in blocks if m>1),
    }

def main(write=True):
    wilson=centralizer([5,2,2])
    parity=centralizer([5,4])
    joint=centralizer([3,2,1,1,1,1])
    sm_dim=(3*3-1)+(2*2-1)+1
    checks={
      'wilson_centralizer_dimension_32':wilson['dimension']==32,
      'parity_centralizer_dimension_40':parity['dimension']==40,
      'joint_centralizer_dimension_16':joint['dimension']==16,
      'joint_center_rank_5':joint['center_rank']==5,
      'joint_semisimple_is_su3_plus_su2':joint['semisimple_dimension']==11,
      'standard_model_dimension_12':sm_dim==12,
      'four_extra_u1_beyond_hypercharge':joint['center_rank']-1==4,
      'joint_is_strictly_larger_than_sm':joint['dimension']-sm_dim==4,
    }
    assert all(checks.values())
    out={
      'schema':'w33.holonomy_joint_centralizer_scope.v1',
      'status':'PASS_SCOPE_CORRECTION',
      'headline':'The commuting (5,2,2) Wilson-line and (5,4) parity holonomies cut the SU(5) neutral block as 3+2, yielding the observable SU(3)xSU(2) factor, but their full SU(9) joint centralizer is S(U(3)xU(2)xU(1)^4), not the Standard Model group. Its Lie algebra is su(3)+su(2)+u(1)^5 of dimension 16; selecting hypercharge leaves four additional local U(1) directions for heterotic projection/Stueckelberg/Green-Schwarz physics to remove or lift.',
      'single_holonomy_centralizers':{'wilson_522':wilson,'theta3_54':parity},
      'joint':joint,
      'observable_sm':{'lie_algebra':'su(3)+su(2)+u(1)_Y','dimension':sm_dim},
      'extra_local_abelian_directions':4,
      'corrected_statement':'The exact mechanism is SU(5)->SU(3)xSU(2) inside the joint centralizer, with hypercharge a selected U(1); the phrase “the SM gauge group is the joint stabilizer” is too strong for the full local SU(9) algebra.',
      'checks':checks,
      'sources':['Holotrade 1d03cbb','Holotrade 94df376','Holotrade 59f2d6f','Holotrade 201cc175'],
      'boundary':'This is exact compact Lie-group centralizer arithmetic from the already-certified joint multiplicities. It does not by itself determine which four extra U(1)s become massive or projected in the full compactification.'
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out

if __name__=='__main__': main(True)
