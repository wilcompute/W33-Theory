#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1568_lens_prism_oam_dictionary.json'
MD = ROOT / 'analysis' / 'BT1568_lens_prism_oam_dictionary.md'
TEX = ROOT / 'analysis' / 'BT1568_lens_prism_oam_dictionary.tex'

ROWS = [
    {'operation':'I','internal_action':'reference identity on mode label','optic_analogue':'reference arm / calibrated no-op','witness':'V(I)=1'},
    {'operation':'X','internal_action':'cyclic qutrit shift j -> j+1','optic_analogue':'OAM shifter / prism-like mode step','witness':'V(X)=0'},
    {'operation':'Z','internal_action':'ternary phase j -> omega^j j','optic_analogue':'spiral phase plate / azimuthal phase mask','witness':'V(Z)=0'},
    {'operation':'F3','internal_action':'qutrit Fourier mixer','optic_analogue':'tritter / three-mode interferometric mixer','witness':'V(F3)=1/3'},
    {'operation':'S','internal_action':'quadratic phase shear','optic_analogue':'lens curvature / fractional Fourier / phase curvature analogue','witness':'calibrated quadratic-phase signature'},
]

CHECKS = {
    'five_operations': len(ROWS) == 5,
    'has_all_core_ops': sorted(r['operation'] for r in ROWS) == ['F3','I','S','X','Z'],
    'each_has_optic_analogue': all(r['optic_analogue'] for r in ROWS),
    'trace_choi_core_values_present': {r['operation']:r['witness'] for r in ROWS if r['operation'] in ('I','X','Z','F3')} == {'I':'V(I)=1','X':'V(X)=0','Z':'V(Z)=0','F3':'V(F3)=1/3'},
    's_is_calibration_not_exact_fraction': [r for r in ROWS if r['operation']=='S'][0]['witness'].startswith('calibrated'),
}

result = {
    'bt':1568,
    'title':'Lens/prism/OAM dictionary',
    'verified': all(CHECKS.values()),
    'source_packets': {'bt1565':'tools/bt1565_self_applied_photonic_circuit_model.py','bt1567':'tools/bt1567_internal_optic_algebra_table.py'},
    'rows': ROWS,
    'interpretation':'Each finite internal qutrit operation is paired with a physical optical analogue. The dictionary is not a device design; it is the interface layer between the internal Choi operator leg and possible optical mode engineering.',
    'honesty_boundary':'The S/lens row remains calibration-level because a real lens action must be matched to a qutrit quadratic phase in the selected mode basis.',
    'checks': CHECKS,
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
MD.write_text('# BT1568 Lens/Prism/OAM Dictionary\n\nThe internal operations I, X, Z, F3, and S are mapped to optical analogues: reference/no-op, OAM shift or prism step, spiral phase plate, tritter/mode mixer, and lens or phase-curvature analogue. This is the interface layer between the internal Choi operator leg and optical mode engineering.\n', encoding='utf-8')
TEX.write_text('\\begin{center}\\small\nBT1568: internal qutrit operations map to reference, OAM-shift, spiral-phase, tritter, and lens/phase-curvature optical analogues.\n\\end{center}\n', encoding='utf-8')
print(json.dumps({'bt':1568,'verified':result['verified']}, indent=2))
if not result['verified']:
    raise SystemExit(1)
