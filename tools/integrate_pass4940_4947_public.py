#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INDEXES=(ROOT/'docs/index.html',ROOT/'index.html')
CARD=ROOT/'analysis/PASS4940_4947_radius_quartic_holonomy_index_insert.html'
TOKEN='W33_PASS4940_4947_RADIUS_QUARTIC_HOLONOMY_CARD'

def main()->int:
    summaries=[]
    for index in INDEXES:
        raw=index.read_bytes()
        newline=b'\r\n' if raw.count(b'\r\n') > raw.count(b'\n')//2 else b'\n'
        marker=b'</main>' if b'</main>' in raw else b'</body>'
        if marker not in raw:
            raise RuntimeError(f'{index.relative_to(ROOT)} has no safe insertion marker')
        if TOKEN.encode() in raw:
            summaries.append(f'{index.relative_to(ROOT)}: already materialized')
            continue
        card=CARD.read_text().strip().replace('\n',newline.decode()).encode()
        raw=raw.replace(marker,card+newline+marker,1)
        index.write_bytes(raw)
        assert TOKEN.encode() in index.read_bytes()
        summaries.append(f'{index.relative_to(ROOT)}: materialized')
    print(' | '.join(summaries))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
