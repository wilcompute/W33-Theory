#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INDEXES=(ROOT/'docs/index.html',ROOT/'index.html')
CARDS=[
    (ROOT/'analysis/PASS4865_4872_ternary_clique_cut_index_insert.html','W33_PASS4865_4872_TERNARY_CLIQUE_CUT_CARD'),
    (ROOT/'analysis/PASS4870_steiner_w33_quadratic_index_insert.html','W33_PASS4870_STEINER_W33_QUADRATIC_CARD'),
]

def main()->int:
    summaries=[]
    for index in INDEXES:
        raw=index.read_bytes()
        newline=b'\r\n' if raw.count(b'\r\n') > raw.count(b'\n')//2 else b'\n'
        marker=b'</main>' if b'</main>' in raw else b'</body>'
        if marker not in raw:
            raise RuntimeError(f'{index.relative_to(ROOT)} has no safe insertion marker')
        inserted=[]
        for path,token in CARDS:
            token_bytes=token.encode()
            if token_bytes in raw:
                continue
            card=path.read_text().strip().replace('\n',newline.decode()).encode()
            raw=raw.replace(marker,card+newline+marker,1)
            inserted.append(token)
        index.write_bytes(raw)
        for _,token in CARDS:
            assert token.encode() in raw
        summaries.append(f'{index.relative_to(ROOT)}: '+
                         (', '.join(inserted) if inserted else 'already materialized'))
    print(' | '.join(summaries))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
