#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parents[1]
card=(R/'analysis/PASS5044_5051_index_insert.html').read_text()
for p in (R/'docs/index.html',R/'index.html'):
 s=p.read_text()
 if 'pass5044-5051' not in s:s=s.replace('</body>',card+'\n</body>',1)
 p.write_text(s)
