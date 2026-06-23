#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1625_unit_map_ledger.json'
MD = ROOT / 'analysis' / 'BT1625_unit_map_ledger.md'
TEX = ROOT / 'analysis' / 'BT1625_unit_map_ledger.tex'

ROWS = [
    {'observable':'fano_bin_entropy_profile','sector':'gauge','unit_status':'dimensionless','required_anchor':'none beyond normalized counts','claim_status':'placeholder_observable'},
    {'observable':'ordered_transition_matrix','sector':'CKM','unit_status':'dimensionless','required_anchor':'normalized transition probabilities','claim_status':'placeholder_observable'},
    {'observable':'protected_zero_syndrome_profile','sector':'PMNS_neutrino','unit_status':'dimensionless','required_anchor':'normalized syndrome/residue counts','claim_status':'placeholder_observable'},
    {'observable':'witting_spectral_hierarchy_trace','sector':'quark_masses','unit_status':'requires_scale_anchor','required_anchor':'v_EW or calibrated spectral energy map','claim_status':'missing_unit_map'},
    {'observable':'scalar_trace_proxy','sector':'Higgs_strong_CP','unit_status':'requires_scale_anchor','required_anchor':'v_EW plus scalar trace normalization','claim_status':'missing_physical_observable'},
    {'observable':'fault_energy_gap','sector':'mass_gap_fault_bridge','unit_status':'requires_dynamic_anchor','required_anchor':'hbar/tau, detector calibration, or stated W33 unit map','claim_status':'candidate_only'},
]

def main() -> None:
    counts = {}
    for r in ROWS:
        counts[r['unit_status']] = counts.get(r['unit_status'], 0) + 1
    checks = {
        'six_rows': len(ROWS) == 6,
        'three_dimensionless': counts.get('dimensionless', 0) == 3,
        'two_scale_anchor': counts.get('requires_scale_anchor', 0) == 2,
        'one_dynamic_anchor': counts.get('requires_dynamic_anchor', 0) == 1,
        'all_have_required_anchor': all(r['required_anchor'] for r in ROWS),
        'no_measured_units_claimed': all(r['claim_status'] != 'measured' for r in ROWS),
    }
    result = {
        'bt': 1625,
        'title': 'Unit-map ledger',
        'verified': all(checks.values()),
        'source_packets': {'observables':'data/bt1622_abi_observable_schema_for_sm_sectors.json','decoded_stats':'data/bt1624_minimal_decoded_stream_statistics.json'},
        'unit_rows': ROWS,
        'unit_status_counts': counts,
        'interpretation': 'The ledger separates dimensionless count observables from sectors requiring v_EW, scalar normalization, hbar/tau, detector calibration, or a W33 unit map. This prevents dimensionful SM comparisons from being treated as already available.',
        'honesty_boundary': 'No physical unit calibration is performed here; this is a unit-dependency ledger only.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1625 Unit-map Ledger\n\nDimensionless decoded-count observables are separated from observables requiring v_EW, scalar trace normalization, hbar/tau, detector calibration, or a W33 unit map. No physical unit calibration is performed here.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1625: unit-map ledger separates dimensionless observables from scale-anchored and dynamic-unit observables.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1625,'verified':result['verified'],'counts':counts}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__': main()
