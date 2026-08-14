#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parents[1];card=(R/'analysis/PASS5090_5097_index_insert.html').read_text().strip()
for rel in ('index.html','docs/index.html'):
 p=R/rel
 if not p.exists():continue
 s=p.read_text()
 if 'id="pass5090-5097"' in s:continue
 s=s.replace('</body>',card+'\n</body>',1) if '</body>' in s else s+'\n'+card+'\n'
 p.write_text(s);print('updated',rel)
