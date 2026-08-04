#!/usr/bin/env python3
"""Pass 3178: optimal twelve-phase epoch family correcting three arbitrary edits."""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_BT3178_THREE_EDIT_PHASE_EPOCH_results.json'
Q=24;N=7;T=3;PAYLOAD=(7,2,16,23,20,15,0,2,7,11,16,19);PHASE=(1,3,4,5,6,8,9,10,12,13,14,17)
def ball_count():
    by={}
    for m in range(N-T,N+T+1):
        total=0
        for c in range(m+1):
            if max(N,m)-min(N,c)<=T:total+=math.comb(m,c)*(Q-1)**(m-c)
        by[str(m)]=total
    return by,sum(by.values())
def main():
    assert set(PHASE).isdisjoint(PAYLOAD) and len(set(PHASE))==12
    by,total=ball_count();assert total==3667012
    out={'schema':'w33.pass3178.three_edit_phase_epoch.v1','alphabet_size':Q,'phases':12,'phase_symbols':list(PHASE),'marker_length':N,'corrected_edits':T,'marker_family':'M_p=u_p^7','minimum_marker_distance':7,'minimum_marker_to_payload_distance':7,'optimality':'unique correction of t=3 adversarial edits requires d_min>=2t+1=7','radius_three_ball_by_received_length':by,'radius_three_ball_size_per_phase':total,'total_distinct_phase_labelled_traces':12*total,'clean_payload_symbols_after_marker':0,'proof':'For constant marker a^7 and received word y of length m containing c copies of a, d_L=max(7,m)-min(7,c).','boundary':'Exact combinatorial insdel/substitution theorem. Physical symbol confusion and marker frequency are unmeasured.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
