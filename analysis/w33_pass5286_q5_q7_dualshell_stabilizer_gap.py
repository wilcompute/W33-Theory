#!/usr/bin/env python3
"""Pass5286: ambient-vs-support symmetry gap for q=5 and q=7 footprint dual shells.

Pass5230 gives a single PSp4(5) orbit of 24,375 weight-8 dual checks whose
selected block graph is K8 minus a perfect matching. Pass5245 gives a PSp4(7)
orbit of 1,920,800 weight-12 dual checks whose selected block graph is 8-regular
and whose complement is the disjoint union of a triangular prism and K3,3.

Orbit-stabilizer determines the ambient symplectic stabilizers exactly. The
abstract support graphs have substantially larger automorphism groups, so not
every combinatorial support symmetry extends to the ambient polar geometry.
This gap is a useful invariant for constructing/stabilizing higher-q shell orbits.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5286_Q5_Q7_DUALSHELL_STABILIZER_GAP.json'

def psp4_order(q):
    return q**4*(q*q-1)*(q**4-1)//2

def main():
    g5=psp4_order(5); o5=24375; s5=g5//o5
    assert g5==4680000 and s5==192
    # Aut(K8 - 4K2) = C2 wr S4: order 2^4*4! = 384.
    aut5=2**4*24; assert aut5==384 and aut5//s5==2

    g7=psp4_order(7); o7=1920800; s7=g7//o7
    assert g7==138297600 and s7==72
    # The q7 complement has two nonisomorphic connected components:
    # triangular prism (Aut order 12) and K3,3 (Aut order 72).
    aut_prism=12; aut_k33=2*6*6
    aut7=aut_prism*aut_k33
    assert aut_k33==72 and aut7==864 and aut7//s7==12

    out={
      'pass':5286,
      'status':'THEOREM_Q5_Q7_DUALSHELL_AMBIENT_SUPPORT_SYMMETRY_GAP',
      'q5':{
        'PSp4_order':g5,'dual_orbit_size':o5,'ambient_support_stabilizer_order':s5,
        'support_graph':'K8 minus a perfect matching = K_{2,2,2,2}',
        'abstract_graph_automorphism_order':aut5,
        'graph_aut_over_ambient_stabilizer_index':2,
      },
      'q7':{
        'PSp4_order':g7,'dual_orbit_size':o7,'ambient_support_stabilizer_order':s7,
        'support_graph':'12 vertices, 8-regular; complement = triangular prism disjoint union K3,3',
        'abstract_graph_automorphism_order':aut7,
        'graph_aut_over_ambient_stabilizer_index':12,
      },
      'interpretation':'The dual-check support graph has combinatorial automorphisms that do not extend to the ambient symplectic P-component action. Stabilizer data therefore carries information invisible to the induced support graph alone.',
      'boundary':'Finite q5/q7 group-order theorem. It does not classify the full q7 weight-12 shell beyond the known orbit and does not assert a general stabilizer formula.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
