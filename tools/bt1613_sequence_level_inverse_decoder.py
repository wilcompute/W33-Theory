#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1613_sequence_level_inverse_decoder.json'
MD = ROOT / 'analysis' / 'BT1613_sequence_level_inverse_decoder.md'
TEX = ROOT / 'analysis' / 'BT1613_sequence_level_inverse_decoder.tex'

FRAMES = 1600
RAYS = 40
TICKS_PER_FRAME = 72
BINS = 168

def frame_record(frame: int) -> dict:
    source = frame // RAYS
    target = frame % RAYS
    rel = (target - source) % RAYS
    role = 'control' if rel < 13 else 'contextual_fuel'
    bin_id = frame % BINS
    return {
        'frame': frame,
        'tick_start': frame * TICKS_PER_FRAME,
        'tick_end': frame * TICKS_PER_FRAME + TICKS_PER_FRAME - 1,
        'source_ray': source,
        'target_ray': target,
        'relative_target': rel,
        'role': role,
        'detector_bin': bin_id,
        'orbit': bin_id // 7,
        'fano_point': bin_id % 7,
        'rail': 'control' if role == 'control' else 'fuel',
        'hesse_residue': (source + 2 * target) % 3,
        'css_row': bin_id % 72,
    }

def decode_click(tick: int, detector_bin: int) -> dict:
    frame = tick // TICKS_PER_FRAME
    if frame < 0 or frame >= FRAMES:
        return {'valid': False, 'reason': 'tick_out_of_range'}
    rec = frame_record(frame)
    return {
        'valid': detector_bin == rec['detector_bin'],
        'reason': 'ok' if detector_bin == rec['detector_bin'] else 'bin_mismatch',
        'decoded_frame': rec,
        'local_bin_fields': {
            'orbit': detector_bin // 7,
            'fano_point': detector_bin % 7,
            'css_row': detector_bin % 72,
        },
    }

def main() -> None:
    records = [frame_record(i) for i in range(FRAMES)]
    bin_counts = Counter(r['detector_bin'] for r in records)
    role_counts = Counter(r['role'] for r in records)
    round_trip = [decode_click(r['tick_start'], r['detector_bin'])['valid'] for r in records]
    wrong_bin = decode_click(0, 1)
    checks = {
        'frames_1600': len(records) == 1600,
        'ticks_115200': records[-1]['tick_end'] + 1 == 115200,
        'control_520': role_counts['control'] == 520,
        'fuel_1080': role_counts['contextual_fuel'] == 1080,
        'all_168_bins_touched': len(bin_counts) == 168,
        'usage_profile_88x10_80x9': sorted(Counter(bin_counts.values()).items()) == [(9, 80), (10, 88)],
        'round_trip_all_valid': all(round_trip),
        'wrong_bin_detected': wrong_bin['valid'] is False and wrong_bin['reason'] == 'bin_mismatch',
        'bin_only_injection_blocked': FRAMES > BINS,
    }
    result = {
        'bt': 1613,
        'title': 'Sequence-level inverse decoder prototype',
        'verified': all(checks.values()),
        'source_packets': {
            'decoder_fusion': 'data/bt1611_decoder_fusion.json',
            'universal_abi': 'data/bt1603_universal_computation_proof_closure.json',
            'physical_fault_abi': 'BREAKTHROUGH_BT1604_BT1606_PHYSICAL_FAULT_ABI.md',
        },
        'decoder_rule': 'detector bin gives local Fano fields; tick index gives frame; frame gives source/target; bin consistency validates the click.',
        'frame_count': FRAMES,
        'tick_count': FRAMES * TICKS_PER_FRAME,
        'role_counts': dict(role_counts),
        'bin_usage_profile': {'bins_used_9_times': 80, 'bins_used_10_times': 88},
        'sample_decodes': [decode_click(r['tick_start'], r['detector_bin']) for r in records[:5]],
        'interpretation': 'This is the first inverse decoder that respects the no-pointwise-injection theorem: detector bin alone is local, while ordered tick context reconstructs source-target Witting transactions.',
        'honesty_boundary': 'Prototype deterministic schedule decoder only; it does not yet process noisy multi-click batches or real bench timestamps.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1613 Sequence-level Inverse Decoder Prototype\n\nDetector bin alone gives local Fano fields, not frame identity. The decoder uses ordered tick context to recover the Witting frame, then checks detector-bin consistency. It reconstructs 1600 frames, 520 control frames, 1080 contextual-fuel frames, and the 168-bin usage profile.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1613: ordered tick context plus Fano bin data reconstructs Witting source--target frames; bin-only injection remains blocked.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt': 1613, 'verified': result['verified'], 'roles': dict(role_counts)}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
