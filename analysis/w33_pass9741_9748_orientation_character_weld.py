#!/usr/bin/env python3
"""Pass9741-9748: compare the Golay/A2 line-orientation bit with G2(4) edge orientation."""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9741_9748_ORIENTATION_CHARACTER_WELD.json'

def main():
 rank=json.loads((ROOT/'data/PART_W33_PASS9481_9488_RANK24_CENTRALIZER_FINGERPRINT.json').read_text())
 g=json.loads((ROOT/'data/PART_W33_PASS9085_9092_LEECH_G24_GRAPH_EDGES.json').read_text())
 orb=json.loads((ROOT/'data/PART_W33_PASS9365_9372_G24_EDGE_ORBITAL_REFINEMENT.json').read_text())
 w_line=rank['E6^4']['projective_image_order'];w_or=rank['A2^12']['projective_image_order']
 assert (w_line,w_or)==(648,324)
 edge=g['stabilizers']['edge'];edge_order=24192;ordered_edge=503193600//41600
 assert edge=='G2(2).2, order 24,192' and ordered_edge==12096 and edge_order//ordered_edge==2
 assert orb['unique_oriented_pair']['degrees']==[1512,1512]
 assert math.gcd(w_line,edge_order)==216 and edge_order%w_line!=0 and w_line%edge_order!=0
 out={'schema':'w33.pass9741_9748.orientation_character_weld.v1','status':'PASS','passes':'9741-9748',
 'W33_line_orientation':{'unoriented_stabilizer':'3^3:S4','order':648,'orientation_kernel':'3^3:A4','order_kernel':324,'quotient':'C2 = sign(S4)'},
 'G2_edge_orientation':{'unoriented_edge_stabilizer':'G2(2).2','order':edge_order,'ordered_edge_stabilizer_order':ordered_edge,'quotient':'C2 = endpoint reversal','rank14_oriented_relation_pair':'AD <-> BB_or_CC','paired_valencies':[1512,1512]},
 'parent_group_obstruction':{'gcd_orders':216,'648_divides_24192':False,'24192_divides_648':False,'reason':'The W33 line stabilizer contains a 3^4 factor whereas the G2 edge stabilizer has only 3^3; conversely the G2 stabilizer contains a factor 7 absent from the W33 line stabilizer. Thus neither local parent stabilizer embeds in the other.'},
 'weld_result':'The two orientation data are exactly the same abstract one-bit object: each is a canonical index-two C2 quotient, and C2 has no nontrivial automorphism, so once any bridge identifies the two underlying unoriented objects the orientation-character identification is forced. But the parent stabilizers are arithmetically incompatible, so this bit-level match does not extend to a direct stabilizer embedding and does not by itself construct the bridge.',
 'theorem':'Golay/A2 line parity and G2(4) edge reversal are canonically isomorphic as abstract C2 orientation quotients, while their full local stabilizers cannot embed into one another by order divisibility. Therefore orientation can be welded only after a higher-level transporter has matched the underlying objects; it is a forced compatibility check, not the transporter itself.',
 'boundary':'Exact group-order and quotient comparison. No canonical objectwise map between a W33 line and a Hall-Janko/G2 edge is asserted.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','quotients':['C2','C2'],'gcd_parent':216}));return 0
if __name__=='__main__':raise SystemExit(main())
