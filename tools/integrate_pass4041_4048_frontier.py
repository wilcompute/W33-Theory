#!/usr/bin/env python3
"""Idempotently register Passes 4041-4048 in the protected frontier."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/w33_current_frontier_manifest_v1.json'
REQ='analysis/BT4041_BT4048_eight_physics_expansion_insert'
CARD={'kind':'id','token':'bt4041-4048-eight-physics-expansion','source':'analysis/BT4041_BT4048_eight_physics_expansion_index_insert.html'}
PAGE={'token':'passes-4041-4048-eight-physics-expansion','source':'docs/eight-physics-expansion.html'}

def main():
    x=json.loads(PATH.read_text())
    r=x.setdefault('required_ordered_inputs',[])
    s=x.setdefault('public_sections',[])
    p=x.setdefault('standalone_public_pages',[])
    if REQ not in r:r.append(REQ)
    if not any(y.get('token')==CARD['token'] for y in s):s.append(CARD)
    if not any(y.get('token')==PAGE['token'] for y in p):p.append(PAGE)
    PATH.write_text(json.dumps(x,separators=(',',':'))+'\n')
    print('PASS_4041_4048_FRONTIER',r.count(REQ),sum(y.get('token')==CARD['token'] for y in s),sum(y.get('token')==PAGE['token'] for y in p))

if __name__=='__main__':main()
