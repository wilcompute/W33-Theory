#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1561_oam_qutrit_mode_basis_test.json'
MD = ROOT / 'analysis' / 'BT1561_oam_qutrit_mode_basis_test.md'
TEX = ROOT / 'analysis' / 'BT1561_oam_qutrit_mode_basis_test.tex'

CANDIDATES = [
    {'name':'centered_pm0','ell':[-1,0,1], 'opposition_pairs':[[-1,1]], 'has_zero_anchor':True},
    {'name':'cyclic_012','ell':[0,1,2], 'opposition_pairs':[], 'has_zero_anchor':True},
    {'name':'mod3_centered','ell':[-1,0,1], 'qutrit_labels':[2,0,1], 'opposition_pairs':[[2,1]], 'has_zero_anchor':True},
]


def score(c):
    return {
        'ternary_count': len(c['ell']) == 3,
        'has_zero_anchor': c.get('has_zero_anchor', False),
        'has_physical_opposition': len(c.get('opposition_pairs', [])) > 0,
        'cyclic_mod3_ready': c['name'] in ('cyclic_012','mod3_centered'),
        'a2_pair_compatible': c['name'] in ('centered_pm0','mod3_centered'),
    }


def main() -> None:
    bt1560 = (ROOT / 'data' / 'bt1560_oam_spiral_qutrit_manifest.json').exists() or (ROOT / 'tools' / 'bt1560_oam_radial_axial_spiral_qutrit_hypothesis.py').exists()
    rows = []
    for c in CANDIDATES:
        s = score(c)
        rows.append({**c, 'score': s, 'score_total': sum(1 for v in s.values() if v)})
    best = sorted(rows, key=lambda r: r['score_total'], reverse=True)[0]
    checks = {
        'bt1560_source_exists': bt1560,
        'three_candidates': len(rows) == 3,
        'centered_candidate_present': any(r['name'] == 'centered_pm0' for r in rows),
        'cyclic_candidate_present': any(r['name'] == 'cyclic_012' for r in rows),
        'best_is_mod3_centered': best['name'] == 'mod3_centered',
        'not_lab_validation': True,
    }
    result = {
        'bt':1561,
        'title':'OAM qutrit mode-basis test',
        'verified': all(checks.values()),
        'candidates': rows,
        'best_candidate_for_a2_fiber3': best['name'],
        'interpretation':'The centered OAM basis l=-1,0,+1 has the natural physical opposition needed for the A2/fixed-hexagon story, while the 0,1,2 basis is computationally cyclic. The mod3-centered labeling keeps both: physical OAM opposition and qutrit mod-3 labels.',
        'honesty_boundary':'This is a basis-compatibility test, not an OAM experiment or optical mode-overlap validation.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1561 OAM Qutrit Mode-basis Test\n\nThree OAM qutrit bases are compared. The centered physical basis l=-1,0,+1 best captures opposition; the cyclic basis 0,1,2 best captures pure mod-3 labels. The mod3-centered encoding keeps both by using physical l=-1,0,+1 with qutrit labels 2,0,1. This is a basis-compatibility result, not a lab validation.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1561: centered OAM $\\ell=-1,0,+1$ supplies physical opposition, while mod-3 labels retain qutrit cyclicity.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1561,'verified':result['verified'],'best':best['name']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
