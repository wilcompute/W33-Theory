#!/usr/bin/env python3
"""Idempotently register Passes 4113-4120 without editing docs/index.html directly."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/w33_current_frontier_manifest_v1.json'
TEX=ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex'
REQ='analysis/BT4113_BT4120_gauge_horizon_dimension_scar_curvature_insert'
CARD={'kind':'id','token':'bt4113-4120-gauge-horizon-dimension-scar-curvature','source':'analysis/BT4113_BT4120_gauge_horizon_dimension_scar_curvature_index_insert.html'}
PAGE={'token':'passes-4113-4120-gauge-horizon-dimension-scar-curvature','source':'docs/gauge-horizon-dimension-scar-curvature-4113-4120.html'}
LINE='\\input{analysis/BT4113_BT4120_gauge_horizon_dimension_scar_curvature_insert}%'
def main():
    x=json.loads(PATH.read_text())
    r=x.setdefault('required_ordered_inputs',[])
    s=x.setdefault('public_sections',[])
    p=x.setdefault('standalone_public_pages',[])
    if REQ not in r:r.append(REQ)
    if not any(y.get('token')==CARD['token'] for y in s):s.append(CARD)
    if not any(y.get('token')==PAGE['token'] for y in p):p.append(PAGE)
    PATH.write_text(json.dumps(x,separators=(',',':'))+'\n')
    lines=TEX.read_text().splitlines()
    lines=[z for z in lines if z!=LINE]
    lines.append(LINE)
    TEX.write_text('\n'.join(lines)+'\n')
    print('PASS_4113_4120_FRONTIER',r.count(REQ),sum(y.get('token')==CARD['token'] for y in s),sum(y.get('token')==PAGE['token'] for y in p),lines.count(LINE))
if __name__=='__main__':main()
