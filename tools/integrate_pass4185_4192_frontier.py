#!/usr/bin/env python3
"""Idempotently register Passes 4185-4192 without editing docs/index.html."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/w33_current_frontier_manifest_v1.json'
TEX=ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex'
REQ='analysis/BT4185_BT4192_adaptive_c2_hawking_hysteresis_3local_cover_holonomy_ihara_heat_insert'
CARD={'kind':'id','token':'bt4185-4192-adaptive-c2-hawking-hysteresis-3local-cover','source':'analysis/BT4185_BT4192_adaptive_c2_hawking_hysteresis_3local_cover_holonomy_ihara_heat_index_insert.html'}
PAGE={'token':'passes-4185-4192-adaptive-c2-hawking-hysteresis-3local-cover','source':'docs/adaptive-c2-hawking-hysteresis-3local-cover-holonomy-ihara-heat-4185-4192.html'}
LINE='\\input{analysis/BT4185_BT4192_adaptive_c2_hawking_hysteresis_3local_cover_holonomy_ihara_heat_insert}%'
def key(s):
    m=re.search(r'BT(\d+)',s); return int(m.group(1)) if m else 10**9

def main():
    x=json.loads(PATH.read_text())
    r=x.setdefault('required_ordered_inputs',[]); s=x.setdefault('public_sections',[]); p=x.setdefault('standalone_public_pages',[])
    if REQ not in r:r.append(REQ)
    r.sort(key=key)
    if not any(y.get('token')==CARD['token'] for y in s):s.append(CARD)
    if not any(y.get('token')==PAGE['token'] for y in p):p.append(PAGE)
    PATH.write_text(json.dumps(x,separators=(',',':'))+'\n')
    lines=TEX.read_text().splitlines(); head=[z for z in lines if not z.startswith('\\input{analysis/BT')]
    body=[z for z in lines if z.startswith('\\input{analysis/BT') and z!=LINE]; body.append(LINE); body.sort(key=key)
    TEX.write_text('\n'.join(head+body)+'\n')
    print('PASS_4185_4192_FRONTIER',r.count(REQ),sum(y.get('token')==CARD['token'] for y in s),sum(y.get('token')==PAGE['token'] for y in p),body.count(LINE))
if __name__=='__main__': main()
