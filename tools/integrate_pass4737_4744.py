#!/usr/bin/env python3
"""Idempotently materialize the Passes 4737--4744 theorem card into docs/index.html."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'docs/index.html'
SOURCE=ROOT/'analysis/PASS4737_4744_residue_router_breakthrough_index_insert.html'
TOKEN='id="pass4737-4744-residue-router-breakthrough"'

def main():
    text=INDEX.read_text(encoding='utf-8');n=text.count(TOKEN)
    if n>1:raise RuntimeError(f'duplicate theorem card: {TOKEN}')
    if n==0:
        html=SOURCE.read_text(encoding='utf-8').rstrip()+'\n';low=text.lower();pos=low.rfind('</main>')
        if pos<0:pos=low.rfind('</body>')
        if pos<0:raise RuntimeError('docs/index.html has no </main> or </body> insertion point')
        text=text[:pos]+html+text[pos:];INDEX.write_text(text,encoding='utf-8')
        mode='inserted'
    else:mode='already_materialized'
    assert INDEX.read_text(encoding='utf-8').count(TOKEN)==1
    print(f'PASS {TOKEN}: {mode}');return 0
if __name__=='__main__':raise SystemExit(main())
