#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1566_oam_operator_witness.json'
MD = ROOT / 'analysis' / 'BT1566_oam_operator_witness.md'
TEX = ROOT / 'analysis' / 'BT1566_oam_operator_witness.tex'

WITNESSES = [
    {'witness':'state_label_only_control','test':'prepare OAM labels but disable internal operator encoding','expected':'no trace-Choi gate pattern beyond passive mode sorting','kills_if':'passive labels alone reproduce all gate witnesses'},
    {'witness':'operator_leg_activation','test':'turn on encoded mode action for X/Z/F3/S','expected':'trace-Choi predictions switch with encoded action','kills_if':'output is independent of operator-leg setting'},
    {'witness':'basis_covariance','test':'change OAM qutrit basis labeling and repeat core witnesses','expected':'mod-3 relabeling preserves qutrit predictions after decoding','kills_if':'predictions depend on arbitrary label convention'},
    {'witness':'self_vs_external_control','test':'compare internal operator encoding with ordinary external optic action','expected':'same trace-Choi signatures within calibrated tolerance','kills_if':'internal encoding cannot reproduce external gate signature'},
]

CHECKS = {
    'four_witnesses': len(WITNESSES) == 4,
    'each_has_test_expected_kill': all(all(k in w for k in ('test','expected','kills_if')) for w in WITNESSES),
    'operator_activation_present': any(w['witness'] == 'operator_leg_activation' for w in WITNESSES),
    'state_label_control_present': any(w['witness'] == 'state_label_only_control' for w in WITNESSES),
    'external_control_comparison_present': any(w['witness'] == 'self_vs_external_control' for w in WITNESSES),
}

result = {
    'bt': 1566,
    'title': 'OAM operator witness',
    'verified': all(CHECKS.values()),
    'source_packets': {'bt1563':'data/bt1563_self_entangled_qutrit_oam_lab_witness.json','bt1565':'data/bt1565_self_applied_photonic_circuit_model.json'},
    'witnesses': WITNESSES,
    'interpretation': 'The witness distinguishes OAM as an active internal operator leg from OAM as a passive spatial label. The key falsifier is whether changing the encoded operator setting changes the trace-Choi gate signature while passive labels alone do not.',
    'honesty_boundary': 'This is a witness design, not experimental evidence. Numerical tolerances and optical implementation details remain lab-calibration tasks.',
    'checks': CHECKS,
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
MD.write_text('# BT1566 OAM Operator Witness\n\nThe witness distinguishes OAM as an active internal operator leg from OAM as a passive spatial label. It uses state-label-only control, operator-leg activation, basis covariance, and self-vs-external control comparisons. The key kill condition is whether encoded operator settings fail to change the trace-Choi gate signature.\n', encoding='utf-8')
TEX.write_text('\\begin{center}\\small\nBT1566: OAM must behave as an active operator leg, not merely a passive spatial label; trace-Choi signatures provide the falsifier.\n\\end{center}\n', encoding='utf-8')
print(json.dumps({'bt':1566,'verified':result['verified']}, indent=2))
if not result['verified']:
    raise SystemExit(1)
