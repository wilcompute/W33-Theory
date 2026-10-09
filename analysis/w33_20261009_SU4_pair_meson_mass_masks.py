"""Conservative exact-charge real-cone upper masks on all 30 parity-even
SU4 conjugate-pair extensions of the Pass11796 D-flat Higgs support.
A nonnegative pair-meson insertion must be matched for hidden SU4
in the explicitly aligned single/two-color Higgs configurations.
Solving LP in FI-core coordinates gives NECESSARY but not sufficient
all-order Yukawa and colored-vectorlike mass compatibility.
No claims about integer charge lattice, R rules or CFT amplitudes.
"""
from pathlib import Path
import gzip,json,sys
import numpy as np
import sympy as S
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
from w33_20261009_SU4_matched_Dflat_extensions import BASE
FI=['n_17','n_47','n_50','n_80','n_82']
BASIS=FI+['n_9','n_37','n_35']
def certificate():
  raw,prior,fields,support,charge=P.load()
  assert set(support)==set(BASE)
  basis=json.load(open(ROOT/'data/w33_pass11793_order_four_matter_action.json'))['candidate_three_family_Higgs_basis']
  orig=json.load(open(ROOT/'data/w33_pass11797_11801_five_physical_fronts.json'))['pass11799']
  cand=json.load(open(ROOT/'data/w33_20261009_SU4_matched_Dflat_extensions.json'))
  B=S.Matrix.hstack(*(S.Matrix(charge[x]) for x in BASIS))
  assert B.rank()==8
  # Get all 8 exact coordinates in one rational map, enforcing actual
  # 9d charge span via equality reconstruction.
  piv=list((B.T).rref()[1]);assert len(piv)==8
  inv=B.extract(piv,list(range(8))).inv()
  def co(names):
    rhs=-sum((S.Matrix(charge[n]) for n in names),S.zeros(9,1))
    coeff=inv*rhs.extract(piv,[0])
    return coeff if B*coeff==rhs else None
  def paircoords(f,a):
    z=co([f,a])
    assert z is not None
    return -z # Charge of positive meson insertion in the B coordinates
  def feasible(names,mesons):
    beta=co(names)
    if beta is None:return False,'outside_charge_span'
    if not mesons:
      return all(z>=0 for z in beta[:5]),'baseline'
    V=S.Matrix.hstack(*(paircoords(*p) for p in mesons))
    b=np.array([float(x) for x in beta[:5]])
    a=np.array([[float(V[i,j]) for j in range(len(mesons))] for i in range(5)])
    # beta - V*t >=0; each t>=0. Linear relaxation.
    res=linprog(np.zeros(len(mesons)),A_ub=a,b_ub=b,
         bounds=[(0,None)]*len(mesons),method='highs',options={'primal_feasibility_tolerance':1e-9,
             'dual_feasibility_tolerance':1e-9})
    return bool(res.success),'relaxed_pair_real_cone'
  down=orig['mass_sectors']['d']
  dd=down['rows'];db=down['columns']
  Q=basis['Q'];U=basis['u_c'];hu=basis['H_u'][0]
  baseline_up=[[int(feasible([q,u,hu],[])[0]) for u in U] for q in Q]
  baseline_d=[[int(feasible([a,b],[])[0]) for b in db] for a in dd]
  assert P.matching_rank(baseline_up)==1
  assert P.matching_rank(baseline_d)==5
  entries=[]
  def run(mesons,name):
    up=[[int(feasible([q,u,hu],mesons)[0]) for u in U] for q in Q]
    mass=[[int(feasible([a,b],mesons)[0]) for b in db] for a in dd]
    return dict(candidate=name,mesons=[list(x) for x in mesons],
       up_mask=up,up_relaxed_matching_rank=P.matching_rank(up),
       colored_mask=mass,colored_relaxed_matching_rank=P.matching_rank(mass),
       added_up_positions=[[i,j] for i in range(len(Q)) for j in range(len(U))
           if up[i][j] and not baseline_up[i][j]],
       added_colored_positions=sum(x and not y for ra,rb in zip(mass,baseline_d) for x,y in zip(ra,rb)))
  for item in cand['allowed_single_matched_SU4_pairs']:
    entries.append(run([(item['fundamental'],item['antifundamental'])],
             'one:'+item['fundamental']+'_'+item['antifundamental']))
  for item in cand['allowed_two_matched_SU4_pairs']:
    entries.append(run([tuple(item['first']),tuple(item['second'])],
             'two:'+item['first'][1]+'_'+item['second'][1]))
  assert len(entries)==30
  bestup=max(x['up_relaxed_matching_rank'] for x in entries)
  bestcolored=max(x['colored_relaxed_matching_rank'] for x in entries)
  from collections import Counter
  out=dict(status='PASS',candidates=30,original_up_rank=1,original_colored_rank=5,
      best_relaxed_up_rank=bestup,best_relaxed_colored_rank=bestcolored,
      rank_histogram={str(k):v for k,v in Counter((x['up_relaxed_matching_rank'],x['colored_relaxed_matching_rank']) for x in entries).items()},
      distinct_candidates=entries,
      criterion='For holomorphic SU4 singlets evaluated on aligned fundamental-antifundamental VEV pairs, a necessary condition is nonnegative real insertions of SU4 mesons F_i.A_i and the 13 original VEV fields. Five FI-core charges yield an exact linear inequality cone; scipy highs tests the <=2-dimensional real relaxation of those inequalities.',
      scope='Real cone ignores integrality, corrected R, nonR, fixed points, color contraction coefficient vanishings, and F-flatness. Thus matching ranks are UPPER bounds, never evidence that a Yukawa or exotic mass actually exists. No new global Dflat vacuum is proved beyond the prior local infinitesimal pair witness.')
  return out
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_SU4_pair_meson_mass_masks.json').write_text(json.dumps(d,indent=2)+'\n')
 print('SU4 PAIR MASKS',d['rank_histogram'],'BEST',d['best_relaxed_up_rank'],d['best_relaxed_colored_rank'])
