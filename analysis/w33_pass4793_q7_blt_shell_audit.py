#!/usr/bin/env python3
"""Pass 4793 — q=7 minimum-shell BLT classification audit.

Pass 4754 proved d(ker_F2 A_*(W(3,q)))=q+1 for odd q, and Pass 4778
identified equality with the BLT condition.  Betten's complete small-order BLT
classification gives exactly two PΓO(5,7)-equivalence classes at q=7, Linear
and Fi/K2, with full stabilizer orders 5376 and 384.  This script freezes the
resulting shell-class arithmetic without silently upgrading it to a PSp orbit
classification.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4793_Q7_BLT_SHELL.json'
q=7
# q is prime, so the semilinear field automorphism factor h is 1.
full_group=q**4*(q**4-1)*(q**2-1)
psp=full_group//2
classes=[('Linear',5376),('Fi/K2',384)]
orbits=[(name,full_group//stab) for name,stab in classes]
assert full_group==276_595_200 and psp==138_297_600
assert orbits==[('Linear',51_450),('Fi/K2',720_300)]
assert sum(n for _,n in orbits)==771_750
out={
 'pass':4793,
 'q':7,
 'kernel_minimum_distance':8,
 'identification':'minimum weight-8 kernel words are exactly BLT-sets',
 'prior_art_source':'Anton Betten, A Classification of BLT-sets of Small Order, q=7 table',
 'full_projective_orthogonal_group_order':full_group,
 'PSp_order':psp,
 'complete_equivalence_classes':[
   {'name':'Linear','full_stabilizer_order':5376,'full_equivalence_class_size':51450},
   {'name':'Fi/K2','full_stabilizer_order':384,'full_equivalence_class_size':720300}],
 'complete_minimum_shell_size_under_full_equivalence_classes':771750,
 'theorem':'At q=7 the complete minimum shell of ker_F2 A_*(W(3,7)) has exactly two classes under the full projective orthogonal equivalence: Linear and Fi/K2, of sizes 51,450 and 720,300.',
 'boundary':'BLT class names/completeness and stabilizer orders are prior art. This pass transfers that complete classification to the line-kernel minimum shell using the independently proved minimum-word=BLT equivalence. It does not claim that either full class remains one PSp orbit; that finer index-two split is left unpromoted until independently certified.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
