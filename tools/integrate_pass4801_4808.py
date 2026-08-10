#!/usr/bin/env python3
"""Idempotently materialize the Passes 4801--4808 theorem card into docs/index.html."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'docs/index.html'
CARD=ROOT/'analysis/PASS4801_4808_radius_golay_homology_index_insert.html'
TOKEN='id="pass4801-4808-radius-golay-homology"'

def main():
    text=INDEX.read_text(encoding='utf-8');n=text.count(TOKEN)
    if n>1:raise RuntimeError('duplicate Pass4801-4808 card')
    if n==0:
        pos=text.lower().rfind('</main>')
        if pos<0:pos=text.lower().rfind('</body>')
        if pos<0:raise RuntimeError('no insertion point in docs/index.html')
        text=text[:pos]+CARD.read_text(encoding='utf-8').rstrip()+'\n'+text[pos:]
        INDEX.write_text(text,encoding='utf-8')
    assert INDEX.read_text(encoding='utf-8').count(TOKEN)==1
    print('PASS','already_materialized' if n else 'inserted',TOKEN)
    return 0
if __name__=='__main__':raise SystemExit(main())
