#!/usr/bin/env python3
"""Canonically register Passes 4214-4221 and remove the superseded collided 4213-4220 frontier entry without editing docs/index.html."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/w33_current_frontier_manifest_v1.json'
TEX=ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex'
REQ='analysis/BT4214_BT4221_small_cover_su4_quantum_hysteresis_clock_hawking_pell_vacuum_velocity_insert'
OLDREQ='analysis/BT4213_BT4220_small_cover_su4_quantum_hysteresis_clock_hawking_pell_vacuum_velocity_insert'
CARD={'kind':'id','token':'bt4214-4221-small-cover-su4-hysteresis-clock-hawking-pell-vacuum-velocity','source':'analysis/BT4214_BT4221_small_cover_su4_quantum_hysteresis_clock_hawking_pell_vacuum_velocity_index_insert.html'}
PAGE={'token':'passes-4214-4221-small-cover-su4-hysteresis-clock-hawking-pell-vacuum-velocity','source':'docs/small-cover-su4-hysteresis-clock-hawking-pell-vacuum-velocity-4214-4221.html'}
OLDTOKENS={'bt4213-4220-small-cover-su4-hysteresis-clock-hawking-pell-vacuum-velocity','passes-4213-4220-small-cover-su4-hysteresis-clock-hawking-pell-vacuum-velocity'}
LINE='\\input{analysis/BT4214_BT4221_small_cover_su4_quantum_hysteresis_clock_hawking_pell_vacuum_velocity_insert}%'
OLDLINE='\\input{analysis/BT4213_BT4220_small_cover_su4_quantum_hysteresis_clock_hawking_pell_vacuum_velocity_insert}%'
def key(s):
    m=re.search(r'BT(\d+)',s);return int(m.group(1)) if m else 10**9
def main():
    x=json.loads(PATH.read_text());r=x.setdefault('required_ordered_inputs',[]);s=x.setdefault('public_sections',[]);p=x.setdefault('standalone_public_pages',[])
    r[:]=[z for z in r if z!=OLDREQ]
    if REQ not in r:r.append(REQ)
    r.sort(key=key)
    s[:]=[z for z in s if z.get('token') not in OLDTOKENS]
    p[:]=[z for z in p if z.get('token') not in OLDTOKENS]
    if not any(z.get('token')==CARD['token'] for z in s):s.append(CARD)
    if not any(z.get('token')==PAGE['token'] for z in p):p.append(PAGE)
    PATH.write_text(json.dumps(x,separators=(',',':'))+'\n')
    lines=TEX.read_text().splitlines();head=[z for z in lines if not z.startswith('\\input{analysis/BT')]
    body=[z for z in lines if z.startswith('\\input{analysis/BT') and z not in {LINE,OLDLINE}];body.append(LINE);body.sort(key=key);TEX.write_text('\n'.join(head+body)+'\n')
    print('PASS_4214_4221_FRONTIER',r.count(REQ),OLDREQ in r,sum(z.get('token')==CARD['token'] for z in s),sum(z.get('token')==PAGE['token'] for z in p),body.count(LINE),body.count(OLDLINE))
if __name__=='__main__':main()
