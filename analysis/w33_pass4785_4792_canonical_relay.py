#!/usr/bin/env python3
"""Canonical relay for the support-12 packet.

The mathematics was first implemented under aliases 4761--4768 after an earlier
reservation, but a later Track A lane began using the same numbers.  Canonical
release numbering is therefore 4785--4792.  This relay executes each original
witness, copies its exact certificate, changes only the public pass number, and
records the implementation alias.  No theorem payload is changed.
"""
from __future__ import annotations
import importlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAP=[
 (4785,4761,'w33_pass4761_thickening_even_cycle_code','PART_W33_PASS4761_THICKENING_EVEN_CYCLE_CODE.json','PART_W33_PASS4785_THICKENING_EVEN_CYCLE_CODE.json'),
 (4786,4762,'w33_pass4762_thickening_partner_rook45','PART_W33_PASS4762_THICKENING_PARTNER_ROOK45.json','PART_W33_PASS4786_THICKENING_PARTNER_ROOK45.json'),
 (4787,4763,'w33_pass4763_support12_reconstructs_srg45','PART_W33_PASS4763_SUPPORT12_RECONSTRUCTS_SRG45.json','PART_W33_PASS4787_SUPPORT12_RECONSTRUCTS_SRG45.json'),
 (4788,4764,'w33_pass4764_rook36_rectangle_partner_action','PART_W33_PASS4764_ROOK36_RECTANGLE_PARTNER_ACTION.json','PART_W33_PASS4788_ROOK36_RECTANGLE_PARTNER_ACTION.json'),
 (4789,4765,'w33_pass4765_dual_edge_code_css_carrier_separation','PART_W33_PASS4765_DUAL_EDGE_CODE_CSS_CARRIER_SEPARATION.json','PART_W33_PASS4789_DUAL_EDGE_CODE_CSS_CARRIER_SEPARATION.json'),
 (4790,4766,'w33_pass4766_grid_code_point_edge_bridge','PART_W33_PASS4766_GRID_CODE_POINT_EDGE_BRIDGE.json','PART_W33_PASS4790_GRID_CODE_POINT_EDGE_BRIDGE.json'),
 (4791,4767,'w33_pass4767_leech_neighbor_golay_parity_matroid','PART_W33_PASS4767_LEECH_NEIGHBOR_GOLAY_PARITY_MATROID.json','PART_W33_PASS4791_LEECH_NEIGHBOR_GOLAY_PARITY_MATROID.json'),
 (4792,4768,'w33_pass4768_deck_vs_even_cycle_parity_boundary','PART_W33_PASS4768_DECK_VS_EVEN_CYCLE_PARITY_BOUNDARY.json','PART_W33_PASS4792_DECK_VS_EVEN_CYCLE_PARITY_BOUNDARY.json'),
]
def main()->int:
    for canon,alias,module,old,new in MAP:
        m=importlib.import_module(module);rc=m.main();assert rc==0
        d=json.loads((ROOT/'data'/old).read_text(encoding='utf-8'));assert d['pass']==alias
        d['implementation_alias']=alias;d['pass']=canon
        (ROOT/'data'/new).write_text(json.dumps(d,indent=2,sort_keys=True)+'\n',encoding='utf-8')
        print(f'canonicalized {alias} -> {canon}: data/{new}')
    return 0
if __name__=='__main__':raise SystemExit(main())
