"""Alternative D-flat support: four independent SU(4) antifundamental
VEVs of equal norm on orthogonal color basis, generating an epsilon
antibaryon. Test all 5 choices among parity-even SM-neutral -4 fields.

Exact U1 charge-span positivity for sufficiently small amplitude;
the full holomorphic SU4 invariant algebra here has the baryon
epsilon A_i A_j A_k A_l. Relax the 79 relevant Yukawa and colored mass
necessary charge constraints to nonnegative REAL insertion powers.
All actual integer/R/CFT/F-term conditions remain open.
"""
from pathlib import Path
import sys,gzip,json
from itertools import combinations
from fractions import Fraction as F
import sympy as S
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
from w33_20261009_SU4_pair_masks_exact_rational import feasible,rational,BASE8
from w33_20261009_SU4_matched_Dflat_extensions import BASE
def certificate():
 raw,prior,fields,support,q=P.load();assert set(support)==set(BASE)
 parity=prior['all176_field_parities']
 anti=[n for n,f in fields.items() if f['dim']=='1,1,-4,1' and not parity[n] and F(q[n][1])==0]
 assert anti==['n_44','n_55','n_66','n_68','n_73'],anti
 B=S.Matrix.hstack(*(S.Matrix(q[n]) for n in BASE8))
 assert B.rank()==8
 piv=list(B.T.rref()[1]);inv=B.extract(piv,list(range(8))).inv()
 def coords(ns,negative=True):
  b=sum((S.Matrix(q[n]) for n in ns),S.zeros(9,1))
  if negative:b=-b
  x=inv*b.extract(piv,[0])
  return tuple(rational(v) for v in x[:5]) if B*x==b else None
 basis=json.load(open(ROOT/'data/w33_pass11793_order_four_matter_action.json'))['candidate_three_family_Higgs_basis']
 UP=[(a,b,basis['H_u'][0]) for a in basis['Q'] for b in basis['u_c']]
 down=json.load(open(ROOT/'data/w33_pass11797_11801_five_physical_fronts.json'))['pass11799']['mass_sectors']['d']
 DD=[(a,b) for a in down['rows'] for b in down['columns']]
 all_targets=[coords(t) for t in UP+DD]
 M=S.Matrix.hstack(*(S.Matrix(q[n]) for n in BASE))
 out=[]
 for subset in combinations(anti,4):
  baryon_coords=coords(subset,negative=False)
  assert baryon_coords is not None
  rhs=-sum((S.Matrix(q[n]) for n in subset),S.zeros(9,1))
  delta,free=M.gauss_jordan_solve(rhs)
  delta=delta.subs({f:0 for f in free})
  assert M*delta==rhs
  # For each x, four anti VEVs are sqrt(x) e_1,...,sqrt(x)e_4,
  # so sum A_i A_i†=x I_4 => all 15 su4 D terms zero.
  masks=[]
  for target in all_targets:
   yes,_=feasible(target,[baryon_coords])
   masks.append(int(yes))
  mu=[masks[i*3:(i+1)*3] for i in range(3)]
  mc=[masks[9+i*len(down['columns']):9+(i+1)*len(down['columns'])] for i in range(len(down['rows']))]
  out.append(dict(antibaryon_fields=list(subset),
      baryon_FI5_charge_coordinates=list(map(str,baryon_coords)),
      FI_support_shift={n:str(delta[i]) for i,n in enumerate(BASE)},
      up_mask=mu,up_real_cone_matching_rank=P.matching_rank(mu),
      colored_mask=mc,colored_real_cone_matching_rank=P.matching_rank(mc)))
 return dict(status='PASS',
     parity_even_SU4_antifundamental_fields=anti,antibaryon_supports=len(out),
     exact_mass_entries_screened=len(out)*len(all_targets),
     worst_colored_mass_rank=max(x['colored_real_cone_matching_rank'] for x in out),
     best_up_rank=max(x['up_real_cone_matching_rank'] for x in out),
     results=out,
     math_result='Each quadruple is a local exact Abelian+hidden-SU4 D-flat deformation of original FI-positive support for sufficiently small t>0: turn on four independent -4 color vectors sqrt(t)*unit basis e1..e4; their total hidden-SU4 moment map is t I4, and compensate 9 U1 charges by exact rational first-order shifts on original support. All fields even under full-field parity.',
     string_boundary='Color-baryon epsilon tensor exists for four distinct -4 fields. The screening ignores quantization/integer exponents, exact worldsheet string rules, mass coefficients and all F terms. Candidates need not remain true supersymmetric vacua or solve rank deficits.',
     subtlety='SU4 is hidden gauge; a nonzero anti-baryon with all four color directions fully breaks SU4, and the corresponding new matter spectrum must be recomputed.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_antibaryon_Dflat_mass_scan.json').write_text(json.dumps(d,indent=2)+'\n')
 print('ANTI BARYON',[(r['antibaryon_fields'],r['up_real_cone_matching_rank'],r['colored_real_cone_matching_rank']) for r in d['results']])
