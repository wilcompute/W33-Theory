#!/usr/bin/env python3
"""Pass4861 — minimal external datum that removes the genuine S3^45 sheet gauge.

Pass4851 proves the class action of C399 is S3^45 : PGSp(4,3).  At each of the
45 recovered GQ points there are three abstract sheet-cells and three incident
quotient lines.  A physical port matching is a bijection between those two
3-sets.  S3 acts simply transitively on the six bijections, so one matching per
point has trivial local stabilizer and kills the entire sheet kernel.  The
stabilizer of a global matching inside S3^45:PGSp is the graph of a unique
correction cocycle and is therefore isomorphic to PGSp.  Adding the independently
certified global chirality/orientation bit reduces that diagonal PGSp to PSp.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4861_PORT_MATCHING_SYMMETRY_BREAK.json'

def compose(p,q):return tuple(p[q[i]] for i in range(3))

def main()->int:
 S3=list(itertools.permutations(range(3)));I=(0,1,2)
 # action on bijections by precomposition on sheet labels is simply transitive
 orbit={compose(I,p) for p in S3};assert len(orbit)==6
 stab_full=[p for p in S3 if compose(I,p)==I];assert len(stab_full)==1
 # weaker local labels leave nontrivial stabilizers
 stab_dist=[p for p in S3 if p[0]==0];assert len(stab_dist)==2
 # parity/cyclic orientation leaves A3=C3
 def parity(p):return sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2
 stab_orient=[p for p in S3 if parity(p)==0];assert len(stab_orient)==3
 out={'pass':4861,'code':'C399=[2025,399,14]_2','intrinsic_class_group':'S3^45 : PGSp(4,3)','local_sheet_kernel':'S3^45',
  'external_datum':'At each of the 45 recovered GQ points, choose a bijection from its three physical sheet-cells to its three incident quotient-line ports.',
  'choices_per_point':6,'local_stabilizer_of_full_matching':1,'weaker_data':{'distinguished_sheet_stabilizer_order':2,'cyclic_orientation_stabilizer_order':3},
  'global_stabilizer':{'port_matching_only':'diagonal/cocycle copy of PGSp(4,3), order 51840','port_matching_plus_global_chirality':'PSp(4,3), order 25920'},
  'proof':'For every g in PGSp and every point, there is a unique local sheet permutation restoring the chosen sheet-to-line bijection after g acts on the incident line pencil. These 45 unique corrections form the graph of a cocycle, so the matching stabilizer projects isomorphically onto PGSp and intersects S3^45 trivially. A local datum with trivial S3 stabilizer must have orbit size at least six; a bijection realizes this minimum.',
  'capability_gain':['canonical physical port for every abstract sheet/line coordinate','deterministic cross-cell router compilation without S3^45 representative ambiguity','hardware placement can preserve the full projective PGSp geometry while removing the local sheet gauge'],
  'invariants_unchanged':['classical C399 parameters [2025,399,14]_2','abstract bounded-distance decoding guarantee','intrinsic code automorphism theorem remains true before external labels are attached'],
  'theorem':'A full three-port matching at each recovered GQ point is the minimal local datum that completely removes the genuine S3^45 sheet kernel. Its stabilizer is a diagonal copy of PGSp(4,3); adding the global chirality bit selects the PSp(4,3) index-two subgroup.',
  'boundary':'This is a symmetry-breaking/compilation theorem. It does not claim that a particular optical or electronic hardware implementation supplies these port labels automatically.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
