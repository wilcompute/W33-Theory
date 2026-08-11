#!/usr/bin/env python3
"""Pass4844 — exact quotient metric of C399/C_Levi.

Use only already frozen local-code and inclusion facts.  C399 is a subcode of the
direct sum of 135 disjoint [15,3,7]_2 local cells.  In one cell the seven
nonzero logical words have weights 7,7,7,8,8,8,15: singleton logical bits have
weight7, pairs weight8 and the triple weight15.  The outer line-parity code is
O21=[27,21,3]_2.  Hence a physical word of total weight14 consists of exactly
two weight7 singleton words; their outer labels must coincide because O21 has
no weight-two word.  There are 15 singleton coordinates over each of 27 lines.

C_Levi has distance96, so it contains no weight14 word and the difference of two
distinct weight14 words (weight <=28) cannot lie in C_Levi.  Thus all 2835
ambient minima give distinct minimum quotient cosets.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4844_CODE399_MOD_LEVI_QUOTIENT.json'
def main()->int:
 local_weights=[7,7,7,8,8,8,15];assert min(local_weights)==7
 outer_distance=3;lines=27;sheets_per_line=15
 A14=lines*math.comb(sheets_per_line,2);assert A14==2835
 out={'pass':4844,'ambient':'C399=[2025,399,14]_2','subcode':'C_Levi=[2025,64,96]_2','quotient_dimension':335,
 'quotient_metric':'minimum physical Hamming weight among representatives of a nonzero Levi coset','quotient_minimum_distance':14,'minimum_quotient_cosets':A14,
 'ambient_weight14_shell':{'size':A14,'structure':'27 fibers, one per outer line; each fiber is the C(15,2)=105 unordered pairs of weight-7 local singleton generators carrying that line label','all_minima_lie_in_C378':True},
 'injectivity_into_quotient':'If two distinct weight14 words represented the same Levi coset, their difference would be a nonzero Levi word of weight at most 28, contradicting d(C_Levi)=96.',
 'theorem':'C399/C_Levi has dimension335 and physical coset minimum distance14. Its complete minimum shell consists of exactly 2835 distinct cosets, represented by pairs of local weight-7 generators with the same outer-line label: 27*C(15,2).',
 'boundary':'This is a quotient metric theorem, not a claim that C399 splits as a PGSp-module direct sum C_Levi plus a 335-dimensional complement.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
