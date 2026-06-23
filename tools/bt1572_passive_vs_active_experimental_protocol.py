#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1572_passive_vs_active_experimental_protocol.json'
MD = ROOT / 'analysis' / 'BT1572_passive_vs_active_experimental_protocol.md'
TEX = ROOT / 'analysis' / 'BT1572_passive_vs_active_experimental_protocol.tex'

PREPARATION = [
    {'step':1,'setting':'single photon source','purpose':'inject one photon carrier'},
    {'step':2,'setting':'centered OAM basis ell=-1,0,+1 with labels 2,0,1','purpose':'prepare state leg'},
    {'step':3,'setting':'three axial time bins 0,tau,2tau','purpose':'prepare Choi past/future support'},
    {'step':4,'setting':'operator leg off/on switch','purpose':'separate passive-label control from active internal operator setting'},
]
OPERATOR_SETTINGS = [
    {'setting':'off','expected':'passive label sorting only','kill_if':'off setting reproduces all active gate signatures'},
    {'setting':'I','expected':'V=1','kill_if':'identity visibility misses tolerance'},
    {'setting':'X','expected':'V=0','kill_if':'shift visibility nonzero beyond tolerance'},
    {'setting':'Z','expected':'V=0','kill_if':'phase visibility nonzero beyond tolerance'},
    {'setting':'F3','expected':'V=1/3','kill_if':'Fourier visibility misses tolerance'},
    {'setting':'S','expected':'quadratic phase signature [1,0,1]','kill_if':'lens phase does not match calibrated S signature'},
]
THRESHOLDS = {'visibility_abs_error':0.05,'oam_leakage':0.10,'radial_leakage':0.10,'basis_covariance':'must pass after mod-3 decoding'}
PROTOCOL_BLOCKS = [
    {'block':'passive_control','actions':['prepare OAM labels','operator leg off','measure trace readout'],'pass_condition':'no active gate pattern'},
    {'block':'active_operator','actions':['turn on I,X,Z,F3,S settings','measure trace-Choi readouts'],'pass_condition':'matches expected gate signatures'},
    {'block':'leakage','actions':['measure outside ell=-1,0,+1','measure radial shell mixing'],'pass_condition':'below leakage thresholds'},
    {'block':'basis_covariance','actions':['relabel centered basis by mod-3 decoding','repeat core readouts'],'pass_condition':'predictions are unchanged after decoding'},
    {'block':'external_reference','actions':['compare to ordinary external optic gate signatures'],'pass_condition':'internal and external signatures agree within tolerance'},
]

def main() -> None:
    checks = {
        'four_preparation_steps': len(PREPARATION) == 4,
        'six_operator_settings': len(OPERATOR_SETTINGS) == 6,
        'five_protocol_blocks': len(PROTOCOL_BLOCKS) == 5,
        'all_operator_rows_have_kill': all('kill_if' in row for row in OPERATOR_SETTINGS),
        'thresholds_present': set(THRESHOLDS) == {'visibility_abs_error','oam_leakage','radial_leakage','basis_covariance'},
        'passive_and_active_blocks_present': {b['block'] for b in PROTOCOL_BLOCKS} >= {'passive_control','active_operator'},
    }
    result = {
        'bt': 1572,
        'title': 'Passive-vs-active experimental protocol',
        'verified': all(checks.values()),
        'source_packets': {'bt1569':'data/bt1569_self_applied_circuit_falsifier_simulator.json','bt1571':'data/bt1571_lens_phase_calibration_model.json'},
        'preparation': PREPARATION,
        'operator_settings': OPERATOR_SETTINGS,
        'thresholds': THRESHOLDS,
        'protocol_blocks': PROTOCOL_BLOCKS,
        'interpretation': 'The protocol turns the passive-vs-active distinction into lab steps. Passive OAM labeling must fail to reproduce active gate signatures, while operator-leg activation must reproduce I, X, Z, F3, and calibrated S readouts with leakage below thresholds and basis covariance after decoding.',
        'honesty_boundary': 'Thresholds are engineering placeholders pending calibration. This is a protocol design, not experimental evidence.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1572 Passive-vs-active Experimental Protocol\n\nThe protocol separates passive OAM labels from active internal operators. It uses centered OAM preparation, axial time-bin support, operator off/on controls, I/X/Z/F3/S settings, leakage checks, basis covariance, and external-reference comparison. Thresholds are placeholders pending lab calibration.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1572: passive-vs-active protocol uses operator-off controls, $I,X,Z,F_3,S$ settings, leakage checks, basis covariance, and external references.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1572,'verified':result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
