#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1584_recentered_protocol_table_expansion.json'
MD = ROOT / 'analysis' / 'BT1584_recentered_protocol_table_expansion.md'
TEX = ROOT / 'analysis' / 'BT1584_recentered_protocol_table_expansion.tex'

CLASSES = [
    {'recenter_class':'centered_frame','count':24,'correction':'I','witness':'I/X/Z/F3/S direct','leakage_threshold':'operation-specific BT1577 threshold','failure_mode':'visibility or covariance failure'},
    {'recenter_class':'oam_shift_only','count':48,'correction':'inverse X shift','witness':'I/X/Z/F3/S after recentering','leakage_threshold':'X envelope plus target-operation envelope','failure_mode':'OAM shift recentering fails or leakage exceeds threshold'},
    {'recenter_class':'phase_shift_only','count':48,'correction':'inverse Z shift','witness':'I/X/Z/F3/S after recentering','leakage_threshold':'Z envelope plus target-operation envelope','failure_mode':'phase recentering fails or visibility signature drifts'},
    {'recenter_class':'mixed_shift_phase','count':96,'correction':'inverse X and inverse Z shift','witness':'I/X/Z/F3/S after recentering','leakage_threshold':'mixed recentering envelope plus target-operation envelope','failure_mode':'mixed correction fails, radial leakage grows, or basis covariance breaks'},
]
GATE_ROWS = [
    {'operation':'I','expected':'V(I)=1','base_threshold':'|delta V| <= 0.05','tier':'exact witness'},
    {'operation':'X','expected':'V(X)=0','base_threshold':'|V| <= 0.05, radial <= 0.08','tier':'exact/calibrated'},
    {'operation':'Z','expected':'V(Z)=0','base_threshold':'|V| <= 0.05, radial <= 0.02','tier':'exact/calibrated'},
    {'operation':'F3','expected':'V(F3)=1/3','base_threshold':'|delta V| <= 0.05, radial <= 0.10','tier':'exact/calibrated'},
    {'operation':'S','expected':'phase signature [1,0,1]','base_threshold':'signature match, radial <= 0.05','tier':'finite exact / lab calibrated'},
]

def main() -> None:
    rows=[]
    for c in CLASSES:
        for g in GATE_ROWS:
            rows.append({**c, **g, 'protocol_action': f"{c['correction']} then {g['operation']} witness" if c['correction'] != 'I' else f"direct {g['operation']} witness"})
    checks={
        'four_recenter_classes': len(CLASSES)==4,
        'five_gate_rows': len(GATE_ROWS)==5,
        'twenty_expanded_rows': len(rows)==20,
        'class_counts_sum_216': sum(c['count'] for c in CLASSES)==216,
        'has_mixed_class_96': any(c['recenter_class']=='mixed_shift_phase' and c['count']==96 for c in CLASSES),
        'all_rows_have_failure_mode': all(r['failure_mode'] for r in rows),
        'all_rows_have_threshold': all(r['base_threshold'] and r['leakage_threshold'] for r in rows),
    }
    result={'bt':1584,'title':'Recentered protocol table expansion','verified':all(checks.values()),'source_packets':{'bt1575':'data/bt1575_protocol_table.json','bt1580':'data/bt1580_recentered_clifford_witness_table.json','bt1581':'data/bt1581_radial_leakage_pass_fail_simulator.json'},'recenter_classes':CLASSES,'gate_rows':GATE_ROWS,'expanded_rows':rows,'interpretation':'The publication protocol is expanded by recentering class. Each Clifford class now has a correction operator, calibrated witness, leakage threshold family, failure mode, and claim tier.','honesty_boundary':'Protocol-table expansion only; no lab data and no paper rewrite are claimed.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    md=['# BT1584 Recentered Protocol Table Expansion','','| Class | Count | Correction | Gate | Expected | Threshold | Failure | Tier |','|---|---:|---|---|---|---|---|---|']
    for r in rows:
        md.append(f"| {r['recenter_class']} | {r['count']} | {r['correction']} | {r['operation']} | {r['expected']} | {r['base_threshold']} / {r['leakage_threshold']} | {r['failure_mode']} | {r['tier']} |")
    MD.write_text('\n'.join(md)+'\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1584: protocol table expands to 20 recentered rows: four Clifford classes times five calibrated witnesses.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1584,'verified':result['verified'],'rows':len(rows)}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
