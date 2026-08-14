#!/usr/bin/env python3
"""Pass5144: exact q=7 native-characteristic root-coset rank test.

Pass5115 observed native rank drops 1 and 8 at q=3,5, numerically matching
((q-1)/2)^3 at only two odd anchors and explicitly kept that as conjectural.
This pass computes the third odd anchor q=7 and kills that interpolation.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5115_q5_root_coset_native_rank_defect import incidence,rank_mod
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5144_Q7_ROOT_COSET_NATIVE_RANK.json'

def main():
    q=7;M=incidence(q);assert M.shape==(2401,1372)
    ranks={str(p):rank_mod(M,p) for p in (2,3,5,7,11)}
    assert ranks=={'2':1183,'3':1183,'5':1183,'7':1173,'11':1183}
    generic=1183;native=1173;drop=generic-native;old=((q-1)//2)**3
    assert drop==10 and old==27 and drop!=old
    out={'pass':5144,'status':'FALSIFIED_TWO_ANCHOR_NATIVE_DROP_CUBE_LAW',
         'q':q,'shape':list(M.shape),'column_weight':q,'row_weight':4,'ranks':ranks,
         'generic_observed_rank':generic,'native_F7_rank':native,'native_rank_drop':drop,
         'previous_two_anchor_guess':'((q-1)/2)^3','guess_at_q7':old,'guess_falsified':True,
         'kernel_dimensions':{'generic_column':1372-generic,'native_column':1372-native,
                              'generic_left':2401-generic,'native_left':2401-native},
         'consequence':'The q=3,5 drops 1,8 do not continue as a cubic law. The native defect is genuinely modular/representation-theoretic and requires a structural formula.',
         'boundary':'Generic rank here means the common rank observed over F2,F3,F5,F11, all non-native for q=7. No all-q generic-rank formula is inferred from this finite table.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
