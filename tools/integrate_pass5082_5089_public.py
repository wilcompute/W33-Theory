#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parents[1]
card=(R/'analysis/PASS5082_5089_index_insert.html').read_text().strip()
for p in (R/'index.html',R/'docs/index.html'):
    s=p.read_text()
    if 'id="pass5082-5089"' not in s:
        if '</body>' in s:s=s.replace('</body>',card+'\n</body>')
        else:s=s+'\n'+card+'\n'
        p.write_text(s)
