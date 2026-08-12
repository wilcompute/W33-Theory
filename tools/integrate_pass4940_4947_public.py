#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INDEXES=(ROOT/'docs/index.html',ROOT/'index.html')
CARD=ROOT/'analysis/PASS4940_4947_radius_quartic_holonomy_index_insert.html'
TOKEN='W33_PASS4940_4947_RADIUS_QUARTIC_HOLONOMY_CARD'


def rendered_card(newline: bytes) -> bytes:
    return CARD.read_text().strip().replace('\n',newline.decode()).encode()


def replace_or_insert(raw: bytes, card: bytes) -> tuple[bytes,str]:
    token=TOKEN.encode()
    if token in raw:
        comment=b'<!-- '+token+b' -->'
        start=raw.find(comment)
        if start < 0:
            raise RuntimeError('token found without canonical comment marker')
        section_start=raw.find(b'<section',start)
        section_end=raw.find(b'</section>',section_start)
        if section_start < 0 or section_end < 0:
            raise RuntimeError('existing theorem card has no safe section boundary')
        end=section_end+len(b'</section>')
        current=raw[start:end]
        if current==card:
            return raw,'already current'
        return raw[:start]+card+raw[end:],'refreshed'

    marker=b'</main>' if b'</main>' in raw else b'</body>'
    if marker not in raw:
        raise RuntimeError('index has no safe insertion marker')
    return raw.replace(marker,card+b'\n'+marker,1),'materialized'


def main()->int:
    summaries=[]
    for index in INDEXES:
        raw=index.read_bytes()
        newline=b'\r\n' if raw.count(b'\r\n') > raw.count(b'\n')//2 else b'\n'
        card=rendered_card(newline)
        updated,status=replace_or_insert(raw,card)
        if updated!=raw:
            index.write_bytes(updated)
        assert TOKEN.encode() in index.read_bytes()
        summaries.append(f'{index.relative_to(ROOT)}: {status}')
    print(' | '.join(summaries))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
