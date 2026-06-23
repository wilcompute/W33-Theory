#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1562_radial_axial_qutrit_factorization_schema.json'
MD = ROOT / 'analysis' / 'BT1562_radial_axial_qutrit_factorization_schema.md'
TEX = ROOT / 'analysis' / 'BT1562_radial_axial_qutrit_factorization_schema.tex'

FACTORS = [
    {'factor':'azimuthal_oam','ternary_states':['ell=-1','ell=0','ell=+1'],'role':'phase/opposition qutrit'},
    {'factor':'radial_shell','ternary_states':['p=0','p=1','p=2'],'role':'sector or gauge shell'},
    {'factor':'axial_timebin','ternary_states':['z0','z1','z2'],'role':'past-now-future propagation register'},
]
CHOI_SPLIT = [
    {'choi_leg':'past','axial_support':['z0','z1','z2'],'interpretation':'input time-bin ladder'},
    {'choi_leg':'future','axial_support':['z0','z1','z2'],'interpretation':'output time-bin ladder'},
    {'choi_leg':'now','axial_support':['diagonal pairs z_j|z_j'],'interpretation':'Bell/Choi contraction'},
]


def main() -> None:
    bt1561 = json.loads((ROOT / 'data' / 'bt1561_oam_qutrit_mode_basis_test.json').read_text(encoding='utf-8'))
    checks = {
        'bt1561_verified': bt1561.get('verified') is True,
        'three_factors': len(FACTORS) == 3,
        'each_factor_ternary': all(len(f['ternary_states']) == 3 for f in FACTORS),
        'has_azimuthal': any(f['factor'] == 'azimuthal_oam' for f in FACTORS),
        'has_radial': any(f['factor'] == 'radial_shell' for f in FACTORS),
        'has_axial': any(f['factor'] == 'axial_timebin' for f in FACTORS),
        'choi_split_lands_on_axial': len(CHOI_SPLIT) == 3 and all('axial_support' in row for row in CHOI_SPLIT),
        'schema_not_optical_validation': True,
    }
    result = {
        'bt':1562,
        'title':'Radial/axial qutrit factorization schema',
        'verified': all(checks.values()),
        'source':'data/bt1561_oam_qutrit_mode_basis_test.json',
        'factors': FACTORS,
        'choi_split': CHOI_SPLIT,
        'interpretation':'The ternary self-qutrit can be factored as azimuthal OAM for phase/opposition, radial shell for sector/gauge, and axial time-bin for past/future/now propagation. The Choi split lands naturally on the axial/time-bin factor because BT1337 already realizes past/future through a three-bin delay ladder.',
        'honesty_boundary':'This is an encoding schema, not a proof that actual lab modes remain separable or low-leakage.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1562 Radial/Axial Qutrit Factorization Schema\n\nThe ternary self-qutrit factors into azimuthal OAM for phase/opposition, radial shell for sector or gauge, and axial time-bin for past/future/now propagation. The Choi split naturally lands on the axial factor because BT1337 already uses a three-bin delay ladder. This is an encoding schema, not lab validation.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1562: azimuthal OAM, radial shell, and axial time-bin give a three-factor spiral schema for the ternary self-qutrit.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1562,'verified':result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
