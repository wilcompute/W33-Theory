#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INDEXES=(ROOT/'docs/index.html',ROOT/'index.html')
CARD=ROOT/'analysis/PASS4984_4991_index_insert.html'
TOKEN='W33_PASS4984_4991_SHELL_DECODER_GAUGE_CARD'
SECTION_ID=b'<section id="pass4984-4991"'
def main()->int:
    summaries=[]
    for index in INDEXES:
        raw=index.read_bytes();newline=b'\r\n' if raw.count(b'\r\n')>raw.count(b'\n')//2 else b'\n'
        marker=b'</main>' if b'</main>' in raw else b'</body>'
        if marker not in raw:raise RuntimeError(f'{index.relative_to(ROOT)} has no safe insertion marker')
        card=CARD.read_text().strip().replace('\n',newline.decode()).encode()
        if TOKEN.encode() in raw:
            start=raw.find(SECTION_ID)
            if start<0:raise RuntimeError(f'{index.relative_to(ROOT)} has token but no section start')
            end=raw.find(b'</section>',start)
            if end<0:raise RuntimeError(f'{index.relative_to(ROOT)} has no section end')
            end+=len(b'</section>');raw=raw[:start]+card+raw[end:];status='refreshed'
        else:
            raw=raw.replace(marker,card+newline+marker,1);status='materialized'
        index.write_bytes(raw);assert raw.count(TOKEN.encode())==1
        summaries.append(f'{index.relative_to(ROOT)}: {status}')
    print(' | '.join(summaries));return 0
if __name__=='__main__':raise SystemExit(main())
