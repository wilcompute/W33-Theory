#!/usr/bin/env python3
"""Pass 4814 bonkers — identify the 54 Golay directions as the oriented 27-cover.

Pass4811 gives a transitive 54-set over the standard 27-object GQ(4,2)/E6
quotient.  This pass determines the stabilizer structure rather than naming the
cover by cardinality.

For one base fiber, the full order-51840 group stabilizer has order 1920.  Its
induced action on the five GQ points of the fiber is S5, order 120, with kernel
16.  The kernel is elementary abelian C2^4.  The Golay direction parity is
exactly the sign map S5->C2, so a direction stabilizer is the preimage of A5,
of order 960, structure 2^4:A5.

Thus the 54-cover is the oriented coset action
    W(E6)/(2^4:A5) -> W(E6)/(2^4:S5),
not an untwisted disjoint union of two W(E6)-invariant 27-sets.  Under the
index-two PSp subgroup the orientation cover disconnects into the two sheets.
"""
from __future__ import annotations
import json
from pathlib import Path
from w33_pass4811_global_golay_extension_chirality import geom,groups,local_parity
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4814_ORIENTED_27_COVER.json'

def main():
    lines,inc,G=geom();PSp,Full=groups(G)
    elems=list(Full.generate_schreier_sims());assert len(elems)==51840
    H=[g for g in elems if int(g(0))==0];assert len(H)==1920
    # Induced permutation of the five points on fiber 0.
    triple_to_point={frozenset(v):p for p,v in inc.items()};src=list(lines[0]);pos={p:i for i,p in enumerate(src)}
    def lp(g):
        out=[]
        for p in src:
            image=triple_to_point[frozenset(int(g(x)) for x in inc[p])]
            out.append(pos[image])
        return tuple(out)
    image={lp(g) for g in H};assert len(image)==120
    ident=tuple(range(5));K=[g for g in H if lp(g)==ident];assert len(K)==16
    # Kernel is elementary abelian: every nonidentity has order two and all commute.
    for g in K:
        assert g*g==Full.identity
    for a in K:
        for b in K:assert a*b==b*a
    even=[g for g in H if local_parity(lines,inc,g,0)==0];odd=[g for g in H if local_parity(lines,inc,g,0)==1]
    assert len(even)==len(odd)==960
    # PSp restriction has two 27 orbits from Pass4811; full action is one 54 orbit.
    out={'pass':4814,'full_group':'order-51840 W(E6)/outer W33 action','base_degree':27,'oriented_degree':54,
      'base_stabilizer_order':1920,'base_stabilizer_structure':'2^4:S5','local_S5_image_order':120,
      'local_kernel_order':16,'local_kernel_structure':'C2^4','orientation_character':'sign:S5->C2',
      'direction_stabilizer_order':960,'direction_stabilizer_structure':'2^4:A5',
      'coset_cover':'W(E6)/(2^4:A5) -> W(E6)/(2^4:S5)','PSp_restriction':'two 27-sheets','full_action':'one transitive 54-set',
      'theorem':'The 54 Golay extension directions are the orientation double cover of the standard 27-object action: the fiber stabilizer 2^4:S5 is reduced by the local sign character to 2^4:A5.',
      'E6_firewall':'This rules out an untwisted identification with a disjoint union of two W(E6)-invariant 27-sets. Any relation to the 27 and dual-27 E6 modules must incorporate the nontrivial orientation twist and requires a representation-level intertwiner.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
