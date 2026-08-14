#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CARD=(ROOT/'analysis'/'PASS5090_5097_index_insert.html').read_text().strip()
for rel in ('index.html','docs/index.html'):
    p=ROOT/rel
    if not p.exists():continue
    s=p.read_text()
    if 'id="pass5090-5097"' in s:continue
    marker='</body>'
    if marker not in s:raise SystemExit(f'missing </body> in {rel}')
    p.write_text(s.replace(marker,CARD+'\n'+marker,1))
    print('updated',rel)
