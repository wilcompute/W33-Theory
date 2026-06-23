#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1559_holonet_splice_update_mixed_self_qutrit.json'
MD = ROOT / 'analysis' / 'BT1559_holonet_splice_update_mixed_self_qutrit.md'
TEX = ROOT / 'analysis' / 'BT1559_holonet_splice_update_mixed_self_qutrit.tex'

INSERTS = [
    'analysis/BT1550_BT1552_holonet_insert.tex',
    'analysis/BT1553_BT1556_holonet_insert.tex',
]
ROWS = [
    {'tier':'structural','claim':'self-entangled qutrit reinterpretation of two-qutrit W33','support':'BT1556'},
    {'tier':'structural','claim':'temporal Choi line to A2 sector-fiber pairs','support':'BT1557'},
    {'tier':'schema','claim':'past/future Choi mu transport schema','support':'BT1558'},
    {'tier':'obstructed','claim':'uniform 270-to-24 mixed-triple projection','support':'BT1553'},
    {'tier':'obstructed','claim':'pair product on 24-row carrier without extra degrees','support':'BT1555'},
]


def main() -> None:
    checks = {
        'two_inserts': len(INSERTS) == 2,
        'all_inserts_exist': all((ROOT / p).exists() for p in INSERTS),
        'five_claim_rows': len(ROWS) == 5,
        'self_qutrit_structural': any(r['support'] == 'BT1556' and r['tier'] == 'structural' for r in ROWS),
        'mu_transport_schema': any(r['support'] == 'BT1558' and r['tier'] == 'schema' for r in ROWS),
        'obstructions_preserved': sum(1 for r in ROWS if r['tier'] == 'obstructed') == 2,
    }
    result = {
        'bt': 1559,
        'title': 'Holonet splice update for mixed projection/self-qutrit packet',
        'verified': all(checks.values()),
        'inserts': INSERTS,
        'claim_rows': ROWS,
        'interpretation': 'BT1553-BT1558 are packaged for the Magic Star/E6 appendix and release firewall: self-entangled qutrit and temporal Choi/A2 map are structural; mu transport is schema; projection/product limitations remain obstructed.',
        'honesty_boundary': 'Splice/firewall update only; no TeX rewrite or PDF build is claimed.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1559 Holonet Splice Update\n\nBT1553-BT1558 are packaged for the Magic Star/E6 appendix and release firewall. Self-entangled qutrit and temporal Choi/A2 map are structural. Mu transport is schema. Uniform projection and pair product remain obstructed. No paper rewrite or PDF build is claimed.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1559: BT1553--BT1558 enter the appendix/firewall; self-qutrit reading is structural, $\\mu$ transport is schema, projection/product layers remain obstructed.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt': 1559, 'verified': result['verified']}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
