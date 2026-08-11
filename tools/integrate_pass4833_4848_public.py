#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'docs/index.html';CARD=ROOT/'analysis/PASS4833_4848_code_cycle_index_insert.html'
TOKEN='W33_PASS4833_4848_CODE_CYCLE_CARD'
def main()->int:
    text=INDEX.read_text();card=CARD.read_text().strip()
    if TOKEN in text:
        print('Pass4833-4848 card already materialized');return 0
    marker='</main>' if '</main>' in text else '</body>'
    if marker not in text:raise RuntimeError('docs/index.html has no safe insertion marker')
    text=text.replace(marker,card+'\n'+marker,1)
    INDEX.write_text(text)
    assert TOKEN in INDEX.read_text()
    print('materialized Pass4833-4848 public theorem card')
    return 0
if __name__=='__main__':raise SystemExit(main())
