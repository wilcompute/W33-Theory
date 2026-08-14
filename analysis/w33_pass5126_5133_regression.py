#!/usr/bin/env python3
"""Frozen regression for Pass5126-5133."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(name):return json.loads((ROOT/'data'/name).read_text())
def main():
    a=J('PART_W33_PASS5126_Q5_LEADER18_EXACT.json');assert a['leader_size_closed']==17 and a['sharp_wedge_cap']==25 and a['delsarte']['weight_lower_bound']==625
    b=J('PART_W33_PASS5127_Q5_COAREA_DEFECT_QUANTIZATION.json');assert b['smallest_nonzero_defect']=={'active_chart_deficit':2,'h8':2,'h9':1,'A_type':248,'heavy_charts':3}
    c=J('PART_W33_PASS5128_Q3_EQUIVARIANT_RADIUS4_DECODER.json');assert c['global_guaranteed_error_weight']==4 and c['fixed_base_connected_component_counts']['4']==13269
    d=J('PART_W33_PASS5129_ALLQ_INTRINSIC_UNIPOTENT_CONTROLLER.json');assert all(d['anchors'][str(q)]['exact_hypergraph_match'] for q in (2,3,4,5))
    e=J('PART_W33_PASS5130_ODDQ_BICYCLE_THEOREM.json');assert e['bicycle_formula']=='dim Bike_2(Levi)=q^3+q-1' and e['anchors']['11']['Levi_bicycle_dimension']==1341
    f=J('PART_W33_PASS5131_Q3_EQUIVARIANT_RADIUS5_DECODER.json');assert f['global_guaranteed_error_weight']==5 and f['fixed_base_connected_counts']['5']==381480
    g=J('PART_W33_PASS5132_THETA_CAYLEY_MINIMUM_SUPPORT.json');assert g['anchors']['5']['degree']==16 and g['anchors']['5']['exact_edge_match']
    h=J('PART_W33_PASS5133_ALLQ_STATE_PROGRAM_POLYNOMIAL_COMPILER.json');assert all(h['anchors'][str(q)]['compiler_bijective'] for q in (2,3,4,5))
    z=J('PART_W33_PASS5126_5133_RESULTS.json');assert z['5126']['q5_counterexample_leader_min']==18 and z['5131']['q3_decoder_radius']==5
    reg=J('w33_pass_namespace_registry_v2.d/5126-5133.json');assert reg['range']==[5126,5133]
    print('PASS5126-5133 frozen regression OK')
if __name__=='__main__':main()
