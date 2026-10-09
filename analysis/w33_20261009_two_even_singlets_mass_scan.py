"""All parity-even, hypercharge-zero, hidden-gauge-SINGLET *two-field*
VEV extensions of the Pass11796 D-flat 13-field FI support.

Unlike previous meson/antibaryon SU4 supports, each extra field is a
true SU3xSU2xSU4xSU2 singlet. Rational charge basis ensures exact local
U1 D-flat deformation. Necessary colored/up Yukawa masks use
nonnegative REAL insertion parameters (permissive LP).

May find or rule out a rank7 color repair in this specific finite
two-singlet family. NOT sufficient for genuine F-flat superpotential.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
import sys,json
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as F
import sympy as S
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
from w33_20261009_SU4_pair_masks_exact_rational import BASE8,rational
from w33_20261009_SU4_matched_Dflat_extensions import BASE
def certificate():
 raw,prior,fields,support,q=P.load()
 parity=prior['all176_field_parities']
 extra=sorted(n for n,f in fields.items() if
    f['dim']=='1,1,1,1' and not parity[n] and F(q[n][1])==0 and n not in BASE)
 B=S.Matrix.hstack(*(S.Matrix(q[n]) for n in BASE8))
 piv=list(B.T.rref()[1]);Inv=B.extract(piv,list(range(8))).inv()
 fullsupport=S.Matrix.hstack(*(S.Matrix(q[n]) for n in BASE))
 def co(names,neg=False):
  b=sum((S.Matrix(q[n]) for n in names),S.zeros(9,1))
  if neg:b=-b
  v=Inv*b.extract(piv,[0])
  return tuple(rational(x) for x in v[:5]) if B*v==b else None
 assert all(co([n]) is not None for n in extra)
 # A small nonnegative VEV squared in any of these fields is offset
 # by exact U1 charge shifts among BASE; original FI-core stays positive
 # under sufficiently small perturbation.
 assert all(fullsupport.gauss_jordan_solve(-S.Matrix(q[n])) for n in extra)
 basis=json.load(open(ROOT/'data/w33_pass11793_order_four_matter_action.json'))['candidate_three_family_Higgs_basis']
 UP=[(a,b,basis['H_u'][0]) for a in basis['Q'] for b in basis['u_c']]
 down=json.load(open(ROOT/'data/w33_pass11797_11801_five_physical_fronts.json'))['pass11799']['mass_sectors']['d']
 DD=[(a,b) for a in down['rows'] for b in down['columns']]
 targets=[co(t,True) for t in UP+DD]
 matrices=[]
 lookup={}
 for n in extra:
  lookup[n]=np.array(list(map(float,co([n]))))
 for i,(a,b) in enumerate(combinations(extra,2)):
  V=np.column_stack([lookup[a],lookup[b]])
  masks=[]
  for y in targets:
   if y is None:masks.append(0);continue
   feasible=linprog([0.,0.],A_ub=V,b_ub=np.array(list(map(float,y))),
     bounds=[(0,None)]*2,method='highs',
     options={'primal_feasibility_tolerance':1e-9,
              'dual_feasibility_tolerance':1e-9}).success
   masks.append(int(feasible))
  ncol=len(down['columns'])
  up=[masks[k*3:(k+1)*3] for k in range(3)]
  color=[masks[9+k*ncol:9+(k+1)*ncol] for k in range(7)]
  matrices.append(dict(pair=[a,b],
       up_real_cone_matching_rank=P.matching_rank(up),
       colored_real_cone_matching_rank=P.matching_rank(color),
       up_mask=up,colored_mask=color))
  if (i+1)%70==0:print('SINGLET SCAN',i+1,'of',len(extra)*(len(extra)-1)//2,flush=True)
 hist={str(k):v for k,v in Counter((x['up_real_cone_matching_rank'],x['colored_real_cone_matching_rank']) for x in matrices).items()}
 bestcol=max(z['colored_real_cone_matching_rank'] for z in matrices)
 return dict(status='PASS',n_available_even_true_singlets=len(extra),
    extra_field_names=extra,two_field_extensions=len(matrices),
    necessary_entry_tests=79*len(matrices),
    rank_histogram=hist,best_colored_rank=bestcol,
    best_up_rank=max(z['up_real_cone_matching_rank'] for z in matrices),
    candidate_colored_rank_at_least6=[x for x in matrices if x['colored_real_cone_matching_rank']>=6],
    results=matrices,
    theorem='Each parity-even true hidden+SM gauge singlet has its U1 charge in the eight-dimensional old charge span, so paired sufficiently small positive VEVs admit exact local Abelian D-flat support corrections. The screen uses a NONNEGATIVE REAL relaxation of two arbitrary singlet monomial powers and five FI-core constraints; matching ranks are necessary-only upper masks.',
    crucial_limits='No worldsheet R/space-group/oscillator selection, integrality of monomial insertion, actual F-flatness, physical masses, nonperturbative condensates or alternative SM Higgs identification has been inferred.')
if __name__=='__main__':
 o=certificate()
 (ROOT/'data/w33_20261009_two_even_singlets_mass_scan.json').write_text(json.dumps(o,separators=(',',':'))+'\n')
 print('SINGLET DONE',o['n_available_even_true_singlets'],o['two_field_extensions'],o['rank_histogram'],'best color',o['best_colored_rank'])
