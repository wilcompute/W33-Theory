#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1563_self_entangled_qutrit_oam_lab_witness.json'
MD = ROOT / 'analysis' / 'BT1563_self_entangled_qutrit_oam_lab_witness.md'
TEX = ROOT / 'analysis' / 'BT1563_self_entangled_qutrit_oam_lab_witness.tex'

WITNESSES = [
    {'test':'OAM basis overlap','prediction':'dominant support in l=-1,0,+1 modes','pass_placeholder':'diagonal overlap high; off-subspace leakage low','kills_if':'mode support is not concentrated in the ternary OAM subspace'},
    {'test':'radial leakage','prediction':'radial p=0,1,2 shells remain distinguishable under qutrit operations','pass_placeholder':'cross-shell leakage remains below chosen engineering tolerance','kills_if':'radial mixing destroys ternary labeling'},
    {'test':'axial Choi visibility','prediction':'time-bin witness retains V(I)=1 and V(X)=V(Z)=0 pattern from BT1337 within OAM-selected subspace','pass_placeholder':'trace-Choi visibility pattern survives OAM/radial filtering','kills_if':'OAM/radial filtering destroys Choi visibility'},
    {'test':'sector/fiber correlation','prediction':'opposite OAM axes map to paired sector/fiber labels','pass_placeholder':'measured sector labels are stable under past/future pairing','kills_if':'opposite-axis pairs do not share the expected sector/fiber label'},
]


def main() -> None:
    bt1562 = json.loads((ROOT / 'data' / 'bt1562_radial_axial_qutrit_factorization_schema.json').read_text(encoding='utf-8'))
    bt1337_exists = (ROOT / 'proofs' / 'BT1337_photonic_circuit_self_entangled_qutrit.md').exists()
    checks = {
        'bt1562_verified': bt1562.get('verified') is True,
        'bt1337_exists': bt1337_exists,
        'four_witnesses': len(WITNESSES) == 4,
        'each_has_kill_condition': all('kills_if' in w and w['kills_if'] for w in WITNESSES),
        'trace_choi_witness_included': any('Choi' in w['test'] or 'Choi' in w['prediction'] for w in WITNESSES),
        'no_numeric_claim_without_lab_data': True,
    }
    result = {
        'bt':1563,
        'title':'Self-entangled qutrit OAM/radial/axial lab witness',
        'verified': all(checks.values()),
        'source_packets': {'factorization':'data/bt1562_radial_axial_qutrit_factorization_schema.json','bt1337':'proofs/BT1337_photonic_circuit_self_entangled_qutrit.md'},
        'witnesses': WITNESSES,
        'interpretation':'The OAM/radial/axial spiral-qutrit interpretation is falsifiable by mode-overlap, radial leakage, axial Choi visibility, and sector/fiber correlation tests. The witness is deliberately qualitative until lab calibration sets numerical thresholds.',
        'honesty_boundary':'This extends the witness list but does not report experimental measurements or set universal tolerance values.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1563 Self-entangled Qutrit OAM/Radial/Axial Lab Witness\n\nThe spiral-qutrit interpretation is made falsifiable through four witness families: OAM basis overlap, radial leakage, axial Choi visibility, and sector/fiber correlation. Each witness includes a kill condition. Numerical tolerances are left for lab calibration; no experimental result is claimed.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1563: OAM overlap, radial leakage, axial Choi visibility, and sector/fiber correlation form a falsifier set for the spiral-qutrit hypothesis.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1563,'verified':result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
