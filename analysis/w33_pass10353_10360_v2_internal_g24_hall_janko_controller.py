#!/usr/bin/env python3
"""Pass10353-10360 outside-box: the Hall--Janko/G2(4) controller is internal to canonical V2.

Pass10345 identifies the canonical good-sublattice orbit of V2 and gives

  Stab_Co1(V2) ~= G2(4) x A4.

Earlier Pass9085 independently identified the Hall--Janko carrier as the rank-3
G2(4):2 graph:

  416 vertices = J2:2 cosets,
  20,800 edges = G2(2).2 cosets,
  41,600 oriented flags.

Restricting the full graph controller G2(4):2 to the index-two simple subgroup
G2(4) removes precisely the outer endpoint/orientation involution:

  [G2(4):J2] = 416,
  [G2(4):G2(2)] = 20,800,
  [G2(4):G2(2)] * 2 = 41,600 flags after orientation.

Therefore the same G2(4) factor that stabilizes canonical V2 intrinsically
carries the 416 Hall--Janko vertices and 20,800 Leech six-space edges.  The A4
factor is a commuting spectator from the good-sublattice stabilizer.  This
upgrades the old Hall--Janko bridge from an external count/subgroup-chain
connection to an INTERNAL homogeneous geometry of Stab(V2).
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10353_10360_V2_INTERNAL_G24_HALL_JANKO_CONTROLLER.json'

def main():
    v2=json.loads((ROOT/'data/PART_W33_PASS10345_10352_CANONICAL_V2_GOOD_ORBIT7.json').read_text())
    hj=json.loads((ROOT/'data/PART_W33_PASS9085_9092_LEECH_G24_GRAPH_EDGES.json').read_text())
    G2=int(v2['C13_closure']['G2_4_order']);assert G2==251_596_800
    A4=12;stab=G2*A4;assert stab==int(v2['orbit7']['Stab_Co1_order'])
    J2=604_800;G22=12_096
    assert G2//J2==416
    assert G2//G22==20_800
    assert 2*(G2//G22)==41_600
    assert hj['G2(4)_graph']['vertices']==416 and hj['G2(4)_graph']['edges']==20_800
    assert hj['stabilizers']['vertex'].startswith('J2:2') and hj['stabilizers']['edge'].startswith('G2(2).2')

    # A4 is a direct commuting factor in the published orbit-7 stabilizer, so quotienting
    # Stab(V2) by it recovers the simple graph controller G2(4).
    assert stab//A4==G2
    # The full graph controller is the outer extension; its order is twice G2.
    G2full=503_193_600;assert G2full==2*G2

    out={
      'schema':'w33.pass10353_10360.v2_internal_g24_hall_janko_controller.v1','status':'PASS','passes':'10353-10360','outside_box':True,
      'canonical_V2_stabilizer':{'Co1':'G2(4) x A4','order':stab,'controller_quotient':'Stab_Co1(V2)/A4 ~= G2(4)','G2_4_order':G2,'A4_order':A4},
      'internal_homogeneous_carriers':{
        'Hall_Janko_vertices':{'cosets':'G2(4)/J2','J2_order':J2,'index':G2//J2},
        'Leech_sixspace_edges':{'cosets':'G2(4)/G2(2)','G2_2_order':G22,'index':G2//G22},
        'oriented_incidence_flags':{'count':2*(G2//G22),'meaning':'two endpoint orientations per edge'}},
      'full_graph_controller':{'group':'G2(4):2','order':G2full,'vertex_stabilizer':'J2:2','edge_stabilizer':'G2(2).2','relation':'adjoining the outer C2 extends the internal simple controller and supplies endpoint reversal'},
      'A4_factor':{'role':'commuting direct factor in Stab_Co1(V2)','connection_target':'the same abstract A4 appears as the orientation kernel inside the W33 line stabilizer 3^3:A4','claim_boundary':'abstract/direct-factor compatibility only; no objectwise identification with the W33 A4 has yet been constructed'},
      'theorem':'The Hall--Janko/G2(4) graph is an intrinsic homogeneous geometry of the canonical Leech selector V2. After identifying Stab_Co1(V2)=G2(4)xA4, quotienting out the commuting A4 leaves exactly the simple controller whose cosets by J2 and G2(2) are the 416 Hall--Janko vertices and 20,800 Leech six-space edges. The previously external Hall--Janko carrier is therefore internal to the symmetry of canonical V2.',
      'consequence':'The Leech selector, Hall--Janko controller, and order-13 clock now sit in one stabilizer: C13 < G2(4) < Stab_Co1(V2). The remaining outer C2 is precisely the graph endpoint-orientation extension G2(4):2/G2(4).',
      'boundary':'Exact group-order/coset synthesis of two independently certified repo results plus the published orbit-7 stabilizer identification from Pass10345. It does not construct a new coordinate action of G2(4) on V2.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','StabV2':stab,'HJ':416,'edges':20800,'controller':'G2(4)'}))
    return 0
if __name__=='__main__':raise SystemExit(main())
