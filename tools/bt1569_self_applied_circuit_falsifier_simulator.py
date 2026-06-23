#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1569_self_applied_circuit_falsifier_simulator.json'
MD = ROOT / 'analysis' / 'BT1569_self_applied_circuit_falsifier_simulator.md'
TEX = ROOT / 'analysis' / 'BT1569_self_applied_circuit_falsifier_simulator.tex'

IDEAL = {'I':1.0, 'X':0.0, 'Z':0.0, 'F3':1/3}
SCENARIOS = [
    {'name':'passive_label_only','pred':{'I':1.0,'X':1.0,'Z':1.0,'F3':1.0},'oam_leakage':0.0,'radial_leakage':0.0,'basis_covariant':True},
    {'name':'internal_operator_good','pred':IDEAL,'oam_leakage':0.01,'radial_leakage':0.02,'basis_covariant':True},
    {'name':'operator_independent_bad','pred':{'I':0.7,'X':0.7,'Z':0.7,'F3':0.7},'oam_leakage':0.02,'radial_leakage':0.02,'basis_covariant':True},
    {'name':'leaky_spiral_bad','pred':{'I':0.8,'X':0.1,'Z':0.2,'F3':0.4},'oam_leakage':0.25,'radial_leakage':0.30,'basis_covariant':True},
    {'name':'label_dependent_bad','pred':IDEAL,'oam_leakage':0.01,'radial_leakage':0.02,'basis_covariant':False},
]

TOL = {'visibility':0.05,'leakage':0.10}

def max_visibility_error(pred):
    return max(abs(pred[k]-IDEAL[k]) for k in IDEAL)

def classify(s):
    visibility_ok = max_visibility_error(s['pred']) <= TOL['visibility']
    leakage_ok = s['oam_leakage'] <= TOL['leakage'] and s['radial_leakage'] <= TOL['leakage']
    covariance_ok = bool(s['basis_covariant'])
    operator_active = s['pred']['X'] != s['pred']['I'] or s['pred']['Z'] != s['pred']['I'] or s['pred']['F3'] != s['pred']['I']
    passed = visibility_ok and leakage_ok and covariance_ok and operator_active
    return {
        'visibility_ok': visibility_ok,
        'leakage_ok': leakage_ok,
        'basis_covariance_ok': covariance_ok,
        'operator_active': operator_active,
        'pass': passed,
        'kill_reason': 'none' if passed else ';'.join(k for k,v in {
            'visibility_mismatch': not visibility_ok,
            'mode_leakage': not leakage_ok,
            'basis_dependence': not covariance_ok,
            'passive_label_behavior': not operator_active,
        }.items() if v),
    }

rows = []
for s in SCENARIOS:
    rows.append({**s, 'max_visibility_error': max_visibility_error(s['pred']), 'classification': classify(s)})

CHECKS = {
    'five_scenarios': len(rows) == 5,
    'exactly_one_pass': sum(1 for r in rows if r['classification']['pass']) == 1,
    'passive_label_fails': not rows[0]['classification']['pass'],
    'internal_good_passes': rows[1]['classification']['pass'],
    'leaky_bad_fails': not rows[3]['classification']['pass'],
    'label_bad_fails': not rows[4]['classification']['pass'],
}

result = {
    'bt':1569,
    'title':'Self-applied circuit falsifier simulator',
    'verified': all(CHECKS.values()),
    'source_packets': {'bt1566':'tools/bt1566_oam_operator_witness.py','bt1568':'tools/bt1568_lens_prism_oam_dictionary.py'},
    'ideal_trace_choi': IDEAL,
    'tolerances': TOL,
    'scenarios': rows,
    'interpretation':'The simulator separates internal-operator behavior from passive OAM labeling. Only the internal_operator_good scenario passes: it matches the trace-Choi gate pattern, keeps OAM/radial leakage below threshold, is basis covariant, and changes with operator setting.',
    'honesty_boundary':'This is a symbolic falsifier simulator with placeholder tolerances, not experimental data.',
    'checks': CHECKS,
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
MD.write_text('# BT1569 Self-applied Circuit Falsifier Simulator\n\nThe simulator compares passive labels, internal-operator behavior, operator-independent behavior, leakage failure, and label-dependence failure. Only the internal-operator scenario passes the symbolic criteria: trace-Choi pattern, low leakage, basis covariance, and operator activation. Tolerances are placeholders, not lab data.\n', encoding='utf-8')
TEX.write_text('\\begin{center}\\small\nBT1569: symbolic falsifier regimes separate internal-operator behavior from passive OAM labeling and leakage/label-dependence failures.\n\\end{center}\n', encoding='utf-8')
print(json.dumps({'bt':1569,'verified':result['verified']}, indent=2))
if not result['verified']:
    raise SystemExit(1)
