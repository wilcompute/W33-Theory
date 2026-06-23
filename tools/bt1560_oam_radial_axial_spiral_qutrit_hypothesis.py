#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1560_oam_radial_axial_spiral_qutrit_hypothesis.json'
MD = ROOT / 'analysis' / 'BT1560_oam_radial_axial_spiral_qutrit_hypothesis.md'
TEX = ROOT / 'analysis' / 'BT1560_oam_radial_axial_spiral_qutrit_hypothesis.tex'

ROWS = [
    {'qutrit_leg':'ternary phase/OAM charge','spiral_component':'azimuthal winding','status':'candidate physical encoding'},
    {'qutrit_leg':'radial mode index','spiral_component':'radial amplitude shell','status':'candidate auxiliary qutrit or gauge'},
    {'qutrit_leg':'axial propagation bin','spiral_component':'past/future time-bin leg','status':'matches self-entangled qutrit reading'},
]


def main() -> None:
    bt1556 = json.loads((ROOT / 'data' / 'bt1556_w33_self_entangled_qutrit_reinterpretation.json').read_text(encoding='utf-8'))
    checks = {
        'bt1556_verified': bt1556.get('verified') is True,
        'three_candidate_rows': len(ROWS) == 3,
        'has_radial': any('radial' in r['spiral_component'] for r in ROWS),
        'has_axial': any('axial' in r['spiral_component'] or 'time-bin' in r['spiral_component'] for r in ROWS),
        'has_oam_winding': any('winding' in r['spiral_component'] for r in ROWS),
        'hypothesis_not_theorem': True,
    }
    result = {
        'bt': 1560,
        'title': 'OAM radial/axial spiral qutrit hypothesis',
        'verified': all(checks.values()),
        'source': 'data/bt1556_w33_self_entangled_qutrit_reinterpretation.json',
        'rows': ROWS,
        'interpretation': 'The ternary self-entangled qutrit may have a photonic spiral encoding: azimuthal OAM winding for ternary phase/charge, radial mode index for shell/gauge, and axial propagation/time-bin for past/future Choi legs. This is a physical-encoding hypothesis to test, not a theorem.',
        'honesty_boundary': 'No OAM experiment or mode decomposition is verified here; this creates the next objectwise test target.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1560 OAM Radial/Axial Spiral Qutrit Hypothesis\n\nThe ternary self-entangled qutrit may have a photonic spiral encoding: azimuthal OAM winding for ternary phase/charge, radial mode index for shell/gauge, and axial propagation/time-bin for past/future Choi legs. This is a physical-encoding hypothesis, not a theorem.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1560: OAM suggests a radial/axial spiral encoding hypothesis for the self-entangled qutrit; this is a test target, not a theorem.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt': 1560, 'verified': result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
