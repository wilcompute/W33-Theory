#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parents[1]
card=(R/'analysis/PASS5052_5059_index_insert.html').read_text().strip()
for p in (R/'index.html',R/'docs/index.html'):
 s=p.read_text()
 if 'id="pass5052-5059"' not in s:
  s=s.replace('</body>',card+'\n</body>')
  p.write_text(s)
