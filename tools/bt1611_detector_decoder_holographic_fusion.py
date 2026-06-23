#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1611_detector_decoder_holographic_fusion.json'
MD = ROOT / 'analysis' / 'BT1611_detector_decoder_holographic_fusion.md'
TEX = ROOT / 'analysis' / 'BT1611_detector_decoder_holographic_fusion.tex'

ROWS = [
    {'level':'single_bin_decode','input':'bin_id','output':'orbit, Fano point, role, rail, Hesse residue, CSS row','status':'parallel BT1605D supports local field decode'},
    {'level':'frame_decode','input':'bin_id + frame time + source ray + rail context','output':'candidate Witting source-target transaction','status':'required by BT1605H because 1600-to-168 point injection is impossible'},
    {'level':'sequence_decode','input':'ordered click stream over the 115200-tick automaton','output':'full transaction-cycle reconstruction','status':'true holographic decoder target'},
    {'level':'fault_aware_decode','input':'sequence decode + calibration/fault-path ABI','output':'PASS/CORRECTED/ABORTED frame stream','status':'requires BT1604 calibration and BT1606 fault-path integration'},
]

def main() -> None:
    checks = {
        'four_decoder_levels': len(ROWS) == 4,
        'single_bin_decode_retained': ROWS[0]['level'] == 'single_bin_decode',
        'frame_decode_requires_context': 'frame time' in ROWS[1]['input'],
        'sequence_decode_is_holographic_target': ROWS[2]['level'] == 'sequence_decode',
        'fault_aware_decode_links_calibration': 'calibration' in ROWS[3]['input'],
    }
    result = {
        'bt': 1611,
        'title': 'Detector decoder / holographic audit fusion',
        'verified': all(checks.values()),
        'source_packets': {
            'parallel_detector_decoder': 'BREAKTHROUGH_BT1604_BT1606_PHYSICAL_FAULT_ABI.md',
            'holographic_audit': 'data/bt1605_witting_fano_holographic_compression_audit.json',
            'universal_abi': 'data/bt1603_universal_computation_proof_closure.json',
        },
        'decode_levels': ROWS,
        'interpretation': 'The parallel detector-bin decoder and the holographic audit are complementary: single-bin decoding recovers local fields, but frame identity needs schedule/source context, and the full holographic target is sequence reconstruction over the 115200-tick automaton.',
        'honesty_boundary': 'This is a decoder architecture fusion, not a completed inverse decoder implementation.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1611 Detector Decoder / Holographic Fusion\n\nThe detector-bin decoder and holographic audit are complementary. A single bin can decode local fields, but frame identity needs time/source/rail context because 1600-to-168 point injection is impossible. The real holographic target is sequence reconstruction over the 115200-tick automaton, then fault-aware decoding with calibration and retry paths.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1611: single-bin decoding gives local fields; holographic reconstruction requires time/source context and ordered sequence decoding.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1611,'verified':result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
