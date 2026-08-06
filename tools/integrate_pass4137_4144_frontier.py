#!/usr/bin/env python3
"""Register Passes 4137-4144 without editing docs/index.html and preserve pass order."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/w33_current_frontier_manifest_v1.json'
TEX=ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex'
REQ='analysis/BT4137_BT4144_matrix_horizon_rg_scar_curvature_insert'
LINE='\\input{analysis/BT4137_BT4144_matrix_horizon_rg_scar_curvature_insert}%'
CARD={'kind':'id','token':'bt4137-4144-matrix-horizon-rg-scar-curvature','source':'analysis/BT4137_BT4144_matrix_horizon_rg_scar_curvature_index_insert.html'}
PAGE={'token':'passes-4137-4144-matrix-horizon-rg-scar-curvature','source':'docs/matrix-horizon-rg-scar-curvature-4137-4144.html'}
def ordered_insert(items,item):
    items=[x for x in items if x!=item]
    anchors=[i for i,x in enumerate(items) if re.search(r'BT4129_BT4136_',x)]
    if not anchors: anchors=[i for i,x in enumerate(items) if re.search(r'BT4121_BT4128_',x)]
    items.insert((max(anchors)+1) if anchors else len(items),item)
    return items
def main():
    x=json.loads(PATH.read_text())
    x['required_ordered_inputs']=ordered_insert(x.setdefault('required_ordered_inputs',[]),REQ)
    s=x.setdefault('public_sections',[]);p=x.setdefault('standalone_public_pages',[])
    if not any(y.get('token')==CARD['token'] for y in s):s.append(CARD)
    if not any(y.get('token')==PAGE['token'] for y in p):p.append(PAGE)
    PATH.write_text(json.dumps(x,separators=(',',':'))+'\n')
    lines=TEX.read_text().splitlines();lines=ordered_insert(lines,LINE);TEX.write_text('\n'.join(lines)+'\n')
    ri=x['required_ordered_inputs'].index(REQ);li=lines.index(LINE)
    print('PASS_4137_4144_FRONTIER',x['required_ordered_inputs'].count(REQ),sum(y.get('token')==CARD['token'] for y in s),sum(y.get('token')==PAGE['token'] for y in p),lines.count(LINE),ri,li)
if __name__=='__main__':main()
