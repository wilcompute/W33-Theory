#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1627_observable_implementation_stubs.json'
MD = ROOT / 'analysis' / 'BT1627_observable_implementation_stubs.md'
TEX = ROOT / 'analysis' / 'BT1627_observable_implementation_stubs.tex'

FRAMES = 1600
BINS = 168

def frame_record(frame: int) -> dict:
    source = frame // 40
    target = frame % 40
    rel = (target - source) % 40
    role = 'control' if rel < 13 else 'contextual_fuel'
    bin_id = frame % BINS
    return {
        'source_ray': source,
        'target_ray': target,
        'relative_target': rel,
        'role': role,
        'detector_bin': bin_id,
        'fano_point': bin_id % 7,
        'css_row': bin_id % 72,
        'hesse_residue': (source + 2 * target) % 3,
    }

def fano_entropy_profile(records):
    return Counter(r['detector_bin'] for r in records)

def ordered_transition_matrix(records):
    return Counter((r['source_ray'], r['target_ray']) for r in records)

def protected_zero_syndrome_profile(records):
    return {
        'css_row_counts': Counter(r['css_row'] for r in records),
        'hesse_residue_counts': Counter(r['hesse_residue'] for r in records),
    }

def main() -> None:
    records = [frame_record(i) for i in range(FRAMES)]
    fano = fano_entropy_profile(records)
    trans = ordered_transition_matrix(records)
    syndrome = protected_zero_syndrome_profile(records)
    stubs = [
        {'sector':'gauge','observable':'fano_entropy_profile','implemented':True,'returns':'Counter[detector_bin]','claim_status':'placeholder_computable'},
        {'sector':'CKM','observable':'ordered_transition_matrix','implemented':True,'returns':'Counter[(source_ray,target_ray)]','claim_status':'placeholder_computable'},
        {'sector':'PMNS_neutrino','observable':'protected_zero_syndrome_profile','implemented':True,'returns':'css_row_counts and hesse_residue_counts','claim_status':'placeholder_computable'},
        {'sector':'quark_masses','observable':'witting_spectral_hierarchy_trace','implemented':False,'returns':'none','claim_status':'missing_unit_map'},
        {'sector':'Higgs_strong_CP','observable':'scalar_trace_and_cp_firewall','implemented':False,'returns':'none','claim_status':'blocked_pending_physical_observable'},
    ]
    checks = {
        'five_stub_rows': len(stubs) == 5,
        'three_computable_placeholders': sum(s['implemented'] for s in stubs) == 3,
        'two_missing_or_blocked': sum(not s['implemented'] for s in stubs) == 2,
        'fano_168_bins': len(fano) == 168,
        'transition_1600_pairs': len(trans) == 1600,
        'css_72_rows': len(syndrome['css_row_counts']) == 72,
        'hesse_three_residues': len(syndrome['hesse_residue_counts']) == 3,
        'no_pass_claims': all(s['claim_status'] != 'PASS' for s in stubs),
    }
    result = {
        'bt': 1627,
        'title': 'Observable implementation stubs',
        'verified': all(checks.values()),
        'source_packets': {'decoded_stats':'data/bt1624_minimal_decoded_stream_statistics.json','schema':'data/bt1622_abi_observable_schema_for_sm_sectors.json'},
        'stub_rows': stubs,
        'summary_stats': {
            'fano_bin_count': len(fano),
            'transition_pair_count': len(trans),
            'css_row_count': len(syndrome['css_row_counts']),
            'hesse_residue_counts': {str(k): v for k, v in sorted(syndrome['hesse_residue_counts'].items())},
        },
        'interpretation': 'Three dimensionless decoded-stream observables are now implemented as placeholder functions; two dimensionful/physical sectors remain missing or blocked.',
        'honesty_boundary': 'Implementation stubs only. These functions compute deterministic decoded-stream statistics and do not validate SM parameters.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1627 Observable Implementation Stubs\n\nThree dimensionless decoded-stream observables are implemented as placeholder functions: Fano/bin profile, ordered transition matrix, and protected-zero syndrome profile. Quark-mass and scalar/CP observables remain missing or blocked. No PASS claims are emitted.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1627: dimensionless decoded-stream observable stubs are implemented; dimensionful and CP rows remain missing or blocked.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1627,'verified':result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__': main()
