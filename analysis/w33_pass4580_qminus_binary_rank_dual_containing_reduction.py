#!/usr/bin/env python3
"""Pass 4580 -- reduce the Q^-(5,q) binary-rank conjecture to one exact code theorem.

For the point-line incidence matrix N of Q^-(5,q)=GQ(q,q^2), q odd, let
C=im(N) in the binary point space.  The candidate rank laws from Passes 4537/4552
are equivalent to

  dim C = q^4+q^2+1,
  C^perp = ker(N^T) is contained in C,
  dim C^perp = q(q^2-q+1).

Under those two incidence-code facts,
rank(N^T N)=dim C-dim C^perp=(q^2+1)(q^2-q+1).
The q=3,5,7 exact anchors satisfy the reduction.  This pass intentionally does
not promote the missing all-q dual-containing/dimension statement to a theorem.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4580_QMINUS_BINARY_RANK_REDUCTION.json'

def formulas(q):
    P=(q+1)*(q**3+1)
    r=q**4+q**2+1
    d=q*(q**2-q+1)
    rho=(q*q+1)*(q*q-q+1)
    assert P-r==d
    assert r-d==rho
    return {'q':q,'points':P,'candidate_rank_N':r,'candidate_dual_dimension':d,'candidate_rank_NtN':rho}

def main()->int:
    c4537=json.loads((ROOT/'data/PART_W33_PASS4537_Q5Q_BINARY_RANK_FRONTIER.json').read_text())
    c4552=json.loads((ROOT/'data/PART_W33_PASS4552_QMINUS5_RANK_THIRD_ANCHOR.json').read_text())
    anchors={a['q']:(a['rank_N'],a['rank_NtN']) for a in c4552['three_exact_anchors']}
    assert anchors=={3:(91,70),5:(651,546),7:(2451,2150)}
    exact=[]
    for q,(r,rho) in sorted(anchors.items()):
        f=formulas(q);d=f['points']-r
        rad=r-rho
        assert r==f['candidate_rank_N'] and rho==f['candidate_rank_NtN']
        assert d==rad==f['candidate_dual_dimension']
        exact.append({**f,'exact_rank_N':r,'exact_rank_NtN':rho,
                      'exact_dim_ker_Nt':d,'exact_dim_imN_intersect_kerNt':rad,
                      'dual_containing_verified_by_dimensions':True})
    # General odd-q line graph is square-zero, independently frozen in Pass 4537.
    assert c4537['general_odd_q_square_zero_theorem']['consequence'].startswith('A^2=0')
    out={
      'pass':4580,
      'exact_anchors':exact,
      'equivalent_missing_theorem':{
        'code':'C=im(N) in F2^(#points)',
        'dimension':'dim C=q^4+q^2+1',
        'dual_containing':'C^perp=ker(N^T) <= C',
        'dual_dimension':'dim C^perp=q(q^2-q+1)',
        'consequence':'rank(N^T N)=dim(C/C^perp)=(q^2+1)(q^2-q+1)'},
      'literature_audit':{
        'status':'NO DIRECT ALL-q CROSS-CHARACTERISTIC BINARY POINT-LINE THEOREM LOCATED',
        'excluded_wrong_route':'Bagchi-Brouwer-Wilbrink O(5,q) concerns the dual of square Sp(4,q), not Q^-(5,q)=GQ(q,q^2).',
        'related_but_insufficient':'Blokhuis-Moorhouse determines defining-characteristic p-ranks for quadric point-hyperplane incidence; Chandler-Sin-Xiang treats symplectic polar spaces. Neither statement is the binary point-line rank needed here for odd q.'},
      'status':'The candidate law is exact at q=3,5,7 and reduced to a single dual-containing incidence-code theorem; infinite proof remains open.',
      'boundary':'A reduction is not a proof of the missing all-q code theorem.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
