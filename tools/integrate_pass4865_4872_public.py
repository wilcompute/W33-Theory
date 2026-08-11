#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'docs/index.html'
CARDS=[
    (ROOT/'analysis/PASS4865_4872_ternary_clique_cut_index_insert.html','W33_PASS4865_4872_TERNARY_CLIQUE_CUT_CARD'),
    (ROOT/'analysis/PASS4870_steiner_w33_quadratic_index_insert.html','W33_PASS4870_STEINER_W33_QUADRATIC_CARD'),
]

def main()->int:
    text=INDEX.read_text()
    marker='</main>' if '</main>' in text else '</body>'
    if marker not in text:
        raise RuntimeError('docs/index.html has no safe insertion marker')
    inserted=[]
    for path,token in CARDS:
        if token in text:
            continue
        card=path.read_text().strip()
        text=text.replace(marker,card+'\n'+marker,1)
        inserted.append(token)
    INDEX.write_text(text)
    final=INDEX.read_text()
    for _,token in CARDS:
        assert token in final
    if inserted:
        print('materialized public cards: '+', '.join(inserted))
    else:
        print('Pass4865-4872 / Pass4870 public cards already materialized')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
