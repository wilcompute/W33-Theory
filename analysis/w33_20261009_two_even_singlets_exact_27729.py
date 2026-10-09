"""Exact rational audit of all 351 ×79 (27729) necessary
two-even-gauge-singlet insertion real-cone masks. Independently
reproduces the floating SciPy discovery.

The two extra fields are TRUE hidden and SM non-Abelian singlets, so
there is no hidden SU4 tensor contraction obstruction of prior track.
Integers, R selection, worldsheet amplitude and F-flatness OPEN.
"""
import json,sys
from pathlib import Path
from fractions import Fraction as F
import sympy as S
from collections import Counter
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
from w33_20261009_SU4_pair_masks_exact_rational import BASE8,rational,feasible
def certificate():
 raw,pr,fields,support,q=P.load()
 original=json.load(open(ROOT/'data/w33_20261009_two_even_singlets_mass_scan.json'))
 basis=json.load(open(ROOT/'data/w33_pass11793_order_four_matter_action.json'))['candidate_three_family_Higgs_basis']
 down=json.load(open(ROOT/'data/w33_pass11797_11801_five_physical_fronts.json'))['pass11799']['mass_sectors']['d']
 up=[(a,b,basis['H_u'][0]) for a in basis['Q'] for b in basis['u_c']]
 DD=[(a,b) for a in down['rows'] for b in down['columns']]
 B=S.Matrix.hstack(*(S.Matrix(q[n]) for n in BASE8))
 piv=list(B.T.rref()[1]);inv=B.extract(piv,list(range(8))).inv()
 def coords(names,negative=False):
  v=sum((S.Matrix(q[n]) for n in names),S.zeros(9,1))
  if negative:v=-v
  x=inv*v.extract(piv,[0])
  return tuple(rational(y) for y in x[:5]) if B*x==v else None
 targets=[coords(x,True) for x in up+DD]
 charge={n:coords([n],False) for n in original['extra_field_names']}
 assert all(x is not None for x in charge.values())
 summary=[];witness={}
 for i,r in enumerate(original['results']):
  a,b=r['pair']
  cols=[charge[a],charge[b]]
  verdict=[];picked=[]
  for j,v in enumerate(targets):
   okay,win=feasible(v,cols)
   verdict.append(int(okay))
   if okay and j<9 and len(picked)<3:picked.append(dict(up_type=list(up[j]),rational_extra_singlet_exponents=win))
  n=10
  mu=[verdict[j*3:(j+1)*3] for j in range(3)]
  mc=[verdict[9+j*n:9+(j+1)*n] for j in range(7)]
  assert mu==r['up_mask'] and mc==r['colored_mask'],(a,b)
  summary.append(dict(pair=[a,b],up_rank=P.matching_rank(mu),colored_rank=P.matching_rank(mc)))
  if P.matching_rank(mu)==3 and P.matching_rank(mc)==7:
   witness[a+'_'+b]=dict(charge_generator_1=[str(t) for t in cols[0]],
      charge_generator_2=[str(t) for t in cols[1]],
      sample_up_witnesses=picked)
  if (i+1)%80==0:print('RATIONAL PAIRS',i+1,flush=True)
 hist={str(k):v for k,v in Counter((x['up_rank'],x['colored_rank']) for x in summary).items()}
 assert len(summary)==351
 assert len(witness)==8
 return dict(status='PASS',verified_pairs=351,exact_rational_entry_checks=351*79,
  integerless_relaxed_rank_histogram=hist,
  exact_double_rank_repair_pairs=[x['pair'] for x in summary if x['up_rank']==3 and x['colored_rank']==7],
  exact_charge_coordinates_and_rational_witnesses=witness,
  all_HiGHS_masks_exactly_reproduced=True,
  theorem='All 27729 necessary TWO-SINGLET, nonnegative REAL insertions independently verified using Fraction vertices. Eight named D-flat-support candidates meet up rank3 AND colored rank7 matching necessary conditions. This is not an integer holomorphic gauge-invariant superpotential, not an exact CFT selection-rule calculation and not physical mass evidence.',
  source='Complete Pass11797 benchmark; no asserted F-flatness or nonzero worldsheet coefficients.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_two_even_singlets_exact_27729.json').write_text(json.dumps(d,indent=2)+'\n')
 print('DONE SINGLET EXACT',d['exact_rational_entry_checks'],d['integerless_relaxed_rank_histogram'],d['exact_double_rank_repair_pairs'])
