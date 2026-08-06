#!/usr/bin/env python3
"""Idempotently register Passes 3981-3988 without modifying protected docs/index.html."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'data/w33_current_frontier_manifest_v1.json'
TEX='analysis/BT3981_BT3988_five_front_three_photon_closure_insert'
SECTION={'kind':'id','token':'bt3981-3988-five-front-photon-closure','source':'analysis/BT3981_BT3988_five_front_three_photon_closure_index_insert.html'}
PAGE={'token':'passes-3981-3988-five-front-photon-closure','source':'docs/five-front-photon-closure.html'}

def add_unique(items,value,key=None):
    if key is None:
        if value in items:return False
    else:
        matches=[x for x in items if x[key]==value[key]]
        if matches:
            if matches!=[value]: raise ValueError((matches,value))
            return False
    items.append(value); return True

def main():
    cfg=json.loads(CONFIG.read_text(encoding='utf-8'))
    changed={
      'required_ordered_inputs':add_unique(cfg['required_ordered_inputs'],TEX),
      'public_sections':add_unique(cfg['public_sections'],SECTION,'token'),
      'standalone_public_pages':add_unique(cfg['standalone_public_pages'],PAGE,'token')}
    CONFIG.write_text(json.dumps(cfg,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','changed':changed,'protected_index_modified':False},sort_keys=True))
if __name__=='__main__':main()
