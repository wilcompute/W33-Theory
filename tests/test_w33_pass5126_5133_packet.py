from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def J(name):return json.loads((ROOT/'data'/name).read_text())
def test_q5_leader18():
    z=J('PART_W33_PASS5126_Q5_LEADER18_EXACT.json');assert z['sharp_wedge_cap']==25;assert z['delsarte']['distance_pair_counts']==[25,66,45,0];assert z['delsarte']['weight_lower_bound']==625
def test_q5_coarea_defect():
    z=J('PART_W33_PASS5127_Q5_COAREA_DEFECT_QUANTIZATION.json');assert z['smallest_nonzero_defect']['heavy_charts']==3;assert z['smallest_nonzero_defect']['A_type']==248
def test_q3_decoder_radius5():
    a=J('PART_W33_PASS5128_Q3_EQUIVARIANT_RADIUS4_DECODER.json');b=J('PART_W33_PASS5131_Q3_EQUIVARIANT_RADIUS5_DECODER.json');assert a['global_guaranteed_error_weight']==4;assert b['global_guaranteed_error_weight']==5;assert b['global_sweep_bound']==3
def test_allq_controller_and_theta():
    a=J('PART_W33_PASS5129_ALLQ_INTRINSIC_UNIPOTENT_CONTROLLER.json');b=J('PART_W33_PASS5132_THETA_CAYLEY_MINIMUM_SUPPORT.json')
    for q in (2,3,4,5):
        assert a['anchors'][str(q)]['U_order']==q**4;assert a['anchors'][str(q)]['active_charts']==4*q**3;assert b['anchors'][str(q)]['degree']==4*(q-1)
def test_oddq_bicycle():
    z=J('PART_W33_PASS5130_ODDQ_BICYCLE_THEOREM.json')
    for q in (3,5,7,11):assert z['anchors'][str(q)]['Levi_bicycle_dimension']==q**3+q-1
def test_allq_compiler():
    z=J('PART_W33_PASS5133_ALLQ_STATE_PROGRAM_POLYNOMIAL_COMPILER.json')
    for q in (2,3,4,5):assert z['anchors'][str(q)]['states']==q**4 and z['anchors'][str(q)]['compiler_bijective']
def test_consolidated_boundary():
    z=J('PART_W33_PASS5126_5133_RESULTS.json');assert z['5126']['q5_counterexample_leader_min']==18;assert 'remains open' in z['boundary']
