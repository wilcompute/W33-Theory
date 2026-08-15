#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parents[1]
card=(R/'analysis/PASS5292_5299_index_insert.html').read_text().strip()
for p in (R/'index.html',R/'docs/index.html'):
    s=p.read_text()
    if 'id="pass5292-5299"' not in s:
        s=s.replace('</body>',card+'\n</body>') if '</body>' in s else s+'\n'+card+'\n'
        p.write_text(s)
