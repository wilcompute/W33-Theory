#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1610_bt160x_namespace_collision_merger.json'
MD = ROOT / 'analysis' / 'BT1610_bt160x_namespace_collision_merger.md'
TEX = ROOT / 'analysis' / 'BT1610_bt160x_namespace_collision_merger.tex'

ROWS = [
    {'id':'BT1604','parallel_meaning':'Physical Calibration ABI','local_or_roadmap_meaning':'Roadmap / SM bridge proposal','canonical_alias':'BT1604_calibration_abi + BT1604R_roadmap'},
    {'id':'BT1605','parallel_meaning':'Detector-Bin Decoder','local_or_roadmap_meaning':'Witting-Fano Holographic Compression Audit','canonical_alias':'BT1605D_decoder + BT1605H_holographic_audit'},
    {'id':'BT1606','parallel_meaning':'Fault-Path Theorem','local_or_roadmap_meaning':'Mass-gap/Fault Bridge Firewall','canonical_alias':'BT1606F_fault_path + BT1606M_mass_gap_firewall'},
    {'id':'BT1607','parallel_meaning':'Witting entropy budget placeholder','local_or_roadmap_meaning':'Full Architecture Closure Map','canonical_alias':'BT1607A_architecture_map + BT1607E_entropy_placeholder'},
]

def main() -> None:
    checks = {
        'four_collision_rows': len(ROWS) == 4,
        'bt1605_collision_recorded': any(r['id'] == 'BT1605' for r in ROWS),
        'detector_and_holographic_both_preserved': any('decoder' in r['canonical_alias'] and 'holographic' in r['canonical_alias'] for r in ROWS),
        'mass_gap_firewall_not_overwritten': any('mass_gap_firewall' in r['canonical_alias'] for r in ROWS),
        'all_have_alias': all(r['canonical_alias'] for r in ROWS),
    }
    result = {
        'bt': 1610,
        'title': 'BT160x namespace collision merger',
        'verified': all(checks.values()),
        'collision_rows': ROWS,
        'interpretation': 'The last-two-day commit wave produced overlapping BT1604-BT1607 labels. The merger preserves all useful objects by aliasing roles rather than deleting or pretending the collision does not exist.',
        'honesty_boundary': 'This does not rewrite old commit messages or rename files; it provides a canonical crosswalk for future analysis.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1610 BT160x Namespace Collision Merger\n\nThe last-two-day commit wave produced overlapping BT1604-BT1607 labels. This ledger preserves all useful objects by aliasing roles: calibration ABI vs roadmap, detector decoder vs holographic audit, fault-path theorem vs mass-gap firewall, and architecture map vs entropy placeholder.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1610: BT160x namespace collisions are resolved by role aliases rather than deleting useful parallel artifacts.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1610,'verified':result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
