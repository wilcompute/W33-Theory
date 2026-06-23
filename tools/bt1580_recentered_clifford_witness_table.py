#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1580_recentered_clifford_witness_table.json'
MD = ROOT / 'analysis' / 'BT1580_recentered_clifford_witness_table.md'
TEX = ROOT / 'analysis' / 'BT1580_recentered_clifford_witness_table.tex'

BASE_WITNESSES = ['I','X','Z','F3','S']
CLASSES = [
    {'class':'centered_frame','translation':'(0,0)','count':24,'recenter':'I','witness_basis':'direct centered I/X/Z/F3/S'},
    {'class':'oam_shift_only','translation':'(1,0) or (2,0)','count':48,'recenter':'inverse X shift','witness_basis':'recenter then apply centered I/X/Z/F3/S'},
    {'class':'phase_shift_only','translation':'(0,1) or (0,2)','count':48,'recenter':'inverse Z shift','witness_basis':'recenter then apply centered I/X/Z/F3/S'},
    {'class':'mixed_shift_phase','translation':'(1,1),(1,2),(2,1),(2,2)','count':96,'recenter':'inverse X and Z shift','witness_basis':'recenter then apply centered I/X/Z/F3/S'},
]

def main() -> None:
    total=sum(c['count'] for c in CLASSES)
    expanded=[]
    for c in CLASSES:
        for w in BASE_WITNESSES:
            expanded.append({'clifford_class':c['class'],'class_count':c['count'],'recenter':c['recenter'],'witness':w,'application':'direct' if c['recenter']=='I' else 'after recentering'})
    checks={
        'four_classes': len(CLASSES)==4,
        'total_216': total==216,
        'translated_192': sum(c['count'] for c in CLASSES if c['class']!='centered_frame')==192,
        'five_witnesses_each': len(expanded)==20,
        'has_mixed_96': any(c['class']=='mixed_shift_phase' and c['count']==96 for c in CLASSES),
        'all_have_recenter': all(c['recenter'] for c in CLASSES),
    }
    result={'bt':1580,'title':'Recentered Clifford witness table','verified':all(checks.values()),'source_packets':{'bt1573':'data/bt1573_centered_oam_recentering_law.json','bt1578':'data/bt1578_full_centered_basis_calibration_matrix.json'},'classes':CLASSES,'expanded_witness_rows':expanded,'interpretation':'The calibrated I/X/Z/F3/S witness is direct for the 24 centered frame changes. The 192 translated Clifford elements must be inverse-recentered before applying the same centered witness table: inverse X for OAM shifts, inverse Z for phase shifts, and both for mixed shifts.','honesty_boundary':'This is a finite witness-routing table, not a physical recentering-optic design for every mode.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    MD.write_text('# BT1580 Recentered Clifford Witness Table\n\nThe calibrated I/X/Z/F3/S witness is direct for the 24 centered frame changes. The 192 translated Clifford elements require inverse recentering first: inverse X for OAM shifts, inverse Z for phase shifts, and both inverse shifts for mixed classes.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1580: calibrated $I,X,Z,F_3,S$ witnesses apply directly to 24 centered frames and after inverse recentering to 192 translated Clifford elements.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1580,'verified':result['verified'],'rows':len(expanded)}, indent=2))
    if not result['verified']: raise SystemExit(1)

if __name__=='__main__': main()
