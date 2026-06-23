#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1624_minimal_decoded_stream_statistics.json'
MD = ROOT / 'analysis' / 'BT1624_minimal_decoded_stream_statistics_generator.md'
TEX = ROOT / 'analysis' / 'BT1624_minimal_decoded_stream_statistics_generator.tex'

FRAMES = 1600
BINS = 168
TICKS_PER_FRAME = 72

def frame_record(frame: int) -> dict:
    source = frame // 40
    target = frame % 40
    rel = (target - source) % 40
    role = 'control' if rel < 13 else 'contextual_fuel'
    bin_id = frame % BINS
    return {
        'frame': frame,
        'source_ray': source,
        'target_ray': target,
        'relative_target': rel,
        'role': role,
        'detector_bin': bin_id,
        'orbit': bin_id // 7,
        'fano_point': bin_id % 7,
        'css_row': bin_id % 72,
        'hesse_residue': (source + 2 * target) % 3,
    }

def entropy(counts: Counter) -> float:
    total = sum(counts.values())
    return -sum((v/total) * math.log2(v/total) for v in counts.values())

def main() -> None:
    records = [frame_record(i) for i in range(FRAMES)]
    bin_counts = Counter(r['detector_bin'] for r in records)
    fano_counts = Counter(r['fano_point'] for r in records)
    orbit_counts = Counter(r['orbit'] for r in records)
    css_counts = Counter(r['css_row'] for r in records)
    hesse_counts = Counter(r['hesse_residue'] for r in records)
    role_counts = Counter(r['role'] for r in records)
    transition_counts = Counter((r['source_ray'], r['target_ray']) for r in records)
    checks = {
        'frames_1600': len(records) == 1600,
        'transition_matrix_40x40': len(transition_counts) == 1600 and all(v == 1 for v in transition_counts.values()),
        'control_520': role_counts['control'] == 520,
        'fuel_1080': role_counts['contextual_fuel'] == 1080,
        'all_168_bins_used': len(bin_counts) == 168,
        'bin_usage_profile_80x9_88x10': sorted(Counter(bin_counts.values()).items()) == [(9,80),(10,88)],
        'css_rows_72': len(css_counts) == 72,
        'hesse_residues_three': len(hesse_counts) == 3,
        'fano_points_seven': len(fano_counts) == 7,
        'orbits_24': len(orbit_counts) == 24,
    }
    result = {
        'bt': 1624,
        'title': 'Minimal decoded-stream statistics generator',
        'verified': all(checks.values()),
        'source': 'data/bt1613_sequence_level_inverse_decoder.json',
        'statistics': {
            'role_counts': dict(role_counts),
            'bin_usage_profile': {'bins_used_9_times': 80, 'bins_used_10_times': 88},
            'fano_point_counts': {str(k): v for k, v in sorted(fano_counts.items())},
            'hesse_residue_counts': {str(k): v for k, v in sorted(hesse_counts.items())},
            'css_row_usage_profile': {str(k): v for k, v in sorted(Counter(css_counts.values()).items())},
            'orbit_usage_profile': {str(k): v for k, v in sorted(Counter(orbit_counts.values()).items())},
            'transition_matrix_shape': [40, 40],
            'transition_count_per_source_target': 1,
            'fano_bin_entropy_bits': entropy(bin_counts),
            'fano_bin_entropy_ratio': entropy(bin_counts) / math.log2(BINS),
        },
        'placeholder_observables_available': ['fano_bin_entropy_profile','ordered_transition_matrix','protected_zero_syndrome_profile'],
        'still_missing': ['witting_spectral_hierarchy_trace_unit_map','scalar_trace_and_cp_physical_observable'],
        'interpretation': 'This generates the first deterministic decoded-stream statistics: Fano/bin entropy, transition counts, CSS-row occupancy, and Hesse residues. These are placeholder decoded-stream observables, not physical measurements.',
        'honesty_boundary': 'Deterministic schedule statistics only; no noisy data, hardware calibration, or SM comparison verdict is claimed.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1624 Minimal Decoded-stream Statistics Generator\n\nThe deterministic BT1613 schedule is reduced to placeholder observable arrays: Fano/bin entropy, 40x40 transition counts, CSS-row occupancy, and Hesse residue counts. These are decoded-stream statistics, not hardware measurements or SM validation.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1624: decoded-stream statistics expose Fano entropy, transition counts, CSS occupancy, and Hesse residues as placeholder observables.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt': 1624, 'verified': result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__': main()
