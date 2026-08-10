#!/usr/bin/env python3
"""Pass 4631 bonkers -- the 45x40 incidence is E6 versus F4-choice moduli.

Pass4628 proves that the 40 compatible F4 structures on the natural minus U6
form exactly the point-side W33 PGSp G-set.  Pass4625 proves that the columns of
T are that point carrier, its rows are the center-quad/E6 45, and its 40 binary
kernel minimum words are the line-side W33 carrier.  Composing these exact
intertwiners gives a new reading of T entirely in terms of compatible F4 choices.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
from exploration.w33_center_quad_gq42_e6_bridge import quotient_points,w33_lines

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4631_F4_MODULI_E6_INCIDENCE.json'

def main()->int:
    f4=json.loads((ROOT/'data/PART_W33_PASS4628_F4_CHOICE_IS_W33_POINT_CARRIER.json').read_text())
    tri=json.loads((ROOT/'data/PART_W33_PASS4625_INTRINSIC_45X40_THREE_CARRIER.json').read_text())
    assert f4['compatible_F4_structures']['unoriented_pairs']==40 and f4['W33_intertwiner']['carrier']=='point-side W33'
    assert tri['matrix']['shape']==[45,40] and tri['line_carrier']['minimum_words']==40
    points=quotient_points();T=np.zeros((45,40),dtype=np.uint8)
    for i,p in enumerate(points):T[i,list(p.support_vertices)]=1
    assert set(map(int,T.sum(1)))=={8} and set(map(int,T.sum(0)))=={9}
    pair_counts={}
    for i,j in itertools.combinations(range(40),2):pair_counts[(i,j)]=int(T[:,i]@T[:,j])
    assert sorted(set(pair_counts.values()))==[1,3]
    assert sum(v==3 for v in pair_counts.values())==240 and sum(v==1 for v in pair_counts.values())==540
    # The 40 W33 lines are exactly the complete minimum weight-four shell of ker T.
    tetrads=[]
    for L in w33_lines():
        x=np.zeros(40,dtype=np.uint8);x[list(L)]=1
        assert not np.any((T@x)%2);tetrads.append(tuple(sorted(L)))
    assert len(set(tetrads))==40
    old=json.loads((ROOT/'data/w33_pass228_sentinel_weight_enumerator.json').read_text())
    assert old['context_40_25_4_via_macwilliams']['low_weight_spectrum']['4']==40
    out={'pass':4631,
      'moduli_points':{'objects':'compatible unoriented F4 structures {J,J^2} on U6','count':40,'G_set':'point-side W33 by Pass4628'},
      'E6_rows':{'objects':'center-quad/E6-tritangent 45 carrier','count':45,'F4_structures_per_row':8,'rows_per_F4_structure':9},
      'pair_cooccurrence':{'three_common_E6_rows':240,'one_common_E6_row':540,'rule':'co-occurrence 3 reconstructs point-side W33 adjacency'},
      'minimal_even_tetrads':{'definition':'four F4 structures whose incidence vector lies in ker_F2(T)','minimum_weight':4,'count':40,'identification':'exactly the W33 lines','reading':'every E6 row meets each tetrad in even cardinality'},
      'Golay_boundary':'A chosen F4-structure feeds the Pass4592 hexacode and the frozen Pass4615 Golay/MOG completion. The PGSp action on the 40 choice structures is not transported to an M24 action on the frozen Golay coordinates.',
      'theorem':'The 45x40 sentinel/center-quad matrix is an exact incidence geometry between 45 E6 carrier objects and the 40 compatible F4 structures on U6. Its 40 minimal binary-even tetrads are precisely the W33 lines, so both W33 point/line geometry is recovered inside the moduli of hexacode-compatible choices.',
      'boundary':'Finite moduli/incidence statement. It does not produce 40 PGSp-related MOG sextets inside one fixed Golay coordinate model.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
