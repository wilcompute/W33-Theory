#!/usr/bin/env python3
"""Pass5238: exact q=5 footprint minimum-distance closure from the weight-8 Tanner shell.

Pass5230 gives the complete 24,375-word weight-8 shell of C_F^perp.  Each
coordinate lies in 600 checks.  Pair co-degrees are 25 on R1, 5 on R2, and 0
on R3, so the maximum pair co-degree is 25.

Let S be the support of a nonzero primal word and, for each weight-8 check H,
write r_H=|S cap H|.  Orthogonality makes every r_H even.  Therefore

  C(r_H,2) >= r_H/2.

Summing first incidences gives sum_H r_H = 600 |S|.  Summing pair incidences
and using pair co-degree <=25 gives

  300 |S| <= sum_H C(r_H,2) <= 25 C(|S|,2).

Thus |S|>=25.  Pass5209 already supplies 156 point-footprint codewords of
weight 25, hence C_F=[325,65,25]_2.

Pass5207 says any P-heavy q=5 apartment-code word of weight 625 would induce a
nonzero footprint word of weight <=24, now impossible.  Pass5191 proves every
P-heavy-free weight-625 word is a chamber star.  Therefore the complete q=5
weight-625 shell consists exactly of chamber stars.

This closes the equality shell only.  The strict sub-625 apartment-code problem
still has the independent chamber-leader-36 frontier.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5238_Q5_FOOTPRINT_TANNER_MOMENT_DISTANCE.json'

def main():
    n=325; k=65
    checks=24375; check_weight=8; coord_degree=600; pair_codegree_max=25
    assert checks*check_weight==n*coord_degree==195000
    # For support size w, 300 w <= 25*C(w,2) iff w>=25 for w>0.
    def possible(w): return 300*w <= pair_codegree_max*(w*(w-1)//2)
    assert not any(possible(w) for w in range(1,25))
    assert possible(25) and 300*25==25*(25*24//2)==7500
    out={
      'pass':5238,
      'status':'THEOREM_Q5_FOOTPRINT_CODE_IS_325_65_25_AND_WEIGHT625_SHELL_IS_STARS',
      'footprint_code':'C_F=[325,65,25]_2',
      'dual_weight8_shell':{'size':checks,'check_weight':check_weight,'coordinate_degree':coord_degree,'maximum_pair_codegree':pair_codegree_max},
      'moment_proof':[
        'For every primal support S and every weight-8 dual check H, r_H=|S cap H| is even.',
        'For even r, C(r,2)>=r/2.',
        'sum_H r_H=600|S|.',
        'sum_H C(r_H,2)<=25 C(|S|,2).',
        'Hence 300|S|<=25 C(|S|,2), so every nonzero word has |S|>=25.'
      ],
      'upper_bound':'Pass5209 provides 156 point-footprint codewords of weight 25, so d=25.',
      'equality_shell_chain':'Pass5207: P-heavy weight625 => nonzero footprint wt<=24, impossible. Pass5191: every P-heavy-free weight625 word is a chamber star.',
      'q5_weight625_shell':'exactly the chamber stars',
      'strict_boundary':'The apartment-code d=625 theorem is not yet closed: sub-625 words with minimum chamber leader >=36 remain open.',
      'method_lemma':'More generally, an even-check family with coordinate degree R and maximum pair co-degree Lambda gives d>=1+ceil(R/Lambda) by the same two-moment squeeze.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
