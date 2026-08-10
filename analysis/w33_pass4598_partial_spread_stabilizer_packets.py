#!/usr/bin/env python3
"""Pass 4598 bonkers -- the 135 maximal partial spreads form a canonical 45x3 cover.

Pass4595 finds that a representative order-192 half-spinor stabilizer fixes
exactly three maximal size-8 W33 partial spreads, and each of those spreads has
that same full stabilizer. Pass1100 gives one transitive 135-object carrier of
all maximal/unextendable size-8 partial spreads. Orbit-stabilizer therefore
forces 45 conjugate stabilizer subgroups and normalizer order 576; N/H=C3 acts
regularly on the three spreads in each packet.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4598_PARTIAL_SPREAD_STABILIZER_PACKETS.json'
def main():
    d=json.loads((ROOT/'data/PART_W33_PASS4595_CONCRETE_D4_TRIALITY_W33_LIFTS.json').read_text())
    old=json.loads((ROOT/'data/w33_pass1100_name_the_135.json').read_text())
    assert d['partial_spread_census']['unextendable_maximal']==135 and old['unextendable']==135
    a=d['transitive_135_family'];assert a['stabilizer_order']==192 and a['fixed_maximal_size8_partial_spreads']==3 and a['each_fixed_partial_spread_stabilizer_order']==192
    G=25920;objects=135;perH=3;nH=objects//perH;normalizer=G//nH
    assert (nH,normalizer,normalizer//192)==(45,576,3)
    out={'pass':4598,'source_carrier':'the transitive 135 maximal/unextendable size-8 W33 partial spreads of Pass1100',
      'packet_definition':'three partial spreads with the same order-192 setwise stabilizer H arising in the Pass4595 half-spinor lift',
      'counts':{'partial_spreads':135,'spreads_per_packet':3,'stabilizer_packets':45,'H_order':192,'normalizer_order':576,'normalizer_quotient_order':3},
      'packet_action':'N_G(H)/H = C3 acts faithfully and transitively on the three partial spreads; an element fixing all three lies in their common full stabilizer H.',
      'theorem':'The 135 maximal size-8 partial spreads carry a canonical 3-to-1 quotient onto 45 conjugacy packets of order-192 stabilizers, with C3 deck action.',
      'comparison_boundary':'This is a second natural 135->45 cover. It is not identified with the Pass4585/4592 center-quad 45-set until an explicit PSp intertwiner is constructed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
