"""Mixed hidden SU4 antibaryon + two fundamental/antifundamental
mesons: scan 5*4*3=60 exact local D-flat support patterns.

Satisfy hidden SU4 D by anti columns sqrt(t+s1)e1,
sqrt(t+s2)e2,sqrt(t)e3,sqrt(t)e4 and fund columns
sqrt(s1)e1,sqrt(s2)e2. Then anti anti† -fund fund†=tI.
Original Abelian Dflat core shift is exactly linear in (t,s1,s2).

Relax holomorphic meson+antibaryon insertion exponents to nonnegative
REALS (LP). Necessary upper bounds only, not physical mass existence.
"""
from pathlib import Path
import sys,json
from itertools import combinations,permutations
from fractions import Fraction as F
import sympy as S
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
from w33_20261009_SU4_pair_masks_exact_rational import BASE8, rational
from w33_20261009_SU4_matched_Dflat_extensions import BASE
def certificate():
 raw,prior,fields,support,q=P.load()
 parity=prior['all176_field_parities']
 anti=['n_44','n_55','n_66','n_68','n_73']
 assert all(not parity[n] for n in anti+['n_69','n_74'])
 basis=json.load(open(ROOT/'data/w33_pass11793_order_four_matter_action.json'))['candidate_three_family_Higgs_basis']
 down=json.load(open(ROOT/'data/w33_pass11797_11801_five_physical_fronts.json'))['pass11799']['mass_sectors']['d']
 UP=[(a,b,basis['H_u'][0]) for a in basis['Q'] for b in basis['u_c']]
 DD=[(a,b) for a in down['rows'] for b in down['columns']]
 B=S.Matrix.hstack(*(S.Matrix(q[n]) for n in BASE8));M=S.Matrix.hstack(*(S.Matrix(q[n]) for n in BASE))
 piv=list(B.T.rref()[1]);inv=B.extract(piv,list(range(8))).inv()
 def coord(ns,minus=True):
  v=sum((S.Matrix(q[n]) for n in ns),S.zeros(9,1))
  if minus:v=-v
  c=inv*v.extract(piv,[0])
  return tuple(rational(x) for x in c[:5]) if B*c==v else None
 targets=[coord(x) for x in UP+DD]
 def screen(gen):
  v=np.array([list(map(float,coord(x,False))) for x in gen]).T
  ans=[]
  for b in targets:
   if b is None:ans.append(0);continue
   yes=linprog(np.zeros(len(gen)),A_ub=v,b_ub=np.array(list(map(float,b))),
       bounds=[(0,None)]*len(gen),method='highs').success
   ans.append(int(yes))
  return ans
 choices=[]
 for quad in combinations(anti,4):
  qshift=coord(quad)
  assert qshift is not None
  for ai,aj in permutations(quad,2):
   gen=[('n_69',ai),('n_74',aj),quad]
   for names in gen:
    assert coord(names,False) is not None
   # Exact three independent rank-one support charge shifts in original FI span
   for names in gen:
    rhs=-sum((S.Matrix(q[n]) for n in names),S.zeros(9,1))
    corr,free=M.gauss_jordan_solve(rhs)
    assert M*corr.subs({x:0 for x in free})==rhs
   mask=screen(gen)
   up=[mask[3*i:3*(i+1)] for i in range(3)]
   col=[mask[9+len(down['columns'])*i:9+len(down['columns'])*(i+1)] for i in range(len(down['rows']))]
   choices.append(dict(four_anti=list(quad),anti_for_fund69=ai,anti_for_fund74=aj,
      up_rank_relaxed=P.matching_rank(up),colored_rank_relaxed=P.matching_rank(col),
      up_mask=up,colored_mask=col,generators=[list(x) for x in gen]))
 assert len(choices)==60
 from collections import Counter
 hist={str(x):y for x,y in Counter((a['up_rank_relaxed'],a['colored_rank_relaxed']) for a in choices).items()}
 return dict(status='PASS',candidate_Dflat_supports=60,real_cone_masks=60*79,
     histogram_up_colored_rank=hist,maximum_up_rank=max(x['up_rank_relaxed'] for x in choices),
     maximum_colored_rank=max(x['colored_rank_relaxed'] for x in choices),
     candidate_examples=[x for x in choices if x['colored_rank_relaxed']==max(y['colored_rank_relaxed'] for y in choices)][:7],
     choices=choices,
     exact_SU4_D_flat='With anti color vectors sqrt(t+s1)e1,sqrt(t+s2)e2,sqrt(t)e3,sqrt(t)e4 and two fundamental vectors sqrt(s1)e1,sqrt(s2)e2, the SU4 Hermitian moment-map difference is t*I4, exactly traceless-zero; all 9 U1 charges can be adjusted by rational perturbation of original FI-positive support, for sufficiently small t,s1,s2>0.',
     boundary='Relaxed real-cone upper masks allow arbitrary nonnegative real powers of the two nonzero mesons plus anti baryon. Holomorphic integer exponents, extra hidden SU4 invariant identities, nonR/R/point-group/CFT constraints and F-flatness remain open. Does not prove physical mass repair.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_SU4_mixed_baryon_mesons.json').write_text(json.dumps(d,indent=2)+'\n')
 print('SU4 MIXED',d['histogram_up_colored_rank'],'best',d['maximum_colored_rank'],d['maximum_up_rank'])
