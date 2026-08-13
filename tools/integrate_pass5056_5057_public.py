#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parents[1]
C=(R/'analysis/PASS5056_5057_index_insert.html').read_text().strip()
T='pass5056-5057'
for p in (R/'docs/index.html',R/'index.html'):
    s=p.read_text()
    if T not in s:
        s=s.replace('</main>',C+'\n</main>',1) if '</main>' in s else s.replace('</body>',C+'\n</body>',1)
        p.write_text(s)
