#!/usr/bin/env python3
"""Pass5208: exact reduction of the odd-q dual-grid spanning conjecture.

Pass5187/5189 give the all-q inclusion D=<dual grids> <= C(W)^perp.  Pass5130
quotes the all-odd-prime-power binary incidence-rank theorem

  rank_2 N = 1 + q(q+1)^2/2,

so for odd q

  dim C(W)^perp = q(q^2+1)/2.

Therefore the proposed odd-q spanning theorem

  <dual grids> = C(W)^perp

is equivalent to the single binary rank formula

  rank_2 F = q(q^2+1)/2,

where F is point x dual-grid incidence.  The repo has exact prime anchors
q=3,5,7,11 attaining 15,65,175,671.  At q=5 Pass5188 proves equality.

This pass deliberately does not promote the finite-anchor pattern to all odd q.
The even-characteristic boundary is known to be genuinely different: for even
q>=4 the binary line-code dual can fail to be spanned by its minimum dual-grid
words.  Thus any proof must use an odd-characteristic module/rank argument, not
a characteristic-free minimum-shell argument.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5208_ODDQ_DUALGRID_SPANNING_RANK_REDUCTION.json'

def target(q): return q*(q*q+1)//2

def main():
    anchors={3:15,5:65,7:175,11:671}
    for q,r in anchors.items():assert r==target(q)
    out={'pass':5208,'status':'THEOREM_ODDQ_DUALGRID_SPANNING_EQUIVALENT_TO_BINARY_RANK_FORMULA',
      'domain':'odd prime powers q',
      'known_inclusion':'The dual-grid span D is contained in C(W)^perp because every W-line meets every dual grid evenly.',
      'Pass5130_incidence_rank':'rank_2 N = 1 + q(q+1)^2/2',
      'Pass5130_dual_dimension':'dim C(W)^perp = q(q^2+1)/2',
      'equivalence':'D=C(W)^perp iff rank_2(F)=q(q^2+1)/2 for the point x dual-grid incidence matrix F.',
      'exact_prime_anchors':{str(q):{'rank_F2_F':r,'target':target(q),'spans_full_dual':True} for q,r in anchors.items()},
      'q5_theorem':'Pass5188 proves the q=5 equality and code [156,65,12]_2.',
      'even_characteristic_firewall':'Known even-q coding results show that for q>=4 the full line-code dual need not be spanned by its minimum dual-grid words; no characteristic-free spanning theorem is possible.',
      'open_step':'Prove the binary p-rank formula for the dual-grid design in cross characteristic 2 for every odd prime power q.',
      'boundary':'All-odd spanning remains a conjecture after this exact reduction; finite anchors are not promoted to a theorem.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
