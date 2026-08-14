#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(name):return json.loads((ROOT/'data'/name).read_text())

def test_pass5118_5125_frozen_certificates():
    a=J('PART_W33_PASS5118_Q5_DELSARTE_LEADER17.json')
    assert a['status']=='THEOREM_Q5_COUNTEREXAMPLE_LEADER_AT_LEAST_17'
    assert [r['bonferroni_weight_lower_bound'] for r in a['delsarte_rows']]==[1160,925,680]
    b=J('PART_W33_PASS5119_THETA_HALF_REGULAR_SUPPORT.json')
    assert b['anchors']['5']['selected_induced_degree']==16
    c=J('PART_W33_PASS5120_U81_STATE_PROGRAM_TRANSPORT.json')
    assert c['q3_bijection'] and c['program_coordinates'][-1]=='d+2ac+a^2 b'
    d=J('PART_W33_PASS5121_Q3_INTEGRAL_TORSION_MODULE.json')
    assert d['rational_left_kernel_dimension']==12 and d['mod3_left_kernel_dimension']==13
    assert d['V4_character']=={'e':'+','a':'-','b':'+','c':'-'}
    e=J('PART_W33_PASS5122_LIE_TYPE_JENNINGS_MEMORY.json')
    assert e['safe_examples']['G2_p7']['coefficient_sum']==117649
    f=J('PART_W33_PASS5123_Q7_NATIVE_RANK_FALSIFIER.json')
    assert f['anchors']['q7']['drop']==10
    g=J('PART_W33_PASS5124_BINARY_BICYCLE_ODD_Q.json')
    assert [g['anchors'][str(q)]['Levi_bicycle_dimension'] for q in (2,3,5,7)]==[0,29,129,349]
    h=J('PART_W33_PASS5125_TORSION_TRIALITY_MODULE_WELD.json')
    assert h['V4_character_on_both']==d['V4_character']
    ns=J('w33_pass_namespace_registry_v2.d/5118-5125.json')
    assert ns['range']==[5118,5125]
