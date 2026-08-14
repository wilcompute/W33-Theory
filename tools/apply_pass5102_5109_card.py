#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CARD=(ROOT/'analysis'/'PASS5102_5109_index_insert.html').read_text().strip()
for rel in ('index.html','docs/index.html'):
    p=ROOT/rel
    if not p.exists():continue
    s=p.read_text()
    if 'id="pass5102-5109"' in s:continue
    if '</body>' not in s:raise SystemExit(f'missing </body> in {rel}')
    p.write_text(s.replace('</body>',CARD+'\n</body>',1));print('updated',rel)
