"""Search 3 additional parity-even full gauge singlets beyond the old FI
support for exact NONNEGATIVE INTEGER charge-neutral Yukawa monomials.

Seed from eight 2-singlet pairs that repaired colored-mass
*integer* matching but not up rank. Test all 3-singlet extensions
by scipy HiGHS mixed-integer feasibility, bounds total exponent<=72.
Every positive candidate witness is reverified by exact integer
charge multiplication. Negative MILP flags are bounded-degree only.

No string R/space-group/oscillator or F-flatness yet.
"""
import json,sys,math
from pathlib import Path
from itertools import combinations
from collections import Counter
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
FI=['n_17','n_47','n_50','n_80','n_82']
def certificate():
 raw,prior,fields,support,q=P.load()
 seeds=json.load(open(ROOT/'data/w33_20261009_two_singlet_all_order_integer_semigroup.json'))['source_singlet_pairs']
 extras=json.load(open(ROOT/'data/w33_20261009_two_even_singlets_mass_scan.json'))['extra_field_names']
 b=json.load(open(ROOT/'data/w33_pass11793_order_four_matter_action.json'))['candidate_three_family_Higgs_basis']
 up=[(a,c,b['H_u'][0]) for a in b['Q'] for c in b['u_c']]
 den=math.lcm(*(x.denominator for vec in q.values() for x in vec))
 iq={n:np.array([int(den*x) for x in z],dtype=np.int64) for n,z in q.items()}
 targets=[-sum((iq[n] for n in triple),np.zeros(9,dtype=np.int64)) for triple in up]
 seen=set();rows=[]
 for a,bb in seeds:
  for c in extras:
   if c in (a,bb):continue
   triple=tuple(sorted((a,bb,c)))
   if triple in seen:continue
   seen.add(triple)
   names=FI+list(triple)
   A=np.stack([iq[n] for n in names],axis=1)
   candidates=[];solver_undecided=0
   for ti,target in enumerate(targets):
    result=milp(np.ones(8),integrality=np.ones(8),
      bounds=Bounds(np.zeros(8),np.full(8,72.)),
      constraints=LinearConstraint(A,target,target),
      options={'time_limit':1.5,'mip_rel_gap':0.})
    if result.x is not None and result.status==0:
     x=np.rint(result.x).astype(np.int64)
     assert np.array_equal(A@x,target) and np.all(x>=0) and np.all(x<=72)
     candidates.append(dict(target=list(up[ti]),index=ti,positive_integer_witness={names[j]:int(x[j]) for j in range(8) if x[j]>0},degree=int(sum(x))))
    elif result.status!=2:
     solver_undecided+=1
   mask=[[int(3*i+j in [e['index'] for e in candidates]) for j in range(3)] for i in range(3)]
   rank=P.matching_rank(mask)
   rows.append(dict(triple=list(triple),integer_up_matching_rank=rank,
       witnessed_Yukawa=candidates,unresolved_solver_entries=solver_undecided))
   if len(rows)%35==0:print('TRIPLES',len(rows),'rank3',sum(x['integer_up_matching_rank']==3 for x in rows),flush=True)
 hist=dict(Counter(str(x['integer_up_matching_rank']) for x in rows))
 matches=[x for x in rows if x['integer_up_matching_rank']==3]
 return dict(status='PASS',checked_distinct_triplets=len(rows),max_individual_field_exponent=72,
  rank_histogram_from_positive_integer_witnesses=hist,
  triple_up_rank3_integer_witnesses=matches,
  total_solver_undecided=sum(x['unresolved_solver_entries'] for x in rows),
  complete_candidate_rows=rows,
  theorem='Every reported nonzero entry is an exact integer U1 gauge-neutral holomorphic insertion witness, checked by A*x=-charge(target). Triple rank3 means a matching of THREE such independently allowed charge monomials. This does not establish nonzero string worldsheet coefficients, corrected R/nonR/space-group constraints, actual rank3 Yukawa or F-flatness.',
  negative_boundary='Solver no-witness is not an all-order no-go: search limits each generator exponent to 72 and uses a finite time limit. Non-SM field identification and full string invariants remain untested.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_three_even_singlets_integer_search.json').write_text(json.dumps(d,separators=(',',':'))+'\n')
 print('TRIPLE SEARCH',d['checked_distinct_triplets'],d['rank_histogram_from_positive_integer_witnesses'],'undecided',d['total_solver_undecided'])
 print('TOP',[(r['triple'],[a['degree'] for a in r['witnessed_Yukawa']]) for r in d['triple_up_rank3_integer_witnesses'][:10]])
