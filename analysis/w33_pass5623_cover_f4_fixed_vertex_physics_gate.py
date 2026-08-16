#!/usr/bin/env python3
"""Pass5623: separate the exact q=5 fixed-vertex singlet from any vacuum claim.

The selected 13-cover is a q=5 NO_5^+(5) object.  Its exact stabilizer image has
orbits 1+12.  The associated 2-(13,6,60) design has 312 blocks and the same
order-576 automorphism action.  Because it is a 2-design every one of the 13
points has identical local incidence numbers; the fixed point is distinguished
only by the GLOBAL embedding/action, not by local degree or pair incidence.

On the centered 13-point simplex module (dimension 12), a 1+12 G-set has a
unique invariant line, represented by
  12 e_fixed - sum_{moving} e_i.
Thus there is a mathematically exact singlet/order-parameter direction relative
to the moving 12.  Calling it a physical vacuum is not justified, especially
because this cover is q=5 while the main W33 physics substrate is q=3.

If the direct GAP S12 conjugator is present, this pass also consumes the existing
Pass5615 cover->F4 dictionary.  Otherwise it remains fail-closed on the explicit
12-object map while still freezing the fixed-line theorem.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5623_COVER_F4_FIXED_VERTEX_PHYSICS_GATE.json'

def main():
    v,k,lam=13,6,60
    r=lam*(v-1)//(k-1)
    b=v*r//k
    assert r==144 and b==312
    # Invariants in C^{1+12}: dimension = number of G-set orbits = 2.
    # Restrict to the sum-zero standard simplex module: one linear relation
    # removes the global constant, leaving exactly one invariant line.
    centered_invariant_dimension=1
    selected=[7,31,74,112,129,141,158,190,194,227,255,278,321]
    dict_path=ROOT/'data/PART_W33_PASS5615_COVER_F4_OBJECT_DICTIONARY.json'
    map_status='PENDING_DIRECT_GAP_CONJUGATOR'
    explicit=None
    if dict_path.exists():
        d=json.loads(dict_path.read_text())
        if d.get('status')=='EXPLICIT_COVER_TO_F4_OBJECT_DICTIONARY':
            map_status='EXPLICIT_MOVING12_TO_F4_DICTIONARY_AVAILABLE'
            explicit={'fixed_cover_vertex':d.get('fixed_cover_vertex'),
                      'cover_vertex_to_F4_short_root_pair_index':d.get('cover_vertex_to_F4_short_root_pair_index')}

    out={
      'pass':5623,'status':'Q5_GLOBAL_FIXED_LINE_THEOREM__'+map_status,
      'selected_q5_13_cover':selected,
      'known_action':{'setwise_stabilizer_order':1152,'S13_image_order':576,'pointwise_kernel_order':2,'orbit_sizes':[1,12]},
      'design':{'parameters':'2-(13,6,60)','blocks':b,'blocks_through_each_point':r,'blocks_through_each_pair':lam,'local_point_statistics_uniform':True},
      'centered_simplex_module':{'dimension':12,'invariant_line_dimension':centered_invariant_dimension,'representative':'12 e_fixed - sum_{moving 12} e_i'},
      'F4_dictionary_status':map_status,'explicit_dictionary':explicit,
      'interpretation':'The fixed point supplies a genuine global symmetry-breaking singlet/order-parameter direction relative to the moving 12. It is not locally distinguished by the balanced design.',
      'physics_firewall':'This is a q=5 cover branch. No action-level bridge identifies its invariant line with the q=3 W33 vacuum, Higgs, photon, or any Standard Model field. "Vacuum" is therefore not promoted.',
      'sources':['analysis/w33_pass5417_cover_orbits.g','analysis/w33_pass5460_5467_the_distinguished_vertex_is_a_q5_fact.py','analysis/w33_pass5606_cover12_explicit_conjugator.g','analysis/w33_pass5615_cover_f4_object_dictionary_gate.py']
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
