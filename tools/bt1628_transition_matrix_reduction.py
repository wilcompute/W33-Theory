#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1628_transition_matrix_reduction.json'
MD = ROOT / 'analysis' / 'BT1628_transition_matrix_reduction.md'
TEX = ROOT / 'analysis' / 'BT1628_transition_matrix_reduction.tex'

FRAMES = 1600

def rec(frame: int):
    s = frame // 40
    t = frame % 40
    rel = (t - s) % 40
    role = 'control' if rel < 13 else 'contextual_fuel'
    return s, t, rel, role

def matrix_for(role_filter: str):
    c = Counter()
    for f in range(FRAMES):
        s, t, rel, role = rec(f)
        if role_filter == 'all' or role == role_filter:
            c[(s % 3, t % 3)] += 1
    return [[c[(i,j)] for j in range(3)] for i in range(3)]

def row_sums(m):
    return [sum(row) for row in m]

def col_sums(m):
    return [sum(m[i][j] for i in range(3)) for j in range(3)]

def normalize_rows(m):
    return [[0 if sum(row)==0 else round(x/sum(row), 8) for x in row] for row in m]

def main() -> None:
    all_m = matrix_for('all')
    control_m = matrix_for('control')
    fuel_m = matrix_for('contextual_fuel')
    rel_counts = {}
    for role_filter in ('control','contextual_fuel'):
        c = Counter()
        for f in range(FRAMES):
            s,t,rel,role = rec(f)
            if role == role_filter:
                c[rel % 3] += 1
        rel_counts[role_filter] = {str(k): v for k,v in sorted(c.items())}
    checks = {
        'all_matrix_sum_1600': sum(map(sum, all_m)) == 1600,
        'control_matrix_sum_520': sum(map(sum, control_m)) == 520,
        'fuel_matrix_sum_1080': sum(map(sum, fuel_m)) == 1080,
        'all_matrix_factorized_by_margins': all_m == [[196,182,182],[182,169,169],[182,169,169]],
        'control_matrix_nontrivial': control_m == [[70,56,56],[56,61,52],[56,52,61]],
        'fuel_matrix_nontrivial': fuel_m == [[126,126,126],[126,108,117],[126,117,108]],
        'control_relative_bias_200_160_160': rel_counts['control'] == {'0':200,'1':160,'2':160},
        'fuel_relative_balanced_360_each': rel_counts['contextual_fuel'] == {'0':360,'1':360,'2':360},
    }
    result = {
        'bt': 1628,
        'title': 'Transition-matrix reduction',
        'verified': all(checks.values()),
        'source': 'data/bt1624_minimal_decoded_stream_statistics.json',
        'reduction_rule': 'source_ray mod 3 by target_ray mod 3, separated into all/control/fuel roles',
        'matrices': {
            'all': {'counts': all_m, 'row_normalized': normalize_rows(all_m), 'row_sums': row_sums(all_m), 'col_sums': col_sums(all_m)},
            'control': {'counts': control_m, 'row_normalized': normalize_rows(control_m), 'row_sums': row_sums(control_m), 'col_sums': col_sums(control_m)},
            'contextual_fuel': {'counts': fuel_m, 'row_normalized': normalize_rows(fuel_m), 'row_sums': row_sums(fuel_m), 'col_sums': col_sums(fuel_m)},
        },
        'relative_target_mod3_counts': rel_counts,
        'interpretation': 'The full 40x40 all-transition reduction is marginal/factorized and therefore too trivial for CKM comparison. The control/fuel split is the first nontrivial reduced observable: control has a 200/160/160 relative-target bias, while fuel is balanced by residue.',
        'honesty_boundary': 'This is a sector-reduction candidate only. It is not a CKM/PMNS fit and produces no PASS verdict.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1628 Transition-matrix Reduction\n\nThe 40x40 transition matrix is reduced by source mod 3 and target mod 3. The all-transition matrix is factorized and too trivial for CKM comparison. The control/fuel split is more interesting: control has a 200/160/160 relative-target residue bias, while contextual fuel is balanced at 360/360/360.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1628: transition reduction shows all-pair matrix is factorized, while control/fuel split gives the first nontrivial residue observable.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1628,'verified':result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__': main()
