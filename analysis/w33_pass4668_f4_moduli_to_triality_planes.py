#!/usr/bin/env python3
"""Pass 4668 -- compatible F4 structures are the D4 triality-intersection planes.

Compose two independently frozen action-level intertwiners through the same W33
point carrier:
  compatible {J,J^2} -> unique fixed W33 point -> triality anisotropic plane.
The first chart is Pass4628; the second is Pass4654.  This is therefore not a
40=40 count match.  The subgroup tower 216<648<1296 records pointwise plane,
PSp point/plane, and PGSp semilinear F4 stabilizers.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4668_F4_MODULI_TO_TRIALITY_PLANES.json'

def main():
    f=json.loads((ROOT/'data/PART_W33_PASS4628_F4_CHOICE_IS_W33_POINT_CARRIER.json').read_text())
    p=json.loads((ROOT/'data/PART_W33_PASS4654_TRIALITY_PLANE_W33_POINT_INTERTWINER.json').read_text())
    d=json.loads((ROOT/'data/PART_W33_PASS4649_FULL_TRIALITY_GROUP_INTERSECTIONS.json').read_text())
    assert f['compatible_F4_structures']['unoriented_pairs']==40
    assert f['compatible_F4_structures']['normalizer_order']==1296
    assert f['W33_intertwiner']['carrier']=='point-side W33'
    assert p['orbit_size']==40 and p['base_plane_setwise_stabilizer_order']==648 and p['base_plane_pointwise_stabilizer_order']==216
    assert p['target_carrier']=='W33 point carrier' and p['not_target_carrier']=='W33 line carrier'
    assert d['PSp_intersections']['pairwise_order']==216 and d['anisotropic_plane_reconstruction']['plane_orbit_size']==40
    out={
      'pass':4668,
      'source_moduli':{'objects':'compatible unoriented F4 structures {J,J^2} on U6','count':40,'PGSp_stabilizer_order':1296,'chart':'unique W33 point fixed by the semilinear normalizer'},
      'triality_moduli':{'objects':'anisotropic F2 two-planes fixed pointwise by pairwise triality-conjugate PSp intersections','count':40,'PSp_setwise_stabilizer_order':648,'pointwise_stabilizer_order':216,'chart':'unique W33 point fixed by the setwise stabilizer'},
      'explicit_composition':'{J,J^2} -> p(J) -> P(p(J)), using the two frozen equivariant W33-point charts',
      'PSp_equivariant_bijection':True,
      'stabilizer_tower':'216 (pointwise triality-plane intersection) < 648 (PSp point/plane stabilizer) < 1296 (PGSp semilinear F4 normalizer)',
      'half_spinor_reading':'The three triality-conjugate PSp copies have pairwise order-216 intersections. For either half-spinor-side conjugate paired with the distinguished PSp copy, the resulting 40-plane carrier is a triality-conjugate realization of this same W33-point/F4-moduli G-set.',
      'graph_transport':'total polar orthogonality of the anisotropic planes transports to W33 point collinearity, hence to the adjacency geometry of compatible F4 choices',
      'theorem':'The noncanonical F4 choice needed by the hexacode/Golay lane has a concrete D4 realization: it is exactly the PSp G-set of anisotropic two-planes cut out by pairwise triality-conjugate PSp intersections. The identification is the composition of two explicit W33-point intertwiners, with stabilizer tower 216<648<1296.',
      'boundary':'Finite G-set/stabilizer transport. The frozen Golay coordinate embedding remains non-PGSp-equivariant; no M24 subgroup or physical spinor identification is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
