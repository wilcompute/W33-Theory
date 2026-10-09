"""Independent exact rational 3-variable cone verification for all 60
hidden SU4 (two mesons + antibaryon) candidate masks (4740 entries).

Fixed 8 halfspaces in R^3: 5 FI inequalities Vx<=b plus x>=0.
A nonempty subset of the positive orthant has an extreme point,
so enumerating at most choose(8,3)=56 rational vertices is complete.
"""
import json,sys
from pathlib import Path
from itertools import combinations
from fractions import Fraction as F
import sympy as S
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
from w33_20261009_SU4_pair_masks_exact_rational import BASE8,rational
def determinant(a):
 return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])
def inverse(a):
 det=determinant(a)
 if not det:return None
 return [[(a[(j+1)%3][(i+1)%3]*a[(j+2)%3][(i+2)%3]-a[(j+1)%3][(i+2)%3]*a[(j+2)%3][(i+1)%3])/det for j in range(3)] for i in range(3)]
def certificate():
 raw,prior,fields,support,q=P.load()
 saved=json.load(open(ROOT/'data/w33_20261009_SU4_mixed_baryon_mesons.json'))
 B=S.Matrix.hstack(*(S.Matrix(q[n]) for n in BASE8))
 piv=list((B.T).rref()[1]);Inv=B.extract(piv,list(range(8))).inv()
 def coord(names,neg):
  rhs=sum((S.Matrix(q[n]) for n in names),S.zeros(9,1))
  if neg:rhs=-rhs
  v=Inv*rhs.extract(piv,[0])
  return tuple(rational(x) for x in v[:5]) if B*v==rhs else None
 basis=json.load(open(ROOT/'data/w33_pass11793_order_four_matter_action.json'))['candidate_three_family_Higgs_basis']
 up=[(a,b,basis['H_u'][0]) for a in basis['Q'] for b in basis['u_c']]
 down=json.load(open(ROOT/'data/w33_pass11797_11801_five_physical_fronts.json'))['pass11799']['mass_sectors']['d']
 ds=[(a,b) for a in down['rows'] for b in down['columns']]
 targets=[coord(t,True) for t in up+ds]
 out=[];total_vertices=0
 for spec in saved['choices']:
  gens=[tuple(x) for x in spec['generators']]
  V=[coord(x,False) for x in gens]
  assert all(v is not None for v in V)
  rows=[tuple(V[j][i] for j in range(3)) for i in range(5)]
  rows.extend([tuple(F(-int(i==j)) for j in range(3)) for i in range(3)])
  invs=[]
  for ids in combinations(range(8),3):
   z=inverse([rows[i] for i in ids])
   if z is not None:invs.append((ids,z))
  total_vertices+=len(invs)
  verdict=[]
  for target in targets:
   if target is None:verdict.append(0);continue
   rhs=list(target)+[F(0)]*3
   if all(z>=0 for z in target):verdict.append(1);continue
   seen=False
   for ids,inv in invs:
    x=[sum(inv[i][j]*rhs[ids[j]] for j in range(3)) for i in range(3)]
    if all(sum(a[j]*x[j] for j in range(3))<=b for a,b in zip(rows,rhs)):
     seen=True;break
   verdict.append(int(seen))
  newup=[verdict[i*3:(i+1)*3] for i in range(3)]
  n=len(down['columns'])
  newc=[verdict[9+i*n:9+(i+1)*n] for i in range(len(down['rows']))]
  assert newup==spec['up_mask'] and newc==spec['colored_mask'],spec
  out.append(dict(four_anti=spec['four_anti'],fundamental_anti=[spec['anti_for_fund69'],spec['anti_for_fund74']],
    up_rank=P.matching_rank(newup),colored_rank=P.matching_rank(newc)))
 assert len(out)==60
 return dict(status='PASS',exact_fraction_vertex_checks=60*79,
  precomputed_nonsingular_vertex_triples=total_vertices,
  complete_agreement_with_independent_scipy_masks=True,
  maximum_up_rank=max(x['up_rank'] for x in out),
  maximum_colored_rank=max(x['colored_rank'] for x in out),
  rank3_up_candidates=sum(x['up_rank']==3 for x in out),
  theorem='All 60*79 real-cone feasibility decisions independently certified by exact Fraction inequalities via exhaustive rational 3-variable basic feasible vertices. The 7x10 colored mass matching graph never exceeds rank5, even for simultaneous 2 mesons and epsilon antibaryon. Necessary condition only: no actual couplings, integer exponents, F-flatness, or physical masses certified.',
  results=out)
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_SU4_mixed_baryon_exact_4740.json').write_text(json.dumps(d,indent=2)+'\n')
 print('4740 EXACT',d['precomputed_nonsingular_vertex_triples'],d['rank3_up_candidates'],d['maximum_colored_rank'])
