#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/w33_current_frontier_manifest_v1.json'
TEX=ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex'
REQ='analysis/BT4253_BT4260_girth16_faultaware_su4_hysteresis_clock_channel_scrambling_modular_capacity_insert'
CARD={'kind':'id','token':'bt4253-4260-girth16-faultaware-holonomy','source':'analysis/BT4253_BT4260_girth16_faultaware_su4_hysteresis_clock_channel_scrambling_modular_capacity_index_insert.html'}
PAGE={'token':'passes-4253-4260-girth16-faultaware-holonomy','source':'docs/girth16-faultaware-holonomy-hysteresis-clock-channel-4253-4260.html'}
LINE='\\input{analysis/BT4253_BT4260_girth16_faultaware_su4_hysteresis_clock_channel_scrambling_modular_capacity_insert}%'
def key(s):
    m=re.search(r'BT(\d+)',s);return int(m.group(1)) if m else 10**9

def main():
    x=json.loads(PATH.read_text());r=x.setdefault('required_ordered_inputs',[]);s=x.setdefault('public_sections',[]);p=x.setdefault('standalone_public_pages',[])
    if REQ not in r:r.append(REQ)
    r.sort(key=key)
    if not any(y.get('token')==CARD['token'] for y in s):s.append(CARD)
    if not any(y.get('token')==PAGE['token'] for y in p):p.append(PAGE)
    PATH.write_text(json.dumps(x,separators=(',',':'))+'\n')
    lines=TEX.read_text().splitlines();head=[z for z in lines if not z.startswith('\\input{analysis/BT')];body=[z for z in lines if z.startswith('\\input{analysis/BT') and z!=LINE];body.append(LINE);body.sort(key=key);TEX.write_text('\n'.join(head+body)+'\n')
    print('PASS_4253_4260_FRONTIER',r.count(REQ),sum(y.get('token')==CARD['token'] for y in s),sum(y.get('token')==PAGE['token'] for y in p),body.count(LINE))
if __name__=='__main__':main()
