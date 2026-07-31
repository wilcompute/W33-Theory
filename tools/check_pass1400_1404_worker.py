#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
worker = sys.argv[1]
observed_path = Path(sys.argv[2])
assert worker in {'1400','1401','1402','1403','1404'}
cert = json.loads((ROOT/'data'/'w33_pass1400_1404_five_frontiers.json').read_text())
observed = json.loads(observed_path.read_text())
assert observed['canonical_pass'] == worker
assert observed['sha256'] == cert['workers'][worker]

if worker == '1400':
    frozen = cert['pass1400']
    assert observed['projector_denominator_lcms'] == frozen['denominators']
    assert observed['localization'] == frozen['localization']
    assert {p: observed['full_orbital_modular_profiles'][p]['radical_power_dimensions'] for p in ('2','3','5')} == frozen['radicals']
    assert observed['characteristic5_regular_factor_census'] == frozen['p5_factors']
elif worker == '1401':
    frozen = cert['pass1401']
    assert observed['invariant_dual_axis'] == frozen['axis']
    assert observed['invariant_dual_plane_basis'] == frozen['plane_basis']
    assert observed['plane_quadratic_form'] == frozen['quadratic_form']
    assert [x['size'] for x in observed['orbit_classification']] == frozen['sizes']
    assert [x['signature'] for x in observed['orbit_classification']] == frozen['signatures']
elif worker == '1402':
    frozen = cert['pass1402']
    assert observed['block_dimensions'] == frozen['blocks']
    assert observed['forward_basis_U']['sha256'] == frozen['U']['sha']
    assert observed['inverse_transform_Uinv']['sha256'] == frozen['Uinv']['sha']
    assert {k: observed['operators'][k]['sha256'] for k in ('A','D','S')} == frozen['operators']
elif worker == '1403':
    frozen = cert['pass1403']
    assert [observed['apartment_rows'], observed['levi_flag_columns'], observed['sheet_rank'], observed['sheet_boundaryless']] == frozen['sheet']
    assert {k: [v['rank'], v['boundaryless'], v['sha256']] for k,v in observed['bridge_scan'].items()} == frozen['bridges']
    assert [x['bridge_rank'] for x in observed['mackey_sector_bridge_ranks']] == frozen['mackey_ranks']
elif worker == '1404':
    frozen = cert['pass1404']
    assert [observed['O_contained_in_selected_M'], observed['selected_M_contained_in_O']] == frozen['containment']
    assert [observed['index_M_over_intersection'], observed['index_O_over_intersection']] == frozen['intersection_indices']
    assert [observed['level_O_to_M'], observed['level_M_to_O']] == frozen['levels']
    assert observed['orbital_reduced_trace_discriminant'] == frozen['disc']
    assert observed['discriminant_factorization'] == frozen['disc_factors']
    assert observed['smith_rational_factor_census'] == frozen['smith']

print(f'PASS worker {worker} matches frozen compact certificate')
