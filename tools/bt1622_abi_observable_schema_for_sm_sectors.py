#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1622_abi_observable_schema_for_sm_sectors.json'
MD = ROOT / 'analysis' / 'BT1622_abi_observable_schema_for_sm_sectors.md'
TEX = ROOT / 'analysis' / 'BT1622_abi_observable_schema_for_sm_sectors.tex'

OBS = [
    {'sector':'gauge','observable':'fano_bin_entropy_profile','decoded_fields':['detector_bin','orbit','fano_point','rail'],'statistic':'usage entropy and rail-normalized residue distribution','needed_for':['alpha_inv_tree','sin2_theta_W','alpha_s'],'status':'missing_decoded_stream'},
    {'sector':'quark_masses','observable':'witting_spectral_hierarchy_trace','decoded_fields':['source_ray','target_ray','role','relative_target'],'statistic':'source-target transition spectrum with calibrated energy/unit map','needed_for':['m_t','m_c','m_u','m_b'],'status':'missing_unit_map'},
    {'sector':'CKM','observable':'ordered_transition_matrix','decoded_fields':['source_ray','target_ray','tick_start','role'],'statistic':'normalized 40x40 transition counts and sector-reduced mixing matrix','needed_for':['V_us','A_wolf','V_cb','V_ub','delta_CKM'],'status':'missing_decoded_stream'},
    {'sector':'PMNS_neutrino','observable':'protected_zero_syndrome_profile','decoded_fields':['css_syndrome_row','hesse_residue','pauli_frame_update'],'statistic':'syndrome-sector occupancy and protected-zero ratios','needed_for':['dm32_dm21_ratio','sin2_theta12_PMNS','sin2_theta23_PMNS','sin2_theta13_PMNS'],'status':'missing_observable_definition'},
    {'sector':'Higgs_strong_CP','observable':'scalar_trace_and_cp_firewall','decoded_fields':['role','hesse_residue','fault_outcome','pauli_frame_update'],'statistic':'scalar-sector trace proxy plus CP/parity diagnostic with blocked strong-CP language','needed_for':['lambda_H','m_H','theta_QCD'],'status':'blocked_pending_physical_observable'},
]

def main() -> None:
    checks = {
        'five_observable_rows': len(OBS) == 5,
        'all_have_decoded_fields': all(o['decoded_fields'] for o in OBS),
        'all_have_needed_for': all(o['needed_for'] for o in OBS),
        'all_status_not_ready': all(o['status'] != 'ready' for o in OBS),
        'has_ckm_transition_matrix': any(o['sector']=='CKM' and 'transition' in o['observable'] for o in OBS),
        'has_strong_cp_firewall': any(o['sector']=='Higgs_strong_CP' and 'firewall' in o['observable'] for o in OBS),
    }
    result = {'bt':1622,'title':'ABI observable schema for SM sectors','verified':all(checks.values()),'source_packets':{'parameters':'data/bt1621_canonical_sm_parameter_table.json','sequence_decoder':'data/bt1613_sequence_level_inverse_decoder.json','fault_decoder':'data/bt1614_fault_aware_decoder_integration.json'},'observables':OBS,'interpretation':'Each algebraic SM sector now has a required ABI observable and decoded-field dependency, but every observable remains missing, blocked, or awaiting a unit map.','honesty_boundary':'Schema only; no observable is evaluated and no SM comparison is performed.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    MD.write_text('# BT1622 ABI Observable Schema for SM Sectors\n\nEach algebraic SM sector is assigned a required ABI observable: Fano entropy/residue profile, Witting spectral hierarchy trace, ordered transition matrix, protected-zero syndrome profile, and scalar trace/CP firewall. All remain missing, blocked, or awaiting a unit map.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1622: SM sectors receive ABI observable schemas, but all observables remain missing, blocked, or unit-map pending.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1622,'verified':result['verified'],'rows':len(OBS)}, indent=2))
    if not result['verified']: raise SystemExit(1)

if __name__ == '__main__': main()
