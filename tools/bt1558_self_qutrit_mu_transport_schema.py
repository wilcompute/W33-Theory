#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1558_self_qutrit_mu_transport_schema.json'
MD = ROOT / 'analysis' / 'BT1558_self_qutrit_mu_transport_schema.md'
TEX = ROOT / 'analysis' / 'BT1558_self_qutrit_mu_transport_schema.tex'

TRANSPORT_FIELDS = ['past_axis','future_axis','sector','fiber','choi_pair','mu_source','transport_status']


def main() -> None:
    bt1554 = json.loads((ROOT / 'data' / 'bt1554_packetwise_mu_sign_assignment_attempt.json').read_text(encoding='utf-8'))
    bt1557 = json.loads((ROOT / 'data' / 'bt1557_temporal_choi_line_to_a2_singleton_map.json').read_text(encoding='utf-8'))
    pairs = []
    for i in range(3):
        past = bt1557['rows'][i]
        future = bt1557['rows'][i+3]
        pairs.append({
            'past_axis': past['axis_label'],
            'future_axis': future['axis_label'],
            'sector': past['sector'],
            'fiber': past['fiber_class'],
            'choi_pair': f"{past['axis_label']}|{future['axis_label']}",
            'mu_source': 'missing packetwise Weyl transport; BT1554 only gives count parity and orientation shadow',
            'transport_status': 'schema_only',
        })
    checks = {
        'bt1554_verified': bt1554.get('verified') is True,
        'bt1557_verified': bt1557.get('verified') is True,
        'three_choi_pairs': len(pairs) == 3,
        'transport_fields_complete': all(all(field in p for field in TRANSPORT_FIELDS) for p in pairs),
        'fibers_are_0_1_2': sorted(p['fiber'] for p in pairs) == [0,1,2],
        'schema_not_transport_artifact': all(p['transport_status'] == 'schema_only' for p in pairs),
    }
    result = {
        'bt': 1558,
        'title': 'Self-entangled qutrit packetwise mu transport schema',
        'verified': all(checks.values()),
        'source_packets': {'mu_attempt':'data/bt1554_packetwise_mu_sign_assignment_attempt.json','choi_a2':'data/bt1557_temporal_choi_line_to_a2_singleton_map.json'},
        'pairs': pairs,
        'interpretation': 'The missing packetwise mu-sign assignment can be reframed as transport across three past/future Choi axis pairs of one self-entangled qutrit. This is cleaner than a two-independent-qutrit gauge story, but it is still schema only until Weyl mu transport is computed on the projected triples.',
        'honesty_boundary': 'No packetwise mu transport is computed here; this is the schema for the next executable artifact.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1558 Self-entangled Qutrit Mu Transport Schema\n\nThe missing packetwise mu-sign assignment is reframed as transport across three past/future Choi axis pairs of one self-entangled qutrit. The schema is cleaner than a two-independent-qutrit gauge story, but no Weyl mu transport is computed here.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1558: packetwise $\\mu$ transport is recast as past/future Choi transport across three A2 axis pairs.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt': 1558, 'verified': result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
