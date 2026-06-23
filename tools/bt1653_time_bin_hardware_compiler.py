#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1653_time_bin_hardware_compiler.json'
MD = ROOT / 'analysis' / 'BT1653_time_bin_hardware_compiler.md'
TEX = ROOT / 'analysis' / 'BT1653_time_bin_hardware_compiler.tex'

TOTAL = 2048
ACTIVE = 1600
GUARD = 448
TAU = 'tau'
DELAY_STAGES = [2**i for i in range(11)]

COMPONENTS = [
    {'component':'single_photon_source','role':'one photon per compiled shot','loss_placeholder':'eta_source'},
    {'component':'11_bit_time_bin_encoder','role':'address 0..2047 using binary delay/switch tree','loss_placeholder':'eta_encoder'},
    {'component':'binary_delay_tree','role':'delays 1,2,4,...,1024 tau','loss_placeholder':'eta_delay_per_stage'},
    {'component':'active_witting_analyzer','role':'time bins 0..1599 decode Witting frame and detector bin','loss_placeholder':'eta_active_analyzer'},
    {'component':'guard_page_router','role':'time bins 1600..2047 route by Fano page and guard slot','loss_placeholder':'eta_guard_router'},
    {'component':'dark_reference_gate','role':'guard slots 0..23 per Fano point','loss_placeholder':'dark_rate_Hz'},
    {'component':'loss_probe_gate','role':'guard slots 24..47 per Fano point','loss_placeholder':'eta_loss_probe'},
    {'component':'parity_overflow_analyzer','role':'guard slots 48..63 per Fano point','loss_placeholder':'eta_css_jitter'},
    {'component':'168_bin_detector_bank','role':'active plus dark/loss detector-bin coverage','loss_placeholder':'eta_detector, dark_count_rate'},
    {'component':'css_retry_controller','role':'consume parity-overflow syndromes and issue retry/abort','loss_placeholder':'retry_budget'},
]

def compile_timebin(tb: int) -> dict:
    word = format(tb, '011b')
    if tb < ACTIVE:
        return {
            'time_bin': tb,
            'word11': word,
            'region': 'ACTIVE',
            'route': 'active_witting_analyzer',
            'detector_bin': tb % 168,
            'trigger': 'active_decode_tick',
            'calibration_action': 'none',
        }
    off = tb - ACTIVE
    fano_point = off // 64
    slot = off % 64
    if slot < 24:
        role = 'DARK_REFERENCE'; route = 'dark_reference_gate'; action = 'measure_dark_baseline'
    elif slot < 48:
        role = 'LOSS_PROBE'; route = 'loss_probe_gate'; action = 'measure_loss_response'
    else:
        role = 'PARITY_OVERFLOW'; route = 'parity_overflow_analyzer'; action = 'measure_css_jitter_or_retry'
    detector_bin = fano_point * 24 + slot if slot < 24 else (fano_point * 24 + (slot - 24) if slot < 48 else None)
    return {
        'time_bin': tb,
        'word11': word,
        'region': 'GUARD',
        'fano_point': fano_point,
        'guard_slot': slot,
        'guard_role': role,
        'route': route,
        'detector_bin': detector_bin,
        'trigger': f'guard_page_{fano_point}_slot_{slot}',
        'calibration_action': action,
    }

def main() -> None:
    sample = [compile_timebin(i) for i in range(8)] + [compile_timebin(i) for i in range(1596,1604)] + [compile_timebin(i) for i in range(2040,2048)]
    counts = {'ACTIVE':0,'DARK_REFERENCE':0,'LOSS_PROBE':0,'PARITY_OVERFLOW':0}
    detector_dark = set(); detector_loss = set(); parity = 0
    for tb in range(TOTAL):
        r = compile_timebin(tb)
        if r['region'] == 'ACTIVE':
            counts['ACTIVE'] += 1
        else:
            counts[r['guard_role']] += 1
            if r['guard_role'] == 'DARK_REFERENCE': detector_dark.add(r['detector_bin'])
            if r['guard_role'] == 'LOSS_PROBE': detector_loss.add(r['detector_bin'])
            if r['guard_role'] == 'PARITY_OVERFLOW': parity += 1
    checks = {
        'total_2048': TOTAL == 2048,
        'active_1600': counts['ACTIVE'] == 1600,
        'guard_448': counts['DARK_REFERENCE'] + counts['LOSS_PROBE'] + counts['PARITY_OVERFLOW'] == 448,
        'delay_stages_11': DELAY_STAGES == [1,2,4,8,16,32,64,128,256,512,1024],
        'components_10': len(COMPONENTS) == 10,
        'dark_168_and_covers_bins': counts['DARK_REFERENCE'] == 168 and len(detector_dark) == 168,
        'loss_168_and_covers_bins': counts['LOSS_PROBE'] == 168 and len(detector_loss) == 168,
        'parity_112': parity == 112,
        'all_components_have_loss_placeholders': all(c['loss_placeholder'] for c in COMPONENTS),
    }
    result = {
        'bt': 1653,
        'title': 'Time-bin hardware compiler',
        'verified': all(checks.values()),
        'source_packets': {'envelope':'data/bt1649_time_bin_qudit_envelope.json','guard_closure':'data/bt1650_guard_page_calibration_closure.json','shot_sim':'data/bt1651_guard_shell_shot_simulator.json'},
        'compiler_target': 'single-photon 11-bit time-bin qudit envelope',
        'delay_stages_tau': DELAY_STAGES,
        'component_rows': COMPONENTS,
        'compiled_region_counts': counts,
        'calibration_triggers': {
            'active': 'time bins 0..1599 active_decode_tick',
            'dark': 'guard slots 0..23 per Fano page measure_dark_baseline',
            'loss': 'guard slots 24..47 per Fano page measure_loss_response',
            'parity': 'guard slots 48..63 per Fano page measure_css_jitter_or_retry',
        },
        'sample_compiled_rows': sample,
        'interpretation': 'The 2048-bin envelope is lowered into source, 11-bit encoder, binary delay tree, active analyzer, guard router, dark/loss/parity gates, detector bank, and CSS retry controller. Every component carries explicit loss/calibration placeholders.',
        'honesty_boundary': 'Compiler schema only; no optical layout dimensions, measured loss, detector efficiency, or real timing jitter is claimed.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1653 Time-bin Hardware Compiler\n\nThe 2048-bin envelope is lowered into a component schema: source, 11-bit time-bin encoder, binary delay tree, active Witting analyzer, guard router, dark/loss/parity gates, detector bank, and CSS retry controller. All components carry loss placeholders and calibration trigger timing. This is a compiler schema, not a measured hardware design.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1653: the 2048-bin envelope is compiled into switch/delay/analyzer/detector components with loss placeholders and calibration triggers.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1653,'verified':result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__': main()
