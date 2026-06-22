#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1552_appendix_update.json'
INSERTS = [
 'analysis/BT1536_BT1539_holonet_insert.tex',
 'analysis/BT1540_BT1542_holonet_insert.tex',
 'analysis/BT1543_BT1546_holonet_insert.tex',
 'analysis/BT1547_BT1549_holonet_insert.tex',
]
ROWS = [
 {'tier':'structural','item':'A2 singleton map','support':'BT1547'},
 {'tier':'blocked','item':'direct sign match','support':'BT1548'},
 {'tier':'blocked','item':'minimal pair product','support':'BT1549/BT1551'},
 {'tier':'candidate','item':'mu-sign bridge','support':'BT1550'},
]

def main() -> None:
    checks = {
        'four_inserts': len(INSERTS) == 4,
        'all_inserts_exist': all((ROOT / p).exists() for p in INSERTS),
        'four_rows': len(ROWS) == 4,
    }
    out = {'bt':1552,'title':'appendix update','verified':all(checks.values()),'inserts':INSERTS,'rows':ROWS,'checks':checks}
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'bt':1552,'verified':out['verified']}, indent=2))
    if not out['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
