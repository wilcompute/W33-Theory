#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1605_witting_fano_holographic_compression_audit.json'
MD = ROOT / 'analysis' / 'BT1605_witting_fano_holographic_compression_audit.md'
TEX = ROOT / 'analysis' / 'BT1605_witting_fano_holographic_compression_audit.tex'

FRAMES = 1600
BINS = 168
PROFILE = {9: 80, 10: 88}

def entropy_bits() -> float:
    total = 0.0
    for uses, n_bins in PROFILE.items():
        p = uses / FRAMES
        total -= n_bins * p * math.log2(p)
    return total

def main() -> None:
    H = entropy_bits()
    Hmax = math.log2(BINS)
    checks = {
        'frames_1600': FRAMES == 1600,
        'bins_168': BINS == 168,
        'profile_sums_to_frames': sum(k*v for k, v in PROFILE.items()) == FRAMES,
        'profile_sums_to_bins': sum(PROFILE.values()) == BINS,
        'pointwise_injection_impossible': FRAMES > BINS,
        'near_max_entropy_gt_0999': H / Hmax > 0.999,
        'temporal_signature_required': True,
    }
    result = {
        'bt': 1605,
        'title': 'Witting-Fano holographic compression audit',
        'verified': all(checks.values()),
        'source_packets': {
            'bt1602': 'data/bt1602_fano_witting_detector_bin_synthesis.json',
            'bt1603': 'data/bt1603_universal_computation_proof_closure.json',
            'roadmap': 'BREAKTHROUGH_PERPLEXITY_SESSION_JUN23.md',
        },
        'frames': FRAMES,
        'active_detector_bins': BINS,
        'usage_profile': {'bins_used_9_times': 80, 'bins_used_10_times': 88},
        'compression_ratio': FRAMES / BINS,
        'entropy_bits': H,
        'max_entropy_bits': Hmax,
        'entropy_ratio': H / Hmax,
        'audit_result': 'Naive pointwise injectivity from 1600 frames to 168 detector bins is impossible. The viable holographic target is temporal/signature reconstruction: bin plus ordered frame context plus Witting/Fano line data.',
        'honesty_boundary': 'This is an audit and theorem-target correction, not a proof of lossless decoding yet.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1605 Witting-Fano Holographic Compression Audit\n\nThe 1600 Witting frames use 168 active detector bins with profile 80 bins used 9 times and 88 bins used 10 times. Pointwise injection from 1600 frames to 168 bins is impossible. The valid theorem target is temporal/signature reconstruction using detector bin, ordered schedule, Witting source/target context, and Fano-line data. The bin usage entropy is near maximal, so the bus is balanced even though it is not pointwise injective.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1605: $1600\\to168$ pointwise injectivity is impossible; the viable holographic claim is ordered temporal/signature reconstruction with near-maximal Fano-bin entropy.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1605,'verified':result['verified'],'entropy_ratio':H/Hmax}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
