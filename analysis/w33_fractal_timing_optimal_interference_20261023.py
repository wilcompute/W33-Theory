#!/usr/bin/env python3
"""Exhaustive optical timing + coherent frame compatibility of W33 path pairs."""
import itertools,json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_time_expanded_linebus_20261023 import fixed_path_schedule
from w33_fractal_linebus_switch_matrix_20261023 import ADJ
def census():
    comparisons=0;equal_arrival_nontriv=[];zero_wait_phase_mismatches=0
    hist={}
    for src in range(40):
        for dst in range(src+1,40):
            if dst in ADJ[src]:continue
            common=sorted(set(ADJ[src])&set(ADJ[dst]))
            assert len(common)==4
            paths=[fixed_path_schedule((src,m,dst),start_slot=0) for m in common]
            for a,b in itertools.combinations(paths,2):
                comparisons+=1
                d=(a['optical_frame_exponent']-b['optical_frame_exponent'])%4
                if d and a['wait_slots']==b['wait_slots']==0:zero_wait_phase_mismatches+=1
                if d and a['elapsed_slots']==b['elapsed_slots']:
                    equal_arrival_nontriv.append({
                      'path_a':a['route'],'path_b':b['route'],
                      'arrival_slots':a['elapsed_slots'],
                      'waits_a':a['wait_slots'],'waits_b':b['wait_slots'],
                      'relative_i_exponent':d})
                    key=(a['elapsed_slots'],d)
                    hist[key]=hist.get(key,0)+1
    assert comparisons==3240 and zero_wait_phase_mismatches==0
    equal_arrival_nontriv.sort(key=lambda x:
        (x['arrival_slots'],x['waits_a']+x['waits_b'],x['path_a'],x['path_b']))
    best=equal_arrival_nontriv[0]
    assert len(equal_arrival_nontriv)==192 and best['arrival_slots']==4
    return {'schema':'w33.linebus.timed_coherent_two_hop.v1',
      'all_path_pair_comparisons':comparisons,
      'same_start_same_arrival_nontrivial_phase_pairs':len(equal_arrival_nontriv),
      'no_wait_nontrivial_phase_pairs':zero_wait_phase_mismatches,
      'minimum_same_arrival_witness':best,
      'relative_phase_histogram':{f't={t};i_exp={e}':n for (t,e),n in sorted(hist.items())},
      'proof_boundary':'with two consecutive no-WAIT moves under globally fixed mask slots, each path has the same mask sequence and thus identical ideal i-phase frame',
      'experiment_boundary':['same discrete tick does not imply same optical carrier phase',
        'all WAIT events require physical optical delay or storage',
        'switch settling and group-delay dispersion unmodelled']}
if __name__=='__main__':
    o=census()
    p=ROOT/'data/w33_fractal_timing_optimal_interference_20261023.json'
    p.write_text(json.dumps(o,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print('PASS',o['same_start_same_arrival_nontrivial_phase_pairs'],o['minimum_same_arrival_witness'])
