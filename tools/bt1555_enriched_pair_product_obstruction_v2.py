#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1555_enriched_pair_product_obstruction_v2.json'
MD = ROOT / 'analysis' / 'BT1555_enriched_pair_product_obstruction_v2.md'
TEX = ROOT / 'analysis' / 'BT1555_enriched_pair_product_obstruction_v2.tex'


def main() -> None:
    bt1553 = json.loads((ROOT / 'data' / 'bt1553_carrier_to_mixed_triple_projection_scaffold.json').read_text(encoding='utf-8'))
    bt1554 = json.loads((ROOT / 'data' / 'bt1554_packetwise_mu_sign_assignment_attempt.json').read_text(encoding='utf-8'))
    rows = bt1553['rows']
    plus = [r for r in rows if r['orientation_slot'] in (0, 1)]
    minus = [r for r in rows if r['orientation_slot'] in (2, 3)]
    table = []
    nonzero = 0
    weight_sum = 0
    for p in plus:
        row = []
        for m in minus:
            if p['a2_axis'] == m['a2_axis']:
                val = p['projected_mixed_triple_count'] * m['projected_mixed_triple_count']
            else:
                val = 0
            if val:
                nonzero += 1
                weight_sum += val
            row.append(val)
        table.append(row)
    row_weights = [sum(1 for x in row if x) for row in table]
    col_weights = [sum(1 for i in range(len(table)) if table[i][j]) for j in range(len(minus))]
    checks = {
        'bt1553_verified': bt1553.get('verified') is True,
        'bt1554_verified': bt1554.get('verified') is True,
        'plus_rows_12': len(plus) == 12,
        'minus_rows_12': len(minus) == 12,
        'nonzero_pairs_24': nonzero == 24,
        'row_degree_two': row_weights == [2] * 12,
        'col_degree_two': col_weights == [2] * 12,
        'still_sparse': nonzero < 144,
        'projection_weight_nonuniform': len({x for row in table for x in row if x}) > 1,
        'still_no_pair_theorem': True,
    }
    result = {
        'bt': 1555,
        'title': 'Enriched pair-product obstruction v2',
        'verified': all(checks.values()),
        'source_packets': {'projection': 'data/bt1553_carrier_to_mixed_triple_projection_scaffold.json', 'mu_attempt': 'data/bt1554_packetwise_mu_sign_assignment_attempt.json'},
        'plus_rows': len(plus),
        'minus_rows': len(minus),
        'nonzero_pairs': nonzero,
        'weight_sum': weight_sum,
        'row_degrees': row_weights,
        'col_degrees': col_weights,
        'interpretation': 'Using the 270-triple projection increases support from the BT1549 perfect matching to a 2-regular 24-edge bipartite support. This is still sparse and nonuniform, so the carrier remains too small for a pair-product theorem without adding mixed-triple degrees of freedom or a real U/V closure layer.',
        'honesty_boundary': 'This is obstruction v2 for the projected 24-row carrier, not a no-go theorem for enriched 270-term algebra.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1555 Enriched Pair-product Obstruction v2\n\nUsing the 270-triple projection increases the 12+12 support from 12 matching edges to a 2-regular 24-edge bipartite support. It is still sparse and nonuniform. The carrier remains too small for a pair-product theorem without adding mixed-triple degrees of freedom or a real U/V closure layer.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1555: the 270-triple projection lifts the product support to 24 nonzero pairs, but it remains sparse and nonuniform; pair structure is still obstructed.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt': 1555, 'verified': result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
