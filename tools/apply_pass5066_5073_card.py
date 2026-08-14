#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parents[1]
card=(R/'analysis/PASS5066_5073_index_insert.html').read_text().strip()
marker='id="pass5066-5073"'
for rel in ('docs/index.html','index.html'):
    p=R/rel
    if not p.exists():continue
    s=p.read_text()
    if marker in s:continue
    pos=s.lower().rfind('</body>')
    if pos<0:pos=len(s)
    p.write_text(s[:pos]+'\n'+card+'\n'+s[pos:])
    print('updated',rel)
