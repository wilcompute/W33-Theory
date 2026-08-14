#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(name): return json.loads((ROOT/'data'/name).read_text())
def main():
    a=J('PART_W33_PASS5110_CHAMBER_KERNEL_CUTSPACE.json')
    b=J('PART_W33_PASS5111_Q5_CUT_GAUGE_LEADER_BARRIER.json')
    c=J('PART_W33_PASS5112_INTRINSIC_ROOT_CHART_RECONSTRUCTION.json')
    d=J('PART_W33_PASS5113_Q3_EQUIVARIANT_RADIUS3_DECODER.json')
    e=J('PART_W33_PASS5114_SQRT17_ORDER_LADDER.json')
    f=J('PART_W33_PASS5115_Q5_ROOT_COSET_NATIVE_RANK_DEFECT.json')
    g=J('PART_W33_PASS5116_CODE_INTRINSIC_U81_CONTROLLER.json')
    h=J('PART_W33_PASS5117_PERFECT_APARTMENT_CHAMBER_DUALITY.json')
    assert a['anchors']['5']['chamber_star_rank']==625 and a['anchors']['5']['kernel_dimension']==311
    assert b['table']['13']['weight_lower_bound']==625 and '>=14' in b['conclusion']
    assert c['anchors']['3']['recovered_charts']==1080 and c['anchors']['4']['recovered_roots']==27200
    assert d['base_fixed_triples_tested']==1309771 and d['second_sweep_failures']==0 and d['global_guaranteed_error_weight']==3
    assert e['discriminants'] if 'discriminants' in e else [x['discriminant'] for x in e['orders']]==[17,68,272]
    assert f['anchors']['q5']['ranks']['5']==397 and f['q5_native_defect']['drop']==8
    assert g['controller']['semidirect_order']==324 and g['chosen_chamber_local_data']['active_charts']==108
    assert h['anchors']['5']['perfect_dual_dimension']==625 and h['anchors']['3']['cut_dimension']==79
    z=J('PART_W33_PASS5110_5117_RESULTS.json')
    assert z['5111']['later_strengthening']=='Pass5118 raises the barrier to >=17'
    assert 'q7' in z['5115']['later_falsifier']
    print('PASS5110-5117 frozen regression: PASS')
if __name__=='__main__': main()
