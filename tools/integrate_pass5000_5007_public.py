#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INDEXES=(ROOT/'docs/index.html',ROOT/'index.html')
CARD=ROOT/'analysis/PASS5000_5007_index_insert.html'
TOKEN=b'W33_PASS5000_5007_KERNEL_COCIRCUIT_TORSOR_CARD'
SECTION=b'<section id="pass5000-5007"'

def main()->int:
    card_text=CARD.read_text(encoding='utf-8').strip();status=[]
    for path in INDEXES:
        raw=path.read_bytes();nl=b'\r\n' if raw.count(b'\r\n')>raw.count(b'\n')//2 else b'\n'
        card=card_text.replace('\n',nl.decode()).encode();marker=b'</main>' if b'</main>' in raw else b'</body>'
        if marker not in raw:raise RuntimeError(f'{path.relative_to(ROOT)} has no safe insertion marker')
        if TOKEN in raw:
            start=raw.find(SECTION)
            if start<0:raise RuntimeError(f'{path.relative_to(ROOT)} has token but no section')
            end=raw.find(b'</section>',start)
            if end<0:raise RuntimeError(f'{path.relative_to(ROOT)} has no section end')
            end+=len(b'</section>');raw=raw[:start]+card+raw[end:];state='refreshed'
        else:
            raw=raw.replace(marker,card+nl+marker,1);state='materialized'
        path.write_bytes(raw);assert raw.count(TOKEN)==1;status.append(f'{path.relative_to(ROOT)}:{state}')
    print(' | '.join(status));return 0
if __name__=='__main__':raise SystemExit(main())
