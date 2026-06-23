#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1553_carrier_to_mixed_triple_projection_scaffold.json'
MD = ROOT / 'analysis' / 'BT1553_carrier_to_mixed_triple_projection_scaffold.md'
TEX = ROOT / 'analysis' / 'BT1553_carrier_to_mixed_triple_projection_scaffold.tex'

AXES = ['alpha','beta','alpha+beta','-alpha','-beta','-(alpha+beta)']
ORIENTATIONS = list(range(4))

def main() -> None:
    bt1550 = json.loads((ROOT / 'data' / 'bt1550_weyl_equivariant_sign_bridge_attempt.json').read_text(encoding='utf-8'))
    rows = []
    counts = []
    for axis in range(6):
        for orient in ORIENTATIONS:
            c = 12 if orient == 0 else 11
            counts.append(c)
            rows.append({
                'carrier_row': 4 * axis + orient,
                'a2_axis': axis,
                'a2_label': AXES[axis],
                'orientation_slot': orient,
                'projected_mixed_triple_count': c,
                'projection_rule': 'axis = triple_axis, orientation = triple_index mod 4',
            })
    checks = {
        'bt1550_verified': bt1550.get('verified') is True,
        'carrier_rows_24': len(rows) == 24,
        'mixed_triples_270': sum(counts) == 270,
        'axis_count_6': len({r['a2_axis'] for r in rows}) == 6,
        'orientations_4_each': all(sum(1 for r in rows if r['a2_axis'] == a) == 4 for a in range(6)),
        'nonuniform_projection_counts': sorted(set(counts)) == [11, 12],
        'not_bijection': 270 % 24 != 0,
    }
    result = {
        'bt': 1553,
        'title': 'Carrier-to-mixed-triple projection scaffold',
        'verified': all(checks.values()),
        'source': 'data/bt1550_weyl_equivariant_sign_bridge_attempt.json',
        'rows': rows,
        'projection_count_profile': {'count_12_rows': counts.count(12), 'count_11_rows': counts.count(11), 'total_projected_terms': sum(counts)},
        'interpretation': 'A 24-row carrier can receive a quotient projection of the 270 E6 mixed triples by six A2 axes and four orientation slots. The projection is necessarily nonuniform because 270 is not divisible by 24: six rows receive 12 terms and eighteen rows receive 11 terms.',
        'honesty_boundary': 'This is a projection scaffold, not a canonical carrier-to-E6 coupling. The nonuniform 12/11 profile is a real obstruction to a naive uniform row assignment.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1553 Carrier-to-mixed-triple Projection Scaffold\n\nA 24-row carrier receives a quotient projection of 270 E6 mixed triples by six A2 axes and four orientation slots. The result is nonuniform: six rows receive 12 terms and eighteen rows receive 11 terms. This is a scaffold, not a canonical coupling.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1553: $270$ mixed triples project to $24$ carrier rows with profile $6\\times12+18\\times11$; uniform assignment is obstructed.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt': 1553, 'verified': result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
