#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parents[1]
card=(R/'analysis/PASS5074_5081_index_insert.html').read_text().strip()
for rel in ('index.html','docs/index.html'):
    p=R/rel
    if not p.exists(): continue
    s=p.read_text()
    if 'id="pass5074-5081"' in s: continue
    marker='</body>'
    if marker in s:s=s.replace(marker,card+'\n'+marker,1)
    else:s+='\n'+card+'\n'
    p.write_text(s)
    print('updated',rel)
