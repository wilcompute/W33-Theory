#!/usr/bin/env python3
"""Passes 4835/4839 — full automorphism group of the intrinsic code399 dual-shell design.

Pass4832 reconstructs, from the [2025,399,14]_2 generator columns alone,
  * 405 equal-column classes of size 4 (cold),
  * 135 equal-column classes of size 3 (hot), and
  * 135 minimum quotient dependencies, each of class-size profile (4,4,4,3),
with every one of the 540 quotient classes used exactly once.

If we deliberately retain ONLY that intrinsic dual-shell relational data, then the
135 minimum relations are pairwise disjoint cells.  In each cell the hot class is
distinguished by size 3 and the three cold classes are indistinguishable.  Hence
its class-level automorphism group is exactly

    S_3 wr S_135 = S_3^135 semidirect S_135.

At physical-coordinate level each cold size-4 class also admits an independent
S_4 and each hot size-3 class an independent S_3.  Thus the dual-shell design is
far more symmetric than PGSp(4,3), and cannot intrinsically reconstruct the
27 Petersen fibers, 45 packets, or GQ(4,2) quotient.  This is an exact negative:
those structures require additional cross-cell relations beyond the weight-two
class partition plus the minimum quotient shell.
"""
from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/PART_W33_PASS4832_CODE399_DUAL_SHELL_GEOMETRY.json'
OUT=ROOT/'data/PART_W33_PASS4835_4839_INTRINSIC_DUALSHELL_SYMMETRY_FALSIFIER.json'

def main()->int:
    d=json.loads(SRC.read_text())
    w2=d['weight2_shell']; q=d['quotient_by_weight2_span']; rec=d['intrinsic_reconstruction']
    prof={int(k):int(v) for k,v in w2['class_size_profile'].items()}
    assert prof=={3:135,4:405}, prof
    assert q['length']==540 and q['weight4_dependency_count']==135
    assert rec['minimum_weight4_dependencies_partition_all_classes'] is True
    # Each relation contains one hot size-3 class and three cold size-4 classes.
    raw=q['weight4_class_size_profiles']
    assert len(raw)==1 and next(iter(raw.values()))==135, raw
    key=next(iter(raw))
    assert all(x in key for x in ('3','4')), key

    cells=135; cold=405; hot=135
    class_aut_order=(math.factorial(3)**cells)*math.factorial(cells)
    internal_coordinate_order=(math.factorial(4)**cold)*(math.factorial(3)**hot)
    physical_relational_aut_order=class_aut_order*internal_coordinate_order
    pgsp=51840
    assert class_aut_order>pgsp

    out={
      'passes':[4835,4839],
      'source':'Pass4832 intrinsic generator-column dual-shell certificate',
      'class_vertices':540,
      'class_size_profile':{'3_hot':hot,'4_cold':cold},
      'minimum_relations':cells,
      'relation_profile':'one hot size-3 class + three cold size-4 classes',
      'relations_partition_all_class_vertices':True,
      'class_level_automorphism_group':'S3 wr S135 = S3^135 semidirect S135',
      'class_level_automorphism_order':str(class_aut_order),
      'physical_coordinate_kernel':'S4^405 x S3^135',
      'physical_coordinate_kernel_order':str(internal_coordinate_order),
      'full_physical_relational_automorphism_order':str(physical_relational_aut_order),
      'PGSp_order':pgsp,
      'equals_PGSp':False,
      'reconstructs_27_Petersen_fibers':False,
      'reconstructs_45_packets_or_GQ42':False,
      'proof':'The 135 minimum quotient relations are disjoint. Class size distinguishes the unique hot vertex in each cell but leaves the three cold vertices freely permutable, while the 135 cells are freely permutable. Therefore the class-level automorphism group is exactly S3 wr S135. This action is transitive on cells with full S135 quotient, so no nontrivial 27- or 45-block cross-cell structure is invariant under the intrinsic design alone.',
      'boundary':'This falsifies reconstruction from ONLY equal-column class sizes plus the complete minimum quotient shell. It does not say the full [2025,399,14]_2 code lacks PGSp/GQ structure; higher dual shells or other code relations may recover it.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
