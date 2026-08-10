#!/usr/bin/env python3
"""Pass 4805 — q=9 minimum line-kernel shell via the complete BLT classification.

Pass4754 proved for every odd prime power q that
  d(ker_F2 A_*(W(3,q)))=q+1,
and equality words are exactly BLT sets (q+1 pairwise-skew W-lines with the
0-or-2 external intersection property).  Therefore a complete BLT
classification transfers verbatim to the complete minimum shell.

Anton Betten's complete q=9 table in PGammaO(5,9) has three classes:
Linear (stabilizer 28800), K1 (5760), and Fi/Mondello (400).  This script
checks the group arithmetic and freezes only that full-equivalence statement;
it does not guess the finer PSp orbit splitting.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4805_Q9_BLT_MINIMUM_SHELL.json'

def main()->int:
    q=9;h=2
    group=h*q**4*(q**4-1)*(q**2-1)
    assert group==6_886_425_600
    rows=[('Linear',28_800,'kernel Dihedral'),('K1',5_760,'kernel cyclic'),('Fi/Mondello',400,'kernel trivial')]
    classes=[]
    for name,stab,note in rows:
        assert group%stab==0
        classes.append({'name':name,'stabilizer_PGammaO':stab,'class_size':group//stab,'Betten_note':note})
    assert [x['class_size'] for x in classes]==[239_112,1_195_560,17_216_064]
    total=sum(x['class_size'] for x in classes);assert total==18_650_736
    out={'pass':4805,'q':9,'kernel_length':(q+1)*(q*q+1),'kernel_minimum_distance':q+1,
      'minimum_word_model':'BLT sets of size 10 in the dual Q(4,9)',
      'full_semilinear_equivalence_group':'PGammaO(5,9)','full_group_order':group,
      'complete_classes':classes,'complete_minimum_shell_size':total,
      'class_count':3,'first_three_phase_shell':True,
      'canonical_projective_involution_fixed_lines':q+3,
      'canonical_involution_is_minimum':False,
      'prior_art':'Anton Betten, A Classification of BLT-sets of Small Order (2009), complete q=9 table',
      'theorem':'At q=9 the complete minimum shell of ker_F2 A_*(W(3,9)) has d=10 and exactly three classes under full projective-semilinear orthogonal equivalence: Linear, K1, and Fi/Mondello, of sizes 239112, 1195560, and 17216064.',
      'boundary':'BLT class names, completeness, and stabilizers are prior art. The repo contribution here is the transfer to the minimum shell using the independently proved minimum-word=BLT theorem. No claim is made that each full class is one PSp(4,9) orbit.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
