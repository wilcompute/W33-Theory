#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1557_temporal_choi_line_to_a2_singleton_map.json'
MD = ROOT / 'analysis' / 'BT1557_temporal_choi_line_to_a2_singleton_map.md'
TEX = ROOT / 'analysis' / 'BT1557_temporal_choi_line_to_a2_singleton_map.tex'

AXES = ['alpha','beta','alpha+beta','-alpha','-beta','-(alpha+beta)']


def main() -> None:
    bt1556 = json.loads((ROOT / 'data' / 'bt1556_w33_self_entangled_qutrit_reinterpretation.json').read_text(encoding='utf-8'))
    bt1547 = json.loads((ROOT / 'data' / 'bt1547_e6_a2_singleton_axis_object_map.json').read_text(encoding='utf-8'))
    bell_generators = ['XpXf', 'ZpZfinv']
    rows = []
    for i, axis in enumerate(AXES):
        rows.append({
            'a2_axis': i,
            'axis_label': axis,
            'choi_leg': 'past' if i < 3 else 'future',
            'opposite_axis': (i + 3) % 6,
            'sector': bt1547['rows'][i]['sector'],
            'fiber_class': bt1547['rows'][i]['fiber_class'],
            'bell_generator_context': bell_generators[i % 2],
        })
    checks = {
        'bt1556_verified': bt1556.get('verified') is True,
        'bt1547_verified': bt1547.get('verified') is True,
        'six_axis_rows': len(rows) == 6,
        'three_past_three_future': sum(1 for r in rows if r['choi_leg'] == 'past') == 3 and sum(1 for r in rows if r['choi_leg'] == 'future') == 3,
        'opposites_pair_past_future': all(rows[i]['choi_leg'] != rows[i+3]['choi_leg'] for i in range(3)),
        'opposites_share_sector': all(rows[i]['sector'] == rows[i+3]['sector'] for i in range(3)),
        'opposites_share_fiber': all(rows[i]['fiber_class'] == rows[i+3]['fiber_class'] for i in range(3)),
        'now_stabilizes_fiber_pairs_not_single_fiber': len({r['fiber_class'] for r in rows}) == 3,
    }
    result = {
        'bt': 1557,
        'title': 'Temporal Choi line to A2 singleton map',
        'verified': all(checks.values()),
        'source_packets': {'self_qutrit':'data/bt1556_w33_self_entangled_qutrit_reinterpretation.json','a2_singleton':'data/bt1547_e6_a2_singleton_axis_object_map.json'},
        'bell_line_generators': bell_generators,
        'rows': rows,
        'interpretation': 'The temporal Choi reading splits the six A2 singleton axes into three past and three future legs. Opposite A2 axes pair past/future and share the same fixed-hexagon sector/fiber class, so now stabilizes sector-fiber pairs rather than choosing one isolated fiber.',
        'honesty_boundary': 'This is a finite Choi/A2 opposition map, not a dynamical time-evolution theorem.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1557 Temporal Choi Line to A2 Singleton Map\n\nThe temporal Choi reading splits the six A2 singleton axes into three past and three future legs. Opposite axes pair past/future and share the same fixed-hexagon sector and fiber class. Thus now stabilizes sector-fiber pairs, not one isolated fiber.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1557: temporal Choi legs split the six A2 axes into three past/future pairs sharing sector and fiber class.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt': 1557, 'verified': result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
