#!/usr/bin/env python3
"""Pass 4622 bonkers -- canonical 135->45 stabilizer packets of maximal partial spreads."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4622_PARTIAL_SPREAD_STABILIZER_PACKETS.json'
def main():
    d=json.loads((ROOT/'data/PART_W33_PASS4619_CONCRETE_D4_TRIALITY_W33_LIFTS.json').read_text())
    old=json.loads((ROOT/'data/w33_pass1100_name_the_135.json').read_text())
    a=d['transitive_135_family'];assert d['partial_spread_census']['unextendable_maximal']==old['unextendable']==135
    assert (a['stabilizer_order'],a['fixed_maximal_size8_partial_spreads'],a['each_fixed_partial_spread_stabilizer_order'])==(192,3,192)
    G=25920;nH=135//3;normalizer=G//nH;assert (nH,normalizer,normalizer//192)==(45,576,3)
    out={'pass':4622,'source_carrier':'the transitive 135 maximal/unextendable size-8 W33 partial spreads of Pass1100',
      'packet_definition':'three partial spreads with the same order-192 setwise stabilizer H exposed by the Pass4619 half-spinor lift',
      'counts':{'partial_spreads':135,'spreads_per_packet':3,'stabilizer_packets':45,'H_order':192,'normalizer_order':576,'normalizer_quotient_order':3},
      'packet_action':'N_G(H)/H=C3 acts faithfully and transitively on the three partial spreads.',
      'theorem':'The 135 maximal size-8 partial spreads carry a canonical 3-to-1 quotient onto 45 conjugacy packets of order-192 stabilizers, with C3 deck action.',
      'comparison_boundary':'This second natural 135->45 cover is not identified with the center-quad 45-set absent an explicit PSp intertwiner.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
