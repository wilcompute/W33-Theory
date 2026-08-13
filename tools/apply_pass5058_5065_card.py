#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parents[1]
card=(R/'analysis/PASS5058_5065_index_insert.html').read_text().strip()
for p in (R/'index.html',R/'docs/index.html'):
 s=p.read_text()
 if 'id="pass5058-5065"' not in s:
  p.write_text(s.replace('</body>',card+'\n</body>'))
