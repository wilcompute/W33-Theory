#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
worker, observed_path = sys.argv[1], Path(sys.argv[2])
assert worker in {'1390','1391','1392','1393','1394'}
frozen = json.loads((ROOT/'data'/'w33_pass1390_1394_five_frontiers.json').read_text())[f'pass{worker}']
observed = json.loads(observed_path.read_text())
assert observed['theorem'] == frozen['theorem']
assert observed['sha256'] == frozen['sha256']
if worker == '1390':
    assert observed['localization'] == frozen['localization']
    for prime in ('2','3','5'):
        assert observed['full_orbital_modular_profiles'][prime]['radical_power_dimensions'] == frozen['full_orbital_modular_profiles'][prime]['radical_power_dimensions']
elif worker == '1391':
    assert observed['orbit_classification'] == frozen['orbit_classification']
elif worker == '1392':
    assert observed['block_dimensions'] == frozen['block_dimensions']
    assert observed['forward_basis_U'] == frozen['forward_basis_U']
    assert observed['inverse_transform_Uinv'] == frozen['inverse_transform_Uinv']
    assert {name: observed['operators'][name]['sha256'] for name in ('A','D','S')} == frozen['operator_hashes']
elif worker == '1393':
    assert observed['bridge_scan'] == frozen['bridge_scan']
    assert observed['mackey_sector_bridge_ranks'] == frozen['mackey_sector_bridge_ranks']
elif worker == '1394':
    for key in ('smith_rational_factor_census','index_M_over_intersection','index_O_over_intersection','discriminant_factorization'):
        assert observed[key] == frozen[key]
print(f'PASS worker {worker} matches frozen certificate')
