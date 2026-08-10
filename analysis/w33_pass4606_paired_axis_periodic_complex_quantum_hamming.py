#!/usr/bin/env python3
"""Pass 4606 -- the paired cubic axes form a 2-periodic complex and quantum Hamming code.

For the actual 27x36 cubic incidence matrix R of Pass4575, RR^T=R^TR=0 over
F2. Hence R and R^T alternate as a genuine 2-periodic differential. Since
rank R=6,
  H_36 = ker R / im R^T has dimension 30-6=24,
  H_27 = ker R^T / im R has dimension 21-6=15.
These dimensions equal the two nontrivial W33 adjacency multiplicities 24 and
15, but this pass does not promote that dimension match to a module isomorphism.

Each self-orthogonal axis also gives a CSS code by taking the same code for X
and Z checks: [36,6,16] -> [[36,24,3]], [27,6,12] -> [[27,15,3]], because the
dual kernels have minimum distance 3 while the check codes have minima 16/12.

Pass4592 fuses the same six message bits across both axes into the simplex
S6=[63,6,32]. S6 is self-orthogonal and S6^perp is the [63,57,3] Hamming code,
so the fused CSS code is [[63,51,3]], the m=6 binary quantum Hamming code.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass4575_cubic_incidence_binary_code as p4575
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4606_PAIRED_AXIS_PERIODIC_COMPLEX_QUANTUM_HAMMING.json'

def rank2(A):return p4575.rank2(np.asarray(A,dtype=np.uint8))
def main():
    R=p4575.build_actual_R();assert R.shape==(27,36) and rank2(R)==6
    assert not np.any((R@R.T)%2) and not np.any((R.T@R)%2)
    h36=(36-rank2(R))-rank2(R.T);h27=(27-rank2(R.T))-rank2(R)
    assert (h36,h27)==(24,15)
    # Reuse exact Pass4575 dual-distance and Pass4592 fused-code certificates.
    c5=json.loads((ROOT/'data/PART_W33_PASS4575_CUBIC_INCIDENCE_BINARY_CODE.json').read_text())
    c2=json.loads((ROOT/'data/PART_W33_PASS4592_PAIRED_AXES_SIMPLEX_HEXACODE_GOLAY.json').read_text())
    assert c5['row_code']['dual_kernel']['parameters']=='[36,30,3]'
    assert c5['column_code']['dual_kernel']['parameters']=='[27,21,3]'
    assert c2['paired_axes']['same_message_concatenation']=='[63,6,32] binary simplex'
    out={'pass':4606,
      'periodic_complex':{'d_even':'R: F2^36 -> F2^27','d_odd':'R^T: F2^27 -> F2^36','d_squared_zero':['R R^T=0','R^T R=0'],'rank':6,'H36_dimension':24,'H27_dimension':15,'Euler_difference':9},
      'axis_CSS':{'C36':'[[36,24,3]]','C27':'[[27,15,3]]'},
      'fused_CSS':{'classical_check_code':'[63,6,32] simplex','normalizer_code':'[63,57,3] Hamming','quantum_parameters':'[[63,51,3]]','family':'binary quantum Hamming m=6'},
      'W33_dimension_echo':'24 and 15 equal the nontrivial W33 adjacency multiplicities; no module isomorphism is claimed here without an explicit intertwiner',
      'boundary':'Exact binary chain-complex/CSS coding statement. The homology-dimension match to W33 spectral multiplicities is recorded as a target for an equivariant comparison, not an identification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
