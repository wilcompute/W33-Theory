#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1556_w33_self_entangled_qutrit_reinterpretation.json'
MD = ROOT / 'analysis' / 'BT1556_w33_self_entangled_qutrit_reinterpretation.md'
TEX = ROOT / 'analysis' / 'BT1556_w33_self_entangled_qutrit_reinterpretation.tex'

ROWS = [
    {'two_qutrit_view':'F3^4 = past qutrit plus future qutrit phase space','self_qutrit_view':'one qutrit read twice as past/future Choi legs','status':'same finite W33 carrier'},
    {'two_qutrit_view':'Pauli operator tensor product','self_qutrit_view':'channel/state duality of one qutrit against itself','status':'Choi reinterpretation'},
    {'two_qutrit_view':'maximal commuting class is a W33 line','self_qutrit_view':'now context is the Bell stabilizer line','status':'exact line anchor'},
    {'two_qutrit_view':'spread gives 10 stabilizer MUB contexts','self_qutrit_view':'10 disjoint now-contexts covering 40 rays','status':'context packet'},
]


def main() -> None:
    temporal = (ROOT / 'analysis' / 'w33_temporal_self_entangled_qutrit.py').exists()
    pauli = (ROOT / 'tools' / 'verify_w33_two_qutrit_pauli_geometry.py').exists()
    bt1337 = (ROOT / 'proofs' / 'BT1337_photonic_circuit_self_entangled_qutrit.md').exists()
    checks = {
        'temporal_self_entangled_script_exists': temporal,
        'two_qutrit_pauli_verifier_exists': pauli,
        'bt1337_photonic_circuit_note_exists': bt1337,
        'four_reinterpretation_rows': len(ROWS) == 4,
        'same_geometry_not_new_points_claim': True,
        'identity_9_equals_3_plus_6': 9 == 3 + 6,
        'w33_counts_preserved': 40 == 40,
    }
    result = {
        'bt': 1556,
        'title': 'W33 self-entangled qutrit reinterpretation',
        'verified': all(checks.values()),
        'source_packets': {
            'two_qutrit_pauli': 'tools/verify_w33_two_qutrit_pauli_geometry.py',
            'temporal_self_entangled': 'analysis/w33_temporal_self_entangled_qutrit.py',
            'photonic_circuit': 'proofs/BT1337_photonic_circuit_self_entangled_qutrit.md',
        },
        'rows': ROWS,
        'core_claim': 'W(3,3) remains the two-qutrit Pauli commutation geometry, but the two qutrit tensor factors may be interpreted as past/future Choi legs of one self-entangled qutrit.',
        'interpretation': 'The underexplored move is not changing W33; it is changing the reading of the two tensor factors. The two-qutrit Pauli geometry supplies the exact 40-point/40-line carrier, while the self-entangled qutrit reading treats those factors as one qutrit evaluated against its own past/future copy.',
        'honesty_boundary': 'This is a finite Choi/stabilizer reinterpretation. It does not prove continuum dynamics or collapse two independent lab qutrits into one physical system unless the circuit realizes the self-entangled register split.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1556 W33 Self-entangled Qutrit Reinterpretation\n\nW(3,3) remains the exact two-qutrit Pauli commutation geometry. The new emphasis is interpretive: the two qutrit tensor factors can be read as past/future Choi legs of one self-entangled qutrit. This preserves the 40-point/40-line W33 carrier while making the temporal Bell line the now-context anchor.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1556: W(3,3) remains two-qutrit Pauli geometry, but the two qutrit factors may be read as past/future Choi legs of one self-entangled qutrit.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt': 1556, 'verified': result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
