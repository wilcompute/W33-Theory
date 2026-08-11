from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_two_order1440_extensions_are_not_conflated():
    d=json.loads((ROOT/'data/PART_W33_PASS4873_TWO_ORDER1440_EXTENSIONS.json').read_text())
    a=d['direct_marked_residue_extension']
    b=d['duad_syntheme_outer_extension']
    assert a['order']==b['order']==1440
    assert a['group']=='S6 x C2'
    assert b['group']=='Aut(S6) = S6 : Out(S6)'
    assert a['center_order']==2 and b['center_order']==1
    assert a['involution_count']==151 and b['involution_count']==111
    assert a['element_order_census'].get('8',0)==0
    assert b['element_order_census']['8']==360
    assert d['nonisomorphism_certificates']['different_complete_order_census']

def test_pass4873_is_in_shared_frontier_once():
    live=(ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text()
    insert=(ROOT/'analysis/PASS4873_two_order1440_extensions_insert.tex').read_text()
    assert live.count('PASS4873_two_order1440_extensions_insert')==1
    assert 'WDDPassFourEightSevenThreeLoaded' in insert
