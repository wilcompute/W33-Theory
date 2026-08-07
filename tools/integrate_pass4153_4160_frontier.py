#!/usr/bin/env python3
"""Idempotently register Passes 4153-4160 without editing docs/index.html."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/w33_current_frontier_manifest_v1.json'
TEX=ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex'
REQ='analysis/BT4153_BT4160_second_chern_disorder_lindblad_clock_thermo_insert'
CARD={'kind':'id','token':'bt4153-4160-second-chern-disorder-lindblad-clock-thermo','source':'analysis/BT4153_BT4160_second_chern_disorder_lindblad_clock_thermo_index_insert.html'}
PAGE={'token':'passes-4153-4160-second-chern-disorder-lindblad-clock-thermo','source':'docs/second-chern-disorder-lindblad-clock-thermo-4153-4160.html'}
LINE='\\input{analysis/BT4153_BT4160_second_chern_disorder_lindblad_clock_thermo_insert}%'
def key(s):
    m=re.search(r'BT(\d+)',s);return int(m.group(1)) if m else 10**9

def main():
    x=json.loads(PATH.read_text())
    r=x.setdefault('required_ordered_inputs',[]);s=x.setdefault('public_sections',[]);p=x.setdefault('standalone_public_pages',[])
    if REQ not in r:r.append(REQ)
    r.sort(key=key)
    if not any(y.get('token')==CARD['token'] for y in s):s.append(CARD)
    if not any(y.get('token')==PAGE['token'] for y in p):p.append(PAGE)
    PATH.write_text(json.dumps(x,separators=(',',':'))+'\n')
    lines=TEX.read_text().splitlines();head=[z for z in lines if not z.startswith('\\input{analysis/BT')]
    body=[z for z in lines if z.startswith('\\input{analysis/BT') and z!=LINE];body.append(LINE);body.sort(key=key)
    TEX.write_text('\n'.join(head+body)+'\n')
    print('PASS_4153_4160_FRONTIER',r.count(REQ),sum(y.get('token')==CARD['token'] for y in s),sum(y.get('token')==PAGE['token'] for y in p),body.count(LINE))
if __name__=='__main__':main()
