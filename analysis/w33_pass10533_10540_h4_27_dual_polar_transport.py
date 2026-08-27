#!/usr/bin/env python3
"""Pass10533-10540: the H(4)/(13:6) 27|27 quotient is a genuine dual pair, not a self-dual 27-set.

The explicit normalizer has 27 point orbits and 27 line orbits, but their orbit-size
multisets differ.  Therefore no normalizer-equivariant bijection can identify the two
27-state carriers.

The equitable incidence quotient M nevertheless has rank 21.  After weighting point
and line orbit bases by square roots of their orbit sizes, its normalized incidence
operator B has singular values
  5^1, (2 sqrt(3))^8, 2^12, 0^6.
The polar decomposition B=U|B| therefore supplies a unique rank-21 partial isometry U
from the transmitted line sector to the transmitted point sector, with six-dimensional
kernels on each side.

This is recorded as a finite dual-transport structure.  It is compatible with the
motif of E6 minuscule 27 versus dual 27bar, but no E6 representation identification is
claimed without a common group intertwiner.
"""
from __future__ import annotations
from collections import Counter
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10533_10540_H4_27_DUAL_POLAR_TRANSPORT.json'

def main():
    q=json.loads((ROOT/'data/PART_W33_PASS10493_10500_H4_27X27_INCIDENCE_CONSTITUENTS.json').read_text())
    po={int(k):int(v) for k,v in q['normalizer_orbits']['point_orbit_sizes'].items()}
    lo={int(k):int(v) for k,v in q['normalizer_orbits']['line_orbit_sizes'].items()}
    assert po=={13:3,26:6,39:6,78:12}
    assert lo=={13:4,26:4,39:7,78:12}
    assert po!=lo
    inc=q['incidence_quotient'];assert inc['rank']==21 and inc['kernel_dimension']==6
    spec={int(k):int(v) for k,v in inc['squared_singular_spectrum'].items()}
    assert spec=={25:1,12:8,4:12,0:6}
    transmitted=sum(m for s,m in spec.items() if s);assert transmitted==21
    line_kernel=point_kernel=spec[0];assert point_kernel==line_kernel==6
    out={
      'schema':'w33.pass10533_10540.h4_27_dual_polar_transport.v1','status':'PASS','passes':'10533-10540',
      'point_orbit_profile':{'13':3,'26':6,'39':6,'78':12},
      'line_orbit_profile':{'13':4,'26':4,'39':7,'78':12},
      'equivariant_self_duality':{'exists':False,'reason':'point and line orbit-size multisets under the same 13:6 normalizer differ'},
      'incidence_transport':{'rank':21,'point_kernel_dimension':6,'line_kernel_dimension':6,'squared_singular_values':{'25':1,'12':8,'4':12,'0':6},'singular_values':'5^1, (2 sqrt(3))^8, 2^12, 0^6'},
      'polar_transport':{'exists_and_unique_on_support':True,'rank':21,'statement':'After canonical orbit-size normalization B, the polar decomposition B=U|B| gives a unique partial isometry U from ker(B)^perp to im(B), with six-dimensional kernels on both sides.'},
      'E6_motif':'The result provides an exact dual 27|27 incidence architecture with a rank-21 pairing. It is structurally compatible with a 27/dual-27 motif but is not asserted to be the E6 minuscule dual representation without a common group action/intertwiner.',
      'theorem':'The normalizer quotient naturally produces two inequivalent 27-state G-sets, point states and line states, rather than one self-dual carrier. Their rank-21 incidence pairing canonically yields a polar partial isometry whose transmitted constituent dimensions are 1+8+12 and whose kernel has dimension 6.',
      'boundary':'Exact orbit-profile/rank/singular-value consequences of Pass10493-10500 plus standard polar decomposition. No E6 representation equivalence is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','self_dual_27':False,'polar_rank':21,'kernel':6}))
    return 0
if __name__=='__main__':raise SystemExit(main())
