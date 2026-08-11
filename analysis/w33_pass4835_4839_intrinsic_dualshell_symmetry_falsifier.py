#!/usr/bin/env python3
"""Passes 4835/4839 — full automorphism group of the intrinsic code399 dual-shell design.

Pass4832 reconstructs, from the [2025,399,14]_2 generator columns alone,
  * 405 equal-column classes of size 4 (cold),
  * 135 equal-column classes of size 3 (hot), and
  * 135 minimum quotient dependencies of class-size profile (3,4,4,4),
with every one of the 540 quotient classes used exactly once.

Retaining ONLY that intrinsic dual-shell relational data leaves 135 pairwise
disjoint cells.  In each cell the hot class is distinguished by size 3 and the
three cold classes are indistinguishable.  Therefore the class-level
automorphism group is exactly S3 wr S135.  This is much larger than PGSp(4,3),
so the dual-shell design alone cannot reconstruct the 27 Petersen fibers, 45
packets, or GQ(4,2) quotient.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/PART_W33_PASS4832_CODE399_DUAL_SHELL_GEOMETRY.json'
OUT=ROOT/'data/PART_W33_PASS4835_4839_INTRINSIC_DUALSHELL_SYMMETRY_FALSIFIER.json'

def main()->int:
    d=json.loads(SRC.read_text());w2=d['weight2_shell'];q=d['quotient_by_weight2_span'];rec=d['intrinsic_reconstruction']
    prof={int(k):int(v) for k,v in w2['class_size_profile'].items()}
    assert prof=={3:135,4:405},prof
    assert q['length']==540 and q['weight4_dependency_count']==135
    assert q['minimum_dependencies_partition_all_540_classes'] is True
    assert list(q['weight4_class_size_profile'])==[3,4,4,4]
    assert rec['K6_cells_recovered']==135 and rec['hot_coordinate_classes']==135 and rec['cold_K22_coordinate_classes']==405
    cells=135;cold=405;hot=135
    class_aut_order=(math.factorial(3)**cells)*math.factorial(cells)
    internal_coordinate_order=(math.factorial(4)**cold)*(math.factorial(3)**hot)
    physical_relational_aut_order=class_aut_order*internal_coordinate_order;pgsp=51840
    assert class_aut_order>pgsp
    out={'passes':[4835,4839],'source':'Pass4832 frozen intrinsic generator-column dual-shell certificate','class_vertices':540,
      'class_size_profile':{'3_hot':hot,'4_cold':cold},'minimum_relations':cells,'relation_profile':'one hot size-3 class + three cold size-4 classes','relations_partition_all_class_vertices':True,
      'class_level_automorphism_group':'S3 wr S135 = S3^135 semidirect S135','class_level_automorphism_order':str(class_aut_order),
      'physical_coordinate_kernel':'S4^405 x S3^135','physical_coordinate_kernel_order':str(internal_coordinate_order),'full_physical_relational_automorphism_order':str(physical_relational_aut_order),
      'PGSp_order':pgsp,'equals_PGSp':False,'reconstructs_27_Petersen_fibers':False,'reconstructs_45_packets_or_GQ42':False,
      'proof':'The 135 minimum quotient relations partition the 540 class vertices. Class size marks the unique hot vertex of every cell; the three cold vertices may be permuted freely and the 135 cells may be permuted freely. Hence Aut on class vertices is exactly S3 wr S135. Its S135 quotient destroys every nontrivial cross-cell 27- or 45-block partition.',
      'boundary':'This falsifies reconstruction from ONLY equal-column class sizes plus the complete minimum quotient shell. The full code may recover PGSp/GQ structure through higher shells or other relations.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
