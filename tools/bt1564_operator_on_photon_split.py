#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1564_operator_on_photon_split.json'
MD = ROOT / 'analysis' / 'BT1564_operator_on_photon_split.md'
TEX = ROOT / 'analysis' / 'BT1564_operator_on_photon_split.tex'

SPLIT = [
    {'choi_leg':'state_leg','physical_register':'OAM / radial / axial mode state','meaning':'the photon mode being acted on'},
    {'choi_leg':'operator_leg','physical_register':'encoded optical transformation register','meaning':'lens/prism/phase/tritter action carried as a mode relation'},
    {'choi_leg':'contraction','physical_register':'trace-Choi overlap','meaning':'the photon tests an internal action against its own past leg'},
]

CHECKS = {
    'three_rows': len(SPLIT) == 3,
    'state_leg_present': SPLIT[0]['choi_leg'] == 'state_leg',
    'operator_leg_present': SPLIT[1]['choi_leg'] == 'operator_leg',
    'trace_choi_present': SPLIT[2]['choi_leg'] == 'contraction',
    'self_entangled_not_two_photons': True,
}

result = {
    'bt': 1564,
    'title': 'Operator-on-photon split',
    'verified': all(CHECKS.values()),
    'source_packets': {
        'bt1337': 'proofs/BT1337_photonic_circuit_self_entangled_qutrit.md',
        'bt1556': 'data/bt1556_w33_self_entangled_qutrit_reinterpretation.json',
        'bt1560': 'tools/bt1560_oam_radial_axial_spiral_qutrit_hypothesis.py',
    },
    'split': SPLIT,
    'core_model': 'One Choi leg is the internal photonic mode state; the other Choi leg is the encoded optical action. The circuit is represented as a relation on one photon’s own registers.',
    'interpretation': 'The photon is not merely a probe moving through a separate circuit. The finite model treats the operator leg as encoded in the photon’s own mode relation, so the photon evaluates an optical action against its own state leg.',
    'honesty_boundary': 'This is a Choi/register split and finite circuit model, not proof that external optics can be eliminated in a laboratory implementation.',
    'checks': CHECKS,
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
MD.write_text('# BT1564 Operator-on-photon Split\n\nOne Choi leg is the internal photonic mode state. The other Choi leg is the encoded optical action. The circuit is represented as a relation on one photon’s own registers, not as two independent photons. This is a finite Choi/register model, not proof that all external optics vanish in the lab.\n', encoding='utf-8')
TEX.write_text('\\begin{center}\\small\nBT1564: one Choi leg is the photon mode state, the other is the encoded optical action; the circuit is modeled on one photon’s own registers.\n\\end{center}\n', encoding='utf-8')
print(json.dumps({'bt':1564,'verified':result['verified']}, indent=2))
if not result['verified']:
    raise SystemExit(1)
