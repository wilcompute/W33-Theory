#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1620_sm_parameter_bridge_firewall_scaffold.json'
MD = ROOT / 'analysis' / 'BT1620_sm_parameter_bridge_firewall_scaffold.md'
TEX = ROOT / 'analysis' / 'BT1620_sm_parameter_bridge_firewall_scaffold.tex'

ROWS = [
    {'sector':'gauge','repo_source':'exploration/w33_complete_sm_derivation.py','example':'alpha^-1, sin^2 theta_W, alpha_s','abi_observable_needed':'Fano/Hesse residue distribution with calibrated normalization','status':'schema_only'},
    {'sector':'quark_masses','repo_source':'exploration/w33_complete_sm_derivation.py','example':'m_t, m_c, m_u, m_b cascade','abi_observable_needed':'spectral hierarchy observable or calibrated energy/unit map','status':'schema_only'},
    {'sector':'CKM','repo_source':'exploration/w33_complete_sm_derivation.py','example':'V_us, V_cb, V_ub, delta_CKM','abi_observable_needed':'transition statistics over ordered Witting source-target transactions','status':'schema_only'},
    {'sector':'PMNS_neutrino','repo_source':'exploration/w33_complete_sm_derivation.py','example':'PMNS sin^2 angles and neutrino splitting ratio','abi_observable_needed':'protected-zero / syndrome-sector statistics','status':'schema_only'},
    {'sector':'Higgs_strong_CP','repo_source':'exploration/w33_complete_sm_derivation.py','example':'lambda_H, m_H, theta_QCD claim','abi_observable_needed':'calibrated scalar-sector trace observable; strong-CP language must be firewalled','status':'schema_only'},
]
BLOCKED = [
    'ABI measurement statistics already reproduce SM parameters',
    'repository algebraic predictions are validated by BT1603 alone',
    'strong CP is solved experimentally by the finite ABI',
    'Yang-Mills continuum theorem follows from finite photonic ABI',
]
REQUIRED = [
    'extract algebraic parameter table into machine-readable canonical JSON',
    'define ABI observables for each parameter sector',
    'run sequence-level decoder on simulated or bench click streams',
    'compare algebraic prediction, ABI-derived statistic, and accepted external measurement with stated tolerances',
]

def main() -> None:
    checks = {
        'five_sector_rows': len(ROWS) == 5,
        'all_schema_only': all(r['status'] == 'schema_only' for r in ROWS),
        'four_blocked_overclaims': len(BLOCKED) == 4,
        'four_required_objects': len(REQUIRED) == 4,
        'has_ckm': any(r['sector'] == 'CKM' for r in ROWS),
        'has_pmns': any(r['sector'] == 'PMNS_neutrino' for r in ROWS),
        'has_firewall': bool(BLOCKED),
    }
    result = {
        'bt': 1620,
        'title': 'SM parameter bridge firewall scaffold',
        'verified': all(checks.values()),
        'source_packets': {
            'sm_derivation': 'exploration/w33_complete_sm_derivation.py',
            'sequence_decoder': 'data/bt1613_sequence_level_inverse_decoder.json',
            'fault_aware_decoder': 'data/bt1614_fault_aware_decoder_integration.json',
            'universal_abi': 'data/bt1603_universal_computation_proof_closure.json',
        },
        'sector_rows': ROWS,
        'required_objects_before_claim': REQUIRED,
        'blocked_overclaims': BLOCKED,
        'interpretation': 'This creates the bridge schema between algebraic SM parameter packets and ABI output statistics, but blocks any agreement claim until a real circuit/statistical comparator exists.',
        'honesty_boundary': 'Scaffold only. No SM parameter agreement, external measurement validation, or physical prediction is claimed here.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1620 SM Parameter Bridge Firewall Scaffold\n\nThis scaffold links algebraic Standard Model parameter sectors to required ABI observables: gauge, quark masses, CKM, PMNS/neutrino, and Higgs/strong-CP sectors. Every row remains schema-only until canonical parameter JSON, ABI observables, decoded click streams, and comparison tolerances exist. Agreement claims are explicitly blocked.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1620: SM-parameter bridge is scaffolded but firewalled; no ABI agreement claim is allowed until a real comparator exists.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt': 1620, 'verified': result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
