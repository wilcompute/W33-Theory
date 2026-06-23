#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1577_radial_leakage_bound_from_oam_phase_ops.json'
MD = ROOT / 'analysis' / 'BT1577_radial_leakage_bound_from_oam_phase_ops.md'
TEX = ROOT / 'analysis' / 'BT1577_radial_leakage_bound_from_oam_phase_ops.tex'

RADIAL = [0, 1, 2]
OPS = [
    {'op':'I', 'eta':0.00, 'reason':'reference action'},
    {'op':'Z', 'eta':0.02, 'reason':'azimuthal phase mask should mostly preserve radial shell'},
    {'op':'S', 'eta':0.05, 'reason':'quadratic phase/lens row can couple weakly to radial curvature'},
    {'op':'X', 'eta':0.08, 'reason':'OAM shift can disturb radial envelope'},
    {'op':'F3', 'eta':0.10, 'reason':'three-mode mixer has the largest allowed calibration envelope'},
]

def leakage_matrix(eta: float):
    if eta == 0:
        return [[1.0 if i == j else 0.0 for j in RADIAL] for i in RADIAL]
    off = eta / 2.0
    return [[round(1.0-eta, 6) if i == j else round(off, 6) for j in RADIAL] for i in RADIAL]

def row_sums(mat):
    return [round(sum(row), 6) for row in mat]

def main() -> None:
    rows=[]
    for o in OPS:
        mat=leakage_matrix(o['eta'])
        rows.append({**o, 'matrix':mat, 'row_sums':row_sums(mat), 'passes_default_threshold': o['eta'] <= 0.10})
    worst=max(r['eta'] for r in rows)
    checks={
        'five_ops': len(rows)==5,
        'three_radial_shells': RADIAL==[0,1,2],
        'all_row_stochastic': all(all(abs(s-1.0)<1e-9 for s in r['row_sums']) for r in rows),
        'worst_bound_010': abs(worst-0.10)<1e-9,
        'all_pass_default_threshold': all(r['passes_default_threshold'] for r in rows),
        'nonzero_leakage_ops_four': sum(r['eta']>0 for r in rows)==4,
    }
    result={'bt':1577,'title':'Radial leakage bound from OAM phase operations','verified':all(checks.values()),'source_packets':{'bt1576':'data/bt1576_oam_entanglement_literature_bridge.json','bt1575':'data/bt1575_protocol_table.json'},'radial_shells':RADIAL,'rows':rows,'default_threshold':0.10,'interpretation':'The radial leakage model gives a symbolic row-stochastic leakage matrix for each internal operation. I has zero leakage; Z, S, X, and F3 receive increasing leakage envelopes. The current protocol threshold is 0.10, with F3 as the worst allowed case.','honesty_boundary':'This is a symbolic engineering bound motivated by OAM/radial coupling literature; it is not measured optical leakage.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    MD.write_text('# BT1577 Radial Leakage Bound from OAM Phase Operations\n\nA symbolic row-stochastic leakage matrix is assigned to each internal operation across radial shells p=0,1,2. I has zero leakage; Z, S, X, and F3 receive increasing envelopes up to the default 0.10 threshold. This is an engineering bound, not measured optical leakage.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1577: radial leakage bounds assign row-stochastic $3\\times3$ shell matrices to $I,Z,S,X,F_3$, with worst allowed envelope $0.10$.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1577,'verified':result['verified'],'worst_bound':worst}, indent=2))
    if not result['verified']: raise SystemExit(1)

if __name__=='__main__': main()
