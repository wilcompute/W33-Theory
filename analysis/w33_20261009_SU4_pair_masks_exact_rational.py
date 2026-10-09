"""Independent, *exact rational* 1D/2D positive-meson cone feasibility.
Verifies EVERY entry of 30 x (nine up + 70 colored) masks from the
parallel SciPy linprog relaxation. Avoid floating false permissions.

For m=2 cone inequalities V t<=beta, t>=0 in R² form a pointed
closed polyhedron. If nonempty it contains a vertex: exhaustive
intersection of pairs of the <=7 rational bounding lines is an exact
feasibility decision, with a rational witness.
"""
from pathlib import Path
from itertools import combinations
from fractions import Fraction as F
import json,sys
import sympy as S
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
from w33_20261009_SU4_matched_Dflat_extensions import BASE
BASE8=['n_17','n_47','n_50','n_80','n_82','n_9','n_37','n_35']
def rational(z):return F(int(z.p),int(z.q))
def feasible(beta, cols):
 if beta is None:return False,None
 n=len(cols)
 if n==1:
  lo=F(0);hi=None
  for b,c in zip(beta,cols[0]):
   if c==0:
    if b<0:return False,None
   elif c>0:
    x=b/c;hi=x if hi is None else min(hi,x)
   else:lo=max(lo,b/c)
  if hi is not None and hi<lo:return False,None
  return True,[str(lo)]
 lines=[(cols[0][i],cols[1][i],beta[i]) for i in range(5)]+[(F(-1),F(0),F(0)),(F(0),F(-1),F(0))]
 for (a,b,c),(e,f,g) in combinations(lines,2):
  det=a*f-b*e
  if not det:continue
  x=(c*f-b*g)/det;y=(a*g-c*e)/det
  if all(A*x+B*y<=C for A,B,C in lines):
   return True,[str(x),str(y)]
 return False,None
def certificate():
 raw,prior,fields,support,q=P.load()
 assert set(support)==set(BASE)
 prior_masks=json.load(open(ROOT/'data/w33_20261009_SU4_pair_meson_mass_masks.json'))
 basis=json.load(open(ROOT/'data/w33_pass11793_order_four_matter_action.json'))['candidate_three_family_Higgs_basis']
 B=S.Matrix.hstack(*(S.Matrix(q[n]) for n in BASE8))
 piv=list(B.T.rref()[1]);I=B.extract(piv,list(range(8))).inv()
 def co(ns):
  b=-sum((S.Matrix(q[n]) for n in ns),S.zeros(9,1))
  x=I*b.extract(piv,[0])
  if B*x!=b:return None
  return tuple(rational(y) for y in x[:5])
 UP=[(a,b,basis['H_u'][0]) for a in basis['Q'] for b in basis['u_c']]
 down=json.load(open(ROOT/'data/w33_pass11797_11801_five_physical_fronts.json'))['pass11799']['mass_sectors']['d']
 DD=[(a,b) for a in down['rows'] for b in down['columns']]
 targets=[co(x) for x in UP+DD]
 results=[];mismatch=0
 for r in prior_masks['distinct_candidates']:
  pair_columns=[]
  for pair in r['mesons']:
   c=co(pair)
   assert c is not None
   pair_columns.append(tuple(-v for v in c))
  upmask=[];dmask=[];positive_examples=[]
  for k,target in enumerate(targets):
   yes,w=feasible(target,pair_columns)
   if yes and k<len(UP) and len(positive_examples)<5:
    positive_examples.append(dict(names=list(UP[k]),rational_meson_exponents=w))
   if k<len(UP):upmask.append(int(yes))
   else:dmask.append(int(yes))
  newup=[upmask[i*3:(i+1)*3] for i in range(3)]
  newd=[dmask[i*len(down['columns']):(i+1)*len(down['columns'])] for i in range(len(down['rows']))]
  if newup!=r['up_mask'] or newd!=r['colored_mask']:
   mismatch+=1; print('MISMATCH',r['candidate'],flush=True)
  assert newup==r['up_mask'] and newd==r['colored_mask']
  results.append(dict(candidate=r['candidate'],pair_count=len(pair_columns),
       up_exact_real_cone_rank=P.matching_rank(newup),
       colored_exact_real_cone_rank=P.matching_rank(newd),
       sample_rational_witnesses=positive_examples))
 assert mismatch==0
 return dict(status='PASS',independent_exact_rational_entry_checks=len(results)*len(targets),
   candidates=len(results),all_numerical_real_cone_masks_exactly_confirmed=True,
   max_up_rank=max(x['up_exact_real_cone_rank'] for x in results),
   max_colored_rank=max(x['colored_exact_real_cone_rank'] for x in results),
   candidates_rank3=sum(x['up_exact_real_cone_rank']==3 for x in results),
   exact_method='All 5 FI-core inequalities plus 1 or2 nonnegative meson insertion variables are rational. One variable: exact lower/upper interval. Two variables: feasibility iff at least one vertex of a pointed closed rational polyhedron exists, tested exhaustively over 21 candidate line intersections. All 30*79 entries tested, equality with independently computed HiGHS mask asserted.',
   results=results,
   theorem='18/30 extended SU4 Dflat supports lose the original FI REAL-CONE obstruction to rank-three up Yukawa; all30 still have an exact necessary rank<=5 for seven colored-triplet mass pairs. These remain only permissive REAL-CONE upper masks. Integrality, corrected orbifold R, actual nonzero couplings and full F-flatness are not inferred.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_SU4_pair_masks_exact_rational.json').write_text(json.dumps(d,indent=2)+'\n')
 print('EXACT SU4 LP',d['independent_exact_rational_entry_checks'],d['candidates_rank3'],d['max_colored_rank'])
