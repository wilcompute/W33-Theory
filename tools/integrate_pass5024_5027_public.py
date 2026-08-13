#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parents[1]
card='<section id="pass5024-5027"><h2>Passes 5024-5027: cover-Levi bridge</h2><p>Exact finite graph continuation.</p></section>'
for p in (R/'docs/index.html',R/'index.html'):
    s=p.read_text()
    if 'pass5024-5027' not in s:
        s=s.replace('</body>',card+'\n</body>',1)
    p.write_text(s)
