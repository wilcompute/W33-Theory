#!/usr/bin/env python3
"""Exact SO10xU1 selection-rule barrier for E6 singlet-only cubic Higgs masses.

All fields are toy vectorlike three-family 27+bar27 Higgs, not SM chiral
matter. An adjoint-Cartan plus bilinear term can algebraically shift the
spinor Hessian but its full F/D-flat vacuum remains unverified.
"""
from __future__ import annotations
from pathlib import Path
import json
import sympy as sp
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_round5_higgs_spinor_selection.json'

def verify():
    # 27 = 16_1 + 10_{-2} + 1_4 (standard SO10xU1 embedding).
    chars={'16':(16,1),'10':(10,-2),'1':(1,4)}
    allowed=[]
    from itertools import combinations_with_replacement
    for triple in combinations_with_replacement(chars,3):
        if sum(chars[c][1] for c in triple)==0:allowed.append(triple)
    assert allowed==[('16','16','10'),('10','10','1')],allowed
    assert ('16','16','1') not in allowed
    families=3
    spinor_fields=2*families*16
    eaten_spinor_goldstone=32
    residual=spinor_fields-eaten_spinor_goldstone
    assert (spinor_fields,eaten_spinor_goldstone,residual)==(96,32,64)
    # Independent 27bar x 78 x 27 gauge invariant: Cartan U1 adjoint
    # VEV a generates masses m+lambda*a*q per SO10 block.
    a,lam=sp.symbols('a lam',nonzero=True)
    mass_singlet=-4*a*lam+lam*a*chars['1'][1]
    mass_spinor=-4*a*lam+lam*a*chars['16'][1]
    mass_ten=-4*a*lam+lam*a*chars['10'][1]
    assert mass_singlet==0 and sp.expand(mass_spinor)==-3*a*lam and sp.expand(mass_ten)==-6*a*lam
    return dict(status='PASS_E6_H27_SINGLET_CUBIC_64_SPINOR_SELECTION_GATE',
     SO10_U1_decomposition='27 = 16_1 + 10_-2 + 1_4',
     U1_neutral_fundamental_cubic_sectors=['16*16*10','10*10*1'],
     U1_forbidden_cubic_sector='16*16*1',
     elementary_spinor_component_count=spinor_fields,
     eaten_spinor_goldstone_modes=eaten_spinor_goldstone,
     residual_quadratic_spinor_modes=residual,
     singlet_VEV_only_cubic_lifts_spinors=False,
     adjoint_Cartan_escape={'m_choice':'m=-4 lambda a','singlet_coefficient':str(mass_singlet),'spinor_coefficient':str(sp.expand(mass_spinor)),'ten_coefficient':str(sp.expand(mass_ten))},
     warning='Adjoint escape computes an allowed Hessian operator, not a full F- and D-flat solution; 78 adjoint fluctuations restore Goldstone constraints. It is not an isolated vacuum or a realistic chiral Standard Model, and a family-uniform vectorlike mass does not predict three chiral families.')
if __name__=='__main__':
 d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(d['status'],d['residual_quadratic_spinor_modes'])
