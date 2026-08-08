#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/w33_current_frontier_manifest_v1.json'
TEX=ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex'
PACKETS=[
 {
  'req':'analysis/BT4253_BT4260_girth16_faultaware_su4_hysteresis_clock_channel_scrambling_modular_capacity_insert',
  'line':'\\input{analysis/BT4253_BT4260_girth16_faultaware_su4_hysteresis_clock_channel_scrambling_modular_capacity_insert}%',
  'card':{'kind':'id','token':'bt4253-4260-girth16-faultaware-holonomy','source':'analysis/BT4253_BT4260_girth16_faultaware_su4_hysteresis_clock_channel_scrambling_modular_capacity_index_insert.html'},
  'page':{'token':'passes-4253-4260-girth16-faultaware-holonomy','source':'docs/girth16-faultaware-holonomy-hysteresis-clock-channel-4253-4260.html'}
 },
 {
  'req':'analysis/BT4261_BT4268_girth18_cd_hysteresis_clock37_nongaussian_search_defect_thermal_insert',
  'line':'\\input{analysis/BT4261_BT4268_girth18_cd_hysteresis_clock37_nongaussian_search_defect_thermal_insert}%',
  'card':{'kind':'id','token':'bt4261-4268-girth18-cd-hysteresis-clock37-nongaussian','source':'analysis/BT4261_BT4268_girth18_cd_hysteresis_clock37_nongaussian_search_defect_thermal_index_insert.html'},
  'page':{'token':'passes-4261-4268-girth18-cd-hysteresis-clock37-nongaussian','source':'docs/girth18-cd-hysteresis-clock37-nongaussian-search-defect-thermal-4261-4268.html'}
 }
]
def key(s):
    m=re.search(r'BT(\d+)',s);return int(m.group(1)) if m else 10**9

def main():
    x=json.loads(PATH.read_text());r=x.setdefault('required_ordered_inputs',[]);s=x.setdefault('public_sections',[]);p=x.setdefault('standalone_public_pages',[])
    for z in PACKETS:
        if z['req'] not in r:r.append(z['req'])
        if not any(y.get('token')==z['card']['token'] for y in s):s.append(z['card'])
        if not any(y.get('token')==z['page']['token'] for y in p):p.append(z['page'])
    r.sort(key=key);PATH.write_text(json.dumps(x,separators=(',',':'))+'\n')
    lines=TEX.read_text().splitlines();head=[z for z in lines if not z.startswith('\\input{analysis/BT')];owned={z['line'] for z in PACKETS};body=[z for z in lines if z.startswith('\\input{analysis/BT') and z not in owned];body.extend(z['line'] for z in PACKETS);body.sort(key=key);TEX.write_text('\n'.join(head+body)+'\n')
    counts=[r.count(z['req']) for z in PACKETS];cards=[sum(y.get('token')==z['card']['token'] for y in s) for z in PACKETS];pages=[sum(y.get('token')==z['page']['token'] for y in p) for z in PACKETS];theorems=[body.count(z['line']) for z in PACKETS]
    print('PASS_4261_4268_FRONTIER',counts,cards,pages,theorems)
if __name__=='__main__':main()
