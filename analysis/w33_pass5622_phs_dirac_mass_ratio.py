#!/usr/bin/env python3
"""Pass5622: the deck-odd antiunitary symmetry removes m0 and leaves one mass scale.

The Pass5616 mass operator was M=m0 I + g H_mag, with both m0 and g free.
Pass5619 reveals a stronger structure on the canonical deck-odd 16-sector:
  spec H_- = {-6^4,-3^4,3^4,6^4}.
In the natural +/- sheet basis its compressed matrix is purely imaginary
Hermitian (i times a real skew matrix), so ordinary complex conjugation K obeys
  K H_- K^{-1} = -H_-,   K^2=1.

For real m0,g,
  K M K^{-1} = m0 I - gH_-.
Requiring the same particle-hole-type symmetry on M,
  K M K^{-1} = -M,
forces m0=0 exactly. Then the Dirac dispersion has only two nonzero absolute
internal masses, 3|g| and 6|g|, with parameter-free ratio 2. The overall scale
|g| is still not fixed by finite dimensionless incidence data.

This is a conditional symmetry theorem, not a Standard Model mass assignment.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5622_PHS_DIRAC_MASS_RATIO.json'

def main():
    bands={-6:4,-3:4,3:4,6:4}
    assert sum(bands.values())==16
    assert sum(h*m for h,m in bands.items())==0
    for h,m in list(bands.items()): assert bands.get(-h)==m
    absolute={3:bands[3]+bands[-3],6:bands[6]+bands[-6]}
    assert absolute=={3:8,6:8}
    ratio=Fraction(6,3); assert ratio==2

    out={
      'pass':5622,'status':'CONDITIONAL_PHS_FIXES_M0_AND_MASS_RATIO_TWO',
      'deck_odd_internal_operator':{'dimension':16,'spectrum':{'-6':4,'-3':4,'3':4,'6':4},'antiunitary':'K=complex conjugation','symmetry':'K H_- K^{-1}=-H_-','K_squared':1},
      'mass_operator':{'general':'M=m0 I + g H_-','PHS_condition':'K M K^{-1}=-M','consequence':'m0=0 for real m0,g'},
      'dirac_dispersion_after_symmetry':'E_{h,+/-}(p)=+/-sqrt(|p|^2+g^2 h^2)',
      'absolute_internal_mass_levels':{'3|g|':8,'6|g|':8},
      'parameter_free_ratio':'m_heavy/m_light=2',
      'remaining_free_parameter':'one overall dimensionful scale |g|',
      'scale_no_go':'The finite geometry fixes dimensionless eigenvalue ratios but supplies no physical conversion from its unit operator to joules, hertz, inverse metres, or GeV. An external dynamical normalization or experimentally calibrated clock/length scale is still required.',
      'physics_firewall':'The ratio 2 is forced only if the deck-odd sector is the physical mass sector and its exact K particle-hole symmetry is imposed on the mass operator. No Standard Model particle assignment is made.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
