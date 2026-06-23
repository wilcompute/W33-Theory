#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1581_radial_leakage_pass_fail_simulator.json'
MD = ROOT / 'analysis' / 'BT1581_radial_leakage_pass_fail_simulator.md'
TEX = ROOT / 'analysis' / 'BT1581_radial_leakage_pass_fail_simulator.tex'

THRESHOLD = 0.10
SCENARIOS = [
    {'name':'ideal_reference','op':'I','observed_leakage':0.00,'visibility_error':0.00,'basis_covariant':True},
    {'name':'good_spiral_phase','op':'Z','observed_leakage':0.02,'visibility_error':0.02,'basis_covariant':True},
    {'name':'good_lens_phase','op':'S','observed_leakage':0.05,'visibility_error':0.03,'basis_covariant':True},
    {'name':'edge_oam_shift','op':'X','observed_leakage':0.08,'visibility_error':0.04,'basis_covariant':True},
    {'name':'max_mixer_pass','op':'F3','observed_leakage':0.10,'visibility_error':0.05,'basis_covariant':True},
    {'name':'radial_leak_fail','op':'F3','observed_leakage':0.14,'visibility_error':0.04,'basis_covariant':True},
    {'name':'visibility_fail','op':'Z','observed_leakage':0.02,'visibility_error':0.09,'basis_covariant':True},
    {'name':'basis_fail','op':'X','observed_leakage':0.04,'visibility_error':0.03,'basis_covariant':False},
]

def classify(s):
    leakage_ok=s['observed_leakage']<=THRESHOLD
    visibility_ok=s['visibility_error']<=0.05
    covariance_ok=bool(s['basis_covariant'])
    passed=leakage_ok and visibility_ok and covariance_ok
    failures=[]
    if not leakage_ok: failures.append('radial_leakage')
    if not visibility_ok: failures.append('visibility')
    if not covariance_ok: failures.append('basis_covariance')
    return {'pass':passed,'leakage_ok':leakage_ok,'visibility_ok':visibility_ok,'basis_covariance_ok':covariance_ok,'failure_modes':failures or ['none']}

def main() -> None:
    rows=[]
    for s in SCENARIOS:
        rows.append({**s,'classification':classify(s)})
    checks={
        'eight_scenarios': len(rows)==8,
        'five_passes': sum(r['classification']['pass'] for r in rows)==5,
        'three_failures': sum(not r['classification']['pass'] for r in rows)==3,
        'radial_fail_present': any('radial_leakage' in r['classification']['failure_modes'] for r in rows),
        'visibility_fail_present': any('visibility' in r['classification']['failure_modes'] for r in rows),
        'basis_fail_present': any('basis_covariance' in r['classification']['failure_modes'] for r in rows),
        'threshold_010': THRESHOLD==0.10,
    }
    result={'bt':1581,'title':'Radial leakage pass/fail simulator','verified':all(checks.values()),'source':'data/bt1577_radial_leakage_bound_from_oam_phase_ops.json','thresholds':{'radial_leakage':THRESHOLD,'visibility_error':0.05},'scenarios':rows,'interpretation':'The simulator turns symbolic leakage envelopes into pass/fail regimes. Good I/Z/S/X/F3 settings pass at or below the leakage and visibility thresholds; radial leakage, visibility mismatch, and basis-covariance failures are separated into distinct kill modes.','honesty_boundary':'Symbolic pass/fail simulator only; numerical thresholds remain protocol placeholders pending lab calibration.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    MD.write_text('# BT1581 Radial Leakage Pass/Fail Simulator\n\nThe simulator turns symbolic radial leakage envelopes into pass/fail regimes. Good I/Z/S/X/F3 settings pass at or below thresholds. Radial leakage, visibility mismatch, and basis-covariance failures are separated as distinct kill modes.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1581: radial leakage pass/fail regimes separate good core gates from radial, visibility, and basis-covariance failures.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1581,'verified':result['verified'],'passes':sum(r['classification']['pass'] for r in rows)}, indent=2))
    if not result['verified']: raise SystemExit(1)

if __name__=='__main__': main()
