#!/usr/bin/env python3
"""BT1802: bounded search for 12-symbol fibre rules above BT1795."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1802_fibre_rule_search.json'
COUNTS=np.array([528,562,578,528,612,580,528,528,480,528,612,564,562,528,578,562,562,560],dtype=int)
LEFT_F2=np.array([[1,0,0,1,1,0,1,0,1,0,0,1,0,1,1,0,1,0],[0,1,1,0,0,1,0,1,0,1,1,0,1,0,0,1,0,1]],dtype=int)
LEFT_F3=np.array([[1,0,0,1,2,0,2,0,0,0,0,2,0,1,0,0,0,0],[2,0,0,1,1,0,2,0,2,0,0,0,0,0,1,0,0,0],[0,0,2,0,0,2,0,1,0,1,2,0,0,0,0,1,0,0],[1,0,2,2,0,2,0,1,0,2,1,0,0,0,0,0,1,0],[2,2,1,1,1,1,2,1,2,1,0,0,1,0,1,1,0,1]],dtype=int)
POINT_REL=[-1,1,1,-1,-1,1,-1,1,-1,1,1,-1,1,-1,-1,1,-1,1]
def main():
    payload={'bt':'BT1802','title':'structured 12-symbol fibre rule search','counts':COUNTS.tolist(),'total':int(COUNTS.sum()),'tests':{'12=3x4_uniform_residue_lift':{'required_multiple':64,'passes':bool(np.all(COUNTS%64==0)),'mod64_histogram':dict(Counter(map(int,COUNTS%64)))},'12=2x6_uniform_binary_lift':{'required_multiple':216,'passes':bool(np.all(COUNTS%216==0)),'mod216_histogram':dict(Counter(map(int,COUNTS%216)))},'coarse_binary_or_quartic_lift':{'required_multiple':8,'passes':bool(np.all(COUNTS%8==0)),'mod8_histogram':dict(Counter(map(int,COUNTS%8)))},'point_additive_27_potential_model':{'left_relation':POINT_REL,'left_relation_dot_counts':int(np.dot(np.array(POINT_REL),COUNTS)),'passes':int(np.dot(np.array(POINT_REL),COUNTS))==0},'double_six_syndrome_over_F2':{'left_kernel_evaluations':(LEFT_F2@COUNTS%2).astype(int).tolist(),'passes':bool(np.all((LEFT_F2@COUNTS)%2==0))},'double_six_syndrome_over_F3':{'left_kernel_evaluations':(LEFT_F3@COUNTS%3).astype(int).tolist(),'passes':bool(np.all((LEFT_F3@COUNTS)%3==0))}},'conclusion':'The 9980 vector fails every simple structured 12-symbol rule tested except trivial even parity over F2. It is not a uniform 3x4 lift, not a uniform 2x6 lift, not point-additive on H27, and not a pure F3 double-six syndrome.'}
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'total':int(COUNTS.sum()),'mod64':bool(np.all(COUNTS%64==0)),'mod216':bool(np.all(COUNTS%216==0)),'F2':payload['tests']['double_six_syndrome_over_F2']['passes'],'F3':payload['tests']['double_six_syndrome_over_F3']['passes']},indent=2,sort_keys=True))
if __name__=='__main__': main()
