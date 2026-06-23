#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1607_full_architecture_closure_map.json'
MD = ROOT / 'analysis' / 'BT1607_full_architecture_closure_map.md'
TEX = ROOT / 'analysis' / 'BT1607_full_architecture_closure_map.tex'

LAYERS = [
    {'layer':'self_entangled_qutrit','objects':'BT1556-BT1558','status':'structural finite Choi/W33 reading'},
    {'layer':'operator_on_photon','objects':'BT1564-BT1569','status':'finite state/operator ABI plus OAM witness firewall'},
    {'layer':'centered_oam_radial_axial_frontend','objects':'BT1570-BT1594','status':'recenter law, calibrated gates, leakage simulator, lab-facing Hesse/T loop'},
    {'layer':'witting_transaction_cycle','objects':'BT1595-BT1600','status':'accepted Witting pairs are control; rejected pairs are contextual fuel'},
    {'layer':'physical_fano_universal_abi','objects':'BT1601-BT1603','status':'finite theorem-level photonic-computation ABI'},
    {'layer':'holographic_bus_audit','objects':'BT1605','status':'near-max entropy Fano bus; pointwise injection blocked; temporal/signature target defined'},
    {'layer':'physics_bridge_firewall','objects':'BT1606','status':'mass-gap/fault bridge candidate with continuum overclaims blocked'},
]

OPEN_GATES = [
    {'gate':'decoder_reconstruction','needed_for':'turn BT1605 temporal/signature target into an actual inverse decoder'},
    {'gate':'fault_decoder_min_chain','needed_for':'turn BT1606 mass-gap/fault bridge into a computed comparison'},
    {'gate':'SM_parameter_circuit_comparator','needed_for':'connect algebraic SM parameter packets to BT1603 ABI outputs'},
    {'gate':'hardware_calibration','needed_for':'convert symbolic OAM/radial/loss placeholders into measured optical tolerances'},
]

def main() -> None:
    checks = {
        'seven_layers': len(LAYERS) == 7,
        'four_open_gates': len(OPEN_GATES) == 4,
        'has_universal_abi': any(l['layer'] == 'physical_fano_universal_abi' for l in LAYERS),
        'has_holographic_audit': any(l['layer'] == 'holographic_bus_audit' for l in LAYERS),
        'has_physics_firewall': any(l['layer'] == 'physics_bridge_firewall' for l in LAYERS),
        'all_layers_have_status': all(l['status'] for l in LAYERS),
        'all_open_gates_have_needed_for': all(g['needed_for'] for g in OPEN_GATES),
    }
    result = {
        'bt': 1607,
        'title': 'Full architecture closure map',
        'verified': all(checks.values()),
        'last_two_day_commit_wave': 'BT1553-BT1606 plus BT1604 roadmap audit',
        'layers': LAYERS,
        'open_gates': OPEN_GATES,
        'interpretation': 'The architecture is now a finite pipeline: self-entangled qutrit -> operator-on-photon -> OAM/radial/axial frontend -> Witting transaction cycle -> Fano detector bus -> Hesse/T non-Clifford port -> CSS syndrome handoff. The remaining unsolved pieces are inverse decoding, minimum-fault-chain computation, SM-parameter circuit comparison, and hardware calibration.',
        'honesty_boundary': 'Architecture map only; it does not prove SM parameters, continuum mass gap, fault tolerance, or hardware performance.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1607 Full Architecture Closure Map\n\nThe last-two-day commit wave closes a finite architecture pipeline: self-entangled qutrit, operator-on-photon, centered OAM/radial/axial frontend, Witting transaction cycle, physical Fano detector bus, Hesse/T non-Clifford port, and CSS syndrome handoff. The remaining open gates are inverse detector decoding, minimum logical-fault-chain computation, SM-parameter circuit comparison, and hardware calibration.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1607: architecture map closes the finite pipeline from self-entangled qutrit to Witting/Fano/Hesse/CSS ABI, with decoder, fault-chain, SM-bridge, and calibration gates left open.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1607,'verified':result['verified'],'layers':len(LAYERS)}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
