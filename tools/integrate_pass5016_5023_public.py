#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parents[1];C=(R/'analysis/PASS5016_5023_index_insert.html').read_text().strip();T='W33_PASS5016_5023_RP2_V60_CUBE81_CARD'
for p in (R/'docs/index.html',R/'index.html'):
 s=p.read_text()
 if T not in s:s=s.replace('</main>',C+'\n</main>',1) if '</main>' in s else s.replace('</body>',C+'\n</body>',1)
 p.write_text(s)
