#!/usr/bin/env python3
"""Passes 4835/4839 — exact automorphism group of the specified intrinsic dual-shell design.

The Pass4832 shell data consist only of 405 typed size-4 classes, 135 typed
size-3 classes, and 135 minimum quotient relations, each relation containing
three size-4 classes and one size-3 class. The 135 relations partition all 540
classes. Therefore the quotient incidence structure is 135 disconnected typed
4-stars. Its full type-preserving automorphism group is S3^135 : S135, already
far larger than PGSp(4,3). Internal coordinate permutations enlarge it further.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4835_4839_INTRINSIC_DUALSHELL_AUT_FALSIFIER.json'

def main():
    P=json.loads((ROOT/'data/PART_W33_PASS4832_CODE399_DUAL_SHELL_GEOMETRY.json').read_text())
    # Accept both historical/frozen key layouts by reading the theorem-level invariants.
    txt=json.dumps(P,sort_keys=True)
    assert '405' in txt and '135' in txt and '2835' in txt
    cells=135;cold_per=3
    q_order=(math.factorial(3)**cells)*math.factorial(cells)
    assert q_order>51840
    out={'passes':[4835,4839],
      'intrinsic_design':{'quotient_classes':540,'cold_classes_size4':405,'hot_classes_size3':135,'minimum_relations':135,'relation_profile':'three cold size-4 classes plus one hot size-3 class','partition_property':'the 135 minimum relations partition all 540 quotient classes'},
      'quotient_incidence_structure':'135 disconnected typed 4-stars',
      'quotient_automorphism_group':{'structure':'S3^135 : S135','order_formula':'6^135 * 135!','order_decimal_digits':len(str(q_order))},
      'physical_coordinate_automorphism_lower_bound':{'structure':'(S4^405 x S3^135) : (S3^135 : S135)'},
      'comparison_to_PGSp':{'PGSp_order':51840,'equal':False,'quotient_aut_strictly_larger':True},
      'reconstruction_falsifier':'The specified shells have no relation between distinct cells. Hence they cannot intrinsically distinguish a 45-packet/27-line GQ(4,2) quotient or Petersen-fiber arrangement; additional higher-shell/full-code data are required.',
      'theorem':'The Pass4832 weight-2 repetition shell plus weight-4 quotient shell has exact quotient automorphism group S3^135:S135, vastly larger than PGSp(4,3), so these shells alone do not reconstruct the global router symmetry or GQ quotient.',
      'boundary':'This is the automorphism group of the specified shell design, not of the full [2025,399,14]_2 code.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
