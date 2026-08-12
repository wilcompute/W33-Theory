#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INDEXES=(ROOT/'docs/index.html',ROOT/'index.html')
CARDS=[
    (ROOT/'analysis/PASS4865_4872_ternary_clique_cut_index_insert.html','W33_PASS4865_4872_TERNARY_CLIQUE_CUT_CARD'),
    (ROOT/'analysis/PASS4870_steiner_w33_quadratic_index_insert.html','W33_PASS4870_STEINER_W33_QUADRATIC_CARD'),
]


def render(path: Path, newline: bytes) -> bytes:
    return path.read_text().strip().replace('\n',newline.decode()).encode()


def replace_or_insert(raw: bytes, card: bytes, token: str, marker: bytes) -> tuple[bytes,str]:
    token_b=token.encode()
    if token_b in raw:
        comment=b'<!-- '+token_b+b' -->'
        start=raw.find(comment)
        if start < 0:
            raise RuntimeError(f'{token}: token found without canonical comment marker')
        section_start=raw.find(b'<section',start)
        section_end=raw.find(b'</section>',section_start)
        if section_start < 0 or section_end < 0:
            raise RuntimeError(f'{token}: existing card has no safe section boundary')
        end=section_end+len(b'</section>')
        current=raw[start:end]
        if current==card:
            return raw,'already current'
        return raw[:start]+card+raw[end:],'refreshed'
    return raw.replace(marker,card+b'\n'+marker,1),'materialized'


def main()->int:
    summaries=[]
    for index in INDEXES:
        raw=index.read_bytes()
        newline=b'\r\n' if raw.count(b'\r\n') > raw.count(b'\n')//2 else b'\n'
        marker=b'</main>' if b'</main>' in raw else b'</body>'
        if marker not in raw:
            raise RuntimeError(f'{index.relative_to(ROOT)} has no safe insertion marker')
        statuses=[]
        for path,token in CARDS:
            raw,status=replace_or_insert(raw,render(path,newline),token,marker)
            statuses.append(f'{token}: {status}')
        index.write_bytes(raw)
        for _,token in CARDS:
            assert token.encode() in raw
        summaries.append(f'{index.relative_to(ROOT)}: '+', '.join(statuses))
    print(' | '.join(summaries))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
