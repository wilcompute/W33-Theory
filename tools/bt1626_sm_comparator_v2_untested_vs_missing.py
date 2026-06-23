#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1626_sm_comparator_v2_untested_vs_missing.json'
MD = ROOT / 'analysis' / 'BT1626_sm_comparator_v2_untested_vs_missing.md'
TEX = ROOT / 'analysis' / 'BT1626_sm_comparator_v2_untested_vs_missing.tex'

PARAMS = [
    ('gauge','alpha_inv_tree'),('gauge','sin2_theta_W'),('gauge','alpha_s'),
    ('quark_masses','m_t'),('quark_masses','m_c'),('quark_masses','m_u'),('quark_masses','m_b'),
    ('CKM','V_us'),('CKM','A_wolf'),('CKM','V_cb'),('CKM','V_ub'),('CKM','delta_CKM'),
    ('Higgs_strong_CP','lambda_H'),('Higgs_strong_CP','m_H'),('Higgs_strong_CP','theta_QCD'),
    ('PMNS_neutrino','dm32_dm21_ratio'),('PMNS_neutrino','sin2_theta12_PMNS'),('PMNS_neutrino','sin2_theta23_PMNS'),('PMNS_neutrino','sin2_theta13_PMNS'),
]
AVAILABLE = {
    'gauge': 'fano_bin_entropy_profile',
    'CKM': 'ordered_transition_matrix',
    'PMNS_neutrino': 'protected_zero_syndrome_profile',
}
MISSING = {
    'quark_masses': 'witting_spectral_hierarchy_trace_unit_map',
    'Higgs_strong_CP': 'scalar_trace_proxy',
}

def verdict_for(sector: str, name: str) -> tuple[str, str, str | None]:
    if name == 'theta_QCD':
        return 'BLOCKED', 'strong-CP row requires physical CP observable', MISSING['Higgs_strong_CP']
    if sector in AVAILABLE:
        return 'UNTESTED', 'placeholder decoded observable exists but no comparator/tolerance exists', AVAILABLE[sector]
    if sector in MISSING:
        return 'MISSING_OBSERVABLE', 'unit map or physical observable missing', MISSING[sector]
    return 'MISSING_OBSERVABLE', 'no schema row', None

def main() -> None:
    rows=[]
    for sector, name in PARAMS:
        verdict, reason, obs = verdict_for(sector, name)
        rows.append({'sector':sector,'parameter':name,'observable':obs,'verdict':verdict,'reason':reason})
    counts = {v: sum(r['verdict']==v for r in rows) for v in ['UNTESTED','MISSING_OBSERVABLE','BLOCKED','PASS']}
    checks = {
        'nineteen_rows': len(rows) == 19,
        'zero_pass': counts['PASS'] == 0,
        'untested_12': counts['UNTESTED'] == 12,
        'missing_6': counts['MISSING_OBSERVABLE'] == 6,
        'blocked_1': counts['BLOCKED'] == 1,
        'theta_qcd_blocked': any(r['parameter']=='theta_QCD' and r['verdict']=='BLOCKED' for r in rows),
        'only_allowed_verdicts': all(r['verdict'] in ('UNTESTED','MISSING_OBSERVABLE','BLOCKED') for r in rows),
    }
    result={'bt':1626,'title':'SM comparator v2: UNTESTED vs MISSING','verified':all(checks.values()),'source_packets':{'parameters':'data/bt1621_canonical_sm_parameter_table.json','observables':'data/bt1622_abi_observable_schema_for_sm_sectors.json','decoded_stats':'data/bt1624_minimal_decoded_stream_statistics.json','unit_map':'data/bt1625_unit_map_ledger.json'},'rows':rows,'verdict_counts':counts,'interpretation':'Rows with placeholder decoded-stream observables become UNTESTED. Rows lacking unit maps or physical observables remain MISSING_OBSERVABLE. Strong-CP remains BLOCKED. No PASS verdict is emitted.','honesty_boundary':'Comparator v2 still performs no numerical SM validation and claims no agreement.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    MD.write_text('# BT1626 SM Comparator v2: UNTESTED vs MISSING\n\nRows with placeholder decoded-stream observables become UNTESTED. Rows lacking unit maps or physical observables remain MISSING_OBSERVABLE. Strong-CP remains BLOCKED. No PASS verdict is emitted.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1626: comparator v2 separates UNTESTED placeholder-observable rows from MISSING rows and emits zero PASS verdicts.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1626,'verified':result['verified'],'counts':counts}, indent=2))
    if not result['verified']: raise SystemExit(1)

if __name__ == '__main__': main()
