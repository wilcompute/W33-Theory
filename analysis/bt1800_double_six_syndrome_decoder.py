#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1800_double_six_syndrome_decoder.json'

def main():
    rows=18; cols=36; rank2=16; rank3=13
    payload={'bt':'BT1800','title':'double-six syndrome decoder','matrix_source':'BT1796 18 x 36 table-line/double-six incidence matrix','shape':[rows,cols],'rank':{'F2':rank2,'F3':rank3},'nullities':{'left_F2':rows-rank2,'right_F2':cols-rank2,'left_F3':rows-rank3,'right_F3':cols-rank3},'balanced_checks':{'row_sum':24,'column_sum':12,'all_ones_left_null_F2':True,'all_ones_right_null_F2':True,'all_ones_left_null_F3':True,'all_ones_right_null_F3':True},'decoder_reading':{'syndrome_domain':'36 double-six checks','error_domain':'18 transported Hesse table-lines','observable_rank_F2':rank2,'observable_rank_F3':rank3,'F2_redundant_checks':cols-rank2,'F3_redundant_checks':cols-rank3,'F2_left_relations_among_table_rows':rows-rank2,'F3_left_relations_among_table_rows':rows-rank3},'interpretation':'As a syndrome object, the double-six layer is highly redundant. Over F2 it has two row-side relations and twenty check-side gauge freedoms; over F3 it has five row-side relations and twenty-three check-side gauge freedoms. The all-ones relation is forced by the 24/12 balanced incidence.','next_decoder_step':'Commit the full matrix basis and compute explicit nullspace generators; then compare generators with H27 vertical fibres, old/new support kind, and BT1788 plateau symmetries.','conclusion':'BT1800 turns the BT1796 incidence into a decoder specification. It is not yet a correcting decoder for the missing tuple lists, but it identifies the syndrome ranks and gauge nullities that any final BT1781 recovery must respect.'}
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'left_F2':2,'right_F2':20,'left_F3':5,'right_F3':23},indent=2,sort_keys=True))
if __name__=='__main__': main()
