#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1571_lens_phase_calibration_model.json'
MD = ROOT / 'analysis' / 'BT1571_lens_phase_calibration_model.md'
TEX = ROOT / 'analysis' / 'BT1571_lens_phase_calibration_model.tex'

# Centered physical OAM basis with mod-3 qutrit labels.
BASIS = [
    {'ell': -1, 'qutrit_label': 2},
    {'ell': 0, 'qutrit_label': 0},
    {'ell': 1, 'qutrit_label': 1},
]
# Work in omega exponents mod 3.  Qutrit S has phase omega^(j^2).
# A quadratic lens/phase-curvature mask has phase omega^(ell^2) on the centered basis.

def mod3_square(x: int) -> int:
    return (x * x) % 3

def main() -> None:
    rows = []
    for row in BASIS:
        ell = row['ell']
        q = row['qutrit_label']
        rows.append({
            'ell': ell,
            'qutrit_label': q,
            's_gate_exponent': mod3_square(q),
            'lens_quadratic_exponent': mod3_square(ell),
            'matches': mod3_square(q) == mod3_square(ell),
        })
    s_signature = [r['s_gate_exponent'] for r in rows]
    lens_signature = [r['lens_quadratic_exponent'] for r in rows]
    checks = {
        'three_basis_states': len(rows) == 3,
        'centered_basis': [r['ell'] for r in rows] == [-1,0,1],
        'mod3_labels': [r['qutrit_label'] for r in rows] == [2,0,1],
        's_signature_101': s_signature == [1,0,1],
        'lens_signature_101': lens_signature == [1,0,1],
        'exact_match_on_centered_basis': all(r['matches'] for r in rows),
    }
    result = {
        'bt': 1571,
        'title': 'Lens-phase calibration model',
        'verified': all(checks.values()),
        'source_packets': {'bt1561':'tools/bt1561_oam_qutrit_mode_basis_test.py','bt1568':'data/bt1568_lens_prism_oam_dictionary.json'},
        'basis': rows,
        'omega_exponent_signature': {'qutrit_S': s_signature, 'centered_lens_quadratic': lens_signature},
        'calibration_rule': 'Choose the quadratic phase curvature so centered OAM mode ell receives omega^(ell^2). With labels ell=-1,0,+1 <-> q=2,0,1, this equals qutrit S: omega^(q^2).',
        'interpretation': 'The S/lens row can be made exact at the finite phase-signature level on the centered OAM basis. Both qutrit S and centered quadratic lens phase have omega-exponent signature [1,0,1].',
        'honesty_boundary': 'This is an exact discrete phase-signature match. A physical lens still needs mode-overlap and aberration calibration in the lab.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1571 Lens-phase Calibration Model\n\nOn the centered OAM basis ell=-1,0,+1 with qutrit labels 2,0,1, qutrit S has omega-exponent signature [1,0,1]. A quadratic lens phase omega^(ell^2) has the same signature [1,0,1]. Thus the S/lens row is exact at the finite phase-signature level. Lab calibration is still required for mode overlaps and aberrations.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1571: on $\\ell=-1,0,+1$ with labels $2,0,1$, the qutrit $S$ phase $\\omega^{j^2}$ matches centered lens phase $\\omega^{\\ell^2}$.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1571,'verified':result['verified'],'signature':s_signature}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
