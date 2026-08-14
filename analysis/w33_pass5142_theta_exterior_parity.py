#!/usr/bin/env python3
"""Pass5142: exterior theta-neighbor parity and active-check conservation.

Pass5119 already proves half-regularity on selected vertices.  This pass extracts
the complementary constraint: every unselected apartment sees an even number of
selected theta-neighbors, and active theta checks obey an exact conservation law.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5142_THETA_EXTERIOR_PARITY.json'

def row(q):
    s=q**4;k=4*(q-1);active=2*(q-1)*s
    return {'q':q,'chamber_star_weight':s,'selected_degree':k,
            'active_theta_checks':active,'exterior_vertices_with_two_selected_neighbors':active,
            'boundary_selected_neighbor_sum':2*active}

def main():
    out={'pass':5142,'status':'THEOREM_ALL_Q_THETA_EXTERIOR_PARITY_CONSERVATION',
         'statement':'For every binary apartment-code support S, each exterior apartment has an even number t_v of selected theta-neighbors. The number of active theta triples is exactly 2(q-1)|S|.',
         'proof':'A theta triple has even codeword parity, hence 0 or 2 selected variables. For v outside S, every active triple through v contributes its other two selected vertices, so t_v is even. Counting selected-variable/check incidences gives 4(q-1)|S|=2 A_active.',
         'identities':['A_active=2(q-1)|S|','sum_{v outside S} t_v=4(q-1)|S|','if b_{2r}=#{v outside:t_v=2r}, then sum_r r b_{2r}=2(q-1)|S|'],
         'chamber_star_equality':'For a chamber star all exterior t_v are 0 or 2, so b_2=2(q-1)q^4 and all b_{2r}=0 for r>=2.',
         'anchors':[row(q) for q in (2,3,4,5)],
         'role':'This is the exterior parity/conservation refinement of Pass5119 and is the exact input to the second-moment curvature theorem in Pass5143.',
         'boundary':'The exterior parity law does not by itself classify codeword supports or prove minimum distance.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
