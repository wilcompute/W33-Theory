#!/usr/bin/env python3
"""Pass 2311: distinguish SRG relation rank from PGSp permutation rank."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_pass2311_regular_spread_rank_three_obstruction.json'
EXPECTED='88071605fd38c0438928e94d8b0ad35508a5e5fe7de91f19c9450c26973f5663'
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def row(q):
 H=2*q*q*(q**4-1);k=q*(q-2)*(q*q+1)//2
 return {'q':q,'stabilizer_order':H,'predicted_qplus1_valency':k,
         'quotient_floor':H//k,'remainder':H%k,'divides':H%k==0}
def build():
 rows=[row(q) for q in (3,5,7,9,11,13)]
 d={'schema':'w33.pass2311.regular_spread_rank_three_obstruction.v1',
 'status':'PASS_WITH_ASSOCIATION_SCHEME_VS_GROUP_RANK_BOUNDARY',
 'inputs':{'regular_spread_orbit_size':'q^2(q^2-1)/2',
 'regular_spread_stabilizer_order':'2q^2(q^4-1)',
 'qplus1_relation_valency':'q(q-2)(q^2+1)/2',
 'valency_scope':'exact at q=3,5,7; conjectural all odd q beyond the computed cases'},
 'divisibility':{'necessary_condition':'A stabilizer suborbit length must divide the point stabilizer order.',
 'ratio':'|H|/k = 4q(q^2-1)/(q-2)',
 'remainder_argument':'Modulo q-2 the numerator 4q(q^2-1) equals 24, hence q-2 must divide 24.',
 'odd_q_consequence':'Because q-2 is odd, the only positive possibilities are q-2 in {1,3}, so q in {3,5}.',
 'sample_table':rows},
 'exact_conclusions':['At q=7 the completely enumerated q+1 relation has valency 875, which does not divide the regular-spread stabilizer order 235200; therefore the PGSp(4,7) action on the regular-spread orbit is not permutation rank three.',
 'If the Pass-2064 valency formula holds for an odd q, the PGSp action can be permutation rank three only for q=3 or q=5.',
 'A strongly regular relation may still exist without being one stabilizer orbital; association-scheme rank and permutation-group rank must not be conflated.'],
 'literature_scope':{'2026_intersection_result':'For Desarguesian line spreads under field reduction, an intersection containing a pseudo-arc of three lines is forced into the regulus/Segre intersection of q+1 lines.',
 'remaining_uniform_gap':'Exclude intersections of size 0 and 2 and derive the common-neighbor numbers uniformly; the current q=3,5,7 computations do this only casewise.'},
 'checks':{'q3_divides':rows[0]['divides'],'q5_divides':rows[1]['divides'],
 'q7_not_divide':not rows[2]['divides'],'q9_not_divide':not rows[3]['divides'],
 'q11_not_divide':not rows[4]['divides'],'q13_not_divide':not rows[5]['divides'],
 'odd_divisor_argument_only_q3_q5':True},
 'theorem':'The regular-spread q+1 relation cannot be a single point-stabilizer orbital for odd q other than 3 or 5, assuming the recorded valency formula. In the exact q=7 census this proves that the strongly regular graph is not a rank-three PGSp permutation action.',
 'boundary':'This corrects group-action terminology. It does not refute the q=7 strongly regular graph, prove the all-odd-q intersection formulas, or classify the finer stabilizer suborbits.'}
 assert all(d['checks'].values());d['sha256_without_hash_field']=digest(d);return d
def main():
 d=build();assert d['sha256_without_hash_field']==EXPECTED
 assert d==json.loads(OUT.read_text())
 print(json.dumps({'status':d['status'],'certificate':EXPECTED,'q7_remainder':700,'rank3_possible_odd_q':[3,5]},sort_keys=True))
if __name__=='__main__':main()
