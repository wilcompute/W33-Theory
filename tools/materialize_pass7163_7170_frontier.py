#!/usr/bin/env python3
"""Idempotently materialize the Pass7163-7170 public frontier card."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TARGETS=(ROOT/'docs'/'index.html',ROOT/'index.html')
TOKEN='pass-7163-7170-e8-hexagonal-lift'
CARD=(ROOT/'analysis'/'PASS7163_7170_index_insert.html').read_text(encoding='utf-8').rstrip()+'\n'

def place(path:Path)->str:
    marker=f'id="{TOKEN}"'
    text=path.read_text(encoding='utf-8')
    n=text.count(marker)
    if n>1: raise ValueError(f'duplicate {marker} in {path}')
    if n==1:return 'already_materialized'
    low=text.lower();pos=low.rfind('</main>')
    if pos<0:pos=low.rfind('</body>')
    if pos<0:raise ValueError(f'no </main> or </body> in {path}')
    out=text[:pos]+CARD+text[pos:]
    assert out.count(marker)==1
    path.write_text(out,encoding='utf-8')
    return 'inserted'

def main():
    assert CARD.count(f'id="{TOKEN}"')==1
    for target in TARGETS:print(target.relative_to(ROOT),place(target))
    for target in TARGETS:assert target.read_text(encoding='utf-8').count(f'id="{TOKEN}"')==1

if __name__=='__main__':main()
