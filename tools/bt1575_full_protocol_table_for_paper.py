#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1575_full_protocol_table_for_paper.json'
MD = ROOT / 'analysis' / 'BT1575_full_protocol_table_for_paper.md'
TEX = ROOT / 'analysis' / 'BT1575_full_protocol_table_for_paper.tex'

ROWS = [
    {'stage':'prepare','operation':'single photon + centered OAM basis','expected':'ell=-1,0,+1 maps to labels 2,0,1','threshold':'OAM leakage <= 0.10','failure':'support outside ternary OAM subspace','tier':'engineering'},
    {'stage':'prepare','operation':'axial three-bin ladder','expected':'past/future qutrit Choi support','threshold':'time-bin visibility calibrated','failure':'loss of temporal Bell support','tier':'structural'},
    {'stage':'control','operation':'operator leg off','expected':'no active gate trace pattern','threshold':'must fail active signature','failure':'passive labels mimic all active gates','tier':'falsifier'},
    {'stage':'gate','operation':'I','expected':'V(I)=1','threshold':'|delta V| <= 0.05','failure':'identity reference misses tolerance','tier':'exact witness'},
    {'stage':'gate','operation':'X','expected':'V(X)=0','threshold':'|V| <= 0.05','failure':'shift trace nonzero','tier':'exact witness'},
    {'stage':'gate','operation':'Z','expected':'V(Z)=0','threshold':'|V| <= 0.05','failure':'phase trace nonzero','tier':'exact witness'},
    {'stage':'gate','operation':'F3','expected':'V(F3)=1/3','threshold':'|delta V| <= 0.05','failure':'mixer trace misses one-third','tier':'exact witness'},
    {'stage':'gate','operation':'S','expected':'phase signature [1,0,1]','threshold':'signature match after calibration','failure':'lens phase fails centered qutrit S','tier':'finite exact / lab calibrated'},
    {'stage':'leakage','operation':'radial shell check','expected':'sector/gauge shell stable','threshold':'radial leakage <= 0.10','failure':'radial mixing destroys labels','tier':'engineering'},
    {'stage':'covariance','operation':'basis relabel by mod-3 decoding','expected':'same decoded predictions','threshold':'all core gates invariant after decoding','failure':'label convention changes physics','tier':'falsifier'},
    {'stage':'reference','operation':'external optic comparison','expected':'same trace signatures as internal operator setting','threshold':'within calibrated tolerance','failure':'internal action cannot reproduce external control','tier':'engineering/falsifier'},
]

def main() -> None:
    checks={'eleven_rows':len(ROWS)==11,'has_prepare_gate_leakage_covariance_reference':{'prepare','control','gate','leakage','covariance','reference'} <= {r['stage'] for r in ROWS},'all_have_threshold':all(r['threshold'] for r in ROWS),'all_have_failure':all(r['failure'] for r in ROWS),'exact_witnesses_four':sum(r['tier']=='exact witness' for r in ROWS)==4,'s_row_present':any(r['operation']=='S' for r in ROWS)}
    result={'bt':1575,'title':'Full protocol table for paper','verified':all(checks.values()),'source':'data/bt1572_passive_vs_active_experimental_protocol.json','rows':ROWS,'interpretation':'This table is paper-ready: each row has preparation/operation, expected readout, leakage or visibility threshold, failure mode, and claim tier. It separates exact trace-Choi witnesses from engineering thresholds and falsifier controls.','honesty_boundary':'Threshold values are protocol placeholders pending lab calibration; table is ready for paper insertion but not experimental evidence.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    md=['# BT1575 Full Protocol Table for Paper','','| Stage | Operation | Expected | Threshold | Failure | Tier |','|---|---|---|---|---|---|']
    for r in ROWS:
        md.append(f"| {r['stage']} | {r['operation']} | {r['expected']} | {r['threshold']} | {r['failure']} | {r['tier']} |")
    MD.write_text('\n'.join(md)+'\n', encoding='utf-8')
    tex=['\\begin{tabular}{lllll}','Stage & Operation & Expected & Failure & Tier \\\\','\\hline']
    for r in ROWS:
        tex.append(f"{r['stage']} & {r['operation']} & {r['expected']} & {r['failure']} & {r['tier']} \\\")
    tex.append('\\end{tabular}\n')
    TEX.write_text('\n'.join(tex), encoding='utf-8')
    print(json.dumps({'bt':1575,'verified':result['verified'],'rows':len(ROWS)}, indent=2))
    if not result['verified']: raise SystemExit(1)

if __name__=='__main__': main()
