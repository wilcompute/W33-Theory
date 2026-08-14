#!/usr/bin/env python3
"""Pass5125 (bonkers): the q3 integral torsion line is the H27 triality-center module."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5125_TORSION_TRIALITY_MODULE_WELD.json'

def J(name):return json.loads((ROOT/'data'/name).read_text())

def main():
    t=J('PART_W33_PASS5121_Q3_INTEGRAL_TORSION_MODULE.json')
    c=J('PART_W33_PASS5109_CURVATURE_KERNEL_V4.json')
    tors=t['V4_character'];ca=c['central_C3']['V4_conjugation']
    center={k:('+' if v=='fix' else '-') for k,v in ca.items()}
    assert tors==center=={'e':'+','a':'-','b':'+','c':'-'}
    assert t['U81_action'].startswith('trivial') and c['central_C3']['order']==3
    out={'pass':5125,'status':'THEOREM_EQUIVARIANT_Z3_TORSION_TRIALITY_WELD',
         'arithmetic_module':'Tor coker(H^T) ~= Z/3 from Pass5121',
         'controller_module':'Z(U81)=Z(H27)=C3 triality axis from Pass5105/5109',
         'U81_action_on_both':'trivial',
         'V4_character_on_both':tors,
         'module_isomorphism':'As F3[U81 semidirect V4]-modules, Tor coker(H^T) is isomorphic to Z(U81). Sending the nonzero torsion generator [w] to either nonzero center generator gives the two scalar-related equivariant isomorphisms.',
         'canonicity':'The one-dimensional module type is canonical; a generator-to-generator map is unique only up to F3^*={1,2}.',
         'interpretation':'The ternary Smith saturation defect and the Heisenberg triality center are two realizations of the same local controller representation character.',
         'boundary':'This is an exact finite arithmetic/group-module identification. It does not assign electric charge, generation physics, or a hardware observable to the torsion class.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
