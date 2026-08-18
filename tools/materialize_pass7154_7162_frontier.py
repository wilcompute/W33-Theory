#!/usr/bin/env python3
"""Idempotently materialize the Pass7154-7162 audited E8 frontier card."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TARGETS=(ROOT/'docs'/'index.html',ROOT/'index.html')
TOKEN='pass-7154-7162-e8-audit'
CARD=(ROOT/'analysis'/'PASS7154_7162_index_insert.html').read_text(encoding='utf-8').rstrip()+'\n'

def place(path:Path)->str:
    marker=f'id="{TOKEN}"'; text=path.read_text(encoding='utf-8'); n=text.count(marker)
    if n>1: raise ValueError(f'duplicate {marker} in {path}')
    if n==1: return 'already_materialized'
    low=text.lower(); pos=low.rfind('</main>')
    if pos<0: pos=low.rfind('</body>')
    if pos<0: raise ValueError(f'no </main> or </body> in {path}')
    out=text[:pos]+CARD+text[pos:]
    assert out.count(marker)==1
    path.write_text(out,encoding='utf-8'); return 'inserted'

def main():
    assert CARD.count(f'id="{TOKEN}"')==1
    for t in TARGETS: print(t.relative_to(ROOT),place(t))
    for t in TARGETS: assert t.read_text(encoding='utf-8').count(f'id="{TOKEN}"')==1
if __name__=='__main__': main()
