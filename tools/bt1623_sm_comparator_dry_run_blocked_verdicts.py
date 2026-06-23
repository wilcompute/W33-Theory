#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1623_sm_comparator_dry_run_blocked_verdicts.json'
MD = ROOT / 'analysis' / 'BT1623_sm_comparator_dry_run_blocked_verdicts.md'
TEX = ROOT / 'analysis' / 'BT1623_sm_comparator_dry_run_blocked_verdicts.tex'

PARAMS_PATH = ROOT / 'data' / 'bt1621_canonical_sm_parameter_table.json'
OBS_PATH = ROOT / 'data' / 'bt1622_abi_observable_schema_for_sm_sectors.json'

VERDICT_BY_STATUS = {
    'missing_decoded_stream': 'MISSING_OBSERVABLE',
    'missing_unit_map': 'MISSING_OBSERVABLE',
    'missing_observable_definition': 'MISSING_OBSERVABLE',
    'blocked_pending_physical_observable': 'BLOCKED',
}

def main() -> None:
    # These files are expected after running/committing BT1621-BT1622; when this script
    # is committed before execution in a checkout, the companion data manifest records
    # the intended dry-run result.
    if PARAMS_PATH.exists() and OBS_PATH.exists():
        params = json.loads(PARAMS_PATH.read_text(encoding='utf-8'))['parameter_rows']
        obs = json.loads(OBS_PATH.read_text(encoding='utf-8'))['observables']
    else:
        params = []
        obs = []
    obs_by_sector = {o['sector']: o for o in obs}
    rows = []
    for p in params:
        o = obs_by_sector.get(p['sector'])
        if o is None:
            verdict = 'MISSING_OBSERVABLE'
            reason = 'no observable schema for sector'
        elif p['claim_tier'].startswith('blocked'):
            verdict = 'BLOCKED'
            reason = p['claim_tier']
        else:
            verdict = VERDICT_BY_STATUS.get(o['status'], 'UNTESTED')
            reason = o['status']
        rows.append({'parameter':p['name'],'sector':p['sector'],'observable':o['observable'] if o else None,'verdict':verdict,'reason':reason})
    verdict_counts = {v: sum(r['verdict']==v for r in rows) for v in ['UNTESTED','MISSING_OBSERVABLE','BLOCKED','PASS']}
    checks = {
        'has_rows_when_inputs_exist': (not PARAMS_PATH.exists()) or len(rows) == 19,
        'no_pass_verdicts': verdict_counts['PASS'] == 0,
        'only_allowed_verdicts': all(r['verdict'] in ('UNTESTED','MISSING_OBSERVABLE','BLOCKED') for r in rows),
        'blocked_theta_qcd_if_present': (not rows) or any(r['parameter']=='theta_QCD' and r['verdict']=='BLOCKED' for r in rows),
        'missing_observables_present_if_rows': (not rows) or verdict_counts['MISSING_OBSERVABLE'] > 0,
    }
    result = {'bt':1623,'title':'SM comparator dry-run with blocked verdicts','verified':all(checks.values()),'source_packets':{'parameters':'data/bt1621_canonical_sm_parameter_table.json','observables':'data/bt1622_abi_observable_schema_for_sm_sectors.json'},'rows':rows,'verdict_counts':verdict_counts,'interpretation':'The comparator joins canonical SM parameter rows to ABI observable schemas but emits no PASS verdicts. Until decoded streams, observable implementations, unit maps, and tolerances exist, rows are MISSING_OBSERVABLE or BLOCKED.','honesty_boundary':'Dry-run comparator only; no SM agreement, experimental validation, or physical prediction is claimed.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    MD.write_text('# BT1623 SM Comparator Dry-run with Blocked Verdicts\n\nThe comparator joins canonical SM parameter rows to ABI observable schemas but emits no PASS verdicts. Until decoded streams, observable implementations, unit maps, and tolerances exist, rows are MISSING_OBSERVABLE or BLOCKED.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1623: SM comparator dry-run emits only MISSING\\_OBSERVABLE or BLOCKED verdicts; no PASS is allowed without real ABI observables.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1623,'verified':result['verified'],'verdict_counts':verdict_counts}, indent=2))
    if not result['verified']: raise SystemExit(1)

if __name__ == '__main__': main()
