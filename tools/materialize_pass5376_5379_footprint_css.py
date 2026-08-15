#!/usr/bin/env python3
"""Materialize the Pass5376--5379 footprint/CSS theorem card into both index mirrors."""
from __future__ import annotations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TARGETS=(ROOT/'docs/index.html',ROOT/'index.html')
SOURCE=ROOT/'analysis/PASS5376_5379_allodd_footprint_rank_css_index_insert.html'
TOKEN='id="pass-5376-5379-allodd-footprint-css"'

def materialize(path:Path,html:str)->str:
    text=path.read_text(encoding='utf-8')
    count=text.count(TOKEN)
    if count==1:return 'already_materialized'
    if count>1:raise ValueError(f'duplicate Pass5376-5379 card in {path}')
    lower=text.lower();pos=lower.rfind('</main>')
    if pos<0:pos=lower.rfind('</body>')
    if pos<0:raise ValueError(f'{path} has no </main> or </body> insertion point')
    updated=text[:pos]+html+text[pos:]
    assert updated.count(TOKEN)==1
    path.write_text(updated,encoding='utf-8')
    return 'inserted'

def main()->None:
    html=SOURCE.read_text(encoding='utf-8').rstrip()+'\n'
    left,right=(p.read_text(encoding='utf-8') for p in TARGETS)
    if TOKEN not in left and TOKEN not in right and left!=right:
        raise ValueError('root and docs index mirrors diverged before footprint/CSS materialization')
    for p in TARGETS:
        print(f'PASS {p.relative_to(ROOT)}: {materialize(p,html)}')
    assert TARGETS[0].read_text(encoding='utf-8')==TARGETS[1].read_text(encoding='utf-8')

if __name__=='__main__':main()
