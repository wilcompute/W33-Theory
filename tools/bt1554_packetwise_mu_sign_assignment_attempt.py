#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1554_packetwise_mu_sign_assignment_attempt.json'
MD = ROOT / 'analysis' / 'BT1554_packetwise_mu_sign_assignment_attempt.md'
TEX = ROOT / 'analysis' / 'BT1554_packetwise_mu_sign_assignment_attempt.tex'


def prof(rows, key):
    return dict(Counter(r[key] for r in rows))


def main() -> None:
    bt1553 = json.loads((ROOT / 'data' / 'bt1553_carrier_to_mixed_triple_projection_scaffold.json').read_text(encoding='utf-8'))
    rows = []
    for r in bt1553['rows']:
        count = r['projected_mixed_triple_count']
        count_parity_mu = 1 if count % 2 == 0 else -1
        balanced_shadow_mu = 1 if r['orientation_slot'] in (0, 2) else -1
        rows.append({
            'carrier_row': r['carrier_row'],
            'a2_axis': r['a2_axis'],
            'orientation_slot': r['orientation_slot'],
            'projected_count': count,
            'count_parity_mu': count_parity_mu,
            'balanced_shadow_mu': balanced_shadow_mu,
        })
    parity_profile = prof(rows, 'count_parity_mu')
    shadow_profile = prof(rows, 'balanced_shadow_mu')
    checks = {
        'bt1553_verified': bt1553.get('verified') is True,
        'rows_24': len(rows) == 24,
        'count_parity_profile_6_plus_18_minus': parity_profile == {1: 6, -1: 18},
        'balanced_shadow_profile_12_12': shadow_profile == {1: 12, -1: 12},
        'parity_not_balanced': parity_profile != shadow_profile,
        'no_actual_mu_artifact_claimed': True,
    }
    result = {
        'bt': 1554,
        'title': 'Packetwise mu-sign assignment attempt',
        'verified': all(checks.values()),
        'source': 'data/bt1553_carrier_to_mixed_triple_projection_scaffold.json',
        'rows': rows,
        'profiles': {'count_parity_mu': {'plus': 6, 'minus': 18}, 'balanced_shadow_mu': {'plus': 12, 'minus': 12}},
        'interpretation': 'The projection count parity gives a nonbalanced 6/18 mu-shadow, while a balanced 12/12 shadow can be imposed by orientation slot. Therefore the 12/12 carrier cannot be said to inherit mu-signs from the projection counts alone; an actual packetwise mu artifact is still required.',
        'honesty_boundary': 'This is a sign-assignment attempt, not a computed Weyl mu transport over the 270 triples.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1554 Packetwise Mu-sign Assignment Attempt\n\nProjection-count parity gives a nonbalanced 6/18 mu-shadow. A balanced 12/12 shadow can be imposed by orientation slot, but it is not inherited from the projection counts. An actual packetwise mu artifact over the 270 triples is still required.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1554: count-parity gives $6/18$, while balanced $12/12$ requires an imposed orientation shadow; packetwise $\\mu$ data remains missing.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt': 1554, 'verified': result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
