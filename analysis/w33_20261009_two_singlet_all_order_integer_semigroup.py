"""ALL-ORDER exact integer U1 semigroup membership on eight promising
fully gauge-singlet extensions, using source Pass11797 support
invariant ring (5 FI charged fields + neutral x,y,M).

For 7 charge columns rank6, every charge solution is x0+t*v with
primitive integer null vector v. Use Bezout w.v=1 to characterize
integer solutions x=b+k*v, b=x0-(w.x0)v. If b not integral,
no integer solution at ANY order; if integral, intersect all exact
linear nonnegativity inequalities to determine whether k exists.
This is truly UNBOUNDED degree for these named charged generators.

CFT R/space group still absent; no F-flatness.
"""
from pathlib import Path
import sys,json,math
from fractions import Fraction as F
import sympy as S
from collections import Counter
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
FI=['n_17','n_47','n_50','n_80','n_82']
def bezout(vector):
 w=[0]*len(vector);g=0
 for i,v in enumerate(vector):
  aa,bb,h=S.gcdex(g,v)
  w=[int(aa)*z for z in w]
  w[i]+=int(bb)
  g=int(h)
 assert g==1 and sum(x*y for x,y in zip(w,vector))==1
 return w
def solve_positive_integer(A,target):
 if A.row_join(target).rank()>A.rank():return None,'charge_span'
 x,free=A.gauss_jordan_solve(target)
 if len(free)==0:
  if all(y.q==1 and y>=0 for y in x):
   return [int(y) for y in x],'unique'
  return None,'unique_negative_or_fractional'
 assert len(free)==1
 v0=A.nullspace()[0]
 den=math.lcm(*(int(z.q) for z in v0))
 v=[int(z*den) for z in v0]
 gg=math.gcd(*v)
 v=[z//gg for z in v]
 if next(y for y in v if y)!=abs(next(y for y in v if y)):
  v=[-z for z in v]
 w=bezout(v)
 z=x.subs({f:0 for f in free})
 t0=sum(w[i]*z[i] for i in range(len(v)))
 b=[z[i]-t0*v[i] for i in range(len(v))]
 if not all(y.q==1 for y in b):
  return None,'nonintegral_lattice_coset'
 b=[int(y) for y in b]
 lo=None;hi=None
 for p,slope in zip(b,v):
  if slope==0:
   if p<0:return None,'fixed_negative'
  elif slope>0:
   t=math.ceil(F(-p,slope));lo=t if lo is None else max(lo,t)
  else:
   t=math.floor(F(p,-slope));hi=t if hi is None else min(hi,t)
 if lo is not None and hi is not None and lo>hi:return None,'positive_cone_empty'
 sumv=sum(v)
 if sumv>=0:
  k=lo if lo is not None else (hi if hi is not None else 0)
 else:
  k=hi if hi is not None else (lo if lo is not None else 0)
 out=[b[i]+k*v[i] for i in range(len(v))]
 assert all(z>=0 for z in out) and A*S.Matrix(out)==target
 return out,'integer_positive'
def certificate():
 raw,prior,fields,support,q=P.load()
 sources=json.load(open(ROOT/'data/w33_20261009_two_even_singlets_exact_27729.json'))
 previous=json.load(open(ROOT/'data/w33_20261009_two_singlet_exact_degree24_integer_gate.json'))
 pairs=sources['exact_double_rank_repair_pairs']
 basis=json.load(open(ROOT/'data/w33_pass11793_order_four_matter_action.json'))['candidate_three_family_Higgs_basis']
 up=[(a,b,basis['H_u'][0]) for a in basis['Q'] for b in basis['u_c']]
 down=json.load(open(ROOT/'data/w33_pass11797_11801_five_physical_fronts.json'))['pass11799']['mass_sectors']['d']
 col=[(a,b) for a in down['rows'] for b in down['columns']]
 targets=up+col
 results=[]
 for pair in pairs:
  A=S.Matrix.hstack(*(S.Matrix(q[n]) for n in FI+pair))
  assert A.rank()==6
  status=Counter();yes=[];witnesses=[]
  for j,t in enumerate(targets):
   b=-sum((S.Matrix(q[n]) for n in t),S.zeros(9,1))
   x,s=solve_positive_integer(A,b)
   status[s]+=1
   if x is not None:
    yes.append(j)
    witnesses.append(dict(target=list(t),target_index=j,
      minimum_total_charged_insertion_degree=sum(x),exponents={n:e for n,e in zip(FI+pair,x) if e}))
  maskup=[[int(i*3+j in yes) for j in range(3)] for i in range(3)]
  maskcol=[[int(9+i*10+j in yes) for j in range(10)] for i in range(7)]
  d24=next(x for x in previous['exact_integer_exponent_candidate_pairs'] if x['pair']==pair)
  assert all(maskup[i][j]>=d24['up_integer_U1_mask'][i][j] for i in range(3) for j in range(3))
  assert all(maskcol[i][j]>=d24['colored_integer_U1_mask'][i][j] for i in range(7) for j in range(10))
  results.append(dict(pair=pair,rank_up=P.matching_rank(maskup),
    rank_colored=P.matching_rank(maskcol),
    up_mask=maskup,colored_mask=maskcol,
    integer_charged_gauge_mononomial_witnesses=witnesses,
    rejected_reasons=dict(status),
    number_charged_gauge_monomials=len(witnesses)))
 hist={str(t):n for t,n in Counter((x['rank_up'],x['rank_colored']) for x in results).items()}
 return dict(status='PASS',all_order_charge_generator_count=7,
    source_singlet_pairs=pairs,
    rank_histogram_unbounded_integer_semigroup=hist,
    results=results,
    theorem='Exact unbounded nonnegative INTEGER semigroup feasibility across all 8×79 named pair/target charge equations, using the complete Pass11797 original hidden-SU2 support invariant ring: the five FI fields carry all nonzero support gauge charges, while old x,y,M meson generators are gauge-charge ZERO. Each augmented rational charge matrix has rank6, so an integer solution is a one-dimensional lattice coset b+k v. Bezout integrality and exact positivity intervals decide ALL insertion degrees, not only degree24.',
    physical_firewall='These are necessary U1 + hidden nonabelian singlet charged-monomial criteria. Addition of old neutral x,y,M may change orbifold R and fixed-point rules; coefficients, chiral and nonR string constraints, F-flatness and physical masses not established. Alternative support covariants not in Pass11797 invariant-ring presentation are not included.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_two_singlet_all_order_integer_semigroup.json').write_text(json.dumps(d,indent=2)+'\n')
 print('ALL ORDER INTEGER SINGLET',d['rank_histogram_unbounded_integer_semigroup'],
       [(x['pair'],x['number_charged_gauge_monomials']) for x in d['results']])
